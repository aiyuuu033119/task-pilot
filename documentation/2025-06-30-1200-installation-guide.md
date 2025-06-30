# Installation and Running Guide
**Date: January 30, 2025**
**Type: Setup/Installation**

## Prerequisites

### System Requirements
- **Python**: 3.9 or higher
- **Operating System**: Windows, macOS, Linux, or WSL
- **Memory**: At least 4GB RAM recommended
- **Storage**: ~500MB free space

### API Requirements
You need at least ONE of the following:
- **OpenAI API Key**: For GPT-4 access
- **Anthropic API Key**: For Claude access

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/pydantic-ai-mcp.git
cd pydantic-ai-mcp
```

### Step 2: Set Up MCP Server

#### Option A: Using Run Script (Recommended)
```bash
cd server
./run.sh   # Linux/macOS/WSL
# or
run.bat    # Windows
```

This script will:
- Create a virtual environment
- Install dependencies
- Start the MCP server on port 8001

#### Option B: Manual Setup
```bash
cd server

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS/WSL
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python mcp_server.py
```

### Step 3: Set Up Client/Backend

#### Option A: Using Run Script (Recommended)
```bash
# In a new terminal
cd client

# First time only: Create .env file
cp .env.example .env

# Edit .env and add your API key(s)
# Use your preferred editor (nano, vim, notepad, etc.)
nano .env  # or vim .env

# Run the client
./run.sh   # Linux/macOS/WSL
# or
run.bat    # Windows
```

#### Option B: Manual Setup
```bash
cd client

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS/WSL
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create and configure .env
cp .env.example .env
# Edit .env with your API keys

# Run the application
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Step 4: Configure Environment Variables

Edit `client/.env` file:

```env
# Required: Set at least one API key
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Optional: Server configuration (defaults shown)
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001
APP_HOST=0.0.0.0
APP_PORT=8000
```

## Running the Application

### Quick Start (Two Terminals)

**Terminal 1 - MCP Server:**
```bash
cd server && ./run.sh
```

**Terminal 2 - Client/Backend:**
```bash
cd client && ./run.sh
```

**Access the application:**
Open http://localhost:8000 in your web browser

### Using Docker

#### Run All Components:
```bash
docker-compose -f docker-compose.separated.yml up
```

#### Run Components Individually:
```bash
# Just MCP Server
docker-compose -f docker-compose.separated.yml up mcp-server

# Just Client/Backend (in another terminal)
docker-compose -f docker-compose.separated.yml up client
```

## Verification

### 1. Check MCP Server
```bash
curl http://localhost:8001/health
# Expected: {"status":"healthy"}
```

### 2. Check Client/Backend
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### 3. Test the Chat Interface
1. Open http://localhost:8000 in your browser
2. You should see the chat interface
3. Type a message and press Enter
4. The AI should respond

## Troubleshooting

### Common Issues

#### 1. "Module not found" Error
**Solution:** Ensure you're in the correct directory and virtual environment is activated
```bash
# For server
cd server && source venv/bin/activate

# For client
cd client && source venv/bin/activate
```

#### 2. "Port already in use" Error
**Solution:** Find and kill the process using the port
```bash
# Linux/macOS
lsof -i :8000  # or :8001
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### 3. "API key not found" Error
**Solution:** Ensure .env file exists and contains valid API keys
```bash
cd client
cat .env  # Check if file exists and has keys
```

#### 4. WebSocket Connection Failed
**Solution:** Ensure both servers are running
- MCP server must be running on port 8001
- Client must be running on port 8000

#### 5. Permission Denied (Linux/macOS)
**Solution:** Make scripts executable
```bash
chmod +x server/run.sh client/run.sh
```

## Platform-Specific Notes

### Windows
- Use `run.bat` instead of `run.sh`
- Use `venv\Scripts\activate` instead of `source venv/bin/activate`
- Use Command Prompt or PowerShell (not Git Bash for .bat files)

### macOS
- May need to install Python via Homebrew: `brew install python@3.9`
- Use `python3` instead of `python` if needed

### Linux
- May need to install python3-venv: `sudo apt install python3-venv`
- Use `python3` instead of `python` if needed

### WSL (Windows Subsystem for Linux)
- Use Linux commands
- Access via `http://localhost:8000` from Windows browser
- Store project in WSL filesystem for better performance

## Development Mode

### Hot Reload
Both servers support hot reload in development:
- MCP Server: Automatically reloads on file changes
- Client: Uses `--reload` flag with uvicorn

### Running Without Scripts
```bash
# MCP Server
cd server
python -m uvicorn mcp_server:app --reload --host 0.0.0.0 --port 8001

# Client/Backend
cd client
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables
You can override defaults:
```bash
# Custom ports
MCP_SERVER_PORT=8002 python server/mcp_server.py
APP_PORT=8080 python -m uvicorn client.app:app --host 0.0.0.0 --port 8080
```

## Production Deployment

### Using Docker Compose
```bash
# Build and run in production mode
docker-compose -f docker-compose.separated.yml up -d

# View logs
docker-compose -f docker-compose.separated.yml logs -f

# Stop services
docker-compose -f docker-compose.separated.yml down
```

### Using systemd (Linux)
Create service files in `/etc/systemd/system/`:
- `mcp-server.service`
- `pydantic-ai-client.service`

### Using PM2 (Node.js Process Manager)
```bash
# Install PM2
npm install -g pm2

# Start services
pm2 start server/mcp_server.py --interpreter python3
pm2 start "cd client && python -m uvicorn app:app --host 0.0.0.0 --port 8000" --name client

# Save configuration
pm2 save
pm2 startup
```

## Next Steps

1. **Test the chat**: Send messages to verify everything works
2. **Add MCP tools**: Edit `server/mcp_server.py` to add custom tools
3. **Customize frontend**: Modify `frontend/index.html` for your needs
4. **Check logs**: Monitor terminal output for errors or warnings

## Support

If you encounter issues:
1. Check the [troubleshooting section](#troubleshooting) above
2. Review terminal output for error messages
3. Ensure all prerequisites are met
4. Check documentation in each component's README.md