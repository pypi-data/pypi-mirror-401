"""CustomerTier - Tier 0 implementation for customer project modifications.

Part of EPIC-SOTA-001: Tiered Agent & Guidance Architecture.

This module provides:
- CustomerTier: Implementation of TierInterface for customer .obra/ directory
- customer_init(): Function to initialize .obra/ structure in a project

Example:
    >>> from obra.workflow.customer_tier import CustomerTier, customer_init
    >>> customer_init(Path('/path/to/project'))
    >>> tier = CustomerTier(Path('/path/to/project/.obra'))
"""

import logging
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from obra.schemas.closeout_schema import CloseoutTemplate
from obra.workflow.tiered_resolver import (
    AgentSuggestion,
    Rule,
    TierInterface,
    ToolGuidance,
    match_patterns,
)

logger = logging.getLogger(__name__)

# Current Obra version for compatibility check
OBRA_VERSION = "2.1.0"


class CustomerTier(TierInterface):
    """Tier 0: Customer modifications from project .obra/ directory.

    This tier has the highest priority and allows customers to:
    - Add custom agents, rules, tools, and patterns
    - Override or extend lower tier assets
    - Disable specific tiers or asset types

    The customer tier is empty by default (no .obra/ directory).
    Use customer_init() to create the structure.

    Attributes:
        path: Path to .obra/ directory
        manifest: Loaded manifest data
        override_mode: How to interact with lower tiers
    """

    name = "customer"
    confidence_threshold = 0.8  # High bar for customer agents

    def __init__(self, obra_path: Path):
        """Initialize CustomerTier.

        Args:
            obra_path: Path to .obra/ directory in customer project
        """
        self.path = Path(obra_path)
        self.manifest: dict[str, Any] = {}
        self.agents: dict[str, dict[str, Any]] = {}
        self.rules: dict[str, dict[str, Any]] = {}
        self.tools: dict[str, dict[str, Any]] = {}
        self.patterns: dict[str, dict[str, Any]] = {}
        self.closeout_template: CloseoutTemplate | None = None
        self._loaded = False
        self._override_mode = "extend"
        self._enabled_categories: dict[str, bool] = {
            "agents": True,
            "rules": True,
            "tools": True,
            "patterns": True,
            "closeout_template": True,
        }

        self._ensure_loaded()

    def _ensure_loaded(self) -> None:
        """Ensure tier assets are loaded if .obra/ exists."""
        if self._loaded:
            return

        if not self.path.exists():
            logger.debug(f"Customer tier not present: {self.path}")
            self._loaded = True
            return

        manifest_path = self.path / "manifest.yaml"
        if not manifest_path.exists():
            logger.debug(f"Customer manifest not found: {manifest_path}")
            self._loaded = True
            return

        try:
            with open(manifest_path, encoding="utf-8") as f:
                self.manifest = yaml.safe_load(f) or {}

            # Load settings
            self._override_mode = self.manifest.get("override_mode", "extend")
            self._enabled_categories = self.manifest.get(
                "enabled",
                {
                    "agents": True,
                    "rules": True,
                    "tools": True,
                    "patterns": True,
                    "closeout_template": True,
                },
            )
            self._enabled_categories.setdefault("closeout_template", True)

            # Update confidence threshold if specified
            settings = self.manifest.get("settings", {})
            if "confidence_threshold" in settings:
                self.confidence_threshold = settings["confidence_threshold"]

            # Load assets if enabled
            if self._enabled_categories.get("agents", True):
                self.agents = self._load_asset_type("agents")
            if self._enabled_categories.get("rules", True):
                self.rules = self._load_asset_type("rules")
            if self._enabled_categories.get("tools", True):
                self.tools = self._load_asset_type("tools")
            if self._enabled_categories.get("patterns", True):
                self.patterns = self._load_asset_type("patterns")
            if self._enabled_categories.get("closeout_template", True):
                self.closeout_template = self._load_closeout_template()

            self._loaded = True
            logger.info(
                f"CustomerTier loaded: {len(self.agents)} agents, "
                f"{len(self.rules)} rules, mode={self._override_mode}"
            )

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse customer manifest: {e}")
            self._loaded = True
        except Exception as e:
            logger.error(f"Failed to load customer tier: {e}")
            self._loaded = True

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
                asset_data["_source_tier"] = "customer"
                assets[asset_id] = asset_data

                logger.debug(f"Loaded customer {asset_type}: {asset_id}")

            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")

        return assets

    def _load_closeout_template(self) -> CloseoutTemplate | None:
        """Load customer-provided close-out template."""
        template_path = self.path / "templates" / "closeout.yaml"
        if not template_path.exists():
            return None

        try:
            with open(template_path, encoding="utf-8") as f:
                template_data = yaml.safe_load(f) or {}

            template = CloseoutTemplate(**template_data)
            logger.debug("Loaded customer close-out template from %s", template_path)
            return template
        except ValidationError as exc:
            logger.error("Invalid customer close-out template at %s: %s", template_path, exc)
        except Exception as exc:
            logger.error("Failed to load customer close-out template: %s", exc)

        return None

    def is_empty(self) -> bool:
        """Check if customer tier has any assets.

        Returns True if:
        - .obra/ directory doesn't exist
        - manifest.yaml doesn't exist
        - No enabled categories have any assets
        """
        if not self.path.exists():
            return True

        if not (self.path / "manifest.yaml").exists():
            return True

        self._ensure_loaded()

        # Check if any enabled category has content
        if self._enabled_categories.get("agents") and self.agents:
            return False
        if self._enabled_categories.get("rules") and self.rules:
            return False
        if self._enabled_categories.get("tools") and self.tools:
            return False
        if self._enabled_categories.get("patterns") and self.patterns:
            return False
        if self._enabled_categories.get("closeout_template", True) and self.closeout_template:
            return False

        return True

    def is_enabled(self) -> bool:
        """Check if tier is enabled.

        Disabled if:
        - .obra/ doesn't exist
        - override_mode is 'disable'
        """
        if not self.path.exists():
            return False

        if self.is_empty():
            return False

        return self._override_mode != "disable"

    def get_override_mode(self) -> str:
        """Get customer's override mode preference.

        Returns:
            'extend': Merge customer assets with lower tiers (default)
            'replace': Customer assets replace lower tier versions
            'disable': Skip this tier entirely
        """
        self._ensure_loaded()
        return self._override_mode

    def should_replace(self, asset_id: str) -> bool:
        """Check if asset should replace lower tier versions.

        Args:
            asset_id: Asset identifier

        Returns:
            True if:
            - Global override_mode is 'replace'
            - Asset has override: true flag
        """
        if self._override_mode == "replace":
            return True

        # Check per-asset override flag
        for assets in [self.agents, self.rules, self.tools, self.patterns]:
            if asset_id in assets:
                return assets[asset_id].get("override", False)

        return False

    def match_agent(self, task: str) -> AgentSuggestion | None:
        """Find matching customer agent for a task description."""
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

            # Check exclusions
            if exclude_patterns:
                excluded, _ = match_patterns(task_lower, exclude_patterns)
                if excluded:
                    continue

            # Calculate confidence
            matched, pattern_conf = (
                match_patterns(task_lower, patterns) if patterns else (False, 0.0)
            )
            keyword_conf = self._compute_keyword_confidence(task_lower, keywords)

            if patterns and keywords:
                base_confidence = (pattern_conf * 0.6) + (keyword_conf * 0.4)
            elif patterns:
                base_confidence = pattern_conf
            elif keywords:
                base_confidence = keyword_conf
            else:
                continue

            total_confidence = min(base_confidence + confidence_boost, 1.0)

            if total_confidence > best_confidence:
                best_confidence = total_confidence
                best_match = AgentSuggestion(
                    agent=agent,
                    confidence=total_confidence,
                    command=agent.get("protocol", {}).get("invocation"),
                    reason=f"Customer agent: {agent.get('name', agent_id)}",
                )

        return best_match

    def _compute_keyword_confidence(self, text: str, keywords: list[str]) -> float:
        """Compute confidence from keyword matches."""
        if not keywords:
            return 0.0

        match_count = sum(1 for kw in keywords if kw.lower() in text)
        if match_count == 0:
            return 0.0

        return min(0.4 + (match_count / len(keywords)) * 0.5, 0.9)

    def get_rules(self, context: str) -> list[Rule]:
        """Get applicable customer rules for a context."""
        self._ensure_loaded()

        rules = []
        for rule_id, rule_data in self.rules.items():
            conditions = rule_data.get("conditions", {})
            contexts = conditions.get("contexts", [])

            if not contexts or context in contexts:
                rules.append(
                    Rule(
                        id=rule_id,
                        name=rule_data.get("name", rule_id),
                        rule_type=rule_data.get("rule_type", "behavior"),
                        content=rule_data.get("content", {}),
                        source_tier=self.name,
                        priority=rule_data.get("priority", 60),  # Higher default for customer
                        override=rule_data.get("override", self._override_mode == "replace"),
                        enabled=rule_data.get("enabled", True),
                    )
                )

        return rules

    def get_tool_guidance(self, tool: str) -> ToolGuidance | None:
        """Get guidance for a specific tool from customer config."""
        self._ensure_loaded()

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

        return None

    def get_patterns(self, category: str | None = None) -> list[dict[str, Any]]:
        """Get workflow patterns, optionally filtered by category."""
        self._ensure_loaded()

        if category:
            return [p for p in self.patterns.values() if p.get("category") == category]
        return list(self.patterns.values())

    def get_closeout_template(self) -> CloseoutTemplate | None:
        """Get customer close-out template if available."""
        self._ensure_loaded()

        if not self._enabled_categories.get("closeout_template", True):
            return None

        return self.closeout_template

    def reload(self) -> None:
        """Force reload of tier assets."""
        self._loaded = False
        self.agents = {}
        self.rules = {}
        self.tools = {}
        self.patterns = {}
        self.closeout_template = None
        self._ensure_loaded()


