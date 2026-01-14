#!/bin/bash
# MCP Server launcher for Vikunja
# This script is called by Claude Desktop via WSL

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use the script's directory (factumerit-bot repo)
cd "$SCRIPT_DIR"

# Run the MCP server using uv
exec /home/ivanadamin/.local/bin/uv run python -m vikunja_mcp.server

