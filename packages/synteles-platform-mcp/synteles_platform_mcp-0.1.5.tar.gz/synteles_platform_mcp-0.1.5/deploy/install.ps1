#!/usr/bin/env pwsh
# Quick installer - downloads and runs the full deployment script
param(
    [string]$ApiDomain,
    [string]$CallbackPort
)
$url = "https://raw.githubusercontent.com/Synteles/platform-mcp-server/main/deploy-windows.ps1"
$params = @{}
if ($ApiDomain) { $params.ApiDomain = $ApiDomain }
if ($CallbackPort) { $params.CallbackPort = $CallbackPort }
irm $url | iex @params
