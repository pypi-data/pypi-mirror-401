"""Prompt builders for scaffolded intent enrichment stages."""

from __future__ import annotations

from typing import Iterable


def build_assumptions_prompt(
    objective: str,
    intent_markdown: str,
    non_inferable_categories: Iterable[str],
) -> str:
    categories = ", ".join(non_inferable_categories)
    return f"""You are refining a user intent before planning.

Objective:
"{objective}"

Current intent:
{intent_markdown}

Task:
1) Identify missing context or assumptions required to plan successfully.
2) Generate explicit questions ONLY for non-inferable gaps.
3) Keep answers intent-level (requirements/constraints), not implementation details.

Non-inferable categories:
- {categories}

Lean guidance:
- Focus on minimum viable scope.
- Do not add speculative features or future-proofing.

Output format (YAML frontmatter only, no prose):
---
assumptions_add:
  - "Assumption to add"
questions:
  - "General clarification question"
non_inferable_questions:
  - "Question that must be answered by the user"
rationale: "Short rationale"
---
"""


def build_expert_alignment_prompt(
    objective: str,
    intent_markdown: str,
    analogue_cache: str | None = None,
) -> str:
    cache_section = ""
    if analogue_cache:
        cache_section = f"\nAnalogue cache (use only if relevant):\n{analogue_cache}\n"

    return f"""You are performing expert-aligned intent enrichment.

Objective:
"{objective}"

Current intent:
{intent_markdown}
{cache_section}

Task:
1) Infer domain(s) and expert roles (include top 2 if ambiguous).
2) Describe how experts in those domains approach similar problems.
3) Compare current intent to expert approach and identify gaps.
4) Propose intent-level updates only (requirements, constraints, non-goals, risks, acceptance criteria, assumptions).

Lean expert guidance:
- Focus on minimum viable steps.
- Do NOT add speculative features, future-proofing, or extra abstractions.
- Prefer reversible, incremental scope.
- Flag scope creep explicitly.

Output format (YAML frontmatter only, no prose):
---
domain_inference:
  - domain: "example"
    confidence: 0.72
    expert_roles:
      - "Expert role"
expert_approach:
  - "Approach bullet"
intent_gaps:
  - "Gap bullet"
proposed_intent_updates:
  assumptions_add:
    - "Assumption"
  requirements_add:
    - "Requirement"
  constraints_add:
    - "Constraint"
  non_goals_add:
    - "Non-goal"
  risks_add:
    - "Risk"
  acceptance_criteria_add:
    - "Acceptance criterion"
rationale: "Short rationale"
---
"""


def build_brief_prompt(objective: str, intent_markdown: str) -> str:
    return f"""You are consolidating an updated intent after expert alignment.

Objective:
"{objective}"

Current intent:
{intent_markdown}

Task:
- Produce a cleaned, consolidated intent with the same sections.
- Keep it lean and scoped to the objective.
- Do NOT add speculative features or implementation details.

Output format (YAML frontmatter only, no prose):
---
problem_statement: "..."
assumptions:
  - "..."
requirements:
  - "..."
constraints:
  - "..."
acceptance_criteria:
  - "..."
non_goals:
  - "..."
risks:
  - "..."
---
"""


def build_review_prompt(
    objective: str,
    intent_markdown: str,
    plan_items_json: str,
) -> str:
    return f"""You are reviewing a derived plan against expert approaches.

Objective:
"{objective}"

Intent:
{intent_markdown}

Plan items (JSON):
{plan_items_json}

Task:
1) Compare the plan against how experts solve similar problems.
2) Flag over-engineering, unnecessary features, or scope drift.
3) If changes are needed, return a refined plan (same JSON structure).

Lean expert guidance:
- Focus on minimum viable scope.
- Do NOT add speculative features or extra abstractions.
- Prefer reversible, incremental changes.

Output format (JSON only):
{{
  "changes_required": true|false,
  "issues": ["..."],
  "plan_items": [{{...}}]
}}
"""
