"""Integration tests for the Synteles Platform MCP Server.

These tests verify that different components work together correctly.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, Mock, patch

from synteles_platform_mcp.auth.oauth_client import OAuthClient
from synteles_platform_mcp.auth.token_store import TokenStore
from synteles_platform_mcp.server import (
    PlatformAPIError,
    _make_request,
    synteles_get_current_user,
    synteles_login,
)


class TestAuthenticationFlow(unittest.TestCase):
    """Integration tests for the complete authentication flow."""

    @patch("synteles_platform_mcp.auth.oauth_client.webbrowser")
    @patch("synteles_platform_mcp.auth.oauth_client.HTTPServer")
    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_full_login_and_api_call_flow(
        self,
        mock_keyring: MagicMock,
        mock_requests: MagicMock,
        mock_http_server: MagicMock,
        mock_webbrowser: MagicMock,
    ) -> None:
        """Test complete flow: login -> store tokens -> make API call."""
        from synteles_platform_mcp.auth.oauth_client import CallbackHandler

        # Mock login flow
        mock_login_response = Mock()
        mock_login_response.status_code = 200
        mock_login_response.json.return_value = {"authorization_url": "https://auth.example.com/login"}

        mock_token_response = Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600,
        }

        mock_requests.post.side_effect = [mock_login_response, mock_token_response]

        CallbackHandler.auth_code = "test_auth_code"
        CallbackHandler.auth_error = None

        mock_server = Mock()
        mock_http_server.return_value = mock_server

        # Mock threading
        with patch("synteles_platform_mcp.auth.oauth_client.threading.Thread") as mock_thread_class:
            mock_thread = Mock()

            # When join() is called, simulate callback receiving auth code
            def mock_join(timeout=None):
                CallbackHandler.auth_code = "test_auth_code"

            mock_thread.join = mock_join
            mock_thread_class.return_value = mock_thread

            # Perform login
            result = synteles_login(callback_port=8888)

            # Verify login succeeded
            assert result["status"] == "success"

            # Verify tokens were saved to keyring
            assert mock_keyring.set_password.call_count >= 2

        # Mock keyring to return the saved tokens
        mock_keyring.get_password.side_effect = lambda service, key: {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
        }.get(key)

        # Now make an API call using stored token - need to patch main.requests
        with patch("synteles_platform_mcp.main.requests") as mock_main_requests:
            # Mock requests.exceptions module
            class MockRequestException(Exception):
                pass

            mock_main_requests.exceptions = MagicMock()
            mock_main_requests.exceptions.RequestException = MockRequestException

            mock_api_response = Mock()
            mock_api_response.status_code = 200
            mock_api_response.json.return_value = {
                "sub": "user-123",
                "email": "test@example.com",
            }
            mock_main_requests.request.return_value = mock_api_response

            user_data = synteles_get_current_user(response_format="json")

            # Verify API call succeeded with stored token
            assert user_data["sub"] == "user-123"
            assert user_data["email"] == "test@example.com"

    @patch("synteles_platform_mcp.main.requests")
    @patch("synteles_platform_mcp.main.oauth_client")
    def test_token_refresh_during_api_call(
        self,
        mock_oauth_client: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        """Test automatic token refresh when API returns 401."""
        # First API call returns 401 (expired token)
        mock_401_response = Mock()
        mock_401_response.status_code = 401

        # Second API call (after refresh) returns 200
        mock_200_response = Mock()
        mock_200_response.status_code = 200
        mock_200_response.json.return_value = {"data": "success"}

        mock_requests.request.side_effect = [mock_401_response, mock_200_response]

        # Mock successful token refresh
        mock_oauth_client.refresh_access_token.return_value = "new_access_token"

        # Make API call
        response = _make_request("GET", "/api/test", access_token="old_token")

        # Verify refresh was called
        mock_oauth_client.refresh_access_token.assert_called_once()

        # Verify second request succeeded
        assert response.status_code == 200

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_token_store_lifecycle(self, mock_keyring: MagicMock) -> None:
        """Test full token storage lifecycle: save -> load -> clear."""
        token_store = TokenStore()

        # Save tokens
        token_store.save_tokens(
            access_token="access_123",
            refresh_token="refresh_456",
            id_token="id_789",
        )

        # Verify tokens were saved
        assert mock_keyring.set_password.call_count == 3

        # Mock loading tokens
        mock_keyring.get_password.side_effect = ["access_123", "refresh_456", "id_789"]

        # Load tokens
        access, refresh, id_token = token_store.load_tokens()

        assert access == "access_123"
        assert refresh == "refresh_456"
        assert id_token == "id_789"

        # Clear tokens
        token_store.clear_tokens()

        # Verify deletion was attempted
        assert mock_keyring.delete_password.call_count == 3


class TestErrorHandling(unittest.TestCase):
    """Integration tests for error handling across components."""

    @patch("synteles_platform_mcp.main.requests")
    @patch("synteles_platform_mcp.main.oauth_client")
    def test_api_error_propagation(
        self,
        mock_oauth_client: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        """Test that API errors are properly propagated."""

        # Mock requests.exceptions module
        class MockRequestException(Exception):
            pass

        mock_requests.exceptions = MagicMock()
        mock_requests.exceptions.RequestException = MockRequestException

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_response.text = '{"error": "Internal Server Error"}'
        mock_requests.request.return_value = mock_response

        with self.assertRaises(PlatformAPIError) as context:
            _make_request("GET", "/api/test", access_token="token")

        assert "500" in str(context.exception)

    @patch("synteles_platform_mcp.main.oauth_client")
    def test_missing_authentication(self, mock_oauth_client: MagicMock) -> None:
        """Test error when trying to make API call without authentication."""
        mock_oauth_client.get_access_token.return_value = None

        with self.assertRaises(PlatformAPIError) as context:
            _make_request("GET", "/api/test")

        assert "authentication required" in str(context.exception).lower()


class TestOAuthClientIntegration(unittest.TestCase):
    """Integration tests for OAuth client with token store."""

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_oauth_client_uses_token_store(self, mock_keyring: MagicMock) -> None:
        """Test that OAuth client properly uses TokenStore."""
        client = OAuthClient(api_domain="api.test.com")

        # Mock tokens in store - get_access_token calls load_tokens which fetches all three
        mock_keyring.get_password.side_effect = [
            "stored_access_token",  # access_token
            "stored_refresh_token",  # refresh_token
            "stored_id_token",  # id_token
        ]

        token = client.get_access_token()

        assert token == "stored_access_token"
        # Verify all three tokens were fetched (implementation calls load_tokens)
        assert mock_keyring.get_password.call_count == 3

    @patch("synteles_platform_mcp.auth.oauth_client.requests")
    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_refresh_updates_token_store(
        self,
        mock_keyring: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        """Test that token refresh updates the token store."""
        client = OAuthClient()

        # Mock refresh token exists
        mock_keyring.get_password.return_value = "old_refresh_token"

        # Mock successful refresh
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
        }
        mock_requests.post.return_value = mock_response

        new_token = client.refresh_access_token()

        # Verify new token returned
        assert new_token == "new_access_token"

        # Verify token store was updated
        assert mock_keyring.set_password.called


class TestEndToEndScenarios(unittest.TestCase):
    """End-to-end scenario tests."""

    @patch("synteles_platform_mcp.main.requests")
    @patch("synteles_platform_mcp.main.oauth_client")
    def test_create_and_list_agentlets(
        self,
        mock_oauth_client: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        """Test creating an agentlet and then listing all agentlets."""
        from synteles_platform_mcp.server import synteles_create_agentlet, synteles_list_agentlets

        org_id = "org-123"

        # Mock create agentlet
        mock_create_response = Mock()
        mock_create_response.status_code = 200
        mock_create_response.json.return_value = {
            "id": "new_agent",
            "description": "Test agent",
        }

        # Mock list agentlets
        mock_list_response = Mock()
        mock_list_response.status_code = 200
        mock_list_response.json.return_value = [
            {"id": "existing_agent"},
            {"id": "new_agent"},
        ]

        mock_requests.request.side_effect = [mock_create_response, mock_list_response]

        # Create agentlet
        created = synteles_create_agentlet(org_id, "new_agent", "Test agent", response_format="json")
        assert created["id"] == "new_agent"

        # List agentlets
        agentlets_result = synteles_list_agentlets(org_id, response_format="json")
        agentlets = agentlets_result["agentlets"]
        assert len(agentlets) == 2
        assert any(a["id"] == "new_agent" for a in agentlets)

    @patch("synteles_platform_mcp.main.requests")
    @patch("synteles_platform_mcp.main.oauth_client")
    def test_create_and_delete_api_key(
        self,
        mock_oauth_client: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        """Test creating and deleting an API key."""
        from synteles_platform_mcp.server import synteles_create_api_key, synteles_delete_api_key

        # Mock create API key
        mock_create_response = Mock()
        mock_create_response.status_code = 200
        mock_create_response.json.return_value = {
            "key_id": "key-123",
            "key": "secret_key",
        }

        # Mock delete API key
        mock_delete_response = Mock()
        mock_delete_response.status_code = 204

        mock_requests.request.side_effect = [mock_create_response, mock_delete_response]

        # Create key
        created = synteles_create_api_key("Test Key", response_format="json")
        key_id = created["key_id"]

        # Delete key
        synteles_delete_api_key(key_id)

        # Verify both requests were made
        assert mock_requests.request.call_count == 2


if __name__ == "__main__":
    unittest.main()
