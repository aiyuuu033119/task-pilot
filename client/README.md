# Client/Backend

FastAPI backend with Pydantic AI integration for the chatbot.

## Quick Start

### Prerequisites
- MCP Server must be running (default: http://localhost:8001)
- API key for OpenAI or Anthropic

### Option 1: Direct Run
```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Run
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

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run application
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Docker
```bash
docker build -t chatbot-client .
docker run -p 8000:8000 --env-file .env chatbot-client
```

## Configuration

Required in `.env`:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (at least one)

Optional:
- `MCP_SERVER_HOST`: MCP server host (default: localhost)
- `MCP_SERVER_PORT`: MCP server port (default: 8001)
- `APP_HOST`: App host (default: 0.0.0.0)
- `APP_PORT`: App port (default: 8000)

## Features

- WebSocket-based real-time chat
- Conversation memory with SQLite
- Automatic model selection (GPT-4 or Claude)
- MCP tool integration
- Streaming responses

## API Endpoints

- `GET /` - Serves frontend
- `GET /health` - Health check
- `GET /conversation/{conversation_id}` - Get conversation history
- `POST /conversation` - Create new conversation
- `WebSocket /ws` - Real-time chat endpoint

## Architecture

```
Frontend (WebSocket) → FastAPI Backend → Pydantic AI Agent
                                      ↓
                                  MCP Client → MCP Server
```

## File Structure

- `app.py` - FastAPI application and WebSocket handler
- `conversation_agent.py` - Main AI agent with tools
- `config.py` - Configuration and model selection
- `database.py` - SQLite database for chat history
- `mcp_client.py` - MCP client for tool integration

## Development

Run with different models:
```bash
# Use GPT-4
OPENAI_API_KEY=your_key python -m uvicorn app:app --reload

# Use Claude
ANTHROPIC_API_KEY=your_key python -m uvicorn app:app --reload
```

## Testing

```bash
# Test health
curl http://localhost:8000/health

# Test WebSocket (use frontend or wscat)
wscat -c ws://localhost:8000/ws
```