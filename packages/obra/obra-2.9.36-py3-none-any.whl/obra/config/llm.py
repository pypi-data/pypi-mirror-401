"""LLM configuration resolution and CLI building for Obra.

Handles model validation, thinking level mapping, config resolution, and CLI argument
construction for all supported LLM providers (Anthropic, OpenAI, Google).

Example:
    from obra.config.llm import resolve_llm_config, build_llm_args

    config = resolve_llm_config("orchestrator", override_model="sonnet")
    args = build_llm_args(config, mode="text")
"""
# pylint: disable=too-many-lines

import logging
import os
import re
import shutil
import uuid
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

import yaml

from obra.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

from .loaders import load_config, load_llm_section, save_config
from .providers import (
    DEFAULT_AUTH_METHOD,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    LLM_AUTH_METHODS,
    LLM_PROVIDERS,
)

# Module logger
logger = logging.getLogger(__name__)

# Default thinking level
DEFAULT_THINKING_LEVEL = "medium"

# Abstract thinking levels (user-facing, provider-agnostic)
# Maps to provider-specific parameters in build_llm_args()
THINKING_LEVELS = ["off", "low", "medium", "high", "maximum"]

# Provider-specific thinking level mappings
# See docs/reference/llm-providers/ for official documentation
THINKING_LEVEL_MAP: dict[str, dict[str, str | None]] = {
    "anthropic": {
        # Claude Code V2 - only "ultrathink" keyword allocates thinking tokens
        # Intermediate levels (think, think hard) were deprecated in V2
        # See: docs/reference/llm-providers/claude-code-thinking.md
        "off": None,  # No thinking, don't use ultrathink
        "low": None,  # No intermediate levels exist
        "medium": None,  # No intermediate levels exist
        "high": None,  # No intermediate levels exist
        "maximum": "ultrathink",  # Only keyword that allocates thinking tokens (31,999)
    },
    "openai": {
        # Codex CLI model_reasoning_effort values
        # See: docs/reference/llm-providers/openai-codex-reasoning.md
        "off": "minimal",  # Minimize reasoning overhead
        "low": "low",
        "medium": "medium",  # Default
        "high": "high",
        "maximum": "xhigh",  # Only gpt-5.1-codex-max and gpt-5.2
    },
    "google": {
        # Gemini CLI - no reasoning effort control available
        "off": None,
        "low": None,
        "medium": None,
        "high": None,
        "maximum": None,
    },
}

# Known model shortcuts for quick switching
# Full model names (e.g., "claude-sonnet-4-5") are passed through
MODEL_SHORTCUTS = {"default", "sonnet", "opus", "haiku"}

# Models that support xhigh/maximum reasoning effort
# Used by get_effective_thinking_value() for fallback logic
XHIGH_SUPPORTED_MODELS: dict[str, set[str]] = {
    "openai": {"gpt-5.2", "gpt-5.1-codex-max"},  # xhigh only on flagship models
    "anthropic": set(),  # All Claude models support ultrathink (prompt keyword)
    "google": set(),  # Gemini has no reasoning effort control
}

# Model name patterns for provider inference (regex)
# Used by infer_provider_from_model() to auto-detect provider
MODEL_PROVIDER_PATTERNS: dict[str, str] = {
    # Anthropic/Claude patterns
    r"^opus$": "anthropic",
    r"^sonnet$": "anthropic",
    r"^haiku$": "anthropic",
    r"^claude": "anthropic",  # claude-*, claude-3-*, etc.
    # OpenAI/Codex patterns
    r"^gpt": "openai",  # gpt-4, gpt-5.2, etc.
    r"^o[134]": "openai",  # o1, o3, o4 models
    r"^codex": "openai",  # codex-*, codex-mini, etc.
    # Google/Gemini patterns
    r"^gemini": "google",  # gemini-2.5-*, gemini-3-*, etc.
}

# Model name prefixes for fast provider inference (non-regex fallback)
MODEL_PROVIDER_PREFIXES: dict[str, str] = {
    "opus": "anthropic",
    "sonnet": "anthropic",
    "haiku": "anthropic",
    "claude": "anthropic",
    "gpt": "openai",
    "o1": "openai",
    "o3": "openai",
    "o4": "openai",
    "codex": "openai",
    "gemini": "google",
}

TIER_NAMES: tuple[str, str, str] = ("fast", "medium", "high")
TIER_FALLBACKS: dict[str, tuple[str, ...]] = {
    "fast": ("fast", "medium", "high"),
    "medium": ("medium", "high"),
    "high": ("high", "medium"),
}

# Provider-specific tier defaults (FEAT-LLM-TIERS-SPLIT-001)
# Maps provider name to default tier model assignments
# Source: docs/design/PROVIDER_TIER_DEFAULTS.md and obra/model_registry.py
PROVIDER_TIER_DEFAULTS: dict[str, dict[str, str]] = {
    "anthropic": {
        "fast": "haiku",
        "medium": "sonnet",
        "high": "opus",
    },
    "openai": {
        "fast": "gpt-5.1-codex-mini",
        "medium": "gpt-5.1-codex-max",
        "high": "gpt-5.1-codex-max",
    },
    "google": {
        "fast": "gemini-2.5-flash-lite",
        "medium": "gemini-2.5-flash",
        "high": "gemini-2.5-pro",
    },
    "ollama": {
        "fast": "qwen2.5-coder:3b",
        "medium": "qwen2.5-coder:14b",
        "high": "qwen2.5-coder:32b",
    },
}


def get_provider_tier_defaults(provider: str) -> dict[str, str]:
    """Get default tier model mappings for a provider.

    Args:
        provider: Provider name (anthropic, openai, google, ollama)

    Returns:
        Dict mapping tier names to model names, or empty dict if unknown provider.

    Example:
        >>> get_provider_tier_defaults("anthropic")
        {'fast': 'haiku', 'medium': 'sonnet', 'high': 'opus'}
        >>> get_provider_tier_defaults("unknown")
        {}
    """
    return PROVIDER_TIER_DEFAULTS.get(provider, {})


