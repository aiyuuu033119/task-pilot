# 🔧 FINAL Claude Desktop Setup - Fixed for v0.11.6

## Problem Identified
Your Claude Desktop v0.11.6 is treating MCP servers as "extensions" which causes the "Extension not found" warnings. This is fixed with the correct configuration format and server setup.

## ✅ Working Configuration

### Option 1: Direct WSL Command (Recommended)
Save this to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "task-pilot-tools": {
      "command": "wsl",
      "args": [
        "-e",
        "bash",
        "-c",
        "cd /mnt/d/CLAUDE/task-pilot-v2/server && source venv/bin/activate && python3 mcp_server_stdio.py"
      ]
    }
  }
}
```

### Option 2: Using Batch File (Alternative)
Save this to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "task-pilot-tools": {
      "command": "D:\\CLAUDE\\task-pilot-v2\\server\\run_claude.bat"
    }
  }
}
```

## 🚀 Setup Steps

### Step 1: Ensure Dependencies
```bash
# In WSL
cd /mnt/d/CLAUDE/task-pilot-v2/server
source venv/bin/activate
pip install mcp httpx
```

### Step 2: Test the Server
```bash
# Test the server can start (should not show errors)
python3 -c "from mcp.types import Tool, TextContent; from mcp.server import Server; from mcp import stdio_server; print('MCP ready!')"
```

### Step 3: Apply Configuration
1. **Open File Explorer** and type `%APPDATA%\Claude` in the address bar
2. **Edit** `claude_desktop_config.json` (create if it doesn't exist)
3. **Copy** Option 1 configuration above
4. **Save** the file

### Step 4: Restart Claude Desktop
1. **Completely close** Claude Desktop
2. **Restart** Claude Desktop
3. **Check logs** - should no longer see "Extension not found" warnings

## 🎯 Expected Results

### Success Indicators:
- No more "Extension task-pilot-tools not found" warnings
- MCP server starts without errors
- Tools become available in Claude conversations

### Available Tools:
1. **Calculator**: `"What's sqrt(144) + 5^2?"`
2. **DateTime**: `"What time is it?"`
3. **UUID Generator**: `"Generate a UUID"`
4. **Text Analysis**: `"Analyze this text: 'Hello world'"`
5. **Hash Generator**: `"Hash this text with SHA256"`
6. **Random Numbers**: `"Give me 3 random numbers"`

## 🛠️ Troubleshooting

### If still getting "Extension not found":
1. **Check file path**: Ensure `/mnt/d/CLAUDE/task-pilot-v2/server/mcp_server_stdio.py` exists
2. **Check WSL**: Run `wsl --version` to ensure WSL is working
3. **Check Python**: Run `wsl python3 --version` to verify Python in WSL

### Test WSL Command:
```cmd
wsl -e bash -c "cd /mnt/d/CLAUDE/task-pilot-v2/server && source venv/bin/activate && python3 -c 'print(\"Test successful\")'"
```

### Alternative Paths:
If your project is in a different location, update the path in the configuration:
- WSL path: `/mnt/d/CLAUDE/task-pilot-v2/server`
- Windows path: `D:\CLAUDE\task-pilot-v2\server`

## 📝 What Was Fixed

1. **Correct MCP Imports**: Updated server to use proper `mcp.types` imports
2. **Right Configuration Format**: Using exact format Claude Desktop v0.11.6 expects
3. **Proper WSL Integration**: Direct command execution in WSL environment
4. **Simplified Dependencies**: Only `mcp` and `httpx` packages needed

## 🎉 Final Test

After setup, try asking Claude:
- "What's 2 + 2?" (should use calculator tool)
- "What time is it?" (should use datetime tool)

You should see the tools working without any "extension not found" warnings!