#!/usr/bin/env python3
"""
Example: Using Multiple Agents Together
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import AgentManager, AgentContext


def main():
    """Demonstrate using multiple agents together."""
    print("Multiple Agents Example\n")
    
    # Create agent manager
    manager = AgentManager()
    
    # Create multiple agents
    print("Creating agents...")
    code_reviewer = manager.create_agent('code_review', 'reviewer')
    doc_agent = manager.create_agent('documentation', 'documenter')
    
    print(f"✓ Created: {code_reviewer.name}")
    print(f"✓ Created: {doc_agent.name}\n")
    
    # Code to review and document
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    """
    
    # Step 1: Review the code
    print("Step 1: Code Review")
    print("-" * 50)
    context = AgentContext()
    review = code_reviewer.execute(context, f"Review this code:\n{code}")
    print(review)
    print("\n")
    
    # Step 2: Generate documentation
    print("Step 2: Generate Documentation")
    print("-" * 50)
    docs = doc_agent.execute(context, f"Generate documentation for:\n{code}")
    print(docs)
    print("\n")
    
    # List all active agents
    print("Active Agents:")
    print("-" * 50)
    for agent_info in manager.list_agents():
        print(f"  - {agent_info['id']}: {agent_info['name']}")


if __name__ == '__main__':
    main()
