"""Firebase authentication state management for Obra.

Handles reading and writing Firebase auth credentials from ~/.obra/client-config.yaml.

Example:
    from obra.config.auth import is_authenticated, get_auth_token

    if is_authenticated():
        token = get_auth_token()
"""

from datetime import UTC, datetime, timedelta

from .loaders import load_config, save_config


def get_firebase_uid() -> str | None:
    """Get stored Firebase UID from config.

    Returns:
        Firebase UID string or None if not authenticated
    """
    config = load_config()
    return config.get("firebase_uid")


def get_user_email() -> str | None:
    """Get stored user email from config.

    Returns:
        User email string or None if not authenticated
    """
    config = load_config()
    return config.get("user_email")


def get_auth_token() -> str | None:
    """Get stored Firebase ID token from config.

    Returns:
        Firebase ID token or None if not authenticated
    """
    config = load_config()
    return config.get("auth_token")


def get_refresh_token() -> str | None:
    """Get stored Firebase refresh token from config.

    Returns:
        Firebase refresh token or None if not authenticated
    """
    config = load_config()
    return config.get("refresh_token")


def get_auth_provider() -> str | None:
    """Get stored auth provider from config.

    Returns:
        Auth provider (e.g., "google.com", "github.com") or None
    """
    config = load_config()
    return config.get("auth_provider")


def is_authenticated() -> bool:
    """Check if user is authenticated with Firebase Auth.

    Returns:
        True if Firebase UID and auth token are present
    """
    config = load_config()
    return bool(config.get("firebase_uid") and config.get("auth_token"))


def save_firebase_auth(
    firebase_uid: str,
    email: str,
    auth_token: str,
    refresh_token: str,
    auth_provider: str,
    display_name: str | None = None,
    token_expires_at: datetime | None = None,
) -> None:
    """Save Firebase authentication to config file.

    Args:
        firebase_uid: Firebase user ID
        email: User's email address
        auth_token: Firebase ID token
        refresh_token: Firebase refresh token
        auth_provider: Auth provider (e.g., "google.com")
        display_name: Optional user display name
        token_expires_at: Optional token expiration time. If not provided,
            defaults to 1 hour from now (Firebase ID token lifetime).
    """
    config = load_config()

    config["firebase_uid"] = firebase_uid
    config["user_email"] = email
    config["auth_token"] = auth_token
    config["refresh_token"] = refresh_token
    config["auth_provider"] = auth_provider
    config["auth_timestamp"] = datetime.now(UTC).isoformat()

    # Firebase ID tokens expire in 1 hour - save expiration for auto-refresh
    if token_expires_at is None:
        token_expires_at = datetime.now(UTC) + timedelta(hours=1)
    config["token_expires_at"] = token_expires_at.isoformat()

    if display_name:
        config["display_name"] = display_name

    # Also set user_id to email for compatibility with existing code
    config["user_id"] = email

    save_config(config)


def clear_firebase_auth() -> None:
    """Clear stored Firebase authentication from config file."""
    config = load_config()

    # Remove Firebase auth fields
    for key in [
        "firebase_uid",
        "user_email",
        "auth_token",
        "refresh_token",
        "auth_provider",
        "auth_timestamp",
        "display_name",
    ]:
        config.pop(key, None)

    save_config(config)


# Public exports
__all__ = [
    "clear_firebase_auth",
    "get_auth_provider",
    "get_auth_token",
    "get_firebase_uid",
    "get_refresh_token",
    "get_user_email",
    "is_authenticated",
    "save_firebase_auth",
]