def update_role_tiers_for_provider(
    role: str, new_provider: str, config: dict[str, Any]
) -> tuple[dict[str, Any], str]:
    """Update tier configuration for a role when provider changes.

    When a role's provider is changed, this function auto-updates the role's
    tier mappings to match the new provider's model names.

    Args:
        role: Role name (orchestrator or implementation)
        new_provider: New provider name (anthropic, openai, google, ollama)
        config: Full config dict (will be modified in place)

    Returns:
        Tuple of (updated_config, notification_message)

    Example:
        >>> config = {"llm": {"orchestrator": {"provider": "openai"}}}
        >>> config, msg = update_role_tiers_for_provider("orchestrator", "openai", config)
        >>> print(msg)
        Updated orchestrator tiers to match OpenAI: fast=gpt-5.1-codex-mini, ...
    """
    tier_defaults = get_provider_tier_defaults(new_provider)
    if not tier_defaults:
        # Unknown provider, no update
        return config, ""

    # Ensure role config exists
    if "llm" not in config:
        config["llm"] = {}
    if role not in config["llm"] or not isinstance(config["llm"][role], dict):
        config["llm"][role] = {}

    # Update tiers
    config["llm"][role]["tiers"] = tier_defaults.copy()

    # Build notification message
    tier_list = ", ".join(f"{tier}={model}" for tier, model in tier_defaults.items())
    provider_display = new_provider.capitalize()
    notification = f"Updated {role} tiers to match {provider_display}: {tier_list}"

    return config, notification


def _coerce_provider(raw: Any, path: str) -> str:
    if isinstance(raw, str) and raw in LLM_PROVIDERS:
        return raw
    if raw is not None:
        logger.warning(
            "%s invalid or unknown provider '%s', using default '%s'",
            path,
            raw,
            DEFAULT_PROVIDER,
        )
    return DEFAULT_PROVIDER


def _coerce_auth_method(raw: Any, path: str) -> str:
    if isinstance(raw, str) and raw in LLM_AUTH_METHODS:
        return raw
    if raw is not None:
        logger.warning(
            "%s invalid auth_method '%s', using default '%s'",
            path,
            raw,
            DEFAULT_AUTH_METHOD,
        )
    return DEFAULT_AUTH_METHOD


def _coerce_thinking_level(raw: Any, path: str) -> str:
    if isinstance(raw, str) and raw in THINKING_LEVELS:
        return raw
    if raw is not None:
        logger.warning(
            "%s invalid thinking_level '%s', using default '%s'", path, raw, DEFAULT_THINKING_LEVEL
        )
    return DEFAULT_THINKING_LEVEL


def _coerce_model(raw: Any, provider: str, path: str) -> str:
    model_value = raw if isinstance(raw, str) and raw.strip() else DEFAULT_MODEL
    try:
        return validate_model(model_value, provider)
    except ValueError as exc:
        logger.warning(
            "%s invalid model '%s' for provider '%s': %s. Using default.",
            path,
            model_value,
            provider,
            exc,
        )
        return DEFAULT_MODEL


def _coerce_bool(raw: Any, default: bool) -> bool:
    if isinstance(raw, bool):
        return raw
    return default


def _base_llm_defaults(raw_llm: dict[str, Any]) -> dict[str, Any]:
    provider = _coerce_provider(raw_llm.get("provider", DEFAULT_PROVIDER), "llm.provider")
    auth_method = _coerce_auth_method(
        raw_llm.get("auth_method", DEFAULT_AUTH_METHOD),
        "llm.auth_method",
    )
    thinking_level = _coerce_thinking_level(
        raw_llm.get("thinking_level", DEFAULT_THINKING_LEVEL), "llm.thinking_level"
    )
    model = _coerce_model(raw_llm.get("model", DEFAULT_MODEL), provider, "llm.model")
    return {
        "provider": provider,
        "auth_method": auth_method,
        "model": model,
        "thinking_level": thinking_level,
        "parse_retry_enabled": _coerce_bool(raw_llm.get("parse_retry_enabled", True), True),
        "parse_retry_providers": raw_llm.get("parse_retry_providers"),
        "parse_retry_models": raw_llm.get("parse_retry_models"),
    }


def _normalize_role_config(
    raw_role: Any, base_defaults: dict[str, Any], role: str
) -> dict[str, Any]:
    if not isinstance(raw_role, dict):
        raw_role = {}
    provider = _coerce_provider(
        raw_role.get("provider", base_defaults["provider"]),
        f"llm.{role}.provider",
    )
    auth_method = _coerce_auth_method(
        raw_role.get("auth_method", base_defaults["auth_method"]),
        f"llm.{role}.auth_method",
    )
    thinking_level = _coerce_thinking_level(
        raw_role.get("thinking_level", base_defaults["thinking_level"]),
        f"llm.{role}.thinking_level",
    )
    model = _coerce_model(
        raw_role.get("model", base_defaults["model"]),
        provider,
        f"llm.{role}.model",
    )

    # Normalize role-specific tiers using provider defaults
    raw_tiers = raw_role.get("tiers")
    normalized_tiers = _normalize_role_tiers(raw_tiers, provider, base_defaults)

    return {
        "provider": provider,
        "auth_method": auth_method,
        "model": model,
        "thinking_level": thinking_level,
        "parse_retry_enabled": _coerce_bool(
            raw_role.get("parse_retry_enabled", base_defaults["parse_retry_enabled"]),
            base_defaults["parse_retry_enabled"],
        ),
        "parse_retry_providers": raw_role.get(
            "parse_retry_providers", base_defaults["parse_retry_providers"]
        ),
        "parse_retry_models": raw_role.get(
            "parse_retry_models", base_defaults["parse_retry_models"]
        ),
        "tiers": normalized_tiers,
    }


def _normalize_tier_entry(
    tier: str, value: Any, base_defaults: dict[str, Any]
) -> dict[str, Any] | None:
    if value is None:
        return None

    if isinstance(value, str):
        provider_guess = infer_provider_from_model(value) or base_defaults["provider"]
        return {
            "provider": provider_guess,
            "auth_method": base_defaults["auth_method"],
            "model": _coerce_model(value, provider_guess, f"llm.tiers.{tier}.model"),
            "thinking_level": base_defaults["thinking_level"],
        }

    if isinstance(value, dict):
        provider = _coerce_provider(
            value.get("provider", base_defaults["provider"]), f"llm.tiers.{tier}.provider"
        )
        auth_method = _coerce_auth_method(
            value.get("auth_method", base_defaults["auth_method"]), f"llm.tiers.{tier}.auth_method"
        )
        thinking_level = _coerce_thinking_level(
            value.get("thinking_level", base_defaults["thinking_level"]),
            f"llm.tiers.{tier}.thinking_level",
        )
        model_value = value.get("model", base_defaults["model"])
        return {
            "provider": provider,
            "auth_method": auth_method,
            "model": _coerce_model(model_value, provider, f"llm.tiers.{tier}.model"),
            "thinking_level": thinking_level,
        }

    raise ConfigurationError(
        f"Invalid llm.tiers.{tier} entry: expected string or mapping, got {type(value).__name__}.",
        f"Set llm.tiers.{tier} to a model shortcut or a mapping with provider/model.",
    )


