"""Synteles Platform MCP Server."""

from __future__ import annotations

import logging
import os
from typing import Any, cast

import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from synteles_platform_mcp.auth.oauth_client import OAuthClient
from synteles_platform_mcp.auth.token_store import TokenStore

mcp = FastMCP("synteles-platform-mcp")
logger = logging.getLogger(__name__)

SYNTELES_API_DOMAIN = os.environ.get("SYNTELES_API_DOMAIN", "api.synteles.dev")
SYNTELES_OAUTH_CALLBACK_PORT = int(os.environ.get("SYNTELES_OAUTH_CALLBACK_PORT", "8888"))

# Initialize OAuth client and token store
oauth_client = OAuthClient(api_domain=SYNTELES_API_DOMAIN)
token_store = TokenStore()

HTTP_200_OK = 200
HTTP_202_ACCEPTED = 202
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409
HTTP_410_GONE = 410
HTTP_500_INTERNAL_SERVER_ERROR = 500

DEFAULT_EXECUTION_LIST_LIMIT = 50
DEFAULT_AGENTLET_LIST_LIMIT = 50
DEFAULT_API_KEY_LIST_LIMIT = 50
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600


class PlatformAPIError(Exception):
    """Custom exception for Synteles Platform API errors."""


def _make_request(
    method: str,
    endpoint: str,
    access_token: str | None = None,
    json_data: dict[str, Any] | None = None,
    params: dict[str, str] | None = None,
) -> requests.Response:
    r"""Make an authenticated HTTP request to the Synteles Platform API.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path (e.g., "/api/users/me")
        access_token: Bearer token for authentication (defaults to OAuth stored token)
        json_data: JSON request body for POST/PUT requests
        params: Query parameters

    Returns:
        Response object from the API

    Raises:
        PlatformAPIError: If the request fails or returns an error status

    """
    # Try to get token in order of preference:
    # 1. Explicitly provided access_token parameter
    # 2. OAuth stored token from keychain
    token = access_token or oauth_client.get_access_token()

    if not token:
        msg = "Authentication required. Please authenticate using the 'synteles_login' tool."
        raise PlatformAPIError(msg)

    url = f"https://{SYNTELES_API_DOMAIN}/v1{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json_data,
            params=params,
            timeout=30,
        )

        # Handle 401 Unauthorized - try to refresh token
        if response.status_code == HTTP_401_UNAUTHORIZED:
            logger.info("Access token expired, attempting refresh")
            new_token = oauth_client.refresh_access_token()

            if new_token:
                # Retry request with new token
                headers["Authorization"] = f"Bearer {new_token}"
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_data,
                    params=params,
                    timeout=30,
                )
            else:
                msg = "Access token expired and refresh failed. Please re-authenticate using the 'synteles_login' tool."
                raise PlatformAPIError(msg)

        # Handle other error codes
        if response.status_code >= HTTP_400_BAD_REQUEST:
            error_msg = response.json().get("error", "Unknown error") if response.text else "Unknown error"
            logger.error(
                "API request failed: %s %s - Status %d: %s",
                method,
                url,
                response.status_code,
                error_msg,
            )
            raise PlatformAPIError(f"API request failed (HTTP {response.status_code}): {error_msg}")

        return response

    except requests.exceptions.RequestException as e:
        logger.exception("Request exception occurred")
        raise PlatformAPIError(f"Request failed: {e}") from e


# ================================
# Response Formatting Helpers
# ================================


def _format_user_profile_markdown(data: dict[str, Any]) -> str:
    """Format user profile as markdown."""
    org_section = ""
    if data.get("org_id") and data.get("org_name"):
        org_section = f"\n**Organization**: {data['org_name']} (`{data['org_id']}`)"

    return f"""# User Profile

**Name**: {data["name"]}
**Email**: {data["email"]}{org_section}
**User ID**: `{data["sub"]}`

## Additional Details
- **Given Name**: {data.get("given_name", "N/A")}
- **Family Name**: {data.get("family_name", "N/A")}
- **Picture**: {data.get("picture", "No profile picture")}
"""


def _format_organization_markdown(data: dict[str, Any]) -> str:
    """Format organization as markdown."""
    users_list = "\n".join([f"- `{user_id}`" for user_id in data.get("users", [])])
    return f"""# Organization: {data["org_name"]}

## Members ({len(data.get("users", []))})
{users_list if users_list else "No members"}
"""


def _format_agentlet_summary_markdown(agentlet: dict[str, Any]) -> str:
    """Format single agentlet summary for markdown."""
    desc = agentlet.get("description") or "No description"
    return f"""### {agentlet["id"]}
**Description**: {desc}
**Created**: {agentlet["created_at"]}
**Updated**: {agentlet["updated_at"]}
"""


def _format_agentlet_list_markdown(agentlets: list[dict[str, Any]], count: int, next_token: str | None) -> str:
    """Format agentlet list as markdown."""
    agentlet_items = "\n".join([_format_agentlet_summary_markdown(a) for a in agentlets])
    pagination_info = f"\n\n*Showing {count} agentlet(s)*"
    if next_token:
        pagination_info += "\n*More results available - use `next_token` parameter to fetch next page*"

    return f"""# Agentlets

{agentlet_items if agentlet_items else "No agentlets found"}
{pagination_info}
"""


