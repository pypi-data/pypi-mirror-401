"""Unit tests for TokenStore class."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from synteles_platform_mcp.auth.token_store import SERVICE_NAME, TokenStore


class TestTokenStore(unittest.TestCase):
    """Test cases for TokenStore class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.token_store = TokenStore()
        self.mock_access_token = "test_access_token_123"
        self.mock_refresh_token = "test_refresh_token_456"
        self.mock_id_token = "test_id_token_789"

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_save_tokens_with_id_token(self, mock_keyring: MagicMock) -> None:
        """Test saving tokens including ID token."""
        self.token_store.save_tokens(
            access_token=self.mock_access_token,
            refresh_token=self.mock_refresh_token,
            id_token=self.mock_id_token,
        )

        # Verify all three tokens were saved
        assert mock_keyring.set_password.call_count == 3
        mock_keyring.set_password.assert_any_call(SERVICE_NAME, "access_token", self.mock_access_token)
        mock_keyring.set_password.assert_any_call(SERVICE_NAME, "refresh_token", self.mock_refresh_token)
        mock_keyring.set_password.assert_any_call(SERVICE_NAME, "id_token", self.mock_id_token)

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_save_tokens_without_id_token(self, mock_keyring: MagicMock) -> None:
        """Test saving tokens without ID token."""
        self.token_store.save_tokens(
            access_token=self.mock_access_token,
            refresh_token=self.mock_refresh_token,
            id_token=None,
        )

        # Verify only access and refresh tokens were saved
        assert mock_keyring.set_password.call_count == 2
        mock_keyring.set_password.assert_any_call(SERVICE_NAME, "access_token", self.mock_access_token)
        mock_keyring.set_password.assert_any_call(SERVICE_NAME, "refresh_token", self.mock_refresh_token)

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_load_tokens(self, mock_keyring: MagicMock) -> None:
        """Test loading tokens from keychain."""
        mock_keyring.get_password.side_effect = [
            self.mock_access_token,
            self.mock_refresh_token,
            self.mock_id_token,
        ]

        access, refresh, id_token = self.token_store.load_tokens()

        assert access == self.mock_access_token
        assert refresh == self.mock_refresh_token
        assert id_token == self.mock_id_token
        assert mock_keyring.get_password.call_count == 3

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_load_tokens_when_missing(self, mock_keyring: MagicMock) -> None:
        """Test loading tokens when they don't exist."""
        mock_keyring.get_password.return_value = None

        access, refresh, id_token = self.token_store.load_tokens()

        assert access is None
        assert refresh is None
        assert id_token is None

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_get_access_token(self, mock_keyring: MagicMock) -> None:
        """Test getting access token."""
        # Mock returns for all three tokens since get_access_token calls load_tokens
        mock_keyring.get_password.side_effect = [
            self.mock_access_token,  # access_token
            self.mock_refresh_token,  # refresh_token
            self.mock_id_token,  # id_token
        ]

        token = self.token_store.get_access_token()

        assert token == self.mock_access_token
        # Verify all three tokens were fetched (implementation calls load_tokens)
        assert mock_keyring.get_password.call_count == 3

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_get_refresh_token(self, mock_keyring: MagicMock) -> None:
        """Test getting refresh token."""
        # Mock returns for all three tokens since get_refresh_token calls load_tokens
        mock_keyring.get_password.side_effect = [
            self.mock_access_token,  # access_token
            self.mock_refresh_token,  # refresh_token
            self.mock_id_token,  # id_token
        ]

        token = self.token_store.get_refresh_token()

        assert token == self.mock_refresh_token
        # Verify all three tokens were fetched (implementation calls load_tokens)
        assert mock_keyring.get_password.call_count == 3

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_clear_tokens(self, mock_keyring: MagicMock) -> None:
        """Test clearing all tokens."""
        self.token_store.clear_tokens()

        # Verify delete_password was called for all three token types
        assert mock_keyring.delete_password.call_count == 3
        mock_keyring.delete_password.assert_any_call(SERVICE_NAME, "access_token")
        mock_keyring.delete_password.assert_any_call(SERVICE_NAME, "refresh_token")
        mock_keyring.delete_password.assert_any_call(SERVICE_NAME, "id_token")

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_clear_tokens_when_not_exist(self, mock_keyring: MagicMock) -> None:
        """Test clearing tokens when they don't exist (no error should be raised)."""
        from unittest.mock import MagicMock

        # Create a mock exception class that inherits from BaseException
        class MockPasswordDeleteError(Exception):
            pass

        # Patch the keyring.errors module
        mock_keyring.errors = MagicMock()
        mock_keyring.errors.PasswordDeleteError = MockPasswordDeleteError
        mock_keyring.delete_password.side_effect = MockPasswordDeleteError("Token not found")

        # Should not raise an exception
        self.token_store.clear_tokens()

        assert mock_keyring.delete_password.call_count == 3

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_has_tokens_when_exists(self, mock_keyring: MagicMock) -> None:
        """Test has_tokens when token exists."""
        # Mock returns for all three tokens since has_tokens calls get_access_token -> load_tokens
        mock_keyring.get_password.side_effect = [
            self.mock_access_token,  # access_token
            self.mock_refresh_token,  # refresh_token
            self.mock_id_token,  # id_token
        ]

        result = self.token_store.has_tokens()

        assert result is True
        # Verify all three tokens were fetched (implementation calls load_tokens)
        assert mock_keyring.get_password.call_count == 3

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_has_tokens_when_missing(self, mock_keyring: MagicMock) -> None:
        """Test has_tokens when token doesn't exist."""
        mock_keyring.get_password.return_value = None

        result = self.token_store.has_tokens()

        assert result is False

    @patch("synteles_platform_mcp.auth.token_store.keyring")
    def test_service_name_constant(self, mock_keyring: MagicMock) -> None:
        """Test that the correct service name is used."""
        self.token_store.save_tokens(
            access_token="test",
            refresh_token="test",
        )

        # Verify service name is correct
        calls = mock_keyring.set_password.call_args_list
        for call in calls:
            assert call[0][0] == "synteles-platform-mcp"


if __name__ == "__main__":
    unittest.main()
