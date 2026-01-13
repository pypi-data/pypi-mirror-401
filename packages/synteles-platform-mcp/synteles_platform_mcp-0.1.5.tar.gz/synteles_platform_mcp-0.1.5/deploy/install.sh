#!/bin/bash
# Quick installer - downloads and runs the full deployment script
curl -fsSL https://raw.githubusercontent.com/Synteles/platform-mcp-server/main/deploy-macos.sh | bash -s -- "$@"
