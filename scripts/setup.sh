#!/bin/bash
# Setup script for Mac mini deployment

set -e

echo "🚀 AI Agent System Setup"
echo "========================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || {
    echo "❌ Python 3 is required but not installed."
    exit 1
}
echo "✓ Python 3 found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Setup configuration
echo "Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your API keys"
    echo "   Required:"
    echo "   - GITHUB_TOKEN"
    echo "   - ANTHROPIC_API_KEY or OPENAI_API_KEY"
else
    echo "✓ .env file already exists"
fi
echo ""

# Validate configuration
echo "Validating configuration..."
python cli.py config validate || {
    echo ""
    echo "⚠️  Configuration validation failed"
    echo "   Please update your .env file with required values"
}
echo ""

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python cli.py config validate"
echo "3. Start server: python cli.py server"
echo ""
echo "For Mac mini service setup, run: ./scripts/setup_launchd.sh"
