"""
Simple Demo: Scrum Master Agent
Shows key scenarios in action
"""

import sys
import io
from agents.agent_registry import AgentRegistry
from agents.base_agent import AgentContext, AgentResponse
from agents.scrum_master_agent import ScrumMasterAgent
from config.settings import load_settings

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def demo_key_scenarios():
    """Run focused demo of key Scrum Master scenarios"""
    
    # Setup
    settings = load_settings()
    context = AgentContext(
        product_name="Demo Product",
        sprint_number=3,
        current_phase="development"
    )
    
    sm_agent = ScrumMasterAgent(context=context)
    AgentRegistry.register_agent(sm_agent)
    AgentRegistry.set_context(context)
    
    print("\n" + "=" * 80)
    print(" SCRUM MASTER AGENT DEMO - Key Scenarios")
    print("=" * 80 + "\n")
    
    # Scenario 1: Impediment
    print("\n[SCENARIO 1: Developer Blocked by Organizational Process]")
    print("-" * 80)
    query1 = "I'm blocked because I need database access but IT says 2 weeks for approval"
    print(f"Query: {query1}\n")
    response1 = sm_agent.process_query(query1)
    print("Scrum Master Response:")
    print(response1.response[:500] + "...\n")
    print(f"Collaboration needed: {response1.requires_collaboration}")
    print(f"Collaborating roles: {', '.join(response1.collaborating_roles) if response1.collaborating_roles else 'None'}")
    
    # Scenario 2: Product Owner frustration
    print("\n" + "=" * 80)
    print("\n[SCENARIO 2: Product Owner Frustrated with Team]")
    print("-" * 80)
    query2 = "The Developers never finish what they commit to. How do I make them work faster?"
    print(f"Query: {query2}\n")
    response2 = sm_agent.process_query(query2)
    print("Scrum Master Response:")
    print(response2.response[:600] + "...\n")
    print(f"Key recommendations: {len(response2.recommendations)}")
    print(f"Questions to consider: {len(response2.questions)}")
    
    # Scenario 3: Daily Scrum issues
    print("\n" + "=" * 80)
    print("\n[SCENARIO 3: Daily Scrum Problems]")
    print("-" * 80)
    query3 = "Daily Scrum is taking 45 minutes and becoming a status update"
    print(f"Query: {query3}\n")
    response3 = sm_agent.process_query(query3)
    print("Scrum Master Response:")
    print(response3.response[:500] + "...\n")
    
    # Scenario 4: Team health
    print("\n" + "=" * 80)
    print("\n[SCENARIO 4: Team Health Concerns]")
    print("-" * 80)
    query4 = "Team seems stressed, Sprint Goals missed, people not speaking up in Retrospectives"
    print(f"Query: {query4}\n")
    response4 = sm_agent.process_query(query4)
    print("Scrum Master Response:")
    print(response4.response[:600] + "...\n")
    
    # Scenario 5: Organizational pressure
    print("\n" + "=" * 80)
    print("\n[SCENARIO 5: Management Pressure]")
    print("-" * 80)
    query5 = "Management wants faster delivery and more features. How should I respond?"
    print(f"Query: {query5}\n")
    response5 = sm_agent.process_query(query5)
    print("Scrum Master Response:")
    print(response5.response[:500] + "...\n")
    
    print("\n" + "=" * 80)
    print(" DEMO COMPLETE")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("- Scrum Master demonstrates servant leadership (coaching, not dictating)")
    print("- Focuses on impediment removal and team effectiveness")
    print("- Grounds advice in Scrum principles")
    print("- Identifies when collaboration with other roles is needed")
    print("- Provides actionable recommendations and thought-provoking questions")
    print()


if __name__ == "__main__":
    try:
        demo_key_scenarios()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
