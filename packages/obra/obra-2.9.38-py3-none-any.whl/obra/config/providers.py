"""LLM provider definitions and health checking for Obra.

Handles provider configuration, CLI availability checks, and installation guidance.

Example:
    from obra.config.providers import check_provider_status, validate_provider_ready

    status = check_provider_status("anthropic")
    if not status.installed:
        print(f"Install with: {status.install_hint}")
"""

import shutil
from dataclasses import dataclass

# =============================================================================
# LLM Provider Definitions
# =============================================================================

# Supported LLM providers
LLM_PROVIDERS = {
    "anthropic": {
        "name": "Anthropic",
        "description": "Claude models",
        "cli": "claude",  # Claude Code CLI
        "models": ["default", "sonnet", "opus", "haiku"],
        "default_model": "default",
        "oauth_env_var": None,  # OAuth uses browser-based login
        "api_key_env_var": "ANTHROPIC_API_KEY",  # pragma: allowlist secret
    },
    "google": {
        "name": "Google",
        "description": "Gemini models",
        "cli": "gemini",  # Gemini CLI
        # Dec 2025: Gemini 3 preview + 2.5 family (gemini-2.0 deprecated)
        # See: docs/reference/llm-providers/gemini-cli-models.md
        "models": [
            "default",  # Same as "auto" - let system choose
            "auto",  # Gemini CLI's auto mode (explicit)
            "gemini-3-pro-preview",  # Latest Gemini 3 (preview)
            "gemini-2.5-pro",  # Production, 1M context
            "gemini-2.5-flash",  # Balance of speed/reasoning
            "gemini-2.5-flash-lite",  # Simple tasks, quick
        ],
        "default_model": "default",
        "oauth_env_var": None,  # OAuth uses browser-based login (gemini auth login)
        "api_key_env_var": "GEMINI_API_KEY",  # pragma: allowlist secret
    },
    "openai": {
        "name": "OpenAI",
        "description": "Codex / GPT models",
        "cli": "codex",  # OpenAI Codex CLI
        # Dec 2025: GPT-5.x family (models below 5.1 are deprecated)
        "models": [
            "default",
            "gpt-5.2",  # Latest frontier (400K context)
            "gpt-5.1-codex-max",  # Codex default, flagship
            "gpt-5.1-codex",  # Codex optimized
            "gpt-5.1-codex-mini",  # Faster, cheaper
            "gpt-5.1",  # General reasoning
        ],
        "default_model": "default",
        "oauth_env_var": None,  # OAuth uses browser-based login (codex --login)
        "api_key_env_var": "OPENAI_API_KEY",  # pragma: allowlist secret
    },
}

# Auth methods
LLM_AUTH_METHODS = {
    "oauth": {
        "name": "OAuth (Flat Rate)",
        "description": "Subscription-based, fixed monthly cost",
        "recommended_model": "default",
        "note": "Recommended - inherits provider's optimal model",
    },
    "api_key": {
        "name": "API Key (Token Billing)",
        "description": "Pay per token usage",
        "recommended_model": None,  # User should choose
        "note": "Warning: API Key method is currently untested",
    },
}

# Default provider settings
DEFAULT_PROVIDER = "anthropic"
DEFAULT_AUTH_METHOD = "oauth"
DEFAULT_MODEL = "default"

# =============================================================================
# Provider Health Check
# =============================================================================


@dataclass
class ProviderStatus:
    """Status of an LLM provider's CLI availability.

    Attributes:
        provider: Provider name (anthropic, openai, google)
        installed: Whether the CLI is installed and accessible
        cli_command: The CLI command name
        cli_path: Full path to CLI executable (if installed)
        install_hint: Installation instructions
        docs_url: Documentation URL
    """

    provider: str
    installed: bool
    cli_command: str
    cli_path: str | None = None
    install_hint: str = ""
    docs_url: str = ""


# Provider CLI information for health checking
PROVIDER_CLI_INFO: dict[str, dict[str, str]] = {
    "anthropic": {
        "cli": "claude",
        "install_hint": "npm install -g @anthropic-ai/claude-code",
        "docs_url": "https://docs.anthropic.com/en/docs/claude-code",
        "auth_hint": "claude login",
    },
    "openai": {
        "cli": "codex",
        "install_hint": "npm install -g @openai/codex",
        "docs_url": "https://platform.openai.com/docs/codex-cli",
        "auth_hint": "codex --login",
    },
    "google": {
        "cli": "gemini",
        "install_hint": "npm install -g @google/gemini-cli",
        "docs_url": "https://ai.google.dev/gemini-api/docs/gemini-cli",
        "auth_hint": "gemini auth login",
    },
}


def check_provider_status(provider: str) -> ProviderStatus:
    """Check if an LLM provider's CLI is installed and accessible.

    Uses shutil.which() to locate the CLI executable in PATH.

    Args:
        provider: Provider name (anthropic, openai, google)

    Returns:
        ProviderStatus with installation details

    Examples:
        >>> status = check_provider_status("anthropic")
        >>> if status.installed:
        ...     print(f"Claude CLI at: {status.cli_path}")
        ... else:
        ...     print(f"Install with: {status.install_hint}")
    """
    cli_info = PROVIDER_CLI_INFO.get(provider, {})
    cli_command_raw = cli_info.get("cli", LLM_PROVIDERS.get(provider, {}).get("cli", ""))
    cli_command = str(cli_command_raw)

    if not cli_command:
        return ProviderStatus(
            provider=provider,
            installed=False,
            cli_command="unknown",
            install_hint=f"Unknown provider: {provider}",
        )

    # Check if CLI is in PATH
    cli_path = shutil.which(cli_command)

    return ProviderStatus(
        provider=provider,
        installed=cli_path is not None,
        cli_command=cli_command,
        cli_path=cli_path,
        install_hint=cli_info.get("install_hint", ""),
        docs_url=cli_info.get("docs_url", ""),
    )


def validate_provider_ready(provider: str) -> None:
    """Validate that a provider's CLI is installed and ready.

    Raises ConfigurationError with installation hints if the CLI is not found.
    This provides a fail-fast check before attempting to use a provider.

    Args:
        provider: Provider name to validate (anthropic, openai, google)

    Raises:
        ConfigurationError: If provider CLI is not installed

    Example:
        >>> try:
        ...     validate_provider_ready("openai")
        ... except ConfigurationError as e:
        ...     print(f"Setup required: {e}")
    """
    from obra.exceptions import ConfigurationError  # noqa: PLC0415

    status = check_provider_status(provider)

    if not status.installed:
        provider_name = LLM_PROVIDERS.get(provider, {}).get("name", provider)
        cli_info = PROVIDER_CLI_INFO.get(provider, {})

        error_msg = f"{provider_name} CLI ({status.cli_command}) not found in PATH."
        details = []

        if status.install_hint:
            details.append(f"Install with: {status.install_hint}")

        auth_hint = cli_info.get("auth_hint")
        if auth_hint:
            details.append(f"Then authenticate: {auth_hint}")

        if status.docs_url:
            details.append(f"See: {status.docs_url}")

        if details:
            error_msg = f"{error_msg}\n\n" + "\n".join(details)

        raise ConfigurationError(error_msg)


# Public exports
__all__ = [
    # Provider definitions
    "LLM_PROVIDERS",
    "LLM_AUTH_METHODS",
    "DEFAULT_PROVIDER",
    "DEFAULT_AUTH_METHOD",
    "DEFAULT_MODEL",
    # Provider health check
    "ProviderStatus",
    "PROVIDER_CLI_INFO",
    "check_provider_status",
    "validate_provider_ready",
]
