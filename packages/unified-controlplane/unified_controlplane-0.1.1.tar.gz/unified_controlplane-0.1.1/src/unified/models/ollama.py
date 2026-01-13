"""OllamaAdapter - Local Ollama inference wrapper.

Wraps the Ollama API for local GPU inference.

See https://github.com/ollama/ollama/blob/main/docs/api.md for API details.
"""

import time
from dataclasses import dataclass

import httpx

from .base import ModelAdapter, ModelResponse


@dataclass
class OllamaResponse:
    """Response from Ollama API (raw)."""

    content: str
    model: str
    done: bool
    total_duration: int | None = None  # nanoseconds
    eval_count: int | None = None  # tokens generated


class OllamaAdapter(ModelAdapter):
    """Adapter for Ollama local inference.

    Usage:
        adapter = OllamaAdapter("llama3", base_url="http://localhost:11434")
        response = adapter.generate(messages)
    """

    def __init__(
        self,
        model_name: str,
        base_url: str = "http://localhost:11434",
        timeout: float = 30.0,
    ):
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, messages: list[dict]) -> ModelResponse:
        """Generate a response from Ollama."""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
        }
        start = time.perf_counter()
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{self.base_url}/api/chat", json=payload)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            return ModelResponse(
                content="",
                model=self.model_name,
                error=str(exc),
            )

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        content = data.get("message", {}).get("content", "")
        total_duration = data.get("total_duration")
        if total_duration is not None:
            elapsed_ms = max(elapsed_ms, int(total_duration / 1_000_000))

        return ModelResponse(
            content=content,
            model=data.get("model", self.model_name),
            tokens_used=data.get("eval_count"),
            latency_ms=elapsed_ms,
            error=None,
        )

    def is_available(self) -> bool:
        """Check if Ollama is reachable."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except httpx.HTTPError:
            return False

    def health_check(self) -> bool:
        """Alias for availability check."""
        return self.is_available()
