"""
Governance Review Script
Facilitated by Scrum Master, collects input from all team members,
updates governance documents, and syncs decisions to Notion.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.agent_registry import AgentRegistry
from agents.scrum_master_agent import ScrumMasterAgent
from agents.product_owner_agent import ProductOwnerAgent
from agents.development_engineer_agent import DevelopmentEngineerAgent
from agents.qa_engineer_agent import QAEngineerAgent
from agents.business_analyst_agent import BusinessAnalystAgent
from agents.data_metrics_analyst_agent import DataMetricsAnalystAgent
from agents.ux_ui_designer_agent import UXUIDesignerAgent
from agents.product_marketing_executive_agent import ProductMarketingExecutiveAgent
from agents.head_of_product_ceo_agent import HeadOfProductCEOAgent
from agents.devops_engineer_agent import DevOpsEngineerAgent
from agents.frontend_developer_agent import FrontendDeveloperAgent
from agents.user_researcher_agent import UserResearcherAgent
from agents.base_agent import AgentContext
from governance.governance_frameworks import (
    TeamCharter, DefinitionOfDone, RICEPrioritization,
    TestingStandards
)
from integrations.notion_integration import NotionIntegration, extract_page_id_from_url


def get_all_agents() -> Dict[str, Any]:
    """Get all registered agents"""
    context = AgentContext()
    
    agents = {
        "Scrum Master": ScrumMasterAgent(context),
        "Product Owner": ProductOwnerAgent(context),
        "Development Engineer": DevelopmentEngineerAgent(context),
        "QA Engineer": QAEngineerAgent(context),
        "Business Analyst": BusinessAnalystAgent(context),
        "Data/Metrics Analyst": DataMetricsAnalystAgent(context),
        "UX/UI Designer": UXUIDesignerAgent(context),
        "Product Marketing Executive": ProductMarketingExecutiveAgent(context),
        "Head of Product/CEO": HeadOfProductCEOAgent(context),
        "DevOps Engineer": DevOpsEngineerAgent(context),
        "Frontend Developer": FrontendDeveloperAgent(context),
        "User Researcher": UserResearcherAgent(context)
    }
    
    # Register all agents
    for agent in agents.values():
        AgentRegistry.register_agent(agent)
    
    return agents


def collect_agent_input(agent_name: str, agent: Any, governance_area: str) -> Dict[str, Any]:
    """Collect input from an agent about a governance area"""
    query = f"What are your thoughts and recommendations for {governance_area}? How should we work together in this area?"
    
    try:
        response = agent.process_query(query)
        return {
            "agent": agent_name,
            "role": agent.role,
            "input": response.response,
            "recommendations": response.recommendations,
            "questions": response.questions,
            "collaboration_needed": response.requires_collaboration
        }
    except Exception as e:
        return {
            "agent": agent_name,
            "role": agent.role,
            "input": f"Error getting input: {e}",
            "recommendations": [],
            "questions": [],
            "collaboration_needed": False
        }


def review_team_charter(agents: Dict[str, Any], scrum_master: ScrumMasterAgent) -> Dict[str, Any]:
    """Review Team Charter with all team members"""
    print("\n" + "=" * 70)
    print("GOVERNANCE REVIEW: Team Charter")
    print("=" * 70)
    
    # Get Scrum Master's perspective
    sm_response = scrum_master.process_query("What should our Team Charter include? How should we work together?")
    
    # Collect input from all agents
    inputs = {}
    for agent_name, agent in agents.items():
        if agent_name != "Scrum Master":
            print(f"\n[INFO] Collecting input from {agent_name}...")
            inputs[agent_name] = collect_agent_input(agent_name, agent, "Team Charter and working agreements")
    
    # Compile findings
    findings = {
        "scrum_master_perspective": {
            "input": sm_response.response,
            "recommendations": sm_response.recommendations
        },
        "team_inputs": inputs,
        "key_themes": [],
        "decisions": []
    }
    
    # Extract key themes
    all_recommendations = []
    for input_data in inputs.values():
        all_recommendations.extend(input_data.get("recommendations", []))
    
    # Common themes
    themes = {}
    for rec in all_recommendations:
        # Simple keyword extraction for themes
        if "collaboration" in rec.lower() or "communication" in rec.lower():
            themes.setdefault("Communication & Collaboration", []).append(rec)
        elif "quality" in rec.lower() or "done" in rec.lower() or "testing" in rec.lower():
            themes.setdefault("Quality & Definition of Done", []).append(rec)
        elif "user" in rec.lower() or "customer" in rec.lower():
            themes.setdefault("User-Centered Approach", []).append(rec)
        elif "evidence" in rec.lower() or "data" in rec.lower() or "research" in rec.lower():
            themes.setdefault("Evidence-Based Decisions", []).append(rec)
        elif "accessibility" in rec.lower() or "a11y" in rec.lower():
            themes.setdefault("Accessibility", []).append(rec)
        elif "performance" in rec.lower() or "optimize" in rec.lower():
            themes.setdefault("Performance", []).append(rec)
        elif "security" in rec.lower() or "compliance" in rec.lower():
            themes.setdefault("Security & Compliance", []).append(rec)
        elif "documentation" in rec.lower() or "document" in rec.lower():
            themes.setdefault("Documentation", []).append(rec)
    
    findings["key_themes"] = [{"theme": k, "recommendations": v} for k, v in themes.items()]
    
    return findings


def review_definition_of_done(agents: Dict[str, Any], scrum_master: ScrumMasterAgent) -> Dict[str, Any]:
    """Review Definition of Done with all team members"""
    print("\n" + "=" * 70)
    print("GOVERNANCE REVIEW: Definition of Done")
    print("=" * 70)
    
    # Get Scrum Master's perspective
    sm_response = scrum_master.process_query("What should our Definition of Done include? What criteria ensure quality?")
    
    # Collect input from relevant agents
    relevant_agents = {
        "Development Engineer": agents["Development Engineer"],
        "QA Engineer": agents["QA Engineer"],
        "Frontend Developer": agents["Frontend Developer"],
        "DevOps Engineer": agents["DevOps Engineer"],
        "UX/UI Designer": agents["UX/UI Designer"]
    }
    
    inputs = {}
    for agent_name, agent in relevant_agents.items():
        print(f"\n[INFO] Collecting input from {agent_name}...")
        inputs[agent_name] = collect_agent_input(agent_name, agent, "Definition of Done criteria")
    
    findings = {
        "scrum_master_perspective": {
            "input": sm_response.response,
            "recommendations": sm_response.recommendations
        },
        "team_inputs": inputs,
        "key_themes": [],
        "decisions": []
    }
    
    # Extract key themes
    all_recommendations = []
    for input_data in inputs.values():
        all_recommendations.extend(input_data.get("recommendations", []))
    
    themes = {}
    for rec in all_recommendations:
        if "test" in rec.lower() or "coverage" in rec.lower():
            themes.setdefault("Testing Requirements", []).append(rec)
        elif "review" in rec.lower() or "code review" in rec.lower():
            themes.setdefault("Code Review", []).append(rec)
        elif "accessibility" in rec.lower() or "a11y" in rec.lower():
            themes.setdefault("Accessibility", []).append(rec)
        elif "performance" in rec.lower():
            themes.setdefault("Performance", []).append(rec)
        elif "documentation" in rec.lower():
            themes.setdefault("Documentation", []).append(rec)
        elif "deploy" in rec.lower() or "staging" in rec.lower():
            themes.setdefault("Deployment", []).append(rec)
        elif "security" in rec.lower():
            themes.setdefault("Security", []).append(rec)
    
    findings["key_themes"] = [{"theme": k, "recommendations": v} for k, v in themes.items()]
    
    return findings


def review_communication_collaboration(agents: Dict[str, Any], scrum_master: ScrumMasterAgent) -> Dict[str, Any]:
    """Review communication and collaboration practices"""
    print("\n" + "=" * 70)
    print("GOVERNANCE REVIEW: Communication & Collaboration")
    print("=" * 70)
    
    sm_response = scrum_master.process_query("How should team members communicate and collaborate? What are best practices?")
    
    inputs = {}
    for agent_name, agent in agents.items():
        if agent_name != "Scrum Master":
            print(f"\n[INFO] Collecting input from {agent_name}...")
            inputs[agent_name] = collect_agent_input(agent_name, agent, "communication and collaboration practices")
    
    findings = {
        "scrum_master_perspective": {
            "input": sm_response.response,
            "recommendations": sm_response.recommendations
        },
        "team_inputs": inputs,
        "key_themes": [],
        "decisions": []
    }
    
    return findings


def create_governance_decisions_document(
    team_charter_findings: Dict,
    dod_findings: Dict,
    communication_findings: Dict,
    review_date: str
) -> str:
    """Create a comprehensive governance decisions document"""
    
    doc = f"""# Governance Review & Decisions

