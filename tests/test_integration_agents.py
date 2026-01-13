"""
Integration tests for agent interactions
Tests cross-functional collaboration and agent coordination
"""
import pytest
from agents.product_owner_agent import ProductOwnerAgent
from agents.development_engineer_agent import DevelopmentEngineerAgent
from agents.qa_engineer_agent import QAEngineerAgent
from agents.agent_registry import AgentRegistry


class TestAgentIntegration:
    """Integration tests for agent interactions"""
    
    def test_agent_registration_and_retrieval(self):
        """Test that agents can be registered and retrieved"""
        po = ProductOwnerAgent()
        dev = DevelopmentEngineerAgent()
        qa = QAEngineerAgent()
        
        AgentRegistry.register_agent(po)
        AgentRegistry.register_agent(dev)
        AgentRegistry.register_agent(qa)
        
        retrieved_po = AgentRegistry.get_agent("Product Owner")
        retrieved_dev = AgentRegistry.get_agent("Development Engineer")
        retrieved_qa = AgentRegistry.get_agent("QA Engineer")
        
        assert retrieved_po is not None
        assert retrieved_dev is not None
        assert retrieved_qa is not None
        assert retrieved_po.role == "Product Owner"
        assert retrieved_dev.role == "Development Engineer"
        assert retrieved_qa.role == "QA Engineer"
    
    def test_collaboration_identification(self):
        """Test that agents identify collaboration needs"""
        po = ProductOwnerAgent()
        dev = DevelopmentEngineerAgent()
        qa = QAEngineerAgent()
        
        # Product Owner should identify need for developers
        po_needs = po.identify_collaboration_needs("Should we build this feature?")
        assert len(po_needs) > 0
        
        # Developer should identify need for QA
        dev_needs = dev.identify_collaboration_needs("How should we test this code?")
        assert "qa_engineer" in dev_needs or len(dev_needs) > 0
    
    def test_cross_functional_awareness(self):
        """Test cross-functional awareness between agents"""
        po = ProductOwnerAgent()
        dev = DevelopmentEngineerAgent()
        qa = QAEngineerAgent()
        
        po_awareness = po.get_cross_functional_awareness()
        dev_awareness = dev.get_cross_functional_awareness()
        qa_awareness = qa.get_cross_functional_awareness()
        
        # All should have awareness structures
        assert "receives_from" in po_awareness
        assert "provides_to" in po_awareness
        assert "receives_from" in dev_awareness
        assert "provides_to" in dev_awareness
        assert "receives_from" in qa_awareness
        assert "provides_to" in qa_awareness
    
    def test_agent_query_processing(self):
        """Test that agents can process queries and return responses"""
        po = ProductOwnerAgent()
        dev = DevelopmentEngineerAgent()
        qa = QAEngineerAgent()
        
        po_response = po.process_query("How should I prioritize features?")
        dev_response = dev.process_query("Is this feature technically feasible?")
        qa_response = qa.process_query("What testing approach should we use?")
        
        assert po_response is not None
        assert dev_response is not None
        assert qa_response is not None
        assert hasattr(po_response, 'response')
        assert hasattr(dev_response, 'response')
        assert hasattr(qa_response, 'response')
        assert len(po_response.response) > 0
        assert len(dev_response.response) > 0
        assert len(qa_response.response) > 0
    
    def test_agent_response_structure(self):
        """Test that agent responses have expected structure"""
        po = ProductOwnerAgent()
        response = po.process_query("Test query")
        
        assert hasattr(response, 'response')
        assert hasattr(response, 'recommendations')
        assert hasattr(response, 'questions')
        assert hasattr(response, 'requires_collaboration')
        assert isinstance(response.recommendations, list)
        assert isinstance(response.questions, list)
        assert isinstance(response.requires_collaboration, bool)
