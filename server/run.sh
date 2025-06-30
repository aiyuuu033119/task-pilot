#!/bin/bash

# MCP Server Run Script

echo "Starting MCP Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
pip install -r requirements.txt

# Set environment variables
export MCP_SERVER_HOST=${MCP_SERVER_HOST:-0.0.0.0}
export MCP_SERVER_PORT=${MCP_SERVER_PORT:-8001}

# Start the MCP server
echo "MCP Server running on http://$MCP_SERVER_HOST:$MCP_SERVER_PORT"
python mcp_server.py