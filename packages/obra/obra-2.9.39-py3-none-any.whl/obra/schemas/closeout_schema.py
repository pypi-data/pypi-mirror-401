"""Pydantic schema for close-out templates.

Close-out templates define quality gate tasks that should be appended
to derived plans. Templates can be provided by customers, Obra domain
defaults, or baseline fallbacks.
"""

from pydantic import BaseModel, Field, model_validator


class CloseoutTask(BaseModel):
    """Schema for an individual close-out task."""

    id: str = Field(
        ...,
        min_length=1,
        description="Task identifier (e.g., CO.T0, SN.T1)",
    )
    desc: str = Field(
        ...,
        min_length=1,
        description="Task description",
    )
    verify: str = Field(
        ...,
        min_length=1,
        description="Verification criteria for task completion",
    )
    conditional: str | None = Field(
        default=None,
        description="Optional condition name used to include/exclude the task",
    )

    model_config = {"extra": "forbid"}


class CloseoutTemplate(BaseModel):
    """Schema for a close-out template."""

    domain: str = Field(
        ...,
        min_length=1,
        description="Domain key for template selection (e.g., software-dev)",
    )
    tasks: list[CloseoutTask] = Field(
        ...,
        min_length=1,
        description="Ordered list of close-out tasks",
    )
    notes: str | None = Field(
        default=None,
        description="Optional notes about template origin or usage",
    )

    @model_validator(mode="after")
    def validate_task_ids_unique(self) -> "CloseoutTemplate":
        """Ensure close-out task IDs are unique within the template."""
        seen_ids: set[str] = set()
        for task in self.tasks:
            if task.id in seen_ids:
                message = f"Duplicate close-out task id: {task.id}"
                raise ValueError(message)
            seen_ids.add(task.id)
        return self

    model_config = {"extra": "forbid"}


__all__ = ["CloseoutTask", "CloseoutTemplate"]
