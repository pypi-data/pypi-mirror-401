"""Model adapter base classes.

Defines a common interface for model adapters used by the control plane.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ModelResponse:
    """Standard response from a model adapter."""

    content: str
    model: str
    tokens_used: int | None = None
    latency_ms: int | None = None
    error: str | None = None


class ModelAdapter(ABC):
    """Base class for all model adapters."""

    @abstractmethod
    def generate(self, messages: list[dict]) -> ModelResponse:
        """Generate a response from the model."""

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the model is available."""
