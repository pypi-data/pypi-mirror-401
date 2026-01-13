"""Shared service functions for unified control plane.

These functions contain the core logic used by CLI commands, interactive mode,
and the web dashboard. They return data structures rather than printing output,
allowing callers to format results appropriately.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import uuid

from unified.core.memory import Memory, MemoryEntry
from unified.core.registry import Registry
from unified.paths import (
    get_audit_dir,
    get_checklists_dir,
    get_default_registry_path,
    get_memory_dir,
    get_unified_home,
    detect_project_name,
)
from unified.supporting.router import Router, Task, RoutingDecision


@dataclass
class StatusResult:
    """Result from status check."""
    home: Path
    models: list
    tools: list
    skills: list
    project: str
    memory_counts: dict  # {type: count}
    audit_entries: int
    registry_error: str | None = None
    memory_error: str | None = None
    model_health: dict | None = None  # {model_name: bool}


@dataclass
class RouteResult:
    """Result from routing a task."""
    model: str
    reason: str
    fallback: str | None
    parameters: dict
    task_intent: str
    task_type: str
    role: str
    constraints: list


def get_status(check_health: bool = False) -> StatusResult:
    """Get control plane status.

    Args:
        check_health: If True, check model availability (may be slow).

    Returns:
        StatusResult with registry, memory, and audit information.
    """
    from unified.models import get_adapter

    home = get_unified_home()

    # Registry
    registry = Registry()
    models = []
    tools = []
    skills = []
    registry_error = None

    try:
        registry.load(str(get_default_registry_path()))
        models = registry.list_models()
        tools = registry.list_tools()
        skills = registry.list_skills()
    except FileNotFoundError as e:
        registry_error = str(e)

    # Memory
    project = detect_project_name() or "default"
    memory_dir = get_memory_dir(project)
    memory_counts = {}
    memory_error = None

    if memory_dir.exists():
        try:
            mem = Memory(str(memory_dir))
            for entry_type in ["decision", "pattern", "finding", "context"]:
                memory_counts[entry_type] = len(mem.list_by_type(entry_type))
        except Exception as e:
            memory_error = str(e)

    # Audit
    audit_path = get_audit_dir() / "audit.jsonl"
    audit_entries = 0
    if audit_path.exists():
        audit_entries = sum(1 for _ in open(audit_path))

    # Model health checks (optional)
    model_health = None
    if check_health and models:
        model_health = {}
        for m in models:
            if m.adapter:
                try:
                    adapter = get_adapter(m)
                    model_health[m.name] = adapter.health_check()
                except Exception:
                    model_health[m.name] = False
            else:
                model_health[m.name] = None  # No adapter configured

    return StatusResult(
        home=home,
        models=models,
        tools=tools,
        skills=skills,
        project=project,
        memory_counts=memory_counts,
        audit_entries=audit_entries,
        registry_error=registry_error,
        memory_error=memory_error,
        model_health=model_health,
    )


def route_task(
    intent: str,
    task_type: str = "code",
    role: str = "lead",
    constraints: list | None = None,
) -> RouteResult:
    """Route a task to the appropriate model.

    Args:
        intent: Task description
        task_type: Type of task (code, review, documentation, etc.)
        role: Role (lead, reviewer, advisor)
        constraints: Optional constraints (low-cost, fast, high-accuracy)

    Returns:
        RouteResult with routing decision.

    Raises:
        ValueError: If task parameters are invalid.
        FileNotFoundError: If registry not found.
    """
    constraints = constraints or []

    registry = Registry()
    registry.load(str(get_default_registry_path()))

    task = Task(
        intent=intent,
        task_type=task_type,
        role=role,
        constraints=constraints,
    )

    router = Router(registry)
    decision = router.route(task)

    return RouteResult(
        model=decision.model,
        reason=decision.reason,
        fallback=decision.fallback,
        parameters=decision.parameters,
        task_intent=intent,
        task_type=task_type,
        role=role,
        constraints=constraints,
    )


def add_memory(
    entry_type: str,
    content: str,
    project: str | None = None,
    tags: list | None = None,
) -> str:
    """Add an entry to project memory.

    Args:
        entry_type: Type of entry (decision, pattern, finding, context)
        content: Content to store
        project: Project namespace (auto-detected if not specified)
        tags: Optional list of tags

    Returns:
        Entry ID of the created memory entry.
    """
    project = project or detect_project_name() or "default"
    tags = tags or []

    memory_dir = get_memory_dir(project)
    memory_dir.mkdir(parents=True, exist_ok=True)

    mem = Memory(str(memory_dir))

    prefix_map = {
        "decision": "dec_",
        "pattern": "pat_",
        "finding": "find_",
        "context": "ctx_",
    }
    stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    entry_id = f"{prefix_map[entry_type]}{stamp}_{uuid.uuid4().hex[:8]}"
    title = content.splitlines()[0][:80] if content else f"{entry_type} entry"

    entry = MemoryEntry(
        id=entry_id,
        type=entry_type,
        timestamp=datetime.utcnow(),
        project=project,
        title=title,
        content=content,
        tags=tags,
    )
    return mem.store(entry)


def list_memory(
    entry_type: str | None = None,
    project: str | None = None,
) -> dict[str, list[MemoryEntry]]:
    """List memory entries.

    Args:
        entry_type: Optional filter by type
        project: Project namespace (auto-detected if not specified)

    Returns:
        Dict mapping entry type to list of entries.
    """
    project = project or detect_project_name() or "default"
    memory_dir = get_memory_dir(project)

    if not memory_dir.exists():
        return {}

    mem = Memory(str(memory_dir))
    types = [entry_type] if entry_type else ["decision", "pattern", "finding", "context"]

    result = {}
    for t in types:
        entries = mem.list_by_type(t)
        if entries:
            result[t] = entries

    return result


def search_memory(
    query: str,
    entry_type: str | None = None,
    project: str | None = None,
) -> list[MemoryEntry]:
    """Search memory entries.

    Args:
        query: Search query
        entry_type: Optional filter by type
        project: Project namespace (auto-detected if not specified)

    Returns:
        List of matching memory entries.
    """
    project = project or detect_project_name() or "default"
    memory_dir = get_memory_dir(project)

    if not memory_dir.exists():
        return []

    mem = Memory(str(memory_dir))
    return mem.search(query, entry_type=entry_type)
