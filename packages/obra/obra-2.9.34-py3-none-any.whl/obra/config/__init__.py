"""Configuration management for Obra.

Handles terms acceptance state and client configuration stored in
~/.obra/client-config.yaml.

Example:
    from obra.config import load_config, save_config, get_api_base_url

    config = load_config()
    api_url = get_api_base_url()
"""

from datetime import UTC, datetime
from pathlib import Path

# =============================================================================
# Eager imports: Constants and core lightweight values
# =============================================================================

# Legal document versions - must match bundled documents
TERMS_VERSION = "2.1"
PRIVACY_VERSION = "1.3"

# Config file path
CONFIG_PATH = Path.home() / ".obra" / "client-config.yaml"

# Firebase configuration
# SEC-002: This is a PUBLIC Firebase Web API Key - intentionally included in client code.
#
# SECURITY NOTE: This is NOT a secret. Firebase Web API Keys are designed to be
# public and embedded in client applications. They are:
# - Safe to commit to version control
# - Safe to distribute in client packages
# - Restricted by Firebase Security Rules (not by key secrecy)
#
# This key is used for:
# - Custom token → ID token exchange via Firebase Auth REST API
# - Client-side Firebase SDK initialization
#
# Actual security is enforced by:
# - Firebase Security Rules (Firestore/Storage)
# - Cloud Functions authentication middleware
# - Server-side Firebase Admin SDK with service account credentials
#
# Project: obra-205b0
# Reference: https://firebase.google.com/docs/projects/api-keys
FIREBASE_API_KEY = "AIzaSyDHQNxR_4BQvK_W_i83H2hNH4p2OKFi2wM"  # pragma: allowlist secret

# =============================================================================
# Lazy loading registry (PEP 562)
# =============================================================================

_LAZY_IMPORTS = {
    # From loaders.py - Config I/O and getters
    "DEFAULT_API_BASE_URL": ".loaders",
    "DEFAULT_LLM_TIMEOUT": ".loaders",
    "DEFAULT_AGENT_EXECUTION_TIMEOUT": ".loaders",
    "DEFAULT_REVIEW_AGENT_TIMEOUT": ".loaders",
    "DEFAULT_MAX_ITERATIONS": ".loaders",
    "DEFAULT_NETWORK_TIMEOUT": ".loaders",
    "DEFAULT_LLM_API_TIMEOUT": ".loaders",
    "DEFAULT_CHECK_FOR_UPDATES": ".loaders",
    "DEFAULT_UPDATE_NOTIFICATION_COOLDOWN_MINUTES": ".loaders",
    "get_config_path": ".loaders",
    "load_config": ".loaders",
    "save_config": ".loaders",
    "get_api_base_url": ".loaders",
    "get_llm_timeout": ".loaders",
    "get_agent_execution_timeout": ".loaders",
    "get_review_agent_timeout": ".loaders",
    "get_heartbeat_interval": ".loaders",
    "get_heartbeat_initial_delay": ".loaders",
    "get_max_iterations": ".loaders",
    "get_default_project_override": ".loaders",
    "get_isolated_mode": ".loaders",
    "set_isolated_mode": ".loaders",
    "get_check_for_updates": ".loaders",
    "get_update_notification_cooldown_minutes": ".loaders",
    "get_project_detection_empty_threshold": ".loaders",
    "get_project_detection_existing_threshold": ".loaders",
    "get_project_detection_enabled": ".loaders",
    "get_prompt_retention": ".loaders",
    # From providers.py - LLM provider definitions and health check
    "LLM_PROVIDERS": ".providers",
    "LLM_AUTH_METHODS": ".providers",
    "DEFAULT_PROVIDER": ".providers",
    "DEFAULT_AUTH_METHOD": ".providers",
    "DEFAULT_MODEL": ".providers",
    "ProviderStatus": ".providers",
    "PROVIDER_CLI_INFO": ".providers",
    "check_provider_status": ".providers",
    "validate_provider_ready": ".providers",
    # From llm.py - LLM config resolution and CLI building
    "DEFAULT_THINKING_LEVEL": ".llm",
    "THINKING_LEVELS": ".llm",
    "THINKING_LEVEL_MAP": ".llm",
    "MODEL_SHORTCUTS": ".llm",
    "XHIGH_SUPPORTED_MODELS": ".llm",
    "MODEL_PROVIDER_PATTERNS": ".llm",
    "MODEL_PROVIDER_PREFIXES": ".llm",
    "infer_provider_from_model": ".llm",
    "get_thinking_level_notes": ".llm",
    "get_effective_thinking_value": ".llm",
    "validate_model": ".llm",
    "resolve_llm_config": ".llm",
    "get_llm_config": ".llm",
    "set_llm_config": ".llm",
    "get_llm_display": ".llm",
    "get_thinking_keyword": ".llm",
    "build_llm_args": ".llm",
    "get_llm_cli": ".llm",
    "get_llm_command": ".llm",
    "PROVIDER_API_KEY_ENV_VARS": ".llm",
    "build_subprocess_env": ".llm",
    # From auth.py - Firebase auth state
    "get_firebase_uid": ".auth",
    "get_user_email": ".auth",
    "get_auth_token": ".auth",
    "get_refresh_token": ".auth",
    "get_auth_provider": ".auth",
    "is_authenticated": ".auth",
    "save_firebase_auth": ".auth",
    "clear_firebase_auth": ".auth",
}


