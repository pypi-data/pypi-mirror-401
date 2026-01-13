"""Unit tests for main MCP server module."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, Mock, patch

from synteles_platform_mcp.server import (
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    PlatformAPIError,
    _format_elapsed_time,
    _format_execution_status_for_display,
    _make_request,
    synteles_auth_status,
    synteles_create_agentlet,
    synteles_create_agentlet_execution,
    synteles_create_api_key,
    synteles_delete_agentlet,
    synteles_delete_api_key,
    synteles_get_agentlet,
    synteles_get_current_user,
    synteles_get_execution_logs,
    get_execution_resource,
    synteles_get_execution_status,
    synteles_get_organization,
    synteles_list_agentlets,
    synteles_list_api_keys,
    synteles_list_executions,
    synteles_login,
    synteles_logout,
    synteles_terminate_execution,
    synteles_update_agentlet,
)


class TestMakeRequest(unittest.TestCase):
    """Test cases for _make_request helper function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_token = "test_access_token"
        self.endpoint = "/api/test"

    @patch("synteles_platform_mcp.main.requests")
    @patch("synteles_platform_mcp.main.oauth_client")
    def test_make_request_success(self, mock_oauth_client: MagicMock, mock_requests: MagicMock) -> None:
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_requests.request.return_value = mock_response

        response = _make_request("GET", self.endpoint, access_token=self.mock_token)

        assert response.status_code == 200
        assert response.json() == {"data": "test"}

    @patch("synteles_platform_mcp.main.requests")
    @patch("synteles_platform_mcp.main.oauth_client")
    def test_make_request_uses_oauth_token_when_not_provided(
        self, mock_oauth_client: MagicMock, mock_requests: MagicMock
    ) -> None:
        """Test that OAuth token is used when access_token not provided."""
        mock_oauth_client.get_access_token.return_value = "oauth_token"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.request.return_value = mock_response

        _make_request("GET", self.endpoint)

        # Verify OAuth client was called to get token
        mock_oauth_client.get_access_token.assert_called_once()

    @patch("synteles_platform_mcp.main.oauth_client")
    def test_make_request_no_token_raises_error(self, mock_oauth_client: MagicMock) -> None:
        """Test that error is raised when no token is available."""
        mock_oauth_client.get_access_token.return_value = None

        with self.assertRaises(PlatformAPIError) as context:
            _make_request("GET", self.endpoint)

        assert "authentication required" in str(context.exception).lower()

    @patch("synteles_platform_mcp.main.requests")
    @patch("synteles_platform_mcp.main.oauth_client")
    def test_make_request_401_triggers_refresh(self, mock_oauth_client: MagicMock, mock_requests: MagicMock) -> None:
        """Test that 401 response triggers token refresh."""
        # First request returns 401
        mock_response_401 = Mock()
        mock_response_401.status_code = HTTP_401_UNAUTHORIZED

        # Second request (after refresh) returns 200
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {"data": "success"}

        mock_requests.request.side_effect = [mock_response_401, mock_response_200]
        mock_oauth_client.refresh_access_token.return_value = "new_token"

        response = _make_request("GET", self.endpoint, access_token="old_token")

        # Verify refresh was called
        mock_oauth_client.refresh_access_token.assert_called_once()

        # Verify second request succeeded
        assert response.status_code == 200

    @patch("synteles_platform_mcp.main.requests")
    @patch("synteles_platform_mcp.main.oauth_client")
    def test_make_request_401_failed_refresh(self, mock_oauth_client: MagicMock, mock_requests: MagicMock) -> None:
        """Test that failed refresh raises error."""

        # Mock requests.exceptions module
        class MockRequestException(Exception):
            pass

        mock_requests.exceptions = MagicMock()
        mock_requests.exceptions.RequestException = MockRequestException

        mock_response = Mock()
        mock_response.status_code = HTTP_401_UNAUTHORIZED
        mock_requests.request.return_value = mock_response
        mock_oauth_client.refresh_access_token.return_value = None

        with self.assertRaises(PlatformAPIError) as context:
            _make_request("GET", self.endpoint, access_token="old_token")

        assert "refresh failed" in str(context.exception).lower()

    @patch("synteles_platform_mcp.main.requests")
    def test_make_request_404_error(self, mock_requests: MagicMock) -> None:
        """Test handling of 404 error."""

        # Mock requests.exceptions module
        class MockRequestException(Exception):
            pass

        mock_requests.exceptions = MagicMock()
        mock_requests.exceptions.RequestException = MockRequestException

        mock_response = Mock()
        mock_response.status_code = HTTP_404_NOT_FOUND
        mock_response.json.return_value = {"error": "Not found"}
        mock_response.text = '{"error": "Not found"}'
        mock_requests.request.return_value = mock_response

        with self.assertRaises(PlatformAPIError) as context:
            _make_request("GET", self.endpoint, access_token=self.mock_token)

        assert "404" in str(context.exception)

    @patch("synteles_platform_mcp.main.requests")
    def test_make_request_network_error(self, mock_requests: MagicMock) -> None:
        """Test handling of network errors."""

        # Create a proper exception instance
        class MockConnectionError(Exception):
            pass

        # Mock the requests module exceptions
        mock_requests.exceptions = MagicMock()
        mock_requests.exceptions.RequestException = MockConnectionError
        mock_requests.exceptions.ConnectionError = MockConnectionError

        mock_requests.request.side_effect = MockConnectionError("Network error")

        with self.assertRaises(PlatformAPIError) as context:
            _make_request("GET", self.endpoint, access_token=self.mock_token)

        assert "request failed" in str(context.exception).lower()


