"""Pydantic models for intent data structures.

This module defines the data models for intent capture and storage.
Intents represent normalized user objectives with structured fields
for problem statement, assumptions, requirements, and acceptance criteria.

Related:
    - docs/design/briefs/AUTO_INTENT_GENERATION_BRIEF.md
    - obra/schemas/plan_schema.py (similar Pydantic patterns)
"""

import re
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    pass

# Constants
SLUG_MAX_LENGTH = 50


class IntentStatus(str, Enum):
    """Status of an intent in the lifecycle."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    SUPERSEDED = "superseded"


class EnrichmentLevel(str, Enum):
    """Level of enrichment achieved during intent parsing.

    Indicates how successfully the LLM response was parsed:
    - FULL: Structured JSON parsed successfully (legacy Tier 3)
    - YAML: YAML frontmatter parsed successfully (Tier 1)
    - PROSE: Extracted from natural language response (Tier 4)
    - NONE: Fallback used, minimal enrichment (Tier 5)
    """

    FULL = "full"
    YAML = "yaml"
    PROSE = "prose"
    NONE = "none"


class InputType(str, Enum):
    """Classification of input source for intent generation."""

    VAGUE_NL = "vague_nl"  # Short, underspecified natural language
    RICH_NL = "rich_nl"  # Detailed natural language description
    PRD = "prd"  # Product requirements document
    PROSE_PLAN = "prose_plan"  # Unstructured plan document
    STRUCTURED_PLAN = "structured_plan"  # MACHINE_PLAN JSON/YAML format


class IntentModel(BaseModel):
    """Pydantic model for intent data.

    An intent captures the normalized user objective with explicit
    structure for problem statement, assumptions, requirements,
    acceptance criteria, and non-goals.

    Attributes:
        id: Unique identifier (format: {timestamp}-{slug})
        project: Project identifier (directory name or hash)
        slug: Human-readable slug derived from objective
        created: Creation timestamp (ISO-8601)
        status: Current status (active, archived, superseded)
        input_type: Classification of original input source
        problem_statement: Clear description of the problem to solve
        assumptions: List of assumptions made during intent generation
        requirements: List of functional requirements
        constraints: Explicit constraints that bound the solution
        acceptance_criteria: List of verifiable completion criteria
        non_goals: Explicit list of out-of-scope items
        risks: Key risks or pitfalls to monitor
        context_amendments: User-added context notes
        raw_objective: Original user input verbatim
        project_state: Project state classification (EMPTY/EXISTING) - optional
        project_state_method: Detection method used (deterministic/llm/forced) - optional
        project_state_rationale: Explanation of why this state was chosen - optional
        file_count: Number of meaningful files found during detection - optional
        metadata: Optional metadata for extensibility

    Example:
        >>> intent = IntentModel(
        ...     id="20260110T1200-add-auth",
        ...     project="my-app",
        ...     slug="add-auth",
        ...     created="2026-01-10T12:00:00Z",
        ...     status=IntentStatus.ACTIVE,
        ...     input_type=InputType.VAGUE_NL,
        ...     problem_statement="Add user authentication to the application",
        ...     assumptions=["JWT-based authentication preferred"],
        ...     requirements=["User can register", "User can login"],
        ...     acceptance_criteria=["Registration flow works", "Login flow works"],
        ...     non_goals=["Social login integration"],
        ...     raw_objective="add auth"
        ... )
    """

    id: str = Field(
        ...,
        description="Unique identifier in format {timestamp}-{slug}",
        examples=["20260110T1200-add-auth"],
    )
    project: str = Field(
        ...,
        description="Project identifier (directory name or hash)",
    )
    slug: str = Field(
        ...,
        description="Human-readable slug derived from objective",
        min_length=1,
        max_length=50,
    )
    created: str = Field(
        ...,
        description="Creation timestamp in ISO-8601 format",
    )
    status: IntentStatus = Field(
        default=IntentStatus.ACTIVE,
        description="Current intent status",
    )
    input_type: InputType = Field(
        ...,
        description="Classification of original input source",
    )
    problem_statement: str = Field(
        ...,
        description="Clear description of the problem to solve",
        min_length=1,
    )
    assumptions: list[str] = Field(
        default_factory=list,
        description="List of assumptions made during intent generation",
    )
    requirements: list[str] = Field(
        default_factory=list,
        description="List of functional requirements",
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="List of explicit constraints that bound the solution",
    )
    acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="List of verifiable completion criteria",
    )
    non_goals: list[str] = Field(
        default_factory=list,
        description="Explicit list of out-of-scope items",
    )
    risks: list[str] = Field(
        default_factory=list,
        description="List of key risks or pitfalls to monitor",
    )
    context_amendments: list[str] = Field(
        default_factory=list,
        description="User-added context notes via 'obra context add'",
    )
    raw_objective: str = Field(
        ...,
        description="Original user input verbatim",
    )
    project_state: str | None = Field(
        default=None,
        description="Project state classification (EMPTY/EXISTING) - optional",
    )
    project_state_method: str | None = Field(
        default=None,
        description="Detection method used (deterministic_fast_path/llm_classification/forced_override/error_fallback) - optional",
    )
    project_state_rationale: str | None = Field(
        default=None,
        description="Explanation of why this state was chosen - optional",
    )
    file_count: int | None = Field(
        default=None,
        description="Number of meaningful files found during detection - optional",
    )
    enrichment_level: EnrichmentLevel | None = Field(
        default=None,
        description="Level of enrichment achieved during parsing (full/prose/none) - optional",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata for extensibility",
    )

    model_config = {"extra": "forbid"}

    @classmethod
    def generate_id(cls, slug: str, timestamp: datetime | None = None) -> str:
        """Generate a unique intent ID from slug and timestamp.

        Args:
            slug: Human-readable slug
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Intent ID in format {timestamp}-{slug}

        Example:
            >>> IntentModel.generate_id("add-auth")
            '20260110T1200-add-auth'
        """
        ts = timestamp or datetime.now(UTC)
        ts_str = ts.strftime("%Y%m%dT%H%M")
        return f"{ts_str}-{slug}"

    @classmethod
    def slugify(cls, text: str) -> str:
        """Convert text to a URL-safe slug.

        Args:
            text: Text to slugify

        Returns:
            Lowercase slug with hyphens, max 50 chars

        Example:
            >>> IntentModel.slugify("Add User Authentication")
            'add-user-authentication'
        """
        # Lowercase and replace non-alphanumeric with hyphens
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
        # Remove leading/trailing hyphens
        slug = slug.strip("-")
        # Truncate to max length
        if len(slug) > SLUG_MAX_LENGTH:
            slug = slug[:SLUG_MAX_LENGTH].rstrip("-")
        return slug or "intent"


# Convenience exports
__all__ = [
    "EnrichmentLevel",
    "InputType",
    "IntentModel",
    "IntentStatus",
]