def __getattr__(name: str):
    """Lazy load heavy components on first access."""
    if name in _LAZY_IMPORTS:
        import importlib

        module = importlib.import_module(_LAZY_IMPORTS[name], __name__)
        return getattr(module, name)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


# =============================================================================
# Terms acceptance functions (kept in __init__.py - core, lightweight)
# =============================================================================


def get_terms_acceptance() -> dict | None:
    """Get stored terms acceptance data.

    Returns:
        Dictionary with terms acceptance info, or None if not accepted:
        {
            "version": "2.1",
            "privacy_version": "1.3",
            "accepted_at": "2025-12-03T12:00:00+00:00"
        }
    """
    from .loaders import load_config  # noqa: PLC0415

    config = load_config()
    return config.get("terms_accepted")


def is_terms_accepted() -> bool:
    """Check if current terms version has been accepted.

    Returns:
        True if terms are accepted and version matches current,
        False otherwise
    """
    acceptance = get_terms_acceptance()

    if not acceptance:
        return False

    # Check if accepted version matches current version
    accepted_version = acceptance.get("version")
    return accepted_version == TERMS_VERSION


def needs_reacceptance() -> bool:
    """Check if terms need to be re-accepted due to version change.

    Returns:
        True if terms were previously accepted but version changed,
        False if never accepted or current version is accepted
    """
    acceptance = get_terms_acceptance()

    if not acceptance:
        return False  # Never accepted, not "re-acceptance"

    accepted_version = acceptance.get("version")
    return accepted_version != TERMS_VERSION


def save_terms_acceptance(
    version: str = TERMS_VERSION,
    privacy_version: str = PRIVACY_VERSION,
) -> None:
    """Save terms acceptance to config file.

    Args:
        version: Terms version being accepted (default: current TERMS_VERSION)
        privacy_version: Privacy policy version (default: current PRIVACY_VERSION)
    """
    from .loaders import load_config, save_config  # noqa: PLC0415

    config = load_config()

    config["terms_accepted"] = {
        "version": version,
        "privacy_version": privacy_version,
        "accepted_at": datetime.now(UTC).isoformat(),
    }

    save_config(config)


def clear_terms_acceptance() -> None:
    """Clear stored terms acceptance (for testing/reset)."""
    from .loaders import load_config, save_config  # noqa: PLC0415

    config = load_config()

    if "terms_accepted" in config:
        del config["terms_accepted"]
        save_config(config)


# =============================================================================
# Public exports - complete for IDE/type checker support
# =============================================================================

__all__ = [
    "CONFIG_PATH",
    "DEFAULT_AGENT_EXECUTION_TIMEOUT",
    # Lazy: loaders.py
    "DEFAULT_API_BASE_URL",
    "DEFAULT_AUTH_METHOD",
    "DEFAULT_CHECK_FOR_UPDATES",
    "DEFAULT_LLM_API_TIMEOUT",
    "DEFAULT_LLM_TIMEOUT",
    "DEFAULT_MAX_ITERATIONS",
    "DEFAULT_MODEL",
    "DEFAULT_NETWORK_TIMEOUT",
    "DEFAULT_PROVIDER",
    "DEFAULT_REVIEW_AGENT_TIMEOUT",
    # Lazy: llm.py
    "DEFAULT_THINKING_LEVEL",
    "DEFAULT_UPDATE_NOTIFICATION_COOLDOWN_MINUTES",
    "FIREBASE_API_KEY",
    "LLM_AUTH_METHODS",
    # Lazy: providers.py
    "LLM_PROVIDERS",
    "MODEL_PROVIDER_PATTERNS",
    "MODEL_PROVIDER_PREFIXES",
    "MODEL_SHORTCUTS",
    "PRIVACY_VERSION",
    "PROVIDER_API_KEY_ENV_VARS",
    "PROVIDER_CLI_INFO",
    # Eager constants
    "TERMS_VERSION",
    "THINKING_LEVELS",
    "THINKING_LEVEL_MAP",
    "XHIGH_SUPPORTED_MODELS",
    "ProviderStatus",
    "build_llm_args",
    "build_subprocess_env",
    "check_provider_status",
    "clear_firebase_auth",
    "clear_terms_acceptance",
    "get_agent_execution_timeout",
    "get_api_base_url",
    "get_auth_provider",
    "get_auth_token",
    "get_check_for_updates",
    "get_config_path",
    "get_default_project_override",
    "get_effective_thinking_value",
    # Lazy: auth.py
    "get_firebase_uid",
    "get_heartbeat_initial_delay",
    "get_heartbeat_interval",
    "get_isolated_mode",
    "get_llm_cli",
    "get_llm_command",
    "get_llm_config",
    "get_llm_display",
    "get_llm_timeout",
    "get_max_iterations",
    "get_refresh_token",
    "get_review_agent_timeout",
    # Terms functions (in __init__.py)
    "get_terms_acceptance",
    "get_thinking_keyword",
    "get_thinking_level_notes",
    "get_update_notification_cooldown_minutes",
    "get_user_email",
    "infer_provider_from_model",
    "is_authenticated",
    "is_terms_accepted",
    "load_config",
    "needs_reacceptance",
    "resolve_llm_config",
    "save_config",
    "save_firebase_auth",
    "save_terms_acceptance",
    "set_isolated_mode",
    "set_llm_config",
    "validate_model",
    "validate_provider_ready",
]
