# Setting up Utility MCP Server in Cursor IDE

This guide explains how to configure and use the Utility MCP Server in Cursor IDE.

## ⚠️ Quick Fix: Command Not Found Error

If you see `spawn utility-mcp-server-stdio ENOENT` error, the command isn't in your PATH. **Use this configuration instead:**

```json
{
  "mcpServers": {
    "utility-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "utility_mcp_server.src.stdio_main"
      ]
    }
  }
}
```

**Or if using a virtual environment**, use the full path to your Python executable:

```json
{
  "mcpServers": {
    "utility-mcp-server": {
      "command": "/path/to/your/venv/bin/python",
      "args": [
        "-m",
        "utility_mcp_server.src.stdio_main"
      ]
    }
  }
}
```

To find your Python path:
```bash
which python  # or: which python3
```

## Prerequisites

1. **Python 3.12+** installed on your system
2. **Utility MCP Server** installed (see main README.md for installation instructions)
3. **Cursor IDE** installed and running

## Installation

1. **Install the MCP server** (if not already installed):

   ```bash
   # Using uv (recommended)
   uv pip install -e .

   # Or using pip
   pip install -e .
   ```

2. **Verify installation**:

   ```bash
   # Check if the stdio command is available
   which utility-mcp-server-stdio
   # Or
   python -m utility_mcp_server.src.stdio_main --help
   ```

## Configuration in Cursor

### Method 1: Using Cursor Settings UI

1. **Open Cursor Settings**:
   - Navigate to `File` > `Preferences` > `Cursor Settings` (or `Cmd+,` on Mac / `Ctrl+,` on Windows/Linux)

2. **Add MCP Server**:
   - In the left sidebar, select `Tools & Integrations`
   - Scroll to the `MCP Tools` section
   - Click `New MCP Server` or `Add MCP Server`

3. **Configure the Server**:
   - The configuration file (`mcp.json`) will open
   - Add the following configuration:

   ```json
   {
     "mcpServers": {
       "utility-mcp-server": {
         "command": "utility-mcp-server-stdio",
         "args": []
       }
     }
   }
   ```

   **Note**: If the `utility-mcp-server-stdio` command is not in your PATH, use the full path:

   ```json
   {
     "mcpServers": {
       "utility-mcp-server": {
         "command": "python",
         "args": [
           "-m",
           "utility_mcp_server.src.stdio_main"
         ]
       }
     }
   }
   ```

   Or if using a virtual environment:

   ```json
   {
     "mcpServers": {
       "utility-mcp-server": {
         "command": "/path/to/venv/bin/python",
         "args": [
           "-m",
           "utility_mcp_server.src.stdio_main"
         ]
       }
     }
   }
   ```

### Method 2: Manual Configuration

1. **Locate Cursor's MCP configuration file**:
   - **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
   - **Windows**: `%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
   - **Linux**: `~/.config/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

2. **Edit the configuration file**:
   - Open the file in a text editor
   - Add or update the `mcpServers` section:

   ```json
   {
     "mcpServers": {
       "utility-mcp-server": {
         "command": "utility-mcp-server-stdio",
         "args": []
       }
     }
   }
   ```

3. **Save the file** and restart Cursor

## Verification

1. **Restart Cursor** to load the new MCP server configuration

2. **Test the MCP server**:
   - Open Cursor's AI chat (press `Ctrl+L` or `Cmd+L`)
   - Try using one of the available tools:
     - `generate_release_notes`: "Generate release notes for version v0.50.0"

3. **Check MCP server status**:
   - In Cursor settings, verify the MCP server is listed and enabled
   - Check Cursor's developer console for any errors (Help > Toggle Developer Tools)

## Available Tools

The Utility MCP Server provides the following tools:

1. **`generate_release_notes`**: Generate release notes from git commits
   - Parameters:
     - `version` (string, required): Current version tag (e.g., "v0.50.0")
     - `previous_version` (string, optional): Previous version tag
     - `repo_path` (string, optional): Path to git repository
     - `repo_url` (string, optional): Repository URL for links
     - `release_date` (string, optional): Release date in "Month Day, Year" format
   - Example: "Generate release notes for version v0.50.0 with previous version v0.49.0"

## Troubleshooting

### MCP Server Not Appearing

1. **Check command path**:
   - Verify the command is in your PATH
   - Use absolute paths if needed
   - Ensure virtual environment is activated if using one

2. **Check Python version**:
   ```bash
   python --version  # Should be 3.12 or higher
   ```

3. **Verify installation**:
   ```bash
   python -m utility_mcp_server.src.stdio_main
   ```

### MCP Server Not Responding

1. **Check Cursor logs**:
   - Open Developer Tools (Help > Toggle Developer Tools)
   - Check the Console tab for errors

2. **Test stdio manually**:
   ```bash
   echo '{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}' | python -m utility_mcp_server.src.stdio_main
   ```

3. **Check permissions**:
   - Ensure the Python executable has execute permissions
   - Check file permissions on the MCP server files

### Common Issues

1. **"Command not found"**:
   - Use full path to Python executable
   - Or use `python -m utility_mcp_server.src.stdio_main` instead

2. **"Module not found"**:
   - Ensure the package is installed: `pip install -e .`
   - Check virtual environment is activated

3. **"Permission denied"**:
   - Check file permissions
   - Ensure Python executable is accessible

## Advanced Configuration

### Using Environment Variables

You can configure the MCP server using environment variables:

```json
{
  "mcpServers": {
    "utility-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "utility_mcp_server.src.stdio_main"
      ],
      "env": {
        "PYTHON_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Custom Working Directory

If you need to run the server from a specific directory:

```json
{
  "mcpServers": {
    "utility-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "utility_mcp_server.src.stdio_main"
      ],
      "cwd": "/path/to/working/directory"
    }
  }
}
```

## Additional Resources

- [Cursor MCP Documentation](https://cursor.directory/mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## Support

For issues or questions:
- Check the main [README.md](README.md) for general information
- Open an issue on [GitHub](https://github.com/redhat-data-and-ai/utility-mcp-server/issues)
