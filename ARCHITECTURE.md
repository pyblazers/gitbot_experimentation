# Architecture Overview

## System Components

The AI Agent System is built with a modular architecture that separates concerns and allows for easy extension.

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Interfaces                             │
├─────────────────────────────────────────────────────────────────┤
│  CLI (cli.py)         │  REST API          │  Examples           │
│  - Commands           │  - HTTP endpoints  │  - Code samples     │
│  - Local execution    │  - JSON responses  │  - Tutorials        │
└──────────┬────────────┴────────┬───────────┴─────────────────────┘
           │                     │
           └─────────┬───────────┘
                     │
         ┌───────────▼────────────┐
         │   Agent Manager        │
         │   (AgentManager)       │
         │   - Create agents      │
         │   - Execute agents     │
         │   - Manage lifecycle   │
         └───────────┬────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼───┐  ┌────▼────┐  ┌────▼─────┐
   │ Code   │  │ Issue   │  │   Doc    │
   │Review  │  │ Triage  │  │ Generator│
   │ Agent  │  │ Agent   │  │  Agent   │
   └────┬───┘  └────┬────┘  └────┬─────┘
        │           │            │
        └───────────┼────────────┘
                    │
       ┌────────────┼────────────┐
       │            │            │
  ┌────▼────┐  ┌───▼────┐  ┌────▼────┐
  │AI Models│  │ GitHub │  │  Config │
  │ Claude  │  │  API   │  │  (.env) │
  │ OpenAI  │  │  PyGit │  │         │
  └─────────┘  └────────┘  └─────────┘
```

## Layer Architecture

### 1. Interface Layer
**Purpose**: User interaction and API exposure

**Components**:
- `cli.py` - Command-line interface
- `src/server/api.py` - REST API server
- `examples/` - Usage examples

**Responsibilities**:
- Parse user input
- Route requests to appropriate handlers
- Format and return responses
- Handle authentication/authorization

### 2. Agent Management Layer
**Purpose**: Orchestrate agent creation and execution

**Components**:
- `src/agents/agent_manager.py` - Agent lifecycle management
- `src/agents/base_agent.py` - Base agent class and built-in agents

**Responsibilities**:
- Create and register agent instances
- Route execution requests to specific agents
- Manage agent state and conversation history
- Provide agent discovery and listing

### 3. Agent Implementation Layer
**Purpose**: Specific agent logic and behaviors

**Components**:
- `CodeReviewAgent` - Code review functionality
- `IssueTriageAgent` - Issue categorization
- `DocumentationAgent` - Documentation generation

**Responsibilities**:
- Define agent-specific system prompts
- Process context and user input
- Generate appropriate responses
- Interact with external services

### 4. Integration Layer
**Purpose**: External service integration

**Components**:
- `src/models/ai_models.py` - AI model abstractions
- `src/github_integration/github_client.py` - GitHub API wrapper

**Responsibilities**:
- Abstract external API differences
- Handle authentication and rate limiting
- Provide unified interfaces for agents
- Manage connection lifecycle

### 5. Configuration Layer
**Purpose**: System configuration and settings

**Components**:
- `src/config.py` - Configuration management
- `.env` - Environment variables

**Responsibilities**:
- Load and validate configuration
- Provide configuration to components
- Manage API keys and secrets
- Set default values

## Data Flow

### Agent Execution Flow

```
1. User Request
   ├─→ CLI command: python cli.py agent execute
   └─→ API call: POST /agents/{id}/execute

2. Request Processing
   ├─→ Parse input and context
   └─→ Validate agent exists

3. Agent Execution
   ├─→ Get agent by ID
   ├─→ Build execution context
   └─→ Call agent.execute()

4. Agent Processing
   ├─→ Apply system prompt
   ├─→ Format user input
   ├─→ Call AI model
   └─→ Process response

5. Response Handling
   ├─→ Format response
   ├─→ Update conversation history
   └─→ Return to user
```

### Configuration Loading Flow

```
1. Application Start
   └─→ Load .env file

2. Config Initialization
   ├─→ Read environment variables
   ├─→ Set defaults
   └─→ Validate required values

3. Component Initialization
   ├─→ Create AI model clients
   ├─→ Initialize GitHub client
   └─→ Setup Flask server

4. Ready for Requests
   └─→ Start accepting commands/requests
```

## Key Design Patterns

### 1. Factory Pattern
**Used in**: `ModelFactory`
```python
model = ModelFactory.create_model('anthropic', api_key)
```
**Benefits**: Easy to add new AI providers without changing agent code

### 2. Strategy Pattern
**Used in**: Agent types (CodeReviewAgent, IssueTriageAgent, etc.)
```python
agent = manager.create_agent('code_review')
response = agent.execute(context, input)
```
**Benefits**: Each agent can implement different strategies while sharing the same interface

### 3. Template Method Pattern
**Used in**: Base `Agent` class
```python
class Agent(ABC):
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, context, input) -> str:
        pass
```
**Benefits**: Common functionality in base class, specific behavior in subclasses

### 4. Dependency Injection
**Used in**: Agent initialization
```python
agent = Agent(
    ai_model=custom_model,
    github_client=custom_client
)
```
**Benefits**: Easy testing and flexibility in component composition

## Extension Points

### Adding a New Agent

1. Create agent class extending `Agent`
2. Implement `get_system_prompt()` and `execute()`
3. Register with `AgentManager`

```python
class CustomAgent(Agent):
    def get_system_prompt(self) -> str:
        return "Your custom prompt..."
    
    def execute(self, context, input) -> str:
        return self.generate_response(input)

