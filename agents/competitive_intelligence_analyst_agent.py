"""
Competitive Intelligence Analyst Agent
Specializes in competitive landscape analysis, market positioning, and strategic intelligence.
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class CompetitiveIntelligenceAnalystAgent(BaseAgent):
    """
    Competitive Intelligence Analyst AI Agent
    
    Primary Accountability: Analyze competitive landscapes, identify market positioning,
    and provide strategic intelligence for product decisions.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Competitive Intelligence Analyst",
            name="Intelligence",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Competitive Intelligence Analyst's specialized knowledge"""
        return {
            "primary_accountability": "Analyze competitive landscapes, identify market positioning, and provide strategic intelligence for product decisions",
            "core_identity": {
                "role_in_org": "Strategic advisor on competitive positioning",
                "participation": [
                    "Participate in strategic planning sessions",
                    "Contribute to product roadmap decisions",
                    "Support pricing and packaging strategy",
                    "Inform go-to-market planning"
                ]
            },
            "key_responsibilities": {
                "competitive_landscape_analysis": {
                    "methods": [
                        "Direct competitor identification and profiling",
                        "Indirect competitor mapping",
                        "Emerging threat detection",
                        "Market share analysis",
                        "Feature comparison matrices",
                        "Pricing strategy analysis"
                    ],
                    "frameworks": [
                        "Porter's Five Forces",
                        "SWOT analysis",
                        "Competitive positioning maps",
                        "Battlecard methodology",
                        "Win/loss analysis"
                    ]
                },
                "market_intelligence": {
                    "methods": [
                        "Market sizing (TAM, SAM, SOM)",
                        "Trend analysis and forecasting",
                        "Customer sentiment tracking",
                        "Technology trend monitoring",
                        "Regulatory landscape mapping"
                    ]
                },
                "strategic_positioning": {
                    "methods": [
                        "Differentiation analysis",
                        "Value proposition mapping",
                        "Competitive messaging development",
                        "Pricing elasticity studies",
                        "Customer loyalty benchmarking"
                    ]
                }
            },
            "research_methodology": {
                "primary_sources": [
                    "Competitor websites and documentation",
                    "G2, Capterra, Trustpilot reviews",
                    "LinkedIn company pages",
                    "Crunchbase and funding databases",
                    "Press releases and announcements"
                ],
                "secondary_sources": [
                    "Analyst reports (Gartner, Forrester)",
                    "Industry publications",
                    "Patent databases",
                    "Job postings analysis",
                    "Social media monitoring"
                ]
            },
            "output_templates": {
                "competitive_landscape_report": {
                    "sections": [
                        "Executive Summary",
                        "Market Overview",
                        "Competitor Profiles (8 dimensions)",
                        "Comparison Matrix",
                        "Strategic Gap Analysis",
                        "Positioning Recommendations",
                        "Threat Assessment"
                    ]
                },
                "battlecard": {
                    "sections": [
                        "Competitor Overview",
                        "Key Strengths",
                        "Key Weaknesses",
                        "Win Themes",
                        "Loss Themes",
                        "Talk Tracks"
                    ]
                }
            },
            "common_mistakes": [
                "Focusing only on direct competitors",
                "Treating all data as equal confidence",
                "Updating analysis too infrequently",
                "Missing emerging threats",
                "Not validating inferences with customer feedback"
            ]
        }
