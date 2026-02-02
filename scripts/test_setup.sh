#!/bin/bash
# Quick test script to verify setup

set -e

echo "🧪 Testing AI Agent System"
echo "========================="
echo ""

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Test 1: Configuration validation
echo "Test 1: Configuration validation"
echo "---------------------------------"
python cli.py config validate
echo ""

# Test 2: List available agents
echo "Test 2: List available agent types"
echo "-----------------------------------"
python cli.py agent list
echo ""

# Test 3: Health check (if server is running)
echo "Test 3: API health check"
echo "------------------------"
curl -s http://localhost:5000/health 2>/dev/null && echo "" || echo "Server not running (expected if not started)"
echo ""

echo "✅ Basic tests complete!"
echo ""
echo "To start the server: python cli.py server"
echo "To run examples: python examples/code_review_example.py"