def _format_agentlet_detail_markdown(data: dict[str, Any], agentlet_id: str) -> str:
    """Format agentlet detail as markdown."""
    desc = data.get("description") or "No description"
    yaml_content = data.get("YAML") or "No YAML configuration"

    return f"""# Agentlet: {agentlet_id}

**Description**: {desc}
**Created**: {data["created_at"]}
**Updated**: {data["updated_at"]}

## YAML Configuration

```yaml
{yaml_content}
```
"""


def _format_api_key_summary_markdown(key: dict[str, Any]) -> str:
    """Format single API key summary for markdown."""
    last_used = key.get("last_used") or "Never used"
    return f"""### {key["key_name"]}
**Key ID**: `{key["key_id"]}`
**Created**: {key["created_at"]}
**Last Used**: {last_used}
"""


def _format_api_key_list_markdown(keys: list[dict[str, Any]], count: int, next_token: str | None) -> str:
    """Format API key list as markdown."""
    key_items = "\n".join([_format_api_key_summary_markdown(k) for k in keys])
    pagination_info = f"\n\n*Showing {count} API key(s)*"
    if next_token:
        pagination_info += "\n*More results available - use `next_token` parameter to fetch next page*"

    return f"""# API Keys

{key_items if key_items else "No API keys found"}
{pagination_info}
"""


def _format_api_key_created_markdown(data: dict[str, Any]) -> str:
    """Format newly created API key as markdown."""
    return f"""# API Key Created Successfully

⚠️ **IMPORTANT**: Save this key securely - it cannot be retrieved again!

**Key Name**: {data["key_name"]}
**Key ID**: `{data["key_id"]}`
**API Key**: `{data["key"]}`
**Created**: {data["created_at"]}

## Usage
Use this key in the `Authorization` header:
```
Authorization: Bearer {data["key"]}
```
"""


def _format_execution_summary_markdown(exec_data: dict[str, Any]) -> str:
    """Format single execution summary for markdown."""
    status_emoji = {
        "deploying": "🚀",
        "running": "⚙️",
        "completed": "✅",
        "failed": "❌",
        "terminated": "⚠️",
    }
    emoji = status_emoji.get(exec_data.get("status", ""), "")

    elapsed = ""
    if exec_data.get("elapsed_seconds"):
        elapsed = f"\n**Duration**: {_format_elapsed_time(exec_data['elapsed_seconds'])}"

    completed = ""
    if exec_data.get("completed_at"):
        completed = f"\n**Completed**: {exec_data['completed_at']}"

    logs = ""
    if exec_data.get("logs_s3_uri"):
        logs = f"\n**Logs**: `{exec_data['logs_s3_uri']}`"

    return f"""### {emoji} {exec_data["execution_id"][:8]}...
**Agentlet**: {exec_data["agentlet_id"]}
**Status**: {exec_data["status"]}
**Provider**: {exec_data["cloud_provider"]}
**Created**: {exec_data["created_at"]}{completed}{elapsed}{logs}
"""


def _format_execution_list_markdown(executions: list[dict[str, Any]], count: int, next_token: str | None) -> str:
    """Format execution list as markdown."""
    exec_items = "\n".join([_format_execution_summary_markdown(e) for e in executions])
    pagination_info = f"\n\n*Showing {count} execution(s)*"
    if next_token:
        pagination_info += "\n*More results available - use `next_token` parameter to fetch next page*"

    return f"""# Executions

{exec_items if exec_items else "No executions found"}
{pagination_info}
"""


# ================================
# Authentication Endpoints
# ================================


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    )
)
def synteles_login(callback_port: int | None = None, timeout: int = 120) -> dict[str, Any]:
    r"""Authenticate with Synteles Platform using OAuth 2.0 with PKCE.

    Opens a browser window for user authentication via AWS Cognito. After successful
    authentication, access and refresh tokens are securely stored in the OS keychain.
    These tokens are automatically used for all subsequent API calls.

    Args:
        callback_port: Port for local callback server (default: from SYNTELES_OAUTH_CALLBACK_PORT env var or 8888)
        timeout: Timeout in seconds for user to complete authentication (default: 120)

    Returns:
        Authentication result including:
        - status: "success" if authentication succeeded
        - message: Human-readable status message
        - expires_in: Token expiration time in seconds (typically 3600)

    Raises:
        PlatformAPIError: If authentication fails or times out

    Example:
        >>> synteles_login()
        {
            "status": "success",
            "message": "Successfully authenticated! Tokens stored securely.",
            "expires_in": 3600
        }

    """
    # Use environment variable if callback_port not explicitly provided
    if callback_port is None:
        callback_port = SYNTELES_OAUTH_CALLBACK_PORT

    try:
        result = oauth_client.login(callback_port=callback_port, timeout=timeout)
        logger.info("User authenticated successfully")
        return result
    except Exception as e:
        logger.exception("Login failed")
        raise PlatformAPIError(f"Login failed: {e}") from e


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        idempotentHint=False,
        openWorldHint=True,
    )
)
def synteles_logout() -> dict[str, str]:
    r"""Logout and clear stored authentication tokens.

    Revokes the refresh token on the server and removes all stored tokens
    from the OS keychain. After logout, you'll need to call synteles_login() again
    to access protected endpoints.

    Returns:
        Logout status:
        - status: "success" if logout succeeded
        - message: Human-readable status message

    Example:
        >>> synteles_logout()
        {
            "status": "success",
            "message": "Logged out successfully. Tokens cleared from secure storage."
        }

    """
    try:
        result = oauth_client.logout()
        logger.info("User logged out successfully")
        return result
    except Exception as e:
        logger.exception("Logout failed")
        raise PlatformAPIError(f"Logout failed: {e}") from e


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        openWorldHint=False,
    )
)
def synteles_auth_status() -> dict[str, Any]:
    r"""Check current authentication status.

    Returns information about whether the user is authenticated and has
    valid tokens stored in the OS keychain.

    Returns:
        Authentication status including:
        - authenticated: True if tokens exist, False otherwise
        - has_access_token: True if access token exists
        - has_refresh_token: True if refresh token exists
        - message: Human-readable status message

    Example:
        >>> synteles_auth_status()
        {
            "authenticated": true,
            "has_access_token": true,
            "has_refresh_token": true,
            "message": "Authenticated - tokens are stored securely"
        }

    """
    has_access = token_store.get_access_token() is not None
    has_refresh = token_store.get_refresh_token() is not None
    authenticated = has_access and has_refresh

    if authenticated:
        message = "Authenticated - tokens are stored securely"
    else:
        message = "Not authenticated - use 'synteles_login' tool to authenticate"

    return {
        "authenticated": authenticated,
        "has_access_token": has_access,
        "has_refresh_token": has_refresh,
        "message": message,
    }


