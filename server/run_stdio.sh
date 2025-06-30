#!/bin/bash

# MCP Server Run Script for Claude Desktop (stdio)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
pip install -q mcp httpx

# Run the MCP server with stdio transport
python3 mcp_server_stdio.py