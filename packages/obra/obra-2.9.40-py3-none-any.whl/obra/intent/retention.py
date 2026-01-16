"""Retention cleanup for scaffolded planning artifacts."""

from __future__ import annotations

from pathlib import Path


def cleanup_retention(root: Path, *, max_files: int) -> int:
    """Delete old files under root based on count limits.

    Returns number of files deleted.
    """
    root = root.expanduser()
    if not root.exists():
        return 0

    files = [p for p in root.rglob("*") if p.is_file()]
    deleted = 0

    if max_files > 0 and len(files) > max_files:
        files.sort(key=lambda p: p.stat().st_mtime)
        for path in files[: len(files) - max_files]:
            try:
                path.unlink()
                deleted += 1
            except OSError:
                continue

    return deleted
