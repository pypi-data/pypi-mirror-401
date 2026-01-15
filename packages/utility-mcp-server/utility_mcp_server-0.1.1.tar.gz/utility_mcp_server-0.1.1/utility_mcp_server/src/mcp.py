"""Utility MCP Server implementation.

This module contains the main Utility tools MCP Server class that provides
tools for MCP clients. It uses FastMCP to register and manage MCP capabilities.
"""

from fastmcp import FastMCP

from utility_mcp_server.src.settings import settings

# Import tools from the tools package
from utility_mcp_server.src.tools.release_notes_tool import (
    generate_release_notes,
)
from utility_mcp_server.utils.pylogger import (
    force_reconfigure_all_loggers,
    get_python_logger,
)

logger = get_python_logger()


class UtilityToolsMCPServer:
    """Main Utility Tools MCP Server implementation following tools-first architecture.

    This server provides only tools, not resources or prompts, adhering to
    the tools-first architectural pattern for MCP servers.
    """

    def __init__(self):
        """Initialize the MCP server with tools following tools-first architecture."""
        try:
            # Initialize FastMCP server
            self.mcp = FastMCP("utilitytools")

            # Force reconfigure all loggers after FastMCP initialization to ensure structured logging
            force_reconfigure_all_loggers(settings.PYTHON_LOG_LEVEL)

            self._register_mcp_tools()

            logger.info("Utility Tools MCP Server initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Utility MCP Server: {e}")
            raise

    def _register_mcp_tools(self) -> None:
        """Register MCP tools for utility operations (tools-first architecture).

        Registers all available tools with the FastMCP server instance.
        In tools-first architecture, the server only provides tools.
        Currently includes:
        - generate_release_notes: Release notes generation from git commits
        """
        self.mcp.tool()(generate_release_notes)
