"""
Demo: Scrum Master Agent in Practice
Demonstrates real-world scenarios and how the Scrum Master agent responds
"""

from agents.agent_registry import AgentRegistry
from agents.base_agent import AgentContext, AgentResponse
from agents.scrum_master_agent import ScrumMasterAgent
from config.settings import load_settings


def print_section(title: str, width: int = 70):
    """Print a formatted section header"""
    print("\n" + "=" * width)
    print(f" {title}")
    print("=" * width + "\n")


def print_response(scenario: str, query: str, response: AgentResponse):
    """Print a formatted scenario and response"""
    print(f"[SCENARIO] {scenario}")
    print(f"[QUERY] {query}\n")
    print("-" * 70)
    print(f"[SCRUM MASTER RESPONSE]\n")
    print(response.response)
    print()
    
    if response.recommendations:
        print("[RECOMMENDATIONS]")
        for i, rec in enumerate(response.recommendations[:5], 1):
            print(f"   {i}. {rec}")
        if len(response.recommendations) > 5:
            print(f"   ... and {len(response.recommendations) - 5} more")
        print()
    
    if response.questions:
        print("[QUESTIONS TO CONSIDER]")
        for i, q in enumerate(response.questions[:3], 1):
            print(f"   {i}. {q}")
        if len(response.questions) > 3:
            print(f"   ... and {len(response.questions) - 3} more")
        print()
    
    if response.requires_collaboration:
        print("[REQUIRES COLLABORATION WITH]")
        for role in response.collaborating_roles:
            print(f"   - {role}")
        print()
    
    print("=" * 70 + "\n")


def demo_scrum_master():
    """Run comprehensive demo of Scrum Master agent"""
    
    # Setup
    settings = load_settings()
    context = AgentContext(
        product_name="Demo Product",
        sprint_number=3,
        current_phase="development",
        shared_knowledge={
            "scrum_framework": True,
            "continuous_discovery": True,
            "opportunity_solution_trees": True
        }
    )
    
    sm_agent = ScrumMasterAgent(context=context)
    AgentRegistry.register_agent(sm_agent)
    AgentRegistry.set_context(context)
    
    print_section("SCRUM MASTER AGENT DEMO - Real-World Scenarios")
    
    # Scenario 1: Developer facing impediment
    print_section("Scenario 1: Developer Facing an Impediment")
    query1 = "I'm blocked on this task because I need access to the production database, but IT says it will take 2 weeks to get approval. What should I do?"
    response1 = sm_agent.process_query(query1)
    print_response(
        "Developer blocked by organizational process",
        query1,
        response1
    )
    
    # Scenario 2: Product Owner frustrated with team
    print_section("Scenario 2: Product Owner Frustration")
    query2 = "The Developers never finish what they commit to in Sprint Planning. How do I make them work faster?"
    response2 = sm_agent.process_query(query2)
    print_response(
        "Product Owner concerned about Sprint Goal completion",
        query2,
        response2
    )
    
    # Scenario 3: Sprint Planning guidance
    print_section("Scenario 3: Sprint Planning Facilitation")
    query3 = "How should I facilitate Sprint Planning? The team seems confused about what to do."
    response3 = sm_agent.process_query(query3)
    print_response(
        "Scrum Master needs guidance on Sprint Planning",
        query3,
        response3
    )
    
    # Scenario 4: Daily Scrum issues
    print_section("Scenario 4: Daily Scrum Problems")
    query4 = "The Daily Scrum is taking 45 minutes and turning into a status update. How do I fix this?"
    response4 = sm_agent.process_query(query4)
    print_response(
        "Daily Scrum not following Scrum principles",
        query4,
        response4
    )
    
    # Scenario 5: Team effectiveness concerns
    print_section("Scenario 5: Team Health Assessment")
    query5 = "I'm worried about the team. They seem stressed, Sprint Goals are being missed, and people aren't speaking up in Retrospectives. What should I do?"
    response5 = sm_agent.process_query(query5)
    print_response(
        "Scrum Master noticing team health issues",
        query5,
        response5
    )
    
    # Scenario 6: Organizational pressure
    print_section("Scenario 6: Organizational Pressure")
    query6 = "Management is asking why the team isn't delivering faster and wants more features. How should I respond?"
    response6 = sm_agent.process_query(query6)
    print_response(
        "Organizational pressure for faster delivery",
        query6,
        response6
    )
    
    # Scenario 7: Definition of Done issues
    print_section("Scenario 7: Definition of Done Problems")
    query7 = "Items are being marked as 'done' but they don't meet our Definition of Done. The team says they'll fix it later. What should I do?"
    response7 = sm_agent.process_query(query7)
    print_response(
        "Definition of Done not being followed",
        query7,
        response7
    )
    
    # Scenario 8: Retrospective effectiveness
    print_section("Scenario 8: Retrospective Improvement")
    query8 = "Our Retrospectives feel like complaint sessions. We identify problems but nothing changes. How can I make them more effective?"
    response8 = sm_agent.process_query(query8)
    print_response(
        "Retrospectives not leading to improvements",
        query8,
        response8
    )
    
    # Scenario 9: Coaching approach
    print_section("Scenario 9: Coaching Self-Management")
    query9 = "The team keeps asking me what to work on. Should I just tell them, or is there a better approach?"
    response9 = sm_agent.process_query(query9)
    print_response(
        "Team not self-managing",
        query9,
        response9
    )
    
    # Scenario 10: Velocity concerns
    print_section("Scenario 10: Velocity Questions")
    query10 = "Our velocity dropped from 30 to 20 story points. Management wants to know why and wants it back up. How should I handle this?"
    response10 = sm_agent.process_query(query10)
    print_response(
        "Velocity concerns from management",
        query10,
        response10
    )
    
    print_section("DEMO COMPLETE - Key Takeaways")
    print("""
The Scrum Master agent demonstrates:
✅ Servant leadership approach (coaching, not dictating)
✅ Impediment removal process
✅ Scrum event facilitation knowledge
✅ Team effectiveness focus
✅ Organizational change agent role
✅ Coaching through questions, not answers
✅ Grounding advice in Scrum principles
✅ Cross-functional collaboration awareness
    """)


if __name__ == "__main__":
    demo_scrum_master()
