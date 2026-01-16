"""ObraTunedTier - Tier 1 implementation for Obra-curated agents and patterns.

Part of EPIC-SOTA-001: Tiered Agent & Guidance Architecture.

This module provides the ObraTunedTier class which implements TierInterface
for Obra's curated, tested agents and patterns.

Example:
    >>> from obra.workflow.obra_tier import ObraTunedTier
    >>> tier = ObraTunedTier(Path('config/tiers/tier1_obra'))
    >>> suggestion = tier.match_agent("investigate bug #123")
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from obra.workflow.tiered_resolver import (
    AgentSuggestion,
    Rule,
    TierInterface,
    ToolGuidance,
)

logger = logging.getLogger(__name__)


# Effectiveness tracking storage (in-memory for now)
_effectiveness_data: dict[str, dict[str, Any]] = {}


class ObraTunedTier(TierInterface):
    """Tier 1: Obra-tuned agents and patterns.

    This tier contains Obra's curated, tested agents that have been
    optimized for autonomous software development workflows.

    Attributes:
        path: Path to tier1_obra directory
        manifest: Loaded manifest data
        agents: Dictionary of loaded agent definitions
        confidence_threshold: Minimum confidence for matches (0.7)
    """

    name = "obra"
    confidence_threshold = 0.7  # High bar for Obra agents

    def __init__(self, tier_path: Path):
        """Initialize ObraTunedTier.

        Args:
            tier_path: Path to tier1_obra directory
        """
        self.path = Path(tier_path)
        self.manifest: dict[str, Any] = {}
        self.agents: dict[str, dict[str, Any]] = {}
        self.rules: dict[str, dict[str, Any]] = {}
        self.tools: dict[str, dict[str, Any]] = {}
        self.patterns: dict[str, dict[str, Any]] = {}
        self._loaded = False
        self._enabled = True

        self._ensure_loaded()

    def _ensure_loaded(self) -> None:
        """Ensure tier assets are loaded."""
        if self._loaded:
            return

        if not self.path.exists():
            logger.debug(f"ObraTunedTier path does not exist: {self.path}")
            self._loaded = True
            return

        manifest_path = self.path / "manifest.yaml"
        if not manifest_path.exists():
            logger.debug(f"ObraTunedTier manifest not found: {manifest_path}")
            self._loaded = True
            return

        try:
            with open(manifest_path, encoding="utf-8") as f:
                self.manifest = yaml.safe_load(f) or {}

            # Update confidence threshold from manifest if specified
            if "confidence_threshold" in self.manifest:
                self.confidence_threshold = self.manifest["confidence_threshold"]

            # Load agents
            self.agents = self._load_agents()

            # Load rules, tools, patterns (if they exist)
            self.rules = self._load_asset_type("rules")
            self.tools = self._load_asset_type("tools")
            self.patterns = self._load_asset_type("patterns")

            self._loaded = True
            logger.info(
                f"ObraTunedTier loaded: {len(self.agents)} agents, "
                f"{len(self.rules)} rules, {len(self.patterns)} patterns"
            )

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse ObraTunedTier manifest: {e}")
            self._loaded = True
        except Exception as e:
            logger.error(f"Failed to load ObraTunedTier: {e}")
            self._loaded = True

    def _load_agents(self) -> dict[str, dict[str, Any]]:
        """Load all agent definitions from agents directory."""
        agents: dict[str, dict[str, Any]] = {}
        agents_dir = self.path / "agents"

        if not agents_dir.exists():
            return agents

        for file_path in agents_dir.glob("*.yaml"):
            if file_path.name.startswith("."):
                continue

            try:
                with open(file_path, encoding="utf-8") as f:
                    agent_data = yaml.safe_load(f) or {}

                agent_id = agent_data.get("id", file_path.stem)
                agent_data["_source_path"] = str(file_path)
                agents[agent_id] = agent_data

                logger.debug(f"Loaded Obra agent: {agent_id}")

            except Exception as e:
                logger.error(f"Failed to load agent {file_path}: {e}")

        return agents

    def _load_asset_type(self, asset_type: str) -> dict[str, dict[str, Any]]:
        """Load all assets of a given type."""
        assets: dict[str, dict[str, Any]] = {}
        assets_dir = self.path / asset_type

        if not assets_dir.exists():
            return assets

        for file_path in assets_dir.glob("*.yaml"):
            if file_path.name.startswith("."):
                continue

            try:
                with open(file_path, encoding="utf-8") as f:
                    asset_data = yaml.safe_load(f) or {}

                asset_id = asset_data.get("id", file_path.stem)
                asset_data["_source_path"] = str(file_path)
                assets[asset_id] = asset_data

            except Exception as e:
                logger.error(f"Failed to load {asset_type}/{file_path.name}: {e}")

        return assets

    def is_empty(self) -> bool:
        """Check if tier has any assets."""
        self._ensure_loaded()
        return not (self.agents or self.rules or self.tools or self.patterns)

    def is_enabled(self) -> bool:
        """Check if tier is enabled."""
        return self._enabled and self.path.exists()

    def match_agent(self, task: str) -> AgentSuggestion | None:
        """Find matching agent for a task description.

        Uses pattern matching with confidence scoring based on:
        - Number of matching patterns
        - Keyword matches
        - Confidence boost for strong matches

        Args:
            task: Natural language task description

        Returns:
            AgentSuggestion if a confident match is found, None otherwise
        """
        self._ensure_loaded()

        if not self.agents:
            return None

        task_lower = task.lower()
        best_match: AgentSuggestion | None = None
        best_confidence = 0.0

        for agent_id, agent in self.agents.items():
            matching = agent.get("matching", {})
            patterns = matching.get("patterns", [])
            keywords = matching.get("keywords", [])
            exclude_patterns = matching.get("exclude_patterns", [])
            confidence_boost = matching.get("confidence_boost", 0.0)

            # Check exclusions first
            if self._matches_any_pattern(task_lower, exclude_patterns):
                continue

            # Calculate confidence from patterns
            pattern_confidence = self._compute_pattern_confidence(task_lower, patterns)

            # Calculate confidence from keywords
            keyword_confidence = self._compute_keyword_confidence(task_lower, keywords)

            # Combine confidences (weighted average)
            if patterns and keywords:
                base_confidence = (pattern_confidence * 0.6) + (keyword_confidence * 0.4)
            elif patterns:
                base_confidence = pattern_confidence
            elif keywords:
                base_confidence = keyword_confidence
            else:
                continue  # No matching criteria

            # Apply confidence boost
            total_confidence = min(base_confidence + confidence_boost, 1.0)

            if total_confidence > best_confidence:
                best_confidence = total_confidence
                best_match = AgentSuggestion(
                    agent=agent,
                    confidence=total_confidence,
                    command=agent.get("protocol", {}).get("invocation"),
                    reason=f"Matched {agent.get('name', agent_id)}",
                )

        # Track effectiveness event
        if best_match:
            self._track_suggestion(best_match.agent.get("id", "unknown"), task)

        return best_match

    def _compute_pattern_confidence(self, text: str, patterns: list[str]) -> float:
        """Compute confidence score based on pattern matches.

        Args:
            text: Text to match (already lowercase)
            patterns: List of regex patterns

        Returns:
            Confidence score between 0 and 1
        """
        if not patterns:
            return 0.0

        match_count = 0
        for pattern in patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    match_count += 1
            except re.error:
                logger.warning(f"Invalid regex pattern: {pattern}")

        if match_count == 0:
            return 0.0

        # Base confidence starts at 0.4 for any match, scales up with more matches
        base = 0.4
        match_ratio = match_count / len(patterns)
        return min(base + (match_ratio * 0.5), 0.9)

    def _compute_keyword_confidence(self, text: str, keywords: list[str]) -> float:
        """Compute confidence score based on keyword matches.

        Args:
            text: Text to match (already lowercase)
            keywords: List of keywords

        Returns:
            Confidence score between 0 and 1
        """
        if not keywords:
            return 0.0

        match_count = sum(1 for kw in keywords if kw.lower() in text)

        if match_count == 0:
            return 0.0

        # Similar scaling to pattern confidence
        base = 0.35
        match_ratio = match_count / len(keywords)
        return min(base + (match_ratio * 0.5), 0.85)

    def _matches_any_pattern(self, text: str, patterns: list[str]) -> bool:
        """Check if text matches any of the given patterns."""
        for pattern in patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    return True
            except re.error:
                pass
        return False

    def get_rules(self, context: str) -> list[Rule]:
        """Get applicable rules for a context."""
        self._ensure_loaded()

        rules = []
        for rule_id, rule_data in self.rules.items():
            conditions = rule_data.get("conditions", {})
            contexts = conditions.get("contexts", [])

            # Include if no contexts specified or context matches
            if not contexts or context in contexts:
                rules.append(
                    Rule(
                        id=rule_id,
                        name=rule_data.get("name", rule_id),
                        rule_type=rule_data.get("rule_type", "behavior"),
                        content=rule_data.get("content", {}),
                        source_tier=self.name,
                        priority=rule_data.get("priority", 50),
                        override=rule_data.get("override", False),
                        enabled=rule_data.get("enabled", True),
                    )
                )

        return rules

    def get_tool_guidance(self, tool: str) -> ToolGuidance | None:
        """Get guidance for a specific tool from this tier."""
        self._ensure_loaded()

        # Check dedicated tool guidance files
        if tool in self.tools:
            tool_data = self.tools[tool]
            guidance = tool_data.get("guidance", {})

            return ToolGuidance(
                tool_name=tool,
                when_to_use=guidance.get("when_to_use", ""),
                when_not_to_use=guidance.get("when_not_to_use"),
                best_practices=guidance.get("best_practices", []),
                examples=tool_data.get("examples", []),
                source_tier=self.name,
            )

        # Also check agent tool_guidance
        for agent in self.agents.values():
            agent_guidance = agent.get("tool_guidance", [])
            for tg in agent_guidance:
                if tg.get("tool") == tool:
                    return ToolGuidance(
                        tool_name=tool,
                        when_to_use=tg.get("when", ""),
                        when_not_to_use=tg.get("avoid_when"),
                        best_practices=tg.get("always_include", []),
                        examples=tg.get("examples", []),
                        source_tier=self.name,
                    )

        return None

    def get_patterns(self, category: str | None = None) -> list[dict[str, Any]]:
        """Get workflow patterns, optionally filtered by category."""
        self._ensure_loaded()

        if category:
            return [p for p in self.patterns.values() if p.get("category") == category]
        return list(self.patterns.values())

    # =========================================================================
    # Effectiveness Tracking (T3.6)
    # =========================================================================

    def _track_suggestion(self, agent_id: str, task: str) -> None:
        """Track when an agent is suggested for effectiveness metrics.

        Args:
            agent_id: ID of the suggested agent
            task: Task description that triggered the suggestion
        """
        global _effectiveness_data

        if agent_id not in _effectiveness_data:
            _effectiveness_data[agent_id] = {
                "suggestion_count": 0,
                "success_count": 0,
                "override_count": 0,
                "last_suggested": None,
            }

        data = _effectiveness_data[agent_id]
        data["suggestion_count"] += 1
        data["last_suggested"] = datetime.utcnow().isoformat()

        logger.debug(
            f"Tracked suggestion for agent '{agent_id}' (total: {data['suggestion_count']})"
        )

    @staticmethod
    def track_outcome(agent_id: str, success: bool) -> None:
        """Track outcome of agent execution for effectiveness metrics.

        Call this after agent completes to track success/failure.

        Args:
            agent_id: ID of the agent that executed
            success: Whether the execution was successful
        """
        global _effectiveness_data

        if agent_id not in _effectiveness_data:
            _effectiveness_data[agent_id] = {
                "suggestion_count": 0,
                "success_count": 0,
                "override_count": 0,
                "last_suggested": None,
            }

        if success:
            _effectiveness_data[agent_id]["success_count"] += 1

        logger.debug(f"Tracked {'success' if success else 'failure'} for agent '{agent_id}'")

    @staticmethod
    def track_override(agent_id: str) -> None:
        """Track when user overrides/rejects an agent suggestion.

        Args:
            agent_id: ID of the agent that was rejected
        """
        global _effectiveness_data

        if agent_id in _effectiveness_data:
            _effectiveness_data[agent_id]["override_count"] += 1
            logger.debug(f"Tracked override for agent '{agent_id}'")

    @staticmethod
    def get_effectiveness_stats() -> dict[str, dict[str, Any]]:
        """Get effectiveness statistics for all agents.

        Returns:
            Dictionary mapping agent IDs to their stats
        """
        return dict(_effectiveness_data)

    @staticmethod
    def clear_effectiveness_stats() -> None:
        """Clear all effectiveness statistics."""
        global _effectiveness_data
        _effectiveness_data.clear()

    def reload(self) -> None:
        """Force reload of tier assets."""
        self._loaded = False
        self.agents = {}
        self.rules = {}
        self.tools = {}
        self.patterns = {}
        self._ensure_loaded()
        logger.info(f"ObraTunedTier reloaded: {len(self.agents)} agents")
