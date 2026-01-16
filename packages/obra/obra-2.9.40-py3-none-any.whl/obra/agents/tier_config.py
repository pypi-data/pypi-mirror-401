"""Agent tier configuration loader.

Loads tier configuration for review agents from config/dobra_config.yaml.
Each agent has a start_tier (for initial sweep) and optional escalate_tier
(for deep analysis).
"""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# Default tier settings per agent
DEFAULT_AGENT_TIERS: dict[str, dict[str, str | None]] = {
    "security": {"start_tier": "fast", "escalate_tier": "high"},
    "testing": {"start_tier": "fast", "escalate_tier": None},
    "code_quality": {"start_tier": "fast", "escalate_tier": None},
    "docs": {"start_tier": "fast", "escalate_tier": None},
}


def load_agent_tier_config(
    agent_name: str,
    config_path: Path | None = None,
) -> dict[str, str | None]:
    """Load tier configuration for an agent.

    Reads from config/dobra_config.yaml under agents.review.{agent_name}.
    Falls back to defaults if config is missing.

    Args:
        agent_name: Name of the agent (security, testing, code_quality, docs)
        config_path: Optional path to dobra_config.yaml (defaults to config/dobra_config.yaml)

    Returns:
        Dict with start_tier and escalate_tier keys.
        escalate_tier may be None if no escalation is configured.

    Example:
        >>> config = load_agent_tier_config("security")
        >>> config["start_tier"]
        'fast'
        >>> config["escalate_tier"]
        'high'
    """
    defaults = DEFAULT_AGENT_TIERS.get(
        agent_name,
        {"start_tier": "fast", "escalate_tier": None},
    )

    # Find config file
    if config_path is None:
        # Look for config/dobra_config.yaml relative to current working directory
        config_path = Path("config/dobra_config.yaml")

    if not config_path.exists():
        logger.debug(f"Config file not found at {config_path}, using defaults")
        return defaults

    try:
        with config_path.open(encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError) as e:
        logger.warning(f"Failed to load config from {config_path}: {e}")
        return defaults

    # Navigate to agents.review.{agent_name}
    agents_config: dict[str, Any] = config.get("agents", {})
    review_config: dict[str, Any] = agents_config.get("review", {})
    agent_config: dict[str, Any] = review_config.get(agent_name, {})

    return {
        "start_tier": agent_config.get("start_tier", defaults["start_tier"]),
        "escalate_tier": agent_config.get("escalate_tier", defaults["escalate_tier"]),
    }


__all__ = ["DEFAULT_AGENT_TIERS", "load_agent_tier_config"]
