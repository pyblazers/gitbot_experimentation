#!/usr/bin/env python3
"""
Example: Using the Code Review Agent
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import AgentManager, AgentContext


def main():
    """Demonstrate code review agent usage."""
    print("Code Review Agent Example\n")
    
    # Create agent manager
    manager = AgentManager()
    
    # Create code review agent
    print("Creating code review agent...")
    agent = manager.create_agent('code_review', 'reviewer')
    print(f"✓ Created: {agent.name}\n")
    
    # Example 1: Review code snippet
    print("Example 1: Review a code snippet")
    print("-" * 50)
    
    code_snippet = """
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price']
    return total
    """
    
    context = AgentContext()
    response = agent.execute(context, f"Please review this Python code:\n{code_snippet}")
    print(response)
    print("\n")
    
    # Example 2: Review with GitHub context
    print("Example 2: Review with GitHub PR context")
    print("-" * 50)
    
    # Note: This requires actual PR data
    # context = AgentContext(
    #     repository='your-username/your-repo',
    #     pr_number=1
    # )
    # response = agent.execute(context, "Please review this pull request")
    # print(response)
    
    print("Note: To review actual PRs, set up a real repository and PR number")


if __name__ == '__main__':
    main()
