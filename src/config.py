"""
Configuration management for the AI Agent system.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for AI Agent system."""
    
    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY', '')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # GitHub Configuration
    GITHUB_TOKEN: str = os.getenv('GITHUB_TOKEN', '')
    GITHUB_USERNAME: str = os.getenv('GITHUB_USERNAME', '')
    
    # Server Configuration
    SERVER_HOST: str = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT: int = int(os.getenv('SERVER_PORT', '5000'))
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Agent Configuration
    DEFAULT_MODEL: str = os.getenv('DEFAULT_MODEL', 'claude-3-sonnet-20240229')
    MAX_TOKENS: int = int(os.getenv('MAX_TOKENS', '4096'))
    TEMPERATURE: float = float(os.getenv('TEMPERATURE', '0.7'))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        required_keys = [
            ('GITHUB_TOKEN', cls.GITHUB_TOKEN),
        ]
        
        missing = [key for key, value in required_keys if not value]
        
        if missing:
            print(f"Warning: Missing required configuration: {', '.join(missing)}")
            return False
        
        return True
    
    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        """Get API key for a specific AI provider."""
        keys = {
            'anthropic': cls.ANTHROPIC_API_KEY,
            'openai': cls.OPENAI_API_KEY,
        }
        return keys.get(provider.lower())


config = Config()
