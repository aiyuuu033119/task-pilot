#!/bin/bash

# Frontend Run Script

echo "Starting Next.js Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Set default values
export PORT=${PORT:-3000}

# Start the development server
echo "Frontend running on http://localhost:$PORT"
npm run dev