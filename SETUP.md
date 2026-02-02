# AI Agent System - Personal GitHub Copilot

A comprehensive AI agent system similar to GitHub Copilot, designed for personal use on your GitHub account. This system allows you to create, manage, and deploy AI-powered agents that can assist with code reviews, issue triaging, documentation, and more.

## Features

- 🤖 **Multiple AI Agents**: Code review, issue triage, documentation generation
- 🧠 **AI Model Support**: Claude (Anthropic), GPT-4 (OpenAI)
- 🐙 **GitHub Integration**: Full GitHub API integration for repositories, issues, PRs
- 🌐 **REST API Server**: Flask-based API for remote agent execution
- 💻 **CLI Tools**: Command-line interface for local agent management
- 🔧 **Extensible**: Easy to create custom agents
- 🍎 **Mac mini Ready**: Optimized for running on Mac mini

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent System                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Code Review  │    │ Issue Triage │    │Documentation │  │
│  │    Agent     │    │    Agent     │    │    Agent     │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                    │                    │          │
│         └────────────────────┼────────────────────┘          │
│                              │                               │
│                    ┌─────────▼─────────┐                     │
│                    │  Agent Manager    │                     │
│                    └─────────┬─────────┘                     │
│                              │                               │
│         ┌────────────────────┼────────────────────┐          │
│         │                    │                    │          │
│    ┌────▼────┐        ┌──────▼──────┐      ┌────▼────┐     │
│    │ Claude  │        │   GitHub    │      │  Flask  │     │
│    │   API   │        │     API     │      │  Server │     │
│    └─────────┘        └─────────────┘      └─────────┘     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- GitHub account with Personal Access Token
- API key for Claude or OpenAI (or both)

### Setup on Mac mini

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/gitbot_experimentation.git
   cd gitbot_experimentation
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

5. **Set up your `.env` file:**
   ```env
   # Required
   GITHUB_TOKEN=ghp_your_github_token_here
   ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here
   
   # Optional
   OPENAI_API_KEY=sk-your_openai_key_here
   GITHUB_USERNAME=your_github_username
   ```

### Getting API Keys

1. **GitHub Personal Access Token:**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Create a token with `repo`, `issues`, `pull_requests` scopes
   - Copy the token to your `.env` file

