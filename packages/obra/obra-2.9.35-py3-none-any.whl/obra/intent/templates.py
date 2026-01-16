"""Intent template rendering for markdown output.

This module provides template rendering for intent files,
converting IntentModel data to markdown with YAML frontmatter.

Related:
    - docs/design/briefs/AUTO_INTENT_GENERATION_BRIEF.md
    - obra/intent/models.py
    - obra/intent/storage.py
"""

from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from obra.intent.models import IntentModel

# Constants
SUMMARY_PREVIEW_LENGTH = 60


def render_intent_template(intent: "IntentModel") -> str:
    """Render an IntentModel to markdown with YAML frontmatter.

    Routes to appropriate template renderer based on project_state:
    - EMPTY: Uses render_intent_template_empty (with Foundation Proposals)
    - EXISTING: Uses render_intent_template_existing (with Questions for Derivation)
    - None: Falls back to basic template (backward compatible)

    Args:
        intent: IntentModel to render

    Returns:
        Markdown content string

    Example:
        >>> content = render_intent_template(intent)
        >>> print(content[:50])
        ---
        id: 20260110T1200-add-auth
        ...
    """
    # Route to appropriate template based on project_state
    if intent.project_state == "EMPTY":
        return render_intent_template_empty(intent)
    if intent.project_state == "EXISTING":
        return render_intent_template_existing(intent)

    # Fallback to basic template for backward compatibility (no project_state)
    return _render_basic_template(intent)


def _render_basic_template(intent: "IntentModel") -> str:
    """Render basic template without project state-specific sections.

    Used for backward compatibility with intents created before FEAT-AUTO-INTENT-002.

    Args:
        intent: IntentModel to render

    Returns:
        Markdown content string
    """
    # Build frontmatter (includes project state metadata if present)
    frontmatter = _build_frontmatter(intent)

    # Render frontmatter
    fm_content = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)

    # Build body sections
    sections: list[str] = []

    # Problem Statement
    sections.append(f"## Problem Statement\n\n{intent.problem_statement}")

    # Assumptions
    if intent.assumptions:
        items = "\n".join(f"- {a}" for a in intent.assumptions)
        sections.append(f"## Assumptions\n\n{items}")
    else:
        sections.append("## Assumptions\n\n_No assumptions documented._")

    # Requirements
    if intent.requirements:
        items = "\n".join(f"- {r}" for r in intent.requirements)
        sections.append(f"## Requirements\n\n{items}")
    else:
        sections.append("## Requirements\n\n_No requirements documented._")

    # Constraints
    if intent.constraints:
        items = "\n".join(f"- {c}" for c in intent.constraints)
        sections.append(f"## Constraints\n\n{items}")
    else:
        sections.append("## Constraints\n\n_No constraints documented._")

    # Acceptance Criteria
    if intent.acceptance_criteria:
        items = "\n".join(f"- {c}" for c in intent.acceptance_criteria)
        sections.append(f"## Acceptance Criteria\n\n{items}")
    else:
        sections.append("## Acceptance Criteria\n\n_No acceptance criteria documented._")

    # Non-Goals
    if intent.non_goals:
        items = "\n".join(f"- {g}" for g in intent.non_goals)
        sections.append(f"## Non-Goals\n\n{items}")
    else:
        sections.append("## Non-Goals\n\n_No non-goals documented._")

    # Risks
    if intent.risks:
        items = "\n".join(f"- {r}" for r in intent.risks)
        sections.append(f"## Risks\n\n{items}")
    else:
        sections.append("## Risks\n\n_No risks documented._")

    # Context Amendments
    if intent.context_amendments:
        items = "\n".join(f"- {a}" for a in intent.context_amendments)
        sections.append(f"## Context Amendments\n\n{items}")

    body = "\n\n".join(sections)

    return f"---\n{fm_content}---\n\n{body}\n"


def render_intent_summary(intent: "IntentModel") -> str:
    """Render a brief summary of an intent for display.

    Args:
        intent: IntentModel to summarize

    Returns:
        Short summary string

    Example:
        >>> summary = render_intent_summary(intent)
        >>> print(summary)
        add-auth (active) - Add user authentication
    """
    status_str = intent.status.value
    problem_preview = intent.problem_statement[:SUMMARY_PREVIEW_LENGTH]
    if len(intent.problem_statement) > SUMMARY_PREVIEW_LENGTH:
        problem_preview += "..."

    return f"{intent.slug} ({status_str}) - {problem_preview}"


