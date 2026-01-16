"""TieredResolver - Prioritized tier resolution for agents, rules, tools, and patterns.

Part of EPIC-SOTA-001: Tiered Agent & Guidance Architecture.

This module provides:
- TierInterface: Abstract base class for tier implementations
- TieredResolver: Main resolver that walks tiers top-down
- BaselineTier: Default fallback tier (Tier 3)
- Resolution dataclasses for type-safe returns

Resolution Order: Customer (Tier 0) > Obra (Tier 1) > SOTA (Tier 2) > Baseline (Tier 3)

Example:
    >>> from obra.workflow.tiered_resolver import TieredResolver
    >>> resolver = TieredResolver(project_path, obra_path)
    >>> result = resolver.resolve_agent("investigate this bug")
    >>> print(f"Selected: {result.agent.name} from {result.source_tier}")
"""

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from obra.schemas.closeout_schema import CloseoutTask, CloseoutTemplate

logger = logging.getLogger(__name__)


# =============================================================================
# Data Classes for Resolution Results
# =============================================================================


@dataclass
class AgentSuggestion:
    """Suggestion from a single tier for an agent match."""

    agent: dict[str, Any]
    confidence: float
    command: str | None = None
    reason: str | None = None


@dataclass
class AgentResolution:
    """Result of agent resolution across all tiers."""

    agent: dict[str, Any] | None
    source_tier: str  # "customer", "obra", "sota", "baseline"
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def found(self) -> bool:
        """Whether an agent was found."""
        return self.agent is not None


@dataclass
class Rule:
    """A resolved rule from the tiered system."""

    id: str
    name: str
    rule_type: str
    content: dict[str, Any]
    source_tier: str
    priority: int = 50
    override: bool = False
    enabled: bool = True


@dataclass
class ToolGuidance:
    """Tool guidance resolved from tiers."""

    tool_name: str
    when_to_use: str
    when_not_to_use: str | None = None
    best_practices: list[str] = field(default_factory=list)
    examples: list[dict[str, str]] = field(default_factory=list)
    source_tier: str = "baseline"

    def without_examples(self) -> "ToolGuidance":
        """Return copy without examples (for standard guidance level)."""
        return ToolGuidance(
            tool_name=self.tool_name,
            when_to_use=self.when_to_use,
            when_not_to_use=self.when_not_to_use,
            best_practices=self.best_practices,
            examples=[],  # Strip examples
            source_tier=self.source_tier,
        )


@dataclass
class CloseoutResolution:
    """Resolution result for close-out template selection."""

    template: CloseoutTemplate
    source_tiers: list[str] = field(default_factory=list)


# =============================================================================
# Tier Interface (Abstract Base Class)
# =============================================================================


class TierInterface(ABC):
    """Abstract interface for configuration tiers.

    Each tier (Customer, Obra, SOTA, Baseline) must implement this interface.
    Tiers are queried in order; first confident match wins.

    Attributes:
        name: Tier identifier (e.g., "customer", "obra", "sota", "baseline")
        confidence_threshold: Minimum confidence for agent matches
    """

    name: str = "unknown"
    confidence_threshold: float = 0.6

    @abstractmethod
    def is_empty(self) -> bool:
        """Check if tier has any assets loaded.

        Returns:
            True if tier has no agents, rules, tools, or patterns
        """

    @abstractmethod
    def is_enabled(self) -> bool:
        """Check if tier is enabled in configuration.

        Returns:
            True if tier should be queried during resolution
        """

    @abstractmethod
    def match_agent(self, task: str) -> AgentSuggestion | None:
        """Find matching agent for a task description.

        Args:
            task: Natural language task description

        Returns:
            AgentSuggestion if a match is found, None otherwise
        """

    @abstractmethod
    def get_rules(self, context: str) -> list[Rule]:
        """Get applicable rules for a context.

        Args:
            context: Context identifier (e.g., "code_review", "implementation")

        Returns:
            List of rules that apply to this context
        """

    @abstractmethod
    def get_tool_guidance(self, tool: str) -> ToolGuidance | None:
        """Get guidance for a specific tool.

        Args:
            tool: Tool name (e.g., "grep", "read", "bash")

        Returns:
            ToolGuidance if found, None otherwise
        """

    def get_patterns(self, category: str | None = None) -> list[dict[str, Any]]:
        """Get workflow patterns, optionally filtered by category.

        Args:
            category: Optional category filter

        Returns:
            List of pattern definitions
        """
        return []