manager.register_agent_type('custom', CustomAgent)
```

### Adding a New AI Provider

1. Create class extending `AIModel`
2. Implement `generate()` and `chat()` methods
3. Add to `ModelFactory`

```python
class NewAIModel(AIModel):
    def generate(self, prompt, system_prompt=None) -> str:
        # Implementation
        pass
    
    def chat(self, messages) -> str:
        # Implementation
        pass
```

### Adding New API Endpoints

1. Add route to `src/server/api.py`
2. Implement handler function
3. Document in API reference

```python
@app.route('/custom/endpoint', methods=['POST'])
def custom_endpoint():
    # Implementation
    return jsonify({"result": "data"})
```

## Security Considerations

### API Key Management
- Never commit `.env` file
- Use environment variables
- Rotate keys regularly
- Minimal scope for GitHub tokens

### Server Security
- Use HTTPS in production
- Implement authentication
- Rate limiting on endpoints
- Input validation

### Code Execution
- No arbitrary code execution
- Sanitize user inputs
- Validate context parameters
- Limit resource usage

## Performance Considerations

### Caching
- Consider caching AI responses for similar inputs
- Cache GitHub API responses where appropriate
- Store conversation history efficiently

### Rate Limiting
- Respect API rate limits (GitHub, AI providers)
- Implement exponential backoff
- Queue requests if needed

### Scalability
- Stateless agents allow horizontal scaling
- Consider Redis for shared state
- Use message queues for async processing

## Deployment Architectures

### Single Machine (Mac mini)
```
┌─────────────────────┐
│     Mac mini        │
│  ┌───────────────┐  │
│  │  AI Agent     │  │
│  │  System       │  │
│  │  (Python)     │  │
│  │  Port: 5000   │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │  launchd      │  │
│  │  (auto-start) │  │
│  └───────────────┘  │
└─────────────────────┘
```

### Docker Deployment
```
┌─────────────────────┐
│   Docker Host       │
│  ┌───────────────┐  │
│  │  Container    │  │
│  │  ai-agent     │  │
│  │  Port: 5000   │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │  Volume       │  │
│  │  /app/logs    │  │
│  └───────────────┘  │
└─────────────────────┘
```

### Distributed Setup (Future)
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Web UI  │───▶│   API    │───▶│  Agent   │
│          │    │  Gateway │    │  Workers │
└──────────┘    └──────────┘    └──────────┘
                      │              │
                      ▼              ▼
                ┌──────────┐    ┌──────────┐
                │  Redis   │    │  Queue   │
                │  Cache   │    │  System  │
                └──────────┘    └──────────┘
```

## Technology Stack

### Core
- **Python 3.9+** - Primary language
- **Flask** - Web server framework
- **Anthropic SDK** - Claude AI integration
- **OpenAI SDK** - GPT integration
- **PyGithub** - GitHub API wrapper
- **GitPython** - Git operations

### Development
- **python-dotenv** - Environment management
- **pyyaml** - Configuration files
- **pydantic** - Data validation

### Deployment
- **Docker** - Containerization
- **Gunicorn** - Production WSGI server
- **launchd** - Mac service management

## File Structure Reference

```
.
├── README.md              # Project overview
├── QUICKSTART.md          # Fast setup guide
├── SETUP.md               # Detailed documentation
├── DOCKER.md              # Docker deployment
├── ARCHITECTURE.md        # This file
├── requirements.txt       # Python dependencies
├── .env.example           # Configuration template
├── .gitignore            # Git ignore rules
├── cli.py                # Command-line interface
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker orchestration
│
├── src/                  # Source code
│   ├── config.py         # Configuration management
│   ├── agents/           # Agent implementations
│   │   ├── base_agent.py      # Base classes
│   │   └── agent_manager.py   # Agent orchestration
│   ├── models/           # AI model integrations
│   │   └── ai_models.py       # Model abstractions
│   ├── github_integration/    # GitHub API
│   │   └── github_client.py   # GitHub operations
│   └── server/           # REST API
│       └── api.py             # Flask application
│
├── examples/             # Usage examples
│   ├── code_review_example.py
│   ├── issue_triage_example.py
│   └── multiple_agents_example.py
│
├── scripts/              # Deployment scripts
│   ├── setup.sh          # Initial setup
│   ├── setup_launchd.sh  # Mac service setup
│   └── test_setup.sh     # Validation tests
│
└── tests/                # Test suite
    └── test_basic.py     # Basic functionality tests
```

## Future Enhancements

### Short Term
- [ ] Add more agent types (debugging, testing, refactoring)
- [ ] Implement conversation persistence
- [ ] Add webhook handlers for GitHub events
- [ ] Create web UI dashboard

### Medium Term
- [ ] Agent collaboration and workflows
- [ ] Advanced context management
- [ ] Multi-repository support
- [ ] Analytics and reporting

### Long Term
- [ ] Custom agent DSL
- [ ] Agent marketplace
- [ ] Fine-tuned models
- [ ] Distributed agent execution
