# Complete Setup and Running Guide
**Date: January 30, 2025**
**Type: Installation/Setup**

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Process](#installation-process)
3. [Running the MCP Server](#running-the-mcp-server)
4. [Running the Client/Backend](#running-the-clientbackend)
5. [Running the Frontend](#running-the-frontend)
6. [Verification](#verification)
7. [Common Issues](#common-issues)

## Prerequisites

### System Requirements
- **Python**: 3.9 or higher
- **Git**: For cloning the repository
- **Text Editor**: To edit configuration files

### API Keys
You need at least ONE of:
- **OpenAI API Key**: Sign up at https://platform.openai.com
- **Anthropic API Key**: Sign up at https://console.anthropic.com

## Installation Process

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/pydantic-ai-mcp.git
cd pydantic-ai-mcp
```

### Step 2: Project Structure Overview
```
pydantic-ai-mcp/
├── server/          # MCP Server (runs on port 8001)
├── client/          # Backend API (runs on port 8000)
├── frontend/        # Web interface (served by client)
└── documentation/   # Project docs
```

## Running the MCP Server

The MCP (Model Context Protocol) server provides tools for the AI agent.

### Option 1: Automated Setup (Recommended)

#### Linux/macOS/WSL:
```bash
cd server
chmod +x run.sh  # Make script executable (first time only)
./run.sh
```

#### Windows:
```bash
cd server
run.bat
```

### Option 2: Manual Setup

#### Step 1: Navigate to server directory
```bash
cd server
```

#### Step 2: Create virtual environment
```bash
# Linux/macOS/WSL
python3 -m venv venv

# Windows
python -m venv venv
```

#### Step 3: Activate virtual environment
```bash
# Linux/macOS/WSL
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Run the server
```bash
python mcp_server.py
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Verify MCP Server
```bash
# In a new terminal
curl http://localhost:8001/health
# Should return: {"status":"healthy"}
```

## Running the Client/Backend

The client serves the API and WebSocket connections for the chat interface.

### Option 1: Automated Setup (Recommended)

#### Linux/macOS/WSL:
```bash
# Open a new terminal (keep MCP server running)
cd client
chmod +x run.sh  # Make script executable (first time only)

# First time: Configure API keys
cp .env.example .env
nano .env  # or use any editor

# Run the client
./run.sh
```

#### Windows:
```bash
# Open a new terminal (keep MCP server running)
cd client

# First time: Configure API keys
copy .env.example .env
notepad .env  # Edit and save

# Run the client
run.bat
```

### Option 2: Manual Setup

#### Step 1: Navigate to client directory
```bash
cd client
```

#### Step 2: Create and configure .env file
```bash
cp .env.example .env  # Linux/macOS
# or
copy .env.example .env  # Windows
```

Edit `.env` file:
```env
# Add your API key (at least one required)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
# or
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# Server configuration (defaults)
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001
APP_HOST=0.0.0.0
APP_PORT=8000
```

#### Step 3: Create virtual environment
```bash
# Linux/macOS/WSL
python3 -m venv venv

# Windows
python -m venv venv
```

#### Step 4: Activate virtual environment
```bash
# Linux/macOS/WSL
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### Step 5: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 6: Run the client
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/client']
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Verify Client/Backend
```bash
# In a new terminal
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

## Running the Frontend

The frontend is automatically served by the client/backend. No separate process needed!

### Accessing the Frontend

1. Ensure both MCP server (port 8001) and client (port 8000) are running
2. Open your web browser
3. Navigate to: **http://localhost:8000**

### Alternative: Standalone Frontend (Optional)

If you want to run the frontend separately:

#### Using Python HTTP Server:
```bash
cd frontend
python -m http.server 8080
# Access at http://localhost:8080
```

#### Using Node.js (if installed):
```bash
cd frontend
npx serve .
# Access at provided URL
```

#### Using Docker:
```bash
cd frontend
docker build -t frontend .
docker run -p 80:80 frontend
# Access at http://localhost
```

## Verification

### Full System Check

1. **Check all services are running:**
   - MCP Server: http://localhost:8001/health
   - Client/Backend: http://localhost:8000/health
   - Frontend: http://localhost:8000

2. **Test the chat interface:**
   - Open http://localhost:8000
   - Type "Hello" in the chat box
   - Press Enter or click Send
   - You should receive a response

3. **Test MCP tools:**
   - Type "What's 2+2?" (tests calculator tool)
   - Type "What's the current time?" (tests datetime tool)

## Common Issues

### Issue 1: "Port already in use"

**Error:**
```
[Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port
lsof -i :8000  # or :8001
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue 2: "No module named 'fastapi'"

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: "API key not found"

**Error:**
```
ValueError: No API keys found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY
```

**Solution:**
1. Check `.env` file exists in client directory
2. Ensure API key is set correctly
3. Restart the client after editing .env

### Issue 4: "Connection refused" in browser

**Solution:**
1. Ensure MCP server is running (port 8001)
2. Ensure client is running (port 8000)
3. Check firewall settings
4. Try http://127.0.0.1:8000 instead of localhost

### Issue 5: "WebSocket connection failed"

**Solution:**
1. Check browser console for errors
2. Ensure both servers are running
3. Try refreshing the page
4. Check for proxy/VPN interference

## Process Summary

### Quick Reference - Three Terminals:

**Terminal 1 - MCP Server:**
```bash
cd server && ./run.sh
```

**Terminal 2 - Client/Backend:**
```bash
cd client && ./run.sh
```

**Terminal 3 - Your Browser:**
```
http://localhost:8000
```

### Docker Alternative (Single Terminal):
```bash
# Ensure .env is configured in client/
docker-compose -f docker-compose.separated.yml up
```

## Tips

1. **Keep terminals open**: Both servers need to run simultaneously
2. **Check logs**: Error messages appear in terminal windows
3. **API keys**: Store securely, never commit to git
4. **Development**: Use `--reload` flag for auto-restart on code changes
5. **Production**: Use Docker or process managers like PM2

## Next Steps

1. **Test the chat**: Send various messages to test functionality
2. **Explore tools**: Try math calculations, time queries, etc.
3. **Customize**: Modify `server/mcp_server.py` to add new tools
4. **Style**: Edit `frontend/index.html` to customize appearance