# ================================
# User Endpoints
# ================================


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        openWorldHint=True,
    )
)
def synteles_get_current_user(
    access_token: str | None = None, response_format: str = "markdown"
) -> str | dict[str, Any]:
    r"""Get the authenticated user's profile including organization information.

    This endpoint retrieves the current user's profile data including their
    Cognito user ID, email, name, and organization details if they belong to one.

    Args:
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        User profile in requested format including:
        - sub: Cognito user UUID
        - email: User's email address
        - name: User's full name
        - given_name: User's first name
        - family_name: User's last name
        - picture: User's profile picture URL
        - org_id: Organization UUID (if user belongs to an organization)
        - org_name: Organization name (if user belongs to an organization)

    Raises:
        PlatformAPIError: If authentication fails or API request fails

    Example:
        >>> synteles_get_current_user()
        # User Profile
        **Name**: John Doe
        **Email**: user@example.com
        ...

    """
    response = _make_request("GET", "/api/users/me", access_token=access_token)
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    return _format_user_profile_markdown(data)


# ================================
# Organization Endpoints
# ================================


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        openWorldHint=True,
    )
)
def synteles_get_organization(
    org_id: str, access_token: str | None = None, response_format: str = "markdown"
) -> str | dict[str, Any]:
    r"""Get organization metadata and list of users.

    Retrieves detailed information about a specific organization including
    its name and the list of user IDs that belong to it.

    Args:
        org_id: Organization UUID
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Organization details in requested format including:
        - org_name: Name of the organization
        - users: List of user UUIDs belonging to the organization

    Raises:
        PlatformAPIError: If organization not found or API request fails

    Example:
        >>> synteles_get_organization("org-uuid-123")
        # Organization: Example Organization
        ## Members (2)
        - user-uuid-1
        - user-uuid-2

    """
    response = _make_request("GET", f"/api/organizations/{org_id}", access_token=access_token)
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    return _format_organization_markdown(data)


