"""Secure token storage using OS keychain with Windows fallback."""

from __future__ import annotations

import contextlib
import hashlib
import json
import logging
import os
import platform
from pathlib import Path
from typing import TYPE_CHECKING

import keyring

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

SERVICE_NAME = "synteles-platform-mcp"

# Windows-specific imports for fallback storage
_IS_WINDOWS = platform.system() == "Windows"
if _IS_WINDOWS:
    try:
        # Test if cryptography is available for Windows DPAPI fallback
        import cryptography.hazmat.backends
        import cryptography.hazmat.primitives.ciphers  # noqa: F401

        _DPAPI_AVAILABLE = True
    except ImportError:
        _DPAPI_AVAILABLE = False
        logger.warning("cryptography library not available - Windows fallback storage disabled")
else:
    _DPAPI_AVAILABLE = False


class TokenStore:
    """Manages secure storage of OAuth tokens in OS keychain with Windows fallback."""

    def __init__(self) -> None:
        """Initialize token store."""
        self._use_file_storage = False
        self._tokens_file = Path.home() / ".synteles" / "tokens.enc"

    def _get_windows_dpapi_key(self) -> bytes:
        """Get or create a machine-specific encryption key using Windows entropy.

        Returns:
            32-byte encryption key derived from machine-specific data

        """
        # Use a combination of username and machine name as entropy
        # This makes the key machine-specific without storing it
        entropy_data = f"{os.environ.get('USERNAME', 'default')}:{os.environ.get('COMPUTERNAME', 'machine')}"
        # Hash to get consistent 32-byte key
        return hashlib.sha256(entropy_data.encode()).digest()

    def _save_to_file(self, tokens: dict[str, str | None]) -> None:
        """Save tokens to encrypted file (Windows fallback).

        Args:
            tokens: Dictionary of token names to values

        """
        if not _DPAPI_AVAILABLE:
            msg = "Cannot use file storage - cryptography library not available"
            raise RuntimeError(msg)

        # Create directory if needed
        self._tokens_file.parent.mkdir(parents=True, exist_ok=True)

        # Encrypt and save tokens
        from cryptography.hazmat.backends import default_backend  # noqa: PLC0415
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # noqa: PLC0415

        key = self._get_windows_dpapi_key()
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Prepare data
        data = json.dumps(tokens).encode()
        # Pad to block size (16 bytes)
        padding_length = 16 - (len(data) % 16)
        padded_data = data + bytes([padding_length] * padding_length)

        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Save IV + encrypted data
        self._tokens_file.write_bytes(iv + encrypted)
        logger.info("Tokens stored in encrypted file (Windows fallback)")

    def _load_from_file(self) -> dict[str, str | None]:
        """Load tokens from encrypted file (Windows fallback).

        Returns:
            Dictionary of token names to values

        """
        if not _DPAPI_AVAILABLE or not self._tokens_file.exists():
            return {}

        try:
            from cryptography.hazmat.backends import default_backend  # noqa: PLC0415
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # noqa: PLC0415

            key = self._get_windows_dpapi_key()
            encrypted_data = self._tokens_file.read_bytes()

            # Extract IV and encrypted content
            iv = encrypted_data[:16]
            encrypted = encrypted_data[16:]

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            padded_data = decryptor.update(encrypted) + decryptor.finalize()

            # Remove padding
            padding_length = padded_data[-1]
            data = padded_data[:-padding_length]

            return json.loads(data.decode())  # type: ignore[no-any-return]
        except Exception:
            logger.exception("Failed to load tokens from file")
            return {}

    def _clear_file_storage(self) -> None:
        """Remove encrypted tokens file."""
        if self._tokens_file.exists():
            self._tokens_file.unlink()
            logger.info("Encrypted tokens file removed")

    def save_tokens(
        self,
        access_token: str,
        refresh_token: str,
        id_token: str | None = None,
    ) -> None:
        """Store tokens in OS keychain or encrypted file on Windows.

        Args:
            access_token: OAuth access token
            refresh_token: OAuth refresh token
            id_token: Optional OpenID Connect ID token

        """
        # Try keyring first
        if not self._use_file_storage:
            try:
                keyring.set_password(SERVICE_NAME, "access_token", access_token)
                keyring.set_password(SERVICE_NAME, "refresh_token", refresh_token)
                if id_token:
                    keyring.set_password(SERVICE_NAME, "id_token", id_token)
                logger.info("Tokens stored securely in OS keychain")
                return
            except Exception as e:
                # Check if it's a Windows credential size error
                if _IS_WINDOWS and ("1783" in str(e) or "stub received bad data" in str(e).lower()):
                    logger.warning("Windows Credential Manager size limit hit - switching to encrypted file storage")
                    self._use_file_storage = True
                else:
                    # Re-raise if it's a different error
                    raise

        # Fallback to encrypted file storage on Windows
        if _IS_WINDOWS and _DPAPI_AVAILABLE:
            tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "id_token": id_token,
            }
            self._save_to_file(tokens)
        else:
            msg = "Failed to store tokens and no fallback available"
            raise RuntimeError(msg)

    def load_tokens(self) -> tuple[str | None, str | None, str | None]:
        """Retrieve tokens from OS keychain or encrypted file.

        Returns:
            Tuple of (access_token, refresh_token, id_token)

        """
        # Try file storage first if we're using it
        if self._use_file_storage or (_IS_WINDOWS and self._tokens_file.exists()):
            tokens = self._load_from_file()
            if tokens:
                self._use_file_storage = True
                return (
                    tokens.get("access_token"),
                    tokens.get("refresh_token"),
                    tokens.get("id_token"),
                )

        # Try keyring
        try:
            access_token = keyring.get_password(SERVICE_NAME, "access_token")
            refresh_token = keyring.get_password(SERVICE_NAME, "refresh_token")
            id_token = keyring.get_password(SERVICE_NAME, "id_token")
            return access_token, refresh_token, id_token
        except Exception:
            logger.exception("Failed to load tokens from keyring")
            return None, None, None

    def get_access_token(self) -> str | None:
        """Get current access token.

        Returns:
            Access token or None if not found

        """
        access_token, _, _ = self.load_tokens()
        return access_token

    def get_refresh_token(self) -> str | None:
        """Get current refresh token.

        Returns:
            Refresh token or None if not found

        """
        _, refresh_token, _ = self.load_tokens()
        return refresh_token

    def clear_tokens(self) -> None:
        """Remove all tokens from keychain and file storage."""
        # Clear file storage
        self._clear_file_storage()

        # Clear keyring
        for key in ["access_token", "refresh_token", "id_token"]:
            with contextlib.suppress(keyring.errors.PasswordDeleteError):
                keyring.delete_password(SERVICE_NAME, key)

        self._use_file_storage = False
        logger.info("Tokens cleared from all storage locations")

    def has_tokens(self) -> bool:
        """Check if tokens exist.

        Returns:
            True if access token exists, False otherwise

        """
        return self.get_access_token() is not None
