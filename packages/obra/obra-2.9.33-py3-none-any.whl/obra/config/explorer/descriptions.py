"""Setting descriptions for the Configuration Explorer.

Provides human-readable descriptions for all configuration options,
used for inline documentation in the TUI.
"""

# Mapping from dot-notation path to description text.
# Descriptions should be concise but informative, explaining what the
# setting does and any important considerations.
CONFIG_DESCRIPTIONS: dict[str, str] = {
    # ==========================================================================
    # Advanced / Diagnostics
    # ==========================================================================
    "advanced": "Advanced and diagnostic settings (use with care).",
    "advanced.monitoring": "File/output monitoring and production logging settings.",
    "advanced.logging": "CLI logging settings (level, format, file rotation).",
    "advanced.debug": "Development/debug flags (disable in production).",
    "advanced.audit": "Audit logging settings for destructive operations.",
    "advanced.metrics": "Work unit metrics reporting configuration.",
    "advanced.observability": "Observability event emission settings.",
    # ==========================================================================
    # LLM Settings - Local Config
    # ==========================================================================
    "llm": "LLM provider configuration for orchestration and implementation layers.",
    "llm.orchestrator": (
        "Settings for the orchestration layer LLM (planning, validation, decisions)."
    ),
    "llm.orchestrator.provider": (
        "LLM provider for the orchestration layer. "
        "Handles planning, validation, and decision-making. "
        "Options: anthropic (Claude), openai (OpenAI Codex), "
        "google (Gemini), ollama (local models)."
    ),
    "llm.orchestrator.model": (
        "Model to use for orchestration. "
        "Options vary by provider: "
        "Anthropic: sonnet, opus, haiku | "
        "Google: gemini-2.5-pro, gemini-2.5-flash, gemini-3-flash-preview | "
        "OpenAI: codex, gpt-5.2, gpt-5.2-codex, gpt-5.1-codex-max, gpt-5.1-codex-mini, gpt-5.1 | "
        "Ollama: qwen2.5-coder variants, phi3:mini. "
        "'default' is recommended."
    ),
    "llm.orchestrator.auth_method": (
        "Authentication method for the orchestration LLM. "
        "'oauth' uses flat-rate billing through Obra subscription. "
        "'api_key' bills directly to your provider account (pay-per-token)."
    ),
    "llm.orchestrator.tiers": (
        "Tiered model configuration for orchestrator adaptive complexity handling. "
        "Define fast/medium/high tiers to automatically select appropriate models "
        "based on task complexity. "
        "Tiers use the orchestrator provider (llm.orchestrator.provider)."
    ),
    "llm.orchestrator.tiers.fast": (
        "Fast tier model for orchestrator - simple, low-complexity tasks. "
        "Use lightweight models (e.g., Anthropic: 'haiku', "
        "OpenAI: 'gpt-5.1-codex-mini', Google: 'gemini-2.5-flash'). "
        "Dropdown options match the orchestrator provider."
    ),
    "llm.orchestrator.tiers.medium": (
        "Medium tier model for orchestrator - moderate-complexity tasks. "
        "Use balanced models (e.g., Anthropic: 'sonnet', "
        "OpenAI: 'gpt-5.1-codex-max', Google: 'gemini-2.5-pro'). "
        "Dropdown options match the orchestrator provider."
    ),
    "llm.orchestrator.tiers.high": (
        "High tier model for orchestrator - complex, critical tasks. "
        "Use frontier models (e.g., Anthropic: 'opus', "
        "OpenAI: 'gpt-5.1-codex-max', Google: 'gemini-2.5-pro'). "
        "Dropdown options match the orchestrator provider."
    ),
    "llm.implementation": (
        "Settings for the implementation layer LLM (code generation, file modifications)."
    ),
    "llm.implementation.provider": (
        "LLM provider for the implementation layer. "
        "Handles code generation and file modifications. "
        "Options: anthropic (Claude Code), openai (OpenAI Codex), "
        "google (Gemini CLI), ollama (local models)."
    ),
    "llm.implementation.model": (
        "Model to use for implementation. "
        "Options vary by provider: "
        "Anthropic: sonnet, opus, haiku | "
        "Google: gemini-2.5-pro, gemini-2.5-flash, gemini-3-flash-preview | "
        "OpenAI: codex, gpt-5.2, gpt-5.2-codex, gpt-5.1-codex-max, gpt-5.1-codex-mini, gpt-5.1 | "
        "Ollama: qwen2.5-coder variants, phi3:mini. "
        "'default' is recommended."
    ),
    "llm.implementation.auth_method": (
        "Authentication method for the implementation LLM. "
        "'oauth' uses your provider's CLI authentication. "
        "'api_key' requires setting the provider's API key environment variable."
    ),
    "llm.implementation.tiers": (
        "Tiered model configuration for implementation adaptive complexity handling. "
        "Define fast/medium/high tiers to automatically select appropriate models "
        "based on task complexity. "
        "Tiers use the implementation provider (llm.implementation.provider)."
    ),
    "llm.implementation.tiers.fast": (
        "Fast tier model for implementation - simple, low-complexity tasks. "
        "Use lightweight models (e.g., Anthropic: 'haiku', "
        "OpenAI: 'gpt-5.1-codex-mini', Google: 'gemini-2.5-flash'). "
        "Dropdown options match the implementation provider."
    ),
    "llm.implementation.tiers.medium": (
        "Medium tier model for implementation - moderate-complexity tasks. "
        "Use balanced models (e.g., Anthropic: 'sonnet', "
        "OpenAI: 'gpt-5.1-codex-max', Google: 'gemini-2.5-pro'). "
        "Dropdown options match the implementation provider."
    ),
    "llm.implementation.tiers.high": (
        "High tier model for implementation - complex, critical tasks. "
        "Use frontier models (e.g., Anthropic: 'opus', "
        "OpenAI: 'gpt-5.1-codex-max', Google: 'gemini-2.5-pro'). "
        "Dropdown options match the implementation provider."
    ),
    # ==========================================================================
    # LLM Git Repository Settings (GIT-HARD-001)
    # ==========================================================================
    "llm.git": "Git repository validation settings for LLM execution.",
    "llm.git.skip_check": (
        "Skip git repository validation before LLM execution. "
        "Auto-enabled when using OpenAI Codex (required for Codex trust compatibility). "
        "When false, Obra requires projects to be in a git repository "
        "for change tracking and safe rollbacks. "
        "You can manually override this setting if needed."
    ),
    "llm.git.auto_init": (
        "Auto-initialize git repository if not present. "
        "When true, Obra will run 'git init' and create a default .gitignore "
        "if the project directory is not already a git repository. "
        "Useful for new projects. Default: false."
    ),
    # ==========================================================================
    # Planning - Scaffolded Intent Enrichment
    # ==========================================================================
    "planning": "Planning configuration for derivation and intent enrichment.",
    "planning.scaffolded": "Scaffolded intent enrichment stages before derivation.",
    "planning.scaffolded.enabled": (
        "Enable scaffolded intent enrichment (assumptions, analogues, brief, review)."
    ),
    "planning.scaffolded.always_on": (
        "When enabled, always run scaffolded stages for derive (unless --no-scaffolded)."
    ),
    "planning.scaffolded.stages": "Stage-specific configuration for scaffolded planning.",
    "planning.scaffolded.stages.assumptions": (
        "Stage A: gather assumptions and non-inferable questions."
    ),
    "planning.scaffolded.stages.assumptions.model_tier": (
        "Model tier for the assumptions stage (fast/medium/high)."
    ),
    "planning.scaffolded.stages.assumptions.reasoning_level": (
        "Reasoning level for the assumptions stage."
    ),
    "planning.scaffolded.stages.assumptions.max_passes": (
        "Max attempts for the assumptions stage."
    ),
    "planning.scaffolded.stages.assumptions.timeout_s": (
        "Timeout in seconds for the assumptions stage."
    ),
    "planning.scaffolded.stages.assumptions.max_questions": (
        "Max non-inferable questions to ask in interactive runs."
    ),
    "planning.scaffolded.stages.analogues": (
        "Stage B: domain inference and expert-aligned intent updates."
    ),
    "planning.scaffolded.stages.analogues.model_tier": (
        "Model tier for the analogues stage (fast/medium/high)."
    ),
    "planning.scaffolded.stages.analogues.reasoning_level": (
        "Reasoning level for the analogues stage."
    ),
    "planning.scaffolded.stages.analogues.max_passes": (
        "Max attempts for the analogues stage."
    ),
    "planning.scaffolded.stages.analogues.timeout_s": (
        "Timeout in seconds for the analogues stage."
    ),
    "planning.scaffolded.stages.brief": (
        "Stage C: consolidate a clean intent brief."
    ),
    "planning.scaffolded.stages.brief.model_tier": (
        "Model tier for the brief stage (fast/medium/high)."
    ),
    "planning.scaffolded.stages.brief.reasoning_level": (
        "Reasoning level for the brief stage."
    ),
    "planning.scaffolded.stages.brief.max_passes": (
        "Max attempts for the brief stage."
    ),
    "planning.scaffolded.stages.brief.timeout_s": (
        "Timeout in seconds for the brief stage."
    ),
    "planning.scaffolded.stages.derive": (
        "Stage D: derive plan from enriched intent."
    ),
    "planning.scaffolded.stages.derive.model_tier": (
        "Model tier for the derive stage (fast/medium/high)."
    ),
    "planning.scaffolded.stages.derive.reasoning_level": (
        "Reasoning level for the derive stage."
    ),
    "planning.scaffolded.stages.derive.max_passes": (
        "Max attempts for the derive stage."
    ),
    "planning.scaffolded.stages.derive.timeout_s": (
        "Timeout in seconds for the derive stage."
    ),
    "planning.scaffolded.stages.review": (
        "Stage E: expert-aligned plan review for scope creep."
    ),
    "planning.scaffolded.stages.review.model_tier": (
        "Model tier for the review stage (fast/medium/high)."
    ),
    "planning.scaffolded.stages.review.reasoning_level": (
        "Reasoning level for the review stage."
    ),
    "planning.scaffolded.stages.review.max_passes": (
        "Max attempts for the review stage."
    ),
    "planning.scaffolded.stages.review.timeout_s": (
        "Timeout in seconds for the review stage."
    ),
    "planning.scaffolded.non_inferable_categories": (
        "Categories that require user input when missing (interactive only)."
    ),
    "planning.scaffolded.diff": "Intent diff output settings.",
    "planning.scaffolded.diff.path_template": (
        "Template for intent diff path (supports {intent_id})."
    ),
    "planning.scaffolded.diff.retention": "Retention policy for intent diffs.",
    "planning.scaffolded.diff.retention.max_age_days": (
        "Max age in days for intent diff retention."
    ),
    "planning.scaffolded.diff.retention.max_files": (
        "Max diff files to retain."
    ),
    "planning.scaffolded.artifacts": "Stage artifact output settings.",
    "planning.scaffolded.artifacts.dir": "Directory for scaffolded stage artifacts.",
    "planning.scaffolded.artifacts.retention": "Retention policy for stage artifacts.",
    "planning.scaffolded.artifacts.retention.max_age_days": (
        "Max age in days for stage artifacts."
    ),
    "planning.scaffolded.artifacts.retention.max_files": (
        "Max artifacts to retain."
    ),
    "planning.scaffolded.analogue_cache": "Analogue cache paths for expert guidance.",
    "planning.scaffolded.analogue_cache.global_path": (
        "Global analogue cache path (shared across projects)."
    ),
    "planning.scaffolded.analogue_cache.project_path": (
        "Project-scoped analogue cache path."
    ),
    "planning.scaffolded.telemetry": "Telemetry output settings for scaffolded runs.",
    "planning.scaffolded.telemetry.enabled": "Enable local telemetry logging.",
    "planning.scaffolded.telemetry.include_content": (
        "Include raw model outputs in telemetry logs."
    ),
    "planning.scaffolded.telemetry.output_path": "Telemetry JSONL output path.",
    # ==========================================================================
    # Local Settings
    # ==========================================================================
    "api_base_url": (
        "Obra SaaS API endpoint URL. "
        "Only change this for testing, self-hosted instances, or staging environments. "
        "Default: production Obra API."
    ),
    "llm_timeout": (
        "Maximum time in seconds to wait for LLM responses. "
        "Increase for complex tasks that may take longer. "
        "Default: 1800 (30 minutes)."
    ),
    # ==========================================================================
    # Orchestration Settings - Timeouts
    # ==========================================================================
    "orchestration": "Orchestration settings for workflow execution and agent management.",
    "orchestration.timeouts": "Timeout configurations for various orchestration operations.",
    "orchestration.timeouts.agent_execution_s": (
        "Timeout in seconds for agent execution (execute and fix handlers). "
        "Controls how long Obra waits for agent task completion. "
        "Can be overridden with OBRA_AGENT_EXECUTION_TIMEOUT environment variable. "
        "Default: 5400 (90 minutes)."
    ),
    "orchestration.timeouts.review_agent_s": (
        "Timeout in seconds for review agents (security, testing, code quality, documentation). "
        "Controls how long each review agent runs before timing out. "
        "Can be overridden with OBRA_REVIEW_AGENT_TIMEOUT environment variable. "
        "Default: 1800 (30 minutes)."
    ),
    "orchestration.timeouts.cli_runner_s": (
        "Timeout in seconds for CLI LLM runner when no explicit timeout is provided. "
        "Fallback timeout for LLM operations via CLI. "
        "Default: 7200 (120 minutes)."
    ),
    # ==========================================================================
    # Orchestration Settings - Progress Visibility
    # ==========================================================================
    "orchestration.progress": "Progress visibility settings for execution monitoring.",
    "orchestration.progress.heartbeat_interval_s": (
        "Interval in seconds between heartbeat progress messages during agent execution. "
        "Automatically scaled by verbosity: QUIET (3x), PROGRESS (1x), DETAIL (0.5x). "
        "Can be overridden with OBRA_HEARTBEAT_INTERVAL environment variable. "
        "Default: 60 seconds."
    ),
    "orchestration.progress.heartbeat_initial_delay_s": (
        "Delay in seconds before first heartbeat message is shown. "
        "Prevents noise for quick tasks. Set to 0 for immediate heartbeat visibility. "
        "Can be overridden with OBRA_HEARTBEAT_INITIAL_DELAY environment variable. "
        "Default: 30 seconds."
    ),
    "terms_accepted": "Terms of Service and Privacy Policy acceptance state.",
    "terms_accepted.version": "Version of Terms of Service that was accepted.",
    "terms_accepted.privacy_version": "Version of Privacy Policy that was accepted.",
    "terms_accepted.accepted_at": "Timestamp when terms were accepted.",
    # ==========================================================================
    # Auth Display Fields (read-only)
    # ==========================================================================
    "user_email": "Your authenticated email address (read-only).",
    "firebase_uid": (
        "Your unique Obra user identifier (read-only). "
        "This ID is used to identify your account in the Obra system."
    ),
    "auth_provider": (
        "Authentication provider used for sign-in (read-only). Examples: google.com, github.com."
    ),
    "display_name": "Your display name from the authentication provider (read-only).",
    "user_id": "Your email address used as user identifier (read-only).",
    # ==========================================================================
    # Server Settings - Features
    # ==========================================================================
    "features": "Feature flags and capabilities that can be enabled or disabled.",
    "features.performance_control": "Performance and resource management settings.",
    "features.performance_control.budgets": "Unified budget control for orchestration sessions.",
    "features.performance_control.budgets.enabled": (
        "Enable unified budget control for orchestration sessions. "
        "When enabled, Obra tracks time, iteration, token, and progress budgets. "
        "Sessions pause when budgets are exceeded, preventing runaway costs."
    ),
    "features.performance_control.budgets.defaults": (
        "Default budget limits when budgets are enabled."
    ),
    "features.performance_control.budgets.defaults.time_minutes": (
        "Default time budget in minutes for a single orchestration session. "
        "Session pauses when this limit is reached."
    ),
    "features.performance_control.budgets.defaults.iterations": (
        "Default iteration budget (number of LLM calls) per session. "
        "Helps prevent infinite loops or excessive API usage."
    ),
    "features.quality_automation": "Quality automation tools and agents.",
    "features.quality_automation.enabled": (
        "Master toggle for quality automation features. "
        "When disabled, all quality automation agents are inactive regardless of individual settings."
    ),
    "features.quality_automation.agents": "Specialized agents for automated tasks.",
    "features.quality_automation.agents.security_audit": (
        "Enable automatic security vulnerability scanning. "
        "Runs OWASP Top 10 checks on code changes. "
        "Recommended for production codebases."
    ),
    "features.quality_automation.agents.rca_agent": (
        "Enable root cause analysis agent. "
        "Automatically investigates test failures, errors, and unexpected behavior. "
        "Provides detailed analysis reports."
    ),
    "features.quality_automation.agents.doc_audit": (
        "Enable documentation audit agent. "
        "Checks documentation for accuracy, completeness, and staleness. "
        "Uses ROT methodology (Redundant, Outdated, Trivial)."
    ),
    "features.quality_automation.agents.test_generation": (
        "Enable test generation agent. "
        "Creates or updates tests based on code changes and objectives."
    ),
    "features.quality_automation.agents.test_execution": (
        "Enable test execution agent. "
        "Runs relevant test suites during review and verification."
    ),
    "features.quality_automation.agents.code_review": (
        "Enable automatic code review agent. "
        "Reviews code changes for best practices, potential issues, and style consistency."
    ),
    # Alternative paths for quality_automation features (direct placement in some configs)
    "features.quality_automation.code_review": (
        "Enable automatic code review. "
        "Reviews code changes for best practices, potential issues, and style consistency."
    ),
    "features.quality_automation.advanced_planning": (
        "Enable advanced planning capabilities. "
        "Includes derivative plan architecture and enhanced task breakdown."
    ),
    "features.quality_automation.documentation_governance": (
        "Enable documentation governance (DG-001). "
        "Keeps documentation synchronized with code through INDEX.yaml coupling."
    ),
    "features.advanced_planning": "Advanced planning capabilities.",
    "features.advanced_planning.enabled": (
        "Enable advanced planning features. "
        "Includes derivative plan architecture and enhanced task breakdown capabilities."
    ),
    "features.documentation_governance": "Documentation governance settings.",
    "features.documentation_governance.enabled": (
        "Enable documentation governance (DG-001). "
        "Keeps documentation synchronized with code through INDEX.yaml coupling."
    ),
    "features.workflow": "Workflow orchestration settings.",
    "features.workflow.enabled": (
        "Enable pattern-guided workflow execution. "
        "Uses ProcessGuardian for validation and guided execution patterns."
    ),
    "features.workflow.process_patterns": "Process pattern configurations for workflow execution.",
    # ==========================================================================
    # Server Settings - Presets
    # ==========================================================================
    "preset": (
        "Configuration preset name. "
        "Presets are curated configurations for different use cases. "
        "Your overrides are applied on top of the preset defaults."
    ),
    # ==========================================================================
    # Advanced Settings
    # ==========================================================================
    "advanced": "Expert settings for advanced users. Change with caution.",
    "advanced.debug_mode": (
        "Enable debug mode for verbose logging. "
        "Useful for troubleshooting but produces much more output."
    ),
    "advanced.experimental_features": (
        "Enable experimental features that may be unstable. "
        "These features are in development and may change or be removed."
    ),
    "advanced.telemetry": "Telemetry and usage analytics settings.",
    "advanced.telemetry.enabled": (
        "Enable anonymous usage telemetry. "
        "Helps improve Obra by sending anonymized usage statistics. "
        "No personal data or code is ever sent."
    ),
}

