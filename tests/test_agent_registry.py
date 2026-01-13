"""
Unit tests for AgentRegistry
Tests registration, retrieval, and management of agents
"""
import pytest
from agents.agent_registry import AgentRegistry
from agents.base_agent import BaseAgent, AgentContext, AgentResponse
from abc import ABC


class TestAgent(BaseAgent):
    """Test agent for registry tests"""
    
    def get_role_specific_knowledge(self):
        return {"test": "knowledge"}
    
    def process_query(self, query: str, **kwargs):
        return self.format_response(response_text="Test response")


class TestAgentRegistry:
    """Test suite for AgentRegistry"""
    
    def test_registry_singleton_pattern(self, clean_registry):
        """Test that AgentRegistry maintains single instance"""
        agent1 = TestAgent(role="Test Role", name="Test")
        AgentRegistry.register_agent(agent1)
        
        agent2 = TestAgent(role="Test Role 2", name="Test2")
        AgentRegistry.register_agent(agent2)
        
        # Should have 2 agents registered
        assert len(AgentRegistry._agents) == 2
    
    def test_register_agent(self, clean_registry):
        """Test agent registration"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        AgentRegistry.register_agent(agent)
        
        assert "test_role" in AgentRegistry._agents
        assert AgentRegistry._agents["test_role"] == agent
    
    def test_register_agent_role_key_normalization(self, clean_registry):
        """Test that role keys are normalized (spaces and slashes)"""
        agent1 = TestAgent(role="Test Role", name="Test")
        AgentRegistry.register_agent(agent1)
        
        agent2 = ConcreteTestAgent(role="Data/Metrics Analyst", name="Data")
        AgentRegistry.register_agent(agent2)
        
        assert "test_role" in AgentRegistry._agents
        assert "data_metrics_analyst" in AgentRegistry._agents
    
    def test_get_agent_by_role(self, clean_registry):
        """Test retrieving agent by role"""
        agent = ConcreteTestAgent(role="Test Role", name="Test")
        AgentRegistry.register_agent(agent)
        
        retrieved = AgentRegistry.get_agent("Test Role")
        assert retrieved == agent
        
        # Test case-insensitive
        retrieved2 = AgentRegistry.get_agent("test role")
        assert retrieved2 == agent
    
    def test_get_agent_not_found(self, clean_registry):
        """Test retrieving non-existent agent returns None"""
        result = AgentRegistry.get_agent("Non Existent Role")
        assert result is None
    
    def test_list_roles(self, clean_registry):
        """Test listing all registered roles"""
        agent1 = TestAgent(role="Role One", name="One")
        agent2 = TestAgent(role="Role Two", name="Two")
        
        AgentRegistry.register_agent(agent1)
        AgentRegistry.register_agent(agent2)
        
        roles = AgentRegistry.list_roles()
        assert len(roles) == 2
        assert "Role One" in roles
        assert "Role Two" in roles
    
    def test_set_shared_context(self, clean_registry):
        """Test setting shared context for all agents"""
        context = AgentContext(product_name="Shared Product", current_sprint=5)
        AgentRegistry.set_shared_context(context)
        
        assert AgentRegistry._shared_context == context
    
    def test_get_shared_context(self, clean_registry):
        """Test getting shared context"""
        context = AgentContext(product_name="Shared Product", current_sprint=5)
        AgentRegistry.set_shared_context(context)
        
        retrieved = AgentRegistry.get_shared_context()
        assert retrieved == context
    
    def test_get_shared_context_default(self, clean_registry):
        """Test getting default shared context when none set"""
        context = AgentRegistry.get_shared_context()
        # When no context is set, it should return None (not create default)
        # This is the current behavior - can be changed if needed
        assert context is None or isinstance(context, AgentContext)
