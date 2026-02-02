#!/usr/bin/env python3
"""
Command-line interface for AI Agent system.
"""
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents import AgentManager, AgentContext
from src.config import config


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AI Agent System - Similar to GitHub Copilot for personal use'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Run the API server')
    server_parser.add_argument('--host', default=config.SERVER_HOST, help='Server host')
    server_parser.add_argument('--port', type=int, default=config.SERVER_PORT, help='Server port')
    
    # Agent command
    agent_parser = subparsers.add_parser('agent', help='Interact with agents')
    agent_parser.add_argument('action', choices=['list', 'create', 'execute'], help='Action to perform')
    agent_parser.add_argument('--type', help='Agent type (for create)')
    agent_parser.add_argument('--id', help='Agent ID')
    agent_parser.add_argument('--input', help='Input for agent execution')
    agent_parser.add_argument('--repo', help='Repository name (owner/repo)')
    agent_parser.add_argument('--issue', type=int, help='Issue number')
    agent_parser.add_argument('--pr', type=int, help='Pull request number')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_parser.add_argument('action', choices=['validate', 'show'], help='Action to perform')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'server':
        from src.server import run_server
        print(f"Starting server on {args.host}:{args.port}")
        run_server()
    
    elif args.command == 'agent':
        manager = AgentManager()
        
        if args.action == 'list':
            types = manager.get_available_agent_types()
            print("\nAvailable Agent Types:")
            for agent_type in types:
                print(f"  - {agent_type}")
            
            agents = manager.list_agents()
            if agents:
                print("\nActive Agents:")
                for agent in agents:
                    print(f"  - {agent['id']}: {agent['name']}")
            else:
                print("\nNo active agents")
        
        elif args.action == 'create':
            if not args.type:
                print("Error: --type is required for create action")
                return
            
            agent = manager.create_agent(args.type, args.id)
            print(f"Created agent: {agent.name}")
        
        elif args.action == 'execute':
            if not args.id or not args.input:
                print("Error: --id and --input are required for execute action")
                return
            
            context = AgentContext(
                repository=args.repo,
                issue_number=args.issue,
                pr_number=args.pr
            )
            
            # Create agent if it doesn't exist
            if not manager.get_agent(args.id):
                agent_type = args.id.split('_')[0] if '_' in args.id else args.id
                manager.create_agent(agent_type, args.id)
            
            response = manager.execute_agent(args.id, context, args.input)
            print("\nAgent Response:")
            print(response)
    
    elif args.command == 'config':
        if args.action == 'validate':
            is_valid = config.validate()
            if is_valid:
                print("✓ Configuration is valid")
            else:
                print("✗ Configuration is invalid (see warnings above)")
        
        elif args.action == 'show':
            print("\nCurrent Configuration:")
            print(f"  GitHub Token: {'*' * 20 if config.GITHUB_TOKEN else 'Not set'}")
            print(f"  GitHub Username: {config.GITHUB_USERNAME or 'Not set'}")
            print(f"  Anthropic API Key: {'*' * 20 if config.ANTHROPIC_API_KEY else 'Not set'}")
            print(f"  OpenAI API Key: {'*' * 20 if config.OPENAI_API_KEY else 'Not set'}")
            print(f"  Default Model: {config.DEFAULT_MODEL}")
            print(f"  Server: {config.SERVER_HOST}:{config.SERVER_PORT}")


if __name__ == '__main__':
    main()
