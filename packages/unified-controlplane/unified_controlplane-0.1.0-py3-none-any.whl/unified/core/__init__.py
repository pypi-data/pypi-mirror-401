"""Core layer - foundational components.

Components:
- Registry: Catalog of models, tools, and skills
- Memory: Project state storage
"""

from .registry import Registry
from .memory import Memory

__all__ = ["Registry", "Memory"]
