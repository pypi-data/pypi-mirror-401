"""Utility functions for the Configuration Explorer.

Provides functions for converting raw config dictionaries into ConfigTree
structures and other helper utilities.
"""

from __future__ import annotations

import logging
from copy import deepcopy
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

from .descriptions import get_choices, get_default, get_description, get_tier, is_locked
from .models import ConfigNode, ConfigSource, ConfigTree, SettingTier, ValueType

logger = logging.getLogger(__name__)

# Fields that should never appear in the explorer (security-sensitive)
HIDDEN_FIELDS = {
    "auth_token",
    "refresh_token",
    "firebase_api_key",
    "token_expires_at",
}

# Fields that should be displayed but not editable
READONLY_FIELDS = {
    "user_email",
    "firebase_uid",
    "auth_provider",
    "display_name",
    "user_id",
    "auth_timestamp",  # Set by auth system, not user-editable
    "terms_accepted",  # Set by acceptance flow, not user-editable
}

# Account/auth fields that should be grouped together in a dedicated section
ACCOUNT_INFO_FIELDS = {
    "auth_provider",
    "auth_timestamp",
    "display_name",
    "firebase_uid",
    "user_email",
    "user_id",
    "terms_accepted",
}

# Field ordering priority within the same tier (lower = earlier)
# Used to ensure parent fields appear before dependent fields
FIELD_ORDER_PRIORITY = {
    # Top-level section ordering
    "llm": 0,  # LLM settings at top (most important)
    "features": 10,  # Features second
    "orchestration": 20,  # Orchestration settings
    # LLM field ordering (within llm section)
    "provider": 0,  # Provider must come before model (parent → child)
    "model": 1,
    "auth_method": 2,
    # Git settings (after auth, before tiers - provider-aware)
    "git": 3,
    "skip_check": 4,
    "auto_init": 5,
    # Tier ordering (fast → medium → high)
    "fast": 6,
    "medium": 7,
    "high": 8,
}


def merge_with_default_schema(local_config: dict[str, Any]) -> dict[str, Any]:
    """Merge local config with default schema for UI display."""
    defaults = load_default_config_schema()
    if not defaults:
        return deepcopy(local_config)
    return _deep_merge(defaults, local_config)


def load_default_config_schema() -> dict[str, Any]:
    try:
        default_path = resources.files("obra.config").joinpath("default_config.yaml")
        content = default_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
        if isinstance(data, dict):
            return data
    except Exception as exc:
        logger.debug("Failed to load packaged default_config.yaml: %s", exc)

    fallback = Path(__file__).resolve().parents[1] / "default_config.yaml"
    try:
        if fallback.exists():
            content = fallback.read_text(encoding="utf-8")
            data = yaml.safe_load(content) or {}
            if isinstance(data, dict):
                return data
    except Exception as exc:
        logger.debug("Failed to load fallback default_config.yaml: %s", exc)

    logger.warning("Default config schema unavailable; config UI may be incomplete.")
    return {}


def iter_schema_paths(
    schema: dict[str, Any],
    prefix: str = "",
) -> list[tuple[str, Any]]:
    """Return dot-paths and values from the config schema."""
    items: list[tuple[str, Any]] = []
    for key, value in schema.items():
        path = f"{prefix}.{key}" if prefix else key
        items.append((path, value))
        if isinstance(value, dict):
            items.extend(iter_schema_paths(value, path))
    return items


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def detect_value_type(value: Any, path: str) -> ValueType:
    """Detect the ValueType for a configuration value.

    Args:
        value: The value to inspect
        path: The dot-notation path (used to check for known enum types)

    Returns:
        The detected ValueType
    """
    # Check if this path has predefined choices (enum)
    if get_choices(path) is not None:
        return ValueType.ENUM

    if isinstance(value, bool):
        return ValueType.BOOLEAN
    if isinstance(value, int):
        return ValueType.INTEGER
    if isinstance(value, str):
        return ValueType.STRING
    if isinstance(value, dict):
        return ValueType.OBJECT

    # Default to string for unknown types
    return ValueType.STRING


def get_setting_tier(path: str) -> SettingTier:
    """Get the SettingTier for a configuration path.

    Args:
        path: Dot-notation path

    Returns:
        The SettingTier for this setting
    """
    tier_str = get_tier(path)
    return SettingTier(tier_str)


