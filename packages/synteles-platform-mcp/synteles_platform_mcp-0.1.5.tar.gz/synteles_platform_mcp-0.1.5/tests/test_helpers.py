"""Test helper utilities and common test functions."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

if TYPE_CHECKING:
    from typing import Any


def create_mock_response(
    status_code: int,
    json_data: dict[str, Any] | None = None,
    text: str | None = None,
) -> Mock:
    """Create a mock requests.Response object.

    Args:
        status_code: HTTP status code
        json_data: Optional JSON response data
        text: Optional response text

    Returns:
        Mock Response object

    """
    mock_response = Mock()
    mock_response.status_code = status_code

    if json_data is not None:
        mock_response.json.return_value = json_data
        if text is None:
            import json

            text = json.dumps(json_data)

    if text is not None:
        mock_response.text = text

    return mock_response


def create_mock_oauth_login_flow() -> tuple[Mock, Mock]:
    """Create mock responses for OAuth login flow.

    Returns:
        Tuple of (login_response, token_response) mocks

    """
    login_response = create_mock_response(
        status_code=200,
        json_data={"authorization_url": "https://auth.example.com/oauth/authorize"},
    )

    token_response = create_mock_response(
        status_code=200,
        json_data={
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600,
            "token_type": "Bearer",
        },
    )

    return login_response, token_response


def create_mock_oauth_refresh_flow() -> Mock:
    """Create mock response for OAuth token refresh.

    Returns:
        Mock refresh response

    """
    return create_mock_response(
        status_code=200,
        json_data={
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
        },
    )


def assert_mock_called_with_bearer_token(mock_call: Any, expected_token: str) -> None:
    """Assert that a mock was called with correct Bearer token header.

    Args:
        mock_call: Mock call object to check
        expected_token: Expected token value

    """
    # Check if headers contain Authorization with Bearer token
    call_kwargs = mock_call.kwargs if hasattr(mock_call, "kwargs") else {}
    headers = call_kwargs.get("headers", {})

    expected_auth = f"Bearer {expected_token}"
    actual_auth = headers.get("Authorization", "")

    assert actual_auth == expected_auth, f"Expected Bearer token {expected_token}, got {actual_auth}"


def create_mock_agentlet(
    agentlet_id: str = "test_agentlet",
    description: str = "Test agentlet",
    yaml_content: str | None = None,
) -> dict[str, str]:
    """Create mock agentlet data.

    Args:
        agentlet_id: Agentlet identifier
        description: Agentlet description
        yaml_content: Optional YAML content

    Returns:
        Mock agentlet dictionary

    """
    if yaml_content is None:
        yaml_content = f"agentlet:\n  name: {agentlet_id}\n  version: 1.0"

    return {
        "id": agentlet_id,
        "description": description,
        "YAML": yaml_content,
        "created_at": "2025-12-01T10:00:00.000000+00:00",
        "updated_at": "2025-12-01T10:00:00.000000+00:00",
    }


def create_mock_api_key(
    key_id: str = "key-123",
    key_name: str = "Test Key",
    include_key_value: bool = False,
) -> dict[str, str]:
    """Create mock API key data.

    Args:
        key_id: API key UUID
        key_name: API key name
        include_key_value: Whether to include the actual key value (only on creation)

    Returns:
        Mock API key dictionary

    """
    data = {
        "key_id": key_id,
        "key_name": key_name,
        "created_at": "2025-12-01T10:00:00.000000+00:00",
        "last_used": None,
    }

    if include_key_value:
        data["key"] = "base64url_encoded_secret_key_43_chars_long"

    return data


def create_mock_user(
    sub: str = "user-123",
    email: str = "test@example.com",
    org_id: str | None = "org-123",
) -> dict[str, Any]:
    """Create mock user data.

    Args:
        sub: User Cognito UUID
        email: User email
        org_id: Optional organization ID

    Returns:
        Mock user dictionary

    """
    data = {
        "sub": sub,
        "email": email,
        "name": "Test User",
        "given_name": "Test",
        "family_name": "User",
        "picture": "https://example.com/avatar.jpg",
    }

    if org_id:
        data["org_id"] = org_id
        data["org_name"] = "Test Organization"

    return data


def create_mock_organization(
    org_name: str = "Test Organization",
    user_count: int = 3,
) -> dict[str, Any]:
    """Create mock organization data.

    Args:
        org_name: Organization name
        user_count: Number of users in organization

    Returns:
        Mock organization dictionary

    """
    return {
        "org_name": org_name,
        "users": [f"user-{i}" for i in range(user_count)],
    }


class MockHTTPServer:
    """Mock HTTP server for testing OAuth callback."""

    def __init__(self) -> None:
        """Initialize mock server."""
        self.closed = False

    def server_close(self) -> None:
        """Mock server close method."""
        self.closed = True

    def handle_request(self) -> None:
        """Mock handle request method."""
        pass


class MockThread:
    """Mock threading.Thread for testing."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize mock thread."""
        self.started = False
        self.daemon = False

    def start(self) -> None:
        """Mock thread start."""
        self.started = True

    def join(self, timeout: float | None = None) -> None:
        """Mock thread join."""
        pass
