# Synteles Platform MCP Server - Deployment Guide

This guide explains how to deploy the Synteles Platform MCP Server on customer machines (Windows and macOS) and configure it with Claude Desktop.

## Prerequisites

- Claude Desktop installed
- Internet connection

## Deployment Scripts

Two deployment scripts are provided for seamless installation:

- `deploy-windows.ps1` - PowerShell script for Windows
- `deploy-macos.sh` - Shell script for macOS

Both scripts will:
1. Install `uv` if not already present
2. Install the `synteles-platform-mcp` package from PyPI
3. Configure Claude Desktop automatically
4. Set up environment variables

## Windows Deployment

### Option 1: Interactive (Recommended)

1. Open PowerShell
2. Navigate to the script location
3. Run:
```powershell
.\deploy-windows.ps1
```

### Option 2: With Custom Parameters

```powershell
.\deploy-windows.ps1 `
    -ApiDomain "api.synteles.dev" `
    -CallbackPort "8888"
```

### Option 3: Remote Execution

```powershell
irm https://raw.githubusercontent.com/Synteles/platform-mcp-server/main/deploy-windows.ps1 | iex
```

## macOS Deployment

### Option 1: Interactive (Recommended)

1. Open Terminal
2. Navigate to the script location
3. Run:
```bash
./deploy-macos.sh
```

### Option 2: With Custom Parameters

```bash
./deploy-macos.sh api.synteles.dev 8888
```

### Option 3: Remote Execution

```bash
curl -fsSL https://raw.githubusercontent.com/Synteles/platform-mcp-server/main/deploy-macos.sh | bash
```

## Configuration

The scripts configure Claude Desktop with the following settings:

```json
{
  "mcpServers": {
    "synteles-platform": {
      "command": "/path/to/synteles-platform-mcp",
      "env": {
        "SYNTELES_API_DOMAIN": "api.synteles.dev",
        "SYNTELES_OAUTH_CALLBACK_PORT": "8888"
      }
    }
  }
}
```

### Configuration Locations

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNTELES_API_DOMAIN` | `api.synteles.dev` | Synteles Platform API domain |
| `SYNTELES_OAUTH_CALLBACK_PORT` | `8888` | OAuth callback port for authentication |

## Post-Deployment

After running the deployment script:

1. **Restart Claude Desktop** - Close and reopen the application
2. **Verify Installation** - The Synteles Platform MCP server should appear in Claude's available tools
3. **First-Time Authentication** - On first use, you'll be prompted to authenticate via OAuth:
   - A browser window will open
   - Log in with your Synteles credentials
   - Authorize the application
   - Return to Claude Desktop

## Troubleshooting

### Windows

**Issue**: Script execution policy error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue**: Login failed with CredWrite error (resolved in v0.1.0+)
```
Error: (1783, 'CredWrite', 'The stub received bad data')
```

**This issue is automatically resolved in version 0.1.0+**

The MCP server now automatically detects when Windows Credential Manager size limits are exceeded and switches to secure encrypted file storage (`~/.synteles/tokens.enc`). No manual intervention required.

If you're using an older version, upgrade to the latest version:
```powershell
uv tool install synteles-platform-mcp --force
```

Or if installed with pip:
```powershell
pip install synteles-platform-mcp --upgrade
```

**Issue**: uv not found after installation
- Restart PowerShell or run: `$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")`

### macOS

**Issue**: Permission denied
```bash
chmod +x deploy-macos.sh
```

**Issue**: uv not found after installation
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Common Issues

**Issue**: Claude Desktop doesn't show the MCP server
- Verify the config file exists and is valid JSON
- Check Claude Desktop logs: 
  - Windows: `%APPDATA%\Claude\logs`
  - macOS: `~/Library/Logs/Claude`

**Issue**: Authentication fails
- Ensure port 8888 is not blocked by firewall
- Check that `SYNTELES_API_DOMAIN` is correct
- Verify network connectivity to the API domain

**Issue**: SSL certificate errors (resolved in v0.1.0+)
```
Error: Could not find a suitable TLS CA certificate bundle
```

**This issue is automatically resolved in version 0.1.0+**

The MCP server now includes the `certifi` library for proper SSL certificate validation on all platforms. If you encounter this error, upgrade to the latest version (see [Updating](#updating) section).

## Manual Installation

If you prefer manual installation:

### 1. Install the package

```bash
# Using uv (recommended)
uv tool install synteles-platform-mcp

# Or using pip
pip install synteles-platform-mcp
```

### 2. Configure Claude Desktop

Edit the configuration file manually:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add:
```json
{
  "mcpServers": {
    "synteles-platform": {
      "command": "synteles-platform-mcp",
      "env": {
        "SYNTELES_API_DOMAIN": "api.synteles.dev",
        "SYNTELES_OAUTH_CALLBACK_PORT": "8888"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

## Updating

To update to a newer version:

```bash
# Windows (PowerShell) and macOS
uv tool install synteles-platform-mcp --force

# Or with pip
pip install synteles-platform-mcp --upgrade
```

Then restart Claude Desktop.

## Uninstallation

### Remove the package

```bash
uv tool uninstall synteles-platform-mcp
```

### Remove from Claude Desktop config

Edit the configuration file and remove the `synteles-platform` entry from `mcpServers`.

## Support

For issues or questions:
- Check the [troubleshooting section](#troubleshooting)
- Review Claude Desktop logs
- Contact Synteles support

## Security Notes

- OAuth tokens are stored securely using the system keyring (macOS Keychain, Windows Credential Manager, Linux Secret Service)
- **Windows**: Automatic fallback to AES-256 encrypted file storage if Credential Manager size limits are exceeded
  - Encrypted file location: `~/.synteles/tokens.enc`
  - Encryption key derived from machine-specific entropy (USERNAME + COMPUTERNAME)
  - Fully transparent to users - no configuration required
- The OAuth callback server only runs during authentication
- All API communication uses HTTPS with certificate validation (certifi library)
- Tokens are never logged or exposed
