# Fix Dependency Conflicts
**Date: June 30, 2025**
**Type: Bugfix**

## Overview
Fixed dependency version conflicts in server and client requirements.txt files to be compatible with fastmcp requirements.

## Problem
The server installation was failing with dependency conflicts:
- `fastmcp` requires `httpx>=0.28.1` but we specified `httpx==0.26.0`
- `fastmcp` requires `fastapi>=0.115.12` but we specified `fastapi==0.110.0`

## Solution
Updated both server and client requirements to use minimum version specifiers (>=) instead of exact versions (==) for better compatibility.

## Changes Made

### 1. Updated server/requirements.txt
Changed from:
```txt
fastapi==0.110.0
uvicorn[standard]==0.27.1
httpx==0.26.0
```

To:
```txt
fastapi>=0.115.12
uvicorn[standard]>=0.27.1
httpx>=0.28.1
```

### 2. Updated client/requirements.txt
Changed from:
```txt
fastapi==0.110.0
uvicorn[standard]==0.27.1
websockets==12.0
python-dotenv==1.0.1
httpx==0.26.0
```

To:
```txt
fastapi>=0.115.12
uvicorn[standard]>=0.27.1
websockets>=12.0
python-dotenv>=1.0.1
httpx>=0.28.1
```

## Benefits
1. **Compatibility** - Dependencies now work with fastmcp requirements
2. **Flexibility** - Using >= allows pip to resolve the best compatible versions
3. **Future-proof** - Can use newer versions without manual updates
4. **Consistency** - Both server and client use the same core versions

## Testing
After this change, run:
```bash
cd server
pip install -r requirements.txt  # Should install without conflicts
```

## Notes
- We kept exact versions for AI-specific packages (pydantic-ai, openai, anthropic) to ensure stability
- The >= operator means "this version or newer"
- This resolves the installation issues while maintaining compatibility