# ================================
# Agentlet Endpoints
# ================================


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        idempotentHint=False,
        openWorldHint=True,
    )
)
def synteles_create_agentlet(
    org_id: str,
    agentlet_id: str,
    description: str | None = None,
    yaml_definition: str | None = None,
    access_token: str | None = None,
    response_format: str = "markdown",
) -> str | dict[str, Any]:
    r"""Create a new agentlet in the organization.

    Creates a new AI agent configuration with the specified ID. The agentlet ID must
    start with a letter or underscore and contain only alphanumeric characters and underscores.

    Args:
        org_id: Organization UUID
        agentlet_id: Unique agentlet identifier (e.g., "my_custom_assistant")
        description: Optional text description of the agentlet
        yaml_definition: Optional YAML configuration string for the agentlet
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Created agentlet details in requested format including:
        - id: Agentlet identifier
        - description: Agentlet description
        - YAML: YAML configuration
        - created_at: Creation timestamp (ISO 8601)
        - updated_at: Last update timestamp (ISO 8601)

    Raises:
        PlatformAPIError: If agentlet ID is invalid, already exists, or API request fails

    Example:
        >>> synteles_create_agentlet(
        ...     org_id="org-123",
        ...     agentlet_id="my_agent",
        ...     description="My first agent",
        ...     yaml_definition="agentlet:\\n  name: MyAgent\\n  ..."
        ... )
        # Agentlet: my_agent
        **Description**: My first agent
        ...

    """
    request_body: dict[str, Any] = {"id": agentlet_id}
    if description is not None:
        request_body["description"] = description
    if yaml_definition is not None:
        request_body["YAML"] = yaml_definition

    response = _make_request(
        "POST",
        f"/api/organizations/{org_id}/agentlets",
        access_token=access_token,
        json_data=request_body,
    )
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    return _format_agentlet_detail_markdown(data, agentlet_id)


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        openWorldHint=True,
    )
)
def synteles_list_agentlets(
    org_id: str,
    limit: int = DEFAULT_AGENTLET_LIST_LIMIT,
    next_token: str | None = None,
    access_token: str | None = None,
    response_format: str = "markdown",
) -> str | dict[str, Any]:
    r"""List all agentlets in the organization with pagination.

    Retrieves a paginated list of all agentlets belonging to the specified organization.
    Returns basic information without YAML content. Use synteles_get_agentlet() to retrieve
    the full definition including YAML.

    Args:
        org_id: Organization UUID
        limit: Maximum number of results per page (default: 50, range: 1-100)
        next_token: Optional pagination token from previous response
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Paginated agentlet list in requested format including:
        - agentlets: List of agentlet summaries
        - count: Number of agentlets in current response
        - next_token: Pagination token (present only if more results available)

        Each agentlet summary contains:
        - id: Agentlet identifier
        - description: Agentlet description
        - created_at: Creation timestamp (ISO 8601)
        - updated_at: Last update timestamp (ISO 8601)

    Raises:
        PlatformAPIError: If API request fails

    Example:
        >>> synteles_list_agentlets("org-123", limit=10)
        # Agentlets
        ### agentlet1
        **Description**: First agent
        ...

    """
    params: dict[str, str] = {}
    if limit != DEFAULT_AGENTLET_LIST_LIMIT:
        params["limit"] = str(limit)
    if next_token is not None:
        params["next_token"] = next_token

    response = _make_request("GET", f"/api/organizations/{org_id}/agentlets", access_token=access_token, params=params)

    # Handle both paginated and non-paginated API responses
    data = cast(dict[str, Any] | list[dict[str, Any]], response.json())

    # If API returns a list (non-paginated), wrap it in pagination structure
    if isinstance(data, list):
        agentlets = data
        result = {
            "agentlets": agentlets,
            "count": len(agentlets),
            "next_token": None,
        }
    else:
        # API returns paginated response
        agentlets = data.get("agentlets", data.get("items", []))
        result = {
            "agentlets": agentlets,
            "count": data.get("count", len(agentlets)),
            "next_token": data.get("next_token"),
        }

    if response_format == "json":
        return result

    return _format_agentlet_list_markdown(
        cast(list[dict[str, Any]], result["agentlets"]),
        cast(int, result["count"]),
        cast(str | None, result.get("next_token")),
    )


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        openWorldHint=True,
    )
)
def synteles_get_agentlet(
    org_id: str, agentlet_id: str, access_token: str | None = None, response_format: str = "markdown"
) -> str | dict[str, Any]:
    r"""Get full agentlet definition including YAML configuration.

    Retrieves the complete agentlet configuration including its YAML definition,
    description, and timestamps.

    Args:
        org_id: Organization UUID
        agentlet_id: Agentlet identifier
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Complete agentlet definition in requested format including:
        - description: Agentlet description
        - YAML: YAML configuration string
        - created_at: Creation timestamp (ISO 8601)
        - updated_at: Last update timestamp (ISO 8601)

    Raises:
        PlatformAPIError: If agentlet not found or API request fails

    Example:
        >>> synteles_get_agentlet("org-123", "my_agent")
        # Agentlet: my_agent
        **Description**: My custom agent
        ## YAML Configuration
        ```yaml
        ...
        ```

    """
    response = _make_request(
        "GET",
        f"/api/organizations/{org_id}/agentlets/{agentlet_id}",
        access_token=access_token,
    )
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    return _format_agentlet_detail_markdown(data, agentlet_id)


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        idempotentHint=True,
        openWorldHint=True,
    )
)
def synteles_update_agentlet(
    org_id: str,
    agentlet_id: str,
    description: str | None = None,
    yaml_definition: str | None = None,
    access_token: str | None = None,
) -> dict[str, str]:
    r"""Update an existing agentlet.

    Updates an agentlet's description and/or YAML configuration. Both fields are
    optional; only provided fields will be updated. The updated_at timestamp is
    automatically set.

    Args:
        org_id: Organization UUID
        agentlet_id: Agentlet identifier
        description: Optional updated description
        yaml_definition: Optional updated YAML configuration string
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.

    Returns:
        Success message: {"message": "Agentlet updated"}

    Raises:
        PlatformAPIError: If agentlet not found or API request fails

    Example:
        >>> synteles_update_agentlet(
        ...     org_id="org-123",
        ...     agentlet_id="my_agent",
        ...     description="Updated description",
        ...     yaml_definition="agentlet:\\n  name: UpdatedAgent\\n  ..."
        ... )
        {"message": "Agentlet updated"}

    """
    request_body: dict[str, str] = {}
    if description is not None:
        request_body["description"] = description
    if yaml_definition is not None:
        request_body["YAML"] = yaml_definition

    response = _make_request(
        "PUT",
        f"/api/organizations/{org_id}/agentlets/{agentlet_id}",
        access_token=access_token,
        json_data=request_body,
    )
    return cast(dict[str, str], response.json())


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        idempotentHint=True,
        openWorldHint=True,
    )
)
def synteles_delete_agentlet(org_id: str, agentlet_id: str, access_token: str | None = None) -> dict[str, str]:
    r"""Delete an agentlet.

    Permanently removes an agentlet from the organization.

    Args:
        org_id: Organization UUID
        agentlet_id: Agentlet identifier
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.

    Returns:
        Empty response on success (HTTP 204 No Content)

    Raises:
        PlatformAPIError: If agentlet not found or API request fails

    Example:
        >>> synteles_delete_agentlet("org-123", "my_agent")
        {}

    """
    _make_request(
        "DELETE",
        f"/api/organizations/{org_id}/agentlets/{agentlet_id}",
        access_token=access_token,
    )
    return {"message": "Agentlet deleted successfully"}


