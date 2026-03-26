"""
Opportunity Analyst Agent
Specializes in identifying and evaluating product opportunities.
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class OpportunityAnalystAgent(BaseAgent):
    """Opportunity Analyst AI Agent"""
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Opportunity Analyst",
            name="Opportunity Analyst",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Identify and evaluate product opportunities using structured frameworks",
            "core_identity": {
                "role_in_org": "Innovation catalyst",
                "participation": [
                    "Support roadmap prioritization",
                    "Identify market gaps",
                    "Evaluate opportunity viability",
                    "Challenge assumptions"
                ]
            },
            "key_responsibilities": {
                "opportunity_identification": [
                    "Market gap analysis",
                    "Customer pain point mapping",
                    "Technology trend scanning",
                    "Competitive whitespace discovery"
                ],
                "opportunity_evaluation": [
                    "ROI modeling",
                    "Effort vs. impact assessment",
                    "Risk assessment",
                    "Strategic fit analysis"
                ]
            },
            "frameworks": [
                "RICE scoring",
                "ICE methodology",
                "Opportunity Solution Trees",
                "Kano model",
                "MoSCoW prioritization"
            ]
        }
