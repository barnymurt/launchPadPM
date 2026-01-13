"""
Base Agent Class
Provides the foundation for all Scrum team AI agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import json


@dataclass
class AgentContext:
    """Context information shared across agents"""
    product_name: str = ""
    sprint_number: int = 0
    current_phase: str = ""  # planning, development, review, retrospective
    shared_knowledge: Dict[str, Any] = field(default_factory=dict)
    team_members: List[str] = field(default_factory=list)


@dataclass
class AgentResponse:
    """Standardized response from an agent"""
    role: str
    response: str
    recommendations: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)
    requires_collaboration: bool = False
    collaborating_roles: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all Scrum team AI agents.
    
    Each agent should inherit from this class and implement:
    - process_query(): Main logic for handling queries
    - get_role_specific_knowledge(): Agent's specialized knowledge
    """
    
    def __init__(self, role: str, name: str, context: Optional[AgentContext] = None):
        """
        Initialize the agent.
        
        Args:
            role: The Scrum role (e.g., "Product Owner", "Scrum Master")
            name: Human-readable name for the agent
            context: Shared context across all agents
        """
        self.role = role
        self.name = name
        self.context = context or AgentContext()
        self.scrum_knowledge = self._load_scrum_knowledge()
        self.continuous_discovery_knowledge = self._load_continuous_discovery_knowledge()
        self.role_knowledge = self.get_role_specific_knowledge()
    
    def _load_scrum_knowledge(self) -> Dict[str, Any]:
        """Load shared Scrum framework knowledge"""
        return {
            "pillars": ["Transparency", "Inspection", "Adaptation"],
            "values": ["Commitment", "Courage", "Focus", "Openness", "Respect"],
            "events": ["Sprint", "Sprint Planning", "Daily Scrum", "Sprint Review", "Sprint Retrospective"],
            "artifacts": ["Product Backlog", "Sprint Backlog", "Increment"],
            "definition_of_done": "The work is complete, tested, and potentially shippable"
        }
    
    def _load_continuous_discovery_knowledge(self) -> Dict[str, Any]:
        """Load Continuous Discovery Habits framework knowledge"""
        return {
            "weekly_customer_interviews": True,
            "opportunity_solution_trees": {
                "structure": "Outcome → Opportunities → Solutions → Assumptions",
                "purpose": "Visualize and prioritize product opportunities"
            },
            "evidence_based_decision_making": True,
            "assumption_testing": True
        }
    
    @abstractmethod
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """
        Return role-specific knowledge and responsibilities.
        Must be implemented by each agent subclass.
        """
        pass
    
    @abstractmethod
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query and return a response.
        Must be implemented by each agent subclass.
        
        Args:
            query: The user's question or request
            **kwargs: Additional context or parameters
            
        Returns:
            AgentResponse object with the agent's response
        """
        pass
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """
        Identify which other roles should be consulted for this query.
        Override in subclasses for role-specific collaboration logic.
        """
        return []
    
    def format_response(self, response_text: str, recommendations: List[str] = None,
                       questions: List[str] = None, requires_collaboration: bool = False,
                       collaborating_roles: List[str] = None,
                       evidence: Dict[str, Any] = None) -> AgentResponse:
        """Helper method to format agent responses consistently"""
        return AgentResponse(
            role=self.role,
            response=response_text,
            recommendations=recommendations or [],
            questions=questions or [],
            requires_collaboration=requires_collaboration,
            collaborating_roles=collaborating_roles or [],
            evidence=evidence or {}
        )
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """
        Define what information this agent receives from and provides to other roles.
        Override in subclasses.
        """
        return {}
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(role='{self.role}', name='{self.name}')"
