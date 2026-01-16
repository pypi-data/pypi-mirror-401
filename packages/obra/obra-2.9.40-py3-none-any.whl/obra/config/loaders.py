"""Configuration file I/O and path management for Obra.

Handles loading and saving client configuration from
~/.obra/config-layers/01-user.yaml, plus environment variable resolution for
API URLs and timeouts.

Example:
    from obra.config.loaders import load_config, save_config, get_api_base_url

    config = load_config()
    api_url = get_api_base_url()
"""

import logging
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

from obra.exceptions import ConfigurationError

# Module logger
logger = logging.getLogger(__name__)

# Config layer paths
CONFIG_LAYER_DIR = Path.home() / ".obra" / "config-layers"
CONFIG_PATH = CONFIG_LAYER_DIR / "01-user.yaml"
LEGACY_CONFIG_PATH = Path.home() / ".obra" / "client-config.yaml"
PROJECT_LAYER_PREFIX = "02-project-"
SESSION_LAYER_PREFIX = "03-session-"
SESSION_CONFIG_ENV_VAR = "OBRA_SESSION_CONFIG"

# Default API URL (production)
# Can be overridden via OBRA_API_BASE_URL environment variable
DEFAULT_API_BASE_URL = "https://us-central1-obra-205b0.cloudfunctions.net"

# Default LLM execution timeout (30 minutes)
# Can be overridden via OBRA_LLM_TIMEOUT environment variable
DEFAULT_LLM_TIMEOUT = 1800

# Default agent execution timeout (90 minutes) - FIX-TIMEOUT-CONSOLIDATION-001
# Can be overridden via OBRA_AGENT_EXECUTION_TIMEOUT environment variable
DEFAULT_AGENT_EXECUTION_TIMEOUT = 5400

# Default review agent timeout (30 minutes) - FIX-TIMEOUT-CONSOLIDATION-001
# Can be overridden via OBRA_REVIEW_AGENT_TIMEOUT environment variable
DEFAULT_REVIEW_AGENT_TIMEOUT = 1800

# Default maximum iterations for orchestration loop
# Can be overridden via 01-user.yaml max_iterations setting
DEFAULT_MAX_ITERATIONS = 100

# Network timeout configuration (C17)
# Default timeout for general network operations (seconds)
DEFAULT_NETWORK_TIMEOUT = 30
# Timeout for LLM API operations (seconds)
DEFAULT_LLM_API_TIMEOUT = 120

# Version check configuration (FEAT-CLI-VERSION-NOTIFY-001)
# Enable/disable automatic version checking
DEFAULT_CHECK_FOR_UPDATES = True
# Cooldown period between version notifications (minutes)
DEFAULT_UPDATE_NOTIFICATION_COOLDOWN_MINUTES = 10

# Prompt file retention
DEFAULT_PROMPT_RETAIN = False
DEFAULT_PROMPT_MAX_FILES = 200

# Deprecated config keys mapped to new paths (schema reorg)
CONFIG_PATH_ALIASES: dict[str, str] = {
    "monitoring": "advanced.monitoring",
    "logging": "advanced.logging",
    "debug": "advanced.debug",
    "audit": "advanced.audit",
    "metrics": "advanced.metrics",
    "observability": "advanced.observability",
}


def get_config_path() -> Path:
    """Get path to user configuration file.

    Returns:
        Path to ~/.obra/config-layers/01-user.yaml
    """
    return CONFIG_PATH


def get_project_layer_path(project_id: str) -> Path:
    """Return the project layer path for a project identifier."""
    return CONFIG_LAYER_DIR / f"{PROJECT_LAYER_PREFIX}{project_id}.yaml"


def get_session_layer_path(session_id: str) -> Path:
    """Return the session layer path for a session identifier."""
    return CONFIG_LAYER_DIR / f"{SESSION_LAYER_PREFIX}{session_id}.yaml"


def get_session_layer_override() -> Path | None:
    """Return the session layer override path from environment, if set."""
    value = os.environ.get(SESSION_CONFIG_ENV_VAR)
    if not value:
        return None
    return Path(value).expanduser()


