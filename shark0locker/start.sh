#!/bin/bash

# shark0locker startup script

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║    🦈  SHARK0LOCKER - HIGH FREQUENCY TRADING BOT  🦈         ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "❌ Virtual environment not found at ../venv"
    echo "Please create a virtual environment first:"
    echo "  python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../venv/bin/activate

# Check if dependencies are installed
if ! python3 -c "import aiohttp" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs data

# Start the bot
echo ""
echo "🦈 Starting shark0locker..."
echo ""
python3 main.py

# Deactivate virtual environment on exit
deactivate
