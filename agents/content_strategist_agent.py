"""
Content Strategist Agent
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class ContentStrategistAgent(BaseAgent):
    def __init__(self, context: AgentContext = None):
        super().__init__(role="Content Strategist", name="Content Strategist", context=context)
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Develop content strategy and messaging for products",
            "key_responsibilities": {
                "content_strategy": ["Content planning", "Messaging frameworks", "Audience segmentation"],
                " copywriting": ["Brand voice", "SEO content", "Product documentation"]
            }
        }
