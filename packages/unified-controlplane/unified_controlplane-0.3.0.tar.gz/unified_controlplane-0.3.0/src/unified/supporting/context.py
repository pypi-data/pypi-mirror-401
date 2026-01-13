"""ContextAssembler - Prompt pack assembly.

Builds the prompt pack that gets sent to a model by combining
task brief, relevant memory, and applicable context.

See docs/control_plane_spec.md Section 3.5 for details.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.registry import Registry
    from ..core.memory import Memory, MemoryEntry
    from .router import Task


@dataclass
class PromptPack:
    """Assembled context ready to send to a model."""

    system_prompt: str  # Role definition and constraints
    task_description: str  # The actual task
    context: str  # Relevant memories, decisions, patterns
    checklist_summary: str  # Evaluation criteria preview

    def to_messages(self) -> list[dict]:
        """Convert to API message format (OpenAI-style)."""
        user_content = f"{self.task_description}\n\n{self.context}"
        if self.checklist_summary:
            user_content += f"\n\n## Evaluation Criteria\n{self.checklist_summary}"
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content},
        ]


class ContextAssembler:
    """Assembles context for model calls.

    Usage:
        assembler = ContextAssembler(registry, memory)
        pack = assembler.assemble(task)
        messages = pack.to_messages()
    """

    def __init__(self, registry: "Registry", memory: "Memory"):
        self.registry = registry
        self.memory = memory

    def assemble(self, task: "Task", max_tokens: int = 4000) -> PromptPack:
        """Assemble context for a task.

        Args:
            task: The task to assemble context for
            max_tokens: Token budget for context (not yet enforced)

        Returns:
            PromptPack ready to send to model

        Note: Token budgeting is a future enhancement. Currently assembles
        all relevant context without truncation.
        """
        # Get relevant memories
        memories = self.get_relevant_memories(task, limit=5)

        # Format memories into context string
        context = self._format_memories(memories)

        # Get checklist summary
        checklist_summary = self._get_checklist_summary(task.task_type)

        # Build system prompt based on role and task type
        system_prompt = self._build_system_prompt(task)

        return PromptPack(
            system_prompt=system_prompt,
            task_description=task.intent,
            context=context,
            checklist_summary=checklist_summary,
        )

    def get_relevant_memories(
        self, task: "Task", limit: int = 5
    ) -> list["MemoryEntry"]:
        """Find memories relevant to this task.

        Uses keyword-based search. Semantic/embedding search is a future
        enhancement when memory.py supports embeddings.

        Args:
            task: The task to find memories for
            limit: Maximum memories to return
        """
        try:
            return self.memory.search(task.intent, limit=limit)
        except NotImplementedError:
            # Memory search not implemented yet
            return []

    def _format_memories(self, memories: list["MemoryEntry"]) -> str:
        """Format memories into context string."""
        if not memories:
            return ""

        sections = {"decision": [], "pattern": [], "finding": [], "context": []}

        for mem in memories:
            sections.get(mem.type, []).append(f"- {mem.title}")

        parts = []
        if sections["decision"]:
            parts.append("## Relevant Decisions\n" + "\n".join(sections["decision"]))
        if sections["pattern"]:
            parts.append("## Relevant Patterns\n" + "\n".join(sections["pattern"]))
        if sections["finding"]:
            parts.append("## Relevant Findings\n" + "\n".join(sections["finding"]))

        return "\n\n".join(parts)

    def _get_checklist_summary(self, task_type: str) -> str:
        """Get summary of evaluation criteria for task type."""
        summaries = {
            "code": (
                "Your output will be checked for:\n"
                "- No hallucinated APIs or imports\n"
                "- Uses current library versions\n"
                "- No hardcoded credentials\n"
                "- Appropriate error handling"
            ),
            "documentation": (
                "Your output will be checked for:\n"
                "- Accuracy and completeness\n"
                "- Clear structure and formatting\n"
                "- No hallucinated references"
            ),
            "review": (
                "Your output will be checked for:\n"
                "- Thorough analysis\n"
                "- Actionable feedback\n"
                "- Clear pass/fail verdict"
            ),
        }
        return summaries.get(task_type, "Your output will be evaluated for quality.")

    def _build_system_prompt(self, task: "Task") -> str:
        """Build system prompt based on task."""
        role_prompts = {
            "lead": "You are a skilled developer generating high-quality output.",
            "reviewer": "You are a thorough code reviewer checking for issues.",
            "advisor": "You provide expert advice and recommendations.",
        }
        base = role_prompts.get(task.role, "You are an AI assistant.")

        type_additions = {
            "code": " Follow best practices and write clean, maintainable code.",
            "documentation": " Write clear, well-structured documentation.",
            "review": " Be thorough but constructive in your feedback.",
        }
        addition = type_additions.get(task.task_type, "")

        return base + addition