# =============================================================================
# Baseline Tier (Tier 3) - Always Available Fallback
# =============================================================================


class BaselineTier(TierInterface):
    """Tier 3: Baseline tier with model native capabilities.

    This tier is never empty and always enabled. It provides fallback
    behavior when no higher tiers have matches.

    The baseline tier represents what the model can do without any
    specialized guidance - essentially "no special handling."
    """

    name = "baseline"
    confidence_threshold = 0.0  # Always matches as fallback

    def __init__(self):
        """Initialize baseline tier with default guidance."""
        self._tool_guidance = self._build_default_tool_guidance()

    def is_empty(self) -> bool:
        """Baseline tier is never empty."""
        return False

    def is_enabled(self) -> bool:
        """Baseline tier is always enabled."""
        return True

    def match_agent(self, task: str) -> AgentSuggestion | None:
        """Baseline provides no specific agent - returns None.

        Higher tiers should handle agent matching. Baseline indicates
        "use general-purpose capabilities" by returning None.
        """
        return None

    def get_rules(self, context: str) -> list[Rule]:
        """Baseline has no special rules."""
        return []

    def get_tool_guidance(self, tool: str) -> ToolGuidance | None:
        """Get basic tool guidance from baseline.

        Provides minimal guidance for common tools.
        """
        return self._tool_guidance.get(tool)

    def _build_default_tool_guidance(self) -> dict[str, ToolGuidance]:
        """Build default tool guidance for common tools."""
        return {
            "grep": ToolGuidance(
                tool_name="grep",
                when_to_use="Searching for patterns across multiple files",
                when_not_to_use="When you know the exact file - use read instead",
                best_practices=[
                    "Use specific patterns to reduce noise",
                    "Prefer file type filters when applicable",
                ],
                source_tier="baseline",
            ),
            "read": ToolGuidance(
                tool_name="read",
                when_to_use="Reading file contents when you know the path",
                when_not_to_use="When searching across many files - use grep",
                best_practices=[
                    "Specify line ranges for large files",
                    "Use for targeted reading after finding location with grep",
                ],
                source_tier="baseline",
            ),
            "bash": ToolGuidance(
                tool_name="bash",
                when_to_use="Running shell commands, git operations, tests",
                when_not_to_use="File operations that have dedicated tools",
                best_practices=[
                    "Prefer dedicated tools over bash for file ops",
                    "Chain commands with && for sequential execution",
                ],
                source_tier="baseline",
            ),
            "edit": ToolGuidance(
                tool_name="edit",
                when_to_use="Making targeted changes to existing files",
                when_not_to_use="Creating new files - use write instead",
                best_practices=[
                    "Provide enough context for unique matching",
                    "Preview changes before applying",
                ],
                source_tier="baseline",
            ),
            "write": ToolGuidance(
                tool_name="write",
                when_to_use="Creating new files or completely rewriting existing ones",
                when_not_to_use="Small edits to existing files - use edit instead",
                best_practices=[
                    "Prefer editing over writing for existing files",
                    "Include all necessary content in single write",
                ],
                source_tier="baseline",
            ),
        }


# =============================================================================
# Tiered Resolver - Main Resolution Engine
# =============================================================================


