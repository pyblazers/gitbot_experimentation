#!/usr/bin/env python3
"""
Simple tests to verify the AI Agent system works.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.config import config
        print("✓ Config module")
        
        from src.models import ModelFactory
        print("✓ Models module")
        
        from src.github_integration import GitHubClient
        print("✓ GitHub integration module")
        
        from src.agents import AgentManager, Agent, AgentContext
        print("✓ Agents module")
        
        from src.server import app
        print("✓ Server module")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from src.config import config
        
        # Check that config attributes exist
        assert hasattr(config, 'GITHUB_TOKEN')
        assert hasattr(config, 'DEFAULT_MODEL')
        assert hasattr(config, 'SERVER_PORT')
        
        print("✓ Configuration structure valid")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_agent_manager():
    """Test agent manager functionality."""
    print("\nTesting agent manager...")
    
    try:
        from src.agents import AgentManager
        
        manager = AgentManager()
        
        # Test listing agent types
        types = manager.get_available_agent_types()
        assert len(types) > 0
        assert 'code_review' in types
        assert 'issue_triage' in types
        assert 'documentation' in types
        
        print(f"✓ Found {len(types)} agent types")
        
        # Test listing agents (should be empty initially)
        agents = manager.list_agents()
        assert isinstance(agents, list)
        
        print("✓ Agent manager working")
        return True
    except Exception as e:
        print(f"✗ Agent manager test failed: {e}")
        return False


def test_agent_creation():
    """Test creating agents without API keys."""
    print("\nTesting agent creation (without API calls)...")
    
    try:
        from src.agents import AgentContext
        
        # Just test that AgentContext can be created
        context = AgentContext(
            repository="test/repo",
            issue_number=1
        )
        
        assert context.repository == "test/repo"
        assert context.issue_number == 1
        
        print("✓ AgentContext working")
        
        # Note: We can't create actual agents without API keys
        print("⚠ Skipping agent creation (requires API keys)")
        
        return True
    except Exception as e:
        print(f"✗ Agent creation test failed: {e}")
        return False


def test_api_routes():
    """Test that API routes are defined."""
    print("\nTesting API routes...")
    
    try:
        from src.server import app
        
        # Get all route rules
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        # Check key routes exist
        assert any('/health' in route for route in routes)
        assert any('/agents' in route for route in routes)
        
        print(f"✓ Found {len(routes)} API routes")
        return True
    except Exception as e:
        print(f"✗ API routes test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("AI Agent System - Basic Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_agent_manager,
        test_agent_creation,
        test_api_routes,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        print("\n⚠️  Some tests failed. Check error messages above.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        print("\nNext steps:")
        print("1. Configure your .env file with API keys")
        print("2. Run: python cli.py config validate")
        print("3. Run: python cli.py server")


if __name__ == '__main__':
    main()
