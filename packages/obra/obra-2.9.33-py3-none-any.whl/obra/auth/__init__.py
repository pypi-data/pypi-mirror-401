"""Firebase Authentication module for Obra.

Provides browser-based OAuth flow for authenticating with Firebase Auth.
Supports Google, GitHub, and email/password providers.

Example:
    from obra.auth import login_with_browser, get_current_auth, ensure_valid_token

    # Login via browser
    auth_result = login_with_browser()
    save_auth(auth_result)

    # Get current auth
    auth = get_current_auth()
    if auth:
        print(f"Logged in as: {auth.email}")

    # Ensure valid token for API calls
    token = ensure_valid_token()
"""

# Eager imports: lightweight types only
from .types import AuthResult

# Lazy loading registry - maps symbol names to submodules
_LAZY_IMPORTS = {
    # From oauth module (heavy: http.server, threading, webbrowser)
    "LocalCallbackServer": ".oauth",
    "login_with_browser": ".oauth",
    "login": ".oauth",
    "FIREBASE_PROJECT_ID": ".oauth",
    "FIREBASE_AUTH_DOMAIN": ".oauth",
    # From tokens module (uses requests, config)
    "get_user_info": ".tokens",
    "refresh_id_token": ".tokens",
    "save_auth": ".tokens",
    "clear_auth": ".tokens",
    "get_current_auth": ".tokens",
    "ensure_valid_token": ".tokens",
    "verify_beta_access": ".tokens",
    "FIREBASE_TOKEN_ENDPOINT": ".tokens",
    "FIREBASE_USERINFO_ENDPOINT": ".tokens",
    "TOKEN_REFRESH_THRESHOLD": ".tokens",
    "DEFAULT_API_BASE_URL": ".tokens",
}


def __getattr__(name: str):
    """Lazy load heavy components on first access."""
    if name in _LAZY_IMPORTS:
        import importlib

        module = importlib.import_module(_LAZY_IMPORTS[name], __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Keep __all__ complete for IDE/type checker support
__all__ = [
    # Eager (lightweight types)
    "AuthResult",
    # Lazy (classes)
    "LocalCallbackServer",
    # Lazy (constants)
    "FIREBASE_PROJECT_ID",
    "FIREBASE_AUTH_DOMAIN",
    "FIREBASE_TOKEN_ENDPOINT",
    "FIREBASE_USERINFO_ENDPOINT",
    "TOKEN_REFRESH_THRESHOLD",
    "DEFAULT_API_BASE_URL",
    # Lazy (functions)
    "login_with_browser",
    "login",
    "get_user_info",
    "refresh_id_token",
    "save_auth",
    "clear_auth",
    "get_current_auth",
    "ensure_valid_token",
    "verify_beta_access",
]
