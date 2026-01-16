"""Analogue cache helpers for scaffolded planning."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_analogue_cache_entries(
    *,
    global_path: Path | None,
    project_path: Path | None,
) -> list[dict[str, Any]]:
    """Load analogue cache entries from global/project paths."""
    entries: list[dict[str, Any]] = []
    if global_path:
        entries.extend(_load_cache_file(global_path))
    if project_path:
        entries.extend(_load_cache_file(project_path))
    return _dedupe_entries(entries)


def append_analogue_cache_entry(
    entry: dict[str, Any],
    *,
    global_path: Path | None,
    project_path: Path | None,
) -> None:
    """Append a cache entry to global and project caches if configured."""
    if global_path:
        _append_entry(global_path, entry)
    if project_path:
        _append_entry(project_path, entry)


def render_analogue_cache(entries: list[dict[str, Any]]) -> str:
    """Render analogue cache entries for prompt inclusion."""
    if not entries:
        return ""
    lines: list[str] = []
    for entry in entries:
        domains = entry.get("domains") or []
        roles = entry.get("expert_roles") or []
        objective = entry.get("objective_preview")
        if domains:
            domain_label = ", ".join(str(domain) for domain in domains)
            if roles:
                role_label = ", ".join(str(role) for role in roles)
                lines.append(f"- Domain: {domain_label} (roles: {role_label})")
            else:
                lines.append(f"- Domain: {domain_label}")
        if objective:
            lines.append(f"  Objective: {objective}")
        for approach in entry.get("expert_approach") or []:
            lines.append(f"  Approach: {approach}")
        for gap in entry.get("intent_gaps") or []:
            lines.append(f"  Gap: {gap}")
        rationale = entry.get("rationale")
        if rationale:
            lines.append(f"  Rationale: {rationale}")
    return "\n".join(lines)


def _load_cache_file(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
    except (OSError, yaml.YAMLError):
        return []
    if isinstance(data, list):
        return [entry for entry in data if isinstance(entry, dict)]
    if isinstance(data, dict):
        entries = data.get("entries", [])
        if isinstance(entries, list):
            return [entry for entry in entries if isinstance(entry, dict)]
    return []


def _append_entry(path: Path, entry: dict[str, Any]) -> None:
    entries = _load_cache_file(path)
    entries.append(entry)
    entries = _dedupe_entries(entries)
    payload = {"entries": entries}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, default_flow_style=False, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def _dedupe_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for entry in entries:
        key = json.dumps(entry, sort_keys=True, default=str)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(entry)
    return deduped
