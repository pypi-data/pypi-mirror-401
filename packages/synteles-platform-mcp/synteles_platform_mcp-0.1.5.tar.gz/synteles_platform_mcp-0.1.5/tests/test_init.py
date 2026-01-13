"""Unit tests for package initialization."""

from __future__ import annotations

import unittest


class TestPackageInit(unittest.TestCase):
    """Test cases for package __init__ module."""

    def test_version_exists(self) -> None:
        """Test that package version is defined."""
        from synteles_platform_mcp import __version__

        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_version_format(self) -> None:
        """Test that version follows semantic versioning."""
        from synteles_platform_mcp import __version__

        # Should be in format X.Y.Z or X.Y.Z-suffix
        parts = __version__.split("-")[0].split(".")
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()

    def test_auth_module_imports(self) -> None:
        """Test that auth module exports are accessible."""
        from synteles_platform_mcp.auth import OAuthClient, TokenStore

        assert OAuthClient is not None
        assert TokenStore is not None

    def test_auth_module_all(self) -> None:
        """Test that auth module __all__ is defined correctly."""
        from synteles_platform_mcp import auth

        assert hasattr(auth, "__all__")
        assert "OAuthClient" in auth.__all__
        assert "TokenStore" in auth.__all__


if __name__ == "__main__":
    unittest.main()
