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
    _shared_context: Optional[AgentContext] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def register_agent(cls, agent: BaseAgent) -> None:
        """
        Register an agent instance in the registry.
        
        Args:
            agent: BaseAgent instance to register
            
        Raises:
            TypeError: If agent is not a BaseAgent instance
            ValueError: If agent role is empty or already registered (will overwrite)
        """
        # Input validation
        if not isinstance(agent, BaseAgent):
            raise TypeError("agent must be an instance of BaseAgent")
        if not agent.role or not agent.role.strip():
            raise ValueError("agent.role cannot be empty")
        
        # Normalize role key for consistent lookup
        role_key = agent.role.lower().replace(" ", "_").replace("/", "_")
        
        # Register agent (overwrites if already exists - this is intentional for updates)
        cls._agents[role_key] = agent
        
        # Apply shared context if one is set
        if cls._shared_context:
            agent.context = cls._shared_context
    
    @classmethod
    def get_agent(cls, role: str) -> Optional[BaseAgent]:
        """
        Get an agent by role name.
        
        This method performs flexible role matching:
        1. Exact normalized match (e.g., "Product Owner" -> "product_owner")
        2. Case-insensitive search across all registered agents
        
        Args:
            role: Role name (e.g., "Product Owner", "product_owner", "ProductOwner")
            
        Returns:
            BaseAgent instance or None if not found
            
        Raises:
            ValueError: If role is empty or None
        """
        # Input validation
        if not role or not role.strip():
            raise ValueError("role cannot be empty or None")
        
        # Normalize input role for matching
        normalized_role = role.lower().replace(" ", "_").replace("/", "_").strip()
        
        # Try exact match first (most common case, fastest)
        if normalized_role in cls._agents:
            return cls._agents[normalized_role]
        
        # Try case-insensitive search across all registered agents
        # This handles edge cases where role key might have slight variations
        for key, agent in cls._agents.items():
            if key.lower() == normalized_role:
                return agent
        
        # Agent not found
        return None
    
    @classmethod
    def get_all_agents(cls) -> Dict[str, BaseAgent]:
        """Get all registered agents"""
        return cls._agents.copy()
    
    @classmethod
    def list_roles(cls) -> List[str]:
        """
        List all registered agent roles.
        
        Returns:
            List of role names (normalized keys) for all registered agents
        """
        return [agent.role for agent in cls._agents.values()]
    
    @classmethod
    def set_shared_context(cls, context: AgentContext) -> None:
        """
        Set shared context for all agents.
        
        Args:
            context: AgentContext to share across all registered agents
            
        Raises:
            TypeError: If context is not an AgentContext instance
        """
        if not isinstance(context, AgentContext):
            raise TypeError("context must be an AgentContext instance")
        
        cls._shared_context = context
        # Apply to all currently registered agents
        for agent in cls._agents.values():
            agent.context = context
    
    @classmethod
    def get_shared_context(cls) -> Optional[AgentContext]:
        """
        Get the shared context for all agents.
        
        Returns:
            AgentContext if set, None otherwise
        """
        return cls._shared_context
    
    @classmethod
    def set_context(cls, context: AgentContext) -> None:
        """
        Alias for set_shared_context for backward compatibility.
        
        Args:
            context: AgentContext to share across all registered agents
        """
        cls.set_shared_context(context)
    
    @classmethod
    def clear_registry(cls) -> None:
        """
        Clear all registered agents (useful for testing).
        
        WARNING: This will remove all registered agents and shared context.
        Use with caution, primarily for testing purposes.
        """
        cls._agents.clear()
        cls._shared_context = None
