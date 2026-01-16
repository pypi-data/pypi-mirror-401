"""Version check module for Obra CLI.

Provides asynchronous version checking against PyPI to notify users
when a newer version of Obra is available. Uses background threading
to avoid blocking CLI startup.

Features:
- Semantic version comparison using packaging.version
- Async PyPI API fetching with timeout
- Local caching to prevent notification spam
- Privacy-friendly (no tracking or user identification)
- Configurable via CLI config
- Exit handler ensures thread completes before CLI exits

Example:
    from obra.version_check import check_for_updates_async

    # Fire background check (non-blocking)
    check_for_updates_async()

Reference: FEAT-CLI-VERSION-NOTIFY-001
"""

import atexit
import json
import logging
import threading
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TypedDict

import requests
from packaging.version import InvalidVersion
from packaging.version import parse as parse_version

logger = logging.getLogger(__name__)

# Thread reference for exit handler coordination
_version_check_thread: threading.Thread | None = None
_VERSION_CHECK_EXIT_TIMEOUT = 3.0  # Max seconds to wait at exit

# PyPI API endpoint for Obra package
PYPI_API_URL = "https://pypi.org/pypi/obra/json"
PYPI_TIMEOUT = 2  # seconds

# Cache location
CACHE_DIR = Path.home() / ".obra"
CACHE_FILE = CACHE_DIR / ".version_check_cache"


class VersionCache(TypedDict, total=False):
    """Structure for version check cache.

    Attributes:
        last_check_time: ISO timestamp of last PyPI check
        latest_version: Latest version fetched from PyPI
        last_shown_time: ISO timestamp when banner was last shown
    """

    last_check_time: str
    latest_version: str
    last_shown_time: str


def compare_versions(current: str, latest: str) -> bool:
    """Compare semantic versions to determine if an update is available.

    Uses packaging.version.parse() for proper semantic version comparison,
    handling major, minor, patch increments, and prerelease versions.

    Args:
        current: Current installed version (e.g., "2.5.47")
        latest: Latest available version from PyPI (e.g., "2.6.0")

    Returns:
        True if latest > current, False otherwise

    Examples:
        >>> compare_versions("2.5.47", "2.6.0")
        True
        >>> compare_versions("2.6.0", "2.5.99")
        False
        >>> compare_versions("2.5.47", "2.5.47")
        False
        >>> compare_versions("2.5.47", "2.5.47-beta.1")
        False
    """
    try:
        current_ver = parse_version(current)
        latest_ver = parse_version(latest)
        return latest_ver > current_ver
    except InvalidVersion as e:
        logger.debug("Invalid version format: %s", e)
        return False


