"""Path resolution for unified control plane.

Handles finding configs, checklists, and data directories whether
running from source or installed as a package.
"""
from pathlib import Path
import os
import sys

import yaml

if sys.version_info >= (3, 11):
    from importlib.resources import files, as_file
else:
    from importlib_resources import files, as_file


def get_unified_home() -> Path:
    """Return the unified home directory (~/.unified/).

    Can be overridden via UNIFIED_HOME environment variable.
    """
    return Path(os.environ.get("UNIFIED_HOME", Path.home() / ".unified"))


def get_memory_dir(project: str | None = None) -> Path:
    """Return memory directory, optionally namespaced by project."""
    base = get_unified_home() / "memory"
    if project:
        return base / project
    return base


def get_audit_dir() -> Path:
    """Return audit log directory."""
    return get_unified_home() / "audit"


def get_default_registry_path() -> Path:
    """Return path to bundled default registry.yaml.

    Checks in order:
    1. Local ./unified.yaml (project override)
    2. ~/.unified/config/registry.yaml (user customization)
    3. Bundled package default
    """
    # Project-local override
    local = Path.cwd() / "unified.yaml"
    if local.exists():
        return local

    # User customization
    user_config = get_unified_home() / "config" / "registry.yaml"
    if user_config.exists():
        return user_config

    # Bundled default (works when installed as package)
    try:
        pkg_files = files("unified")
        configs_ref = pkg_files.joinpath("resources/configs/registry.yaml")
        with as_file(configs_ref) as path:
            if path.exists():
                return path
    except (TypeError, FileNotFoundError):
        pass

    # Fallback: relative to this file (development mode)
    dev_path = Path(__file__).parent / "resources" / "configs" / "registry.yaml"
    if dev_path.exists():
        return dev_path

    raise FileNotFoundError(
        "No registry.yaml found. Add unified.yaml or ~/.unified/config/registry.yaml."
    )


def get_checklists_dir() -> Path:
    """Return path to checklists directory.

    Checks in order:
    1. ~/.unified/checklists/ (user customization)
    2. Bundled package default
    """
    user_checklists = get_unified_home() / "checklists"
    if user_checklists.exists():
        return user_checklists

    # Bundled default
    try:
        pkg_files = files("unified")
        checklists_ref = pkg_files.joinpath("resources/checklists")
        with as_file(checklists_ref) as path:
            if path.exists():
                return path
    except (TypeError, FileNotFoundError):
        pass

    # Fallback: development mode
    dev_path = Path(__file__).parent / "resources" / "checklists"
    if dev_path.exists():
        return dev_path

    raise FileNotFoundError("No checklists directory found.")


def get_project_id_from_config() -> str | None:
    """Return project_id from local unified.yaml, if present."""
    config_path = Path.cwd() / "unified.yaml"
    if not config_path.exists():
        return None
    try:
        data = yaml.safe_load(config_path.read_text()) or {}
    except Exception:
        return None
    project_id = data.get("project_id")
    if isinstance(project_id, str) and project_id.strip():
        return project_id.strip()
    return None


def detect_project_name() -> str | None:
    """Auto-detect project name from git or folder.

    Checks in order:
    1. project_id in local unified.yaml
    2. Git remote origin name
    3. Current folder name

    Returns:
        Project name if detected, None otherwise.
    """
    # Check unified.yaml first
    project_id = get_project_id_from_config()
    if project_id:
        return project_id

    cwd = Path.cwd()

    # Try git remote
    git_dir = cwd / ".git"
    if git_dir.exists():
        config_file = git_dir / "config"
        if config_file.exists():
            # Simple parse for origin URL
            try:
                content = config_file.read_text()
                for line in content.split("\n"):
                    if "url = " in line:
                        url = line.split("url = ")[-1].strip()
                        # Extract repo name from URL
                        name = url.rstrip("/").split("/")[-1]
                        if name.endswith(".git"):
                            name = name[:-4]
                        return name
            except Exception:
                pass

    # Fallback: folder name
    return cwd.name