# Metadata for configuration paths (used by CLI and TUI helpers)
# Currently supports: sensitive (bool)
CONFIG_METADATA: dict[str, dict[str, object]] = {
    # Auth/session secrets
    "auth_token": {"sensitive": True},
    "refresh_token": {"sensitive": True},
    "firebase_uid": {"sensitive": True},
    "firebase_api_key": {"sensitive": True},
    "token_expires_at": {"sensitive": True},
    # Core orchestration toggles - locked to prevent breaking the system
    "features.core_orchestration.enabled": {
        "locked": True,
        "lock_reason": "Core system setting; use presets instead.",
    },
    "features.core_orchestration.state_manager": {
        "locked": True,
        "lock_reason": "Core system setting; disabling breaks state management.",
    },
    "features.core_orchestration.orchestrator": {
        "locked": True,
        "lock_reason": "Core system setting; disabling breaks orchestration.",
    },
    "features.core_orchestration.llm_provider": {
        "locked": True,
        "lock_reason": "Core system setting; disabling breaks provider selection.",
    },
    "features.core_orchestration.implementation_agent": {
        "locked": True,
        "lock_reason": "Core system setting; disabling breaks implementation.",
    },
    "features.core_orchestration.config_loading": {
        "locked": True,
        "lock_reason": "Core system setting; disabling breaks config loading.",
    },
    "features.core_orchestration.response_validation": {
        "locked": True,
        "lock_reason": "Core system setting; disabling breaks validation.",
    },
    "features.core_orchestration.context_awareness": {
        "locked": True,
        "lock_reason": "Core system setting; disabling breaks context handling.",
    },
    "features.core_orchestration.working_memory": {
        "locked": True,
        "lock_reason": "Core system setting; disabling breaks working memory.",
    },
}


