"""
Flask REST API server for AI Agent system.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
import logging

from ..agents import AgentManager, AgentContext
from ..config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Initialize agent manager
agent_manager = AgentManager()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "AI Agent Server"
    })


@app.route('/agents', methods=['GET'])
def list_agents():
    """List all available agents."""
    try:
        agents = agent_manager.list_agents()
        agent_types = agent_manager.get_available_agent_types()
        
        return jsonify({
            "agents": agents,
            "available_types": agent_types
        })
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/agents', methods=['POST'])
def create_agent():
    """Create a new agent."""
    try:
        data = request.json
        agent_type = data.get('type')
        agent_id = data.get('id')
        
        if not agent_type:
            return jsonify({"error": "Agent type is required"}), 400
        
        agent = agent_manager.create_agent(agent_type, agent_id)
        
        return jsonify({
            "message": "Agent created successfully",
            "agent": agent.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id: str):
    """Get agent details."""
    try:
        agent = agent_manager.get_agent(agent_id)
        if not agent:
            return jsonify({"error": "Agent not found"}), 404
        
        return jsonify(agent.to_dict())
    except Exception as e:
        logger.error(f"Error getting agent: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id: str):
    """Delete an agent."""
    try:
        success = agent_manager.remove_agent(agent_id)
        if not success:
            return jsonify({"error": "Agent not found"}), 404
        
        return jsonify({"message": "Agent deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting agent: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/agents/<agent_id>/execute', methods=['POST'])
def execute_agent(agent_id: str):
    """Execute an agent with given input."""
    try:
        data = request.json
        user_input = data.get('input', '')
        
        # Build context
        context = AgentContext(
            repository=data.get('repository'),
            issue_number=data.get('issue_number'),
            pr_number=data.get('pr_number'),
            metadata=data.get('metadata', {})
        )
        
        response = agent_manager.execute_agent(agent_id, context, user_input)
        
        return jsonify({
            "response": response,
            "context": {
                "repository": context.repository,
                "timestamp": context.timestamp
            }
        })
    except Exception as e:
        logger.error(f"Error executing agent: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/agents/<agent_id>/conversation', methods=['DELETE'])
def clear_conversation(agent_id: str):
    """Clear agent conversation history."""
    try:
        agent = agent_manager.get_agent(agent_id)
        if not agent:
            return jsonify({"error": "Agent not found"}), 404
        
        agent.clear_conversation()
        return jsonify({"message": "Conversation cleared"})
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/github/repositories', methods=['GET'])
def list_repositories():
    """List GitHub repositories."""
    try:
        # This would require GitHub client initialization
        return jsonify({"message": "Not implemented yet"}), 501
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        return jsonify({"error": str(e)}), 500


def run_server():
    """Run the Flask server."""
    config.validate()
    logger.info(f"Starting AI Agent Server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=False
    )


if __name__ == '__main__':
    run_server()