def dict_to_config_node(
    data: dict[str, Any],
    source: ConfigSource,
    parent_path: str = "",
) -> ConfigNode:
    """Convert a dictionary into a ConfigNode tree.

    Recursively builds a ConfigNode tree from a nested dictionary,
    attaching descriptions, choices, and defaults from the registry.

    Args:
        data: Dictionary of configuration values
        source: ConfigSource indicating where this config comes from
        parent_path: Parent path for building full dot-notation paths

    Returns:
        Root ConfigNode containing the tree structure
    """
    # Create root node for this level
    key = parent_path.split(".")[-1] if parent_path else "root"
    root = ConfigNode(
        key=key,
        path=parent_path,
        value=None,
        value_type=ValueType.OBJECT,
        source=source,
        tier=get_setting_tier(parent_path) if parent_path else SettingTier.STANDARD,
        description=get_description(parent_path) if parent_path else None,
    )

    for k, v in data.items():
        # Skip sensitive fields that shouldn't be visible
        if k in HIDDEN_FIELDS:
            continue

        child_path = f"{parent_path}.{k}" if parent_path else k

        if isinstance(v, dict):
            # Recursive case - nested object
            child = dict_to_config_node(v, source, child_path)
            child.key = k
        else:
            # Leaf case - actual value
            value_type = detect_value_type(v, child_path)
            child = ConfigNode(
                key=k,
                path=child_path,
                value=v,
                value_type=value_type,
                source=source,
                tier=get_setting_tier(child_path),
                description=get_description(child_path),
                default_value=get_default(child_path),
                choices=get_choices(child_path),
                is_readonly=is_locked(child_path) or k in READONLY_FIELDS,
            )

        root.children.append(child)

    # Sort children: basic first, then standard, then advanced
    # Within same tier, sort by field priority (provider before model), then alphabetically
    tier_order = {SettingTier.BASIC: 0, SettingTier.STANDARD: 1, SettingTier.ADVANCED: 2}
    root.children.sort(
        key=lambda n: (
            tier_order.get(n.tier, 1),
            FIELD_ORDER_PRIORITY.get(n.key, 999),  # Fields with priority come first
            n.key,  # Alphabetical within same tier/priority
        )
    )

    return root


def _extract_account_nodes(node: ConfigNode) -> list[ConfigNode]:
    """Extract account/auth info nodes from tree for dedicated section.

    Args:
        node: ConfigNode to search

    Returns:
        List of account info nodes (auth_provider, user_email, etc.)
    """
    account_nodes: list[ConfigNode] = []
    children_to_keep = []

    for child in node.children:
        # Check if this is an account info field (top-level only)
        if child.key in ACCOUNT_INFO_FIELDS:
            # Mark as read-only if in READONLY_FIELDS
            if is_locked(child.path) or child.key in READONLY_FIELDS:
                child.is_readonly = True
            account_nodes.append(child)
        else:
            children_to_keep.append(child)

    node.children = children_to_keep
    return account_nodes


def _extract_advanced_nodes(node: ConfigNode, parent_context: str = "") -> list[ConfigNode]:
    """Recursively extract all advanced-tier nodes from a tree.

    Args:
        node: ConfigNode to search
        parent_context: Parent path context for better naming (e.g., "telemetry" for "enabled")

    Returns:
        List of advanced-tier nodes (both leaf and branch) with improved display names
    """
    advanced_nodes: list[ConfigNode] = []

    # Extract advanced children, keeping track of which to keep
    children_to_keep = []

    for child in node.children:
        if child.tier == SettingTier.ADVANCED:
            # This is an advanced node - extract it
            # Improve display name if we have parent context
            if parent_context and child.is_leaf:
                # e.g., "enabled" becomes "telemetry.enabled"
                child.key = f"{parent_context}.{child.key}"
            advanced_nodes.append(child)
        elif not child.is_leaf:
            # This is a non-advanced branch - recursively search it
            # Build context from parent path (skip generic names like "features")
            new_context = child.key if child.key not in {"features", "advanced"} else parent_context
            if parent_context and new_context and new_context != parent_context:
                new_context = f"{parent_context}.{new_context}"

            child_advanced = _extract_advanced_nodes(child, new_context)
            advanced_nodes.extend(child_advanced)

            # Only keep this branch if it still has children after extraction
            # This removes empty parent nodes like "advanced" after all children extracted
            if len(child.children) > 0:
                children_to_keep.append(child)
        else:
            # This is a non-advanced leaf - keep it
            children_to_keep.append(child)

    # Update node's children to exclude extracted advanced nodes and empty branches
    node.children = children_to_keep

    return advanced_nodes


