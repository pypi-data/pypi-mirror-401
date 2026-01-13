"""Unit tests for OAuthClient class."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, Mock, patch

from synteles_platform_mcp.auth.oauth_client import CallbackHandler, OAuthClient


class TestOAuthClient(unittest.TestCase):
    """Test cases for OAuthClient class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.api_domain = "api.test.example.com"
        self.oauth_client = OAuthClient(api_domain=self.api_domain)
        self.callback_port = 8888

    def test_init_default_domain(self) -> None:
        """Test initialization with default API domain."""
        client = OAuthClient()
        assert client.api_domain == "api.synteles.dev"
        assert client.base_url == "https://api.synteles.dev/v1"

    def test_init_custom_domain(self) -> None:
        """Test initialization with custom API domain."""
        assert self.oauth_client.api_domain == self.api_domain
        assert self.oauth_client.base_url == f"https://{self.api_domain}/v1"

    def test_generate_pkce_pair(self) -> None:
        """Test PKCE code verifier and challenge generation."""
        verifier, challenge = self.oauth_client._generate_pkce_pair()

        # Verify verifier is base64url encoded and correct length
        assert isinstance(verifier, str)
        assert len(verifier) >= 43  # 32 bytes base64url encoded

        # Verify challenge is base64url encoded SHA256 hash
        assert isinstance(challenge, str)
        assert len(challenge) >= 43  # SHA256 hash base64url encoded

        # Verify they are different
        assert verifier != challenge

    def test_generate_pkce_pair_uniqueness(self) -> None:
        """Test that each PKCE pair is unique."""
        pair1 = self.oauth_client._generate_pkce_pair()
        pair2 = self.oauth_client._generate_pkce_pair()

        assert pair1[0] != pair2[0]  # Different verifiers
        assert pair1[1] != pair2[1]  # Different challenges

    @patch("synteles_platform_mcp.auth.oauth_client.webbrowser")
    @patch("synteles_platform_mcp.auth.oauth_client.HTTPServer")
    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_login_success(
        self,
        mock_keyring: MagicMock,
        mock_requests: MagicMock,
        mock_http_server: MagicMock,
        mock_webbrowser: MagicMock,
    ) -> None:
        """Test successful OAuth login flow."""
        # Mock /auth/login response
        mock_login_response = Mock()
        mock_login_response.status_code = 200
        mock_login_response.json.return_value = {"authorization_url": "https://auth.example.com/login"}

        # Mock /auth/token response
        mock_token_response = Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {
            "access_token": "test_access",
            "refresh_token": "test_refresh",
            "id_token": "test_id",
            "expires_in": 3600,
        }

        mock_requests.post.side_effect = [mock_login_response, mock_token_response]

        # Mock server
        mock_server = Mock()
        mock_http_server.return_value = mock_server

        # Mock thread to set auth_code when join() is called
        with patch("synteles_platform_mcp.auth.oauth_client.threading.Thread") as mock_thread_class:
            mock_thread = Mock()

            # When join() is called, simulate the callback receiving the auth code
            def mock_join(timeout=None):
                CallbackHandler.auth_code = "test_auth_code"

            mock_thread.join = mock_join
            mock_thread_class.return_value = mock_thread

            result = self.oauth_client.login(callback_port=self.callback_port, timeout=120)

            # Verify result
            assert result["status"] == "success"
            assert result["expires_in"] == 3600
            assert "successfully" in result["message"].lower()

            # Verify server was started and closed
            mock_server.server_close.assert_called_once()

            # Verify browser was opened
            mock_webbrowser.open.assert_called_once()

    @patch("synteles_platform_mcp.auth.oauth_client.HTTPServer")
    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    def test_login_failed_login_request(
        self,
        mock_requests: MagicMock,
        mock_http_server: MagicMock,
    ) -> None:
        """Test login failure when /auth/login request fails."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_requests.post.return_value = mock_response

        mock_server = Mock()
        mock_http_server.return_value = mock_server

        with self.assertRaises(RuntimeError) as context:
            self.oauth_client.login(callback_port=self.callback_port)

        assert "Login request failed" in str(context.exception)
        # Verify server was closed on error
        mock_server.server_close.assert_called_once()

    @patch("synteles_platform_mcp.auth.oauth_client.webbrowser")
    @patch("synteles_platform_mcp.auth.oauth_client.HTTPServer")
    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    def test_login_auth_timeout(
        self,
        mock_requests: MagicMock,
        mock_http_server: MagicMock,
        mock_webbrowser: MagicMock,
    ) -> None:
        """Test login timeout when user doesn't complete auth."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"authorization_url": "https://auth.example.com/login"}
        mock_requests.post.return_value = mock_response

        # Simulate timeout - no auth code received
        CallbackHandler.auth_code = None
        CallbackHandler.auth_error = None

        mock_server = Mock()
        mock_http_server.return_value = mock_server

        with patch("synteles_platform_mcp.auth.oauth_client.threading.Thread") as mock_thread_class:
            mock_thread = Mock()
            mock_thread_class.return_value = mock_thread

            with self.assertRaises(RuntimeError) as context:
                self.oauth_client.login(callback_port=self.callback_port, timeout=1)

            assert "timeout" in str(context.exception).lower()
            mock_server.server_close.assert_called_once()

    @patch("synteles_platform_mcp.auth.oauth_client.webbrowser")
    @patch("synteles_platform_mcp.auth.oauth_client.HTTPServer")
    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    def test_login_auth_error(
        self,
        mock_requests: MagicMock,
        mock_http_server: MagicMock,
        mock_webbrowser: MagicMock,
    ) -> None:
        """Test login when user denies authorization."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"authorization_url": "https://auth.example.com/login"}
        mock_requests.post.return_value = mock_response

        mock_server = Mock()
        mock_http_server.return_value = mock_server

        with patch("synteles_platform_mcp.auth.oauth_client.threading.Thread") as mock_thread_class:
            mock_thread = Mock()

            # When join() is called, simulate user denying access
            def mock_join(timeout=None):
                CallbackHandler.auth_error = "access_denied"
                CallbackHandler.auth_code = None

            mock_thread.join = mock_join
            mock_thread_class.return_value = mock_thread

            with self.assertRaises(RuntimeError) as context:
                self.oauth_client.login(callback_port=self.callback_port)

            # Should contain the auth error
            exception_str = str(context.exception)
            # The code checks auth_error BEFORE checking for timeout
            assert "Authentication failed" in exception_str and "access_denied" in exception_str
            mock_server.server_close.assert_called_once()

    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    def test_refresh_access_token_success(self, mock_requests: MagicMock) -> None:
        """Test successful token refresh."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
        }
        mock_requests.post.return_value = mock_response

        with patch.object(
            self.oauth_client.token_store,
            "get_refresh_token",
            return_value="old_refresh",
        ):
            with patch.object(self.oauth_client.token_store, "save_tokens") as mock_save:
                new_token = self.oauth_client.refresh_access_token()

                assert new_token == "new_access_token"
                mock_save.assert_called_once()

    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    def test_refresh_access_token_no_refresh_token(self, mock_requests: MagicMock) -> None:
        """Test token refresh when no refresh token is available."""
        with patch.object(self.oauth_client.token_store, "get_refresh_token", return_value=None):
            result = self.oauth_client.refresh_access_token()

            assert result is None
            mock_requests.post.assert_not_called()

    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    def test_refresh_access_token_failure(self, mock_requests: MagicMock) -> None:
        """Test token refresh failure."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Invalid refresh token"
        mock_requests.post.return_value = mock_response

        with patch.object(
            self.oauth_client.token_store,
            "get_refresh_token",
            return_value="invalid_refresh",
        ):
            result = self.oauth_client.refresh_access_token()

            assert result is None

    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    def test_logout_success(self, mock_requests: MagicMock) -> None:
        """Test successful logout."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        with patch.object(
            self.oauth_client.token_store,
            "get_refresh_token",
            return_value="test_refresh",
        ):
            with patch.object(self.oauth_client.token_store, "clear_tokens") as mock_clear:
                result = self.oauth_client.logout()

                assert result["status"] == "success"
                assert "logged out" in result["message"].lower()
                mock_clear.assert_called_once()

    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    def test_logout_with_api_failure(self, mock_requests: MagicMock) -> None:
        """Test logout continues even if API call fails."""
        mock_requests.post.side_effect = Exception("Network error")

        with patch.object(
            self.oauth_client.token_store,
            "get_refresh_token",
            return_value="test_refresh",
        ):
            with patch.object(self.oauth_client.token_store, "clear_tokens") as mock_clear:
                result = self.oauth_client.logout()

                # Should still succeed and clear tokens
                assert result["status"] == "success"
                mock_clear.assert_called_once()

    def test_get_access_token(self) -> None:
        """Test getting access token from store."""
        with patch.object(self.oauth_client.token_store, "get_access_token", return_value="test_token"):
            token = self.oauth_client.get_access_token()

            assert token == "test_token"

    def test_get_access_token_when_missing(self) -> None:
        """Test getting access token when it doesn't exist."""
        with patch.object(self.oauth_client.token_store, "get_access_token", return_value=None):
            token = self.oauth_client.get_access_token()

            assert token is None


class TestCallbackHandler(unittest.TestCase):
    """Test cases for OAuth callback handler."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        CallbackHandler.auth_code = None
        CallbackHandler.auth_error = None

    def test_callback_handler_class_variables(self) -> None:
        """Test that CallbackHandler has the required class variables."""
        assert hasattr(CallbackHandler, "auth_code")
        assert hasattr(CallbackHandler, "auth_error")

    def test_log_message_suppression(self) -> None:
        """Test that log_message method has correct signature."""
        # Simply verify the method exists and can be called
        assert hasattr(CallbackHandler, "log_message")
        # The method should accept format and args
        import inspect

        sig = inspect.signature(CallbackHandler.log_message)
        # Should have self, format, and *args parameters
        assert len(sig.parameters) >= 2


if __name__ == "__main__":
    unittest.main()