def get_description(path: str) -> str | None:
    """Get description for a configuration path.

    Args:
        path: Dot-notation path like "llm.orchestrator.provider"

    Returns:
        Description string or None if not found
    """
    return CONFIG_DESCRIPTIONS.get(path)


def is_sensitive(path: str) -> bool:
    """Check if a configuration path is marked as sensitive.

    Args:
        path: Dot-notation path like "llm.orchestrator.provider"

    Returns:
        True if the path should be redacted by default
    """
    meta = CONFIG_METADATA.get(path)
    if meta:
        return bool(meta.get("sensitive"))

    # Fallback pattern checks for unknown paths
    if path.startswith(("auth.", "providers.")):
        return True
    return bool(path.endswith((".api_key", ".token")))


def is_locked(path: str) -> bool:
    """Check if a configuration path is locked (read-only)."""
    meta = CONFIG_METADATA.get(path)
    if meta:
        return bool(meta.get("locked"))
    return False


def get_lock_reason(path: str) -> str | None:
    """Return lock reason for a path, if any."""
    meta = CONFIG_METADATA.get(path)
    if meta:
        reason = meta.get("lock_reason")
        if isinstance(reason, str):
            return reason
    return None


def get_all_paths() -> list[str]:
    """Get all documented configuration paths.

    Returns:
        List of all paths that have descriptions
    """
    return list(CONFIG_DESCRIPTIONS.keys())


