"""Model backends - wrappers for LLM APIs."""

from typing import TYPE_CHECKING

from .base import ModelAdapter, ModelResponse


def is_adapter_available(adapter_type: str | None) -> bool:
    """Check if an adapter's SDK is installed."""
    if not adapter_type:
        return False
    try:
        if adapter_type == "ollama":
            return True
        if adapter_type == "claude":
            import anthropic  # noqa: F401
            return True
        if adapter_type == "openai":
            import openai  # noqa: F401
            return True
        if adapter_type == "gemini":
            import google.generativeai  # noqa: F401
            return True
        return False
    except ImportError:
        return False


def get_adapter(model_config: "ModelConfig") -> ModelAdapter:
    """Get adapter instance for a model config.

    Imports are kept inside to avoid ImportError when optional SDKs
    are not installed.
    """
    model_id = model_config.model_id or model_config.name
    adapter = model_config.adapter

    if adapter == "ollama":
        from .ollama import OllamaAdapter
        return OllamaAdapter(model_id, model_config.endpoint or "http://localhost:11434")
    if adapter == "claude":
        from .claude import ClaudeAdapter
        return ClaudeAdapter(model_id)
    if adapter == "openai":
        from .openai_adapter import OpenAIAdapter
        return OpenAIAdapter(model_id)
    if adapter == "gemini":
        from .gemini_adapter import GeminiAdapter
        return GeminiAdapter(model_id)

    raise ValueError(f"No adapter configured for model: {model_config.name}")


__all__ = [
    "ModelAdapter",
    "ModelResponse",
    "get_adapter",
    "is_adapter_available",
]


if TYPE_CHECKING:
    from ..core.registry import ModelConfig