# ================================
# API Key Management Endpoints
# ================================


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        idempotentHint=False,
        openWorldHint=True,
    )
)
def synteles_create_api_key(
    key_name: str, access_token: str | None = None, response_format: str = "markdown"
) -> str | dict[str, Any]:
    r"""Create a new API key for programmatic access.

    Creates a new API key for the authenticated user. The key is returned only once
    and cannot be retrieved later, so it must be stored securely.

    Args:
        key_name: Descriptive name for the API key (e.g., "Production API Key")
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        API key details in requested format including:
        - key_id: UUID for the API key
        - key: The actual API key (43-character base64url-encoded string) - STORE THIS SECURELY
        - key_name: Name of the API key
        - created_at: Creation timestamp (ISO 8601)

    Raises:
        PlatformAPIError: If key_name is missing, user not in organization, or API request fails

    Example:
        >>> synteles_create_api_key("Production Key")
        # API Key Created Successfully
        ⚠️ **IMPORTANT**: Save this key securely - it cannot be retrieved again!
        ...

    """
    request_body = {"key_name": key_name}
    response = _make_request(
        "POST",
        "/api/users/apikeys",
        access_token=access_token,
        json_data=request_body,
    )
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    return _format_api_key_created_markdown(data)


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        openWorldHint=True,
    )
)
def synteles_list_api_keys(
    limit: int = DEFAULT_API_KEY_LIST_LIMIT,
    next_token: str | None = None,
    access_token: str | None = None,
    response_format: str = "markdown",
) -> str | dict[str, Any]:
    r"""List all API keys for the authenticated user with pagination.

    Retrieves all API keys created by the authenticated user, including their
    names, creation dates, and last usage timestamps. The actual key values
    are never returned (only stored as hashes).

    Args:
        limit: Maximum number of results per page (default: 50, range: 1-100)
        next_token: Optional pagination token from previous response
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Paginated API key list in requested format including:
        - api_keys: List of API key summaries
        - count: Number of keys in current response
        - next_token: Pagination token (present only if more results available)

        Each API key summary contains:
        - key_id: UUID for the API key
        - key_name: Name of the API key
        - created_at: Creation timestamp (ISO 8601)
        - last_used: Last usage timestamp (ISO 8601) or null if never used

    Raises:
        PlatformAPIError: If API request fails

    Example:
        >>> synteles_list_api_keys(limit=10)
        # API Keys
        ### Production Key
        **Key ID**: uuid-1
        **Created**: 2025-12-01T10:00:00
        **Last Used**: 2025-12-01T15:30:00

    """
    params: dict[str, str] = {}
    if limit != DEFAULT_API_KEY_LIST_LIMIT:
        params["limit"] = str(limit)
    if next_token is not None:
        params["next_token"] = next_token

    response = _make_request("GET", "/api/users/apikeys", access_token=access_token, params=params)

    # Handle both paginated and non-paginated API responses
    data = cast(dict[str, Any] | list[dict[str, Any]], response.json())

    # If API returns a list (non-paginated), wrap it in pagination structure
    if isinstance(data, list):
        api_keys = data
        result = {
            "api_keys": api_keys,
            "count": len(api_keys),
            "next_token": None,
        }
    else:
        # API returns paginated response
        api_keys = data.get("api_keys", data.get("items", []))
        result = {
            "api_keys": api_keys,
            "count": data.get("count", len(api_keys)),
            "next_token": data.get("next_token"),
        }

    if response_format == "json":
        return result

    return _format_api_key_list_markdown(
        cast(list[dict[str, Any]], result["api_keys"]),
        cast(int, result["count"]),
        cast(str | None, result.get("next_token")),
    )


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        idempotentHint=True,
        openWorldHint=True,
    )
)
def synteles_delete_api_key(key_id: str, access_token: str | None = None) -> dict[str, str]:
    r"""Delete an API key.

    Permanently removes an API key. The key will immediately stop working
    for authentication.

    Args:
        key_id: API key UUID to delete
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.

    Returns:
        Empty response on success (HTTP 204 No Content)

    Raises:
        PlatformAPIError: If key not found, unauthorized, or API request fails

    Example:
        >>> synteles_delete_api_key("key-uuid-123")
        {}

    """
    _make_request(
        "DELETE",
        f"/api/users/apikeys/{key_id}",
        access_token=access_token,
    )
    return {"message": "API key deleted successfully"}