2. **Anthropic API Key:**
   - Visit [Anthropic Console](https://console.anthropic.com/)
   - Create an API key
   - Copy to your `.env` file

3. **OpenAI API Key (Optional):**
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Create an API key
   - Copy to your `.env` file

## Usage

### Command-Line Interface

The system includes a CLI for local agent management:

```bash
# Validate configuration
python cli.py config validate

# Show current configuration
python cli.py config show

# List available agent types
python cli.py agent list

# Create an agent
python cli.py agent create --type code_review --id my_reviewer

# Execute an agent
python cli.py agent execute --id code_review --input "Review this function: def foo(): pass"

# Execute with GitHub context
python cli.py agent execute \
  --id code_review \
  --repo owner/repository \
  --pr 123 \
  --input "Please review this PR"
```

### REST API Server

Start the server to enable remote agent access:

```bash
# Start the server
python cli.py server

# Or with custom host/port
python cli.py server --host 0.0.0.0 --port 8000
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:5000/health
```

#### List Agents
```bash
curl http://localhost:5000/agents
```

#### Create Agent
```bash
curl -X POST http://localhost:5000/agents \
  -H "Content-Type: application/json" \
  -d '{"type": "code_review", "id": "my_reviewer"}'
```

#### Execute Agent
```bash
curl -X POST http://localhost:5000/agents/my_reviewer/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Review this code",
    "repository": "owner/repo",
    "pr_number": 123
  }'
```

## Available Agents

### Code Review Agent
Analyzes code changes and provides detailed reviews.

**Usage:**
```python
from src.agents import AgentManager, AgentContext

manager = AgentManager()
agent = manager.create_agent('code_review')
context = AgentContext(repository='owner/repo', pr_number=123)
response = agent.execute(context, "Review this PR")
```

### Issue Triage Agent
Triages and categorizes GitHub issues.

**Usage:**
```python
context = AgentContext(repository='owner/repo', issue_number=456)
agent = manager.create_agent('issue_triage')
response = agent.execute(context, "Triage this issue")
```

### Documentation Agent
Generates and improves documentation.

**Usage:**
```python
agent = manager.create_agent('documentation')
response = agent.execute(AgentContext(), "Document the API endpoints")
```

## Creating Custom Agents

You can create custom agents by extending the base `Agent` class:

```python
from src.agents.base_agent import Agent, AgentContext

class CustomAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            name="Custom Agent",
            description="My custom agent",
            **kwargs
        )
    
    def get_system_prompt(self) -> str:
        return "You are a custom AI agent that..."
    
    def execute(self, context: AgentContext, user_input: str) -> str:
        # Your custom logic here
        return self.generate_response(user_input)

# Register the custom agent
from src.agents import AgentManager
manager = AgentManager()
manager.register_agent_type('custom', CustomAgent)

# Use the custom agent
agent = manager.create_agent('custom')
```

## Running on Mac mini

### As a Background Service

Create a launch agent to run the server automatically:

1. **Create launch agent plist:**
   ```bash
   mkdir -p ~/Library/LaunchAgents
   ```

2. **Create file `~/Library/LaunchAgents/com.user.aiagent.plist`:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.user.aiagent</string>
       <key>ProgramArguments</key>
       <array>
           <string>/path/to/venv/bin/python</string>
           <string>/path/to/cli.py</string>
           <string>server</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
       <key>WorkingDirectory</key>
       <string>/path/to/gitbot_experimentation</string>
   </dict>
   </plist>
   ```

3. **Load the service:**
   ```bash
   launchctl load ~/Library/LaunchAgents/com.user.aiagent.plist
   ```

### Using with GitHub Actions

You can integrate this with GitHub Actions to automatically trigger agents:

```yaml
name: AI Agent Workflow
on: [pull_request, issues]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger AI Agent
        run: |
          curl -X POST http://your-macmini-ip:5000/agents/code_review/execute \
            -H "Content-Type: application/json" \
            -d '{"repository": "${{ github.repository }}", "pr_number": ${{ github.event.pull_request.number }}}'
```

## Configuration

All configuration is managed through environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Anthropic/Claude API key | Yes (if using Claude) |
| `OPENAI_API_KEY` | OpenAI API key | Yes (if using OpenAI) |
| `GITHUB_TOKEN` | GitHub Personal Access Token | Yes |
| `GITHUB_USERNAME` | Your GitHub username | No |
| `SERVER_HOST` | Server host address | No (default: 0.0.0.0) |
| `SERVER_PORT` | Server port | No (default: 5000) |
| `DEFAULT_MODEL` | Default AI model | No (default: claude-3-sonnet-20240229) |
| `MAX_TOKENS` | Max tokens for responses | No (default: 4096) |
| `TEMPERATURE` | AI temperature setting | No (default: 0.7) |

## Troubleshooting

### Common Issues

1. **"No API key configured"**
   - Make sure your `.env` file is in the project root
   - Verify API keys are set correctly
   - Run `python cli.py config validate`

2. **"GitHub token not configured"**
   - Create a GitHub Personal Access Token
   - Add it to your `.env` file

3. **Port already in use**
   - Change the port in `.env` or use `--port` flag
   - Check for other services using the port

4. **Module import errors**
   - Activate your virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

## Security Considerations

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Use environment-specific tokens (development vs production)
- Consider using a secrets manager for production deployments
- Limit GitHub token scopes to minimum required permissions

## Contributing

To add new features or agents:

1. Create a new branch
2. Implement your changes
3. Add tests if applicable
4. Submit a pull request

## License

This project is for personal use. Modify as needed for your requirements.

## Support

For issues or questions:
- Check the troubleshooting section
- Review the code in the `src/` directory
- Open an issue on GitHub

## Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Agent scheduling and automation
- [ ] Multi-repository management
- [ ] Advanced analytics and reporting
- [ ] Web UI dashboard
- [ ] Integration with more AI models
- [ ] Custom webhook handlers
- [ ] Agent collaboration features
