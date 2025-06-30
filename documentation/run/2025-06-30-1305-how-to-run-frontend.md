# How to Run Frontend
**Date: June 30, 2025**
**Type: Running Instructions**

## Quick Start

### Terminal 3 (Frontend):
```bash
cd frontend
./run.sh   # Linux/macOS
# or
run.bat    # Windows
```

This will:
1. Install dependencies (first time only)
2. Start the Next.js development server
3. Open at http://localhost:3000

## Manual Steps

### 1. Navigate to frontend directory:
```bash
cd frontend
```

### 2. Install dependencies (first time only):
```bash
npm install
```

### 3. Run development server:
```bash
npm run dev
```

### 4. Open browser:
Navigate to **http://localhost:3000**

## Prerequisites

Before running the frontend, make sure:

1. **Node.js 18+** is installed
2. **Backend is running** on port 8000 (Terminal 2)
3. **MCP Server is running** on port 8001 (Terminal 1)

## Full Stack Setup

You need all 3 services running:

```bash
# Terminal 1: MCP Server
cd server && ./run.sh

# Terminal 2: Backend API
cd client && ./run.sh  

# Terminal 3: Frontend
cd frontend && ./run.sh
```

## Environment Variables

Create `.env.local` in frontend folder (optional):
```env
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_API_URL=http://localhost:8000
PORT=3000
```

## Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## Common Issues

### "npm: command not found"
Install Node.js from https://nodejs.org

### "Cannot connect to backend"
Make sure the backend is running on port 8000:
```bash
curl http://localhost:8000/health
```

### Port 3000 already in use
```bash
# Find process using port
lsof -i :3000  # Linux/macOS
netstat -ano | findstr :3000  # Windows

# Or change port
PORT=3001 npm run dev
```

### Connection issues
- Ensure all three services are running
- Check browser console for WebSocket errors
- Verify CORS settings on backend

### Module not found errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Production Build

```bash
cd frontend
npm run build
npm start
```

## Docker (Alternative)

```bash
cd frontend
docker build -t frontend .
docker run -p 3000:3000 frontend
```

## Success Indicators

When running correctly, you'll see:
```
▲ Next.js 14.1.0
- Local:        http://localhost:3000
- Environments: .env.local

✓ Ready in 2.3s
```

## What the Frontend Does

- **Serves the chat UI** at http://localhost:3000
- **Connects to backend** WebSocket at ws://localhost:8000/ws
- **Provides real-time chat** with AI assistant
- **Manages conversations** with Zustand state
- **Renders markdown** in AI responses
- **Shows connection status** and loading states

## Tech Stack

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Zustand** - State management
- **React Markdown** - Message rendering