# How to Run Client
**Date: June 30, 2025**
**Type: Running Instructions**

## Running the Client/Backend

### Prerequisites
1. **MCP Server must be running first** (on port 8001)
2. **API key configured** in `.env` file

### Quick Start (Automated)

#### Linux/macOS/WSL:
```bash
cd client
chmod +x run.sh  # Only needed first time
./run.sh
```

#### Windows:
```bash
cd client
run.bat
```

### Manual Method

#### Step 1: Navigate to client directory
```bash
cd client
```

#### Step 2: Configure environment (first time only)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or vim, notepad, etc.
```

Add at least one API key:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
# or
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

#### Step 3: Create virtual environment (first time only)
```bash
# Linux/macOS
python3 -m venv venv

# Windows
python -m venv venv
```

#### Step 4: Activate virtual environment
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### Step 5: Install dependencies (first time only)
```bash
pip install -r requirements.txt
```

#### Step 6: Run the client
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Success Indicators

When running correctly, you'll see:
```
INFO:     Will watch for changes in these directories: ['/path/to/client']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Accessing the Application

1. Open your web browser
2. Navigate to: **http://localhost:8000**
3. You should see the chat interface

### Verify It's Working

In another terminal:
```bash
# Check health endpoint
curl http://localhost:8000/health
```

Should return:
```json
{"status":"healthy"}
```

### Important Notes

- The client runs on **port 8000**
- It serves both the API and the frontend
- Keep this terminal open while using the app
- The client connects to MCP server on port 8001
- Press `Ctrl+C` to stop the client

### Environment Variables

The client uses these environment variables from `.env`:

**Required (at least one):**
- `OPENAI_API_KEY` - For GPT-4 access
- `ANTHROPIC_API_KEY` - For Claude access

**Optional:**
- `MCP_SERVER_HOST` - MCP server host (default: localhost)
- `MCP_SERVER_PORT` - MCP server port (default: 8001)
- `APP_HOST` - Client host (default: 0.0.0.0)
- `APP_PORT` - Client port (default: 8000)

### Troubleshooting

**"No API key found" error:**
```bash
# Check .env file exists and has keys
cat .env
# Make sure at least one API key is set
```

**"Connection refused to MCP server":**
```bash
# Ensure MCP server is running on port 8001
curl http://localhost:8001/health
```

**Port already in use:**
```bash
# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Permission denied:**
```bash
chmod +x run.sh
```

**Module not found:**
```bash
# Ensure virtual environment is activated
which python  # Should show venv path
# Reinstall dependencies
pip install -r requirements.txt
```

### Development Tips

1. **Auto-reload**: The `--reload` flag restarts the server when code changes
2. **Logs**: Watch the terminal for request logs and errors
3. **Database**: SQLite database is created automatically as `chatbot.db`
4. **Multiple models**: Add both OpenAI and Anthropic keys for flexibility

### What the Client Does

- **Serves the frontend** at http://localhost:8000
- **Provides WebSocket** endpoint for real-time chat
- **Manages conversations** with SQLite database
- **Connects to MCP server** for AI tools
- **Handles AI responses** with streaming support