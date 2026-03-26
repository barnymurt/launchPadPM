"""
Innovation Lead Agent
Specializes in innovation strategy and emerging technology assessment.
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class InnovationLeadAgent(BaseAgent):
    """Innovation Lead AI Agent"""
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Innovation Lead",
            name="Innovation Lead",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Drive innovation strategy and assess emerging technologies",
            "core_identity": {
                "role_in_org": "Innovation strategist",
                "participation": ["Product roadmap planning", "Technology decisions", "Innovation programs"]
            },
            "key_responsibilities": {
                "innovation_strategy": [
                    "Technology radar maintenance",
                    "Emerging tech assessment",
                    "Innovation portfolio management",
                    "Build vs. buy analysis"
                ],
                "emerging_tech": [
                    "AI/ML opportunity assessment",
                    "Web3 and decentralized systems",
                    "AR/VR applications",
                    "IoT integration potential"
                ]
            }
        }
