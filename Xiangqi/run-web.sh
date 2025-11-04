#!/bin/bash
# Launch script for Xiangqi web server

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "Installing dependencies..."
    "$SCRIPT_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
fi

echo "Starting Xiangqi web server..."
echo "Open your browser to: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

"$SCRIPT_DIR/venv/bin/python3" -m uvicorn server.api:app --host 127.0.0.1 --port 8000