class TestAuthenticationTools(unittest.TestCase):
    """Test cases for authentication MCP tools."""

    @patch("synteles_platform_mcp.main.oauth_client")
    def test_login_success(self, mock_oauth_client: MagicMock) -> None:
        """Test successful login."""
        mock_oauth_client.login.return_value = {
            "status": "success",
            "message": "Successfully authenticated",
            "expires_in": 3600,
        }

        result = synteles_login()

        assert result["status"] == "success"
        mock_oauth_client.login.assert_called_once()

    @patch("synteles_platform_mcp.main.oauth_client")
    def test_login_with_custom_port(self, mock_oauth_client: MagicMock) -> None:
        """Test login with custom callback port."""
        mock_oauth_client.login.return_value = {"status": "success"}

        synteles_login(callback_port=9999)

        mock_oauth_client.login.assert_called_once_with(callback_port=9999, timeout=120)

    @patch("synteles_platform_mcp.main.oauth_client")
    def test_login_failure(self, mock_oauth_client: MagicMock) -> None:
        """Test login failure."""
        mock_oauth_client.login.side_effect = Exception("Login failed")

        with self.assertRaises(PlatformAPIError):
            synteles_login()

    @patch("synteles_platform_mcp.main.oauth_client")
    def test_logout_success(self, mock_oauth_client: MagicMock) -> None:
        """Test successful logout."""
        mock_oauth_client.logout.return_value = {
            "status": "success",
            "message": "Logged out successfully",
        }

        result = synteles_logout()

        assert result["status"] == "success"
        mock_oauth_client.logout.assert_called_once()

    @patch("synteles_platform_mcp.main.token_store")
    def test_auth_status_authenticated(self, mock_token_store: MagicMock) -> None:
        """Test auth status when authenticated."""
        mock_token_store.get_access_token.return_value = "test_token"
        mock_token_store.get_refresh_token.return_value = "test_refresh"

        result = synteles_auth_status()

        assert result["authenticated"] is True
        assert result["has_access_token"] is True
        assert result["has_refresh_token"] is True

    @patch("synteles_platform_mcp.main.token_store")
    def test_auth_status_not_authenticated(self, mock_token_store: MagicMock) -> None:
        """Test auth status when not authenticated."""
        mock_token_store.get_access_token.return_value = None
        mock_token_store.get_refresh_token.return_value = None

        result = synteles_auth_status()

        assert result["authenticated"] is False
        assert result["has_access_token"] is False
        assert result["has_refresh_token"] is False