def _normalize_role_tiers(
    raw_tiers: Any, provider: str, base_defaults: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    """Normalize tier configuration for a specific role.

    Uses provider-specific tier defaults as fallback when tiers are not explicitly
    configured. This allows each role to have tier mappings matching its provider's
    model names.

    Args:
        raw_tiers: Raw tiers dict from config (e.g., {fast: haiku, medium: sonnet})
        provider: Provider name for this role (anthropic, openai, google, ollama)
        base_defaults: Base config defaults for fallback (provider, auth_method, etc.)

    Returns:
        Dict mapping tier names to normalized config dicts with provider, model, etc.
        Falls back to PROVIDER_TIER_DEFAULTS for the given provider.

    Example:
        >>> _normalize_role_tiers({"fast": "haiku"}, "anthropic", base_defaults)
        {
            "fast": {"provider": "anthropic", "model": "haiku", ...},
            "medium": {"provider": "anthropic", "model": "sonnet", ...},  # from defaults
            "high": {"provider": "anthropic", "model": "opus", ...}        # from defaults
        }
    """
    if raw_tiers is None:
        raw_tiers = {}
    if not isinstance(raw_tiers, dict):
        raw_tiers = {}

    # Get provider-specific tier defaults
    provider_defaults = get_provider_tier_defaults(provider)

    normalized: dict[str, dict[str, Any]] = {}
    for tier_name in TIER_NAMES:
        # Check if tier is explicitly configured
        if tier_name in raw_tiers:
            entry = _normalize_tier_entry(tier_name, raw_tiers[tier_name], base_defaults)
            if entry:
                normalized[tier_name] = entry
        elif tier_name in provider_defaults:
            # Fall back to provider defaults
            default_model = provider_defaults[tier_name]
            normalized[tier_name] = {
                "provider": provider,
                "auth_method": base_defaults["auth_method"],
                "model": _coerce_model(default_model, provider, f"llm.{tier_name}.model"),
                "thinking_level": base_defaults["thinking_level"],
            }

    return normalized


def _normalize_tiers(raw_tiers: Any, base_defaults: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if raw_tiers is None:
        return {}
    if not isinstance(raw_tiers, dict):
        raise ConfigurationError(
            "Invalid llm.tiers section in ~/.obra/client-config.yaml.",
            "Set llm.tiers to a mapping like {fast: haiku, medium: sonnet, high: opus}.",
        )

    normalized: dict[str, dict[str, Any]] = {}
    for tier_name in TIER_NAMES:
        if tier_name not in raw_tiers:
            continue
        entry = _normalize_tier_entry(tier_name, raw_tiers[tier_name], base_defaults)
        if entry:
            normalized[tier_name] = entry
    return normalized


def _get_env_tier_override(tier: str) -> str | None:
    env_value = os.environ.get(f"OBRA_{tier.upper()}_MODEL")
    if not env_value:
        return None
    stripped = env_value.strip()
    return stripped or None


def _normalized_llm_config(raw_llm: dict[str, Any]) -> dict[str, Any]:
    base_defaults = _base_llm_defaults(raw_llm)
    return {
        "provider": base_defaults["provider"],
        "auth_method": base_defaults["auth_method"],
        "model": base_defaults["model"],
        "thinking_level": base_defaults["thinking_level"],
        "parse_retry_enabled": base_defaults["parse_retry_enabled"],
        "parse_retry_providers": base_defaults["parse_retry_providers"],
        "parse_retry_models": base_defaults["parse_retry_models"],
        "orchestrator": _normalize_role_config(
            raw_llm.get("orchestrator", {}),
            base_defaults,
            "orchestrator",
        ),
        "implementation": _normalize_role_config(
            raw_llm.get("implementation", {}), base_defaults, "implementation"
        ),
    }


def infer_provider_from_model(model: str) -> str | None:
    """Infer the LLM provider from a model name.

    Uses regex patterns first (MODEL_PROVIDER_PATTERNS), then falls back
    to prefix matching (MODEL_PROVIDER_PREFIXES).

    Args:
        model: Model name to analyze (e.g., "opus", "gpt-5.2", "gemini-2.5-flash")

    Returns:
        Provider name ("anthropic", "openai", "google") or None if unknown

    Examples:
        >>> infer_provider_from_model("opus")
        'anthropic'
        >>> infer_provider_from_model("gpt-5.2")
        'openai'
        >>> infer_provider_from_model("gemini-2.5-flash")
        'google'
        >>> infer_provider_from_model("custom-model")
        None
    """
    if not model or model == "default":
        return None

    model_lower = model.lower()

    # Try regex patterns first (most precise)
    for pattern, provider in MODEL_PROVIDER_PATTERNS.items():
        if re.match(pattern, model_lower):
            return provider

    # Fall back to prefix matching
    for prefix, provider in MODEL_PROVIDER_PREFIXES.items():
        if model_lower.startswith(prefix):
            return provider

    return None


def get_thinking_level_notes(
    provider: str,
    thinking_level: str,
    model: str | None = None,
) -> list[str]:
    """Get user-facing notes about thinking level behavior for a provider.

    Provides feedback about how the selected thinking level maps to
    provider-specific behavior, including limitations and recommendations.

    Args:
        provider: LLM provider name
        thinking_level: Abstract thinking level (off, low, medium, high, maximum)
        model: Optional model name for model-specific notes

    Returns:
        List of note strings to display to the user

    Examples:
        >>> get_thinking_level_notes("anthropic", "maximum")
        ['Using "ultrathink" prompt keyword for extended thinking (31,999 tokens)']

        >>> get_thinking_level_notes("google", "high")
        ['Gemini CLI does not support reasoning effort control']

        >>> get_thinking_level_notes("openai", "maximum", "gpt-5.1")
        ['xhigh reasoning not supported on gpt-5.1, using "high" instead']
    """
    notes = []

    # Provider-specific notes
    if provider == "anthropic":
        if thinking_level == "maximum":
            notes.append('Using "ultrathink" prompt keyword for extended thinking (31,999 tokens)')
        elif thinking_level in ("low", "high"):
            notes.append(
                f'Claude Code V2 only supports "off" (no thinking) or "maximum" (ultrathink). '
                f'Level "{thinking_level}" has no effect.'
            )

    elif provider == "openai":
        # Check xhigh support
        if thinking_level == "maximum":
            supported = XHIGH_SUPPORTED_MODELS.get("openai", set())
            if model and model not in supported:
                notes.append(f'xhigh reasoning not supported on {model}, using "high" instead')
                notes.append(f'For xhigh, use: {", ".join(sorted(supported))}')
            else:
                notes.append("Using xhigh reasoning effort for maximum analysis")

    elif provider == "google" and thinking_level != "off":
        notes.append("Gemini CLI does not support reasoning effort control")

    return notes


def get_effective_thinking_value(
    provider: str,
    thinking_level: str,
    model: str | None = None,
) -> str | None:
    """Get the effective provider-specific thinking value with fallback.

    Maps abstract thinking level to provider-specific value, applying
    fallback logic for unsupported configurations (e.g., xhigh -> high
    for OpenAI models that don't support xhigh).

    Args:
        provider: LLM provider name
        thinking_level: Abstract thinking level (off, low, medium, high, maximum)
        model: Optional model name for model-specific fallback

    Returns:
        Provider-specific thinking value (e.g., "xhigh", "high", "ultrathink")
        or None if the provider doesn't support the level

    Examples:
        >>> get_effective_thinking_value("openai", "maximum", "gpt-5.2")
        'xhigh'
        >>> get_effective_thinking_value("openai", "maximum", "gpt-5.1")
        'high'  # Fallback - xhigh not supported
        >>> get_effective_thinking_value("anthropic", "maximum")
        'ultrathink'
        >>> get_effective_thinking_value("google", "high")
        None  # No reasoning control
    """
    provider_map: dict[str, str | None] = THINKING_LEVEL_MAP.get(provider, {})
    base_value = provider_map.get(thinking_level)

    # Apply fallback logic for OpenAI xhigh
    if provider == "openai" and thinking_level == "maximum":
        supported = XHIGH_SUPPORTED_MODELS.get("openai", set())
        if model and model not in supported:
            # Fall back to high
            return provider_map.get("high", "high")

    return base_value


def validate_model(model: str, provider: str = DEFAULT_PROVIDER) -> str:
    """Validate and normalize a model name.

    Supports two types of model names:
    1. Shortcuts: default, sonnet, opus, haiku (validated against provider)
    2. Full model names: claude-sonnet-4-5, gpt-4o, etc. (passthrough)

    Args:
        model: Model name to validate (shortcut or full name)
        provider: Provider to validate against for shortcuts

    Returns:
        Validated model name (unchanged)

    Raises:
        ValueError: If shortcut is not valid for the given provider
    """
    if not model:
        return DEFAULT_MODEL

    # Shortcuts are validated against provider's model list
    if model in MODEL_SHORTCUTS:
        provider_info = LLM_PROVIDERS.get(provider, LLM_PROVIDERS[DEFAULT_PROVIDER])
        valid_models = cast(Sequence[str], provider_info.get("models", []))
        if model not in valid_models:
            raise ValueError(
                f"Model '{model}' not valid for provider '{provider}'. "
                f"Valid: {', '.join(valid_models)}"
            )
        return model

    # Full model names are passed through without validation
    # This allows users to use specific model versions like "claude-sonnet-4-5"
    return model


def get_project_planning_config(project_path: Path | None) -> dict[str, Any]:
    """Load planning configuration from project-level .obra/config.yaml.

    Args:
        project_path: Base project path (repo root preferred)

    Returns:
        Dictionary with planning config values (empty if not set)

    Raises:
        ConfigurationError: If the planning section is malformed
    """
    if project_path is None:
        return {}

    config_path = Path(project_path) / ".obra" / "config.yaml"
    if not config_path.exists():
        return {}

    try:
        with config_path.open(encoding="utf-8") as config_file:
            raw_config = yaml.safe_load(config_file) or {}
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            f"Invalid YAML in {config_path}: {exc}",
            "Fix the YAML syntax in .obra/config.yaml and try again.",
        ) from exc
    except OSError as exc:
        raise ConfigurationError(
            f"Unable to read {config_path}: {exc}",
            "Check file permissions for .obra/config.yaml and retry.",
        ) from exc

    planning_section = raw_config.get("planning")
    if planning_section is None:
        return {}
    if not isinstance(planning_section, dict):
        logger.warning(
            "Ignoring invalid planning section in %s (expected mapping).",
            config_path,
        )
        return {}

    config: dict[str, Any] = {}
    perm_value = planning_section.get("permissive_mode")
    if perm_value is not None:
        if not isinstance(perm_value, bool):
            logger.warning(
                "Ignoring invalid planning.permissive_mode in %s (expected boolean).",
                config_path,
            )
        else:
            config["permissive_mode"] = perm_value

    domain_value = planning_section.get("domain")
    if domain_value is not None:
        if not isinstance(domain_value, str) or not domain_value.strip():
            logger.warning(
                "Ignoring invalid planning.domain in %s (expected non-empty string).",
                config_path,
            )
        else:
            config["domain"] = domain_value.strip()

    # Backward compatibility: allow top-level domain key if present
    if "domain" not in config and isinstance(raw_config.get("domain"), str):
        domain_top = raw_config["domain"].strip()
        if domain_top:
            config["domain"] = domain_top

    return config


def resolve_llm_config(
    role: str,
    override_provider: str | None = None,
    override_model: str | None = None,
    override_auth_method: str | None = None,
    override_thinking_level: str | None = None,
    override_skip_git_check: bool | None = None,
    override_auto_init_git: bool | None = None,
) -> dict[str, Any]:
    """Resolve LLM configuration for a role with optional overrides.

    Resolution order (highest to lowest priority):
    1. Session overrides (passed as arguments, e.g., CLI flags)
    2. Global config file (~/.obra/client-config.yaml)
    3. Defaults (anthropic, oauth, default, medium)

    Args:
        role: "orchestrator" or "implementation"
        override_provider: Optional provider override (session-only)
        override_model: Optional model override (session-only)
        override_auth_method: Optional auth method override (session-only)
        override_thinking_level: Optional thinking level override (session-only)
        override_skip_git_check: Optional git skip check override (CLI flag)
        override_auto_init_git: Optional git auto init override (CLI flag)

    Returns:
        Resolved config dict with provider, auth_method, model, thinking_level keys
        and optional parse retry controls.
    """
    if role not in ("orchestrator", "implementation"):
        raise ValueError(f"Invalid role: {role}")

    # Get base config from global config file
    llm_config = get_llm_config()
    role_config = llm_config.get(role, {})

    # Load git section from raw config (GIT-HARD-001)
    raw_config = load_config()
    raw_llm = load_llm_section(raw_config)
    git_config = raw_llm.get("git", {}) if raw_llm else {}

    # Backward compatibility: Check for old llm.codex.skip_git_check config (GIT-HARD-001)
    skip_check = git_config.get("skip_check")
    if skip_check is None:
        # Check old config path: llm.codex.skip_git_check
        codex_config = raw_llm.get("codex", {}) if raw_llm else {}
        old_skip_check = codex_config.get("skip_git_check")
        if old_skip_check is not None:
            skip_check = old_skip_check
            logger.warning(
                "Config key 'llm.codex.skip_git_check' is deprecated. "
                "Please migrate to 'llm.git.skip_check' in your config file."
            )
        else:
            skip_check = False
    else:
        skip_check = bool(skip_check)

    # Start with defaults
    resolved = {
        "provider": role_config.get("provider", DEFAULT_PROVIDER),
        "auth_method": role_config.get("auth_method", DEFAULT_AUTH_METHOD),
        "model": role_config.get("model", DEFAULT_MODEL),
        "thinking_level": role_config.get("thinking_level", DEFAULT_THINKING_LEVEL),
        "parse_retry_enabled": role_config.get("parse_retry_enabled", True),
        "parse_retry_providers": role_config.get("parse_retry_providers"),
        "parse_retry_models": role_config.get("parse_retry_models"),
        "git": {
            "skip_check": skip_check,
            "auto_init": git_config.get("auto_init", False),
        },
    }

    # Apply overrides (session-only, don't persist)
    if override_provider:
        if override_provider not in LLM_PROVIDERS:
            raise ValueError(f"Invalid provider: {override_provider}")
        resolved["provider"] = override_provider

    if override_auth_method:
        if override_auth_method not in LLM_AUTH_METHODS:
            raise ValueError(f"Invalid auth method: {override_auth_method}")
        resolved["auth_method"] = override_auth_method

    if override_model:
        # Validate model against resolved provider
        resolved["model"] = validate_model(override_model, resolved["provider"])

    if override_thinking_level:
        if override_thinking_level not in THINKING_LEVELS:
            raise ValueError(
                f"Invalid thinking level: {override_thinking_level}. "
                f"Valid: {', '.join(THINKING_LEVELS)}"
            )
        resolved["thinking_level"] = override_thinking_level

    # Apply git overrides (CLI flags override config)
    if override_skip_git_check is not None:
        resolved["git"]["skip_check"] = override_skip_git_check
        logger.debug(f"Git skip_check overridden by CLI flag: {override_skip_git_check}")

    if override_auto_init_git is not None:
        resolved["git"]["auto_init"] = override_auto_init_git
        logger.debug(f"Git auto_init overridden by CLI flag: {override_auto_init_git}")

    return resolved


# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-branches,too-many-locals
def resolve_tier_config(
    tier: str,
    role: str = "implementation",
    override_provider: str | None = None,
    override_model: str | None = None,
    override_auth_method: str | None = None,
    override_thinking_level: str | None = None,
) -> dict[str, Any]:
    """Resolve model config for a given tier with role-specific fallback chain.

    Reads tier configuration from llm.{role}.tiers and falls back to provider-specific
    tier defaults when not explicitly configured.

    Fallback order:
    - fast: llm.{role}.tiers.fast -> medium -> high -> provider tier defaults -> role defaults
    - medium: llm.{role}.tiers.medium -> high -> provider tier defaults -> role defaults
    - high: llm.{role}.tiers.high -> medium -> provider tier defaults -> role defaults

    Args:
        tier: Tier name (fast, medium, high)
        role: Role to resolve for (orchestrator or implementation)
        override_provider: Optional provider override
        override_model: Optional model override
        override_auth_method: Optional auth method override
        override_thinking_level: Optional thinking level override

    Returns:
        Resolved config dict with provider, model, auth_method, thinking_level, etc.

    Example:
        >>> resolve_tier_config("fast", role="orchestrator")
        {'provider': 'anthropic', 'model': 'haiku', ...}
    """
    if tier not in TIER_FALLBACKS:
        raise ValueError(f"Invalid tier: {tier}. Valid: {', '.join(TIER_NAMES)}")
    if role not in ("orchestrator", "implementation"):
        raise ValueError(f"Invalid role: {role}")

    env_override_model = _get_env_tier_override(tier)
    override_model = override_model or env_override_model
    if override_model and not override_provider:
        inferred_provider = infer_provider_from_model(override_model)
        if inferred_provider:
            override_provider = inferred_provider

    llm_config = get_llm_config()
    role_config = llm_config.get(role, {})

    base_config = {
        "provider": role_config.get("provider", llm_config.get("provider", DEFAULT_PROVIDER)),
        "auth_method": role_config.get(
            "auth_method",
            llm_config.get("auth_method", DEFAULT_AUTH_METHOD),
        ),
        "model": role_config.get("model", llm_config.get("model", DEFAULT_MODEL)),
        "thinking_level": role_config.get(
            "thinking_level",
            llm_config.get("thinking_level", DEFAULT_THINKING_LEVEL),
        ),
        "parse_retry_enabled": role_config.get("parse_retry_enabled", True),
        "parse_retry_providers": role_config.get("parse_retry_providers"),
        "parse_retry_models": role_config.get("parse_retry_models"),
    }

    tier_overrides = role_config.get("tiers", {})
    fallback_chain = TIER_FALLBACKS[tier]

    chosen: dict[str, Any] = {}
    for candidate in fallback_chain:
        candidate_config = tier_overrides.get(candidate, {})
        if candidate_config:
            chosen = candidate_config
            break

    # Fall back to provider tier defaults if no tier configuration found
    if not chosen:
        role_provider = role_config.get("provider", base_config["provider"])
        provider_defaults = get_provider_tier_defaults(role_provider)
        if tier in provider_defaults:
            default_model = provider_defaults[tier]
            chosen = {
                "provider": role_provider,
                "auth_method": base_config["auth_method"],
                "model": default_model,
                "thinking_level": base_config["thinking_level"],
            }

    resolved = {
        "provider": chosen.get("provider", base_config["provider"]),
        "auth_method": chosen.get("auth_method", base_config["auth_method"]),
        "model": chosen.get("model", base_config["model"]),
        "thinking_level": chosen.get("thinking_level", base_config["thinking_level"]),
        "parse_retry_enabled": base_config["parse_retry_enabled"],
        "parse_retry_providers": base_config["parse_retry_providers"],
        "parse_retry_models": base_config["parse_retry_models"],
    }

    if override_provider:
        if override_provider not in LLM_PROVIDERS:
            raise ValueError(f"Invalid provider: {override_provider}")
        resolved["provider"] = override_provider

    if override_auth_method:
        if override_auth_method not in LLM_AUTH_METHODS:
            raise ValueError(f"Invalid auth method: {override_auth_method}")
        resolved["auth_method"] = override_auth_method

    if override_model:
        resolved["model"] = validate_model(override_model, resolved["provider"])

    if override_thinking_level:
        if override_thinking_level not in THINKING_LEVELS:
            raise ValueError(
                f"Invalid thinking level: {override_thinking_level}. "
                f"Valid: {', '.join(THINKING_LEVELS)}"
            )
        resolved["thinking_level"] = override_thinking_level

    return resolved


def get_llm_config() -> dict[str, Any]:
    """Get LLM configuration from config file.

    Returns:
        Normalized LLM config with role defaults and optional tiers:
        {
            "provider": "anthropic",
            "auth_method": "oauth",
            "model": "default",
            "thinking_level": "medium",
            "orchestrator": {...},
            "implementation": {...},
            "tiers": {
                "fast": {
                    "provider": "...",
                    "auth_method": "...",
                    "model": "...",
                    "thinking_level": "...",
                }
            }
        }
    """
    config = load_config()
    llm_section = load_llm_section(config)
    if not llm_section:
        return _normalized_llm_config({})
    return _normalized_llm_config(llm_section)


def set_llm_config(
    role: str,  # "orchestrator" or "implementation"
    provider: str,
    auth_method: str,
    model: str = "default",
    thinking_level: str = "medium",
) -> str:
    """Set LLM configuration for a specific role.

    Args:
        role: "orchestrator" or "implementation"
        provider: LLM provider (anthropic, openai, google)
        auth_method: Auth method (oauth, api_key)
        model: Model to use (default recommended for oauth)
        thinking_level: Abstract thinking level (off, low, medium, high, maximum)
            Maps to provider-specific values via THINKING_LEVEL_MAP

    Returns:
        Notification message if tiers were auto-updated, empty string otherwise

    Raises:
        ValueError: If any parameter is invalid
    """
    if role not in ("orchestrator", "implementation"):
        raise ValueError(f"Invalid role: {role}. Must be 'orchestrator' or 'implementation'")

    if provider not in LLM_PROVIDERS:
        raise ValueError(f"Invalid provider: {provider}. Valid: {list(LLM_PROVIDERS.keys())}")

    if auth_method not in LLM_AUTH_METHODS:
        raise ValueError(
            f"Invalid auth method: {auth_method}. Valid: {list(LLM_AUTH_METHODS.keys())}"
        )

    provider_info = LLM_PROVIDERS[provider]
    provider_models = cast(Sequence[str], provider_info.get("models", []))
    if model not in provider_models:
        raise ValueError(
            f"Invalid model '{model}' for {provider}. Valid: {provider_models}"
        )

    if thinking_level not in THINKING_LEVELS:
        raise ValueError(
            f"Invalid thinking level: {thinking_level}. Valid: {', '.join(THINKING_LEVELS)}"
        )

    config = load_config()
    if "llm" not in config:
        config["llm"] = get_llm_config()

    if provider == "openai":
        llm_section = config.get("llm")
        if isinstance(llm_section, dict):
            git_config = llm_section.setdefault("git", {})
            if isinstance(git_config, dict):
                git_config["skip_check"] = True

    # Check if provider is changing (FEAT-LLM-TIERS-SPLIT-001)
    old_provider = None
    if role in config["llm"] and isinstance(config["llm"][role], dict):
        old_provider = config["llm"][role].get("provider")

    notification = ""
    if old_provider and old_provider != provider:
        # Provider changed - auto-update tiers
        config, notification = update_role_tiers_for_provider(role, provider, config)

    config["llm"][role] = {
        "provider": provider,
        "auth_method": auth_method,
        "model": model,
        "thinking_level": thinking_level,
    }

    save_config(config)
    return notification


def get_llm_display(role: str) -> str:
    """Get a human-readable display string for LLM config.

    Args:
        role: "orchestrator" or "implementation"

    Returns:
        Display string like "Anthropic (OAuth, default)"
    """
    llm_config = get_llm_config()
    role_config = llm_config.get(role, {})

    provider = role_config.get("provider", DEFAULT_PROVIDER)
    auth_method = role_config.get("auth_method", DEFAULT_AUTH_METHOD)
    model = role_config.get("model", DEFAULT_MODEL)

    provider_name = LLM_PROVIDERS.get(provider, {}).get("name", provider)
    auth_name = "OAuth" if auth_method == "oauth" else "API Key"

    return f"{provider_name} ({auth_name}, {model})"


def get_thinking_keyword(resolved_config: dict[str, str]) -> str | None:
    """Get the thinking keyword to prepend to prompts (Claude Code only).

    Claude Code V2 uses prompt keywords (not CLI args) to trigger extended thinking.
    Only "ultrathink" allocates thinking tokens; other levels were deprecated.

    Args:
        resolved_config: Resolved config dict from resolve_llm_config()

    Returns:
        "ultrathink" if provider is anthropic and thinking_level is maximum,
        None otherwise.

    Example:
        >>> get_thinking_keyword({"provider": "anthropic", "thinking_level": "maximum"})
        "ultrathink"
        >>> get_thinking_keyword({"provider": "anthropic", "thinking_level": "high"})
        None
        >>> get_thinking_keyword({"provider": "openai", "thinking_level": "maximum"})
        None  # OpenAI uses CLI args, not keywords
    """
    provider = resolved_config.get("provider", DEFAULT_PROVIDER)
    thinking_level = resolved_config.get("thinking_level", DEFAULT_THINKING_LEVEL)

    if provider == "anthropic" and thinking_level == "maximum":
        return "ultrathink"
    return None


def build_llm_args(resolved_config: dict[str, str], mode: str = "text") -> list[str]:
    """Build CLI arguments from resolved LLM configuration.

    Generates provider-specific CLI arguments including the --model flag
    when model != "default" and thinking_level mapped to provider-specific
    parameters via THINKING_LEVEL_MAP.

    Note: For Claude Code, thinking is triggered via prompt keyword (see
    get_thinking_keyword()), not CLI args. For OpenAI Codex, thinking is
    controlled via --config model_reasoning_effort=<level>.

    Args:
        resolved_config: Resolved config dict from resolve_llm_config()
            Must have: provider, model keys
            Optional: thinking_level
                (maps to provider-specific values)
        mode: Operation mode - "text" for derive/examine phases that need
            --print and JSON output, "execute" for execute/fix phases that
            need to write files (no --print). Default is "text" for backward
            compatibility. (ISSUE-SAAS-035)

    Returns:
        List of CLI arguments (e.g., ["--dangerously-skip-permissions", "--model", "sonnet"])

    Example:
        # OpenAI with maximum thinking -> xhigh reasoning effort
        >>> build_llm_args({"provider": "openai", "model": "gpt-5.2", "thinking_level": "maximum"})
        ["exec", "--full-auto", "--model", "gpt-5.2", "--config", "model_reasoning_effort=xhigh"]

        # Anthropic text mode (derive/examine) - with --print for JSON output
        >>> build_llm_args({"provider": "anthropic", "model": "sonnet"}, mode="text")
        [
            "--print",
            "--output-format",
            "json",
            "--dangerously-skip-permissions",
            "--model",
            "sonnet",
            "...",
        ]

        # Anthropic execute mode (execute/fix) - no --print, allows file writing
        >>> build_llm_args({"provider": "anthropic", "model": "sonnet"}, mode="execute")
        ["--dangerously-skip-permissions", "--model", "sonnet", ...]
    """
    provider = resolved_config.get("provider", DEFAULT_PROVIDER)
    model = resolved_config.get("model", DEFAULT_MODEL)
    thinking_level = resolved_config.get("thinking_level", DEFAULT_THINKING_LEVEL)

    # Map abstract thinking_level to provider-specific value
    provider_thinking_map = THINKING_LEVEL_MAP.get(provider, {})
    provider_thinking_value = provider_thinking_map.get(thinking_level)

    # Build args based on provider CLI
    if provider == "anthropic":
        # Claude Code CLI
        # ISSUE-SAAS-035 FIX: Mode-aware argument building
        # - "text" mode: For derive/examine phases that need --print and JSON output
        # - "execute" mode: For execute/fix phases that need to write files (no --print)
        args = []
        if mode == "text":
            # ISSUE-LLM-002 FIX: Use --print mode for text generation (not code implementation)
            # and --output-format json to enforce JSON responses for derivation/examine phases
            args.append("--print")  # Text generation mode (prevents code writing)
            args.extend(["--output-format", "json"])  # Force JSON output
        # Execute mode: No --print flag - allows Claude Code to write files
        args.append("--dangerously-skip-permissions")
        if model and model != "default":
            args.extend(["--model", model])
        # Note: Claude thinking mode (ultrathink, etc.) would be passed via prompt
        # or environment, not CLI args - handled separately by orchestrator

        # FEAT-CLI-ISOLATION-001: Context isolation flags to prevent cross-session pollution
        # Fresh session ID ensures no cached context from prior invocations
        session_id = str(uuid.uuid4())
        args.extend(["--no-session-persistence"])  # Don't persist session state
        args.extend(["--session-id", session_id])  # Fresh session each invocation
        args.extend(["--setting-sources", ""])  # Block user-level settings pollution
        logger.info("Claude CLI isolation: session_id=%s...", session_id[:8])
        return args

    if provider == "google":
        # Gemini CLI - no reasoning effort control
        # See: docs/reference/llm-providers/gemini-cli-models.md
        # ISSUE-SAAS-046 FIX: Mode-aware argument building for Gemini
        # - "text" mode: For derive/examine phases (JSON output, no file writes)
        # - "execute" mode: For execute/fix phases (auto-approve file writes)
        #
        # ISSUE-SAAS-048 FIX: Use --sandbox=none for text mode to disable tools.
        # With --sandbox=permissive, Gemini has access to internal tools
        # (write_todos, etc.) that can hijack the response instead of returning
        # structured JSON. This causes intermittent failures where plan items
        # have "Untitled" fields because Gemini uses tools instead of returning JSON.
        if mode == "text":
            # Text generation mode - disable tools, structured output for parsing
            args = ["--sandbox=none"]
            args.extend(["--output-format", "json"])
        else:
            # Execute mode - MUST have --sandbox=permissive for file operations
            # and --yolo for auto-approval (Gemini waits for approval in headless mode)
            args = ["--sandbox=permissive"]
            args.append("--yolo")
        # "default" and "auto" both mean let Gemini choose (no --model flag)
        if model and model not in ("default", "auto"):
            args.extend(["--model", model])
        return args

    if provider == "openai":
        # OpenAI Codex CLI - uses exec mode for non-interactive operation
        # BUG-a1dd1b85: Simplified flags to match working headless pattern.
        # Previous approach used --full-auto which was redundant with explicit --sandbox.
        # ISSUE-SAAS-051: Mode-aware sandbox configuration
        # - "text" mode: For derive/examine phases (JSON output, no file writes)
        # - "execute" mode: For execute/fix phases (file writes allowed)
        args = ["exec"]
        if mode == "text":
            # Text mode uses read-only sandbox (no file writes needed)
            args.extend(["--sandbox", "read-only"])
        else:
            # Execute mode needs workspace-write to allow file operations
            # Using explicit flag instead of --full-auto to avoid conflicts
            args.extend(["--sandbox", "workspace-write"])
        if model and model != "default":
            args.extend(["--model", model])
        # Add reasoning effort (codex uses --config flag)
        if provider_thinking_value:
            args.extend(["--config", f"model_reasoning_effort={provider_thinking_value}"])
        return args

    # Fallback to Claude Code CLI args
    return ["--dangerously-skip-permissions"]


def get_llm_cli(provider: str = DEFAULT_PROVIDER) -> str:
    """Get the CLI executable path for a provider.

    Returns the full executable path for cross-platform subprocess compatibility.
    On Windows, this ensures extensions (.cmd/.exe) are included.
    On macOS/Linux, returns the resolved path for reliability.

    Args:
        provider: LLM provider name

    Returns:
        Full path to CLI executable, or bare command name as fallback
    """
    provider_info = LLM_PROVIDERS.get(provider, LLM_PROVIDERS[DEFAULT_PROVIDER])
    cli_name = str(provider_info.get("cli", "claude"))
    # Full path for Windows compatibility (.cmd/.exe) and reliability everywhere
    cli_path = shutil.which(cli_name)
    return cli_path or cli_name


def get_llm_command() -> tuple[str, list[str]]:
    """Get the implementation LLM command and arguments.

    Returns:
        Tuple of (command, args) for subprocess execution.
        Uses provider-specific CLI:
        - Anthropic: claude (Claude Code CLI)
        - Google: gemini (Gemini CLI)
        - OpenAI: codex (OpenAI Codex CLI)

    Note:
        Consider using resolve_llm_config() + build_llm_args() for more control.
    """
    llm_config = get_llm_config()
    impl_config = llm_config.get("implementation", {})

    provider = impl_config.get("provider", DEFAULT_PROVIDER)
    model = impl_config.get("model", DEFAULT_MODEL)

    cli = get_llm_cli(provider)
    args = build_llm_args({"provider": provider, "model": model})

    return cli, args


# API key environment variable names for each provider
# Used by build_subprocess_env() to strip keys when OAuth is configured
PROVIDER_API_KEY_ENV_VARS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GOOGLE_API_KEY",
}