def fetch_latest_version() -> str | None:
    """Fetch the latest version of Obra from PyPI.

    Makes a synchronous HTTP request to the PyPI JSON API with a 2-second
    timeout. This function is intended to be called from a background thread
    to avoid blocking CLI startup.

    Returns:
        Latest version string (e.g., "2.6.0") if successful, None on error

    Examples:
        >>> version = fetch_latest_version()
        >>> if version:
        ...     print(f"Latest version: {version}")
    """
    try:
        response = requests.get(PYPI_API_URL, timeout=PYPI_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        version = data.get("info", {}).get("version")
        if version:
            logger.debug("Fetched latest version from PyPI: %s", version)
            return version
        logger.warning("PyPI response missing version field")
        return None
    except requests.exceptions.Timeout:
        logger.debug("PyPI request timed out")
        return None
    except requests.exceptions.RequestException as e:
        logger.debug("PyPI request failed: %s", e)
        return None
    except (json.JSONDecodeError, KeyError) as e:
        logger.debug("Failed to parse PyPI response: %s", e)
        return None


def read_cache() -> VersionCache | None:
    """Read version check cache from disk.

    Returns:
        Cache dict with last_check_time, latest_version, and last_shown_time,
        or None if cache doesn't exist or is invalid

    Examples:
        >>> cache = read_cache()
        >>> if cache and "latest_version" in cache:
        ...     print(f"Cached version: {cache['latest_version']}")
    """
    try:
        if not CACHE_FILE.exists():
            return None

        with CACHE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate structure
        if not isinstance(data, dict):
            logger.warning("Cache file has invalid structure")
            return None

        return data
    except (json.JSONDecodeError, OSError) as e:
        logger.debug("Failed to read cache: %s", e)
        return None


def write_cache(cache: VersionCache) -> bool:
    """Write version check cache to disk.

    Args:
        cache: Cache dict with last_check_time, latest_version, last_shown_time

    Returns:
        True if successful, False on error

    Examples:
        >>> cache = {
        ...     "last_check_time": "2026-01-08T12:34:56Z",
        ...     "latest_version": "2.6.0",
        ...     "last_shown_time": "2026-01-08T12:34:56Z"
        ... }
        >>> write_cache(cache)
        True
    """
    try:
        # Ensure cache directory exists
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        with CACHE_FILE.open("w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)

        logger.debug("Cache written to %s", CACHE_FILE)
        return True
    except OSError as e:
        logger.debug("Failed to write cache: %s", e)
        return False


def _background_check() -> None:
    """Background worker that checks for version updates.

    This function runs in a daemon thread and handles all the logic
    for fetching, comparing, and displaying version updates. Fails
    silently on any error to avoid disrupting CLI usage.
    """
    try:
        from obra import __version__ as current_version

        # Read cache
        cache = read_cache()

        # Fetch latest version from PyPI
        latest_version = fetch_latest_version()
        if not latest_version:
            return

        # Update cache with latest check
        now = datetime.now(UTC).isoformat()
        new_cache: VersionCache = {
            "last_check_time": now,
            "latest_version": latest_version,
        }

        # Check if we should show the banner
        should_show = False
        if compare_versions(current_version, latest_version):
            # New version available - check cooldown
            if cache and "last_shown_time" in cache:
                # Get cooldown from config
                # pylint: disable=no-name-in-module
                from obra.config import get_update_notification_cooldown_minutes

                cooldown_minutes = get_update_notification_cooldown_minutes()
                try:
                    last_shown = datetime.fromisoformat(cache["last_shown_time"])
                    if datetime.now(UTC) - last_shown > timedelta(
                        minutes=cooldown_minutes
                    ):
                        should_show = True
                except (ValueError, KeyError):
                    # Invalid timestamp, show banner
                    should_show = True
            else:
                # Never shown before, show banner
                should_show = True

        if should_show:
            # Display update banner
            _display_update_banner(current_version, latest_version)
            new_cache["last_shown_time"] = now
        elif cache and "last_shown_time" in cache:
            # Preserve existing last_shown_time
            new_cache["last_shown_time"] = cache["last_shown_time"]

        # Write cache
        write_cache(new_cache)

    except Exception as e:  # pylint: disable=broad-except
        # Fail silently - version check should never disrupt CLI
        logger.debug("Version check failed: %s", e)


def _display_update_banner(current: str, latest: str) -> None:
    """Display update notification banner to stderr.

    Args:
        current: Current installed version
        latest: Latest available version from PyPI
    """
    # Import here to avoid circular dependencies and reduce startup overhead
    from rich.console import Console
    from rich.panel import Panel

    err_console = Console(stderr=True)

    message = (
        f"[bold yellow]Update available![/bold yellow] "
        f"{current} → [bold green]{latest}[/bold green]\n\n"
        "Upgrade command:\n"
        "  [bold cyan]pipx upgrade obra[/bold cyan]\n\n"
        "Changelog:\n"
        "  [link=https://obra.dev/changelog]https://obra.dev/changelog[/link]"
    )

    panel = Panel(
        message,
        title="[bold]Obra Version Notification[/bold]",
        border_style="yellow",
        padding=(1, 2),
    )

    err_console.print(panel)


def _on_exit_wait_for_version_check() -> None:
    """Exit handler that waits for version check thread to complete.

    This ensures the version check has time to complete before the CLI
    exits, even for quick commands like `obra --help`. Uses a timeout
    to avoid blocking indefinitely if something goes wrong.
    """
    global _version_check_thread
    if _version_check_thread is not None and _version_check_thread.is_alive():
        logger.debug("Waiting for version check to complete...")
        _version_check_thread.join(timeout=_VERSION_CHECK_EXIT_TIMEOUT)
        if _version_check_thread.is_alive():
            logger.debug("Version check timed out at exit")


def check_for_updates_async() -> None:
    """Spawn background thread to check for version updates.

    This is the main entry point for version checking. It spawns a
    daemon thread that performs the check asynchronously, returning
    immediately to avoid blocking CLI startup.

    The thread will:
    - Fetch latest version from PyPI with 2-second timeout
    - Compare with current version
    - Display banner on stderr if update available
    - Respect cooldown period to avoid notification spam
    - Fail silently on any error

    An atexit handler ensures the thread has time to complete before
    the CLI exits, even for quick commands.

    Examples:
        >>> # Call from CLI main() before app() invocation
        >>> check_for_updates_async()
        >>> # CLI continues immediately, version check runs in background
    """
    global _version_check_thread

    # Check config flag - skip if disabled
    # pylint: disable=no-name-in-module
    from obra.config import get_check_for_updates

    if not get_check_for_updates():
        logger.debug("Version check disabled via config")
        return

    # Skip if already running (shouldn't happen, but be safe)
    if _version_check_thread is not None and _version_check_thread.is_alive():
        logger.debug("Version check already in progress")
        return

    thread = threading.Thread(target=_background_check, daemon=True)
    thread.start()
    _version_check_thread = thread

    # Register exit handler to wait for thread completion
    atexit.register(_on_exit_wait_for_version_check)

    # Return immediately - thread runs in background
