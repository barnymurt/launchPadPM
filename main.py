"""
Main entry point for the Scrum Team AI Agents framework.
Provides CLI interface and orchestration.
"""

import sys
from typing import Optional
from agents.agent_registry import AgentRegistry
from agents.base_agent import AgentContext
from config.settings import load_settings, Settings

# Import available agents
try:
    from agents.product_owner_agent import ProductOwnerAgent
    PRODUCT_OWNER_AVAILABLE = True
except ImportError:
    PRODUCT_OWNER_AVAILABLE = False

try:
    from agents.scrum_master_agent import ScrumMasterAgent
    SCRUM_MASTER_AVAILABLE = True
except ImportError:
    SCRUM_MASTER_AVAILABLE = False

try:
    from agents.development_engineer_agent import DevelopmentEngineerAgent
    DEVELOPMENT_ENGINEER_AVAILABLE = True
except ImportError:
    DEVELOPMENT_ENGINEER_AVAILABLE = False

try:
    from agents.qa_engineer_agent import QAEngineerAgent
    QA_ENGINEER_AVAILABLE = True
except ImportError:
    QA_ENGINEER_AVAILABLE = False

try:
    from agents.business_analyst_agent import BusinessAnalystAgent
    BUSINESS_ANALYST_AVAILABLE = True
except ImportError:
    BUSINESS_ANALYST_AVAILABLE = False

try:
    from agents.data_metrics_analyst_agent import DataMetricsAnalystAgent
    DATA_METRICS_ANALYST_AVAILABLE = True
except ImportError:
    DATA_METRICS_ANALYST_AVAILABLE = False

try:
    from agents.ux_ui_designer_agent import UXUIDesignerAgent
    UX_UI_DESIGNER_AVAILABLE = True
except ImportError:
    UX_UI_DESIGNER_AVAILABLE = False


def initialize_framework(settings: Optional[Settings] = None) -> None:
    """
    Initialize the framework with settings and context.
    
    Args:
        settings: Settings object (loads from config.json if not provided)
    """
    if settings is None:
        settings = load_settings()
    
    # Create shared context
    context = AgentContext(
        product_name=settings.product_name,
        sprint_number=0,
        current_phase="planning",
        shared_knowledge={
            "scrum_framework": True,
            "continuous_discovery": settings.enable_continuous_discovery,
            "opportunity_solution_trees": settings.enable_opportunity_solution_trees
        }
    )
    
    AgentRegistry.set_context(context)
    
    # Register available agents
    register_available_agents()
    
    print(f"[OK] Framework initialized for product: {settings.product_name}")
    print(f"[OK] Collaboration enabled: {settings.enable_collaboration}")
    print(f"[OK] Continuous Discovery enabled: {settings.enable_continuous_discovery}")


def register_available_agents() -> None:
    """Register all available agents with the registry"""
    registered_count = 0
    
    if PRODUCT_OWNER_AVAILABLE:
        po_agent = ProductOwnerAgent()
        AgentRegistry.register_agent(po_agent)
        registered_count += 1
    
    if SCRUM_MASTER_AVAILABLE:
        sm_agent = ScrumMasterAgent()
        AgentRegistry.register_agent(sm_agent)
        registered_count += 1
    
    if DEVELOPMENT_ENGINEER_AVAILABLE:
        dev_agent = DevelopmentEngineerAgent()
        AgentRegistry.register_agent(dev_agent)
        registered_count += 1
    
    if QA_ENGINEER_AVAILABLE:
        qa_agent = QAEngineerAgent()
        AgentRegistry.register_agent(qa_agent)
        registered_count += 1
    
    if BUSINESS_ANALYST_AVAILABLE:
        ba_agent = BusinessAnalystAgent()
        AgentRegistry.register_agent(ba_agent)
        registered_count += 1
    
    if DATA_METRICS_ANALYST_AVAILABLE:
        data_agent = DataMetricsAnalystAgent()
        AgentRegistry.register_agent(data_agent)
        registered_count += 1
    
    if UX_UI_DESIGNER_AVAILABLE:
        ux_agent = UXUIDesignerAgent()
        AgentRegistry.register_agent(ux_agent)
        registered_count += 1
    
    if registered_count > 0:
        print(f"[OK] Registered {registered_count} agent(s)")


def list_agents() -> None:
    """List all registered agents"""
    agents = AgentRegistry.get_all_agents()
    if not agents:
        print("No agents registered yet.")
        print("\nTo add agents, import and register them:")
        print("  from agents.example_agent import ExampleAgent")
        print("  from agents.agent_registry import AgentRegistry")
        print("  AgentRegistry.register_agent(ExampleAgent())")
        return
    
    print(f"\nRegistered Agents ({len(agents)}):")
    print("-" * 50)
    for role, agent in agents.items():
        print(f"  • {agent.role} ({agent.name})")
        print(f"    Key: {role}")


def query_agent(role: str, query: str) -> None:
    """
    Query a specific agent.
    
    Args:
        role: Agent role name
        query: Question or request
    """
    agent = AgentRegistry.get_agent(role)
    if not agent:
        print(f"[ERROR] Agent '{role}' not found.")
        print(f"Available agents: {', '.join(AgentRegistry.list_roles())}")
        return
    
    print(f"\n[AGENT] Querying {agent.role}...")
    print(f"Query: {query}\n")
    print("-" * 50)
    
    try:
        response = agent.process_query(query)
        print(f"Response:\n{response.response}\n")
        
        if response.recommendations:
            print("Recommendations:")
            for i, rec in enumerate(response.recommendations, 1):
                print(f"  {i}. {rec}")
            print()
        
        if response.questions:
            print("Questions to consider:")
            for i, q in enumerate(response.questions, 1):
                print(f"  {i}. {q}")
            print()
        
        if response.requires_collaboration:
            print("[COLLABORATION] This requires collaboration with:")
            for role in response.collaborating_roles:
                print(f"  • {role}")
            print()
    
    except Exception as e:
        print(f"[ERROR] Error processing query: {e}")


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Scrum Team AI Agents Framework")
        print("=" * 50)
        print("\nUsage:")
        print("  python main.py init              - Initialize framework")
        print("  python main.py list              - List registered agents")
        print("  python main.py query <role> <q>   - Query an agent")
        print("\nExample:")
        print("  python main.py query product_owner 'Should we prioritize dark mode?'")
        return
    
    command = sys.argv[1]
    
    if command == "init":
        initialize_framework()
        print("\n[OK] Framework ready!")
        print("\nNext steps:")
        print("  1. Create agent implementations (see agents/example_agent.py)")
        print("  2. Register agents using AgentRegistry.register_agent()")
        print("  3. Start querying agents!")
    
    elif command == "list":
        initialize_framework()
        list_agents()
    
    elif command == "query":
        if len(sys.argv) < 4:
            print("Usage: python main.py query <role> <query>")
            return
        role = sys.argv[2]
        query = " ".join(sys.argv[3:])
        initialize_framework()
        query_agent(role, query)
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'init', 'list', or 'query'")


if __name__ == "__main__":
    main()
