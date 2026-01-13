"""
Unit tests for ProductOwnerAgent
Tests Product Owner specific functionality
"""
import pytest
from agents.product_owner_agent import ProductOwnerAgent
from agents.base_agent import AgentContext


class TestProductOwnerAgent:
    """Test suite for ProductOwnerAgent"""
    
    def test_product_owner_initialization(self, agent_context):
        """Test ProductOwnerAgent initialization"""
        po = ProductOwnerAgent(context=agent_context)
        assert po.role == "Product Owner"
        assert po.name == "PO"
        assert po.context == agent_context
    
    def test_product_owner_role_knowledge(self):
        """Test that Product Owner has role-specific knowledge"""
        po = ProductOwnerAgent()
        knowledge = po.get_role_specific_knowledge()
        
        assert "primary_accountability" in knowledge
        assert "key_responsibilities" in knowledge
        assert "continuous_discovery" in knowledge
        assert "opportunity_solution_trees" in knowledge
        assert "prioritization_model" in knowledge
    
    def test_prioritization_query(self):
        """Test Product Owner handles prioritization queries"""
        po = ProductOwnerAgent()
        response = po.process_query("How should I prioritize features?")
        
        assert response is not None
        assert hasattr(response, 'response')
        assert len(response.response) > 0
        assert "prioritization" in response.response.lower() or "priority" in response.response.lower()
    
    def test_calculate_priority_score(self):
        """Test priority score calculation"""
        po = ProductOwnerAgent()
        
        # Test high priority item
        score = po.calculate_priority_score(
            user_value=10,
            time_criticality=10,
            risk_reduction=8,
            effort=2
        )
        assert score > 0
        assert score == (10 + 10 + 8) / 2  # Should be 14.0
        
        # Test low priority item
        score2 = po.calculate_priority_score(
            user_value=2,
            time_criticality=1,
            risk_reduction=1,
            effort=5
        )
        assert score2 < score
        assert score2 == (2 + 1 + 1) / 5  # Should be 0.8
    
    def test_ost_query(self):
        """Test Product Owner handles Opportunity Solution Tree queries"""
        po = ProductOwnerAgent()
        response = po.process_query("How do I create an Opportunity Solution Tree?")
        
        assert response is not None
        assert len(response.response) > 0
    
    def test_customer_interview_query(self):
        """Test Product Owner handles customer interview queries"""
        po = ProductOwnerAgent()
        response = po.process_query("How should I conduct customer interviews?")
        
        assert response is not None
        assert len(response.response) > 0
    
    def test_collaboration_identification(self):
        """Test Product Owner identifies collaboration needs"""
        po = ProductOwnerAgent()
        
        # Technical query should identify need for developers
        needs = po.identify_collaboration_needs("Is this feature technically feasible?")
        assert "development_engineer" in needs
        
        # Data query should identify need for data analyst
        needs2 = po.identify_collaboration_needs("What metrics should we track?")
        assert "data_metrics_analyst" in needs2 or len(needs2) > 0
    
    def test_cross_functional_awareness(self):
        """Test Product Owner has cross-functional awareness"""
        po = ProductOwnerAgent()
        awareness = po.get_cross_functional_awareness()
        
        assert "receives_from" in awareness
        assert "provides_to" in awareness
        assert "development_engineer" in awareness["receives_from"] or "development_engineer" in awareness["provides_to"]
