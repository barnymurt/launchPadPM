"""Agile Coach Agent"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext

class AgileCoachAgent(BaseAgent):
    def __init__(self, context: AgentContext = None):
        super().__init__(role="Agile Coach", name="Agile Coach", context=context)
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Coach teams on agile practices and continuous improvement",
            "key_responsibilities": {
                "coaching": ["Team coaching", "Ceremony facilitation", "Impediment removal"],
                "methodology": ["Scrum", "Kanban", "SAFe", "Lean"]
            }
        }
