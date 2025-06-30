# Pydantic AI Chatbot with MCP

A modern chatbot application built with Pydantic AI and Model Context Protocol (MCP) integration.

## Architecture

Three independent components:
- **Server**: MCP Server providing AI tools via FastMCP
- **Client**: FastAPI backend with Pydantic AI and WebSocket support  
- **Frontend**: Modern React app with Next.js, TypeScript, and Tailwind CSS

## Project Structure

```
.
├── server/              # MCP Server (independent)
│   ├── mcp_server.py   # Tool definitions
│   ├── requirements.txt # Server dependencies
│   ├── run.sh/bat      # Run scripts
│   └── README.md       # Server documentation
├── client/              # Backend/API (independent)
│   ├── app.py          # FastAPI + WebSocket
│   ├── conversation_agent.py  # AI agent logic
│   ├── requirements.txt # Client dependencies
│   ├── .env.example    # Configuration template
│   ├── run.sh/bat      # Run scripts
│   └── README.md       # Client documentation
├── frontend/            # Next.js React application
│   ├── src/            # Source code
│   ├── package.json    # Dependencies
│   └── README.md       # Frontend documentation
└── documentation/       # Project documentation
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI or Anthropic API key

### Setup

1. **Configure API Keys**:
   ```bash
   cd client
   cp .env.example .env
   # Edit .env and add your API key:
   # OPENAI_API_KEY=sk-... or ANTHROPIC_API_KEY=sk-ant-...
   cd ..
   ```

2. **Install Dependencies**:
   ```bash
   # Server
   cd server && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   cd ..

   # Client
   cd client && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   cd ..

   # Frontend
   cd frontend && npm install
   cd ..
   ```

### Running the Application

Start all three services:

```bash
# Terminal 1: MCP Server (port 8001)
cd server && ./run.sh

# Terminal 2: Backend API (port 8000)
cd client && ./run.sh

# Terminal 3: Frontend (port 3000)
cd frontend && npm run dev
```

Open http://localhost:3000 in your browser.

## Docker

```bash
# Run all components
docker-compose -f docker-compose.separated.yml up

# Run specific component
docker-compose -f docker-compose.separated.yml up mcp-server
docker-compose -f docker-compose.separated.yml up client
```

## Adding MCP Tools

Edit `server/mcp_server.py`:

```python
@mcp.tool()
async def your_tool(param: str) -> Dict[str, Any]:
    """Tool description"""
    return {"result": "..."}
```

## Testing

```bash
python test_app.py
```

## License

MIT