class TestUserTools(unittest.TestCase):
    """Test cases for user-related MCP tools."""

    @patch("synteles_platform_mcp.main._make_request")
    def test_get_current_user_success(self, mock_make_request: MagicMock) -> None:
        """Test getting current user."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "sub": "user-123",
            "email": "test@example.com",
            "name": "Test User",
        }
        mock_make_request.return_value = mock_response

        result = synteles_get_current_user(response_format="json")

        assert result["sub"] == "user-123"
        assert result["email"] == "test@example.com"
        mock_make_request.assert_called_once_with("GET", "/api/users/me", access_token=None)


class TestOrganizationTools(unittest.TestCase):
    """Test cases for organization-related MCP tools."""

    @patch("synteles_platform_mcp.main._make_request")
    def test_get_organization_success(self, mock_make_request: MagicMock) -> None:
        """Test getting organization."""
        org_id = "org-123"
        mock_response = Mock()
        mock_response.json.return_value = {
            "org_name": "Test Org",
            "users": ["user-1", "user-2"],
        }
        mock_make_request.return_value = mock_response

        result = synteles_get_organization(org_id, response_format="json")

        assert result["org_name"] == "Test Org"
        assert len(result["users"]) == 2
        mock_make_request.assert_called_once_with("GET", f"/api/organizations/{org_id}", access_token=None)


class TestAgentletTools(unittest.TestCase):
    """Test cases for agentlet-related MCP tools."""

    @patch("synteles_platform_mcp.main._make_request")
    def test_create_agentlet_success(self, mock_make_request: MagicMock) -> None:
        """Test creating an agentlet."""
        org_id = "org-123"
        agentlet_id = "my_agent"
        description = "Test agent"
        yaml_def = "agentlet:\n  name: Test"

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": agentlet_id,
            "description": description,
            "YAML": yaml_def,
        }
        mock_make_request.return_value = mock_response

        result = synteles_create_agentlet(org_id, agentlet_id, description, yaml_def, response_format="json")

        assert result["id"] == agentlet_id
        assert result["description"] == description
        mock_make_request.assert_called_once()

    @patch("synteles_platform_mcp.main._make_request")
    def test_list_agentlets_success(self, mock_make_request: MagicMock) -> None:
        """Test listing agentlets."""
        org_id = "org-123"
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": "agent1", "description": "First agent"},
            {"id": "agent2", "description": "Second agent"},
        ]
        mock_make_request.return_value = mock_response

        result = synteles_list_agentlets(org_id, response_format="json")

        # Result is paginated now
        assert result["count"] == 2
        assert result["agentlets"][0]["id"] == "agent1"

    @patch("synteles_platform_mcp.main._make_request")
    def test_get_agentlet_success(self, mock_make_request: MagicMock) -> None:
        """Test getting agentlet details."""
        org_id = "org-123"
        agentlet_id = "my_agent"

        mock_response = Mock()
        mock_response.json.return_value = {
            "description": "Test agent",
            "YAML": "agentlet:\n  name: Test",
        }
        mock_make_request.return_value = mock_response

        result = synteles_get_agentlet(org_id, agentlet_id, response_format="json")

        assert "description" in result
        assert "YAML" in result

    @patch("synteles_platform_mcp.main._make_request")
    def test_update_agentlet_success(self, mock_make_request: MagicMock) -> None:
        """Test updating an agentlet."""
        org_id = "org-123"
        agentlet_id = "my_agent"
        new_description = "Updated description"

        mock_response = Mock()
        mock_response.json.return_value = {"message": "Agentlet updated"}
        mock_make_request.return_value = mock_response

        result = synteles_update_agentlet(org_id, agentlet_id, description=new_description)

        assert "message" in result

    @patch("synteles_platform_mcp.main._make_request")
    def test_delete_agentlet_success(self, mock_make_request: MagicMock) -> None:
        """Test deleting an agentlet."""
        org_id = "org-123"
        agentlet_id = "my_agent"

        synteles_delete_agentlet(org_id, agentlet_id)

        mock_make_request.assert_called_once_with(
            "DELETE",
            f"/api/organizations/{org_id}/agentlets/{agentlet_id}",
            access_token=None,
        )


class TestAPIKeyTools(unittest.TestCase):
    """Test cases for API key management MCP tools."""

    @patch("synteles_platform_mcp.main._make_request")
    def test_create_api_key_success(self, mock_make_request: MagicMock) -> None:
        """Test creating an API key."""
        key_name = "Test Key"
        mock_response = Mock()
        mock_response.json.return_value = {
            "key_id": "key-123",
            "key": "abc123def456",
            "key_name": key_name,
        }
        mock_make_request.return_value = mock_response

        result = synteles_create_api_key(key_name, response_format="json")

        assert result["key_name"] == key_name
        assert "key" in result

    @patch("synteles_platform_mcp.main._make_request")
    def test_list_api_keys_success(self, mock_make_request: MagicMock) -> None:
        """Test listing API keys."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"key_id": "key-1", "key_name": "Key 1"},
            {"key_id": "key-2", "key_name": "Key 2"},
        ]
        mock_make_request.return_value = mock_response

        result = synteles_list_api_keys(response_format="json")

        # Result is paginated now
        assert result["count"] == 2
        assert result["api_keys"][0]["key_id"] == "key-1"

    @patch("synteles_platform_mcp.main._make_request")
    def test_delete_api_key_success(self, mock_make_request: MagicMock) -> None:
        """Test deleting an API key."""
        key_id = "key-123"

        synteles_delete_api_key(key_id)

        mock_make_request.assert_called_once_with(
            "DELETE",
            f"/api/users/apikeys/{key_id}",
            access_token=None,
        )