# ================================
# Execution/Scheduler Endpoints
# ================================


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        idempotentHint=False,
        openWorldHint=True,
    )
)
def synteles_create_agentlet_execution(
    org_id: str,
    agentlet_id: str,
    cloud_provider: str = "gcp",
    prompt: str | None = None,
    timeout: int = 3600,
    access_token: str | None = None,
    response_format: str = "markdown",
) -> str | dict[str, Any]:
    r"""Create a new agentlet execution on a cloud provider.

    Creates an execution record and asynchronously deploys the agentlet to a cloud provider
    (GCP Cloud Run or Azure Container Instances). The execution runs in the background and
    can be monitored using synteles_get_execution_status() or the MCP resource.

    Note:
        Monitor execution progress using the MCP resource:
        `execution://{execution_id}` for real-time status updates.
        Claude Desktop will automatically poll this resource every 3-5 seconds.

    Args:
        org_id: Organization UUID
        agentlet_id: Agentlet identifier
        cloud_provider: Cloud provider selection ("gcp" or "azure", default: "gcp")
        prompt: Optional task description passed to agentlet container as environment variable
        timeout: Maximum execution time in seconds (default: 3600, range: 1-86400)
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Execution details in requested format including:
        - execution_id: UUID for the execution
        - status: Current status (typically "running" or "deploying")
        - agentlet_id: Agentlet identifier
        - cloud_provider: Cloud provider used
        - created_at: Creation timestamp (ISO 8601)

    Raises:
        PlatformAPIError: If agentlet not found, invalid parameters, or API request fails

    Example:
        >>> synteles_create_agentlet_execution(
        ...     org_id="org-123",
        ...     agentlet_id="my_agentlet",
        ...     cloud_provider="gcp",
        ...     prompt="Generate monthly sales report",
        ...     timeout=1800
        ... )
        🚀 Execution Created
        **Execution ID**: 550e8400-e29b-41d4-a716-446655440000
        **Status**: running
        ...

    """
    request_body: dict[str, Any] = {
        "cloud_provider": cloud_provider,
        "timeout": timeout,
    }
    if prompt is not None:
        request_body["prompt"] = prompt

    response = _make_request(
        "POST",
        f"/api/organizations/{org_id}/agentlets/{agentlet_id}/executions",
        access_token=access_token,
        json_data=request_body,
    )
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    # Markdown format for execution creation
    exec_id = data.get("execution_id", "unknown")
    status = data.get("status", "unknown")
    provider = data.get("cloud_provider", "unknown")

    return f"""🚀 Execution Created

**Execution ID**: `{exec_id}`
**Agentlet**: {agentlet_id}
**Status**: {status}
**Cloud Provider**: {provider}
**Created**: {data.get("created_at", "unknown")}

Monitor progress with: `synteles_get_execution_status("{exec_id}")`
Or subscribe to resource: `execution://{exec_id}`
"""


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        openWorldHint=True,
    )
)
def synteles_get_execution_status(
    execution_id: str, access_token: str | None = None, response_format: str = "markdown"
) -> str | dict[str, Any]:
    r"""Get execution status and metadata.

    Retrieves the current status of an agentlet execution including metadata,
    progress information, and results if completed.

    Note:
        For automatic real-time updates, Claude Desktop can subscribe to the
        MCP resource `execution://{execution_id}` which polls this endpoint
        every 3-5 seconds. This tool provides the same data via direct API call.

    Args:
        execution_id: Execution UUID
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Execution status in requested format including:
        - execution_id: UUID for the execution
        - agentlet_id: Agentlet identifier
        - cloud_provider: Cloud provider used
        - status: Current status (deploying, running, completed, failed, terminated)
        - logs_s3_uri: S3 URI for log file (null if execution still in progress)
        - created_at: Creation timestamp (ISO 8601)
        - completed_at: Completion timestamp (ISO 8601, null if still running)
        - elapsed_seconds: Total execution time (only present if completed)

    Status Values:
        - deploying: Container deployment in progress
        - running: Container is executing
        - completed: Execution finished successfully
        - failed: Execution encountered an error
        - terminated: Execution was manually terminated

    Raises:
        PlatformAPIError: If execution not found or API request fails

    Example:
        >>> synteles_get_execution_status("550e8400-e29b-41d4-a716-446655440000")
        ✅ Execution Completed
        **Status**: completed
        **Duration**: 5m 5s
        ...

    """
    response = _make_request("GET", f"/api/executions/{execution_id}/status", access_token=access_token)
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    return _format_execution_status_for_display(data)


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        openWorldHint=True,
    )
)
def synteles_get_execution_logs(
    execution_id: str,
    log_format: str = "text",
    download: bool = False,
    access_token: str | None = None,
) -> dict[str, Any]:
    r"""Get execution logs from S3 storage.

    Retrieves the execution logs. If the execution is still in progress, returns
    a 202 Accepted status with information about when logs will be available.

    Note:
        Logs are only available after execution completes. Use the MCP resource
        `execution://{execution_id}` to monitor execution progress, then call this
        tool once the status is "completed" or "failed" to retrieve logs.

    Args:
        execution_id: Execution UUID
        log_format: Response format ("text" or "json", default: "text")
        download: Add Content-Disposition header for file download (default: False)
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.

    Returns:
        For completed executions (format="json"):
        - execution_id: UUID for the execution
        - status: Current execution status
        - logs_available: True if logs are available
        - s3_uri: S3 URI of log file
        - log_size_bytes: Size of log file in bytes
        - created_at: Creation timestamp (ISO 8601)
        - completed_at: Completion timestamp (ISO 8601)
        - logs: Array of parsed log entries with timestamp, severity, and message

        For in-progress executions:
        - execution_id: UUID for the execution
        - status: Current status
        - logs_available: False
        - message: Information about when logs will be available
        - created_at: Creation timestamp (ISO 8601)

    Raises:
        PlatformAPIError: If execution not found, logs not available (410 Gone),
                         or API request fails

    Example (in progress):
        >>> synteles_get_execution_logs("550e8400-e29b-41d4-a716-446655440000")
        {
            "execution_id": "550e8400-e29b-41d4-a716-446655440000",
            "status": "running",
            "logs_available": false,
            "message": "Execution is running. Logs will be available after completion.",
            "created_at": "2025-12-13T10:30:45Z"
        }

    Example (completed, JSON format):
        >>> synteles_get_execution_logs("550e8400-e29b-41d4-a716-446655440000", log_format="json")
        {
            "execution_id": "550e8400-e29b-41d4-a716-446655440000",
            "status": "completed",
            "logs_available": true,
            "s3_uri": "s3://synteles-platform-dev-execution-logs/executions/550e8400/logs.txt",
            "log_size_bytes": 2048,
            "created_at": "2025-12-13T10:30:45Z",
            "completed_at": "2025-12-13T10:35:50Z",
            "logs": [...]
        }

    """
    params = {}
    if log_format != "text":
        params["format"] = log_format
    if download:
        params["download"] = "true"

    response = _make_request(
        "GET",
        f"/api/executions/{execution_id}/logs",
        access_token=access_token,
        params=params,
    )

    # If log_format is text and response is successful, return the text content
    if log_format == "text" and response.status_code == HTTP_200_OK:
        return {
            "execution_id": execution_id,
            "status": response.headers.get("X-Execution-Status", "unknown"),
            "logs_available": True,
            "s3_uri": response.headers.get("X-S3-Uri", ""),
            "logs_text": response.text,
        }

    return cast(dict[str, Any], response.json())


