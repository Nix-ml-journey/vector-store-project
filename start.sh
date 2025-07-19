#!/bin/bash

# Vector Store Book Search - Startup Script
echo "🚀 Starting Vector Store Book Search..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if embeddings exist
if [ ! -f "src/embeddings.npy" ]; then
    echo "🧠 Generating embeddings (this may take a few minutes)..."
    cd src
    python embedding_generation.py
    cd ..
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 To start the application:"
echo "   Terminal 1: cd src && python app.py"
echo "   Terminal 2: cd src && streamlit run streamlit_frontend.py"
echo ""
echo "🌐 Then open: http://localhost:8501" 