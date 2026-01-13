"""Evaluator - Quality gates and checklist runner.

Validates model outputs against checklists and produces structured verdicts.

See docs/control_plane_spec.md Section 3.4 for details.
"""

from dataclasses import dataclass, field
from pathlib import Path
import re
import sys


@dataclass
class EvalContext:
    """Context for evaluation."""

    task_type: str  # "code", "review", "documentation", etc.
    task_brief: str  # Original task description
    model_used: str  # Which model generated the output
    checklists: list[str]  # Which checklists to apply


@dataclass
class ChecklistItem:
    """A single checklist item."""

    id: str  # Auto-generated, e.g., "ai_01"
    description: str
    severity: str = "blocking"  # "blocking" or "warning"


@dataclass
class CheckResult:
    """Result of checking a single item."""

    item_id: str  # Reference to ChecklistItem.id
    passed: bool
    notes: str | None = None


@dataclass
class Verdict:
    """Evaluation verdict."""

    passed: bool  # Overall PASS/FAIL
    results: list[CheckResult] = field(default_factory=list)
    blocking_issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "passed": self.passed,
            "results": [
                {"item_id": r.item_id, "passed": r.passed, "notes": r.notes}
                for r in self.results
            ],
            "blocking_issues": self.blocking_issues,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
        }


@dataclass
class Checklist:
    """A parsed checklist."""

    name: str
    items: list[ChecklistItem] = field(default_factory=list)


class Evaluator:
    """Validates model outputs against quality criteria.

    Usage:
        evaluator = Evaluator("checklists/", audit_log)
        verdict = evaluator.evaluate(output, context)
    """

    def __init__(self, checklists_dir: str, audit_log: "AuditLog | None" = None):
        self.checklists_dir = Path(checklists_dir)
        self.audit_log = audit_log
        self._checklists: dict[str, Checklist] = {}

    def load_checklist(self, name: str) -> Checklist:
        """Load and parse a checklist by name.

        Args:
            name: Checklist name (e.g., "ai_output_review")

        Returns:
            Parsed Checklist object

        """
        if name in self._checklists:
            return self._checklists[name]
        path = self.checklists_dir / f"{name}.md"
        if not path.exists():
            raise FileNotFoundError(f"Checklist not found: {path}")

        items: list[ChecklistItem] = []
        prefix = name.split("_", maxsplit=1)[0]
        pattern = re.compile(r"^- \[(?: |x|X)\]\s+(.*)$")
        index = 1

        with open(path) as f:
            for line in f:
                match = pattern.match(line.strip())
                if not match:
                    continue
                description = match.group(1).strip()
                severity = "blocking"
                if description.endswith("(warning)"):
                    severity = "warning"
                    description = description[: -len("(warning)")].strip()
                item_id = f"{prefix}_{index:02d}"
                items.append(
                    ChecklistItem(
                        id=item_id,
                        description=description,
                        severity=severity,
                    )
                )
                index += 1

        checklist = Checklist(name=name, items=items)
        self._checklists[name] = checklist
        return checklist

    def get_applicable_checklists(self, task_type: str) -> list[str]:
        """Determine which checklists apply to a task type.

        Returns checklist names based on task type. Add new checklists
        to checklists/ directory and update mapping as needed.
        """
        mapping = {
            "code": ["ai_output_review", "code_review"],
            "documentation": ["ai_output_review"],
            "architecture": ["ai_output_review", "architecture_review"],
            "review": ["ai_output_review"],
            "analysis": ["ai_output_review"],
        }
        return mapping.get(task_type, ["ai_output_review"])

    def evaluate(self, output: str, context: EvalContext) -> Verdict:
        """Evaluate output against applicable checklists.

        Args:
            output: The generated output to evaluate
            context: Evaluation context with task info and checklists

        Returns:
            Verdict with PASS/FAIL and details

        """
        checklist_names = context.checklists or self.get_applicable_checklists(
            context.task_type
        )

        results: list[CheckResult] = []
        blocking_issues: list[str] = []
        warnings: list[str] = []
        suggestions: list[str] = []

        for name in checklist_names:
            checklist = self.load_checklist(name)
            for item in checklist.items:
                passed, notes, suggestion = self._evaluate_item(
                    item=item,
                    output=output,
                    context=context,
                )
                results.append(
                    CheckResult(item_id=item.id, passed=passed, notes=notes)
                )
                if not passed:
                    issue = notes or item.description
                    if item.severity == "warning":
                        warnings.append(issue)
                    else:
                        blocking_issues.append(issue)
                if suggestion:
                    suggestions.append(suggestion)

        verdict = Verdict(
            passed=len(blocking_issues) == 0,
            results=results,
            blocking_issues=blocking_issues,
            warnings=warnings,
            suggestions=suggestions,
        )

        if self.audit_log is not None:
            self.audit_log.log_evaluation(context, verdict)

        return verdict

    def _evaluate_item(
        self, item: ChecklistItem, output: str, context: EvalContext
    ) -> tuple[bool, str | None, str | None]:
        """Evaluate a single checklist item against output."""
        text = output or ""
        output_lower = text.lower()
        desc = item.description.lower()

        if not text.strip():
            return False, "Output is empty", "Provide output for evaluation"

        if "hardcoded secrets" in desc or "credentials" in desc:
            match = _SECRET_REGEX.search(text)
            if match:
                return (
                    False,
                    f"Possible secret detected: {match.group(0)}",
                    "Remove secrets and use environment variables or placeholders",
                )
            return True, None, None

        if "hallucinated" in desc or "dependencies" in desc or "files" in desc:
            missing_imports = _find_missing_imports(text)
            missing_paths = _find_missing_files(text)
            issues = []
            if missing_imports:
                issues.append(f"Unrecognized imports: {', '.join(missing_imports)}")
            if missing_paths:
                issues.append(f"Missing file references: {', '.join(missing_paths)}")
            if issues:
                return (
                    False,
                    "; ".join(issues),
                    "Verify imports and file references or update the project files",
                )
            return True, None, None

        if "reviewer verdict" in desc or "pass/fail" in desc:
            has_verdict = re.search(r"\b(PASS|FAIL)\b", text, re.IGNORECASE)
            has_label = re.search(r"\b(review|verdict)\b", text, re.IGNORECASE)
            if not (has_verdict and has_label):
                return (
                    False,
                    "Missing explicit PASS/FAIL verdict",
                    "Add a Review/Verdict section with PASS or FAIL",
                )
            return True, None, None

        if "risks and assumptions" in desc:
            if re.search(r"\brisk\b|\bassumption\b", output_lower):
                return True, None, None
            if context.task_type in ["documentation", "analysis", "architecture", "review"]:
                return (
                    False,
                    "No explicit risks or assumptions found",
                    "Add a Risks and Assumptions section",
                )
            return True, "Manual review recommended", None

        if "task brief" in desc or "success criteria" in desc:
            overlap = _keyword_overlap(context.task_brief, text)
            if overlap == 0:
                return (
                    False,
                    "Low alignment with task brief",
                    "Ensure the output addresses the stated task",
                )
            return True, None, None

        if "tests exist" in desc:
            if re.search(r"\btest(s)?\b|pytest|unittest|not run|skip", output_lower):
                return True, None, None
            return True, "Manual review recommended", None

        if "error handling" in desc:
            if re.search(r"\btry\b|except|raise|error handling|validate", output_lower):
                return True, None, None
            return True, "Manual review recommended", None

        if "edge cases" in desc:
            if re.search(r"edge case|empty|none|null|invalid|boundary", output_lower):
                return True, None, None
            return True, "Manual review recommended", None

        if "hallucinated" in desc or "current versions" in desc:
            return True, "Manual review recommended", None

        if "avoid unnecessary complexity" in desc or "naming is clear" in desc:
            return True, "Manual review recommended", None

        if "no regressions" in desc:
            return True, "Manual review recommended", None

        return True, None, None


