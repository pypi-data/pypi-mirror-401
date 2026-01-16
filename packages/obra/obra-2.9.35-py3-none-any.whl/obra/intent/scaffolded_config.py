"""Scaffolded planning configuration loading.

Loads defaults from config/default_config.yaml and merges project-level
overrides from .obra/config.yaml. All scaffolded planning values are
config-driven (no hardcoded fallbacks).
"""

from __future__ import annotations

from copy import deepcopy
import logging
from pathlib import Path
from typing import Any

import yaml

from obra.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

SCAFFOLDED_CONFIG_PATH = ("planning", "scaffolded")


def load_scaffolded_config(project_path: Path) -> dict[str, Any]:
    """Load scaffolded planning configuration for a project.

    Args:
        project_path: Project root (repo root or working directory)

    Returns:
        Merged scaffolded configuration dict
    """
    defaults = _load_default_scaffolded_config()
    overrides = _load_project_scaffolded_config(project_path)
    return _deep_merge(defaults, overrides)


def _load_default_scaffolded_config() -> dict[str, Any]:
    config_path = _find_default_config()
    try:
        content = config_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigurationError(
            f"Failed to read default config at {config_path}: {exc}",
            "Verify config/default_config.yaml exists and is valid YAML.",
        ) from exc

    scaffolded = _extract_scaffolded_section(data)
    if scaffolded is None:
        raise ConfigurationError(
            "Default config missing planning.scaffolded section.",
            "Add planning.scaffolded defaults to config/default_config.yaml.",
        )
    return scaffolded


def _load_project_scaffolded_config(project_path: Path) -> dict[str, Any]:
    config_path = project_path / ".obra" / "config.yaml"
    if not config_path.exists():
        return {}

    try:
        content = config_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigurationError(
            f"Failed to read project config at {config_path}: {exc}",
            "Fix the YAML syntax in .obra/config.yaml and try again.",
        ) from exc

    try:
        scaffolded = _extract_scaffolded_section(data)
    except ConfigurationError as exc:
        logger.warning(
            "Invalid planning.scaffolded config in %s (using defaults): %s",
            config_path,
            exc,
        )
        return {}
    return scaffolded or {}


def _extract_scaffolded_section(data: dict[str, Any]) -> dict[str, Any] | None:
    planning = data.get("planning")
    if planning is None:
        return None
    if not isinstance(planning, dict):
        raise ConfigurationError(
            "planning section must be a mapping.",
            "Set planning: { scaffolded: { ... } } in config.",
        )
    scaffolded = planning.get("scaffolded")
    if scaffolded is None:
        return None
    if not isinstance(scaffolded, dict):
        raise ConfigurationError(
            "planning.scaffolded must be a mapping.",
            "Set planning.scaffolded to a mapping of scaffolded settings.",
        )
    return scaffolded


def _find_default_config() -> Path:
    start = Path(__file__).resolve()
    for parent in start.parents:
        candidate = parent / "config" / "default_config.yaml"
        if candidate.exists():
            return candidate
    raise ConfigurationError(
        "Unable to locate config/default_config.yaml for scaffolded defaults.",
        "Ensure the repository includes config/default_config.yaml.",
    )


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result
