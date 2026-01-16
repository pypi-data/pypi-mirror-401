"""Retention cleanup for scaffolded planning artifacts."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path


def cleanup_retention(root: Path, *, max_age_days: int, max_files: int) -> int:
    """Delete old files under root based on age and count limits.

    Returns number of files deleted.
    """
    root = root.expanduser()
    if not root.exists():
        return 0

    files = [p for p in root.rglob("*") if p.is_file()]
    deleted = 0

    if max_age_days > 0:
        cutoff = datetime.now(UTC) - timedelta(days=max_age_days)
        for path in list(files):
            try:
                mtime = datetime.fromtimestamp(path.stat().st_mtime, UTC)
            except OSError:
                continue
            if mtime < cutoff:
                try:
                    path.unlink()
                    deleted += 1
                    files.remove(path)
                except OSError:
                    continue

    if max_files > 0 and len(files) > max_files:
        files.sort(key=lambda p: p.stat().st_mtime)
        for path in files[: len(files) - max_files]:
            try:
                path.unlink()
                deleted += 1
            except OSError:
                continue

    return deleted
