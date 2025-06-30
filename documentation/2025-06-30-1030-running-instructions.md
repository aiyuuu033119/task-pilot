# Running Instructions
**Date: January 30, 2025**

## Quick Start (Recommended)

### Option 1: Using Start Scripts (Easiest)

#### Linux/macOS/WSL:
```bash
# First time setup
./setup.sh

# Run everything
./start.sh
```

#### Windows:
```bash
# First time setup
setup.bat

# Run everything
start.bat
```

This will:
- Start MCP server on port 8001
- Start backend/client on port 8000
- Frontend is served by the backend

**Access the application at: http://localhost:8000**

---

## Manual Start (Individual Components)

### Prerequisites
1. Create and activate virtual environment:
```bash
# Linux/macOS/WSL
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
# Copy example and edit with your API keys
cp .env.example .env
# Edit .env and add OPENAI_API_KEY or ANTHROPIC_API_KEY
```

### Starting Each Component

#### 1. MCP Server (Required First)
```bash
# Terminal 1
python server/mcp_server.py
```
- Runs on: http://localhost:8001
- Provides tools for the AI agent
- Must be running before starting the client

#### 2. Backend/Client (FastAPI + Pydantic AI)
```bash
# Terminal 2
python -m uvicorn client.app:app --reload --host 0.0.0.0 --port 8000

# Or alternatively:
cd client && python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
- Runs on: http://localhost:8000
- Serves both API and frontend
- WebSocket endpoint for real-time chat

#### 3. Frontend
The frontend is automatically served by the FastAPI backend at http://localhost:8000
- No separate process needed
- Access directly in browser
- Real-time chat interface with WebSocket

---

## Docker Option

### Development Mode:
```bash
docker-compose up
```

### Production Mode (with Nginx):
```bash
docker-compose --profile production up
```

### Individual Services:
```bash
# Just MCP server
docker-compose up mcp-server

# Just backend/client
docker-compose up chatbot-backend

# With Nginx proxy
docker-compose --profile production up nginx
```

---

## Verification Steps

1. **Check MCP Server**:
   ```bash
   curl http://localhost:8001/health
   ```
   Should return: `{"status":"healthy"}`

2. **Check Backend**:
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy"}`

3. **Test Frontend**:
   - Open http://localhost:8000 in browser
   - You should see the chat interface
   - Try sending a message

---

## Common Issues

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill the process or use different ports in .env
```

### API Key Issues
- Ensure .env file exists and contains valid API keys
- At least one of OPENAI_API_KEY or ANTHROPIC_API_KEY must be set

### Module Import Errors
```bash
# Ensure you're in the project root
pwd  # Should show .../pydantic-ai-mcp

# Check PYTHONPATH includes current directory
export PYTHONPATH="${PWD}:${PYTHONPATH}"
```

### WebSocket Connection Failed
- Ensure both MCP server and backend are running
- Check browser console for errors
- Try refreshing the page

---

## Architecture Overview

```
Browser (Frontend)
    ↓ WebSocket
FastAPI Backend (port 8000)
    ↓ HTTP/SSE
MCP Server (port 8001)
    ↓
External Tools (weather, search, etc.)
```

## Stopping the Application

### If using start scripts:
Press `Ctrl+C` in the terminal

### If running manually:
Press `Ctrl+C` in each terminal window

### If using Docker:
```bash
docker-compose down
```