def dict_to_config_tree(
    local_config: dict[str, Any],
    server_config: dict[str, Any],
) -> ConfigTree:
    """Convert local and server config dicts into a ConfigTree.

    Consolidates advanced-tier settings and account info into dedicated sections
    for better UX organization.

    Args:
        local_config: Local configuration dictionary from ~/.obra/client-config.yaml
        server_config: Server configuration dictionary from API

    Returns:
        ConfigTree with both local and server roots populated
    """
    # Handle server config structure (may have resolved/overrides/preset keys)
    server_data = server_config.get("resolved", server_config)

    local_root = dict_to_config_node(local_config, ConfigSource.LOCAL, "")
    local_root.key = "Local Settings"

    # Extract account/auth info nodes and create dedicated section
    account_nodes = _extract_account_nodes(local_root)

    if account_nodes:
        # Create "Account Info" section
        account_section = ConfigNode(
            key="📋 Account Info - Read Only",
            path="account_info",
            value=None,
            value_type=ValueType.OBJECT,
            source=ConfigSource.LOCAL,
            tier=SettingTier.STANDARD,
            description="Account and authentication information (read-only)",
        )

        # Sort account nodes alphabetically
        account_nodes.sort(key=lambda n: n.key)

        # Add account nodes as children
        account_section.children = account_nodes

        # Add Account section to local_root (will be before Advanced)
        local_root.children.append(account_section)

    # Extract all advanced-tier nodes and consolidate under "Advanced" section
    advanced_nodes = _extract_advanced_nodes(local_root)

    if advanced_nodes:
        # Create "Advanced" parent node
        advanced_section = ConfigNode(
            key="⚙️ Advanced",
            path="advanced",
            value=None,
            value_type=ValueType.OBJECT,
            source=ConfigSource.LOCAL,
            tier=SettingTier.ADVANCED,
            description="Advanced configuration settings for expert users",
        )

        # Sort advanced nodes alphabetically
        advanced_nodes.sort(key=lambda n: n.key)

        # Add advanced nodes as children
        advanced_section.children = advanced_nodes

        # Add Advanced section to local_root at the end
        local_root.children.append(advanced_section)

    server_root = dict_to_config_node(server_data, ConfigSource.SERVER, "")
    server_root.key = "📋 Server Info (SaaS) - Read Only"

    return ConfigTree(local_root=local_root, server_root=server_root)


def flatten_config(node: ConfigNode, prefix: str = "") -> dict[str, Any]:
    """Flatten a ConfigNode tree into a dot-notation dictionary.

    Args:
        node: ConfigNode to flatten
        prefix: Current path prefix

    Returns:
        Dictionary mapping dot-notation paths to values
    """
    result: dict[str, Any] = {}

    for child in node.children:
        path = f"{prefix}.{child.key}" if prefix else child.key

        if child.is_leaf:
            result[path] = child.value
        else:
            result.update(flatten_config(child, path))

    return result


def unflatten_config(flat_config: dict[str, Any]) -> dict[str, Any]:
    """Convert a flat dot-notation dict back to nested structure.

    Args:
        flat_config: Dictionary with dot-notation keys

    Returns:
        Nested dictionary structure
    """
    result: dict[str, Any] = {}

    for path, value in flat_config.items():
        parts = path.split(".")
        current = result

        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        current[parts[-1]] = value

    return result


def get_preset_name(server_config: dict[str, Any]) -> str | None:
    """Extract preset name from server config.

    Args:
        server_config: Server configuration dictionary

    Returns:
        Preset name or None
    """
    return server_config.get("preset")


def count_children(node: ConfigNode, include_nested: bool = True) -> int:
    """Count child nodes in a config tree.

    Args:
        node: ConfigNode to count children of
        include_nested: If True, count recursively; if False, count direct children only

    Returns:
        Number of child nodes
    """
    if not include_nested:
        return len(node.children)

    count = 0
    for child in node.children:
        if child.is_leaf:
            count += 1
        else:
            count += count_children(child, include_nested=True)

    return count


def find_nodes_by_path_pattern(
    root: ConfigNode,
    pattern: str,
) -> list[ConfigNode]:
    """Find all nodes whose paths match a pattern.

    Args:
        root: Root node to search from
        pattern: Pattern to match (case-insensitive substring)

    Returns:
        List of matching ConfigNodes
    """
    matches: list[ConfigNode] = []
    pattern_lower = pattern.lower()

    def search(node: ConfigNode) -> None:
        if pattern_lower in node.path.lower() or pattern_lower in node.key.lower():
            matches.append(node)

        for child in node.children:
            search(child)

    search(root)
    return matches
