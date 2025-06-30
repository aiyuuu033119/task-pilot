# Component Separation Documentation
**Date: January 30, 2025**
**Type: Architecture/Refactor**

## Overview
Separated the monolithic application into three independent components that can be developed, deployed, and run separately.

## Changes Made

### 1. Independent Requirements
Created separate `requirements.txt` for each component:

- **server/requirements.txt**: MCP server dependencies only
  - fastapi, uvicorn, httpx, fastmcp
  
- **client/requirements.txt**: Backend/API dependencies
  - fastapi, uvicorn, websockets, pydantic-ai, openai, anthropic, aiosqlite
  
- **frontend/README.md**: No dependencies (static HTML/JS)

### 2. Individual Run Scripts
Each component now has its own run scripts:

- **Server**: `server/run.sh` and `server/run.bat`
- **Client**: `client/run.sh` and `client/run.bat`
- **Frontend**: Served by client or standalone nginx

### 3. Separate Docker Support
- Individual Dockerfiles in each folder
- New `docker-compose.separated.yml` for running components independently
- Each service can be built and deployed separately

### 4. Independent Configuration
- **Server**: Uses environment variables (MCP_SERVER_HOST/PORT)
- **Client**: Has its own `.env.example` file
- **Frontend**: Configuration embedded in HTML

## Running Instructions

### Running All Components Together

```bash
# Terminal 1: Start MCP Server
cd server
./run.sh  # or run.bat on Windows

# Terminal 2: Start Client/Backend (includes frontend)
cd client
./run.sh  # or run.bat on Windows

# Access at http://localhost:8000
```

### Running with Docker Compose

```bash
# Run all services
docker-compose -f docker-compose.separated.yml up

# Run specific service
docker-compose -f docker-compose.separated.yml up mcp-server
docker-compose -f docker-compose.separated.yml up client
```

### Running Components Individually

#### MCP Server Only
```bash
cd server
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python mcp_server.py
```

#### Client/Backend Only
```bash
cd client
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys
python -m uvicorn app:app --reload
```

#### Frontend Only
The frontend can be served by any static file server:
```bash
cd frontend
python -m http.server 8080
# or
npx serve .
```

## Benefits

1. **Independent Development**: Each team can work on their component
2. **Separate Deployment**: Components can be scaled independently
3. **Clear Dependencies**: Each component has only what it needs
4. **Easier Testing**: Components can be tested in isolation
5. **Flexible Architecture**: Components can be replaced or upgraded independently

## File Structure

```
pydantic-ai-mcp/
├── server/
│   ├── mcp_server.py
│   ├── requirements.txt
│   ├── run.sh / run.bat
│   ├── Dockerfile
│   └── README.md
├── client/
│   ├── app.py
│   ├── conversation_agent.py
│   ├── requirements.txt
│   ├── run.sh / run.bat
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md
├── frontend/
│   ├── index.html
│   ├── nginx.conf
│   ├── Dockerfile
│   └── README.md
└── docker-compose.separated.yml
```

## Migration Notes

- The original unified structure still exists for backward compatibility
- Both `docker-compose.yml` and `docker-compose.separated.yml` are available
- Choose the structure that best fits your deployment needs