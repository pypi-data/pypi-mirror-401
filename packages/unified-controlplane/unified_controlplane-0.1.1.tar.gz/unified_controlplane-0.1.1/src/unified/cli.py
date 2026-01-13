"""CLI for the AI Control Plane.

Usage:
    unified route "Generate unit tests" --type code --role lead
    unified status
    unified memory add --type decision --content "Using pytest"

Requires: click (pip install click)
"""

import sys
from datetime import datetime
from pathlib import Path
import uuid

import click


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AI Control Plane CLI."""
    pass


@cli.command()
@click.argument("intent")
@click.option("--type", "task_type", default="code", help="Task type (code, review, documentation, etc.)")
@click.option("--role", default="lead", help="Role (lead, reviewer, advisor)")
@click.option("--constraint", "-c", multiple=True, help="Constraints (low-cost, fast, high-accuracy)")
@click.option("--dry-run", is_flag=True, help="Show routing decision without executing")
def route(intent: str, task_type: str, role: str, constraint: tuple, dry_run: bool):
    """Route a task to the appropriate model.

    Example:
        unified route "Generate unit tests" --type code --role lead -c low-cost
    """
    from unified.core.registry import Registry
    from unified.paths import get_default_registry_path
    from unified.supporting.router import Router, Task

    # Load registry
    registry = Registry()
    try:
        registry.load(str(get_default_registry_path()))
    except (NotImplementedError, FileNotFoundError) as e:
        click.echo(f"Warning: {e}", err=True)

    # Create task
    try:
        task = Task(
            intent=intent,
            task_type=task_type,
            role=role,
            constraints=list(constraint),
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    # Route task
    router = Router(registry)
    decision = router.route(task)

    # Output
    click.echo(f"\n{'=' * 50}")
    click.echo(f"Task: {intent}")
    click.echo(f"Type: {task_type} | Role: {role}")
    if constraint:
        click.echo(f"Constraints: {', '.join(constraint)}")
    click.echo(f"{'=' * 50}")
    click.echo(f"\nRouting Decision:")
    click.echo(f"  Model: {decision.model}")
    click.echo(f"  Reason: {decision.reason}")
    click.echo(f"  Fallback: {decision.fallback or 'None'}")
    click.echo(f"  Parameters: {decision.parameters}")

    if dry_run:
        click.echo("\n[Dry run - no execution]")


@cli.command("dry-run")
@click.argument("intent")
@click.option("--type", "task_type", default="code", help="Task type (code, review, documentation, etc.)")
@click.option("--role", default="lead", help="Role (lead, reviewer, advisor)")
@click.option("--constraint", "-c", multiple=True, help="Constraints (low-cost, fast, high-accuracy)")
def dry_run(intent: str, task_type: str, role: str, constraint: tuple):
    """Run the full control plane loop with a mocked model response."""
    from unified.core.memory import Memory
    from unified.core.registry import Registry
    from unified.governance.audit import AuditLog
    from unified.governance.evaluator import EvalContext, Evaluator
    from unified.paths import (
        get_audit_dir,
        get_checklists_dir,
        get_default_registry_path,
        get_memory_dir,
        detect_project_name,
    )
    from unified.supporting.context import ContextAssembler
    from unified.supporting.router import Router, Task

    registry = Registry()
    registry.load(str(get_default_registry_path()))

    task = Task(
        intent=intent,
        task_type=task_type,
        role=role,
        constraints=list(constraint),
    )

    router = Router(registry)
    decision = router.route(task)

    audit_dir = get_audit_dir()
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit = AuditLog(str(audit_dir / "audit.jsonl"))
    audit.log_routing(task, decision)

    project = detect_project_name() or "default"
    memory_dir = get_memory_dir(project)
    memory_dir.mkdir(parents=True, exist_ok=True)
    memory = Memory(str(memory_dir))
    assembler = ContextAssembler(registry, memory)
    prompt_pack = assembler.assemble(task)

    mock_output = f"[MOCK OUTPUT] Task: {task.intent}"

    evaluator = Evaluator(str(get_checklists_dir()), audit_log=audit)
    eval_context = EvalContext(
        task_type=task.task_type,
        task_brief=task.intent,
        model_used=decision.model,
        checklists=[],
    )
    verdict = evaluator.evaluate(mock_output, eval_context)

    click.echo("\n=== Dry Run Summary ===\n")
    click.echo(f"Task: {task.intent}")
    click.echo(f"Model: {decision.model} (fallback: {decision.fallback or 'None'})")
    click.echo("\nPrompt Pack:")
    click.echo(f"- System: {prompt_pack.system_prompt}")
    click.echo(f"- Context: {prompt_pack.context or '[none]'}")
    click.echo(f"- Checklist: {prompt_pack.checklist_summary}")
    click.echo("\nMock Output:")
    click.echo(mock_output)
    click.echo("\nVerdict:")
    click.echo(f"- PASS: {verdict.passed}")
    click.echo(f"- Results: {len(verdict.results)} checks")


@cli.command()
@click.argument("intent")
@click.option("--type", "task_type", default="code", help="Task type (code, review, documentation, etc.)")
@click.option("--role", default="lead", help="Role (lead, reviewer, advisor)")
@click.option("--constraint", "-c", multiple=True, help="Constraints (low-cost, fast, high-accuracy)")
@click.option("--model", "model_name", default=None, help="Override model name from registry")
def run(intent: str, task_type: str, role: str, constraint: tuple, model_name: str | None):
    """Run the full control plane loop with real model output."""
    from unified.core.memory import Memory
    from unified.core.registry import Registry
    from unified.governance.audit import AuditLog
    from unified.governance.evaluator import EvalContext, Evaluator
    from unified.models import get_adapter
    from unified.paths import (
        get_audit_dir,
        get_checklists_dir,
        get_default_registry_path,
        get_memory_dir,
        detect_project_name,
    )
    from unified.supporting.context import ContextAssembler
    from unified.supporting.router import Router, Task

    registry = Registry()
    registry.load(str(get_default_registry_path()))

    task = Task(
        intent=intent,
        task_type=task_type,
        role=role,
        constraints=list(constraint),
    )

    router = Router(registry)
    decision = router.route(task)
    if model_name:
        decision.model = model_name
        decision.reason = "Model override"

    model_config = registry.get_model(decision.model)
    if model_config is None:
        available = ", ".join(m.name for m in registry.list_models())
        click.echo(
            f"Error: Model '{decision.model}' not in registry. Available: {available}",
            err=True,
        )
        sys.exit(1)

    try:
        adapter = get_adapter(model_config)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if not adapter.health_check():
        click.echo(
            f"Error: {model_config.name} is not available. Check model or API key.",
            err=True,
        )
        sys.exit(1)

    audit_dir = get_audit_dir()
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit = AuditLog(str(audit_dir / "audit.jsonl"))
    audit.log_routing(task, decision)

    project = detect_project_name() or "default"
    memory_dir = get_memory_dir(project)
    memory_dir.mkdir(parents=True, exist_ok=True)
    memory = Memory(str(memory_dir))
    assembler = ContextAssembler(registry, memory)
    prompt_pack = assembler.assemble(task)
    messages = prompt_pack.to_messages()

    response = adapter.generate(messages)
    if response.error:
        audit.log_event(
            "error",
            {"model": model_config.name, "error": response.error},
        )
        click.echo(f"Error: {response.error}", err=True)
        sys.exit(1)

    evaluator = Evaluator(str(get_checklists_dir()), audit_log=audit)
    eval_context = EvalContext(
        task_type=task.task_type,
        task_brief=task.intent,
        model_used=response.model,
        checklists=[],
    )
    verdict = evaluator.evaluate(response.content, eval_context)

    click.echo("\n=== Run Result ===\n")
    click.echo(f"Model: {response.model}")
    click.echo(f"Routing reason: {decision.reason}")
    click.echo("\nOutput:\n")
    click.echo(response.content)
    click.echo("\nVerdict:")
    click.echo(f"- PASS: {verdict.passed}")
    if verdict.blocking_issues:
        click.echo("\nBlocking Issues:")
        for issue in verdict.blocking_issues:
            click.echo(f"- {issue}")
    if verdict.warnings:
        click.echo("\nWarnings:")
        for warning in verdict.warnings:
            click.echo(f"- {warning}")
    if verdict.suggestions:
        click.echo("\nSuggestions:")
        for suggestion in verdict.suggestions:
            click.echo(f"- {suggestion}")


@cli.command()
@click.option("--check-health", is_flag=True, help="Check model availability (may be slow)")
def status(check_health: bool):
    """Show control plane status.

    Displays registry info, memory stats, and recent audit entries.
    """
    from unified.core.memory import Memory
    from unified.core.registry import Registry
    from unified.models import get_adapter
    from unified.paths import (
        get_audit_dir,
        get_default_registry_path,
        get_memory_dir,
        get_unified_home,
        detect_project_name,
    )

    click.echo("\n=== AI Control Plane Status ===\n")
    click.echo(f"Home: {get_unified_home()}")

    # Registry status
    click.echo("\nRegistry:")
    registry = Registry()
    models = []
    try:
        registry.load(str(get_default_registry_path()))
        models = registry.list_models()
        tools = registry.list_tools()
        skills = registry.list_skills()
        click.echo(f"  Models: {len(models)}")
        for m in models:
            adapter_status = f"[{m.adapter}]" if m.adapter else "[no adapter]"
            click.echo(f"    - {m.name} ({m.provider}) {adapter_status}")
        click.echo(f"  Tools: {len(tools)}")
        for t in tools:
            click.echo(f"    - {t.name}: {t.description}")
        click.echo(f"  Skills: {len(skills)}")
        for s in skills:
            click.echo(f"    - {s.name}: {s.description}")
    except FileNotFoundError as e:
        click.echo(f"  Status: {e}")

    # Memory status
    project = detect_project_name() or "default"
    click.echo(f"\nMemory (project: {project}):")
    memory_dir = get_memory_dir(project)
    if memory_dir.exists():
        memory = Memory(str(memory_dir))
        try:
            decisions = memory.list_by_type("decision")
            patterns = memory.list_by_type("pattern")
            findings = memory.list_by_type("finding")
            contexts = memory.list_by_type("context")
            total = len(decisions) + len(patterns) + len(findings) + len(contexts)
            click.echo(f"  Total entries: {total}")
            click.echo(f"    - Decisions: {len(decisions)}")
            click.echo(f"    - Patterns: {len(patterns)}")
            click.echo(f"    - Findings: {len(findings)}")
            click.echo(f"    - Context: {len(contexts)}")
        except Exception as e:
            click.echo(f"  Status: Error reading memory ({e})")
    else:
        click.echo("  Status: No memory directory yet")

    # Audit status
    click.echo("\nAudit Log:")
    audit_path = get_audit_dir() / "audit.jsonl"
    if audit_path.exists():
        line_count = sum(1 for _ in open(audit_path))
        click.echo(f"  Entries: {line_count}")
        click.echo(f"  Path: {audit_path}")
    else:
        click.echo("  Status: No audit log yet")

    # Model health checks (optional)
    if check_health and models:
        click.echo("\nModel Health:")
        for m in models:
            if m.adapter:
                try:
                    adapter = get_adapter(m)
                    healthy = adapter.health_check()
                    status_str = "OK" if healthy else "UNAVAILABLE"
                    click.echo(f"  {m.name}: {status_str}")
                except Exception as e:
                    click.echo(f"  {m.name}: ERROR ({e})")
            else:
                click.echo(f"  {m.name}: [no adapter configured]")


@cli.command("config-validate")
@click.option("--path", "config_path", default=None, help="Path to registry.yaml")
def config_validate(config_path: str | None):
    """Validate registry configuration."""
    from unified.core.registry import Registry
    from unified.paths import get_default_registry_path

    if config_path is None:
        config_path = str(get_default_registry_path())

    registry = Registry()
    try:
        registry.load(config_path)
    except (FileNotFoundError, ValueError) as exc:
        click.echo(f"Config error: {exc}", err=True)
        sys.exit(1)

    click.echo(f"Registry config OK: {config_path}")
    click.echo(f"- Models: {len(registry.list_models())}")
    click.echo(f"- Tools: {len(registry.list_tools())}")
    click.echo(f"- Skills: {len(registry.list_skills())}")


@cli.command()
@click.option("--file", "file_path", type=click.Path(exists=True), help="Path to file to evaluate")
@click.option("--task-type", default="code", help="Task type (code, review, documentation, etc.)")
@click.option("--task-brief", default="", help="Short task brief for alignment checks")
@click.option("--model", default="mock-model", help="Model name used for output")
@click.option("--checklist", "-c", multiple=True, help="Checklist name (without .md)")
def evaluate(file_path: str | None, task_type: str, task_brief: str, model: str, checklist: tuple):
    """Evaluate output against checklists.

    Examples:
        unified evaluate --file output.md --task-type documentation --task-brief "Draft spec"
        unified evaluate --file output.md -c ai_output_review -c code_review
    """
    from unified.governance.audit import AuditLog
    from unified.governance.evaluator import EvalContext, Evaluator
    from unified.paths import get_audit_dir, get_checklists_dir

    if file_path:
        with open(file_path) as f:
            output = f.read()
    else:
        output = sys.stdin.read()
        if not output.strip():
            click.echo("Error: Provide --file or pipe content via stdin.", err=True)
            sys.exit(1)

    audit_dir = get_audit_dir()
    audit_dir.mkdir(parents=True, exist_ok=True)

    evaluator = Evaluator(str(get_checklists_dir()), audit_log=AuditLog(str(audit_dir / "audit.jsonl")))
    eval_context = EvalContext(
        task_type=task_type,
        task_brief=task_brief or "N/A",
        model_used=model,
        checklists=list(checklist),
    )
    verdict = evaluator.evaluate(output, eval_context)

    click.echo("\n=== Evaluation Verdict ===\n")
    click.echo(f"PASS: {verdict.passed}")
    if verdict.blocking_issues:
        click.echo("\nBlocking Issues:")
        for issue in verdict.blocking_issues:
            click.echo(f"- {issue}")
    if verdict.warnings:
        click.echo("\nWarnings:")
        for warning in verdict.warnings:
            click.echo(f"- {warning}")
    if verdict.suggestions:
        click.echo("\nSuggestions:")
        for suggestion in verdict.suggestions:
            click.echo(f"- {suggestion}")
    click.echo(f"\nChecks: {len(verdict.results)} items evaluated")


@cli.command()
@click.argument("checklist")
def check(checklist: str):
    """Load and display a checklist.

    Example:
        unified check ai_output_review
    """
    from unified.governance.evaluator import Evaluator
    from unified.paths import get_checklists_dir

    evaluator = Evaluator(str(get_checklists_dir()))
    try:
        cl = evaluator.load_checklist(checklist)
        click.echo(f"\nChecklist: {cl.name}")
        for item in cl.items:
            click.echo(f"  [{item.severity}] {item.id}: {item.description}")
    except NotImplementedError:
        click.echo("Warning: Checklist loading not implemented", err=True)
        click.echo(f"Would load: {get_checklists_dir()}/{checklist}.md")


# ============================================================================
# Memory subcommands
# ============================================================================


@cli.group()
def memory():
    """Manage project memory (decisions, patterns, findings)."""
    pass


@memory.command("add")
@click.option("--type", "entry_type", required=True,
              type=click.Choice(["decision", "pattern", "finding", "context"]))
@click.option("--content", required=True, help="Content to store")
@click.option("--project", default=None, help="Project namespace (auto-detected if not specified)")
@click.option("--tags", default="", help="Comma-separated tags")
def memory_add(entry_type: str, content: str, project: str | None, tags: str):
    """Add an entry to project memory."""
    from unified.core.memory import Memory, MemoryEntry
    from unified.paths import get_memory_dir, detect_project_name

    project = project or detect_project_name() or "default"
    memory_dir = get_memory_dir(project)
    memory_dir.mkdir(parents=True, exist_ok=True)

    mem = Memory(str(memory_dir))
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

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
        tags=tag_list,
    )
    entry_id = mem.store(entry)

    click.echo(f"Added {entry_type} to project '{project}': {entry_id}")


@memory.command("list")
@click.option("--type", "entry_type", default=None,
              type=click.Choice(["decision", "pattern", "finding", "context"]))
@click.option("--project", default=None, help="Project namespace")
def memory_list(entry_type: str | None, project: str | None):
    """List memory entries."""
    from unified.core.memory import Memory
    from unified.paths import get_memory_dir, detect_project_name

    project = project or detect_project_name() or "default"
    memory_dir = get_memory_dir(project)

    if not memory_dir.exists():
        click.echo(f"No memory found for project '{project}'")
        return

    mem = Memory(str(memory_dir))

    types = [entry_type] if entry_type else ["decision", "pattern", "finding", "context"]
    found_any = False
    for t in types:
        entries = mem.list_by_type(t)
        if entries:
            found_any = True
            click.echo(f"\n{t.upper()}S ({len(entries)}):")
            for entry in entries:
                preview = entry.content[:60].replace("\n", " ")
                click.echo(f"  [{entry.id[:12]}] {preview}...")

    if not found_any:
        click.echo(f"No entries found for project '{project}'")


@memory.command("search")
@click.argument("query")
@click.option("--type", "entry_type", default=None,
              type=click.Choice(["decision", "pattern", "finding", "context"]))
@click.option("--project", default=None, help="Project namespace")
def memory_search(query: str, entry_type: str | None, project: str | None):
    """Search memory entries."""
    from unified.core.memory import Memory
    from unified.paths import get_memory_dir, detect_project_name

    project = project or detect_project_name() or "default"
    memory_dir = get_memory_dir(project)

    if not memory_dir.exists():
        click.echo(f"No memory found for project '{project}'")
        return

    mem = Memory(str(memory_dir))
    entries = mem.search(query, entry_type=entry_type)

    if not entries:
        click.echo("No matches.")
        return

    click.echo(f"\nSearch results for '{query}':\n")
    for entry in entries:
        click.echo(f"[{entry.id[:12]}] {entry.title} ({entry.type})")


def main():
    """Entry point."""
    cli()


if __name__ == "__main__":
    main()
