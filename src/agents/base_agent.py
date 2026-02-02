"""
Base agent class for AI agents.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

from ..models import AIModel, ModelFactory
from ..github_integration import GitHubClient
from ..config import config


class AgentContext:
    """Context information for agent execution."""
    
    def __init__(self, repository: Optional[str] = None, issue_number: Optional[int] = None,
                 pr_number: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None):
        self.repository = repository
        self.issue_number = issue_number
        self.pr_number = pr_number
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()


class Agent(ABC):
    """Base class for all AI agents."""
    
    def __init__(self, name: str, description: str, 
                 ai_model: Optional[AIModel] = None,
                 github_client: Optional[GitHubClient] = None):
        """
        Initialize an agent.
        
        Args:
            name: Agent name
            description: Agent description
            ai_model: AI model to use (defaults to Claude)
            github_client: GitHub client for repository operations
        """
        self.name = name
        self.description = description
        self.ai_model = ai_model or self._create_default_model()
        self.github_client = github_client or self._create_github_client()
        self.conversation_history: List[Dict[str, str]] = []
    
    def _create_default_model(self) -> AIModel:
        """Create default AI model."""
        api_key = config.get_api_key('anthropic')
        if not api_key:
            raise ValueError("No API key configured for AI model")
        return ModelFactory.create_model(
            'anthropic',
            api_key,
            config.DEFAULT_MODEL,
            config.MAX_TOKENS,
            config.TEMPERATURE
        )
    
    def _create_github_client(self) -> GitHubClient:
        """Create GitHub client."""
        if not config.GITHUB_TOKEN:
            raise ValueError("GitHub token not configured")
        return GitHubClient(config.GITHUB_TOKEN)
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        pass
    
    @abstractmethod
    def execute(self, context: AgentContext, user_input: str) -> str:
        """
        Execute the agent with given context and input.
        
        Args:
            context: Agent execution context
            user_input: User input or command
            
        Returns:
            Agent response
        """
        pass
    
    def add_to_conversation(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def generate_response(self, prompt: str, use_history: bool = True) -> str:
        """
        Generate a response using the AI model.
        
        Args:
            prompt: The prompt to send to the model
            use_history: Whether to include conversation history
            
        Returns:
            Generated response
        """
        if use_history and self.conversation_history:
            messages = self.conversation_history + [{"role": "user", "content": prompt}]
            response = self.ai_model.chat(messages)
        else:
            system_prompt = self.get_system_prompt()
            response = self.ai_model.generate(prompt, system_prompt)
        
        self.add_to_conversation("user", prompt)
        self.add_to_conversation("assistant", response)
        
        return response
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "conversation_length": len(self.conversation_history)
        }


class CodeReviewAgent(Agent):
    """Agent specialized in code review."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Code Review Agent",
            description="Analyzes code changes and provides detailed reviews",
            **kwargs
        )
    
    def get_system_prompt(self) -> str:
        return """You are an expert code reviewer. Your role is to:
1. Analyze code changes for bugs, security issues, and best practices
2. Provide constructive feedback with specific suggestions
3. Consider performance, maintainability, and readability
4. Be thorough but concise in your reviews
5. Highlight both positive aspects and areas for improvement"""
    
    def execute(self, context: AgentContext, user_input: str) -> str:
        """Execute code review."""
        if context.pr_number and context.repository:
            # Get PR details
            repo = self.github_client.get_repository(context.repository)
            pr = repo.get_pull(context.pr_number)
            
            # Prepare review prompt
            prompt = f"""Please review the following pull request:

Title: {pr.title}
Description: {pr.body or 'No description provided'}

Files changed: {pr.changed_files}
Additions: +{pr.additions}
Deletions: -{pr.deletions}

Additional context: {user_input}

Provide a comprehensive code review."""
            
            return self.generate_response(prompt, use_history=False)
        
        return self.generate_response(f"Review this code:\n\n{user_input}", use_history=False)


class IssueTriageAgent(Agent):
    """Agent specialized in issue triage and management."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Issue Triage Agent",
            description="Triages and categorizes GitHub issues",
            **kwargs
        )
    
    def get_system_prompt(self) -> str:
        return """You are an expert at triaging GitHub issues. Your role is to:
1. Categorize issues by type (bug, feature, documentation, etc.)
2. Assess priority and severity
3. Suggest appropriate labels
4. Identify duplicates or related issues
5. Provide actionable next steps"""
    
    def execute(self, context: AgentContext, user_input: str) -> str:
        """Execute issue triage."""
        if context.issue_number and context.repository:
            # Get issue details
            repo = self.github_client.get_repository(context.repository)
            issue = repo.get_issue(context.issue_number)
            
            prompt = f"""Please triage the following GitHub issue:

Title: {issue.title}
Body: {issue.body or 'No description provided'}
Labels: {[label.name for label in issue.labels]}
State: {issue.state}

Provide triage analysis including category, priority, suggested labels, and next steps."""
            
            return self.generate_response(prompt, use_history=False)
        
        return self.generate_response(f"Triage this issue:\n\n{user_input}", use_history=False)


class DocumentationAgent(Agent):
    """Agent specialized in documentation generation and updates."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Documentation Agent",
            description="Generates and improves documentation",
            **kwargs
        )
    
    def get_system_prompt(self) -> str:
        return """You are an expert technical writer. Your role is to:
1. Create clear, comprehensive documentation
2. Explain complex concepts in simple terms
3. Provide code examples where appropriate
4. Maintain consistent formatting and style
5. Ensure documentation is up-to-date with code changes"""
    
    def execute(self, context: AgentContext, user_input: str) -> str:
        """Execute documentation generation."""
        return self.generate_response(f"Generate documentation for:\n\n{user_input}", use_history=False)
