@echo off
REM Frontend Run Script for Windows

echo Starting Next.js Frontend...

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    npm install
)

REM Set default values
if "%PORT%"=="" set PORT=3000

REM Start the development server
echo Frontend running on http://localhost:%PORT%
npm run dev