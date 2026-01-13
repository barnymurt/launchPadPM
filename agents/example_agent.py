"""
Example Agent Implementation
Demonstrates how to create a new agent by extending BaseAgent.
This serves as a template for creating the 8 Scrum team agents.
"""

from typing import Dict, List, Any
from .base_agent import BaseAgent, AgentResponse, AgentContext


class ExampleAgent(BaseAgent):
    """
    Example agent implementation showing the pattern for all Scrum team agents.
    
    This is a template - replace with actual agent implementations:
    - ProductOwnerAgent
    - ScrumMasterAgent
    - DevelopmentEngineerAgent
    - QAEngineerAgent
    - BusinessAnalystAgent
    - DataMetricsAnalystAgent
    - UXUIDesignerAgent
    - ProductMarketingExecutiveAgent
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Example Agent",
            name="Example",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define this agent's specialized knowledge and responsibilities"""
        return {
            "primary_responsibilities": [
                "Example responsibility 1",
                "Example responsibility 2"
            ],
            "key_frameworks": [
                "Framework 1",
                "Framework 2"
            ],
            "collaboration_patterns": {
                "receives_from": ["Other Role 1"],
                "provides_to": ["Other Role 2"]
            }
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query and return a response.
        
        This is where the agent's main logic lives. In a full implementation,
        this would use LLM APIs or rule-based logic to generate responses.
        """
        # Example: Simple keyword-based routing
        query_lower = query.lower()
        
        if "priority" in query_lower or "prioritize" in query_lower:
            return self._handle_prioritization_query(query, **kwargs)
        elif "estimate" in query_lower or "effort" in query_lower:
            return self._handle_estimation_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_prioritization_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about prioritization"""
        return self.format_response(
            response_text=f"As the {self.role}, I would analyze this prioritization request "
                         f"based on user value, business impact, and technical feasibility.",
            recommendations=[
                "Gather user feedback through customer interviews",
                "Assess business value using opportunity solution trees",
                "Consult with Development Engineer for technical feasibility"
            ],
            questions=[
                "What is the expected user outcome?",
                "What evidence supports this priority?"
            ],
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "data_metrics_analyst"]
        )
    
    def _handle_estimation_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about effort estimation"""
        return self.format_response(
            response_text=f"As the {self.role}, I would need more information to provide "
                         f"an accurate estimate. Let me break this down...",
            recommendations=[
                "Break down the work into smaller, estimable tasks",
                "Consider dependencies and technical complexity",
                "Review similar past work for reference"
            ],
            questions=[
                "What is the scope of this work?",
                "Are there any technical dependencies?"
            ]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries"""
        return self.format_response(
            response_text=f"As the {self.role}, I understand your question: '{query}'. "
                         f"Let me provide guidance based on Scrum best practices and "
                         f"continuous discovery principles.",
            recommendations=[
                "Follow Scrum values: Commitment, Courage, Focus, Openness, Respect",
                "Base decisions on evidence and data",
                "Collaborate with cross-functional team members"
            ]
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted"""
        query_lower = query.lower()
        needs = []
        
        if "technical" in query_lower or "implementation" in query_lower:
            needs.append("development_engineer")
        
        if "data" in query_lower or "metrics" in query_lower:
            needs.append("data_metrics_analyst")
        
        if "design" in query_lower or "ux" in query_lower:
            needs.append("ux_ui_designer")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define collaboration patterns"""
        return {
            "receives_from": {
                "data_metrics_analyst": "User behavior data and analytics insights",
                "ux_ui_designer": "User research findings and design recommendations"
            },
            "provides_to": {
                "development_engineer": "Prioritized requirements and acceptance criteria",
                "scrum_master": "Product backlog updates and sprint goals"
            }
        }
