"""OAuth browser-based authentication for Obra.

Provides browser-based OAuth flow for authenticating with Firebase Auth.
This module contains heavy components that use http.server, threading, and webbrowser.
"""

import http.server
import json
import logging
import secrets
import socket
import threading
import urllib.parse
import webbrowser
from typing import TYPE_CHECKING

from obra.config import FIREBASE_API_KEY
from obra.exceptions import AuthenticationError

if TYPE_CHECKING:
    from obra.auth.types import AuthResult

logger = logging.getLogger(__name__)

# Firebase project configuration
FIREBASE_PROJECT_ID = "obra-205b0"
FIREBASE_AUTH_DOMAIN = f"{FIREBASE_PROJECT_ID}.firebaseapp.com"


class LocalCallbackServer:
    """Local HTTP server to receive OAuth callback.

    Starts a temporary server on localhost to receive the auth callback
    from Firebase Auth after browser-based sign-in.
    """

    def __init__(self):
        self.port = self._find_available_port()
        self.auth_result: dict | None = None
        self.error: str | None = None
        self._server: http.server.HTTPServer | None = None
        self._server_thread: threading.Thread | None = None
        self._state = secrets.token_urlsafe(32)

    def _find_available_port(self) -> int:
        """Find an available port for the callback server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    @property
    def callback_url(self) -> str:
        """URL for OAuth callback."""
        return f"http://localhost:{self.port}/callback"

    @property
    def state(self) -> str:
        """CSRF state token."""
        return self._state

    def start(self) -> None:
        """Start the callback server in a background thread."""
        server = self

        class CallbackHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                # Suppress HTTP logging
                pass

            def do_GET(self):
                """Handle GET request (OAuth callback)."""
                parsed = urllib.parse.urlparse(self.path)

                if parsed.path == "/callback":
                    # Parse query parameters
                    params = urllib.parse.parse_qs(parsed.query)

                    # Check for error
                    if "error" in params:
                        server.error = params.get("error", ["Unknown error"])[0]
                        self._send_error_page(server.error)
                        return

                    # Extract token data
                    # Firebase Auth redirects with token in fragment, but we'll
                    # use a custom page that posts the token data via query params
                    id_token = params.get("id_token", [None])[0]
                    refresh_token = params.get("refresh_token", [None])[0]
                    state = params.get("state", [None])[0]

                    # Validate state to prevent CSRF
                    if state != server.state:
                        server.error = "Invalid state parameter (CSRF protection)"
                        self._send_error_page(server.error)
                        return

                    if id_token:
                        server.auth_result = {
                            "id_token": id_token,
                            "refresh_token": refresh_token,
                        }
                        self._send_success_page()
                    else:
                        # Serve the auth page that will handle Firebase sign-in
                        self._send_auth_page()

                elif parsed.path == "/":
                    # Serve the initial auth page
                    self._send_auth_page()

                else:
                    self.send_error(404)

            def do_POST(self):
                """Handle POST request (token submission from auth page)."""
                parsed = urllib.parse.urlparse(self.path)

                if parsed.path == "/callback":
                    content_length = int(self.headers.get("Content-Length", 0))
                    post_data = self.rfile.read(content_length).decode("utf-8")
                    params = urllib.parse.parse_qs(post_data)

                    state = params.get("state", [None])[0]
                    if state != server.state:
                        server.error = "Invalid state parameter"
                        self._send_json({"error": server.error}, 400)
                        return

                    id_token = params.get("id_token", [None])[0]
                    refresh_token = params.get("refresh_token", [None])[0]

                    if id_token:
                        server.auth_result = {
                            "id_token": id_token,
                            "refresh_token": refresh_token,
                        }
                        self._send_json({"success": True})
                    else:
                        error = params.get("error", ["No token received"])[0]
                        server.error = error
                        self._send_json({"error": error}, 400)
                else:
                    self.send_error(404)

            def _send_json(self, data: dict, status: int = 200):
                """Send JSON response."""
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())

            def _send_success_page(self):
                """Send success page after authentication."""
                html = """<!DOCTYPE html>
