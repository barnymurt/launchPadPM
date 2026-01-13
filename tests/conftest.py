"""
Pytest configuration and shared fixtures
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.base_agent import AgentContext
from agents.agent_registry import AgentRegistry


@pytest.fixture
def agent_context():
    """Create a test AgentContext"""
    return AgentContext(
        product_name="Test Product",
        sprint_number=1,
        current_phase="development"
    )


@pytest.fixture
def clean_registry():
    """Clear agent registry before each test"""
    # Save original state
    original_agents = AgentRegistry._agents.copy()
    original_context = AgentRegistry._shared_context
    
    # Clear for test
    AgentRegistry._agents = {}
    AgentRegistry._shared_context = None
    
    yield
    
    # Restore original state
    AgentRegistry._agents = original_agents
    AgentRegistry._shared_context = original_context