class TestHTTPStatusConstants(unittest.TestCase):
    """Test cases for HTTP status code constants."""

    def test_http_status_constants(self) -> None:
        """Test that HTTP status constants are defined correctly."""
        assert HTTP_400_BAD_REQUEST == 400
        assert HTTP_401_UNAUTHORIZED == 401
        assert HTTP_404_NOT_FOUND == 404


class TestPlatformAPIError(unittest.TestCase):
    """Test cases for PlatformAPIError exception."""

    def test_platform_api_error_is_exception(self) -> None:
        """Test that PlatformAPIError is an Exception."""
        error = PlatformAPIError("Test error")
        assert isinstance(error, Exception)

    def test_platform_api_error_message(self) -> None:
        """Test that PlatformAPIError stores message correctly."""
        message = "Test error message"
        error = PlatformAPIError(message)
        assert str(error) == message


class TestExecutionTools(unittest.TestCase):
    """Test cases for execution/scheduler tools."""

    @patch("synteles_platform_mcp.main._make_request")
    def test_create_agentlet_execution_success(self, mock_make_request: MagicMock) -> None:
        """Test creating an agentlet execution."""
        org_id = "org-123"
        agentlet_id = "my_agentlet"
        execution_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_response = Mock()
        mock_response.json.return_value = {
            "execution_id": execution_id,
            "status": "running",
            "agentlet_id": agentlet_id,
            "cloud_provider": "gcp",
            "created_at": "2025-12-13T10:30:45Z",
        }
        mock_make_request.return_value = mock_response

        result = synteles_create_agentlet_execution(
            org_id=org_id,
            agentlet_id=agentlet_id,
            cloud_provider="gcp",
            prompt="Test prompt",
            timeout=1800,
            response_format="json",
        )

        assert result["execution_id"] == execution_id
        assert result["status"] == "running"
        assert result["agentlet_id"] == agentlet_id
        mock_make_request.assert_called_once_with(
            "POST",
            f"/api/organizations/{org_id}/agentlets/{agentlet_id}/executions",
            access_token=None,
            json_data={
                "cloud_provider": "gcp",
                "prompt": "Test prompt",
                "timeout": 1800,
            },
        )

    @patch("synteles_platform_mcp.main._make_request")
    def test_create_agentlet_execution_defaults(self, mock_make_request: MagicMock) -> None:
        """Test creating an agentlet execution with default parameters."""
        org_id = "org-123"
        agentlet_id = "my_agentlet"

        mock_response = Mock()
        mock_response.json.return_value = {
            "execution_id": "exec-123",
            "status": "deploying",
            "agentlet_id": agentlet_id,
            "cloud_provider": "gcp",
            "created_at": "2025-12-13T10:30:45Z",
        }
        mock_make_request.return_value = mock_response

        synteles_create_agentlet_execution(org_id=org_id, agentlet_id=agentlet_id)

        # Verify default values are used
        call_args = mock_make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["cloud_provider"] == "gcp"
        assert json_data["timeout"] == 3600
        assert "prompt" not in json_data

    @patch("synteles_platform_mcp.main._make_request")
    def test_get_execution_status_running(self, mock_make_request: MagicMock) -> None:
        """Test getting execution status when running."""
        execution_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_response = Mock()
        mock_response.json.return_value = {
            "execution_id": execution_id,
            "agentlet_id": "my_agentlet",
            "cloud_provider": "gcp",
            "status": "running",
            "created_at": "2025-12-13T10:30:45Z",
            "updated_at": "2025-12-13T10:31:00Z",
            "elapsed_seconds": 15,
        }
        mock_make_request.return_value = mock_response

        result = synteles_get_execution_status(execution_id, response_format="json")

        assert result["execution_id"] == execution_id
        assert result["status"] == "running"
        assert result["elapsed_seconds"] == 15
        mock_make_request.assert_called_once_with(
            "GET",
            f"/api/executions/{execution_id}/status",
            access_token=None,
        )

    @patch("synteles_platform_mcp.main._make_request")
    def test_get_execution_status_completed(self, mock_make_request: MagicMock) -> None:
        """Test getting execution status when completed."""
        execution_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_response = Mock()
        mock_response.json.return_value = {
            "execution_id": execution_id,
            "agentlet_id": "my_agentlet",
            "cloud_provider": "gcp",
            "status": "completed",
            "logs_s3_uri": "s3://bucket/executions/550e8400/logs.txt",
            "created_at": "2025-12-13T10:30:45Z",
            "completed_at": "2025-12-13T10:35:50Z",
            "elapsed_seconds": 305,
        }
        mock_make_request.return_value = mock_response

        result = synteles_get_execution_status(execution_id, response_format="json")

        assert result["status"] == "completed"
        assert result["logs_s3_uri"] == "s3://bucket/executions/550e8400/logs.txt"
        assert result["elapsed_seconds"] == 305

    @patch("synteles_platform_mcp.main._make_request")
    def test_get_execution_logs_text_format(self, mock_make_request: MagicMock) -> None:
        """Test getting execution logs in text format."""
        execution_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_response = Mock()
        mock_response.status_code = HTTP_200_OK
        mock_response.text = "[2025-12-13T10:30:45.123Z] [INFO] Container started\n"
        mock_response.headers = {
            "X-Execution-Status": "completed",
            "X-S3-Uri": "s3://bucket/executions/550e8400/logs.txt",
        }
        mock_make_request.return_value = mock_response

        result = synteles_get_execution_logs(execution_id, log_format="text")

        assert result["execution_id"] == execution_id
        assert result["status"] == "completed"
        assert result["logs_available"] is True
        assert "Container started" in result["logs_text"]
        mock_make_request.assert_called_once_with(
            "GET",
            f"/api/executions/{execution_id}/logs",
            access_token=None,
            params={},
        )

    @patch("synteles_platform_mcp.main._make_request")
    def test_get_execution_logs_json_format(self, mock_make_request: MagicMock) -> None:
        """Test getting execution logs in JSON format."""
        execution_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_response = Mock()
        mock_response.status_code = HTTP_202_ACCEPTED
        mock_response.json.return_value = {
            "execution_id": execution_id,
            "status": "completed",
            "logs_available": True,
            "s3_uri": "s3://bucket/executions/550e8400/logs.txt",
            "log_size_bytes": 2048,
            "logs": [
                {
                    "timestamp": "2025-12-13T10:30:45.123Z",
                    "severity": "INFO",
                    "message": "Container started",
                }
            ],
        }
        mock_make_request.return_value = mock_response

        result = synteles_get_execution_logs(execution_id, log_format="json")

        assert result["logs_available"] is True
        assert len(result["logs"]) == 1
        assert result["logs"][0]["message"] == "Container started"
        mock_make_request.assert_called_once_with(
            "GET",
            f"/api/executions/{execution_id}/logs",
            access_token=None,
            params={"format": "json"},
        )

    @patch("synteles_platform_mcp.main._make_request")
    def test_get_execution_logs_with_download(self, mock_make_request: MagicMock) -> None:
        """Test getting execution logs with download flag."""
        execution_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_response = Mock()
        mock_response.status_code = HTTP_200_OK
        mock_response.text = "Log content"
        mock_response.headers = {
            "X-Execution-Status": "completed",
            "X-S3-Uri": "s3://bucket/logs.txt",
        }
        mock_make_request.return_value = mock_response

        synteles_get_execution_logs(execution_id, log_format="text", download=True)

        call_args = mock_make_request.call_args
        params = call_args[1]["params"]
        assert params["download"] == "true"

    @patch("synteles_platform_mcp.main._make_request")
    def test_terminate_execution_success(self, mock_make_request: MagicMock) -> None:
        """Test terminating an execution."""
        execution_id = "550e8400-e29b-41d4-a716-446655440000"

        mock_response = Mock()
        mock_response.json.return_value = {
            "execution_id": execution_id,
            "status": "terminated",
            "terminated_at": "2025-12-13T10:40:00Z",
        }
        mock_make_request.return_value = mock_response

        result = synteles_terminate_execution(execution_id, response_format="json")

        assert result["execution_id"] == execution_id
        assert result["status"] == "terminated"
        mock_make_request.assert_called_once_with(
            "DELETE",
            f"/api/executions/{execution_id}",
            access_token=None,
        )

    @patch("synteles_platform_mcp.main._make_request")
    def test_list_executions_no_filters(self, mock_make_request: MagicMock) -> None:
        """Test listing executions without filters."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "executions": [
                {
                    "execution_id": "exec-1",
                    "agentlet_id": "agentlet1",
                    "status": "completed",
                    "cloud_provider": "gcp",
                    "created_at": "2025-12-13T10:30:45Z",
                    "completed_at": "2025-12-13T10:35:50Z",
                    "elapsed_seconds": 305,
                }
            ],
            "count": 1,
        }
        mock_make_request.return_value = mock_response

        result = synteles_list_executions(response_format="json")

        assert result["count"] == 1
        assert len(result["executions"]) == 1
        mock_make_request.assert_called_once_with(
            "GET",
            "/api/executions",
            access_token=None,
            params={},
        )

    @patch("synteles_platform_mcp.main._make_request")
    def test_list_executions_with_filters(self, mock_make_request: MagicMock) -> None:
        """Test listing executions with filters."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "executions": [],
            "count": 0,
        }
        mock_make_request.return_value = mock_response

        synteles_list_executions(
            agentlet_id="my_agentlet",
            status="completed",
            limit=10,
            next_token="token123",
            response_format="json",
        )

        call_args = mock_make_request.call_args
        params = call_args[1]["params"]
        assert params["agentlet_id"] == "my_agentlet"
        assert params["status"] == "completed"
        assert params["limit"] == "10"
        assert params["next_token"] == "token123"

    @patch("synteles_platform_mcp.main._make_request")
    def test_list_executions_with_date_filters(self, mock_make_request: MagicMock) -> None:
        """Test listing executions with date filters."""
        mock_response = Mock()
        mock_response.json.return_value = {"executions": [], "count": 0}
        mock_make_request.return_value = mock_response

        synteles_list_executions(
            created_at_start="2025-12-01T00:00:00Z",
            created_at_end="2025-12-31T23:59:59Z",
            response_format="json",
        )

        call_args = mock_make_request.call_args
        params = call_args[1]["params"]
        assert params["created_at_start"] == "2025-12-01T00:00:00Z"
        assert params["created_at_end"] == "2025-12-31T23:59:59Z"