@mcp.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        idempotentHint=True,
        openWorldHint=True,
    )
)
def synteles_terminate_execution(
    execution_id: str, access_token: str | None = None, response_format: str = "markdown"
) -> str | dict[str, Any]:
    r"""Terminate a running execution.

    Terminates a running execution by deleting the cloud provider container/service.
    If the execution has already completed, failed, or been terminated, only the
    database status is updated.

    Note:
        If monitoring via the MCP resource `execution://{execution_id}`, the resource
        will automatically reflect the terminated status after this operation completes.

    Args:
        execution_id: Execution UUID
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Termination result in requested format including:
        - execution_id: UUID for the execution
        - status: New status (should be "terminated")
        - terminated_at: Termination timestamp (ISO 8601)

    Raises:
        PlatformAPIError: If execution not found or API request fails

    Example:
        >>> synteles_terminate_execution("550e8400-e29b-41d4-a716-446655440000")
        ⚠️ Execution Terminated
        **Execution ID**: 550e8400-...
        **Status**: terminated
        ...

    """
    response = _make_request("DELETE", f"/api/executions/{execution_id}", access_token=access_token)
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    return f"""⚠️ Execution Terminated

**Execution ID**: `{data.get("execution_id", "unknown")}`
**Status**: {data.get("status", "terminated")}
**Terminated At**: {data.get("terminated_at", "unknown")}
"""


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        openWorldHint=True,
    )
)
def synteles_list_executions(
    agentlet_id: str | None = None,
    status: str | None = None,
    created_at_start: str | None = None,
    created_at_end: str | None = None,
    completed_at_start: str | None = None,
    completed_at_end: str | None = None,
    limit: int = DEFAULT_EXECUTION_LIST_LIMIT,
    next_token: str | None = None,
    access_token: str | None = None,
    response_format: str = "markdown",
) -> str | dict[str, Any]:
    r"""List executions with filtering and pagination support.

    Retrieves a paginated list of executions for the user's organization with
    optional filtering by agentlet, status, and date ranges.

    Note:
        For real-time monitoring of individual executions, use the MCP resource
        `execution://{execution_id}` which provides automatic status updates
        every 3-5 seconds. This tool is for listing and filtering multiple executions.

    Args:
        agentlet_id: Optional filter by agentlet identifier
        status: Optional filter by execution status (deploying, running, completed, failed, terminated)
        created_at_start: Optional filter by creation date (ISO 8601 timestamp, inclusive)
        created_at_end: Optional filter by creation date (ISO 8601 timestamp, inclusive)
        completed_at_start: Optional filter by completion date (ISO 8601 timestamp, inclusive)
        completed_at_end: Optional filter by completion date (ISO 8601 timestamp, inclusive)
        limit: Maximum number of results per page (default: 50, range: 1-100)
        next_token: Optional pagination token from previous response
        access_token: Optional Bearer token for authentication. If not provided,
                     uses OAuth token from secure keychain storage.
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Paginated execution list in requested format including:
        - executions: Array of execution summaries
        - count: Number of executions in current response
        - next_token: Pagination token (present only if more results available)

        Each execution summary contains:
        - execution_id: UUID for the execution
        - agentlet_id: Agentlet identifier
        - status: Current status
        - cloud_provider: Cloud provider used
        - created_at: Creation timestamp (ISO 8601)
        - completed_at: Completion timestamp (ISO 8601, null for in-progress)
        - logs_s3_uri: S3 URI for logs (null for in-progress)
        - elapsed_seconds: Total execution time (only present for completed)

    Raises:
        PlatformAPIError: If invalid parameters, user not in organization, or API request fails

    Example:
        >>> synteles_list_executions(agentlet_id="my_agentlet", status="completed", limit=10)
        # Executions
        ### ✅ 550e8400...
        **Agentlet**: my_agentlet
        **Status**: completed
        ...

    """
    params: dict[str, str] = {}
    if agentlet_id is not None:
        params["agentlet_id"] = agentlet_id
    if status is not None:
        params["status"] = status
    if created_at_start is not None:
        params["created_at_start"] = created_at_start
    if created_at_end is not None:
        params["created_at_end"] = created_at_end
    if completed_at_start is not None:
        params["completed_at_start"] = completed_at_start
    if completed_at_end is not None:
        params["completed_at_end"] = completed_at_end
    if limit != DEFAULT_EXECUTION_LIST_LIMIT:
        params["limit"] = str(limit)
    if next_token is not None:
        params["next_token"] = next_token

    response = _make_request("GET", "/api/executions", access_token=access_token, params=params)
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    executions = data.get("executions", [])
    count = data.get("count", len(executions))
    next_token_val = data.get("next_token")

    return _format_execution_list_markdown(executions, count, next_token_val)