# Provider-specific model choices - DYNAMICALLY LOADED from obra.model_registry
# This ensures config command always shows correct, up-to-date model lists
def _load_provider_model_choices() -> dict[str, list[str]]:
    """Load model choices from authoritative MODEL_REGISTRY.

    Returns dict mapping provider name to list of usable model IDs.
    Smart alias filtering:
    - If alias target exists in registry: Hide alias (avoid duplicates)
    - If alias target doesn't exist: Show FIRST alias only (prefer shorter names)
    """
    from obra.model_registry import MODEL_REGISTRY, ModelStatus

    choices: dict[str, list[str]] = {}
    for provider_name, provider_config in MODEL_REGISTRY.items():
        # Add "default" as first option for all providers
        model_list = ["default"]

        # Track which alias targets we've already included
        seen_targets = set()

        # Add all non-deprecated models with smart alias filtering
        for model_id, model_info in provider_config.models.items():
            # Skip deprecated models
            if model_info.status == ModelStatus.DEPRECATED:
                continue

            # Smart alias handling
            if hasattr(model_info, "resolves_to") and model_info.resolves_to is not None:
                target = model_info.resolves_to

                # If target exists in registry, skip this alias (avoid duplicates)
                if target in provider_config.models:
                    continue

                # If we've already shown an alias for this target, skip this one
                if target in seen_targets:
                    continue

                # Mark this target as seen
                seen_targets.add(target)

            model_list.append(model_id)

        choices[provider_name] = model_list

    return choices