def build_subprocess_env(
    auth_method: str,
    base_env: dict[str, str] | None = None,
    extra_env: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build subprocess environment with auth-aware API key handling.

    When auth_method is "oauth", API key environment variables are stripped
    to ensure the CLI uses OAuth authentication instead of API key billing.
    This prevents unexpected billing when a user has both OAuth configured
    in Obra and API keys set in their shell environment.

    Provider CLI auth priority (applies to all providers):
    1. API key environment variable (highest - API billing)
    2. OAuth token
    3. Subscription (lowest)

    By stripping API keys when OAuth is configured, we ensure Obra respects
    the user's auth_method configuration.

    Args:
        auth_method: Authentication method ("oauth" or "api_key")
        base_env: Base environment dict (defaults to os.environ.copy())
        extra_env: Additional environment variables to add

    Returns:
        Environment dict suitable for subprocess.run(env=...)

    Example:
        >>> # OAuth mode - API keys stripped
        >>> env = build_subprocess_env("oauth")
        >>> "ANTHROPIC_API_KEY" in env
        False

        >>> # API key mode - API keys preserved
        >>> env = build_subprocess_env("api_key")
        >>> "ANTHROPIC_API_KEY" in env  # if set in os.environ
        True

    Note:
        This is NON-DESTRUCTIVE. The original os.environ is never modified.
        Only the returned copy has API keys removed when auth_method is "oauth".
        Other processes (parallel Obra runs, direct API calls) are unaffected.
    """
    # Start with base environment (copy to avoid modifying original)
    if base_env is None:
        env = os.environ.copy()
    else:
        env = base_env.copy()

    # When OAuth is configured, strip API keys to prevent CLI from using them
    if auth_method == "oauth":
        stripped_keys = []
        for key_var in PROVIDER_API_KEY_ENV_VARS.values():
            if key_var in env:
                env.pop(key_var)
                stripped_keys.append(key_var)

        if stripped_keys:
            logger.info(
                "OAuth mode: Stripped API key env vars from subprocess environment: %s. "
                "CLI will use OAuth authentication.",
                ", ".join(stripped_keys),
            )
    else:
        # API key mode - log if API keys are present
        present_keys = [
            key_var
            for key_var in PROVIDER_API_KEY_ENV_VARS.values()
            if key_var in env
        ]
        if present_keys:
            logger.debug(
                "API key mode: Using API key authentication. Present: %s",
                ", ".join(present_keys),
            )

    # Add extra environment variables
    if extra_env:
        env.update(extra_env)

    return env


# Public exports
__all__ = [
    # Thinking constants
    "DEFAULT_THINKING_LEVEL",
    "THINKING_LEVELS",
    "THINKING_LEVEL_MAP",
    # Model constants
    "MODEL_SHORTCUTS",
    "XHIGH_SUPPORTED_MODELS",
    "MODEL_PROVIDER_PATTERNS",
    "MODEL_PROVIDER_PREFIXES",
    "TIER_NAMES",
    "TIER_FALLBACKS",
    "PROVIDER_TIER_DEFAULTS",
    # Model inference
    "infer_provider_from_model",
    # Thinking level functions
    "get_thinking_level_notes",
    "get_effective_thinking_value",
    # Model validation
    "validate_model",
    # Config resolution
    "resolve_llm_config",
    "resolve_tier_config",
    "get_provider_tier_defaults",
    "update_role_tiers_for_provider",
    "get_llm_config",
    "get_project_planning_config",
    "set_llm_config",
    "get_llm_display",
    # CLI building
    "get_thinking_keyword",
    "build_llm_args",
    "get_llm_cli",
    "get_llm_command",
    # Subprocess environment
    "PROVIDER_API_KEY_ENV_VARS",
    "build_subprocess_env",
]
