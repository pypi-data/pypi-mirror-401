"""Main entry point for the Synteles Platform MCP Server when run as a module."""

import logging

from synteles_platform_mcp.server import mcp


def main() -> None:
    r"""Run the MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
