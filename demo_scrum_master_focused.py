"""
Focused Demo: Scrum Master Agent
Demonstrates correct routing and responses
"""

import sys
import io
from agents.agent_registry import AgentRegistry
from agents.base_agent import AgentContext
from agents.scrum_master_agent import ScrumMasterAgent
from config.settings import load_settings

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def print_scenario(num, title, query, agent):
    """Print a scenario and response"""
    print(f"\n{'='*80}")
    print(f"SCENARIO {num}: {title}")
    print('='*80)
    print(f"\nQuery: {query}\n")
    print("-"*80)
    
    response = agent.process_query(query)
    
    print("Scrum Master Response:\n")
    # Print full response (it's already well-formatted)
    print(response.response)
    
    if response.recommendations:
        print(f"\n[Provides {len(response.recommendations)} recommendations]")
        print("Sample recommendations:")
        for i, rec in enumerate(response.recommendations[:3], 1):
            print(f"  {i}. {rec}")
    
    if response.questions:
        print(f"\n[Asks {len(response.questions)} questions to consider]")
        print("Sample questions:")
        for i, q in enumerate(response.questions[:2], 1):
            print(f"  {i}. {q}")
    
    if response.requires_collaboration:
        print(f"\n[Requires collaboration with: {', '.join(response.collaborating_roles)}]")


def main():
    """Run focused demo"""
    
    # Setup
    context = AgentContext(
        product_name="Demo Product",
        sprint_number=3,
        current_phase="development"
    )
    
    sm_agent = ScrumMasterAgent(context=context)
    AgentRegistry.register_agent(sm_agent)
    AgentRegistry.set_context(context)
    
    print("\n" + "="*80)
    print(" SCRUM MASTER AGENT - PRACTICAL DEMONSTRATION")
    print("="*80)
    print("\nThis demo shows how the Scrum Master agent responds to real-world scenarios.")
    print("The agent demonstrates servant leadership, coaching, and impediment removal.\n")
    
    # Scenario 1: Impediment (should route correctly)
    print_scenario(
        1,
        "Developer Blocked by Organizational Process",
        "I'm blocked on my task because I need access to the production database, but IT says it will take 2 weeks to get approval. What should I do?",
        sm_agent
    )
    
    # Scenario 2: Team effectiveness (explicit team keyword)
    print_scenario(
        2,
        "Product Owner Concerned About Team Performance",
        "The team never finishes what they commit to in Sprint Planning. How do I make them work faster?",
        sm_agent
    )
    
    # Scenario 3: Daily Scrum (should route correctly)
    print_scenario(
        3,
        "Daily Scrum Anti-Pattern",
        "The Daily Scrum is taking 45 minutes and turning into a status update to me. How do I fix this?",
        sm_agent
    )
    
    # Scenario 4: Retrospective (should route correctly)
    print_scenario(
        4,
        "Retrospective Not Effective",
        "Our Sprint Retrospective feels like a complaint session. We identify problems but nothing changes. How can I make it more effective?",
        sm_agent
    )
    
    # Scenario 5: Definition of Done (should route correctly)
    print_scenario(
        5,
        "Definition of Done Issues",
        "Items are being marked as done but they don't meet our Definition of Done. The team says they'll fix it later. What should I do?",
        sm_agent
    )
    
    # Scenario 6: Organizational (should route correctly)
    print_scenario(
        6,
        "Organizational Pressure",
        "Management is asking why the team isn't delivering faster and wants more features. How should I respond as Scrum Master?",
        sm_agent
    )
    
    print("\n" + "="*80)
    print(" DEMO COMPLETE")
    print("="*80)
    print("\nKey Observations:")
    print("1. Agent demonstrates servant leadership - coaches rather than dictates")
    print("2. Provides Scrum framework guidance grounded in principles")
    print("3. Identifies impediments and offers removal process")
    print("4. Suggests collaboration with other roles when appropriate")
    print("5. Offers actionable recommendations and thought-provoking questions")
    print("6. Focuses on team effectiveness and continuous improvement")
    print()


if __name__ == "__main__":
    main()
