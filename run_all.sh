#!/bin/bash

# Configuration
API_PORT=8000
API_URL="http://127.0.0.1:$API_PORT"
SIMULATOR_SCRIPT="simulator/generate_events.py"

echo "🚀 Starting RFID Simulator Project..."

# 1. Setup Environment
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Using system Python."
fi

# 2. Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 2. Start FastAPI backend in the background
echo "🌐 Starting FastAPI backend on $API_URL..."
uvicorn app.main:app --host 127.0.0.1 --port $API_PORT --reload &
BACKEND_PID=$!

# 3. Wait for the backend to be ready
echo "⏳ Waiting for backend to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0
while ! curl -s $API_URL/docs > /dev/null; do
    sleep 1
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "❌ Error: Backend failed to start after $MAX_RETRIES seconds."
        kill $BACKEND_PID
        exit 1
    fi
done

echo "✅ Backend is up and running!"

# 4. Start the RFID simulator
echo "📡 Starting RFID event simulator ($SIMULATOR_SCRIPT)..."
python3 $SIMULATOR_SCRIPT

# Clean up: Kill backend when simulator exits
echo "🛑 Simulator finished. Stopping backend..."
kill $BACKEND_PID
echo "👋 Done."