# ================================
# MCP Resources for Execution Status Polling
# ================================


def _format_elapsed_time(seconds: int) -> str:
    """Format elapsed time in human-readable format.

    Args:
        seconds: Elapsed time in seconds

    Returns:
        Formatted time string (e.g., "30s", "2m 15s", "1h 5m")

    """
    if seconds < SECONDS_PER_MINUTE:
        return f"{seconds}s"
    if seconds < SECONDS_PER_HOUR:
        minutes = seconds // SECONDS_PER_MINUTE
        secs = seconds % SECONDS_PER_MINUTE
        return f"{minutes}m {secs}s"
    hours = seconds // SECONDS_PER_HOUR
    minutes = (seconds % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE
    return f"{hours}h {minutes}m"


def _format_execution_status_for_display(status_data: dict[str, Any]) -> str:
    """Format execution status for conversational display.

    Args:
        status_data: Execution status data from the API

    Returns:
        Formatted status string for display in Claude Desktop

    """
    execution_id = status_data.get("execution_id", "unknown")
    agentlet_id = status_data.get("agentlet_id", "unknown")
    status = status_data.get("status", "unknown")
    elapsed_seconds = status_data.get("elapsed_seconds", 0)
    elapsed = _format_elapsed_time(elapsed_seconds)

    if status == "deploying":
        return f"""🚀 Deploying "{agentlet_id}" agentlet...

Status: Starting container
Time elapsed: {elapsed}

Please wait, this usually takes 30-60 seconds..."""

    if status == "running":
        cloud_provider = status_data.get("cloud_provider", "unknown")
        return f"""⚙️ Agentlet "{agentlet_id}" is processing...

Status: Running
Cloud Provider: {cloud_provider}
Time elapsed: {elapsed}

Still working on it..."""

    if status == "completed":
        logs_s3_uri = status_data.get("logs_s3_uri", "")
        return f"""✅ Agentlet "{agentlet_id}" completed successfully!

Status: Completed
Total time: {elapsed}

Logs available at: {logs_s3_uri}
Use synteles_get_execution_logs("{execution_id}") to retrieve full logs."""

    if status == "failed":
        error = status_data.get("error", "Unknown error")
        return f"""❌ Agentlet "{agentlet_id}" failed

Status: Failed
Time elapsed: {elapsed}

Error: {error}

Use synteles_get_execution_logs("{execution_id}") to view error logs."""

    if status == "terminated":
        terminated_at = status_data.get("terminated_at", "unknown")
        return f"""⚠️ Agentlet "{agentlet_id}" was terminated

Status: Terminated
Time elapsed: {elapsed}
Terminated at: {terminated_at}

The execution was stopped by user request."""

    return f"""Status: {status}
Time: {elapsed}"""


@mcp.resource("execution://{execution_id}")
def get_execution_resource(execution_id: str) -> str:
    """MCP resource for polling execution status.

    This resource provides real-time status updates for agentlet executions.
    Claude Desktop will automatically poll this resource every 3-5 seconds
    when the execution is in progress.

    Args:
        execution_id: Execution UUID from the URI template

    Returns:
        Formatted execution status for display

    """
    try:
        status_data = synteles_get_execution_status(execution_id, response_format="json")
        if isinstance(status_data, dict):
            return _format_execution_status_for_display(status_data)
        return "Error: Invalid response format from execution status"
    except PlatformAPIError as e:
        return f"Error retrieving execution status: {e}"
