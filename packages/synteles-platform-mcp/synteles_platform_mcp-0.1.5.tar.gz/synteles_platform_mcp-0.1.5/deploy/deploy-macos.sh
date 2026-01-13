#!/bin/bash
# Synteles Platform MCP Server - macOS Deployment Script

set -e

API_DOMAIN="${1:-api.synteles.dev}"
CALLBACK_PORT="${2:-8888}"

echo "=== Synteles Platform MCP Server Deployment ==="

# Check if uv is installed
echo -e "\nChecking for uv..."
if ! command -v uv &> /dev/null; then
    echo "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install the package
echo -e "\nInstalling synteles-platform-mcp..."
uv tool install synteles-platform-mcp --force

# Get uv tool bin path
UV_TOOL_BIN=$(uv tool dir)
MCP_COMMAND="$UV_TOOL_BIN/synteles-platform-mcp"

# Claude Desktop config path
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_PATH="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# Create config directory if it doesn't exist
mkdir -p "$CLAUDE_CONFIG_DIR"

# Read existing config or create new
if [ -f "$CLAUDE_CONFIG_PATH" ]; then
    echo -e "\nReading existing Claude Desktop config..."
    CONFIG=$(cat "$CLAUDE_CONFIG_PATH")
else
    CONFIG='{"mcpServers":{}}'
fi

# Add/update Synteles Platform MCP server config using jq or python
echo -e "\nConfiguring Claude Desktop..."
if command -v jq &> /dev/null; then
    # Use jq if available
    echo "$CONFIG" | jq --arg cmd "$MCP_COMMAND" --arg domain "$API_DOMAIN" --arg port "$CALLBACK_PORT" \
        '.mcpServers["synteles-platform"] = {
            "command": $cmd,
            "env": {
                "SYNTELES_API_DOMAIN": $domain,
                "SYNTELES_OAUTH_CALLBACK_PORT": $port
            }
        }' > "$CLAUDE_CONFIG_PATH"
else
    # Fallback to python
    python3 << EOF
import json
import sys

config = json.loads('''$CONFIG''')
if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['synteles-platform'] = {
    'command': '$MCP_COMMAND',
    'env': {
        'SYNTELES_API_DOMAIN': '$API_DOMAIN',
        'SYNTELES_OAUTH_CALLBACK_PORT': '$CALLBACK_PORT'
    }
}

with open('$CLAUDE_CONFIG_PATH', 'w') as f:
    json.dump(config, f, indent=2)
EOF
fi

echo -e "\n=== Deployment Complete ==="
echo -e "\nConfiguration saved to: $CLAUDE_CONFIG_PATH"
echo -e "\nNext steps:"
echo "1. Restart Claude Desktop"
echo "2. The Synteles Platform MCP server will be available"
echo "3. On first use, you'll be prompted to authenticate via OAuth"
