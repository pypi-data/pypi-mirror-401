"""ClaudeAdapter - Anthropic Claude API wrapper.

Wraps the Anthropic API for Claude model access.

See https://docs.anthropic.com/claude/reference for API details.
"""

import os
import time
from dataclasses import dataclass

from .base import ModelAdapter, ModelResponse


@dataclass
class ClaudeResponse:
    """Response from Claude API (raw)."""

    content: str
    model: str
    stop_reason: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None


class ClaudeAdapter(ModelAdapter):
    """Adapter for Anthropic Claude API.

    Usage:
        adapter = ClaudeAdapter("claude-3-sonnet-20240229")
        response = adapter.generate(messages)

    Requires ANTHROPIC_API_KEY environment variable.
    """

    def __init__(
        self,
        model_name: str,
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        self.model_name = model_name
        self.api_key = api_key  # Falls back to env var if None
        self.timeout = timeout

        try:
            import anthropic
        except ImportError as exc:
            raise ImportError(
                "anthropic package is required for ClaudeAdapter"
            ) from exc

        self._anthropic = anthropic
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate(self, messages: list[dict]) -> ModelResponse:
        """Generate a response from Claude."""
        system = None
        user_messages = []
        for message in messages:
            if message.get("role") == "system":
                system = message.get("content")
            else:
                user_messages.append(message)

        start = time.perf_counter()
        try:
            response = self.client.messages.create(
                model=self.model_name,
                system=system,
                messages=user_messages,
                max_tokens=4096,
                temperature=0.2,
            )
        except Exception as exc:
            return ModelResponse(
                content="",
                model=self.model_name,
                error=str(exc),
            )

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        content_parts = []
        for block in getattr(response, "content", []):
            text = getattr(block, "text", None)
            if text is not None:
                content_parts.append(text)

        content = "\n".join(content_parts)
        usage = getattr(response, "usage", None)
        tokens_used = None
        if usage is not None:
            tokens_used = getattr(usage, "input_tokens", 0) + getattr(
                usage, "output_tokens", 0
            )

        return ModelResponse(
            content=content,
            model=self.model_name,
            tokens_used=tokens_used,
            latency_ms=elapsed_ms,
            error=None,
        )

    def health_check(self) -> bool:
        """Check if API key is configured."""
        return bool(self.api_key or os.environ.get("ANTHROPIC_API_KEY"))