def customer_init(project_path: Path, force: bool = False) -> Path:
    """Initialize .obra/ directory in a customer project.

    Creates the directory structure with a default manifest.

    Args:
        project_path: Path to customer project root
        force: If True, overwrite existing manifest

    Returns:
        Path to created .obra/ directory

    Raises:
        FileExistsError: If .obra/ exists and force=False

    Example:
        >>> obra_path = customer_init(Path('/path/to/project'))
        >>> print(f"Created {obra_path}")
    """
    project_path = Path(project_path)
    obra_path = project_path / ".obra"

    if obra_path.exists() and not force:
        manifest_path = obra_path / "manifest.yaml"
        if manifest_path.exists():
            raise FileExistsError(
                f".obra/ already exists at {obra_path}. Use force=True to overwrite."
            )

    # Create directory structure
    obra_path.mkdir(exist_ok=True)

    for subdir in ["agents", "rules", "tools", "patterns"]:
        subdir_path = obra_path / subdir
        subdir_path.mkdir(exist_ok=True)
        (subdir_path / ".gitkeep").touch()

    # Create default manifest
    manifest = {
        "version": "1.0.0",
        "obra_compatibility": f">={OBRA_VERSION}",
        "description": "Customer modifications for this project",
        "enabled": {
            "agents": True,
            "rules": True,
            "tools": True,
            "patterns": True,
        },
        "override_mode": "extend",
        "settings": {
            "confidence_threshold": 0.8,
            "auto_reload": True,
        },
    }

    manifest_path = obra_path / "manifest.yaml"
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)

    # Create example agent file (commented out)
    example_agent = """# Example Customer Agent
# Uncomment and customize to add your own agent

# id: "my_custom_agent"
# version: "1.0.0"
# name: "My Custom Agent"
# source: "customer"
#
# matching:
#   patterns:
#     - "my.?project|custom.?task"
#   keywords:
#     - "custom"
#   confidence_boost: 0.1
#
# protocol:
#   description: "Custom agent for project-specific tasks"
#   tools:
#     read_operations: ["read", "grep"]
#     write_operations: ["edit"]
#     execution_operations: ["bash"]
#   output_format: "mixed"
"""

    example_path = obra_path / "agents" / "_example_agent.yaml.disabled"
    with open(example_path, "w", encoding="utf-8") as f:
        f.write(example_agent)

    logger.info(f"Initialized customer .obra/ at {obra_path}")
    return obra_path
