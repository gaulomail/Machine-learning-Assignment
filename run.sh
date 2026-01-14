#!/bin/bash

# GuardAI Run Script
# This script runs the GuardAI application

set -e  # Exit on error

echo "🛡️  GuardAI - Advanced Threat Intelligence"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Check if model exists
if [ ! -f "model.pkl" ] || [ ! -f "model_metadata.pkl" ]; then
    echo "⚠️  Model not found. Training model..."
    source .venv/bin/activate
    PYTHONPATH=. python src/train_quick.py
    echo "✅ Model trained"
    echo ""
fi

# Activate virtual environment
source .venv/bin/activate

# Kill any existing process on port 5000
echo "🔍 Checking for existing processes on port 5000..."
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true
echo ""

# Start the application
echo "🚀 Starting GuardAI Dashboard..."
echo "📍 Access the dashboard at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

PYTHONPATH=. python -m src.app
