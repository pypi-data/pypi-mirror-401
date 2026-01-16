"""Token management for Obra authentication.

Provides functions for token refresh, validation, and auth state management.
"""

import logging
from datetime import UTC, datetime, timedelta

import requests

from obra.config import (
    DEFAULT_NETWORK_TIMEOUT,
    FIREBASE_API_KEY,
    load_config,
    save_config,
)
from obra.exceptions import AuthenticationError

from .types import AuthResult

logger = logging.getLogger(__name__)

# Firebase Auth REST API endpoints
FIREBASE_TOKEN_ENDPOINT = "https://securetoken.googleapis.com/v1/token"
FIREBASE_USERINFO_ENDPOINT = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"

# Refresh if less than 5 minutes until expiration
TOKEN_REFRESH_THRESHOLD = timedelta(minutes=5)

# Default API base URL
DEFAULT_API_BASE_URL = "https://us-central1-obra-205b0.cloudfunctions.net"


def get_user_info(id_token: str) -> dict:
    """Get user info from Firebase ID token.

    Args:
        id_token: Firebase ID token

    Returns:
        User info dict with localId, email, displayName, etc.

    Raises:
        AuthenticationError: If token is invalid
    """
    url = f"{FIREBASE_USERINFO_ENDPOINT}?key={FIREBASE_API_KEY}"

    try:
        response = requests.post(
            url,
            json={"idToken": id_token},
            timeout=DEFAULT_NETWORK_TIMEOUT,
        )

        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Unknown error")
            raise AuthenticationError(f"Failed to get user info: {error_msg}")

        data = response.json()
        users = data.get("users", [])

        if not users:
            raise AuthenticationError("No user found for token")

        return users[0]

    except requests.RequestException as e:
        raise AuthenticationError(f"Network error getting user info: {e}") from e


def refresh_id_token(refresh_token: str) -> tuple[str, str]:
    """Refresh Firebase ID token using refresh token.

    Args:
        refresh_token: Firebase refresh token

    Returns:
        Tuple of (new_id_token, new_refresh_token)

    Raises:
        AuthenticationError: If refresh fails
    """
    url = f"{FIREBASE_TOKEN_ENDPOINT}?key={FIREBASE_API_KEY}"

    try:
        response = requests.post(
            url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            timeout=DEFAULT_NETWORK_TIMEOUT,
        )

        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Unknown error")
            raise AuthenticationError(f"Failed to refresh token: {error_msg}")

        data = response.json()
        return data["id_token"], data["refresh_token"]

    except requests.RequestException as e:
        raise AuthenticationError(f"Network error refreshing token: {e}") from e


def save_auth(auth_result: AuthResult) -> None:
    """Save authentication result to config file.

    Args:
        auth_result: Authentication result to save
    """
    config = load_config()

    config["firebase_uid"] = auth_result.firebase_uid
    config["user_email"] = auth_result.email
    config["auth_token"] = auth_result.id_token
    config["refresh_token"] = auth_result.refresh_token
    config["auth_provider"] = auth_result.auth_provider
    config["auth_timestamp"] = datetime.now(UTC).isoformat()

    # Firebase ID tokens expire in 1 hour - save expiration for auto-refresh
    token_expires_at = auth_result.expires_at or (datetime.now(UTC) + timedelta(hours=1))
    if token_expires_at.tzinfo is None:
        token_expires_at = token_expires_at.replace(tzinfo=UTC)
    config["token_expires_at"] = token_expires_at.isoformat()

    if auth_result.display_name:
        config["display_name"] = auth_result.display_name

    # Set user_id for compatibility with existing code
    config["user_id"] = auth_result.email

    # Remove old license key if present (migrated to OAuth)
    config.pop("license_key", None)

    save_config(config)
    logger.info(f"Saved auth for user: {auth_result.email}")


def clear_auth() -> None:
    """Clear stored authentication from config file."""
    config = load_config()

    # Remove auth fields
    for key in [
        "firebase_uid",
        "user_email",
        "user_id",
        "auth_token",
        "refresh_token",
        "auth_provider",
        "auth_timestamp",
        "display_name",
        "token_expires_at",
    ]:
        config.pop(key, None)

    save_config(config)
    logger.info("Cleared stored authentication")