# Lazy-loaded to avoid circular imports
_PROVIDER_MODEL_CHOICES_CACHE: dict[str, list[str]] | None = None


def _get_provider_model_choices() -> dict[str, list[str]]:
    """Get cached provider model choices, loading on first access."""
    global _PROVIDER_MODEL_CHOICES_CACHE
    if _PROVIDER_MODEL_CHOICES_CACHE is None:
        _PROVIDER_MODEL_CHOICES_CACHE = _load_provider_model_choices()
    return _PROVIDER_MODEL_CHOICES_CACHE


# Mapping of paths to their choices (for enum types)
# Note: model choices are dynamically determined by provider via MODEL_REGISTRY
# Provider list is also dynamically loaded from MODEL_REGISTRY
def _get_provider_list() -> list[str]:
    """Get list of supported providers from MODEL_REGISTRY.

    Excludes Ollama as it's for advanced local use only.
    """
    from obra.model_registry import get_provider_names
    providers = get_provider_names()
    # Hide Ollama from config UI (advanced users can set via YAML)
    return [p for p in providers if p != "ollama"]


CONFIG_CHOICES: dict[str, list[str] | None] = {
    # Providers loaded dynamically - will be populated by get_choices()
    "llm.orchestrator.provider": None,
    "llm.orchestrator.model": ["default"],  # Fallback - dynamically populated by provider
    "llm.orchestrator.auth_method": ["oauth", "api_key"],
    "llm.orchestrator.tiers.fast": ["default"],  # Dynamically populated by orchestrator provider
    "llm.orchestrator.tiers.medium": ["default"],  # Dynamically populated by orchestrator provider
    "llm.orchestrator.tiers.high": ["default"],  # Dynamically populated by orchestrator provider
    "llm.implementation.provider": None,
    "llm.implementation.model": ["default"],  # Fallback - dynamically populated by provider
    "llm.implementation.auth_method": ["oauth", "api_key"],
    "llm.implementation.tiers.fast": ["default"],  # Dynamically populated by implementation provider
    "llm.implementation.tiers.medium": ["default"],  # Dynamically populated by implementation provider
    "llm.implementation.tiers.high": ["default"],  # Dynamically populated by implementation provider
    "planning.scaffolded.stages.assumptions.model_tier": ["fast", "medium", "high"],
    "planning.scaffolded.stages.analogues.model_tier": ["fast", "medium", "high"],
    "planning.scaffolded.stages.brief.model_tier": ["fast", "medium", "high"],
    "planning.scaffolded.stages.derive.model_tier": ["fast", "medium", "high"],
    "planning.scaffolded.stages.review.model_tier": ["fast", "medium", "high"],
    "planning.scaffolded.stages.assumptions.reasoning_level": [
        "off",
        "low",
        "medium",
        "high",
        "maximum",
    ],
    "planning.scaffolded.stages.analogues.reasoning_level": [
        "off",
        "low",
        "medium",
        "high",
        "maximum",
    ],
    "planning.scaffolded.stages.brief.reasoning_level": [
        "off",
        "low",
        "medium",
        "high",
        "maximum",
    ],
    "planning.scaffolded.stages.derive.reasoning_level": [
        "off",
        "low",
        "medium",
        "high",
        "maximum",
    ],
    "planning.scaffolded.stages.review.reasoning_level": [
        "off",
        "low",
        "medium",
        "high",
        "maximum",
    ],
}


