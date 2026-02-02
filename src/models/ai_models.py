"""
AI Model abstraction layer supporting multiple providers.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import anthropic
import openai


class AIModel(ABC):
    """Abstract base class for AI models."""
    
    def __init__(self, api_key: str, model: str, max_tokens: int = 4096, temperature: float = 0.7):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response from the AI model."""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response using chat format."""
        pass


class ClaudeModel(AIModel):
    """Claude/Anthropic AI model implementation."""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229", 
                 max_tokens: int = 4096, temperature: float = 0.7):
        super().__init__(api_key, model, max_tokens, temperature)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response from Claude."""
        messages = [{"role": "user", "content": prompt}]
        
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": messages
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response using chat format."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages
        )
        return response.content[0].text


class OpenAIModel(AIModel):
    """OpenAI GPT model implementation."""
    
    def __init__(self, api_key: str, model: str = "gpt-4", 
                 max_tokens: int = 4096, temperature: float = 0.7):
        super().__init__(api_key, model, max_tokens, temperature)
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response from OpenAI."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages
        )
        return response.choices[0].message.content
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response using chat format."""
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages
        )
        return response.choices[0].message.content


class ModelFactory:
    """Factory for creating AI model instances."""
    
    @staticmethod
    def create_model(provider: str, api_key: str, model: Optional[str] = None,
                     max_tokens: int = 4096, temperature: float = 0.7) -> AIModel:
        """Create an AI model instance based on provider."""
        provider = provider.lower()
        
        if provider == 'anthropic' or provider == 'claude':
            model = model or "claude-3-sonnet-20240229"
            return ClaudeModel(api_key, model, max_tokens, temperature)
        elif provider == 'openai':
            model = model or "gpt-4"
            return OpenAIModel(api_key, model, max_tokens, temperature)
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
