"""Intent diff generation and rendering."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import yaml

from obra.intent.models import IntentModel

SECTION_FIELDS = (
    "assumptions",
    "requirements",
    "constraints",
    "acceptance_criteria",
    "non_goals",
    "risks",
)


def build_intent_diff(
    before: IntentModel,
    after: IntentModel,
    *,
    stage: str,
    rationale: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a structured diff between two intents."""
    metadata = metadata or {}
    diff: dict[str, Any] = {
        "intent_id": after.id,
        "created": datetime.now(UTC).isoformat(),
        "stage": stage,
        "added": {},
        "removed": {},
        "changed": {},
        "rationale": rationale or "",
        "metadata": metadata,
    }

    if before.problem_statement != after.problem_statement:
        diff["changed"]["problem_statement"] = {
            "from": before.problem_statement,
            "to": after.problem_statement,
        }

    for field in SECTION_FIELDS:
        before_list = getattr(before, field, [])
        after_list = getattr(after, field, [])
        added = [item for item in after_list if item not in before_list]
        removed = [item for item in before_list if item not in after_list]
        if added:
            diff["added"][field] = added
        if removed:
            diff["removed"][field] = removed

    return diff


def render_intent_diff(diff: dict[str, Any]) -> str:
    """Render intent diff to markdown with YAML frontmatter."""
    frontmatter = {
        "intent_id": diff.get("intent_id"),
        "created": diff.get("created"),
        "stage": diff.get("stage"),
        "added": diff.get("added", {}),
        "removed": diff.get("removed", {}),
        "changed": diff.get("changed", {}),
        "rationale": diff.get("rationale", ""),
        "metadata": diff.get("metadata", {}),
    }
    fm_content = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)
    return f"---\n{fm_content}---\n"
