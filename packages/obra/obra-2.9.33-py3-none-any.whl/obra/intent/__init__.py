"""Intent management module for Obra.

This module provides intent capture and storage functionality for the
auto-intent generation feature. Intents capture user objectives in a
structured format for derivation and verification workflows.

Architecture:
    - IntentModel: Pydantic data model for intent structure
    - IntentStorage: Persistence layer for ~/.obra/intents/{project}/
    - detect_input_type: Classifier for input types (vague_nl, rich_nl, etc.)

Storage Location:
    ~/.obra/intents/{project}/{timestamp}-{slug}.md

Related:
    - docs/design/briefs/AUTO_INTENT_GENERATION_BRIEF.md
    - docs/decisions/ADR-027-two-tier-prompting-architecture.md

Feature Flag:
    - config key: derivation.intent.enabled (default: true)
"""

from typing import TYPE_CHECKING

# PEP 562 lazy loading for heavy components (ADR-045 Rule 20)
# This module exports IntentStorage, IntentModel, and detect_input_type

__all__ = [
    "IntentModel",
    "IntentStorage",
    "detect_input_type",
]


def __getattr__(name: str):
    """Lazy load module exports to minimize import time."""
    if name == "IntentModel":
        from obra.intent.models import IntentModel  # noqa: PLC0415

        return IntentModel
    if name == "IntentStorage":
        from obra.intent.storage import IntentStorage  # noqa: PLC0415

        return IntentStorage
    if name == "detect_input_type":
        from obra.intent.detection import detect_input_type  # noqa: PLC0415

        return detect_input_type
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


if TYPE_CHECKING:
    from obra.intent.detection import detect_input_type
    from obra.intent.models import IntentModel
    from obra.intent.storage import IntentStorage
