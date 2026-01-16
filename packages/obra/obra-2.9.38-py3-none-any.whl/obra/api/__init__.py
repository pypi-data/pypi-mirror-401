"""API client module for Obra.

Provides HTTP client wrapper for communicating with Cloud Functions endpoints,
implementing retry logic, timeout handling, and optional compression.

Also provides protocol types for the hybrid architecture message passing.

Example:
    from obra.api import APIClient
    from obra.api.protocol import ServerAction, DeriveRequest

    client = APIClient.from_config()
    response = client.orchestrate(
        user_id="user123",
        project_id="proj456",
        working_dir="/home/user/project",
        objective="Add user authentication"
    )

Note:
    This package uses PEP 562 lazy loading (ADR-045, Rule 20) to minimize import time.
    APIClient is loaded on first access since it imports requests, pydantic, yaml.
    Protocol types are loaded eagerly since they are lightweight enums/dataclasses.
"""

# Eager imports: lightweight enums and dataclasses (no heavy dependencies)
from obra.api.protocol import (
    ActionType,
    AgentReport,
    AgentType,
    CompletionNotice,
    DerivedPlan,
    DeriveRequest,
    EscalationNotice,
    EscalationReason,
    ExaminationReport,
    ExamineRequest,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    FixRequest,
    FixResult,
    Priority,
    ResumeContext,
    ReviewRequest,
    RevisedPlan,
    RevisionRequest,
    ServerAction,
    SessionPhase,
    SessionStart,
    SessionStatus,
    UserDecision,
    UserDecisionChoice,
)

# Lazy loading registry: maps symbol names to their module paths
_LAZY_IMPORTS = {
    # From client.py (imports requests, pydantic, yaml, obra.config)
    "APIClient": ".client",
}


def __getattr__(name: str):
    """Lazy load heavy components on first access (PEP 562).

    This reduces package import time by deferring APIClient loading
    (which imports requests, pydantic, yaml) until actually needed.
    """
    if name in _LAZY_IMPORTS:
        import importlib

        module = importlib.import_module(_LAZY_IMPORTS[name], __name__)
        value = getattr(module, name)
        # Cache in module globals for subsequent access
        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """Return all public symbols for IDE autocomplete support."""
    return list(__all__)


__all__ = [
    # Lazy import (heavy - imports requests, pydantic, yaml)
    "APIClient",
    # Eager imports (lightweight enums)
    "ActionType",
    "SessionPhase",
    "SessionStatus",
    "Priority",
    "ExecutionStatus",
    "AgentType",
    "EscalationReason",
    "UserDecisionChoice",
    # Eager imports (lightweight dataclasses - Server -> Client)
    "ServerAction",
    "DeriveRequest",
    "ExamineRequest",
    "RevisionRequest",
    "ExecutionRequest",
    "ReviewRequest",
    "FixRequest",
    "EscalationNotice",
    "CompletionNotice",
    # Eager imports (lightweight dataclasses - Client -> Server)
    "SessionStart",
    "DerivedPlan",
    "ExaminationReport",
    "RevisedPlan",
    "ExecutionResult",
    "AgentReport",
    "FixResult",
    "UserDecision",
    # Eager imports (Resume)
    "ResumeContext",
]