class TieredResolver:
    """Resolve assets through prioritized tier system.

    Resolution walks tiers top-down (Customer > Obra > SOTA > Baseline),
    returning the first confident match.

    Attributes:
        tiers: List of tiers in priority order
        project_path: Path to customer project
        obra_path: Path to Obra installation

    Example:
        >>> resolver = TieredResolver(project_path, obra_path)
        >>> result = resolver.resolve_agent("fix the login bug")
        >>> if result.found:
        ...     print(f"Use {result.agent['name']} from {result.source_tier}")
    """

    def __init__(
        self,
        project_path: Path | None = None,
        obra_path: Path | None = None,
        tiers: list[TierInterface] | None = None,
    ):
        """Initialize TieredResolver.

        Args:
            project_path: Path to customer project (for Tier 0)
            obra_path: Path to Obra installation (for Tier 1, 2)
            tiers: Optional pre-configured tier list (for testing)
        """
        self.project_path = Path(project_path) if project_path else None
        self.obra_path = Path(obra_path) if obra_path else None

        if tiers is not None:
            self.tiers = tiers
        else:
            self.tiers = self._build_default_tiers()

        logger.info(
            f"TieredResolver initialized with {len(self.tiers)} tiers: "
            f"{[t.name for t in self.tiers]}"
        )

    def _build_default_tiers(self) -> list[TierInterface]:
        """Build default tier stack.

        Returns list in priority order:
        1. CustomerTier (if project_path exists)
        2. ObraTunedTier (if obra_path exists)
        3. SOTALibraryTier (if obra_path exists)
        4. BaselineTier (always)
        """
        tiers: list[TierInterface] = []

        # Tier 0: Customer (lazy import to avoid circular deps)
        if self.project_path:
            try:
                from obra.workflow.customer_tier import CustomerTier

                customer_tier = CustomerTier(self.project_path / ".obra")
                tiers.append(customer_tier)
            except ImportError:
                logger.debug("CustomerTier not available yet")

        # Tier 1: Obra-tuned
        if self.obra_path:
            try:
                from obra.workflow.obra_tier import ObraTunedTier

                obra_tier = ObraTunedTier(self.obra_path / "config/tiers/tier1_obra")
                tiers.append(obra_tier)
            except ImportError:
                logger.debug("ObraTunedTier not available yet")

        # Tier 2: SOTA Library
        if self.obra_path:
            try:
                from obra.workflow.sota_tier import SOTALibraryTier

                sota_tier = SOTALibraryTier(self.obra_path / "config/tiers/tier2_sota")
                tiers.append(sota_tier)
            except ImportError:
                logger.debug("SOTALibraryTier not available yet")

        # Tier 3: Baseline (always present)
        tiers.append(BaselineTier())

        return tiers

    def resolve_agent(self, task: str) -> AgentResolution:
        """Resolve agent for a task using tiered resolution.

        Walks tiers in priority order, returning first confident match.

        Args:
            task: Natural language task description

        Returns:
            AgentResolution with agent details and source tier

        Example:
            >>> result = resolver.resolve_agent("investigate bug #123")
            >>> if result.found:
            ...     print(f"Selected {result.agent['name']} ({result.confidence:.2f})")
        """
        for tier in self.tiers:
            # Skip empty or disabled tiers
            if tier.is_empty() or not tier.is_enabled():
                logger.debug(
                    f"Skipping tier '{tier.name}' (empty={tier.is_empty()}, enabled={tier.is_enabled()})"
                )
                continue

            suggestion = tier.match_agent(task)

            if suggestion and suggestion.confidence >= tier.confidence_threshold:
                logger.info(
                    f"Agent resolved from tier '{tier.name}': "
                    f"{suggestion.agent.get('name', 'unknown')} "
                    f"(confidence: {suggestion.confidence:.2f})"
                )
                return AgentResolution(
                    agent=suggestion.agent,
                    source_tier=tier.name,
                    confidence=suggestion.confidence,
                    metadata={
                        "command": suggestion.command,
                        "reason": suggestion.reason,
                        "tier_threshold": tier.confidence_threshold,
                    },
                )

        # No match - return baseline resolution
        logger.debug(f"No agent match for task: {task[:50]}...")
        return AgentResolution(
            agent=None,
            source_tier="baseline",
            confidence=0.0,
            metadata={"reason": "No tier provided confident match"},
        )

    def resolve_rules(self, context: str) -> list[Rule]:
        """Resolve rules from all tiers with merge semantics.

        Rules are collected from all enabled tiers and merged:
        - extend mode (default): Rules from all tiers are combined
        - replace mode: Higher tier rule with same ID replaces lower
        - disable mode: Rule is excluded

        Args:
            context: Context identifier for rule filtering

        Returns:
            List of applicable rules, merged from all tiers

        Example:
            >>> rules = resolver.resolve_rules("code_review")
            >>> for rule in rules:
            ...     print(f"{rule.name} from {rule.source_tier}")
        """
        rules: list[Rule] = []
        seen_ids: set = set()

        for tier in self.tiers:
            if not tier.is_enabled():
                continue

            tier_rules = tier.get_rules(context)

            for rule in tier_rules:
                if not rule.enabled:
                    continue

                if rule.override and rule.id in seen_ids:
                    # Replace mode: remove existing rule with same ID
                    rules = [r for r in rules if r.id != rule.id]
                    logger.debug(f"Rule '{rule.id}' overridden by {tier.name}")

                if rule.id not in seen_ids or rule.override:
                    rules.append(rule)
                    seen_ids.add(rule.id)

        # Sort by priority (higher first)
        rules.sort(key=lambda r: r.priority, reverse=True)

        logger.debug(f"Resolved {len(rules)} rules for context '{context}'")
        return rules

    def resolve_tool_guidance(self, tool: str) -> ToolGuidance | None:
        """Resolve tool guidance from highest priority tier.

        Args:
            tool: Tool name to get guidance for

        Returns:
            ToolGuidance from first tier that has it, or None

        Example:
            >>> guidance = resolver.resolve_tool_guidance("grep")
            >>> if guidance:
            ...     print(guidance.when_to_use)
        """
        for tier in self.tiers:
            if tier.is_empty() or not tier.is_enabled():
                continue

            guidance = tier.get_tool_guidance(tool)
            if guidance:
                logger.debug(f"Tool guidance for '{tool}' from tier '{tier.name}'")
                return guidance

        return None

    def get_all_tool_guidance(self) -> dict[str, ToolGuidance]:
        """Get merged tool guidance from all tiers.

        Returns:
            Dictionary mapping tool names to guidance (higher tiers override)
        """
        all_guidance: dict[str, ToolGuidance] = {}

        # Process in reverse order so higher tiers override
        for tier in reversed(self.tiers):
            if tier.is_empty() or not tier.is_enabled():
                continue

            # Get all tools this tier has guidance for
            if hasattr(tier, "_tool_guidance"):
                for tool_name, guidance in tier._tool_guidance.items():
                    all_guidance[tool_name] = guidance

        return all_guidance

    def resolve_pattern(self, pattern_id: str) -> dict[str, Any] | None:
        """Resolve a specific pattern by ID.

        Args:
            pattern_id: Pattern identifier

        Returns:
            Pattern definition from highest priority tier, or None
        """
        for tier in self.tiers:
            if tier.is_empty() or not tier.is_enabled():
                continue

            patterns = tier.get_patterns()
            for pattern in patterns:
                if pattern.get("id") == pattern_id:
                    pattern["_source_tier"] = tier.name
                    return pattern

        return None

    def resolve_closeout(self, domain: str | None = None) -> CloseoutResolution | None:
        """Resolve close-out template using tier priority.

        Resolution order:
        1. Baseline template (fallback)
        2. Domain template (e.g., software-dev)
        3. Customer template (.obra/templates/closeout.yaml)

        Higher tiers override lower-tier tasks by ID; new tasks append in order.

        Args:
            domain: Optional domain key for template selection. Defaults to software-dev.

        Returns:
            CloseoutResolution with merged template and source tiers, or None if nothing found.
        """
        selected_domain = domain or "software-dev"
        templates: list[tuple[str, CloseoutTemplate]] = []

        baseline_template = self._load_baseline_closeout_template()
        if baseline_template:
            templates.append(("baseline", baseline_template))

        domain_template = self._load_domain_closeout_template(selected_domain)
        if domain_template:
            templates.append(("domain", domain_template))

        customer_template = self._load_customer_closeout_template()
        if customer_template:
            templates.append(("customer", customer_template))

        if not templates:
            logger.warning("No close-out templates found for resolution")
            return None

        resolution = self._merge_closeout_templates(templates, selected_domain)
        logger.debug(
            "Resolved close-out template for domain '%s' from tiers: %s",
            selected_domain,
            resolution.source_tiers,
        )
        return resolution

    def list_agents(self) -> list[dict[str, Any]]:
        """List all available agents from all tiers.

        Returns:
            List of agent definitions with source tier info
        """
        agents = []
        seen_ids: set = set()

        for tier in self.tiers:
            if tier.is_empty() or not tier.is_enabled():
                continue

            # Access tier's agents if available
            if hasattr(tier, "agents"):
                for agent_id, agent in tier.agents.items():
                    if agent_id not in seen_ids:
                        agent_copy = dict(agent)
                        agent_copy["_source_tier"] = tier.name
                        agents.append(agent_copy)
                        seen_ids.add(agent_id)

        return agents

    def _load_closeout_template_from_path(self, path: Path) -> CloseoutTemplate | None:
        """Load and validate close-out template from a YAML file."""
        if not path.exists():
            return None

        try:
            with open(path, encoding="utf-8") as f:
                template_data = yaml.safe_load(f) or {}

            template = CloseoutTemplate(**template_data)
            logger.debug("Loaded close-out template from %s", path)
            return template

        except ValidationError as exc:
            logger.error("Invalid close-out template at %s: %s", path, exc)
        except Exception as exc:
            logger.error("Failed to load close-out template from %s: %s", path, exc)

        return None

    def _load_customer_closeout_template(self) -> CloseoutTemplate | None:
        """Load close-out template provided by customer tier."""
        for tier in self.tiers:
            if not tier.is_enabled():
                continue

            getter = getattr(tier, "get_closeout_template", None)
            if callable(getter):
                template = getter()
                if template:
                    return template

        if not self.project_path:
            return None

        fallback_path = self.project_path / ".obra" / "templates" / "closeout.yaml"
        return self._load_closeout_template_from_path(fallback_path)

    def _load_domain_closeout_template(self, domain: str) -> CloseoutTemplate | None:
        """Load domain-specific close-out template from Obra templates."""
        if not self.obra_path:
            return None

        domain_path = self.obra_path / "obra" / "templates" / "closeout" / f"{domain}.yaml"
        return self._load_closeout_template_from_path(domain_path)

    def _load_baseline_closeout_template(self) -> CloseoutTemplate | None:
        """Load baseline close-out template."""
        if not self.obra_path:
            return None

        baseline_path = self.obra_path / "obra" / "templates" / "closeout" / "baseline.yaml"
        return self._load_closeout_template_from_path(baseline_path)

    def _merge_closeout_templates(
        self, templates: list[tuple[str, CloseoutTemplate]], domain: str
    ) -> CloseoutResolution:
        """Merge close-out templates in priority order (lowest to highest)."""
        merged_tasks: dict[str, CloseoutTask] = {}
        ordered_ids: list[str] = []
        source_tiers: list[str] = []

        for source, template in templates:
            source_tiers.append(source)
            for task in template.tasks:
                if task.id in merged_tasks:
                    merged_tasks[task.id] = task
                    continue

                merged_tasks[task.id] = task
                ordered_ids.append(task.id)

        notes = None
        for _, template in reversed(templates):
            if template.notes:
                notes = template.notes
                break

        merged_template = CloseoutTemplate(
            domain=domain,
            tasks=[merged_tasks[task_id] for task_id in ordered_ids],
            notes=notes,
        )
        return CloseoutResolution(template=merged_template, source_tiers=source_tiers)

    def get_tier_status(self) -> list[dict[str, Any]]:
        """Get status of all tiers for diagnostics.

        Returns:
            List of tier status dictionaries
        """
        return [
            {
                "name": tier.name,
                "enabled": tier.is_enabled(),
                "empty": tier.is_empty(),
                "confidence_threshold": tier.confidence_threshold,
            }
            for tier in self.tiers
        ]


# =============================================================================
# Utility Functions
# =============================================================================


def compute_text_similarity(text1: str, text2: str) -> float:
    """Compute simple text similarity using word overlap.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score between 0 and 1
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = words1 & words2
    union = words1 | words2

    return len(intersection) / len(union)


def match_patterns(text: str, patterns: list[str]) -> tuple[bool, float]:
    """Match text against a list of regex patterns.

    Args:
        text: Text to match
        patterns: List of regex patterns

    Returns:
        Tuple of (matched, confidence)
    """
    text_lower = text.lower()
    match_count = 0

    for pattern in patterns:
        try:
            if re.search(pattern, text_lower, re.IGNORECASE):
                match_count += 1
        except re.error:
            logger.warning(f"Invalid regex pattern: {pattern}")

    if match_count == 0:
        return False, 0.0

    # Confidence based on pattern match ratio
    confidence = min(0.5 + (match_count / len(patterns)) * 0.5, 1.0)
    return True, confidence


# Type alias for backward compatibility
