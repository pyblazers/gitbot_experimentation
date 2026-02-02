"""
Agent manager for creating and managing multiple agents.
"""
from typing import Dict, List, Optional, Type
from .base_agent import Agent, AgentContext, CodeReviewAgent, IssueTriageAgent, DocumentationAgent
from ..models import AIModel
from ..github_integration import GitHubClient


class AgentManager:
    """Manages multiple AI agents."""
    
    def __init__(self):
        """Initialize agent manager."""
        self.agents: Dict[str, Agent] = {}
        self.agent_types: Dict[str, Type[Agent]] = {
            'code_review': CodeReviewAgent,
            'issue_triage': IssueTriageAgent,
            'documentation': DocumentationAgent,
        }
    
    def create_agent(self, agent_type: str, agent_id: Optional[str] = None,
                     ai_model: Optional[AIModel] = None,
                     github_client: Optional[GitHubClient] = None) -> Agent:
        """
        Create a new agent instance.
        
        Args:
            agent_type: Type of agent to create
            agent_id: Unique identifier for the agent (defaults to agent_type)
            ai_model: Optional AI model to use
            github_client: Optional GitHub client
            
        Returns:
            Created agent instance
        """
        if agent_type not in self.agent_types:
            raise ValueError(f"Unknown agent type: {agent_type}. Available: {list(self.agent_types.keys())}")
        
        agent_id = agent_id or agent_type
        agent_class = self.agent_types[agent_type]
        
        kwargs = {}
        if ai_model:
            kwargs['ai_model'] = ai_model
        if github_client:
            kwargs['github_client'] = github_client
        
        agent = agent_class(**kwargs)
        self.agents[agent_id] = agent
        
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID."""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, str]]:
        """List all registered agents."""
        return [
            {
                "id": agent_id,
                "name": agent.name,
                "description": agent.description
            }
            for agent_id, agent in self.agents.items()
        ]
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent by ID."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False
    
    def execute_agent(self, agent_id: str, context: AgentContext, user_input: str) -> str:
        """
        Execute a specific agent.
        
        Args:
            agent_id: ID of the agent to execute
            context: Execution context
            user_input: User input
            
        Returns:
            Agent response
        """
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent not found: {agent_id}")
        
        return agent.execute(context, user_input)
    
    def register_agent_type(self, type_name: str, agent_class: Type[Agent]):
        """Register a custom agent type."""
        self.agent_types[type_name] = agent_class
    
    def get_available_agent_types(self) -> List[str]:
        """Get list of available agent types."""
        return list(self.agent_types.keys())
