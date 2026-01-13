"""Pytest configuration and shared fixtures.

This file is automatically loaded by pytest and provides
shared fixtures and configuration for all tests.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Generator


# Configure logging for tests
logging.basicConfig(
    level=logging.WARNING,  # Reduce noise during tests
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@pytest.fixture
def mock_api_domain() -> str:
    """Fixture providing a mock API domain for testing."""
    return "api.test.example.com"


@pytest.fixture
def mock_tokens() -> dict[str, str]:
    """Fixture providing mock OAuth tokens."""
    return {
        "access_token": "mock_access_token_123456",
        "refresh_token": "mock_refresh_token_789012",
        "id_token": "mock_id_token_345678",
    }


@pytest.fixture
def mock_org_id() -> str:
    """Fixture providing a mock organization ID."""
    return "org-test-123"


@pytest.fixture
def mock_user_data() -> dict[str, str]:
    """Fixture providing mock user data."""
    return {
        "sub": "user-uuid-123",
        "email": "test@example.com",
        "name": "Test User",
        "given_name": "Test",
        "family_name": "User",
        "org_id": "org-test-123",
        "org_name": "Test Organization",
    }


@pytest.fixture
def mock_agentlet_data() -> dict[str, str]:
    """Fixture providing mock agentlet data."""
    return {
        "id": "test_agentlet",
        "description": "Test agentlet for unit tests",
        "YAML": "agentlet:\n  name: TestAgent\n  version: 1.0",
        "created_at": "2025-12-01T10:00:00.000000+00:00",
        "updated_at": "2025-12-01T10:00:00.000000+00:00",
    }


@pytest.fixture
def mock_api_key_data() -> dict[str, str]:
    """Fixture providing mock API key data."""
    return {
        "key_id": "key-uuid-123",
        "key": "base64url_encoded_key_43_characters_long",
        "key_name": "Test API Key",
        "created_at": "2025-12-01T10:00:00.000000+00:00",
    }


@pytest.fixture(autouse=True)
def reset_callback_handler() -> Generator[None, None, None]:
    """Fixture to reset CallbackHandler class variables before each test."""
    from synteles_platform_mcp.auth.oauth_client import CallbackHandler

    # Reset before test
    CallbackHandler.auth_code = None
    CallbackHandler.auth_error = None

    yield

    # Clean up after test
    CallbackHandler.auth_code = None
    CallbackHandler.auth_error = None


@pytest.fixture
def mock_oauth_callback_port() -> int:
    """Fixture providing a mock OAuth callback port."""
    return 8888