class TestExecutionHelpers(unittest.TestCase):
    """Test cases for execution helper functions."""

    def test_format_elapsed_time_seconds(self) -> None:
        """Test formatting elapsed time in seconds."""
        assert _format_elapsed_time(30) == "30s"
        assert _format_elapsed_time(59) == "59s"

    def test_format_elapsed_time_minutes(self) -> None:
        """Test formatting elapsed time in minutes and seconds."""
        assert _format_elapsed_time(60) == "1m 0s"
        assert _format_elapsed_time(90) == "1m 30s"
        assert _format_elapsed_time(135) == "2m 15s"
        assert _format_elapsed_time(3599) == "59m 59s"

    def test_format_elapsed_time_hours(self) -> None:
        """Test formatting elapsed time in hours and minutes."""
        assert _format_elapsed_time(3600) == "1h 0m"
        assert _format_elapsed_time(3660) == "1h 1m"
        assert _format_elapsed_time(7200) == "2h 0m"
        assert _format_elapsed_time(7380) == "2h 3m"

    def test_format_execution_status_deploying(self) -> None:
        """Test formatting deploying status."""
        status_data = {
            "execution_id": "exec-123",
            "agentlet_id": "my_agentlet",
            "status": "deploying",
            "elapsed_seconds": 15,
        }
        result = _format_execution_status_for_display(status_data)

        assert "🚀" in result
        assert "Deploying" in result
        assert "my_agentlet" in result
        assert "15s" in result

    def test_format_execution_status_running(self) -> None:
        """Test formatting running status."""
        status_data = {
            "execution_id": "exec-123",
            "agentlet_id": "my_agentlet",
            "status": "running",
            "cloud_provider": "gcp",
            "elapsed_seconds": 90,
        }
        result = _format_execution_status_for_display(status_data)

        assert "⚙️" in result
        assert "running" in result.lower() or "processing" in result.lower()
        assert "my_agentlet" in result
        assert "1m 30s" in result
        assert "gcp" in result

    def test_format_execution_status_completed(self) -> None:
        """Test formatting completed status."""
        status_data = {
            "execution_id": "exec-123",
            "agentlet_id": "my_agentlet",
            "status": "completed",
            "logs_s3_uri": "s3://bucket/logs.txt",
            "elapsed_seconds": 305,
        }
        result = _format_execution_status_for_display(status_data)

        assert "✅" in result
        assert "completed" in result.lower()
        assert "my_agentlet" in result
        assert "5m 5s" in result
        assert "s3://bucket/logs.txt" in result

    def test_format_execution_status_failed(self) -> None:
        """Test formatting failed status."""
        status_data = {
            "execution_id": "exec-123",
            "agentlet_id": "my_agentlet",
            "status": "failed",
            "error": "Container failed to start",
            "elapsed_seconds": 120,
        }
        result = _format_execution_status_for_display(status_data)

        assert "❌" in result
        assert "failed" in result.lower()
        assert "my_agentlet" in result
        assert "2m 0s" in result
        assert "Container failed to start" in result

    def test_format_execution_status_terminated(self) -> None:
        """Test formatting terminated status."""
        status_data = {
            "execution_id": "exec-123",
            "agentlet_id": "my_agentlet",
            "status": "terminated",
            "terminated_at": "2025-12-13T10:40:00Z",
            "elapsed_seconds": 45,
        }
        result = _format_execution_status_for_display(status_data)

        assert "⚠️" in result
        assert "terminated" in result.lower()
        assert "my_agentlet" in result
        assert "45s" in result


class TestExecutionResources(unittest.TestCase):
    """Test cases for execution MCP resources."""

    @patch("synteles_platform_mcp.main.synteles_get_execution_status")
    def test_get_execution_resource_success(self, mock_get_status: MagicMock) -> None:
        """Test getting execution resource successfully."""
        execution_id = "exec-123"
        mock_get_status.return_value = {
            "execution_id": execution_id,
            "agentlet_id": "my_agentlet",
            "status": "running",
            "cloud_provider": "gcp",
            "elapsed_seconds": 30,
        }

        result = get_execution_resource(execution_id)

        assert isinstance(result, str)
        assert "running" in result.lower() or "processing" in result.lower()
        assert "my_agentlet" in result
        mock_get_status.assert_called_once_with(execution_id, response_format="json")

    @patch("synteles_platform_mcp.main.synteles_get_execution_status")
    def test_get_execution_resource_error(self, mock_get_status: MagicMock) -> None:
        """Test getting execution resource when error occurs."""
        execution_id = "exec-123"
        mock_get_status.side_effect = PlatformAPIError("Execution not found")

        result = get_execution_resource(execution_id)

        assert "Error" in result
        assert "Execution not found" in result


if __name__ == "__main__":
    unittest.main()
