"""
Configuration settings for the AI agents framework
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json
import os
from pathlib import Path


@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    enabled: bool = True
    model: str = "default"  # LLM model to use
    temperature: float = 0.7
    max_tokens: int = 2000
    custom_prompts: Dict[str, str] = field(default_factory=dict)


@dataclass
class Settings:
    """Main settings class"""
    # Project settings
    product_name: str = "Product"
    sprint_duration_days: int = 14
    
    # Agent settings
    agents: Dict[str, AgentConfig] = field(default_factory=dict)
    
    # Framework settings
    enable_collaboration: bool = True
    enable_continuous_discovery: bool = True
    enable_opportunity_solution_trees: bool = True
    
    # LLM settings (for future integration)
    llm_provider: str = "openai"  # openai, anthropic, etc.
    api_key: Optional[str] = None
    
    # Notion integration settings
    notion_enabled: bool = False
    notion_api_token: Optional[str] = None
    notion_team_space_id: Optional[str] = None
    
    # Paths
    agent_prompts_dir: str = "agent_prompts"
    knowledge_base_dir: str = "knowledge_base"
    
    @classmethod
    def load_from_file(cls, config_path: str = "config.json") -> 'Settings':
        """Load settings from a JSON file"""
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                data = json.load(f)
                return cls.from_dict(data)
        return cls()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Settings':
        """Create Settings from a dictionary"""
        settings = cls()
        
        if "product_name" in data:
            settings.product_name = data["product_name"]
        if "sprint_duration_days" in data:
            settings.sprint_duration_days = data["sprint_duration_days"]
        if "agents" in data:
            for role, config in data["agents"].items():
                settings.agents[role] = AgentConfig(**config)
        if "enable_collaboration" in data:
            settings.enable_collaboration = data["enable_collaboration"]
        if "llm_provider" in data:
            settings.llm_provider = data["llm_provider"]
        if "api_key" in data:
            settings.api_key = data.get("api_key") or os.getenv("LLM_API_KEY")
        
        return settings
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary"""
        return {
            "product_name": self.product_name,
            "sprint_duration_days": self.sprint_duration_days,
            "agents": {
                role: {
                    "enabled": config.enabled,
                    "model": config.model,
                    "temperature": config.temperature,
                    "max_tokens": config.max_tokens
                }
                for role, config in self.agents.items()
            },
            "enable_collaboration": self.enable_collaboration,
            "enable_continuous_discovery": self.enable_continuous_discovery,
            "enable_opportunity_solution_trees": self.enable_opportunity_solution_trees,
            "llm_provider": self.llm_provider,
            "notion_enabled": self.notion_enabled,
            "notion_api_token": self.notion_api_token,
            "notion_team_space_id": self.notion_team_space_id
        }
    
    def save_to_file(self, config_path: str = "config.json") -> None:
        """Save settings to a JSON file"""
        config_file = Path(config_path)
        with open(config_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


def load_settings(config_path: str = "config.json") -> Settings:
    """Convenience function to load settings"""
    if config_path == "config.json":
        app_env = os.getenv("APP_ENV")
        if app_env:
            env_path = Path("config") / f"config.{app_env}.json"
            if env_path.exists():
                config_path = str(env_path)
        else:
            default_path = Path("config") / "config.json"
            if default_path.exists():
                config_path = str(default_path)
    return Settings.load_from_file(config_path)
