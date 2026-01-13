"""Synteles Platfrom MCP Server."""

from importlib.metadata import version

from synteles_platform_mcp import server as main

__version__ = version("synteles-platform-mcp")
__all__ = ["main"]
