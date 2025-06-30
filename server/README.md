# MCP Server

Model Context Protocol (MCP) server providing tools for the AI chatbot.

## Quick Start

### Option 1: Direct Run
```bash
./run.sh      # Linux/macOS
run.bat       # Windows
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python mcp_server.py
```

### Option 3: Docker
```bash
docker build -t mcp-server .
docker run -p 8001:8001 mcp-server
```

## Configuration

Environment variables:
- `MCP_SERVER_HOST`: Host to bind to (default: 0.0.0.0)
- `MCP_SERVER_PORT`: Port to listen on (default: 8001)

## Available Tools

The server provides these tools via MCP:

1. **calculator** - Evaluate mathematical expressions
2. **get_datetime** - Get current date and time
3. **weather** - Get weather information (mock data)
4. **web_search** - Search the web (mock implementation)
5. **create_note** - Create a note
6. **read_notes** - Read saved notes

## API Endpoints

- `GET /health` - Health check
- `GET /tools` - List available tools
- MCP protocol endpoints for tool execution

## Adding New Tools

Edit `mcp_server.py` and add:

```python
@mcp.tool()
async def your_tool(param: str) -> Dict[str, Any]:
    """Tool description"""
    return {"result": "..."}
```

## Development

Run with auto-reload:
```bash
uvicorn mcp_server:app --reload --host 0.0.0.0 --port 8001
```

## Testing

```bash
# Test health endpoint
curl http://localhost:8001/health

# Test tools endpoint  
curl http://localhost:8001/tools
```