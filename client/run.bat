@echo off
REM Client/Backend Run Script for Windows

echo Starting Client/Backend...

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found!
    echo Copy .env.example to .env and add your API keys
    
    REM Create basic .env if it doesn't exist
    (
        echo # API Keys ^(set at least one^)
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo ANTHROPIC_API_KEY=your_anthropic_api_key_here
        echo.
        echo # MCP Server URL
        echo MCP_SERVER_HOST=localhost
        echo MCP_SERVER_PORT=8001
        echo.
        echo # App Configuration
        echo APP_HOST=0.0.0.0
        echo APP_PORT=8000
    ) > .env
    echo Created .env file. Please edit it with your API keys.
    pause
    exit /b 1
)

REM Load environment variables from .env
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%b"=="" set "%%a=%%b"
)

REM Check for API keys
if "%OPENAI_API_KEY%"=="" if "%ANTHROPIC_API_KEY%"=="" (
    echo Error: No API keys found in .env file!
    echo Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install/upgrade dependencies
pip install -r requirements.txt

REM Set default values
if "%APP_HOST%"=="" set APP_HOST=0.0.0.0
if "%APP_PORT%"=="" set APP_PORT=8000

REM Set PYTHONPATH to current directory
set PYTHONPATH=%CD%;%PYTHONPATH%

REM Start the client/backend
echo Client/Backend running on http://%APP_HOST%:%APP_PORT%
echo Frontend available at http://localhost:%APP_PORT%
python -m uvicorn app:app --host %APP_HOST% --port %APP_PORT% --reload