"""
Test script for Product Owner Agent
Demonstrates the agent's capabilities
"""

from agents.agent_registry import AgentRegistry
from agents.base_agent import AgentContext
from agents.product_owner_agent import ProductOwnerAgent
from config.settings import load_settings


def test_product_owner_agent():
    """Test the Product Owner agent with various queries"""
    
    # Load settings and create context
    settings = load_settings()
    context = AgentContext(
        product_name=settings.product_name,
        sprint_number=1,
        current_phase="planning",
        shared_knowledge={
            "scrum_framework": True,
            "continuous_discovery": True,
            "opportunity_solution_trees": True
        }
    )
    
    # Register agent
    po_agent = ProductOwnerAgent(context=context)
    AgentRegistry.register_agent(po_agent)
    AgentRegistry.set_context(context)
    
    print("=" * 70)
    print("Product Owner Agent Test")
    print("=" * 70)
    print()
    
    # Test queries
    test_queries = [
        "Should we add a dark mode feature?",
        "How should I prioritize these five features?",
        "Tell me about Opportunity Solution Trees",
        "What's the best way to conduct customer interviews?",
        "How do I manage the Product Backlog?",
        "What is the Product Goal?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 70}")
        print(f"Test {i}: {query}")
        print('=' * 70)
        print()
        
        try:
            response = po_agent.process_query(query)
            
            print(f"Response:\n{response.response}\n")
            
            if response.recommendations:
                print("Recommendations:")
                for j, rec in enumerate(response.recommendations[:5], 1):  # Show first 5
                    print(f"  {j}. {rec}")
                if len(response.recommendations) > 5:
                    print(f"  ... and {len(response.recommendations) - 5} more")
                print()
            
            if response.questions:
                print("Questions to consider:")
                for j, q in enumerate(response.questions[:3], 1):  # Show first 3
                    print(f"  {j}. {q}")
                if len(response.questions) > 3:
                    print(f"  ... and {len(response.questions) - 3} more")
                print()
            
            if response.requires_collaboration:
                print("⚠️  Requires collaboration with:")
                for role in response.collaborating_roles:
                    print(f"  • {role}")
                print()
        
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Test prioritization calculation
    print("\n" + "=" * 70)
    print("Prioritization Score Calculation Test")
    print("=" * 70)
    print()
    
    test_cases = [
        {"name": "High Value, Low Effort", "user_value": 9, "time_criticality": 8, "risk_reduction": 7, "effort": 2},
        {"name": "Medium Value, Medium Effort", "user_value": 6, "time_criticality": 5, "risk_reduction": 4, "effort": 5},
        {"name": "Low Value, High Effort", "user_value": 3, "time_criticality": 2, "risk_reduction": 2, "effort": 8},
    ]
    
    for case in test_cases:
        score = po_agent.calculate_priority_score(
            case["user_value"],
            case["time_criticality"],
            case["risk_reduction"],
            case["effort"]
        )
        print(f"{case['name']}:")
        print(f"  User Value: {case['user_value']}, Time Criticality: {case['time_criticality']}, "
              f"Risk Reduction: {case['risk_reduction']}, Effort: {case['effort']}")
        print(f"  Priority Score: {score:.2f}")
        print()
    
    print("=" * 70)
    print("Test Complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_product_owner_agent()
