"""Model backends - wrappers for LLM APIs."""

from .base import ModelAdapter, ModelResponse
from .ollama import OllamaAdapter
from .claude import ClaudeAdapter


def get_adapter(model_config: "ModelConfig") -> ModelAdapter:
    """Get adapter instance for a model config."""
    model_id = model_config.model_id or model_config.name

    if model_config.adapter == "ollama":
        return OllamaAdapter(model_id, model_config.endpoint or "http://localhost:11434")
    if model_config.adapter == "claude":
        return ClaudeAdapter(model_id)

    raise ValueError(f"No adapter configured for model: {model_config.name}")


__all__ = ["ModelAdapter", "ModelResponse", "OllamaAdapter", "ClaudeAdapter", "get_adapter"]


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.registry import ModelConfig
