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

try:
    from .development_engineer_agent import DevelopmentEngineerAgent
    _agents.append('DevelopmentEngineerAgent')
except ImportError:
    pass

try:
    from .qa_engineer_agent import QAEngineerAgent
    _agents.append('QAEngineerAgent')
except ImportError:
    pass

try:
    from .business_analyst_agent import BusinessAnalystAgent
    _agents.append('BusinessAnalystAgent')
except ImportError:
    pass

try:
    from .data_metrics_analyst_agent import DataMetricsAnalystAgent
    _agents.append('DataMetricsAnalystAgent')
except ImportError:
    pass

try:
    from .ux_ui_designer_agent import UXUIDesignerAgent
    _agents.append('UXUIDesignerAgent')
except ImportError:
    pass

try:
    from .product_marketing_executive_agent import ProductMarketingExecutiveAgent
    _agents.append('ProductMarketingExecutiveAgent')
except ImportError:
    pass

try:
    from .head_of_product_ceo_agent import HeadOfProductCEOAgent
    _agents.append('HeadOfProductCEOAgent')
except ImportError:
    pass

try:
    from .devops_engineer_agent import DevOpsEngineerAgent
    _agents.append('DevOpsEngineerAgent')
except ImportError:
    pass

__all__ = _agents
