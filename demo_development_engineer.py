"""
Demo: Development Engineer Agent - Real Code Problems
Demonstrates the agent handling actual development scenarios
"""

import sys
import io
from agents.agent_registry import AgentRegistry
from agents.base_agent import AgentContext
from agents.development_engineer_agent import DevelopmentEngineerAgent
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
    
    print("Development Engineer Response:\n")
    print(response.response)
    
    if response.recommendations:
        print(f"\n[Provides {len(response.recommendations)} recommendations]")
        print("Key recommendations:")
        for i, rec in enumerate(response.recommendations[:4], 1):
            print(f"  {i}. {rec}")
    
    if response.questions:
        print(f"\n[Asks {len(response.questions)} questions]")
        print("Key questions:")
        for i, q in enumerate(response.questions[:3], 1):
            print(f"  {i}. {q}")
    
    if response.requires_collaboration:
        print(f"\n[Requires collaboration with: {', '.join(response.collaborating_roles)}]")


def main():
    """Run demo with real code problems"""
    
    # Setup
    context = AgentContext(
        product_name="Demo Product",
        sprint_number=3,
        current_phase="development"
    )
    
    dev_agent = DevelopmentEngineerAgent(context=context)
    AgentRegistry.register_agent(dev_agent)
    AgentRegistry.set_context(context)
    
    print("\n" + "="*80)
    print(" DEVELOPMENT ENGINEER AGENT - REAL CODE PROBLEMS DEMO")
    print("="*80)
    print("\nThis demo shows how the Development Engineer agent handles actual")
    print("development scenarios and code problems.\n")
    
    # Scenario 1: Real-time feature request
    print_scenario(
        1,
        "Product Owner: Real-Time Collaboration Feature",
        "Can we add real-time collaboration to the editor? Users want to edit documents together like Google Docs.",
        dev_agent
    )
    
    # Scenario 2: Bug found by QA
    print_scenario(
        2,
        "QA Engineer: Critical Bug Found",
        "I found a bug where the invoice total calculation is wrong when there are multiple tax rates. The system calculates 10% tax on the subtotal, then adds another 5% tax on the total, which is incorrect. Should I add it to the Sprint Backlog?",
        dev_agent
    )
    
    # Scenario 3: UX Design feasibility
    print_scenario(
        3,
        "UX Designer: Animation Implementation",
        "I designed an animated transition between the login screen and dashboard. It's a fade and slide effect that takes 300ms. Is this possible to implement? Will it work on mobile devices?",
        dev_agent
    )
    
    # Scenario 4: Technical debt concern
    print_scenario(
        4,
        "Developer: Technical Debt Decision",
        "I'm working on the payment processing feature and I noticed our current authentication system uses deprecated libraries that will stop receiving security updates next year. Should we refactor this now or add it to the backlog?",
        dev_agent
    )
    
    # Scenario 5: Architecture decision
    print_scenario(
        5,
        "Team: Database Architecture Choice",
        "We need to decide between using a relational database (PostgreSQL) or a NoSQL database (MongoDB) for storing user activity logs. The logs will be write-heavy and we need to query by user ID and date range. What's your recommendation?",
        dev_agent
    )
    
    # Scenario 6: Estimation request
    print_scenario(
        6,
        "Product Owner: Feature Estimation",
        "We want to add a search feature that allows users to search across all their documents with filters (by date, type, tags). Can you estimate how long this would take?",
        dev_agent
    )
    
    # Scenario 7: Definition of Done question
    print_scenario(
        7,
        "Developer: Definition of Done Clarification",
        "I finished implementing the user profile page. I wrote the code, it passes unit tests, and I deployed it to staging. But I haven't written integration tests yet. Is this 'done' according to our Definition of Done?",
        dev_agent
    )
    
    # Scenario 8: Blocker situation
    print_scenario(
        8,
        "Developer: Blocked on External API",
        "I'm blocked on integrating the payment gateway. Their API documentation is unclear about webhook authentication, and I've been waiting 2 days for their support team to respond. The Sprint Goal depends on this. What should I do?",
        dev_agent
    )
    
    print("\n" + "="*80)
    print(" DEMO COMPLETE")
    print("="*80)
    print("\nKey Observations:")
    print("1. Agent provides technical feasibility assessments with multiple options")
    print("2. Considers Definition of Done in all responses")
    print("3. Identifies when collaboration with other roles is needed")
    print("4. Offers honest estimates based on technical complexity")
    print("5. Balances ideal solutions with pragmatic delivery")
    print("6. Emphasizes quality and self-management")
    print("7. Surfaces blockers and technical debt transparently")
    print()


if __name__ == "__main__":
    main()
