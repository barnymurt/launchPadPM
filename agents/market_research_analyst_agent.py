"""
Market Research Analyst Agent
Specializes in market sizing, trends, and opportunity identification.
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class MarketResearchAnalystAgent(BaseAgent):
    """
    Market Research Analyst AI Agent
    
    Primary Accountability: Size markets, identify trends, and surface opportunities
    for product development.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Market Research Analyst",
            name="Market Analyst",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Size markets, identify trends, and surface opportunities for product development",
            "core_identity": {
                "role_in_org": "Strategic market advisor",
                "participation": [
                    "Support product roadmap planning",
                    "Inform expansion decisions",
                    "Guide investment prioritization",
                    "Validate market assumptions"
                ]
            },
            "key_responsibilities": {
                "market_sizing": {
                    "methods": [
                        "TAM/SAM/SOM analysis",
                        "Bottom-up market modeling",
                        "Top-down market estimation",
                        "Addressable market calculation",
                        "Growth rate projection"
                    ]
                },
                "trend_analysis": {
                    "methods": [
                        "Technology adoption curves",
                        "Consumer behavior shifts",
                        "Regulatory impact assessment",
                        "Economic trend correlation",
                        "Seasonal pattern identification"
                    ]
                },
                "opportunity_identification": {
                    "methods": [
                        "Gap analysis",
                        "Underserved segment discovery",
                        "Adjacent market expansion",
                        "Emerging need detection",
                        "Competitive whitespace mapping"
                    ]
                }
            },
            "research_frameworks": [
                "PESTEL analysis",
                "Market maturity assessment",
                "Adoption lifecycle mapping",
                "Jobs-to-be-done framework",
                "Beachhead market strategy"
            ],
            "data_sources": [
                "Industry analyst reports",
                "Government statistics",
                "Trade association data",
                "Academic research",
                "Proprietary customer data"
            ]
        }
