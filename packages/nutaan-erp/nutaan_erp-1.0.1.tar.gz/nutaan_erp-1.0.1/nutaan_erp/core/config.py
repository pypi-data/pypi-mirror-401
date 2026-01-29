"""Configuration management for AI Agent SDK"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class AgentConfig:
    """Configuration for AI Agent"""
    
    # API Configuration
    api_key: str
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.1
    max_tokens: int = 4000
    
    # Agent Configuration
    max_iterations: int = 10
    timeout: int = 300  # seconds
    
    # Additional settings
    extra_config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate configuration"""
        if not self.api_key:
            raise ValueError("api_key is required")
        
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("temperature must be between 0 and 1")
        
        if self.max_tokens < 100:
            raise ValueError("max_tokens must be at least 100")
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "AgentConfig":
        """Create config from dictionary"""
        return cls(
            api_key=config_dict.get("api_key", ""),
            model_name=config_dict.get("model_name", "gemini-2.0-flash-exp"),
            temperature=config_dict.get("temperature", 0.1),
            max_tokens=config_dict.get("max_tokens", 4000),
            max_iterations=config_dict.get("max_iterations", 10),
            timeout=config_dict.get("timeout", 300),
            extra_config=config_dict.get("extra_config", {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "api_key": self.api_key,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "max_iterations": self.max_iterations,
            "timeout": self.timeout,
            "extra_config": self.extra_config
        }