<html>
<head>
    <title>Obra - Login Successful</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; text-align: center; }
        .success { color: #22c55e; font-size: 48px; }
        h1 { color: #1f2937; }
        p { color: #6b7280; }
    </style>
</head>
<body>
    <div class="success">✓</div>
    <h1>Login Successful!</h1>
    <p>You can close this window and return to the terminal.</p>
    <script>setTimeout(() => window.close(), 2000);</script>
</body>
</html>"""
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))

            def _send_error_page(self, error: str):
                """Send error page."""
                html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Obra - Login Failed</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; text-align: center; }}
        .error {{ color: #ef4444; font-size: 48px; }}
        h1 {{ color: #1f2937; }}
        p {{ color: #6b7280; }}
        .error-msg {{ color: #ef4444; background: #fef2f2; padding: 10px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="error">✗</div>
    <h1>Login Failed</h1>
    <p class="error-msg">{error}</p>
    <p>Please close this window and try again.</p>
</body>
</html>"""
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))

            def _send_auth_page(self):
                """Send the Firebase Auth sign-in page."""
                # This page uses Firebase Auth JS SDK to handle sign-in
                # and posts the result back to our callback
                html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Obra - Sign In</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }}
        h1 {{ color: #1f2937; text-align: center; }}
        .subtitle {{ color: #6b7280; text-align: center; margin-bottom: 30px; }}
        .btn {{ display: block; width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #d1d5db; border-radius: 6px; background: white; cursor: pointer; font-size: 16px; }}
        .btn:hover {{ background: #f3f4f6; }}
        .btn-google {{ border-color: #4285f4; color: #4285f4; }}
        .btn-github {{ border-color: #24292e; color: #24292e; }}
        .divider {{ text-align: center; color: #9ca3af; margin: 20px 0; }}
        .error {{ color: #ef4444; text-align: center; padding: 10px; background: #fef2f2; border-radius: 4px; display: none; }}
        .loading {{ text-align: center; color: #6b7280; display: none; }}
    </style>
</head>
<body>
    <h1>Sign in to Obra</h1>
    <p class="subtitle">Choose your authentication method</p>

    <div id="error" class="error"></div>
    <div id="loading" class="loading">Signing in...</div>

    <div id="buttons">
        <button class="btn btn-google" onclick="signInWithGoogle()">
            Continue with Google
        </button>
        <button class="btn btn-github" onclick="signInWithGithub()">
            Continue with GitHub
        </button>
    </div>

    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
    <script>
        const firebaseConfig = {{
            apiKey: "{FIREBASE_API_KEY}",
            authDomain: "{FIREBASE_AUTH_DOMAIN}",
            projectId: "{FIREBASE_PROJECT_ID}"
        }};
        firebase.initializeApp(firebaseConfig);

        const state = "{server.state}";

        function showError(msg) {{
            document.getElementById('error').textContent = msg;
            document.getElementById('error').style.display = 'block';
            document.getElementById('loading').style.display = 'none';
            document.getElementById('buttons').style.display = 'block';
        }}

        function showLoading() {{
            document.getElementById('error').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('buttons').style.display = 'none';
        }}

        async function handleSignIn(provider) {{
            showLoading();
            try {{
                const result = await firebase.auth().signInWithPopup(provider);
                const user = result.user;
                const idToken = await user.getIdToken();
                const refreshToken = user.refreshToken;

                // Redirect with tokens
                const params = new URLSearchParams({{
                    id_token: idToken,
                    refresh_token: refreshToken,
                    state: state
                }});
                window.location.href = '/callback?' + params.toString();
            }} catch (error) {{
                console.error('Auth error:', error);
                showError(error.message || 'Authentication failed');
            }}
        }}

        function signInWithGoogle() {{
            const provider = new firebase.auth.GoogleAuthProvider();
            handleSignIn(provider);
        }}

        function signInWithGithub() {{
            const provider = new firebase.auth.GithubAuthProvider();
            handleSignIn(provider);
        }}
    </script>
</body>
</html>"""
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))

        self._server = http.server.HTTPServer(("127.0.0.1", self.port), CallbackHandler)
        self._server_thread = threading.Thread(target=self._server.serve_forever)
        self._server_thread.daemon = True
        self._server_thread.start()

    def stop(self) -> None:
        """Stop the callback server."""
        if self._server:
            self._server.shutdown()
            self._server = None
        if self._server_thread:
            self._server_thread.join(timeout=1)
            self._server_thread = None

    def wait_for_callback(self, timeout: float = 300) -> dict | None:
        """Wait for the authentication callback.

        Args:
            timeout: Maximum seconds to wait (default: 5 minutes)

        Returns:
            Auth result dict with id_token and refresh_token, or None on error
        """
        import time

        start = time.time()
        while time.time() - start < timeout:
            if self.auth_result:
                return self.auth_result
            if self.error:
                return None
            time.sleep(0.1)
        return None


def login_with_browser(timeout: float = 300, auto_open: bool = True) -> "AuthResult":
    """Authenticate with Firebase Auth using browser-based OAuth.

    Opens the default browser to a local page that handles Firebase Auth
    sign-in with Google or GitHub OAuth.

    Args:
        timeout: Maximum seconds to wait for authentication (default: 5 minutes)
        auto_open: Whether to automatically open the browser (default: True).
            If False, prints the URL for manual opening.

    Returns:
        AuthResult with user info and tokens

    Raises:
        AuthenticationError: If authentication fails
        TimeoutError: If user doesn't complete auth within timeout
    """
    # Import here to avoid circular imports at module load time
    from obra.auth.tokens import get_user_info
    from obra.auth.types import AuthResult

    # Start local callback server
    server = LocalCallbackServer()
    server.start()

    try:
        # Open browser to local auth page
        auth_url = f"http://localhost:{server.port}/"
        logger.info(f"Opening browser for authentication: {auth_url}")

        if auto_open:
            if not webbrowser.open(auth_url):
                raise AuthenticationError(
                    "Could not open browser. Please open this URL manually:\n" f"  {auth_url}"
                )
        else:
            # Print URL for manual opening
            print(f"\n  {auth_url}\n")

        # Wait for callback
        result = server.wait_for_callback(timeout=timeout)

        if server.error:
            raise AuthenticationError(f"Authentication failed: {server.error}")

        if not result:
            raise TimeoutError(
                f"Authentication timed out after {timeout} seconds. " "Please try again."
            )

        # Get user info from the ID token
        user_info = get_user_info(result["id_token"])

        return AuthResult(
            firebase_uid=user_info["localId"],
            email=user_info.get("email", ""),
            id_token=result["id_token"],
            refresh_token=result.get("refresh_token", ""),
            auth_provider=user_info.get("providerUserInfo", [{}])[0].get("providerId", "unknown"),
            display_name=user_info.get("displayName"),
        )

    finally:
        server.stop()


# Convenience alias
login = login_with_browser


__all__ = [
    "FIREBASE_AUTH_DOMAIN",
    "FIREBASE_PROJECT_ID",
    "LocalCallbackServer",
    "login",
    "login_with_browser",
]
