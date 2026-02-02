# AI Agent System - Personal GitHub Copilot

An AI-powered agent system similar to GitHub Copilot, designed for personal use on your own GitHub account. Built to run on Mac mini and utilize Claude 4 or other AI models.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your API keys
cp .env.example .env
# Edit .env with your GitHub token and AI API keys

# 3. Validate configuration
python cli.py config validate

# 4. Start the server
python cli.py server
```

## ✨ Features

- 🤖 Multiple AI agents (code review, issue triage, documentation)
- 🧠 Support for Claude and GPT-4
- 🐙 Full GitHub integration
- 🌐 REST API server
- 💻 Command-line interface
- 🔧 Extensible agent framework

## 📖 Documentation

For detailed setup instructions, see [SETUP.md](SETUP.md)

## 🎯 Use Cases

- Automated code reviews on pull requests
- Issue triaging and categorization
- Documentation generation
- Custom agent workflows

## 🛠️ Available Agents

1. **Code Review Agent** - Analyzes code changes
2. **Issue Triage Agent** - Categorizes and prioritizes issues
3. **Documentation Agent** - Generates documentation

## 📚 Learn More

- [Complete Setup Guide](SETUP.md) - Installation and configuration
- [API Documentation](SETUP.md#api-endpoints) - REST API reference
- [Creating Custom Agents](SETUP.md#creating-custom-agents) - Extend the system 
