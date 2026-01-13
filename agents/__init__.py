"""
Scrum Team AI Agents Framework
A modular system for managing specialized AI agents in a Scrum product development team.
"""

__version__ = "1.0.0"

from .base_agent import BaseAgent
from .agent_registry import AgentRegistry

# Import agent implementations
_agents = ['BaseAgent', 'AgentRegistry']
try:
    from .product_owner_agent import ProductOwnerAgent
    _agents.append('ProductOwnerAgent')
except ImportError:
    pass

try:
    from .scrum_master_agent import ScrumMasterAgent
    _agents.append('ScrumMasterAgent')
except ImportError:
    pass

__all__ = _agents
