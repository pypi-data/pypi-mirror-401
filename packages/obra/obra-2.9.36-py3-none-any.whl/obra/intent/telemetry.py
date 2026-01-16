"""Telemetry logging for scaffolded planning (local JSONL)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def log_scaffolded_event(path: Path, payload: dict[str, Any]) -> None:
    """Append a scaffolded planning telemetry event to JSONL file."""
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(payload)
    payload.setdefault("timestamp", datetime.now(UTC).isoformat())
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