def _keyword_overlap(task_brief: str, output: str) -> int:
    """Count overlapping keywords from task brief in output."""
    stopwords = {
        "the",
        "and",
        "with",
        "from",
        "this",
        "that",
        "your",
        "into",
        "will",
        "should",
        "have",
        "for",
        "what",
        "why",
        "when",
        "where",
        "which",
    }
    tokens = re.findall(r"[a-zA-Z]{4,}", task_brief.lower())
    keywords = {t for t in tokens if t not in stopwords}
    if not keywords:
        return 1
    output_lower = output.lower()
    return sum(1 for word in keywords if word in output_lower)


_SECRET_REGEX = re.compile(
    r"(sk-[A-Za-z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16}|"
    r"ghp_[A-Za-z0-9]{20,}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"][^'\"]{8,}['\"])",
    re.IGNORECASE,
)

_IMPORT_RE = re.compile(
    r"^\s*(?:from\s+([a-zA-Z_][\w\.]*)\s+import|import\s+([a-zA-Z_][\w\.]*))",
    re.MULTILINE,
)

_FILE_REF_RE = re.compile(
    r"\b(?:src|docs|configs|checklists|templates|projects|tests|memory|audit)"
    r"/[^\s)\"']+\.(?:py|md|json|yaml|yml|txt|toml|ini|cfg)\b"
)


def _find_missing_imports(text: str) -> list[str]:
    """Identify imports that are not recognized locally or via stdlib."""
    stdlib = getattr(sys, "stdlib_module_names", set())
    allowlist = {
        "pytest",
        "django",
        "flask",
        "fastapi",
        "requests",
        "httpx",
        "yaml",
        "click",
    }
    allowlist = allowlist.union(stdlib)

    imports = []
    for match in _IMPORT_RE.finditer(text):
        module = match.group(1) or match.group(2)
        if module.startswith("."):
            continue
        top = module.split(".")[0]
        if top in allowlist:
            continue
        if _is_local_module(top):
            continue
        imports.append(module)

    return sorted(set(imports))


def _is_local_module(name: str) -> bool:
    """Check if module name maps to local package or file."""
    candidates = [
        Path("src") / name,
        Path("src") / f"{name}.py",
        Path(name),
        Path(f"{name}.py"),
    ]
    return any(path.exists() for path in candidates)


def _find_missing_files(text: str) -> list[str]:
    """Find referenced files that do not exist."""
    missing = []
    for match in _FILE_REF_RE.finditer(text):
        path = Path(match.group(0))
        if not path.exists():
            missing.append(match.group(0))
    return sorted(set(missing))


# Avoid circular import
from .audit import AuditLog  # noqa: E402
