# How to Run Server
**Date: January 30, 2025**
**Type: Running Instructions**

## Running the MCP Server

### Quick Start (Automated)

#### Linux/macOS/WSL:
```bash
cd server
chmod +x run.sh  # Only needed first time
./run.sh
```

#### Windows:
```bash
cd server
run.bat
```

### Manual Method

#### Step 1: Navigate to server directory
```bash
cd server
```

#### Step 2: Create virtual environment (first time only)
```bash
# Linux/macOS
python3 -m venv venv

# Windows
python -m venv venv
```

#### Step 3: Activate virtual environment
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### Step 4: Install dependencies (first time only)
```bash
pip install -r requirements.txt
```

#### Step 5: Run the server
```bash
python mcp_server.py
```

### Success Indicators

When running correctly, you'll see:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Verify It's Working

In another terminal:
```bash
curl http://localhost:8001/health
```

Should return:
```json
{"status":"healthy"}
```

### Important Notes

- The server runs on **port 8001**
- Keep this terminal open while using the app
- The server provides AI tools for the chatbot
- Press `Ctrl+C` to stop the server

### Troubleshooting

**Port already in use:**
```bash
# Linux/macOS
lsof -ti:8001 | xargs kill -9

# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

**Permission denied:**
```bash
chmod +x run.sh
```