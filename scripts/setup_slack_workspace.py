"""
Slack Workspace Setup Script
Development Engineer and DevOps Engineer collaborate to set up Slack workspace
for CEO and team communication.
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.development_engineer_agent import DevelopmentEngineerAgent
from agents.devops_engineer_agent import DevOpsEngineerAgent
from agents.base_agent import AgentContext
from integrations.slack_integration import SlackIntegration


def dev_engineer_analysis(dev_agent: DevelopmentEngineerAgent) -> Dict[str, Any]:
    """Get Development Engineer's perspective on Slack setup"""
    query = """
We need to set up Slack for team communication. The CEO wants to easily communicate 
with the team via Slack, and team members should be able to ask questions and receive 
instructions. 

As a Development Engineer, what channels and structure would you recommend? 
What would help the development team collaborate effectively?
"""
    
    response = dev_agent.process_query(query)
    
    return {
        "perspective": response.response,
        "recommendations": response.recommendations,
        "questions": response.questions,
        "channels_suggested": [
            "dev-engineering",
            "code-reviews",
            "technical-discussions",
            "sprint-planning"
        ]
    }


def devops_engineer_analysis(devops_agent: DevOpsEngineerAgent) -> Dict[str, Any]:
    """Get DevOps Engineer's perspective on Slack setup"""
    query = """
We need to set up Slack for team communication. The CEO wants to easily communicate 
with the team via Slack, and team members should be able to ask questions and receive 
instructions.

As a DevOps Engineer, what channels and integrations would you recommend? 
What would help with infrastructure, deployments, monitoring, and incident response?
"""
    
    response = devops_agent.process_query(query)
    
    return {
        "perspective": response.response,
        "recommendations": response.recommendations,
        "questions": response.questions,
        "channels_suggested": [
            "devops-infrastructure",
            "deployments",
            "incidents",
            "monitoring-alerts"
        ],
        "integrations_suggested": [
            "CI/CD notifications",
            "Monitoring alerts",
            "Deployment status",
            "Incident notifications"
        ]
    }


def create_setup_plan(dev_analysis: Dict, devops_analysis: Dict) -> Dict[str, Any]:
    """Create a comprehensive setup plan based on both agents' input"""
    
    # Combine channel suggestions
    all_channels = set()
    all_channels.update(dev_analysis.get("channels_suggested", []))
    all_channels.update(devops_analysis.get("channels_suggested", []))
    
    # Standard channels that should always exist
    standard_channels = {
        "general": "General team discussions",
        "ceo-announcements": "CEO announcements and strategic updates",
        "product-team": "Product team discussions",
        "dev-engineering": "Development engineering discussions",
        "devops-infrastructure": "DevOps and infrastructure discussions",
        "sprint-planning": "Sprint planning sessions",
        "daily-standup": "Daily standup updates",
        "incidents": "Production incidents and alerts",
        "random": "Casual conversations"
    }
    
    # Add suggested channels
    for channel in all_channels:
        if channel not in standard_channels:
            standard_channels[channel] = f"{channel.replace('-', ' ').title()} discussions"
    
    plan = {
        "channels": standard_channels,
        "dev_recommendations": dev_analysis.get("recommendations", []),
        "devops_recommendations": devops_analysis.get("recommendations", []),
        "integrations": devops_analysis.get("integrations_suggested", []),
        "setup_steps": [
            "1. Test Slack API connection",
            "2. Create standard team channels",
            "3. Set channel topics and descriptions",
            "4. Configure channel permissions",
            "5. Set up welcome message",
            "6. Document channel purposes",
            "7. Save configuration"
        ]
    }
    
    return plan


