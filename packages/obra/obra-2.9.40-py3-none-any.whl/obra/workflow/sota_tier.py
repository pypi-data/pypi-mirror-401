"""SOTALibraryTier - Tier 2 implementation for SOTA patterns from industry sources.

Part of EPIC-SOTA-001: Tiered Agent & Guidance Architecture.

This module provides the SOTALibraryTier class which implements TierInterface
for state-of-the-art patterns imported from research repositories.

Example:
    >>> from obra.workflow.sota_tier import SOTALibraryTier
    >>> tier = SOTALibraryTier(Path('config/tiers/tier2_sota'))
    >>> suggestion = tier.match_agent("research this topic comprehensively")
"""

import logging
import re
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


class SOTALibraryTier(TierInterface):
    """Tier 2: SOTA Library with patterns from industry sources.

    This tier contains state-of-the-art agent patterns imported from
    research repositories like Anthropic Cookbook, OpenAI Agents SDK,
    and LangGraph examples.

    Attributes:
        path: Path to tier2_sota directory
        manifest: Loaded manifest data
        agents: Dictionary of loaded agent definitions
        confidence_threshold: Minimum confidence for matches (0.6)
    """

    name = "sota"
    confidence_threshold = 0.6  # Lower than Obra tier - fallback patterns

    def __init__(self, tier_path: Path):
        """Initialize SOTALibraryTier.

        Args:
            tier_path: Path to tier2_sota directory
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
            logger.debug(f"SOTALibraryTier path does not exist: {self.path}")
            self._loaded = True
            return

        manifest_path = self.path / "manifest.yaml"
        if not manifest_path.exists():
            logger.debug(f"SOTALibraryTier manifest not found: {manifest_path}")
            self._loaded = True
            return

        try:
            with open(manifest_path, encoding="utf-8") as f:
                self.manifest = yaml.safe_load(f) or {}

            # Update confidence threshold from manifest if specified
            if "confidence_threshold" in self.manifest:
                self.confidence_threshold = self.manifest["confidence_threshold"]

            # Load agents from library directories
            self.agents = self._load_library_agents()

            self._loaded = True
            logger.info(f"SOTALibraryTier loaded: {len(self.agents)} agents from library")

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse SOTALibraryTier manifest: {e}")
            self._loaded = True
        except Exception as e:
            logger.error(f"Failed to load SOTALibraryTier: {e}")
            self._loaded = True

    def _load_library_agents(self) -> dict[str, dict[str, Any]]:
        """Load all agent definitions from library directories."""
        agents: dict[str, dict[str, Any]] = {}
        library_dir = self.path / "library"

        if not library_dir.exists():
            return agents

        # Walk through all source directories
        for source_dir in library_dir.iterdir():
            if not source_dir.is_dir():
                continue

            for file_path in source_dir.glob("*.yaml"):
                if file_path.name.startswith("."):
                    continue

                try:
                    with open(file_path, encoding="utf-8") as f:
                        agent_data = yaml.safe_load(f) or {}

                    agent_id = agent_data.get("id", file_path.stem)
                    agent_data["_source_path"] = str(file_path)
                    agent_data["_source_library"] = source_dir.name
                    agents[agent_id] = agent_data

                    logger.debug(f"Loaded SOTA agent: {agent_id} from {source_dir.name}")

                except Exception as e:
                    logger.error(f"Failed to load agent {file_path}: {e}")

        return agents

    def is_empty(self) -> bool:
        """Check if tier has any assets."""
        self._ensure_loaded()
        return not self.agents

    def is_enabled(self) -> bool:
        """Check if tier is enabled."""
        return self._enabled and self.path.exists()

    def match_agent(self, task: str) -> AgentSuggestion | None:
        """Find matching agent for a task description.

        Uses pattern matching similar to ObraTunedTier but with lower
        confidence threshold since SOTA patterns are fallbacks.

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

            # Combine confidences
            if patterns and keywords:
                base_confidence = (pattern_confidence * 0.6) + (keyword_confidence * 0.4)
            elif patterns:
                base_confidence = pattern_confidence
            elif keywords:
                base_confidence = keyword_confidence
            else:
                # No matching criteria - try name/description match
                name = agent.get("name", "").lower()
                desc = agent.get("protocol", {}).get("description", "").lower()

                name_words = set(name.split())
                desc_words = set(desc.split())
                task_words = set(task_lower.split())

                name_overlap = len(name_words & task_words) / max(len(name_words), 1)
                desc_overlap = len(desc_words & task_words) / max(len(desc_words), 1)

                base_confidence = max(name_overlap * 0.6, desc_overlap * 0.4)

            # Apply confidence boost
            total_confidence = min(base_confidence + confidence_boost, 1.0)

            if total_confidence > best_confidence:
                best_confidence = total_confidence
                source_lib = agent.get("_source_library", "unknown")
                best_match = AgentSuggestion(
                    agent=agent,
                    confidence=total_confidence,
                    command=agent.get("protocol", {}).get("invocation"),
                    reason=f"SOTA pattern from {source_lib}: {agent.get('name', agent_id)}",
                )

        return best_match

    def _compute_pattern_confidence(self, text: str, patterns: list[str]) -> float:
        """Compute confidence score based on pattern matches."""
        if not patterns:
            return 0.0

        match_count = 0
        for pattern in patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    match_count += 1
            except re.error:
                pass

        if match_count == 0:
            return 0.0

        base = 0.35  # Lower base than Obra tier
        match_ratio = match_count / len(patterns)
        return min(base + (match_ratio * 0.45), 0.8)

    def _compute_keyword_confidence(self, text: str, keywords: list[str]) -> float:
        """Compute confidence score based on keyword matches."""
        if not keywords:
            return 0.0

        match_count = sum(1 for kw in keywords if kw.lower() in text)

        if match_count == 0:
            return 0.0

        base = 0.3
        match_ratio = match_count / len(keywords)
        return min(base + (match_ratio * 0.4), 0.7)

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
        """Get applicable rules for a context (SOTA tier has no rules)."""
        return []

    def get_tool_guidance(self, tool: str) -> ToolGuidance | None:
        """Get guidance for a specific tool from SOTA patterns.

        Searches agent tool_guidance sections for the tool.
        """
        self._ensure_loaded()

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

    def list_sources(self) -> list[str]:
        """List available source libraries."""
        library_dir = self.path / "library"
        if not library_dir.exists():
            return []

        return [d.name for d in library_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

    def get_agents_by_source(self, source: str) -> list[dict[str, Any]]:
        """Get agents from a specific source library."""
        self._ensure_loaded()

        return [agent for agent in self.agents.values() if agent.get("_source_library") == source]

    def reload(self) -> None:
        """Force reload of tier assets."""
        self._loaded = False
        self.agents = {}
        self.rules = {}
        self.tools = {}
        self.patterns = {}
        self._ensure_loaded()
        logger.info(f"SOTALibraryTier reloaded: {len(self.agents)} agents")
