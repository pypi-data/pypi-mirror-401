"""Tests for the MCP server module."""

from unittest.mock import Mock, patch

import pytest

from utility_mcp_server.src.mcp import UtilityToolsMCPServer


class TestUtilityToolsMCPServer:
    """Test the UtilityMCPServer class."""

    @patch("utility_mcp_server.src.mcp.force_reconfigure_all_loggers")
    @patch("utility_mcp_server.src.mcp.settings")
    @patch("utility_mcp_server.src.mcp.FastMCP")
    @patch("utility_mcp_server.src.mcp.logger")
    def test_init_success(
        self, mock_logger, mock_fastmcp, mock_settings, mock_force_reconfigure
    ):
        """Test successful initialization of UtilityMCPServer."""
        # Arrange
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        mock_settings.PYTHON_LOG_LEVEL = "INFO"

        # Act
        server = UtilityToolsMCPServer()

        # Assert
        assert server.mcp == mock_mcp
        mock_logger.info.assert_called_with(
            "Utility Tools MCP Server initialized successfully"
        )
        # In tools-first architecture, we only register tools
        mock_mcp.tool.assert_called()

    @patch("utility_mcp_server.src.mcp.force_reconfigure_all_loggers")
    @patch("utility_mcp_server.src.mcp.settings")
    @patch("utility_mcp_server.src.mcp.FastMCP")
    @patch("utility_mcp_server.src.mcp.logger")
    def test_init_failure(
        self, mock_logger, mock_fastmcp, mock_settings, mock_force_reconfigure
    ):
        """Test initialization failure handling."""
        # Arrange
        mock_fastmcp.side_effect = Exception("Test error")
        mock_settings.PYTHON_LOG_LEVEL = "INFO"

        # Act & Assert
        with pytest.raises(Exception, match="Test error"):
            UtilityToolsMCPServer()

        mock_logger.error.assert_called_with(
            "Failed to initialize Utility MCP Server: Test error"
        )

    @patch("utility_mcp_server.src.mcp.force_reconfigure_all_loggers")
    @patch("utility_mcp_server.src.mcp.settings")
    @patch("utility_mcp_server.src.mcp.FastMCP")
    def test_register_mcp_tools(
        self, mock_fastmcp, mock_settings, mock_force_reconfigure
    ):
        """Test MCP tools registration."""
        # Arrange
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        mock_settings.PYTHON_LOG_LEVEL = "INFO"
        server = UtilityToolsMCPServer()

        # Act
        server._register_mcp_tools()

        # Assert
        mock_mcp.tool.assert_called()

    @patch("utility_mcp_server.src.mcp.force_reconfigure_all_loggers")
    @patch("utility_mcp_server.src.mcp.settings")
    @patch("utility_mcp_server.src.mcp.FastMCP")
    def test_register_mcp_tools_functionality(
        self, mock_fastmcp, mock_settings, mock_force_reconfigure
    ):
        """Test that MCP tools registration includes all expected tools."""
        # Arrange
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        mock_settings.PYTHON_LOG_LEVEL = "INFO"
        server = UtilityToolsMCPServer()

        # Act
        server._register_mcp_tools()

        # Assert
        # Verify that tool() was called (for generate_release_notes)
        assert mock_mcp.tool.call_count >= 1

    def test_server_attributes(self):
        """Test that server has required attributes for tools-first architecture."""
        # Arrange & Act
        with (
            patch("utility_mcp_server.src.mcp.settings") as mock_settings,
            patch("utility_mcp_server.src.mcp.FastMCP"),
            patch("utility_mcp_server.src.mcp.force_reconfigure_all_loggers"),
        ):
            mock_settings.PYTHON_LOG_LEVEL = "INFO"
            server = UtilityToolsMCPServer()

        # Assert
        assert hasattr(server, "mcp")
        assert hasattr(server, "_register_mcp_tools")

    def test_tools_first_architecture_compliance(self):
        """Test that server adheres to tools-first architecture by not having resource/prompt methods."""
        # Arrange & Act
        with (
            patch("utility_mcp_server.src.mcp.settings") as mock_settings,
            patch("utility_mcp_server.src.mcp.FastMCP"),
            patch("utility_mcp_server.src.mcp.force_reconfigure_all_loggers"),
        ):
            mock_settings.PYTHON_LOG_LEVEL = "INFO"
            server = UtilityToolsMCPServer()

        # Assert - These methods should NOT exist in tools-first architecture
        assert not hasattr(server, "_register_mcp_resources"), (
            "_register_mcp_resources should not exist in tools-first architecture"
        )
        assert not hasattr(server, "_register_mcp_prompts"), (
            "_register_mcp_prompts should not exist in tools-first architecture"
        )