def _ensure_user_config_exists() -> None:
    if CONFIG_PATH.exists():
        return
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text("{}\n", encoding="utf-8")


def resolve_config_alias(path: str) -> str:
    """Resolve deprecated config paths to their canonical replacements."""
    return CONFIG_PATH_ALIASES.get(path, path)


def _get_nested_value(config: dict[str, Any], path: str) -> Any:
    """Return nested value by dotted path."""
    current: Any = config
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _has_nested_key(config: dict[str, Any], path: str) -> bool:
    """Check whether a dotted path exists in the config."""
    current: Any = config
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False
    return True


def _set_nested_value(config: dict[str, Any], path: str, value: Any) -> None:
    """Set a nested value by dotted path, creating containers as needed."""
    parts = path.split(".")
    current: dict[str, Any] = config
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value


def _apply_config_aliases(
    config: dict[str, Any],
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """Apply deprecated path aliases without mutating the source dict."""
    normalized = deepcopy(config)
    for legacy, canonical in CONFIG_PATH_ALIASES.items():
        legacy_exists = _has_nested_key(normalized, legacy)
        canonical_exists = _has_nested_key(normalized, canonical)
        legacy_value = _get_nested_value(normalized, legacy) if legacy_exists else None
        canonical_value = _get_nested_value(normalized, canonical) if canonical_exists else None

        if legacy_exists and not canonical_exists:
            _set_nested_value(normalized, canonical, legacy_value)
            if warnings is not None:
                warnings.append(
                    f"Deprecated config key '{legacy}' detected; use '{canonical}'."
                )
        elif canonical_exists and not legacy_exists:
            _set_nested_value(normalized, legacy, canonical_value)
        elif legacy_exists and canonical_exists and legacy_value != canonical_value:
            _set_nested_value(normalized, legacy, canonical_value)
            if warnings is not None:
                warnings.append(
                    f"Config keys '{legacy}' and '{canonical}' both set; "
                    f"'{canonical}' takes precedence."
                )

    return normalized


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load configuration from ~/.obra/config-layers/01-user.yaml.

    Returns:
        Configuration dictionary, empty dict if file doesn't exist
    """
    path = config_path or CONFIG_PATH
    if path == CONFIG_PATH:
        _ensure_user_config_exists()
    if not path.exists():
        return {}

    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return {}

    if not isinstance(data, dict):
        logger.warning(
            "Invalid user config at %s: expected mapping, got %s",
            path,
            type(data).__name__,
        )
        return {}

    return _apply_config_aliases(data)


def load_config_with_warnings(
    config_path: Path | None = None,
) -> tuple[dict[str, Any], list[str], bool]:
    """Load user configuration and return warnings instead of raising.

    Args:
        config_path: Optional override path for the config file.

    Returns:
        Tuple of (config dict, warnings list, file_exists).
    """
    path = config_path or CONFIG_PATH
    warnings: list[str] = []

    if path == CONFIG_PATH:
        _ensure_user_config_exists()

    if not path.exists():
        return {}, warnings, False

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        warnings.append(f"Failed to read config at {path}: {exc}. Using defaults.")
        return {}, warnings, True

    try:
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as exc:
        warnings.append(f"Invalid YAML in config at {path}: {exc}. Using defaults.")
        return {}, warnings, True

    if not isinstance(data, dict):
        warnings.append(
            f"Invalid config at {path}: expected mapping, got {type(data).__name__}. "
            "Using defaults."
        )
        return {}, warnings, True

    return _apply_config_aliases(data, warnings), warnings, True


def _load_layer_file(
    path: Path,
    warnings: list[str],
    label: str,
) -> dict[str, Any]:
    if not path.exists():
        return {}

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        warnings.append(f"Failed to read {label} at {path}: {exc}. Ignoring.")
        return {}

    try:
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as exc:
        warnings.append(f"Invalid YAML in {label} at {path}: {exc}. Ignoring.")
        return {}

    if not isinstance(data, dict):
        warnings.append(
            f"Invalid {label} at {path}: expected mapping, got {type(data).__name__}. "
            "Ignoring."
        )
        return {}

    return _apply_config_aliases(data, warnings)


def _record_origins(
    data: dict[str, Any],
    layer: str,
    origins: dict[str, str],
    prefix: str = "",
) -> None:
    for key, value in data.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            _record_origins(value, layer, origins, path)
        else:
            origins[path] = layer


def _merge_with_origins(
    base: dict[str, Any],
    override: dict[str, Any],
    layer: str,
    origins: dict[str, str],
    prefix: str = "",
) -> None:
    for key, value in override.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            base_value = base.get(key)
            if not isinstance(base_value, dict):
                base_value = {}
            base[key] = base_value
            _merge_with_origins(base_value, value, layer, origins, path)
        else:
            base[key] = value
            origins[path] = layer


def _load_default_schema() -> dict[str, Any]:
    try:
        from importlib import resources

        default_path = resources.files("obra.config").joinpath("default_config.yaml")
        content = default_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
        if isinstance(data, dict):
            return data
    except Exception as exc:
        logger.debug("Failed to load default_config.yaml: %s", exc)
    return {}


def load_layered_config(
    project_id: str | None = None,
    session_path: Path | None = None,
    include_defaults: bool = False,
) -> tuple[dict[str, Any], dict[str, str], list[str]]:
    """Load layered config with deterministic precedence."""
    warnings: list[str] = []

    user_config, user_warnings, _ = load_config_with_warnings()
    warnings.extend(user_warnings)

    resolved_project_id = project_id
    if resolved_project_id is None:
        try:
            from obra.intent.storage import IntentStorage

            resolved_project_id = IntentStorage().get_project_id(Path.cwd())
        except Exception as exc:
            warnings.append(
                f"Unable to resolve project ID for config layers: {exc}. "
                "Skipping project layer."
            )
            resolved_project_id = None

    project_config: dict[str, Any] = {}
    if resolved_project_id:
        project_path = get_project_layer_path(resolved_project_id)
        project_config = _load_layer_file(project_path, warnings, "project config")

    session_config: dict[str, Any] = {}
    resolved_session_path = session_path or get_session_layer_override()
    if resolved_session_path:
        if not resolved_session_path.exists():
            warnings.append(
                f"Session config not found at {resolved_session_path}. Ignoring."
            )
        else:
            session_config = _load_layer_file(
                resolved_session_path, warnings, "session config"
            )

    layers_empty = not user_config and not project_config and not session_config
    if LEGACY_CONFIG_PATH.exists() and layers_empty:
        warnings.append(
            f"Legacy config detected at {LEGACY_CONFIG_PATH}. "
            "Run 'obra setup' to regenerate config layers."
        )

    origins: dict[str, str] = {}
    merged: dict[str, Any] = {}
    if include_defaults:
        defaults = _load_default_schema()
        merged = deepcopy(defaults)
        _record_origins(defaults, "default", origins)

    _merge_with_origins(merged, user_config, "user", origins)
    if project_config:
        _merge_with_origins(merged, project_config, "project", origins)
    if session_config:
        _merge_with_origins(merged, session_config, "session", origins)

    return merged, origins, warnings


def load_project_layer(project_id: str) -> tuple[dict[str, Any], list[str], bool]:
    """Load a project-specific config layer."""
    warnings: list[str] = []
    path = get_project_layer_path(project_id)
    if not path.exists():
        return {}, warnings, False
    return _load_layer_file(path, warnings, "project config"), warnings, True


def save_config(config: dict[str, Any]) -> None:
    """Save configuration to ~/.obra/config-layers/01-user.yaml.

    Args:
        config: Configuration dictionary to save

    Raises:
        OSError: If unable to write config file
    """
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)


def get_api_base_url() -> str:
    """Get API base URL with environment variable override support.

    Resolution order:
    1. OBRA_API_BASE_URL environment variable
    2. api_base_url from config file
    3. DEFAULT_API_BASE_URL constant

    Returns:
        API base URL string

    Example:
        # Override for local development
        export OBRA_API_BASE_URL="http://localhost:5001/obra-205b0/us-central1"

        # Override for staging
        export OBRA_API_BASE_URL="https://us-central1-obra-staging.cloudfunctions.net"
    """
    # Priority 1: Environment variable
    env_url = os.environ.get("OBRA_API_BASE_URL")
    if env_url:
        return env_url.rstrip("/")

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    config_url = config.get("api_base_url")
    if isinstance(config_url, str):
        return config_url.rstrip("/")

    # Priority 3: Default constant
    return DEFAULT_API_BASE_URL


def get_llm_timeout() -> int:
    """Get LLM execution timeout in seconds.

    Resolution order:
    1. OBRA_LLM_TIMEOUT environment variable
    2. llm_timeout from config file
    3. DEFAULT_LLM_TIMEOUT constant (1800s = 30 min)

    Returns:
        Timeout in seconds

    Example:
        # Override for long-running tasks
        export OBRA_LLM_TIMEOUT=3600

        # Or set in ~/.obra/config-layers/01-user.yaml:
        # llm_timeout: 3600
    """
    # Priority 1: Environment variable
    env_timeout = os.environ.get("OBRA_LLM_TIMEOUT")
    if env_timeout:
        try:
            return int(env_timeout)
        except ValueError:
            pass  # Fall through to config file

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    config_timeout = config.get("llm_timeout")
    if config_timeout:
        return int(config_timeout)

    # Priority 3: Default constant
    return DEFAULT_LLM_TIMEOUT


def get_agent_execution_timeout() -> int:
    """Get agent execution timeout in seconds.

    Resolution order:
    1. OBRA_AGENT_EXECUTION_TIMEOUT environment variable
    2. orchestration.timeouts.agent_execution_s from config file
    3. DEFAULT_AGENT_EXECUTION_TIMEOUT constant (5400s = 90 min)

    Returns:
        Timeout in seconds

    Example:
        # Override for shorter timeout
        export OBRA_AGENT_EXECUTION_TIMEOUT=300

        # Or set in ~/.obra/config-layers/01-user.yaml:
        # orchestration:
        #   timeouts:
        #     agent_execution_s: 300
    """
    # Priority 1: Environment variable
    env_timeout = os.environ.get("OBRA_AGENT_EXECUTION_TIMEOUT")
    if env_timeout:
        try:
            return int(env_timeout)
        except ValueError:
            pass  # Fall through to config file

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    orch_config = config.get("orchestration", {})
    if isinstance(orch_config, dict):
        timeouts_config = orch_config.get("timeouts", {})
        if isinstance(timeouts_config, dict):
            timeout = timeouts_config.get("agent_execution_s")
            if timeout is not None:
                return int(timeout)

    # Priority 3: Default constant
    return DEFAULT_AGENT_EXECUTION_TIMEOUT


def get_prompt_retention() -> bool:
    """Get prompt file retention setting.

    Resolution order:
    1. orchestration.prompts.retain from config file
    2. DEFAULT_PROMPT_RETAIN constant (False)

    Returns:
        True if prompt files should be retained, else False
    """
    config, _, _ = load_layered_config()
    orch_config = config.get("orchestration", {})
    if isinstance(orch_config, dict):
        prompts_config = orch_config.get("prompts", {})
        if isinstance(prompts_config, dict):
            retain = prompts_config.get("retain")
            if retain is not None:
                return bool(retain)
    return DEFAULT_PROMPT_RETAIN


def get_prompt_max_files() -> int:
    """Get max prompt files to retain before cleanup.

    Resolution order:
    1. orchestration.prompts.max_files from config file
    2. DEFAULT_PROMPT_MAX_FILES constant (200)

    Returns:
        Max prompt files to retain before cleanup
    """
    config, _, _ = load_layered_config()
    orch_config = config.get("orchestration", {})
    if isinstance(orch_config, dict):
        prompts_config = orch_config.get("prompts", {})
        if isinstance(prompts_config, dict):
            max_files = prompts_config.get("max_files")
            if max_files is not None:
                try:
                    return int(max_files)
                except (TypeError, ValueError):
                    pass
    return DEFAULT_PROMPT_MAX_FILES


def get_review_agent_timeout() -> int:
    """Get review agent timeout in seconds.

    Resolution order:
    1. OBRA_REVIEW_AGENT_TIMEOUT environment variable
    2. orchestration.timeouts.review_agent_s from config file
    3. DEFAULT_REVIEW_AGENT_TIMEOUT constant (1800s = 30 min)

    Returns:
        Timeout in seconds

    Example:
        # Override for longer review timeout
        export OBRA_REVIEW_AGENT_TIMEOUT=120

        # Or set in ~/.obra/config-layers/01-user.yaml:
        # orchestration:
        #   timeouts:
        #     review_agent_s: 120
    """
    # Priority 1: Environment variable
    env_timeout = os.environ.get("OBRA_REVIEW_AGENT_TIMEOUT")
    if env_timeout:
        try:
            return int(env_timeout)
        except ValueError:
            pass  # Fall through to config file

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    orch_config = config.get("orchestration", {})
    if isinstance(orch_config, dict):
        timeouts_config = orch_config.get("timeouts", {})
        if isinstance(timeouts_config, dict):
            timeout = timeouts_config.get("review_agent_s")
            if timeout is not None:
                return int(timeout)

    # Priority 3: Default constant
    return DEFAULT_REVIEW_AGENT_TIMEOUT


def get_heartbeat_interval() -> int:
    """Get heartbeat interval in seconds.

    Resolution order:
    1. OBRA_HEARTBEAT_INTERVAL environment variable
    2. orchestration.progress.heartbeat_interval_s from config file
    3. Default 60 seconds

    Returns:
        Heartbeat interval in seconds

    Example:
        # Override for more frequent heartbeats
        export OBRA_HEARTBEAT_INTERVAL=30

        # Or set in ~/.obra/config-layers/01-user.yaml:
        # orchestration:
        #   progress:
        #     heartbeat_interval_s: 30
    """
    # Priority 1: Environment variable
    env_interval = os.environ.get("OBRA_HEARTBEAT_INTERVAL")
    if env_interval:
        try:
            return int(env_interval)
        except ValueError:
            pass  # Fall through to config file

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    orch_config = config.get("orchestration", {})
    if isinstance(orch_config, dict):
        progress_config = orch_config.get("progress", {})
        if isinstance(progress_config, dict):
            interval = progress_config.get("heartbeat_interval_s")
            if interval is not None:
                return int(interval)

    # Priority 3: Default constant
    return 60


def get_heartbeat_initial_delay() -> int:
    """Get heartbeat initial delay in seconds.

    Resolution order:
    1. OBRA_HEARTBEAT_INITIAL_DELAY environment variable
    2. orchestration.progress.heartbeat_initial_delay_s from config file
    3. Default 30 seconds

    Returns:
        Heartbeat initial delay in seconds

    Example:
        # Override for shorter initial delay
        export OBRA_HEARTBEAT_INITIAL_DELAY=10

        # Or set in ~/.obra/config-layers/01-user.yaml:
        # orchestration:
        #   progress:
        #     heartbeat_initial_delay_s: 10
    """
    # Priority 1: Environment variable
    env_delay = os.environ.get("OBRA_HEARTBEAT_INITIAL_DELAY")
    if env_delay:
        try:
            return int(env_delay)
        except ValueError:
            pass  # Fall through to config file

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    orch_config = config.get("orchestration", {})
    if isinstance(orch_config, dict):
        progress_config = orch_config.get("progress", {})
        if isinstance(progress_config, dict):
            delay = progress_config.get("heartbeat_initial_delay_s")
            if delay is not None:
                return int(delay)

    # Priority 3: Default constant
    return 30


def get_max_iterations() -> int:
    """Get maximum orchestration loop iterations.

    Resolution order:
    1. OBRA_MAX_ITERATIONS environment variable
    2. max_iterations from config file
    3. DEFAULT_MAX_ITERATIONS constant (100)

    Returns:
        Maximum iterations

    Example:
        # Override for complex tasks
        export OBRA_MAX_ITERATIONS=150

        # Or set in ~/.obra/config-layers/01-user.yaml:
        # max_iterations: 150
    """
    # Priority 1: Environment variable
    env_max_iterations = os.environ.get("OBRA_MAX_ITERATIONS")
    if env_max_iterations:
        try:
            return int(env_max_iterations)
        except ValueError:
            pass  # Fall through to config file

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    config_max_iterations = config.get("max_iterations")
    if config_max_iterations:
        return int(config_max_iterations)

    # Priority 3: Default constant
    return DEFAULT_MAX_ITERATIONS


def get_default_project_override() -> str | None:
    """Get local default project override from layered config."""
    config, _, _ = load_layered_config()
    projects = config.get("projects", {})
    if isinstance(projects, dict):
        value = projects.get("default_project")
        return str(value) if value is not None else None
    return None


def get_isolated_mode() -> bool | None:
    """Get agent isolation mode from config.

    Returns:
        True: Enable isolation
        False: Disable isolation
        None: Use default (auto-detect from CLI/ENV/CI)

    Config location: ~/.obra/config-layers/01-user.yaml

    Example:
        # In 01-user.yaml:
        agent:
          isolated_mode: true
    """
    config, _, _ = load_layered_config()
    agent_config = config.get("agent", {})
    if isinstance(agent_config, dict):
        return agent_config.get("isolated_mode")
    return None


def set_isolated_mode(enabled: bool | None) -> None:
    """Set agent isolation mode in config.

    Args:
        enabled: True to enable, False to disable, None to clear

    Config location: ~/.obra/config-layers/01-user.yaml
    """
    config, _, _ = load_layered_config()

    if enabled is None:
        # Clear the setting
        if "agent" in config and isinstance(config["agent"], dict):
            config["agent"].pop("isolated_mode", None)
            if not config["agent"]:
                del config["agent"]
    else:
        if "agent" not in config:
            config["agent"] = {}
        config["agent"]["isolated_mode"] = enabled

    save_config(config)


def get_check_for_updates() -> bool:
    """Get version check enable/disable setting.

    Resolution order:
    1. OBRA_CHECK_FOR_UPDATES environment variable
    2. cli.check_for_updates from config file
    3. DEFAULT_CHECK_FOR_UPDATES constant (True)

    Returns:
        True to enable version checks, False to disable

    Example:
        # Disable via environment variable
        export OBRA_CHECK_FOR_UPDATES=false

        # Or set in ~/.obra/config-layers/01-user.yaml:
        # cli:
        #   check_for_updates: false
    """
    # Priority 1: Environment variable
    env_check = os.environ.get("OBRA_CHECK_FOR_UPDATES")
    if env_check:
        return env_check.lower() in ("true", "1", "yes", "on")

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    cli_config = config.get("cli", {})
    if isinstance(cli_config, dict):
        check = cli_config.get("check_for_updates")
        if check is not None:
            return bool(check)

    # Priority 3: Default constant
    return DEFAULT_CHECK_FOR_UPDATES


def get_update_notification_cooldown_minutes() -> int:
    """Get cooldown period between version update notifications.

    Resolution order:
    1. OBRA_UPDATE_NOTIFICATION_COOLDOWN_MINUTES environment variable
    2. cli.update_notification_cooldown_minutes from config file
    3. DEFAULT_UPDATE_NOTIFICATION_COOLDOWN_MINUTES constant (10)

    Returns:
        Cooldown period in minutes

    Example:
        # Override for shorter cooldown
        export OBRA_UPDATE_NOTIFICATION_COOLDOWN_MINUTES=5

        # Or set in ~/.obra/config-layers/01-user.yaml:
        # cli:
        #   update_notification_cooldown_minutes: 5
    """
    # Priority 1: Environment variable
    env_cooldown = os.environ.get("OBRA_UPDATE_NOTIFICATION_COOLDOWN_MINUTES")
    if env_cooldown:
        try:
            return int(env_cooldown)
        except ValueError:
            pass  # Fall through to config file

    # Priority 2: Config file
    config, _, _ = load_layered_config()
    cli_config = config.get("cli", {})
    if isinstance(cli_config, dict):
        cooldown = cli_config.get("update_notification_cooldown_minutes")
        if cooldown is not None:
            return int(cooldown)

    # Priority 3: Default constant
    return DEFAULT_UPDATE_NOTIFICATION_COOLDOWN_MINUTES


def get_project_detection_empty_threshold() -> int:
    """Get project detection empty threshold.

    Resolution order:
    1. intent.project_detection.empty_threshold from config file
    2. Default 5

    Returns:
        Empty threshold (number of files)

    Example:
        # In ~/.obra/config-layers/01-user.yaml:
        # intent:
        #   project_detection:
        #     empty_threshold: 10
    """
    config, _, _ = load_layered_config()
    intent_config = config.get("intent", {})
    if isinstance(intent_config, dict):
        detection_config = intent_config.get("project_detection", {})
        if isinstance(detection_config, dict):
            threshold = detection_config.get("empty_threshold")
            if threshold is not None:
                return int(threshold)

    # Default
    return 5


def get_project_detection_existing_threshold() -> int:
    """Get project detection existing threshold.

    Resolution order:
    1. intent.project_detection.existing_threshold from config file
    2. Default 50

    Returns:
        Existing threshold (number of files)

    Example:
        # In ~/.obra/config-layers/01-user.yaml:
        # intent:
        #   project_detection:
        #     existing_threshold: 100
    """
    config, _, _ = load_layered_config()
    intent_config = config.get("intent", {})
    if isinstance(intent_config, dict):
        detection_config = intent_config.get("project_detection", {})
        if isinstance(detection_config, dict):
            threshold = detection_config.get("existing_threshold")
            if threshold is not None:
                return int(threshold)

    # Default
    return 50


def get_project_detection_enabled() -> bool:
    """Get project detection enabled flag.

    Resolution order:
    1. intent.project_detection.enabled from config file
    2. Default True

    Returns:
        True if detection is enabled

    Example:
        # In ~/.obra/config-layers/01-user.yaml:
        # intent:
        #   project_detection:
        #     enabled: false
    """
    config, _, _ = load_layered_config()
    intent_config = config.get("intent", {})
    if isinstance(intent_config, dict):
        detection_config = intent_config.get("project_detection", {})
        if isinstance(detection_config, dict):
            enabled = detection_config.get("enabled")
            if enabled is not None:
                return bool(enabled)

    # Default
    return True


def load_llm_section(config: dict[str, Any]) -> dict[str, Any]:
    """Extract and validate llm section from client config."""
    llm_config = config.get("llm")
    if llm_config is None:
        return {}
    if not isinstance(llm_config, dict):
        msg = "Invalid llm section in ~/.obra/config-layers/01-user.yaml."
        raise ConfigurationError(
            msg,
            "Set llm to a mapping. Example:\nllm:\n  provider: anthropic\n  model: sonnet",
        )
    return llm_config


# Public exports
__all__ = [
    # Constants
    "CONFIG_PATH",
    "CONFIG_LAYER_DIR",
    "LEGACY_CONFIG_PATH",
    "DEFAULT_AGENT_EXECUTION_TIMEOUT",
    "DEFAULT_API_BASE_URL",
    "DEFAULT_CHECK_FOR_UPDATES",
    "DEFAULT_LLM_API_TIMEOUT",
    "DEFAULT_LLM_TIMEOUT",
    "DEFAULT_MAX_ITERATIONS",
    "DEFAULT_NETWORK_TIMEOUT",
    "DEFAULT_REVIEW_AGENT_TIMEOUT",
    "DEFAULT_UPDATE_NOTIFICATION_COOLDOWN_MINUTES",
    "get_agent_execution_timeout",
    # Getters with env override
    "get_api_base_url",
    # Version check config
    "get_check_for_updates",
    # Config I/O functions
    "get_config_path",
    "get_project_layer_path",
    "get_session_layer_path",
    "get_session_layer_override",
    # Project config
    "get_default_project_override",
    # Agent isolation config
    "get_isolated_mode",
    "get_llm_timeout",
    "get_max_iterations",
    "get_review_agent_timeout",
    "get_update_notification_cooldown_minutes",
    "load_config",
    "load_llm_section",
    "load_layered_config",
    "load_project_layer",
    "save_config",
    "set_isolated_mode",
]