def get_choices(path: str, current_config: dict | None = None) -> list[str] | None:
    """Get valid choices for an enum-type setting.

    For model settings, returns provider-specific choices if provider is known.
    For provider settings, returns dynamic list from MODEL_REGISTRY.

    Args:
        path: Dot-notation path
        current_config: Optional current config dict to determine provider

    Returns:
        List of valid choices or None if not an enum type
    """
    # Handle provider choices dynamically
    if path.endswith(".provider"):
        return _get_provider_list()

    # Handle provider-specific model choices
    if path.endswith(".model") and current_config:
        # Determine if this is orchestrator or implementation
        if "orchestrator" in path:
            provider_path = "llm.orchestrator.provider"
        elif "implementation" in path:
            provider_path = "llm.implementation.provider"
        else:
            return CONFIG_CHOICES.get(path)

        # Get the current provider from config
        provider = _get_nested_value(current_config, provider_path)
        if isinstance(provider, str):
            model_choices = _get_provider_model_choices()
            if provider in model_choices:
                return model_choices[provider]

    # Handle tier model choices (fast/medium/high)
    if current_config and ".tiers." in path and (path.endswith(".fast") or path.endswith(".medium") or path.endswith(".high")):
        # Determine if this is orchestrator or implementation tier
        if "llm.orchestrator.tiers" in path:
            provider_path = "llm.orchestrator.provider"
        elif "llm.implementation.tiers" in path:
            provider_path = "llm.implementation.provider"
        else:
            return CONFIG_CHOICES.get(path)

        # Get the role provider from config
        provider = _get_nested_value(current_config, provider_path)
        if isinstance(provider, str):
            model_choices = _get_provider_model_choices()
            if provider in model_choices:
                return model_choices[provider]

    return CONFIG_CHOICES.get(path)


def _get_nested_value(config: dict, path: str) -> object | None:
    """Get a nested value from config dict using dot notation.

    Args:
        config: Configuration dictionary
        path: Dot-notation path like "llm.orchestrator.provider"

    Returns:
        Value at that path or None if not found
    """
    parts = path.split(".")
    current = config
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


