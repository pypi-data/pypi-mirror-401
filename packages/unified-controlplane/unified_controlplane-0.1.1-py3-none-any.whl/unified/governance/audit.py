"""AuditLog - Runtime event logging.

Append-only log of routing decisions, evaluations, and other runtime events.

See docs/control_plane_spec.md Section 3.6 for details.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json


@dataclass
class AuditEntry:
    """A single audit log entry."""

    timestamp: datetime
    type: str  # "routing", "evaluation", "error", "info"
    data: dict

    def to_json(self) -> str:
        """Convert to JSON line."""
        return json.dumps(
            {
                "timestamp": self.timestamp.isoformat(),
                "type": self.type,
                **self.data,
            }
        )


class AuditLog:
    """Append-only audit log for runtime events.

    Usage:
        audit = AuditLog("audit/audit.jsonl")
        audit.log_routing(task, decision)
        audit.log_evaluation(context, verdict)
    """

    def __init__(self, path: str = "audit/audit.jsonl"):
        self.path = Path(path)
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Create audit directory if needed."""
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _append(self, entry: AuditEntry) -> None:
        """Append an entry to the log file."""
        with open(self.path, "a") as f:
            f.write(entry.to_json() + "\n")

    def log_routing(self, task: "Task", decision: "RoutingDecision") -> None:
        """Log a routing decision.

        Args:
            task: The task being routed
            decision: The routing decision made
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            type="routing",
            data={
                "task_intent": task.intent,
                "task_type": task.task_type,
                "model": decision.model,
                "reason": decision.reason,
                "fallback": decision.fallback,
            },
        )
        self._append(entry)

    def log_evaluation(self, context: "EvalContext", verdict: "Verdict") -> None:
        """Log an evaluation result.

        Args:
            context: The evaluation context
            verdict: The evaluation verdict
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            type="evaluation",
            data={
                "model_used": context.model_used,
                "passed": verdict.passed,
                "blocking_issues": verdict.blocking_issues,
                "warnings": verdict.warnings,
            },
        )
        self._append(entry)

    def log_event(self, event_type: str, data: dict) -> None:
        """Log a generic event.

        Args:
            event_type: Type of event (e.g., "error", "info")
            data: Event-specific data
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            type=event_type,
            data=data,
        )
        self._append(entry)

    def query(self, filters: dict | None = None, limit: int = 100) -> list[AuditEntry]:
        """Query audit entries.

        Args:
            filters: Optional filters (e.g., {"type": "routing"})
            limit: Maximum entries to return

        Returns:
            List of matching AuditEntry objects, most recent first
        """
        if not self.path.exists():
            return []

        entries = []
        with open(self.path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    entry_type = data.pop("type", "unknown")
                    timestamp_str = data.pop("timestamp", None)
                    timestamp = (
                        datetime.fromisoformat(timestamp_str)
                        if timestamp_str
                        else datetime.now()
                    )
                    entry = AuditEntry(timestamp=timestamp, type=entry_type, data=data)

                    # Apply filters
                    if filters:
                        match = True
                        if "type" in filters and entry.type != filters["type"]:
                            match = False
                        if match:
                            entries.append(entry)
                    else:
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue

        # Return most recent first, limited
        return list(reversed(entries))[:limit]


# Type hints for forward references
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..supporting.router import Task, RoutingDecision
    from .evaluator import EvalContext, Verdict
