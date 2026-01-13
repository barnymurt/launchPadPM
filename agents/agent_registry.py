"""
Agent Registry
Manages registration and retrieval of all available agents.
"""

from typing import Dict, Optional, List
from .base_agent import BaseAgent, AgentContext


class AgentRegistry:
    """
    Central registry for managing all Scrum team agents.
    Provides singleton-like access to agents.
    """
    
    _instance: Optional['AgentRegistry'] = None
    _agents: Dict[str, BaseAgent] = {}
    _context: Optional[AgentContext] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def register_agent(cls, agent: BaseAgent) -> None:
        """Register an agent instance"""
        cls._agents[agent.role.lower().replace(" ", "_")] = agent
        if cls._context:
            agent.context = cls._context
    
    @classmethod
    def get_agent(cls, role: str) -> Optional[BaseAgent]:
        """
        Get an agent by role name.
        
        Args:
            role: Role name (e.g., "Product Owner", "product_owner", "ProductOwner")
            
        Returns:
            BaseAgent instance or None if not found
        """
        # Try exact match first
        role_key = role.lower().replace(" ", "_")
        if role_key in cls._agents:
            return cls._agents[role_key]
        
        # Try case-insensitive search
        for key, agent in cls._agents.items():
            if key.lower() == role.lower().replace(" ", "_"):
                return agent
        
        return None
    
    @classmethod
    def get_all_agents(cls) -> Dict[str, BaseAgent]:
        """Get all registered agents"""
        return cls._agents.copy()
    
    @classmethod
    def list_roles(cls) -> List[str]:
        """List all registered agent roles"""
        return list(cls._agents.keys())
    
    @classmethod
    def set_context(cls, context: AgentContext) -> None:
        """Set shared context for all agents"""
        cls._context = context
        for agent in cls._agents.values():
            agent.context = context
    
    @classmethod
    def clear_registry(cls) -> None:
        """Clear all registered agents (useful for testing)"""
        cls._agents.clear()
        cls._context = None