# Mapping of paths to their default values
CONFIG_DEFAULTS: dict[str, object] = {
    "llm.orchestrator.provider": "anthropic",
    "llm.orchestrator.model": "default",
    "llm.orchestrator.auth_method": "oauth",
    "llm.git.skip_check": False,
    "llm.git.auto_init": False,
    "llm.orchestrator.tiers.fast": "haiku",
    "llm.orchestrator.tiers.medium": "sonnet",
    "llm.orchestrator.tiers.high": "opus",
    "llm.implementation.provider": "anthropic",
    "llm.implementation.model": "default",
    "llm.implementation.auth_method": "oauth",
    "llm.implementation.tiers.fast": "haiku",
    "llm.implementation.tiers.medium": "sonnet",
    "llm.implementation.tiers.high": "opus",
    "llm_timeout": 1800,
    "orchestration.timeouts.agent_execution_s": 5400,
    "orchestration.timeouts.review_agent_s": 1800,
    "orchestration.timeouts.cli_runner_s": 7200,
    "orchestration.progress.heartbeat_interval_s": 60,
    "orchestration.progress.heartbeat_initial_delay_s": 30,
    "features.performance_control.budgets.enabled": True,
    "features.performance_control.budgets.defaults.time_minutes": 30,
    "features.performance_control.budgets.defaults.iterations": 50,
    "features.quality_automation.agents.security_audit": False,
    "features.quality_automation.agents.rca_agent": True,
    "features.quality_automation.agents.doc_audit": False,
    "features.quality_automation.agents.code_review": True,
    "features.quality_automation.agents.test_generation": True,
    "features.quality_automation.agents.test_execution": True,
    "features.workflow.enabled": True,
    "advanced.debug_mode": False,
    "advanced.experimental_features": False,
    "advanced.telemetry.enabled": True,
    "planning.scaffolded.enabled": False,
    "planning.scaffolded.always_on": True,
    "planning.scaffolded.stages.assumptions.model_tier": "medium",
    "planning.scaffolded.stages.assumptions.reasoning_level": "medium",
    "planning.scaffolded.stages.assumptions.max_passes": 1,
    "planning.scaffolded.stages.assumptions.timeout_s": 20,
    "planning.scaffolded.stages.assumptions.max_questions": 3,
    "planning.scaffolded.stages.analogues.model_tier": "high",
    "planning.scaffolded.stages.analogues.reasoning_level": "high",
    "planning.scaffolded.stages.analogues.max_passes": 1,
    "planning.scaffolded.stages.analogues.timeout_s": 40,
    "planning.scaffolded.stages.brief.model_tier": "medium",
    "planning.scaffolded.stages.brief.reasoning_level": "medium",
    "planning.scaffolded.stages.brief.max_passes": 1,
    "planning.scaffolded.stages.brief.timeout_s": 20,
    "planning.scaffolded.stages.derive.model_tier": "high",
    "planning.scaffolded.stages.derive.reasoning_level": "high",
    "planning.scaffolded.stages.derive.max_passes": 1,
    "planning.scaffolded.stages.derive.timeout_s": 60,
    "planning.scaffolded.stages.review.model_tier": "high",
    "planning.scaffolded.stages.review.reasoning_level": "high",
    "planning.scaffolded.stages.review.max_passes": 1,
    "planning.scaffolded.stages.review.timeout_s": 30,
    "planning.scaffolded.non_inferable_categories": [
        "platform",
        "environment",
        "taste",
        "brand",
        "legal",
        "compliance",
    ],
    "planning.scaffolded.diff.path_template": "~/.obra/intents/{intent_id}.diff.md",
    "planning.scaffolded.diff.retention.max_age_days": 30,
    "planning.scaffolded.diff.retention.max_files": 200,
    "planning.scaffolded.artifacts.dir": "~/.obra/intents/artifacts",
    "planning.scaffolded.artifacts.retention.max_age_days": 30,
    "planning.scaffolded.artifacts.retention.max_files": 200,
    "planning.scaffolded.analogue_cache.global_path": "~/.obra/analogue_cache.yaml",
    "planning.scaffolded.analogue_cache.project_path": ".obra/analogue_cache.yaml",
    "planning.scaffolded.telemetry.enabled": False,
    "planning.scaffolded.telemetry.include_content": False,
    "planning.scaffolded.telemetry.output_path": "~/.obra/telemetry/scaffolded.jsonl",
}


def get_default(path: str) -> object:
    """Get default value for a setting.

    Args:
        path: Dot-notation path

    Returns:
        Default value or None if not defined
    """
    return CONFIG_DEFAULTS.get(path)


