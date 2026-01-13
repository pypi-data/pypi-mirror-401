"""Supporting layer - routing and context assembly.

Components:
- Router: Model selection logic
- ContextAssembler: Prompt pack assembly
"""

from .router import Router, Task, RoutingDecision, TASK_TYPES
from .context import ContextAssembler, PromptPack

__all__ = [
    "Router",
    "Task",
    "RoutingDecision",
    "TASK_TYPES",
    "ContextAssembler",
    "PromptPack",
]
