"""
Unit tests for BaseAgent class
Tests core functionality, inheritance, and shared behaviors
"""
import pytest
from agents.base_agent import BaseAgent, AgentContext, AgentResponse
from abc import ABC


class ConcreteTestAgent(BaseAgent):
    """Test agent implementation for testing BaseAgent"""
    
    def get_role_specific_knowledge(self):
        return {"test": "knowledge"}
    
    def process_query(self, query: str, **kwargs):
        return self.format_response(
            response_text=f"Test response to: {query}",
            recommendations=["Test recommendation"]
        )


class TestBaseAgent:
    """Test suite for BaseAgent"""
    
    def test_base_agent_is_abstract(self):
        """Test that BaseAgent cannot be instantiated directly"""
        with pytest.raises(TypeError):
            BaseAgent(role="Test", name="Test")
    
    def test_base_agent_initialization(self, agent_context):
        """Test BaseAgent initialization with context"""
        agent = TestAgent(role="Test Role", name="Test", context=agent_context)
        assert agent.role == "Test Role"
        assert agent.name == "Test"
        assert agent.context == agent_context
        assert agent.context.product_name == "Test Product"
    
    def test_base_agent_default_context(self):
        """Test BaseAgent creates default context if none provided"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        assert agent.context is not None
        assert isinstance(agent.context, AgentContext)
    
    def test_scrum_knowledge_loaded(self):
        """Test that Scrum knowledge is loaded"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        assert "pillars" in agent.scrum_knowledge
        assert "values" in agent.scrum_knowledge
        assert "events" in agent.scrum_knowledge
        assert "artifacts" in agent.scrum_knowledge
        assert len(agent.scrum_knowledge["pillars"]) == 3
        assert len(agent.scrum_knowledge["values"]) == 5
    
    def test_continuous_discovery_knowledge_loaded(self):
        """Test that Continuous Discovery knowledge is loaded"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        assert "weekly_customer_interviews" in agent.continuous_discovery_knowledge
        assert "opportunity_solution_trees" in agent.continuous_discovery_knowledge
    
    def test_role_knowledge_loaded(self):
        """Test that role-specific knowledge is loaded"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        assert agent.role_knowledge == {"test": "knowledge"}
    
    def test_format_response(self):
        """Test format_response helper method"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        response = agent.format_response(
            response_text="Test response",
            recommendations=["Rec 1", "Rec 2"],
            questions=["Q1", "Q2"],
            requires_collaboration=True,
            collaborating_roles=["role1", "role2"]
        )
        
        assert isinstance(response, AgentResponse)
        assert response.response == "Test response"
        assert len(response.recommendations) == 2
        assert len(response.questions) == 2
        assert response.requires_collaboration is True
        assert len(response.collaborating_roles) == 2
    
    def test_format_response_minimal(self):
        """Test format_response with minimal parameters"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        response = agent.format_response(response_text="Minimal response")
        
        assert isinstance(response, AgentResponse)
        assert response.response == "Minimal response"
        assert response.recommendations == []
        assert response.questions == []
        assert response.requires_collaboration is False
    
    def test_process_query_implementation(self):
        """Test that process_query is implemented by subclass"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        response = agent.process_query("test query")
        
        assert isinstance(response, AgentResponse)
        assert "test query" in response.response
    
    def test_identify_collaboration_needs_default(self):
        """Test default identify_collaboration_needs returns empty list"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        needs = agent.identify_collaboration_needs("test query")
        assert isinstance(needs, list)
        # Default implementation returns empty list
        assert len(needs) == 0
    
    def test_get_cross_functional_awareness_default(self):
        """Test default get_cross_functional_awareness returns empty dict"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        awareness = agent.get_cross_functional_awareness()
        assert isinstance(awareness, dict)
        # Default implementation returns empty dict
        assert len(awareness) == 0