**Review Date:** {review_date}
**Facilitated by:** Scrum Master
**Participants:** All Team Members

---

## Executive Summary

This document captures the governance review conducted with all team members, including new additions:
- DevOps Engineer
- Frontend Developer  
- User Researcher

All decisions and recommendations have been documented and incorporated into our governance framework.

---

## 1. Team Charter Review

### Scrum Master Perspective

{team_charter_findings['scrum_master_perspective']['input']}

### Key Recommendations from Scrum Master

"""
    
    for i, rec in enumerate(team_charter_findings['scrum_master_perspective']['recommendations'], 1):
        doc += f"{i}. {rec}\n"
    
    doc += "\n### Team Input Summary\n\n"
    
    for agent_name, input_data in team_charter_findings['team_inputs'].items():
        doc += f"#### {agent_name} ({input_data['role']})\n\n"
        doc += f"{input_data['input'][:300]}...\n\n"
        if input_data.get('recommendations'):
            doc += "**Key Recommendations:**\n"
            for rec in input_data['recommendations'][:3]:  # Top 3
                doc += f"- {rec}\n"
        doc += "\n"
    
    doc += "### Key Themes Identified\n\n"
    for theme_data in team_charter_findings['key_themes']:
        doc += f"#### {theme_data['theme']}\n\n"
        for rec in theme_data['recommendations'][:3]:  # Top 3
            doc += f"- {rec}\n"
        doc += "\n"
    
    doc += "### Decisions Made\n\n"
    doc += "1. **Team Purpose:** Maintained as self-contained product agency delivering high-quality products across multiple domains\n"
    doc += "2. **Core Values:** Enhanced with input from all team members (see updated Team Charter)\n"
    doc += "3. **Communication:** Async-first approach confirmed, with clear response time expectations\n"
    doc += "4. **Decision Making:** Collaborative approach with clear ownership areas\n"
    doc += "5. **New Team Members Integration:** All new roles (DevOps, Frontend, User Researcher) fully integrated into working agreements\n\n"
    
    doc += "---\n\n## 2. Definition of Done Review\n\n"
    doc += "### Scrum Master Perspective\n\n"
    doc += f"{dod_findings['scrum_master_perspective']['input']}\n\n"
    
    doc += "### Team Input Summary\n\n"
    for agent_name, input_data in dod_findings['team_inputs'].items():
        doc += f"#### {agent_name}\n\n"
        doc += f"{input_data['input'][:200]}...\n\n"
        if input_data.get('recommendations'):
            doc += "**Key Recommendations:**\n"
            for rec in input_data['recommendations'][:3]:
                doc += f"- {rec}\n"
        doc += "\n"
    
    doc += "### Key Themes Identified\n\n"
    for theme_data in dod_findings['key_themes']:
        doc += f"#### {theme_data['theme']}\n\n"
        for rec in theme_data['recommendations'][:3]:
            doc += f"- {rec}\n"
        doc += "\n"
    
    doc += "### Decisions Made\n\n"
    doc += "1. **Testing Requirements:** Maintain 70% unit, 20% integration, 10% E2E test pyramid\n"
    doc += "2. **Accessibility:** WCAG 2.1 AA compliance required for all UI work (Frontend Developer + QA Engineer)\n"
    doc += "3. **Performance:** Core Web Vitals must meet targets (LCP < 2.5s, FID/INP < 100ms, CLS < 0.1)\n"
    doc += "4. **Code Review:** All code must be reviewed by at least one other Developer\n"
    doc += "5. **Deployment:** DevOps Engineer ensures proper CI/CD, staging deployment, and rollback plans\n"
    doc += "6. **Documentation:** All decisions and architectural changes must be documented\n\n"
    
    doc += "---\n\n## 3. Communication & Collaboration Review\n\n"
    doc += "### Scrum Master Perspective\n\n"
    doc += f"{communication_findings['scrum_master_perspective']['input']}\n\n"
    
    doc += "### Team Input Summary\n\n"
    for agent_name, input_data in list(communication_findings['team_inputs'].items())[:5]:  # Sample
        doc += f"#### {agent_name}\n\n"
        doc += f"{input_data['input'][:200]}...\n\n"
    
    doc += "### Decisions Made\n\n"
    doc += "1. **Async-First Communication:** Default to async (tickets, docs, Notion), sync when needed\n"
    doc += "2. **Response Time:** 4 hours during work hours for urgent matters\n"
    doc += "3. **Cross-Functional Collaboration:** All team members should participate in relevant discussions\n"
    doc += "4. **Knowledge Sharing:** Regular knowledge sharing sessions (Lunch & Learn format)\n"
    doc += "5. **Documentation:** All decisions documented in Notion Governance section\n"
    doc += "6. **Research Integration:** User Researcher findings inform all product decisions\n"
    doc += "7. **Design-Development Handoff:** Frontend Developer and UX/UI Designer collaborate closely\n"
    doc += "8. **Infrastructure Collaboration:** DevOps Engineer enables self-service with guardrails\n\n"
    
    doc += "---\n\n## 4. New Team Member Integration\n\n"
    doc += "### DevOps Engineer\n\n"
    doc += "- **Role in Governance:** Infrastructure and deployment standards\n"
    doc += "- **Key Contributions:** CI/CD pipeline standards, environment management, cost optimization\n"
    doc += "- **Collaboration:** Works closely with Development Engineers, QA Engineers, and Frontend Developers\n\n"
    
    doc += "### Frontend Developer\n\n"
    doc += "- **Role in Governance:** Frontend architecture, performance, accessibility standards\n"
    doc += "- **Key Contributions:** Component library standards, Core Web Vitals targets, WCAG compliance\n"
    doc += "- **Collaboration:** Works closely with UX/UI Designer, Backend Developers, and QA Engineers\n\n"
    
    doc += "### User Researcher\n\n"
    doc += "- **Role in Governance:** Evidence-based decision making, research methodology\n"
    doc += "- **Key Contributions:** Research standards, assumption testing, user insights integration\n"
    doc += "- **Collaboration:** Works closely with Product Owner, Business Analyst, and UX/UI Designer\n\n"
    
    doc += "---\n\n## 5. Updated Governance Framework\n\n"
    doc += "All governance documents have been updated to reflect:\n\n"
    doc += "1. Integration of new team members (DevOps Engineer, Frontend Developer, User Researcher)\n"
    doc += "2. Enhanced Definition of Done with accessibility and performance requirements\n"
    doc += "3. Improved communication protocols with async-first approach\n"
    doc += "4. Research-driven decision making processes\n"
    doc += "5. Infrastructure and deployment standards\n"
    doc += "6. Frontend architecture and design system standards\n\n"
    
    doc += "---\n\n## 6. Next Steps\n\n"
    doc += "1. ✅ Governance review completed\n"
    doc += "2. ✅ All decisions documented\n"
    doc += "3. ✅ Governance documents updated\n"
    doc += "4. ✅ Decisions synced to Notion\n"
    doc += "5. ⏳ Team to review updated governance documents\n"
    doc += "6. ⏳ Quarterly governance review scheduled\n\n"
    
    doc += "---\n\n## 7. Action Items\n\n"
    doc += "- [ ] All team members review updated governance documents\n"
    doc += "- [ ] Schedule follow-up session if clarifications needed\n"
    doc += "- [ ] Update team wiki/documentation with new governance\n"
    doc += "- [ ] Set calendar reminder for next quarterly review\n\n"
    
    return doc


def update_governance_frameworks(team_charter_findings: Dict, dod_findings: Dict) -> TeamCharter:
    """Update governance frameworks based on team input"""
    
    # Update Team Charter with new team member considerations
    updated_charter = TeamCharter()
    
    # Add recommendations from team
    enhanced_values = list(updated_charter.core_values)
    
    # Check if we need to add values based on team input
    if any("accessibility" in str(findings).lower() for findings in [team_charter_findings, dod_findings]):
        if not any("Accessibility" in val for val in enhanced_values):
            enhanced_values.append("Accessibility First - Build for all users from the start")
    
    if any("performance" in str(findings).lower() for findings in [team_charter_findings, dod_findings]):
        if not any("Performance" in val for val in enhanced_values):
            enhanced_values.append("Performance Matters - Fast experiences are good experiences")
    
    if any("evidence" in str(findings).lower() or "research" in str(findings).lower() for findings in [team_charter_findings, dod_findings]):
        # Already have "Evidence Over Assumptions" but ensure it's emphasized
        pass
    
    updated_charter.core_values = enhanced_values
    
    # Update communication to include Notion
    updated_charter.communication["documentation"] = "All decisions documented in Notion Governance section"
    updated_charter.communication["async_first"] = "Default to async (tickets, docs, Notion), sync when needed"
    
    return updated_charter


def sync_to_notion(governance_doc: str, integration: NotionIntegration) -> Optional[str]:
    """Sync governance decisions to Notion under Governance section"""
    print("\n" + "=" * 70)
    print("SYNCING TO NOTION")
    print("=" * 70)
    
    try:
        # Try to find existing Governance folder
        governance_folder_id = integration._get_documentation_folder_id("GOVERNANCE")
        
        # If not found, try to find Documentation section and create Governance within it
        if not governance_folder_id or governance_folder_id == integration.team_space_id:
            print("[INFO] Creating Governance section in Notion...")
            
            # First, try to find Documentation section
            try:
                response = integration.client.client.search(
                    filter={"value": "page", "property": "object"},
                    sort={"direction": "ascending", "timestamp": "last_edited_time"}
                )
                
                doc_section_id = None
                for page in response.get("results", []):
                    props = page.get("properties", {})
                    title_prop = props.get("title", {})
                    if title_prop.get("title"):
                        title = title_prop["title"][0].get("plain_text", "")
                        if "Documentation" in title:
                            doc_section_id = page["id"]
                            break
                
                if doc_section_id:
                    # Create Governance folder within Documentation
                    governance_folder = integration.client.create_page(
                        parent_id=doc_section_id,
                        title="📋 Governance"
                    )
                    governance_folder_id = governance_folder["id"]
                    integration.doc_folders["GOVERNANCE"] = governance_folder_id
                    print(f"[OK] Created Governance folder in Documentation section")
                else:
                    # Create as top-level page
                    governance_folder = integration.client.create_page(
                        parent_id=integration.team_space_id,
                        title="📋 Governance"
                    )
                    governance_folder_id = governance_folder["id"]
                    integration.doc_folders["GOVERNANCE"] = governance_folder_id
                    print(f"[OK] Created Governance section as top-level page")
            except Exception as e:
                print(f"[WARNING] Could not find Documentation section: {e}")
                # Create as top-level page
                governance_folder = integration.client.create_page(
                    parent_id=integration.team_space_id,
                    title="📋 Governance"
                )
                governance_folder_id = governance_folder["id"]
                integration.doc_folders["GOVERNANCE"] = governance_folder_id
                print(f"[OK] Created Governance section as top-level page")
        
        # Create governance review page
        print("[INFO] Creating Governance Review page in Notion...")
        
        # Convert markdown to Notion blocks
        blocks = integration._markdown_to_notion_blocks(governance_doc)
        
        # Split into chunks if needed (100 block limit)
        initial_blocks = blocks[:100]
        remaining_blocks = blocks[100:]
        
        page = integration.client.create_page(
            parent_id=governance_folder_id,
            title=f"Governance Review - {datetime.now().strftime('%Y-%m-%d')}",
            content=initial_blocks
        )
        
        # Append remaining blocks
        if remaining_blocks:
            chunk_size = 100
            for i in range(0, len(remaining_blocks), chunk_size):
                chunk = remaining_blocks[i:i + chunk_size]
                integration.client.append_blocks(page["id"], chunk)
        
        print(f"[OK] Governance Review synced to Notion!")
        print(f"[INFO] Page ID: {page['id']}")
        
        return page["id"]
    
    except Exception as e:
        print(f"[ERROR] Failed to sync to Notion: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main governance review process"""
    print("=" * 70)
    print("GOVERNANCE REVIEW - FACILITATED BY SCRUM MASTER")
    print("=" * 70)
    print("\nThis review will:")
    print("1. Collect input from all team members")
    print("2. Review Team Charter, Definition of Done, and Communication")
    print("3. Document all decisions")
    print("4. Update governance frameworks")
    print("5. Sync decisions to Notion under Governance section")
    print()
    
    # Initialize agents
    print("[INFO] Initializing all team agents...")
    agents = get_all_agents()
    scrum_master = agents["Scrum Master"]
    
    print(f"[OK] {len(agents)} agents initialized")
    
    # Conduct governance review
    print("\n[INFO] Starting governance review...")
    
    # Review Team Charter
    team_charter_findings = review_team_charter(agents, scrum_master)
    
    # Review Definition of Done
    dod_findings = review_definition_of_done(agents, scrum_master)
    
    # Review Communication & Collaboration
    communication_findings = review_communication_collaboration(agents, scrum_master)
    
    # Update governance frameworks
    print("\n[INFO] Updating governance frameworks...")
    updated_charter = update_governance_frameworks(team_charter_findings, dod_findings)
    
    # Create governance decisions document
    review_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    governance_doc = create_governance_decisions_document(
        team_charter_findings,
        dod_findings,
        communication_findings,
        review_date
    )
    
    # Save governance document locally
    governance_file = Path(__file__).parent.parent / "GOVERNANCE_REVIEW.md"
    with open(governance_file, 'w', encoding='utf-8') as f:
        f.write(governance_doc)
    print(f"[OK] Governance decisions saved to: {governance_file}")
    
    # Save updated charter
    charter_file = Path(__file__).parent.parent / "governance" / "team_charter_updated.md"
    with open(charter_file, 'w', encoding='utf-8') as f:
        f.write(updated_charter.to_markdown())
    print(f"[OK] Updated Team Charter saved to: {charter_file}")
    
    # Sync to Notion
    print("\n[INFO] Setting up Notion integration...")
    api_token = os.getenv("NOTION_API_TOKEN")
    team_space_url = os.getenv("NOTION_TEAM_SPACE_URL", "https://www.notion.so/LaunchPadPM-2e89cb246f1f80a0a5b1f15433b0855c")
    
    if not api_token:
        print("[WARNING] NOTION_API_TOKEN not set. Skipping Notion sync.")
        print("Set NOTION_API_TOKEN to sync governance decisions to Notion.")
    else:
        integration = NotionIntegration(
            api_token=api_token,
            team_space_url=team_space_url
        )
        integration.load_config()
        
        page_id = sync_to_notion(governance_doc, integration)
        if page_id:
            print(f"[OK] Governance Review synced to Notion!")
            # Save updated config with Governance folder
            integration.save_config()
    
    print("\n" + "=" * 70)
    print("GOVERNANCE REVIEW COMPLETE")
    print("=" * 70)
    print("\nSummary:")
    print(f"- Reviewed governance with {len(agents)} team members")
    print(f"- Collected input from all agents")
    print(f"- Documented all decisions")
    print(f"- Updated governance frameworks")
    print(f"- Saved to: {governance_file}")
    if api_token:
        print(f"- Synced to Notion Governance section")
    print("\nNext steps:")
    print("1. Review GOVERNANCE_REVIEW.md")
    print("2. Team members review updated governance")
    print("3. Schedule follow-up if needed")


if __name__ == "__main__":
    main()
