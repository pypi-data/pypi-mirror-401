"""Registry - Catalog of models, tools, and skills.

The Registry stores metadata about available resources and provides
query interfaces for other components (Router, Context Assembler).

See docs/control_plane_spec.md Section 3.1 for details.
"""

from dataclasses import dataclass
from typing import Callable
import importlib
import yaml


@dataclass
class ModelConfig:
    """Configuration for a model backend."""

    name: str
    provider: str  # "anthropic", "openai", "ollama"
    endpoint: str | None  # None for cloud APIs with SDK defaults
    capabilities: list[str]  # ["code", "reasoning", "review"]
    cost_tier: str  # "free", "low", "medium", "high"
    max_tokens: int
    is_local: bool
    adapter: str | None = None  # "ollama", "claude", or None
    model_id: str | None = None  # Actual provider model ID


@dataclass
class ToolConfig:
    """Configuration for a callable tool."""

    name: str
    description: str
    module: str  # Module path relative to src/, e.g., "tools.testing"
    function_name: str
    parameters: dict  # JSON schema for parameters

    def resolve(self) -> Callable:
        """Dynamically import and return the function.

        Assumes src/ is on PYTHONPATH.
        """
        mod = importlib.import_module(self.module)
        return getattr(mod, self.function_name)


@dataclass
class SkillConfig:
    """Configuration for a reusable prompt pattern."""

    name: str
    description: str
    template_path: str
    applicable_to: list[str]  # Task types this skill applies to


class Registry:
    """Catalog of available models, tools, and skills.

    Usage:
        registry = Registry()
        registry.load("configs/registry.yaml")
        model = registry.get_model("claude-sonnet")
    """

    def __init__(self):
        self._models: dict[str, ModelConfig] = {}
        self._tools: dict[str, ToolConfig] = {}
        self._skills: dict[str, SkillConfig] = {}

    def load(self, path: str) -> None:
        """Load registry configuration from YAML file.

        Args:
            path: Path to registry.yaml

        Raises:
            FileNotFoundError: If the config file does not exist
            ValueError: If required fields are missing
        """
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}

        self._models = {}
        self._tools = {}
        self._skills = {}

        for name, cfg in (data.get("models") or {}).items():
            provider = self._require(cfg, "provider", "models", name)
            max_tokens = self._require(cfg, "max_tokens", "models", name)
            self.register_model(
                name,
                ModelConfig(
                    name=name,
                    provider=provider,
                    endpoint=cfg.get("endpoint"),
                    capabilities=list(cfg.get("capabilities", [])),
                    cost_tier=cfg.get("cost_tier", "medium"),
                    max_tokens=int(max_tokens),
                    is_local=bool(cfg.get("is_local", provider == "ollama")),
                    adapter=cfg.get("adapter"),
                    model_id=cfg.get("model_id"),
                ),
            )

        for name, cfg in (data.get("tools") or {}).items():
            self.register_tool(
                name,
                ToolConfig(
                    name=name,
                    description=self._require(cfg, "description", "tools", name),
                    module=self._require(cfg, "module", "tools", name),
                    function_name=self._require(cfg, "function_name", "tools", name),
                    parameters=cfg.get("parameters", {}),
                ),
            )

        for name, cfg in (data.get("skills") or {}).items():
            self.register_skill(
                name,
                SkillConfig(
                    name=name,
                    description=self._require(cfg, "description", "skills", name),
                    template_path=self._require(cfg, "template_path", "skills", name),
                    applicable_to=list(cfg.get("applicable_to", ["all"])),
                ),
            )

    def register_model(self, name: str, config: ModelConfig) -> None:
        """Add or update a model in the registry."""
        self._models[name] = config

    def register_tool(self, name: str, config: ToolConfig) -> None:
        """Add or update a tool in the registry."""
        self._tools[name] = config

    def register_skill(self, name: str, config: SkillConfig) -> None:
        """Add or update a skill in the registry."""
        self._skills[name] = config

    def get_model(self, name: str) -> ModelConfig | None:
        """Retrieve a model by name."""
        return self._models.get(name)

    def get_tool(self, name: str) -> ToolConfig | None:
        """Retrieve a tool by name."""
        return self._tools.get(name)

    def get_skill(self, name: str) -> SkillConfig | None:
        """Retrieve a skill by name."""
        return self._skills.get(name)

    def list_models(self, filters: dict | None = None) -> list[ModelConfig]:
        """List all models, optionally filtered.

        Args:
            filters: Optional dict with keys like "capabilities", "cost_tier"

        """
        models = list(self._models.values())
        if not filters:
            return models

        capabilities = filters.get("capabilities")
        if capabilities:
            models = [
                m for m in models if all(c in m.capabilities for c in capabilities)
            ]

        if "cost_tier" in filters:
            models = [m for m in models if m.cost_tier == filters["cost_tier"]]

        if "provider" in filters:
            models = [m for m in models if m.provider == filters["provider"]]

        if "is_local" in filters:
            models = [m for m in models if m.is_local == filters["is_local"]]

        return models

    def available_models(self) -> list[ModelConfig]:
        """List models whose adapters are available."""
        from unified.models import is_adapter_available

        return [m for m in self.list_models() if is_adapter_available(m.adapter)]

    @staticmethod
    def _require(cfg: dict, key: str, section: str, name: str):
        """Return required field from cfg or raise ValueError."""
        if key not in cfg:
            raise ValueError(f"Missing {section}.{name}.{key} in registry config")
        return cfg[key]

    def list_tools(self) -> list[ToolConfig]:
        """List all registered tools."""
        return list(self._tools.values())

    def list_skills(self) -> list[SkillConfig]:
        """List all registered skills."""
        return list(self._skills.values())
