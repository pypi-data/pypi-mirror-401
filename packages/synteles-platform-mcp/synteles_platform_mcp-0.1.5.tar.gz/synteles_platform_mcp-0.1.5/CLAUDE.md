# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides Claude Desktop with tools to interact with the Synteles Platform API. It's a Python-based server using FastMCP that exposes authenticated API endpoints as MCP tools.

**Key Technologies:**
- Python 3.13+
- FastMCP (MCP server framework)
- OAuth 2.0 with PKCE (via AWS Cognito)
- OS keychain for secure token storage (keyring library)
- Cryptography library for Windows fallback storage (AES-256 encryption)
- Requests for HTTP client with certifi for SSL certificate validation

## Architecture

### Core Components

**MCP Server** (`synteles_platform_mcp/server.py`)
- Entry point that defines all MCP tools using `@mcp.tool()` decorators with annotations
- Each tool corresponds to a Synteles Platform API endpoint
- All tools prefixed with `synteles_` to prevent namespace conflicts
- Supports dual response formats (JSON/Markdown) for better UX
- Handles automatic token refresh on 401 responses
- All API calls go through `_make_request()` helper function

**Authentication Layer** (`synteles_platform_mcp/auth/`)
- `oauth_client.py`: Implements OAuth 2.0 PKCE flow with local callback server
  - Opens browser for user authentication
  - Receives authorization code via localhost callback
  - Exchanges code for tokens using code_verifier
  - Handles token refresh and logout
- `token_store.py`: Manages secure token storage in OS keychain with Windows fallback
  - Uses `keyring` library for cross-platform keychain access
  - Stores access_token, refresh_token, and id_token separately
  - **Windows fallback**: Automatically switches to AES-256 encrypted file storage when Windows Credential Manager size limit (2560 bytes) is exceeded
  - Fallback storage location: `~/.synteles/tokens.enc` (machine-specific encryption key)

### Authentication Flow

1. User calls `synteles_login` tool from Claude Desktop
2. MCP server generates PKCE code_verifier and code_challenge
3. Server starts temporary HTTP server on localhost (default port 8888)
4. Browser opens to `POST /auth/login` endpoint with PKCE challenge
5. User authenticates via AWS Cognito
6. Cognito redirects to `http://localhost:8888` with authorization code
7. Server exchanges code + verifier for tokens via `POST /auth/token`
8. Tokens stored securely in OS keychain using `keyring` library
9. All subsequent API calls automatically use stored access_token

### API Request Pattern

All API tools follow this pattern:
1. Call `_make_request(method, endpoint, access_token, json_data, params)`
2. Helper tries access_token parameter first, falls back to OAuth stored token
3. If 401 received, automatically attempts token refresh
4. If refresh succeeds, retries original request
5. If refresh fails, raises PlatformAPIError prompting re-authentication

### Environment Variables

- `SYNTELES_API_DOMAIN`: API domain (default: `api.synteles.dev`)
- `SYNTELES_OAUTH_CALLBACK_PORT`: OAuth callback port (default: `8888`)

## Development Commands

### Setup
```bash
# Install uv if not already installed (recommended package manager)
pip install uv

# Install in editable mode with dependencies
uv pip install -e .
```

### Testing
```bash
# Run all tests
make test

# Or directly:
python -m unittest discover tests -v
```

### Code Quality
```bash
# Lint code (checks all rules via ruff)
make lint

# Format code
make format

# Or directly:
ruff check synteles_platform_mcp/
ruff format synteles_platform_mcp/ tests/
```

### Running the MCP Server

The server is designed to be run by Claude Desktop via the MCP protocol. For manual testing:

```bash
# Run the server (uses stdio transport for MCP)
uv run synteles-platform-mcp

# Or with Python module syntax
python -m synteles_platform_mcp.main
```

### Cleanup
```bash
make clean  # Remove __pycache__ and .pyc files
```

## Claude Desktop Configuration

Example configuration for `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "synteles-platform": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/platform-mcp-server",
        "run",
        "synteles-platform-mcp"
      ],
      "env": {
        "SYNTELES_API_DOMAIN": "api.synteles.dev",
        "SYNTELES_OAUTH_CALLBACK_PORT": "8888"
      }
    }
  }
}
```

## API Integration

The MCP server exposes these tool categories (all tools prefixed with `synteles_`):

**Authentication Tools (3):**
- `synteles_login` - OAuth 2.0 PKCE authentication with browser
- `synteles_logout` - Clear tokens and revoke access
- `synteles_auth_status` - Check authentication state

**User Tools (1):**
- `synteles_get_current_user` - Get authenticated user profile

**Organization Tools (1):**
- `synteles_get_organization` - Get org metadata and user list

**Agentlet Tools (6):**
- `synteles_create_agentlet` - Create new AI agent configuration
- `synteles_list_agentlets` - List all agentlets in org (with pagination)
- `synteles_get_agentlet` - Get full agentlet definition with YAML
- `synteles_update_agentlet` - Update agentlet description/YAML
- `synteles_delete_agentlet` - Delete agentlet

**API Key Tools (3):**
- `synteles_create_api_key` - Generate new API key (returned once only)
- `synteles_list_api_keys` - List user's API keys (with pagination)
- `synteles_delete_api_key` - Revoke API key

