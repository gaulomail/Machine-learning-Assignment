#!/bin/bash

# GuardAI Setup Script
# This script sets up the entire project environment

set -e  # Exit on error

echo "🛡️  GuardAI Setup Script"
echo "======================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check if dataset exists
if [ ! -f "brazilian-malware.csv" ]; then
    if [ -f "brazilian-malware.zip" ]; then
        echo "📂 Extracting dataset..."
        unzip -q brazilian-malware.zip
        echo "✅ Dataset extracted"
    else
        echo "⚠️  Dataset not found. Please download brazilian-malware.csv"
    fi
else
    echo "✅ Dataset found"
fi
echo ""

# Train model
echo "🤖 Training model (this may take 30-60 seconds)..."
PYTHONPATH=. python src/train_quick.py
echo "✅ Model trained and saved"
echo ""

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v
echo "✅ All tests passed"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "🚀 Starting GuardAI Dashboard..."
echo "📍 Access the dashboard at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Kill any existing process on port 5000
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true

# Start the application
PYTHONPATH=. python -m src.app

