#!/usr/bin/env python3
"""
Example: Using the Issue Triage Agent
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import AgentManager, AgentContext


def main():
    """Demonstrate issue triage agent usage."""
    print("Issue Triage Agent Example\n")
    
    # Create agent manager
    manager = AgentManager()
    
    # Create issue triage agent
    print("Creating issue triage agent...")
    agent = manager.create_agent('issue_triage', 'triager')
    print(f"✓ Created: {agent.name}\n")
    
    # Example: Triage an issue
    print("Example: Triage a bug report")
    print("-" * 50)
    
    issue_text = """
Title: Application crashes when uploading large files

Description:
When I try to upload files larger than 10MB, the application crashes with
an out of memory error. This happens consistently on both Chrome and Firefox.

Steps to reproduce:
1. Navigate to upload page
2. Select a file > 10MB
3. Click upload
4. Application crashes

Expected: File should upload successfully
Actual: Application crashes
    """
    
    context = AgentContext()
    response = agent.execute(context, f"Triage this issue:\n{issue_text}")
    print(response)


if __name__ == '__main__':
    main()