def get_current_auth() -> AuthResult | None:
    """Get current authentication from config file.

    Returns:
        AuthResult if authenticated, None otherwise
    """
    config = load_config()

    firebase_uid = config.get("firebase_uid")
    if not firebase_uid:
        return None

    return AuthResult(
        firebase_uid=firebase_uid,
        email=config.get("user_email", ""),
        id_token=config.get("auth_token", ""),
        refresh_token=config.get("refresh_token", ""),
        auth_provider=config.get("auth_provider", "unknown"),
        display_name=config.get("display_name"),
    )


def ensure_valid_token() -> str:
    """Ensure we have a valid ID token, refreshing if necessary.

    Returns:
        Valid Firebase ID token

    Raises:
        AuthenticationError: If not authenticated or refresh fails
    """
    auth = get_current_auth()

    if not auth:
        raise AuthenticationError("Not authenticated. Run 'obra login' to sign in.")

    if not auth.id_token:
        raise AuthenticationError("No auth token found. Run 'obra login' to sign in.")

    config = load_config()
    expires_at_raw = config.get("token_expires_at")
    expires_at: datetime | None = None

    if isinstance(expires_at_raw, str) and expires_at_raw:
        try:
            expires_at = datetime.fromisoformat(expires_at_raw.replace("Z", "+00:00"))
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=UTC)
        except ValueError:
            expires_at = None

    if expires_at:
        time_until_expiry = expires_at - datetime.now(UTC)
        if time_until_expiry > TOKEN_REFRESH_THRESHOLD:
            return auth.id_token
    else:
        return auth.id_token

    if not auth.refresh_token:
        return auth.id_token

    try:
        new_id_token, new_refresh_token = refresh_id_token(auth.refresh_token)
    except AuthenticationError as e:
        logger.warning("Token refresh failed: %s", e)
        return auth.id_token

    config["auth_token"] = new_id_token
    config["refresh_token"] = new_refresh_token
    config["token_expires_at"] = (datetime.now(UTC) + timedelta(hours=1)).isoformat()
    save_config(config)

    return new_id_token


def verify_beta_access(id_token: str, api_base_url: str | None = None) -> dict:
    """Verify user has beta access by checking allowlist.

    Calls the /verify_beta_access endpoint to check if the authenticated
    user's email is on the beta allowlist.

    Args:
        id_token: Firebase ID token
        api_base_url: Optional API base URL (default: production)

    Returns:
        Dict with user info if access granted

    Raises:
        AuthenticationError: If not on allowlist or token invalid
    """
    base_url = api_base_url or DEFAULT_API_BASE_URL
    url = f"{base_url}/verify_beta_access"

    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {id_token}"},
            timeout=DEFAULT_NETWORK_TIMEOUT,
        )

        if response.status_code == 200:
            return response.json()

        if response.status_code == 403:
            data = response.json()
            error_code = data.get("code", "access_denied")

            if error_code == "not_on_allowlist":
                raise AuthenticationError(
                    "Your email is not on the beta allowlist.\n"
                    "Contact the Obra team to request access."
                )
            if error_code == "access_revoked":
                raise AuthenticationError(
                    "Your beta access has been revoked.\n"
                    "Contact the Obra team for more information."
                )
            raise AuthenticationError(f"Access denied: {data.get('message', error_code)}")

        if response.status_code == 401:
            raise AuthenticationError(
                "Authentication token is invalid or expired.\nRun 'obra login' to sign in again."
            )

        raise AuthenticationError(f"Failed to verify access: HTTP {response.status_code}")

    except requests.RequestException as e:
        raise AuthenticationError(f"Network error: {e}") from e


__all__ = [
    # Functions
    "get_user_info",
    "refresh_id_token",
    "save_auth",
    "clear_auth",
    "get_current_auth",
    "ensure_valid_token",
    "verify_beta_access",
    # Constants
    "FIREBASE_TOKEN_ENDPOINT",
    "FIREBASE_USERINFO_ENDPOINT",
    "TOKEN_REFRESH_THRESHOLD",
    "DEFAULT_API_BASE_URL",
]