def generate_setup_report(dev_analysis: Dict, devops_analysis: Dict, plan: Dict, setup_result: Dict) -> str:
    """Generate a setup report"""
    
    report = f"""# Slack Workspace Setup Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Facilitated by:** Development Engineer & DevOps Engineer

---

## Executive Summary

Slack workspace has been set up to enable seamless communication between the CEO and the team. 
The setup includes dedicated channels for different aspects of team collaboration, following 
recommendations from both Development Engineer and DevOps Engineer.

---

## 1. Development Engineer Analysis

### Perspective
{dev_analysis['perspective'][:500]}...

### Key Recommendations
{chr(10).join(f"- {rec}" for rec in dev_analysis['recommendations'][:5])}

### Suggested Channels
{chr(10).join(f"- #{channel}" for channel in dev_analysis.get('channels_suggested', []))}

---

## 2. DevOps Engineer Analysis

### Perspective
{devops_analysis['perspective'][:500]}...

### Key Recommendations
{chr(10).join(f"- {rec}" for rec in devops_analysis['recommendations'][:5])}

### Suggested Channels
{chr(10).join(f"- #{channel}" for channel in devops_analysis.get('channels_suggested', []))}

### Suggested Integrations
{chr(10).join(f"- {integration}" for integration in devops_analysis.get('integrations_suggested', []))}

---

## 3. Setup Plan

### Channels Created

"""
    
    for channel_name, description in plan['channels'].items():
        report += f"**#{channel_name}**\n"
        report += f"- {description}\n\n"
    
    report += f"""
### Setup Steps Completed

{chr(10).join(plan['setup_steps'])}

---

## 4. Setup Results

**Workspace:** {setup_result.get('workspace', 'Unknown')}
**Workspace ID:** {setup_result.get('workspace_id', 'Unknown')}
**Total Channels:** {setup_result.get('total_channels', 0)}

### Channels Created

"""
    
    for channel_key, channel_info in setup_result.get('channels', {}).items():
        report += f"- **#{channel_info['name']}** (ID: {channel_info['id']})\n"
        report += f"  - Topic: {channel_info.get('topic', 'N/A')}\n\n"
    
    report += """
---

## 5. Usage Guidelines

### For CEO

1. **#ceo-announcements** - Use for important announcements, strategic updates, and company-wide communications
2. **#product-team** - Engage with the product team on priorities and direction
3. **#general** - General team communications

### For Team Members

1. **Ask Questions** - Use appropriate channels for questions:
   - Technical questions → #dev-engineering
   - Infrastructure questions → #devops-infrastructure
   - Product questions → #product-team
   - General questions → #general

2. **Share Updates** - Use #daily-standup for daily progress updates

3. **Report Issues** - Use #incidents for production issues

### Channel Purposes

- **#general** - General team discussions and announcements
- **#ceo-announcements** - CEO announcements, strategic updates
- **#product-team** - Product team discussions, sprint planning
- **#dev-engineering** - Development engineering discussions, code reviews
- **#devops-infrastructure** - DevOps, infrastructure, deployments
- **#sprint-planning** - Sprint planning sessions
- **#daily-standup** - Daily standup updates
- **#incidents** - Production incidents and alerts
- **#random** - Casual conversations

---

## 6. Next Steps

1. ✅ Slack workspace setup complete
2. ⏳ Invite team members to workspace
3. ⏳ Set up CI/CD integrations (DevOps Engineer)
4. ⏳ Configure monitoring alerts (DevOps Engineer)
5. ⏳ Set up webhook integrations for automated notifications
6. ⏳ Train team on Slack usage and channel purposes

---

## 7. Integration Opportunities

### Recommended Integrations (from DevOps Engineer)

"""
    
    for integration in plan.get('integrations', []):
        report += f"- {integration}\n"
    
    report += """
### Implementation Notes

- CI/CD notifications can be configured to post to #deployments or #devops-infrastructure
- Monitoring alerts should post to #incidents
- Deployment status can be posted to #deployments
- Consider setting up Slack apps for:
  - GitHub/GitLab integration
  - Jira/Linear integration
  - Monitoring tools (Datadog, New Relic, etc.)
  - Calendar integration for sprint events

---

## 8. Configuration

Configuration saved to: `config/slack_config.json`

This file contains:
- Workspace ID and name
- Channel IDs and names
- Last update timestamp

**Note:** Keep this file secure and do not commit sensitive tokens to version control.

"""
    
    return report


def main():
    """Main Slack setup process"""
    print("=" * 70)
    print("SLACK WORKSPACE SETUP")
    print("Development Engineer & DevOps Engineer Collaboration")
    print("=" * 70)
    
    # Check for Slack token
    api_token = os.getenv("SLACK_BOT_TOKEN")
    if not api_token:
        print("\n[ERROR] SLACK_BOT_TOKEN not set.")
        print("\nTo set up Slack integration:")
        print("1. Go to https://api.slack.com/apps")
        print("2. Create a new app or select existing app")
        print("3. Go to 'OAuth & Permissions'")
        print("4. Add the following Bot Token Scopes:")
        print("   - channels:read")
        print("   - channels:write")
        print("   - channels:manage")
        print("   - chat:write")
        print("   - chat:write.public")
        print("   - conversations:read")
        print("   - conversations:write")
        print("5. Install the app to your workspace")
        print("6. Copy the 'Bot User OAuth Token' (starts with xoxb-)")
        print("7. Set it as SLACK_BOT_TOKEN environment variable")
        print("\nExample:")
        print("  export SLACK_BOT_TOKEN='xoxb-your-token-here'")
        print("  # or on Windows:")
        print("  $env:SLACK_BOT_TOKEN='xoxb-your-token-here'")
        return
    
    print("\n[INFO] Initializing agents...")
    context = AgentContext()
    dev_agent = DevelopmentEngineerAgent(context)
    devops_agent = DevOpsEngineerAgent(context)
    
    print("[OK] Agents initialized")
    
    # Get agent perspectives
    print("\n[INFO] Getting Development Engineer perspective...")
    dev_analysis = dev_engineer_analysis(dev_agent)
    
    print("[INFO] Getting DevOps Engineer perspective...")
    devops_analysis = devops_engineer_analysis(devops_agent)
    
    # Create setup plan
    print("\n[INFO] Creating setup plan...")
    plan = create_setup_plan(dev_analysis, devops_analysis)
    
    # Initialize Slack integration
    print("\n[INFO] Initializing Slack integration...")
    integration = SlackIntegration(api_token=api_token)
    
    if not integration.test_connection():
        print("[ERROR] Failed to connect to Slack. Check your token and permissions.")
        return
    
    # Set up workspace
    print("\n[INFO] Setting up Slack workspace...")
    setup_result = integration.setup_team_workspace("Product Team")
    
    # Generate report
    report = generate_setup_report(dev_analysis, devops_analysis, plan, setup_result)
    
    # Save report
    report_file = Path(__file__).parent.parent / "SLACK_SETUP_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n[OK] Setup report saved to: {report_file}")
    
    print("\n" + "=" * 70)
    print("SLACK WORKSPACE SETUP COMPLETE")
    print("=" * 70)
    print(f"\nWorkspace: {setup_result.get('workspace', 'Unknown')}")
    print(f"Channels created: {setup_result.get('total_channels', 0)}")
    print(f"\nReview the report: {report_file}")
    print("\nNext steps:")
    print("1. Review SLACK_SETUP_REPORT.md")
    print("2. Invite team members to the workspace")
    print("3. Set up CI/CD and monitoring integrations")
    print("4. Configure webhook integrations for automated notifications")


if __name__ == "__main__":
    main()
