#!/bin/bash
set -e

echo "=== AI Knowledge Inbox - Setup ==="
echo ""

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "Error: Python 3 is required. Install it from https://python.org"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Error: Node.js is required. Install it from https://nodejs.org"; exit 1; }

PYTHON_CMD="python3"
if command -v python3.10 >/dev/null 2>&1; then
    PYTHON_CMD="python3.10"
fi

# Setup .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[1/4] Created .env from .env.example"
    echo "      -> Add your Groq API key: https://console.groq.com"
    echo "      -> Then re-run this script"
    exit 0
else
    echo "[1/4] .env found"
fi

# Check Groq key
if grep -q "your_groq_api_key_here" .env; then
    echo "Error: Update GROQ_API_KEY in .env with your actual key"
    echo "       Get one free at https://console.groq.com"
    exit 1
fi

# Backend setup
echo "[2/4] Setting up backend..."
cd backend
$PYTHON_CMD -m venv venv
source venv/bin/activate
pip install -r requirements.txt --quiet
deactivate
cd ..
echo "      Backend ready"

# Frontend setup
echo "[3/4] Setting up frontend..."
cd frontend
npm install --silent
cd ..
echo "      Frontend ready"

echo "[4/4] Setup complete!"
echo ""
echo "To run the app:"
echo ""
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    uvicorn main:app --reload"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  API Docs: http://localhost:8000/docs"
