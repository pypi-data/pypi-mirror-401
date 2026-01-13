"""OpenAIAdapter - OpenAI API wrapper.

Provides access to OpenAI chat models (GPT-4, Codex, etc.).
"""

from __future__ import annotations

import os
import time

from .base import ModelAdapter, ModelResponse


class OpenAIAdapter(ModelAdapter):
    """Adapter for OpenAI chat models."""

    def __init__(
        self,
        model_id: str,
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        try:
            import openai
        except ImportError as exc:
            raise ImportError(
                "OpenAI adapter requires the openai SDK. "
                "Install with: pip install unified-controlplane[openai]"
            ) from exc

        self._openai = openai
        self.model_id = model_id
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.timeout = timeout
        self.client = openai.OpenAI(api_key=self.api_key, timeout=timeout)

    def generate(self, messages: list[dict]) -> ModelResponse:
        """Generate a response from OpenAI."""
        start = time.perf_counter()
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
            )
        except Exception as exc:
            return ModelResponse(
                content="",
                model=self.model_id,
                error=str(exc),
            )

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        content = ""
        try:
            content = response.choices[0].message.content or ""
        except Exception:
            content = ""

        usage = getattr(response, "usage", None)
        tokens_used = getattr(usage, "total_tokens", None) if usage else None

        return ModelResponse(
            content=content,
            model=self.model_id,
            tokens_used=tokens_used,
            latency_ms=elapsed_ms,
            error=None,
        )

    def health_check(self) -> bool:
        """Check if API key is configured."""
        return bool(self.api_key)
