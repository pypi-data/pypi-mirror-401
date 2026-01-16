"""Review configuration helpers for review agent selection and behavior."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from obra.api.protocol import DEFAULT_REVIEW_AGENTS
from obra.exceptions import ConfigurationError

# Allowed agent identifiers come from the shared protocol enum.
ALLOWED_AGENTS: tuple[str, ...] = tuple(DEFAULT_REVIEW_AGENTS)
ALLOWED_OUTPUT_FORMATS: tuple[str, ...] = ("text", "json")
ALLOWED_FAIL_THRESHOLDS: tuple[str, ...] = ("p1", "p2")
REVIEW_CONFIG_RELATIVE_PATH = Path(".obra") / "config.yaml"
_FEATURE_AGENT_MAP: dict[str, list[str]] = {
    "security_audit": ["security"],
    "code_review": ["code_quality"],
    "doc_audit": ["docs"],
    "test_generation": ["testing", "test_execution"],
}


def _load_quality_feature_section() -> Mapping[str, Any]:
    """Load quality_automation feature settings from client config."""
    try:
        from obra.config import load_config
    except Exception:
        return {}

    config = load_config()
    features = config.get("features", {})
    if not isinstance(features, Mapping):
        return {}
    quality = features.get("quality_automation", {})
    if not isinstance(quality, Mapping):
        return {}
    return quality


def _get_quality_agent_flag(
    quality_section: Mapping[str, Any],
    agent_key: str,
) -> bool | None:
    agents = quality_section.get("agents", {})
    if isinstance(agents, Mapping) and agent_key in agents:
        return bool(agents.get(agent_key))
    if agent_key in quality_section:
        return bool(quality_section.get(agent_key))
    return None


def resolve_feature_review_gates() -> tuple[bool, list[str]]:
    """Resolve review gating based on quality_automation feature flags."""
    quality_section = _load_quality_feature_section()
    if not quality_section:
        return False, []

    enabled = quality_section.get("enabled")
    if enabled is False:
        return True, []

    disabled_agents: list[str] = []
    for agent_key, review_agents in _FEATURE_AGENT_MAP.items():
        flag = _get_quality_agent_flag(quality_section, agent_key)
        if flag is False:
            disabled_agents.extend(review_agents)

    return False, _filter_allowed(disabled_agents)


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    """Return a list with duplicates removed while preserving order."""
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value not in seen:
            deduped.append(value)
            seen.add(value)
    return deduped


def _validate_agents(values: Sequence[str] | None, field_name: str) -> list[str] | None:
    """Validate agent identifiers against the allowed set."""
    if values is None:
        return None

    normalized = []
    for value in values:
        agent = str(value).strip()
        if agent not in ALLOWED_AGENTS:
            allowed = ", ".join(ALLOWED_AGENTS)
            raise ValueError(f"Invalid agent '{value}' in {field_name}. Allowed: {allowed}.")
        normalized.append(agent)

    return _dedupe_preserve_order(normalized)


def _filter_allowed(values: Sequence[str] | None) -> list[str]:
    """Filter a sequence down to allowed agents, removing duplicates."""
    if not values:
        return []
    return [agent for agent in _dedupe_preserve_order(values) if agent in ALLOWED_AGENTS]


def load_review_config(project_path: Path) -> dict[str, Any]:
    """Load and validate review configuration from .obra/config.yaml.

    Args:
        project_path: Project root used to resolve .obra/config.yaml

    Returns:
        Normalized dictionary of review settings keyed by ReviewConfig fields.
        Missing files or sections return an empty dict so callers can fall back
        to detection/server defaults.

    Raises:
        ConfigurationError: If the config file exists but contains invalid YAML
            or unsupported review values.
    """
    config_path = Path(project_path) / REVIEW_CONFIG_RELATIVE_PATH
    if not config_path.exists():
        return {}

    try:
        with config_path.open(encoding="utf-8") as config_file:
            raw_config = yaml.safe_load(config_file) or {}
    except FileNotFoundError:
        return {}
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            f"Invalid YAML in {config_path}: {exc}",
            "Fix the YAML syntax in .obra/config.yaml and try again.",
        )
    except OSError as exc:
        raise ConfigurationError(
            f"Unable to read {config_path}: {exc}",
            "Check file permissions for .obra/config.yaml and retry.",
        )

    review_section = raw_config.get("review")
    if review_section is None:
        return {}
    if not isinstance(review_section, Mapping):
        raise ConfigurationError(
            f"The review section in {config_path} must be a mapping of keys to values.",
            "Update the review section to a mapping with fields like default_agents and output_format.",
        )

    allowed_keys = {
        "default_agents",
        "always_full_review",
        "skip_review",
        "output_format",
        "summary_only",
        "fail_on_p1",
        "fail_on_p2",
        "agent_timeout_seconds",
    }
    unknown_keys = [key for key in review_section.keys() if key not in allowed_keys]
    if unknown_keys:
        unknown = ", ".join(sorted(str(key) for key in unknown_keys))
        raise ConfigurationError(
            f"Unsupported review config option(s) in {config_path}: {unknown}",
            "Remove or rename unsupported fields under the review section.",
        )

    normalized: dict[str, Any] = {}

    if "default_agents" in review_section:
        raw_agents = review_section["default_agents"]
        if not isinstance(raw_agents, list):
            raise ConfigurationError(
                f"review.default_agents in {config_path} must be a list.",
                "Use a list of review agent identifiers under the review section.",
            )
        try:
            normalized["default_agents"] = _validate_agents(
                raw_agents, "review.default_agents"
            )
        except ValueError as exc:
            allowed = ", ".join(ALLOWED_AGENTS)
            raise ConfigurationError(
                f"{exc} Update review.default_agents in {config_path} to one of: {allowed}.",
                "Replace invalid agent names with supported review agents.",
            )

    if "always_full_review" in review_section:
        raw_full = review_section["always_full_review"]
        if not isinstance(raw_full, bool):
            raise ConfigurationError(
                f"review.always_full_review in {config_path} must be a boolean.",
                "Set always_full_review to true or false.",
            )
        normalized["full_review"] = raw_full

    if "skip_review" in review_section:
        raw_skip = review_section["skip_review"]
        if not isinstance(raw_skip, bool):
            raise ConfigurationError(
                f"review.skip_review in {config_path} must be a boolean.",
                "Set skip_review to true or false.",
            )
        normalized["skip_review"] = raw_skip

    if "output_format" in review_section:
        raw_format = review_section["output_format"]
        if not isinstance(raw_format, str):
            raise ConfigurationError(
                f"review.output_format in {config_path} must be a string.",
                "Use 'text' or 'json' for output_format.",
            )
        normalized_format = raw_format.strip().lower()
        if normalized_format not in ALLOWED_OUTPUT_FORMATS:
            allowed_formats = ", ".join(ALLOWED_OUTPUT_FORMATS)
            raise ConfigurationError(
                f"Invalid review.output_format '{raw_format}' in {config_path}. Allowed: {allowed_formats}.",
                "Set output_format to text or json.",
            )
        normalized["output_format"] = normalized_format

    if "summary_only" in review_section:
        raw_summary = review_section["summary_only"]
        if not isinstance(raw_summary, bool):
            raise ConfigurationError(
                f"review.summary_only in {config_path} must be a boolean.",
                "Set summary_only to true or false.",
            )
        normalized["summary_only"] = raw_summary

    fail_on_p2 = review_section.get("fail_on_p2")
    fail_on_p1 = review_section.get("fail_on_p1")
    if fail_on_p2 is not None and not isinstance(fail_on_p2, bool):
        raise ConfigurationError(
            f"review.fail_on_p2 in {config_path} must be a boolean.",
            "Set fail_on_p2 to true or false.",
        )
    if fail_on_p1 is not None and not isinstance(fail_on_p1, bool):
        raise ConfigurationError(
            f"review.fail_on_p1 in {config_path} must be a boolean.",
            "Set fail_on_p1 to true or false.",
        )
    if fail_on_p2 or fail_on_p1:
        normalized["fail_threshold"] = "p2" if fail_on_p2 else "p1"

    if "agent_timeout_seconds" in review_section:
        raw_timeout = review_section["agent_timeout_seconds"]
        if not isinstance(raw_timeout, int):
            raise ConfigurationError(
                f"review.agent_timeout_seconds in {config_path} must be an integer.",
                "Use a positive integer number of seconds.",
            )
        if raw_timeout <= 0:
            raise ConfigurationError(
                f"review.agent_timeout_seconds in {config_path} must be greater than zero.",
                "Increase agent_timeout_seconds to a positive number of seconds.",
            )
        normalized["timeout_seconds"] = raw_timeout

    return normalized


@dataclass
class ReviewConfig:
    """User-configurable review options.

    Attributes:
        explicit_agents: Exact list of agents to run (highest precedence).
        add_agents: Agents to add to the baseline selection.
        remove_agents: Agents to remove from the baseline selection.
        default_agents: Configured default agent set when detection/server are absent or overridden.
        full_review: Force all review agents to run.
        skip_review: Skip the review phase entirely.
        output_format: Optional output format (text or json).
        quiet: Suppress detailed review output.
        summary_only: Show only summary counts.
        fail_threshold: Optional failure threshold identifier (p1 or p2).
        timeout_seconds: Optional per-agent timeout in seconds.
    """

    explicit_agents: list[str] | None = None
    add_agents: list[str] = field(default_factory=list)
    remove_agents: list[str] = field(default_factory=list)
    default_agents: list[str] | None = None
    full_review: bool = False
    skip_review: bool = False
    output_format: str | None = None
    quiet: bool = False
    summary_only: bool = False
    fail_threshold: str | None = None
    timeout_seconds: int | None = None

    def __post_init__(self) -> None:
        """Validate agent lists and incompatible options."""
        if self.full_review and self.skip_review:
            raise ValueError("full_review and skip_review cannot both be true.")

        self.explicit_agents = _validate_agents(self.explicit_agents, "explicit_agents")
        self.add_agents = _validate_agents(self.add_agents, "add_agents") or []
        self.remove_agents = _validate_agents(self.remove_agents, "remove_agents") or []
        self.default_agents = _validate_agents(self.default_agents, "default_agents")

        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be a positive integer when provided.")

        if self.output_format is not None:
            normalized_format = self.output_format.strip().lower()
            if normalized_format not in ALLOWED_OUTPUT_FORMATS:
                allowed = ", ".join(ALLOWED_OUTPUT_FORMATS)
                raise ValueError(
                    f"Invalid output_format '{self.output_format}'. Allowed: {allowed}."
                )
            self.output_format = normalized_format

        if self.fail_threshold is not None:
            normalized_threshold = self.fail_threshold.strip().lower()
            if normalized_threshold not in ALLOWED_FAIL_THRESHOLDS:
                allowed = ", ".join(ALLOWED_FAIL_THRESHOLDS)
                raise ValueError(
                    f"Invalid fail_threshold '{self.fail_threshold}'. Allowed: {allowed}."
                )
            self.fail_threshold = normalized_threshold

    @classmethod
    def from_cli_and_config(
        cls,
        *,
        project_path: Path | None,
        explicit_agents: list[str] | None = None,
        add_agents: list[str] | None = None,
        remove_agents: list[str] | None = None,
        default_agents: list[str] | None = None,
        full_review: bool = False,
        skip_review: bool = False,
        output_format: str | None = None,
        quiet: bool = False,
        summary_only: bool = False,
        fail_threshold: str | None = None,
        timeout_seconds: int | None = None,
    ) -> ReviewConfig:
        """Create a ReviewConfig merged from CLI inputs and project config.

        Precedence:
        - CLI flags: explicit/skip/full/output/summary/fail/timeout
        - Project config: .obra/config.yaml review section
        - Defaults: rely on detection/server for agent selection

        Args:
            project_path: Project root containing .obra/config.yaml
            explicit_agents: Exact list of agents from CLI --review-agents
            add_agents: Agents to add via CLI modifiers
            remove_agents: Agents to remove via CLI modifiers
            default_agents: Optional default baseline agents (CLI/config)
            full_review: CLI flag to run all agents
            skip_review: CLI flag to skip review entirely
            output_format: CLI review output format (text/json)
            quiet: CLI quiet flag
            summary_only: CLI summary-only flag
            fail_threshold: CLI failure threshold (p1/p2)
            timeout_seconds: CLI per-agent timeout seconds

        Returns:
            ReviewConfig instance with merged settings.
        """
        config_values = load_review_config(project_path) if project_path else {}
        add_agents = add_agents or []
        remove_agents = remove_agents or []
        effective_default_agents = default_agents or config_values.get("default_agents")

        config_full = bool(config_values.get("full_review", False))
        config_skip = bool(config_values.get("skip_review", False))
        effective_skip = skip_review
        effective_full = full_review
        if not effective_skip and not effective_full:
            effective_skip = config_skip
            effective_full = config_full

        config_output_format = config_values.get("output_format")
        config_summary_only = bool(config_values.get("summary_only", False))
        config_fail_threshold = config_values.get("fail_threshold")
        config_timeout = config_values.get("timeout_seconds")

        effective_output_format = output_format or config_output_format
        effective_summary_only = summary_only or config_summary_only
        effective_fail_threshold = fail_threshold or config_fail_threshold
        effective_timeout = (
            timeout_seconds if timeout_seconds is not None else config_timeout
        )

        feature_skip, feature_disabled = resolve_feature_review_gates()
        explicit_override = explicit_agents is not None or full_review
        if not explicit_override:
            if feature_skip and not effective_full:
                effective_skip = True
            if feature_disabled and not effective_skip and not effective_full:
                explicit_additions = set(add_agents)
                for agent in feature_disabled:
                    if agent in explicit_additions:
                        continue
                    if agent not in remove_agents:
                        remove_agents.append(agent)

        return cls(
            explicit_agents=explicit_agents,
            add_agents=add_agents,
            remove_agents=remove_agents,
            default_agents=effective_default_agents,
            full_review=effective_full,
            skip_review=effective_skip,
            output_format=effective_output_format,
            quiet=quiet or bool(config_values.get("quiet", False)),
            summary_only=effective_summary_only,
            fail_threshold=effective_fail_threshold,
            timeout_seconds=effective_timeout,
        )

    def resolve_agents(
        self,
        detected_agents: Sequence[str] | None = None,
        server_agents: Sequence[str] | None = None,
    ) -> list[str]:
        """Resolve which review agents should run.

        Precedence (highest to lowest):
        1. skip_review short-circuits to no agents
        2. explicit_agents (when provided)
        3. add/remove modifiers applied on top of the baseline
        4. full_review/default_agents override the baseline list
        5. server_agents baseline, otherwise detected_agents

        Args:
            detected_agents: Agents chosen by local detection.
            server_agents: Agents provided by the server.

        Returns:
            Ordered list of agent identifiers to run.
        """
        if self.skip_review:
            return []

        baseline: list[str] = []

        if self.full_review:
            baseline = list(ALLOWED_AGENTS)
        else:
            server_list = _filter_allowed(server_agents)
            detected_list = _filter_allowed(detected_agents)

            baseline = server_list or detected_list
            if self.default_agents is not None:
                baseline = list(self.default_agents)

        if not baseline:
            baseline = list(ALLOWED_AGENTS)

        # Apply removals first so additions can reintroduce if desired.
        if self.remove_agents:
            remove_set = set(self.remove_agents)
            baseline = [agent for agent in baseline if agent not in remove_set]

        for agent in self.add_agents:
            if agent not in baseline:
                baseline.append(agent)

        if self.explicit_agents is not None:
            return list(self.explicit_agents)

        return baseline


__all__ = [
    "ALLOWED_AGENTS",
    "ALLOWED_FAIL_THRESHOLDS",
    "ALLOWED_OUTPUT_FORMATS",
    "REVIEW_CONFIG_RELATIVE_PATH",
    "ReviewConfig",
    "load_review_config",
    "resolve_feature_review_gates",
]