# Setting tier mapping (basic, standard, advanced)
SETTING_TIERS: dict[str, str] = {
    # Basic - most users need these
    "llm.orchestrator.provider": "basic",
    "llm.orchestrator.model": "basic",
    "llm.implementation.provider": "basic",
    "llm.implementation.model": "basic",
    "preset": "basic",
    # Standard - common use
    "llm.orchestrator.auth_method": "standard",
    "llm.implementation.auth_method": "standard",
    "llm.orchestrator.tiers": "standard",
    "llm.orchestrator.tiers.fast": "standard",
    "llm.orchestrator.tiers.medium": "standard",
    "llm.orchestrator.tiers.high": "standard",
    "llm.implementation.tiers": "standard",
    "llm.implementation.tiers.fast": "standard",
    "llm.implementation.tiers.medium": "standard",
    "llm.implementation.tiers.high": "standard",
    "features.performance_control.budgets.enabled": "standard",
    "features.quality_automation.agents.security_audit": "standard",
    "features.quality_automation.agents.rca_agent": "standard",
    "features.quality_automation.agents.doc_audit": "standard",
    "features.quality_automation.agents.code_review": "standard",
    "features.quality_automation.agents.test_generation": "standard",
    "features.quality_automation.agents.test_execution": "standard",
    "features.workflow.enabled": "standard",
    # Git settings - visible for provider-aware auto-configuration
    "llm.git": "basic",
    "llm.git.skip_check": "basic",
    "llm.git.auto_init": "standard",
    # Advanced - expert users
    "api_base_url": "advanced",
    "llm_timeout": "advanced",
    "orchestration.timeouts.agent_execution_s": "advanced",
    "orchestration.timeouts.review_agent_s": "advanced",
    "orchestration.timeouts.cli_runner_s": "advanced",
    "orchestration.progress.heartbeat_interval_s": "advanced",
    "orchestration.progress.heartbeat_initial_delay_s": "advanced",
    "advanced.debug_mode": "advanced",
    "advanced.experimental_features": "advanced",
    "advanced.telemetry.enabled": "advanced",
    "features.performance_control.budgets.defaults.time_minutes": "advanced",
    "features.performance_control.budgets.defaults.iterations": "advanced",
    "planning": "advanced",
    "planning.scaffolded": "advanced",
    "planning.scaffolded.enabled": "advanced",
    "planning.scaffolded.always_on": "advanced",
    "planning.scaffolded.stages": "advanced",
    "planning.scaffolded.stages.assumptions": "advanced",
    "planning.scaffolded.stages.assumptions.model_tier": "advanced",
    "planning.scaffolded.stages.assumptions.reasoning_level": "advanced",
    "planning.scaffolded.stages.assumptions.max_passes": "advanced",
    "planning.scaffolded.stages.assumptions.timeout_s": "advanced",
    "planning.scaffolded.stages.assumptions.max_questions": "advanced",
    "planning.scaffolded.stages.analogues": "advanced",
    "planning.scaffolded.stages.analogues.model_tier": "advanced",
    "planning.scaffolded.stages.analogues.reasoning_level": "advanced",
    "planning.scaffolded.stages.analogues.max_passes": "advanced",
    "planning.scaffolded.stages.analogues.timeout_s": "advanced",
    "planning.scaffolded.stages.brief": "advanced",
    "planning.scaffolded.stages.brief.model_tier": "advanced",
    "planning.scaffolded.stages.brief.reasoning_level": "advanced",
    "planning.scaffolded.stages.brief.max_passes": "advanced",
    "planning.scaffolded.stages.brief.timeout_s": "advanced",
    "planning.scaffolded.stages.derive": "advanced",
    "planning.scaffolded.stages.derive.model_tier": "advanced",
    "planning.scaffolded.stages.derive.reasoning_level": "advanced",
    "planning.scaffolded.stages.derive.max_passes": "advanced",
    "planning.scaffolded.stages.derive.timeout_s": "advanced",
    "planning.scaffolded.stages.review": "advanced",
    "planning.scaffolded.stages.review.model_tier": "advanced",
    "planning.scaffolded.stages.review.reasoning_level": "advanced",
    "planning.scaffolded.stages.review.max_passes": "advanced",
    "planning.scaffolded.stages.review.timeout_s": "advanced",
    "planning.scaffolded.non_inferable_categories": "advanced",
    "planning.scaffolded.diff": "advanced",
    "planning.scaffolded.diff.path_template": "advanced",
    "planning.scaffolded.diff.retention": "advanced",
    "planning.scaffolded.diff.retention.max_age_days": "advanced",
    "planning.scaffolded.diff.retention.max_files": "advanced",
    "planning.scaffolded.artifacts": "advanced",
    "planning.scaffolded.artifacts.dir": "advanced",
    "planning.scaffolded.artifacts.retention": "advanced",
    "planning.scaffolded.artifacts.retention.max_age_days": "advanced",
    "planning.scaffolded.artifacts.retention.max_files": "advanced",
    "planning.scaffolded.analogue_cache": "advanced",
    "planning.scaffolded.analogue_cache.global_path": "advanced",
    "planning.scaffolded.analogue_cache.project_path": "advanced",
    "planning.scaffolded.telemetry": "advanced",
    "planning.scaffolded.telemetry.enabled": "advanced",
    "planning.scaffolded.telemetry.include_content": "advanced",
    "planning.scaffolded.telemetry.output_path": "advanced",
}


def get_tier(path: str) -> str:
    """Get visibility tier for a setting.

    Args:
        path: Dot-notation path

    Returns:
        "basic", "standard", or "advanced" (defaults to "standard")
    """
    if path.startswith("advanced."):
        return "advanced"
    return SETTING_TIERS.get(path, "standard")