def render_intent_template_empty(intent: "IntentModel") -> str:
    """Render an IntentModel for an EMPTY project with Foundation Proposals.

    This template includes a "Foundation Proposals" section for new/minimal
    projects that need technology recommendations.

    Args:
        intent: IntentModel to render

    Returns:
        Markdown content string

    Example:
        >>> content = render_intent_template_empty(intent)
        >>> "Foundation Proposals" in content
        True
    """
    # Build frontmatter with project state metadata
    frontmatter = _build_frontmatter(intent)

    # Render frontmatter
    fm_content = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)

    # Build body sections
    sections: list[str] = []

    # Problem Statement
    sections.append(f"## Problem Statement\n\n{intent.problem_statement}")

    # Assumptions
    if intent.assumptions:
        items = "\n".join(f"- {a}" for a in intent.assumptions)
        sections.append(f"## Assumptions\n\n{items}")
    else:
        sections.append("## Assumptions\n\n_No assumptions documented._")

    # Requirements
    if intent.requirements:
        items = "\n".join(f"- {r}" for r in intent.requirements)
        sections.append(f"## Requirements\n\n{items}")
    else:
        sections.append("## Requirements\n\n_No requirements documented._")

    # Constraints
    if intent.constraints:
        items = "\n".join(f"- {c}" for c in intent.constraints)
        sections.append(f"## Constraints\n\n{items}")
    else:
        sections.append("## Constraints\n\n_No constraints documented._")

    # Acceptance Criteria
    if intent.acceptance_criteria:
        items = "\n".join(f"- {c}" for c in intent.acceptance_criteria)
        sections.append(f"## Acceptance Criteria\n\n{items}")
    else:
        sections.append("## Acceptance Criteria\n\n_No acceptance criteria documented._")

    # Non-Goals
    if intent.non_goals:
        items = "\n".join(f"- {g}" for g in intent.non_goals)
        sections.append(f"## Non-Goals\n\n{items}")
    else:
        sections.append("## Non-Goals\n\n_No non-goals documented._")

    # Risks
    if intent.risks:
        items = "\n".join(f"- {r}" for r in intent.risks)
        sections.append(f"## Risks\n\n{items}")
    else:
        sections.append("## Risks\n\n_No risks documented._")

    # Foundation Proposals (EMPTY project specific)
    foundation_proposals = intent.metadata.get("foundation_proposals", [])
    if foundation_proposals:
        items = "\n".join(f"- {p}" for p in foundation_proposals)
        sections.append(f"## Foundation Proposals\n\n{items}")
    else:
        sections.append("## Foundation Proposals\n\n_No technology proposals documented._")

    # Context Amendments
    if intent.context_amendments:
        items = "\n".join(f"- {a}" for a in intent.context_amendments)
        sections.append(f"## Context Amendments\n\n{items}")

    body = "\n\n".join(sections)

    return f"---\n{fm_content}---\n\n{body}\n"


def render_intent_template_existing(intent: "IntentModel") -> str:
    """Render an IntentModel for an EXISTING project with Questions for Derivation.

    This template includes a "Questions for Derivation" section for established
    codebases that need investigation questions.

    Args:
        intent: IntentModel to render

    Returns:
        Markdown content string

    Example:
        >>> content = render_intent_template_existing(intent)
        >>> "Questions for Derivation" in content
        True
    """
    # Build frontmatter with project state metadata
    frontmatter = _build_frontmatter(intent)

    # Render frontmatter
    fm_content = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)

    # Build body sections
    sections: list[str] = []

    # Problem Statement
    sections.append(f"## Problem Statement\n\n{intent.problem_statement}")

    # Assumptions
    if intent.assumptions:
        items = "\n".join(f"- {a}" for a in intent.assumptions)
        sections.append(f"## Assumptions\n\n{items}")
    else:
        sections.append("## Assumptions\n\n_No assumptions documented._")

    # Requirements
    if intent.requirements:
        items = "\n".join(f"- {r}" for r in intent.requirements)
        sections.append(f"## Requirements\n\n{items}")
    else:
        sections.append("## Requirements\n\n_No requirements documented._")

    # Constraints
    if intent.constraints:
        items = "\n".join(f"- {c}" for c in intent.constraints)
        sections.append(f"## Constraints\n\n{items}")
    else:
        sections.append("## Constraints\n\n_No constraints documented._")

    # Acceptance Criteria
    if intent.acceptance_criteria:
        items = "\n".join(f"- {c}" for c in intent.acceptance_criteria)
        sections.append(f"## Acceptance Criteria\n\n{items}")
    else:
        sections.append("## Acceptance Criteria\n\n_No acceptance criteria documented._")

    # Non-Goals
    if intent.non_goals:
        items = "\n".join(f"- {g}" for g in intent.non_goals)
        sections.append(f"## Non-Goals\n\n{items}")
    else:
        sections.append("## Non-Goals\n\n_No non-goals documented._")

    # Risks
    if intent.risks:
        items = "\n".join(f"- {r}" for r in intent.risks)
        sections.append(f"## Risks\n\n{items}")
    else:
        sections.append("## Risks\n\n_No risks documented._")

    # Questions for Derivation (EXISTING project specific)
    derivation_questions = intent.metadata.get("derivation_questions", [])
    if derivation_questions:
        items = "\n".join(f"- {q}" for q in derivation_questions)
        sections.append(f"## Questions for Derivation\n\n{items}")
    else:
        sections.append("## Questions for Derivation\n\n_No investigation questions documented._")

    # Context Amendments
    if intent.context_amendments:
        items = "\n".join(f"- {a}" for a in intent.context_amendments)
        sections.append(f"## Context Amendments\n\n{items}")

    body = "\n\n".join(sections)

    return f"---\n{fm_content}---\n\n{body}\n"


def _build_frontmatter(intent: "IntentModel") -> dict:
    """Build YAML frontmatter with project state metadata.

    Args:
        intent: IntentModel to extract metadata from

    Returns:
        Dictionary for YAML frontmatter
    """
    frontmatter = {
        "id": intent.id,
        "slug": intent.slug,
        "project": intent.project,
        "created": intent.created,
        "status": intent.status.value,
        "input_type": intent.input_type.value,
        "raw_objective": intent.raw_objective,
    }

    # Add project state metadata if present
    if intent.project_state is not None:
        frontmatter["project_state"] = intent.project_state
    if intent.project_state_method is not None:
        frontmatter["project_state_method"] = intent.project_state_method
    if intent.project_state_rationale is not None:
        frontmatter["project_state_rationale"] = intent.project_state_rationale
    if intent.file_count is not None:
        frontmatter["file_count"] = intent.file_count

    if intent.metadata:
        frontmatter["metadata"] = intent.metadata

    return frontmatter


# Convenience exports
__all__ = [
    "render_intent_summary",
    "render_intent_template",
    "render_intent_template_empty",
    "render_intent_template_existing",
]
