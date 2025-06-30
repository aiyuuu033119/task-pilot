# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Pydantic AI Chatbot with Model Context Protocol (MCP) integration. It consists of three independent components:
- **Server**: MCP Server (FastAPI) providing extensible tools via HTTP/SSE
- **Client**: FastAPI backend with Pydantic AI, WebSocket support, and SQLite database
- **Frontend**: Web-based chat interface (served by the client)

## Project Structure

```
.
├── server/              # MCP Server (independent)
│   ├── mcp_server.py   # Tool definitions
│   ├── requirements.txt # Server-specific dependencies
│   └── run.sh/bat      # Run scripts
├── client/              # Backend/API (independent)
│   ├── app.py          # FastAPI + WebSocket
│   ├── requirements.txt # Client-specific dependencies
│   ├── .env.example    # Configuration template
│   └── run.sh/bat      # Run scripts
├── frontend/            # Static web interface
│   └── index.html      # Chat UI (served by client)
└── documentation/       # Project documentation
```

## Essential Commands

```bash
# Running Components Separately (Recommended)

# Terminal 1: Start MCP Server
cd server
./run.sh              # Linux/macOS/WSL
run.bat               # Windows

# Terminal 2: Start Client/Backend (includes frontend)
cd client
./run.sh              # Linux/macOS/WSL
run.bat               # Windows

# Access frontend at http://localhost:8000

# Docker (all components)
docker-compose -f docker-compose.separated.yml up
```

## Architecture

### Component Communication Flow
1. **Frontend** (index.html) → WebSocket → **FastAPI Backend** (client/app.py)
2. **Backend** → **Pydantic AI Agent** (client/conversation_agent.py) → Processes with context
3. **Agent** can use:
   - Local tools (datetime, calculator)
   - MCP Server tools via HTTP (weather, web search, notes)
4. **Database** (SQLite) stores conversation history persistently

### Key Files

**Server Component:**
- `server/mcp_server.py`: MCP server with extensible tools
- `server/requirements.txt`: Server dependencies (fastmcp, fastapi, etc.)

**Client Component:**
- `client/app.py`: FastAPI backend with WebSocket streaming
- `client/conversation_agent.py`: Core AI agent with tool integration
- `client/config.py`: Configuration and model selection logic
- `client/requirements.txt`: Client dependencies (pydantic-ai, openai, etc.)

**Frontend Component:**
- `frontend/index.html`: Complete chat interface

### Adding New MCP Tools
Edit `server/mcp_server.py` and add:
```python
@mcp.tool()
async def your_tool(param: str) -> Dict[str, Any]:
    """Tool description"""
    return {"result": "..."}
```

## Development Notes

### Environment Variables
Required in `client/.env`:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (at least one)
- Optional: `MCP_SERVER_HOST`, `MCP_SERVER_PORT`, `APP_HOST`, `APP_PORT`

Copy `client/.env.example` to `client/.env` and configure your API keys.

### Model Selection
The system automatically selects:
- GPT-4 if `OPENAI_API_KEY` is set
- Claude-3-5-sonnet if `ANTHROPIC_API_KEY` is set
- Prioritizes OpenAI if both are available

### Component Independence
- Each component has its own `requirements.txt` and can be developed independently
- Server runs on port 8001, Client on port 8000
- Components communicate via HTTP/WebSocket

### Running Individual Components
- Server: `cd server && ./run.sh`
- Client: `cd client && ./run.sh` (requires server to be running)
- Frontend: Automatically served by client at http://localhost:8000

### WSL Considerations
- Use WSL file system for better performance
- Access via `http://localhost:8000` from Windows browser
- Ensure scripts are executable: `chmod +x *.sh`