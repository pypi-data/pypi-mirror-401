"""GeminiAdapter - Google Gemini API wrapper."""

from __future__ import annotations

import os
import time

from .base import ModelAdapter, ModelResponse


class GeminiAdapter(ModelAdapter):
    """Adapter for Google Gemini models."""

    def __init__(
        self,
        model_id: str,
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        try:
            import google.generativeai as genai
        except ImportError as exc:
            raise ImportError(
                "Gemini adapter requires the google-generativeai SDK. "
                "Install with: pip install unified-controlplane[gemini]"
            ) from exc

        self._genai = genai
        self.model_id = model_id
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.timeout = timeout

        if self.api_key:
            genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(model_id)

    def generate(self, messages: list[dict]) -> ModelResponse:
        """Generate a response from Gemini."""
        prompt = self._messages_to_prompt(messages)
        start = time.perf_counter()
        try:
            response = self.model.generate_content(prompt)
        except Exception as exc:
            return ModelResponse(
                content="",
                model=self.model_id,
                error=str(exc),
            )

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        content = getattr(response, "text", "") or ""

        return ModelResponse(
            content=content,
            model=self.model_id,
            tokens_used=None,
            latency_ms=elapsed_ms,
            error=None,
        )

    def health_check(self) -> bool:
        """Check if API key is configured."""
        return bool(self.api_key)

    @staticmethod
    def _messages_to_prompt(messages: list[dict]) -> str:
        """Convert chat-style messages to a plain prompt string."""
        lines = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            if role == "system":
                prefix = "System"
            elif role == "assistant":
                prefix = "Assistant"
            else:
                prefix = "User"
            lines.append(f"{prefix}: {content}")
        return "\n".join(lines)
