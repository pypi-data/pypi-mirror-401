"""Stdio entry point for the Utility MCP Server.

This module provides a stdio-based entry point for MCP servers that need to
communicate via standard input/output, such as Cursor IDE integration.
"""

import sys

from utility_mcp_server.src.mcp import UtilityToolsMCPServer
from utility_mcp_server.src.settings import settings
from utility_mcp_server.utils.pylogger import (
    force_reconfigure_all_loggers,
    get_python_logger,
)

logger = get_python_logger()


def main() -> None:
    """Main entry point for stdio-based MCP server.

    Initializes the MCP server and runs it via stdio transport for
    integration with Cursor IDE and other stdio-based MCP clients.
    """
    try:
        force_reconfigure_all_loggers(settings.PYTHON_LOG_LEVEL)
        logger.info("Starting Utility Tools MCP Server in stdio mode")

        server = UtilityToolsMCPServer()

        logger.info("Utility MCP Server initialized, running via stdio")

        server.mcp.run()

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
