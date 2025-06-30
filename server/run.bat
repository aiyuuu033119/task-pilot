@echo off
REM MCP Server Run Script for Windows

echo Starting MCP Server...

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install/upgrade dependencies
pip install -r requirements.txt

REM Set environment variables
if "%MCP_SERVER_HOST%"=="" set MCP_SERVER_HOST=0.0.0.0
if "%MCP_SERVER_PORT%"=="" set MCP_SERVER_PORT=8001

REM Start the MCP server
echo MCP Server running on http://%MCP_SERVER_HOST%:%MCP_SERVER_PORT%
python mcp_server.py