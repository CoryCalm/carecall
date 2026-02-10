#!/bin/bash

# CareCall Setup Script
# Run this to get everything installed and ready!

echo "🩺 CareCall - Setup Script"
echo "=========================="
echo ""

# Check Python version
echo "📍 Checking Python version..."
python3 --version
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip
echo ""

# Install requirements
echo "📥 Installing Python packages..."
pip install -r requirements.txt
echo "✅ All packages installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo ""
else
    echo "ℹ️  .env file already exists"
    echo ""
fi

echo "=========================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get Deepgram API key: https://console.deepgram.com/signup"
echo "2. Add API key to .env file"
echo "3. Run: source venv/bin/activate"
echo "4. Run: python test_deepgram.py"
echo "5. Run: uvicorn src.main:app --reload"
echo ""
echo "Let's build CareCall! 🚀"
