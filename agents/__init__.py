"""
Scrum Team AI Agents Framework
A modular system for managing specialized AI agents in a Scrum product development team.
"""

__version__ = "1.0.0"

from .base_agent import BaseAgent
from .agent_registry import AgentRegistry

# Import agent implementations
try:
    from .product_owner_agent import ProductOwnerAgent
    __all__ = ['BaseAgent', 'AgentRegistry', 'ProductOwnerAgent']
except ImportError:
    __all__ = ['BaseAgent', 'AgentRegistry']
