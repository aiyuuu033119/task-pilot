#!/bin/bash

# Client/Backend Run Script

echo "Starting Client/Backend..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Copy .env.example to .env and add your API keys"
    
    # Create basic .env if it doesn't exist
    cat > .env << 'EOL'
# API Keys (set at least one)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# MCP Server URL
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001

# App Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
EOL
    echo "Created .env file. Please edit it with your API keys."
    exit 1
fi

# Source .env file
set -a
source .env
set +a

# Check for API keys
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: No API keys found in .env file!"
    echo "Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
pip install -r requirements.txt

# Set default values
export APP_HOST=${APP_HOST:-0.0.0.0}
export APP_PORT=${APP_PORT:-8000}

# Set PYTHONPATH to current directory
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Start the client/backend
echo "Client/Backend running on http://$APP_HOST:$APP_PORT"
echo "Frontend available at http://localhost:$APP_PORT"
python -m uvicorn app:app --host $APP_HOST --port $APP_PORT --reload