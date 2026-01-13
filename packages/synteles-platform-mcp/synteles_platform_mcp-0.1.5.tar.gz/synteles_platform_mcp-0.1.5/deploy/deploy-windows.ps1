#!/usr/bin/env pwsh
# Synteles Platform MCP Server - Windows Deployment Script

param(
    [string]$ApiDomain = "api.synteles.dev",
    [string]$CallbackPort = "8888"
)

$ErrorActionPreference = "Stop"

Write-Host "=== Synteles Platform MCP Server Deployment ===" -ForegroundColor Cyan

# Check if uv is installed
Write-Host "`nChecking for uv..." -ForegroundColor Yellow
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv not found. Installing uv..." -ForegroundColor Yellow
    irm https://astral.sh/uv/install.ps1 | iex
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Install the package
Write-Host "`nInstalling synteles-platform-mcp..." -ForegroundColor Yellow
uv tool install synteles-platform-mcp --force

# Get uv tool bin path
$uvToolBin = & uv tool dir
$mcpCommand = Join-Path $uvToolBin "synteles-platform-mcp.exe"

# Claude Desktop config path
$claudeConfigDir = "$env:APPDATA\Claude"
$claudeConfigPath = Join-Path $claudeConfigDir "claude_desktop_config.json"

# Create config directory if it doesn't exist
if (!(Test-Path $claudeConfigDir)) {
    New-Item -ItemType Directory -Path $claudeConfigDir -Force | Out-Null
}

# Read existing config or create new
if (Test-Path $claudeConfigPath) {
    Write-Host "`nReading existing Claude Desktop config..." -ForegroundColor Yellow
    $configJson = Get-Content $claudeConfigPath -Raw | ConvertFrom-Json
    $config = @{
        mcpServers = @{}
    }
    if ($configJson.mcpServers) {
        foreach ($prop in $configJson.mcpServers.PSObject.Properties) {
            $config.mcpServers[$prop.Name] = $prop.Value
        }
    }
} else {
    $config = @{
        mcpServers = @{}
    }
}

# Add/update Synteles Platform MCP server config
Write-Host "`nConfiguring Claude Desktop..." -ForegroundColor Yellow
$config.mcpServers["synteles-platform"] = @{
    command = $mcpCommand
    env = @{
        SYNTELES_API_DOMAIN = $ApiDomain
        SYNTELES_OAUTH_CALLBACK_PORT = $CallbackPort
    }
}

# Write config
$config | ConvertTo-Json -Depth 10 | Set-Content $claudeConfigPath -Encoding UTF8

Write-Host "`n=== Deployment Complete ===" -ForegroundColor Green
Write-Host "`nConfiguration saved to: $claudeConfigPath" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Restart Claude Desktop" -ForegroundColor White
Write-Host "2. The Synteles Platform MCP server will be available" -ForegroundColor White
Write-Host "3. On first use, you'll be prompted to authenticate via OAuth" -ForegroundColor White