**Execution Tools (5):**
- `synteles_create_agentlet_execution` - Deploy agentlet to cloud (GCP/Azure)
- `synteles_get_execution_status` - Check execution progress
- `synteles_get_execution_logs` - Retrieve execution logs from S3
- `synteles_terminate_execution` - Stop running execution
- `synteles_list_executions` - List executions with filtering and pagination

**MCP Resources (1):**
- `execution://{execution_id}` - Real-time execution status polling

Total: **20 tools + 1 resource**

For detailed API contracts, see README.md for usage examples.

## Code Conventions

- Python 3.13+ with modern type hints (`str | None` instead of `Optional[str]`)
- Use `from __future__ import annotations` for forward references
- Ruff configured with line length 120, target Python 3.8 for compatibility
- All API errors raise `PlatformAPIError` with descriptive messages
- Use raw docstrings (`r"""..."""`) to avoid escaping issues
- HTTP status codes defined as module constants (e.g., `HTTP_401_UNAUTHORIZED`)

## Security Notes

- **Never log or print tokens** - they're sensitive credentials
- Tokens stored in OS keychain (macOS Keychain, Windows Credential Manager, Linux Secret Service)
- **Windows-specific**: Automatic fallback to AES-256 encrypted file storage if Credential Manager size limit is exceeded
  - Encryption key derived from machine-specific entropy (USERNAME + COMPUTERNAME)
  - File location: `~/.synteles/tokens.enc`
  - Transparent to users - automatically selects best storage method
- PKCE prevents authorization code interception attacks
- Access tokens expire after 1 hour (3600 seconds)
- Refresh tokens expire after 30 days (2592000 seconds)
- Token refresh is automatic on 401 responses

## Key Files

- `synteles_platform_mcp/server.py` - All MCP tool definitions, annotations, and API logic
- `synteles_platform_mcp/models.py` - Pydantic models for request/response validation
- `synteles_platform_mcp/__main__.py` - Server entry point
- `synteles_platform_mcp/auth/oauth_client.py` - OAuth PKCE implementation
- `synteles_platform_mcp/auth/token_store.py` - Secure keychain storage
- `docs/OAUTH_IMPLEMENTATION_PROPOSAL.md` - OAuth implementation specification
- `pyproject.toml` - Project metadata and dependencies
- `Makefile` - Common development tasks
- `.env.example` - Environment variable template

## Common Development Patterns

**Adding a new API endpoint tool:**
1. Add HTTP status code constants if needed (e.g., `HTTP_422_UNPROCESSABLE_ENTITY`)
2. Define tool with `@mcp.tool()` decorator INCLUDING annotations:
   - `readOnlyHint`: True for GET operations that don't modify data
   - `destructiveHint`: True for DELETE or operations that modify data
   - `idempotentHint`: True if repeated calls have no additional effect
   - `openWorldHint`: True if tool interacts with external services
3. **Use `synteles_` prefix** for tool name to prevent namespace conflicts
4. Add `response_format` parameter for data-returning tools (default: "markdown")
5. Use raw docstring with full parameter and return documentation
6. Call `_make_request()` with appropriate method and endpoint
7. Implement both JSON and Markdown response formats using formatting helpers
8. Return formatted response based on `response_format` parameter
9. Let `_make_request()` handle auth, token refresh, and errors

**Example:**
```python
@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": True,
    }
)
def synteles_get_resource(
    resource_id: str,
    access_token: str | None = None,
    response_format: str = "markdown"
) -> str | dict[str, Any]:
    r"""Get resource details.

    Args:
        resource_id: Resource UUID
        access_token: Optional Bearer token
        response_format: Output format ("json" or "markdown", default: "markdown")

    Returns:
        Resource details in requested format
    """
    response = _make_request("GET", f"/api/resources/{resource_id}", access_token=access_token)
    data = cast(dict[str, Any], response.json())

    if response_format == "json":
        return data

    return _format_resource_markdown(data)
```

**Testing authentication flow:**
1. Clear keychain tokens: `python -c "from synteles_platform_mcp.auth.token_store import TokenStore; TokenStore().clear_tokens()"`
2. Run `synteles_login` tool from Claude Desktop
3. Check keychain for stored tokens:
   - macOS: Keychain Access app, search for "synteles-platform-mcp"
   - Windows: Credential Manager or check for `~/.synteles/tokens.enc` file
   - Linux: Use `secret-tool` or check distribution-specific keyring manager

**Testing response formats:**
1. Call any data-returning tool with `response_format="json"` to verify JSON output
2. Call same tool with `response_format="markdown"` (or omit for default) to verify Markdown formatting
3. Ensure markdown output is human-readable with proper headers and formatting

**Testing pagination:**
1. Call `synteles_list_agentlets()`, `synteles_list_api_keys()`, or `synteles_list_executions()` with `limit=5`
2. Verify response includes `next_token` if more results exist
3. Use `next_token` parameter to fetch subsequent pages
4. Verify pagination works correctly in both JSON and Markdown formats

**Debugging API calls:**
- Enable debug logging: `logging.basicConfig(level=logging.DEBUG)`
- Check logs for request/response details
- Inspect `_make_request()` error messages for API error responses
