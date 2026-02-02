# Quick Start Guide

Get your AI Agent system running in 5 minutes!

## Prerequisites
- Python 3.9+
- GitHub account
- At least one AI API key (Anthropic or OpenAI)

## Installation Steps

### 1. Setup Dependencies
```bash
# Install Python packages
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Copy the example configuration
cp .env.example .env

# Edit .env and add your keys:
# - GITHUB_TOKEN (from GitHub Settings > Developer settings > Personal access tokens)
# - ANTHROPIC_API_KEY (from console.anthropic.com)
```

Minimum required `.env` content:
```env
GITHUB_TOKEN=ghp_your_token_here
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

### 3. Verify Setup
```bash
# Run basic tests
python tests/test_basic.py

# Validate configuration
python cli.py config validate
```

### 4. Start Using

#### Option A: Command Line
```bash
# List available agent types
python cli.py agent list

# Create and use an agent
python cli.py agent create --type code_review --id reviewer
python cli.py agent execute --id reviewer --input "Review this code: def hello(): pass"
```

#### Option B: Run as Server
```bash
# Start the API server
python cli.py server

# In another terminal, test it
curl http://localhost:5000/health
curl http://localhost:5000/agents
```

#### Option C: Use Examples
```bash
# Run example scripts
python examples/code_review_example.py
python examples/issue_triage_example.py
python examples/multiple_agents_example.py
```

## Mac mini Specific Setup

### Run as Background Service
```bash
# Setup launchd service (auto-start on boot)
./scripts/setup_launchd.sh

# Service commands
launchctl start com.user.aiagent
launchctl stop com.user.aiagent
```

### View Logs
```bash
tail -f logs/stdout.log
tail -f logs/stderr.log
```

## Docker Deployment

```bash
# Quick start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Common Commands Reference

```bash
# Configuration
python cli.py config validate
python cli.py config show

# Agents
python cli.py agent list
python cli.py agent create --type <type> --id <id>
python cli.py agent execute --id <id> --input "<text>"

# Server
python cli.py server
python cli.py server --host 0.0.0.0 --port 8000

# Testing
python tests/test_basic.py
./scripts/test_setup.sh
```

## API Usage Examples

### Create an Agent
```bash
curl -X POST http://localhost:5000/agents \
  -H "Content-Type: application/json" \
  -d '{"type": "code_review", "id": "my_reviewer"}'
```

### Execute Agent
```bash
curl -X POST http://localhost:5000/agents/my_reviewer/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Review this function: def add(a, b): return a + b",
    "repository": "owner/repo"
  }'
```

### List Agents
```bash
curl http://localhost:5000/agents
```

## Troubleshooting

### "No API key configured"
- Check that `.env` file exists in project root
- Verify API keys are set correctly
- Run `python cli.py config validate`

### "Module not found"
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
# Use different port
python cli.py server --port 8000
```

### Tests failing
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Run tests with more info
python tests/test_basic.py
```

## Next Steps

1. **Read full documentation**: See [SETUP.md](SETUP.md) for detailed information
2. **Try examples**: Run scripts in `examples/` directory
3. **Create custom agents**: See "Creating Custom Agents" in SETUP.md
4. **Deploy to production**: Use Docker or launchd service
5. **Integrate with GitHub**: Set up webhooks for automatic triggers

## Need Help?

- Check [SETUP.md](SETUP.md) for detailed documentation
- Review example scripts in `examples/`
- Run diagnostic: `./scripts/test_setup.sh`
- Verify configuration: `python cli.py config show`

## What Can You Do?

- ✅ Automated code reviews
- ✅ Issue triage and categorization
- ✅ Documentation generation
- ✅ Custom AI agent workflows
- ✅ GitHub integration
- ✅ Remote API access
- ✅ Run on Mac mini as service
