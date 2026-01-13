"""Router - Model selection logic.

Selects the right model for a task based on constraints, role, and availability.
Uses two-pass evaluation: constraints first, then role-based defaults.

See docs/control_plane_spec.md Section 3.2 for details.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.registry import Registry

# Standardized task types
TASK_TYPES = [
    "code",  # Code generation, modification
    "review",  # Code or document review
    "documentation",  # Docs, specs, READMEs
    "architecture",  # Design decisions, structure
    "analysis",  # Research, investigation
]

MODEL_ALIASES = {
    "claude": "claude-sonnet",
}

CAPABILITIES_BY_TASK = {
    "code": ["code"],
    "review": ["review"],
    "documentation": ["documentation"],
    "architecture": ["reasoning"],
    "analysis": ["reasoning"],
}


@dataclass
class Task:
    """A unit of work to be routed."""

    intent: str  # What needs to be done
    task_type: str  # One of TASK_TYPES
    role: str  # "lead", "reviewer", "advisor"
    constraints: list[str] = field(default_factory=list)  # ["low-cost", "fast", etc.]

    def __post_init__(self):
        if self.task_type not in TASK_TYPES:
            raise ValueError(f"Invalid task_type: {self.task_type}")
        if self.role not in ["lead", "reviewer", "advisor"]:
            raise ValueError(f"Invalid role: {self.role}")


@dataclass
class RoutingDecision:
    """Result of routing a task."""

    model: str  # Selected model name
    reason: str  # Why this model was chosen
    fallback: str | None = None  # Backup if primary unavailable
    parameters: dict = field(default_factory=dict)  # temperature, max_tokens, etc.


class Router:
    """Selects the right model for a task.

    Uses two-pass evaluation:
    1. Constraint overrides (highest priority)
    2. Role-based defaults

    Usage:
        router = Router(registry)
        decision = router.route(task)
    """

    def __init__(self, registry: "Registry"):
        self.registry = registry

    def route(self, task: Task) -> RoutingDecision:
        """Select model(s) for a task.

        Args:
            task: The task to route

        Returns:
            RoutingDecision with selected model and reasoning
        """
        # Pass 1: Check constraint overrides (highest priority)
        if "low-cost" in task.constraints:
            decision = RoutingDecision(
                model="ollama-llama3",
                reason="Low-cost constraint: using local model",
                fallback="codex",
                parameters={"temperature": 0.2},
            )
            return self._ensure_capability(task, decision)
        if "high-accuracy" in task.constraints:
            decision = RoutingDecision(
                model="claude",
                reason="High-accuracy constraint",
                fallback="codex",
                parameters={"temperature": 0.1},
            )
            return self._ensure_capability(task, decision)
        if "fast" in task.constraints:
            decision = RoutingDecision(
                model="ollama-llama3",
                reason="Speed constraint: using local model",
                fallback="claude",
                parameters={"temperature": 0.2},
            )
            return self._ensure_capability(task, decision)

        # Pass 2: Apply role-based defaults (if no constraint matched)
        if task.role == "lead" and task.task_type == "code":
            decision = RoutingDecision(
                model="codex",
                reason="Lead code task",
                fallback="claude",
                parameters={"temperature": 0.2},
            )
            return self._ensure_capability(task, decision)
        if task.role == "lead" and task.task_type == "documentation":
            decision = RoutingDecision(
                model="claude",
                reason="Lead documentation task",
                fallback="codex",
                parameters={"temperature": 0.3},
            )
            return self._ensure_capability(task, decision)
        if task.role == "reviewer":
            decision = RoutingDecision(
                model="claude",
                reason="Reviewer role",
                fallback="codex",
                parameters={"temperature": 0.1},
            )
            return self._ensure_capability(task, decision)

        # Fallback default (catches advisor role, unknown task types, etc.)
        decision = RoutingDecision(
            model="claude",
            reason="Default fallback",
            fallback="ollama-llama3",
            parameters={"temperature": 0.2},
        )
        return self._ensure_capability(task, decision)

    def check_availability(self, model_name: str) -> bool:
        """Check if a model is registered (registry-only check).

        For actual health checks (network connectivity, API availability),
        use adapter.health_check() directly in the run command.

        Args:
            model_name: Name of the model to check

        Returns:
            True if model exists in registry, False otherwise
        """
        model = self.registry.get_model(model_name)
        return model is not None

    def get_fallback(self, model_name: str) -> str | None:
        """Get fallback model if primary is unavailable."""
        fallback_chain = {
            "codex": "claude",
            "claude": "ollama-llama3",
            "ollama-llama3": "claude",
        }
        return fallback_chain.get(model_name)

    def _ensure_capability(self, task: Task, decision: RoutingDecision) -> RoutingDecision:
        """Ensure selected model supports required capabilities."""
        required = CAPABILITIES_BY_TASK.get(task.task_type, [])
        if not required:
            return decision

        decision.model = self._resolve_model_name(decision.model)
        if decision.fallback:
            decision.fallback = self._resolve_model_name(decision.fallback)

        if self._model_supports(decision.model, required):
            return decision

        if decision.fallback and self._model_supports(decision.fallback, required):
            decision.model = decision.fallback
            return decision

        candidate = self._pick_candidate(required, task.constraints)
        if candidate is not None:
            decision.model = candidate
        return decision

    def _resolve_model_name(self, model_name: str) -> str:
        """Resolve model alias to registry name when possible."""
        if self.registry.get_model(model_name) is not None:
            return model_name
        alias = MODEL_ALIASES.get(model_name)
        if alias and self.registry.get_model(alias) is not None:
            return alias
        return model_name

    def _model_supports(self, model_name: str, required: list[str]) -> bool:
        """Check if model supports required capabilities."""
        model = self.registry.get_model(model_name)
        if model is None:
            return False
        return all(cap in model.capabilities for cap in required)

    def _pick_candidate(self, required: list[str], constraints: list[str]) -> str | None:
        """Pick a registry model that supports required capabilities."""
        candidates = self.registry.list_models({"capabilities": required})
        if not candidates:
            return None
        if "low-cost" in constraints or "fast" in constraints:
            local = [m for m in candidates if m.is_local]
            if local:
                return local[0].name
        return candidates[0].name
