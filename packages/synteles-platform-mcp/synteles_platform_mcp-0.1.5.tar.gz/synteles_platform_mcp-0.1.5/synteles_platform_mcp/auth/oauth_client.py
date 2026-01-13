"""OAuth 2.0 with PKCE client for Synteles Platform API."""

from __future__ import annotations

import base64
import hashlib
import logging
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING, Any, cast
from urllib.parse import parse_qs, urlparse

import requests

from .token_store import TokenStore

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# HTTP Status Constants
HTTP_200_OK = 200


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback - receives authorization code from Cognito."""

    auth_code: str | None = None
    auth_error: str | None = None

    def do_GET(self) -> None:
        """Handle GET request for OAuth callback with authorization code."""
        query = urlparse(self.path).query
        params = parse_qs(query)

        if "code" in params:
            # Successfully received authorization code from Cognito
            CallbackHandler.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"""
                <html>
                <body style="font-family: system-ui; padding: 40px; text-align: center;">
                    <h1 style="color: #22c55e;">&#x2713; Authentication In Progress...</h1>
                    <p>Completing authentication securely.</p>
                    <p>You can close this window and return to Claude Desktop.</p>
                </body>
                </html>
            """
            )
        elif "error" in params:
            CallbackHandler.auth_error = params["error"][0]
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            error_msg = params["error"][0]
            self.wfile.write(
                f"""
                <html>
                <body style="font-family: system-ui; padding: 40px; text-align: center;">
                    <h1 style="color: #ef4444;">&#x2717; Authentication Failed</h1>
                    <p>Error: {error_msg}</p>
                    <p>You can close this window and try again.</p>
                </body>
                </html>
            """.encode()
            )
        else:
            # Unexpected response
            CallbackHandler.auth_error = "Invalid callback - missing code"
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"""
                <html>
                <body style="font-family: system-ui; padding: 40px; text-align: center;">
                    <h1 style="color: #ef4444;">&#x2717; Invalid Callback</h1>
                    <p>Missing authorization code. Please try again.</p>
                </body>
                </html>
            """
            )

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        """Suppress HTTP server logs."""


class OAuthClient:
    """OAuth 2.0 PKCE client for Synteles Platform API."""

    def __init__(self, api_domain: str = "api.synteles.dev") -> None:
        """Initialize OAuth client.

        Args:
            api_domain: API domain (default: api.synteles.dev)

        """
        self.api_domain = api_domain
        self.base_url = f"https://{api_domain}/v1"
        self.token_store = TokenStore()

    def _generate_pkce_pair(self) -> tuple[str, str]:
        """Generate PKCE code verifier and challenge.

        Returns:
            Tuple of (code_verifier, code_challenge)

        """
        # Generate 32-byte random code verifier
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")

        # Generate SHA256 challenge
        code_challenge = (
            base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).decode("utf-8").rstrip("=")
        )

        return code_verifier, code_challenge

    def login(self, callback_port: int = 8888, timeout: int = 120) -> dict[str, Any]:
        """Start OAuth login flow with PKCE using POST /auth/login endpoint.

        Args:
            callback_port: Port for local callback server (default: 8888)
            timeout: Timeout in seconds for user to complete auth (default: 120)

        Returns:
            Dict with login result

        Raises:
            Exception: If authentication fails

        """
        # Generate PKCE pair
        code_verifier, code_challenge = self._generate_pkce_pair()

        # Start local callback server to receive authorization code
        CallbackHandler.auth_code = None
        CallbackHandler.auth_error = None

        server = HTTPServer(("localhost", callback_port), CallbackHandler)
        server_thread = threading.Thread(target=server.handle_request)
        server_thread.daemon = True
        server_thread.start()

        try:
            # Call POST /auth/login to get authorization URL
            redirect_uri = f"http://localhost:{callback_port}/callback"
            try:
                response = requests.post(
                    f"{self.base_url}/auth/login",
                    json={
                        "code_challenge": code_challenge,
                        "redirect_uri": redirect_uri,
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=10,
                )

                if response.status_code != HTTP_200_OK:
                    msg = f"Login request failed: {response.text}"
                    raise RuntimeError(msg)

                auth_response = response.json()
                authorization_url = auth_response.get("authorization_url")

                if not authorization_url:
                    msg = "No authorization_url in response"
                    raise RuntimeError(msg)

            except Exception as e:
                msg = f"Failed to get authorization URL: {e}"
                raise RuntimeError(msg) from e

            logger.info("Opening browser for authentication")
            logger.info("\n🔐 Opening browser for authentication...")
            logger.info(f"If browser doesn't open, visit:\n{authorization_url}\n")

            # Open browser to Cognito authorization page
            webbrowser.open(authorization_url)

            # Wait for callback with authorization code
            server_thread.join(timeout=timeout)

            if CallbackHandler.auth_error:
                msg = f"Authentication failed: {CallbackHandler.auth_error}"
                raise RuntimeError(msg)

            if not CallbackHandler.auth_code:
                msg = "Authentication timeout - no authorization code received"
                raise RuntimeError(msg)

            # Exchange authorization code for tokens using POST /auth/token
            try:
                token_response = requests.post(
                    f"{self.base_url}/auth/token",
                    json={
                        "code": CallbackHandler.auth_code,
                        "code_verifier": code_verifier,
                        "redirect_uri": redirect_uri,
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                )

                if token_response.status_code != HTTP_200_OK:
                    msg = f"Token exchange failed: {token_response.text}"
                    raise RuntimeError(msg)

                tokens = token_response.json()

            except Exception as e:
                msg = f"Failed to exchange code for tokens: {e}"
                raise RuntimeError(msg) from e

            # Store tokens securely in OS keychain
            self.token_store.save_tokens(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                id_token=tokens.get("id_token"),
            )

            logger.info("Successfully authenticated and stored tokens")
            return {
                "status": "success",
                "message": "Successfully authenticated! Tokens stored securely.",
                "expires_in": tokens.get("expires_in", 3600),
            }
        finally:
            # Always close the server socket to free the port
            server.server_close()
            logger.debug("OAuth callback server closed")

    def refresh_access_token(self) -> str | None:
        """Refresh access token using refresh token.

        Returns:
            New access token or None if refresh fails

        """
        refresh_token = self.token_store.get_refresh_token()

        if not refresh_token:
            logger.warning("No refresh token available")
            return None

        try:
            response = requests.post(
                f"{self.base_url}/auth/refresh",
                json={"refresh_token": refresh_token},
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code != HTTP_200_OK:
                logger.error("Token refresh failed: %s", response.text)
                return None

            tokens = response.json()

            # Update stored tokens
            self.token_store.save_tokens(
                access_token=tokens["access_token"],
                refresh_token=tokens.get("refresh_token", refresh_token),  # Use new or keep existing
                id_token=tokens.get("id_token"),
            )

            logger.info("Access token refreshed successfully")
            return cast(str, tokens["access_token"])

        except Exception:
            logger.exception("Error refreshing token")
            return None

    def logout(self) -> dict[str, str]:
        """Clear stored tokens and logout.

        Returns:
            Logout status

        """
        refresh_token = self.token_store.get_refresh_token()

        # Try to revoke refresh token
        if refresh_token:
            try:
                requests.post(
                    f"{self.base_url}/auth/logout",
                    json={"refresh_token": refresh_token},
                    headers={"Content-Type": "application/json"},
                    timeout=10,
                )
            except Exception as e:
                logger.warning("Logout request failed (continuing anyway): %s", e)

        # Clear tokens from keychain
        self.token_store.clear_tokens()
        logger.info("User logged out, tokens cleared")
        return {
            "status": "success",
            "message": "Logged out successfully. Tokens cleared from secure storage.",
        }

    def get_access_token(self) -> str | None:
        """Get current access token, refreshing if needed.

        Returns:
            Valid access token or None

        """
        access_token = self.token_store.get_access_token()

        if not access_token:
            return None

        # TODO: Add token expiration check and auto-refresh
        # For now, return the token as-is
        return access_token
