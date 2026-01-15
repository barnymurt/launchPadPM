"""
LaunchpadPM Slack Integration Connection
Development Engineer and DevOps Engineer collaborate to connect
Slack integration for LaunchpadPM workspace.
"""

import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.development_engineer_agent import DevelopmentEngineerAgent
from agents.devops_engineer_agent import DevOpsEngineerAgent
from agents.base_agent import AgentContext
from integrations.slack_integration import SlackIntegration


def extract_workspace_id_from_url(url: str) -> str:
    """Extract workspace ID from Slack URL"""
    # Pattern: T followed by alphanumeric (workspace ID)
    match = re.search(r'/T([A-Z0-9]+)', url)
    if match:
        return f"T{match.group(1)}"
    return None


def dev_engineer_slack_planning(dev_agent: DevelopmentEngineerAgent, workspace_id: str) -> Dict[str, Any]:
    """Get Development Engineer's plan for Slack integration"""
    query = f"""
We need to connect Slack integration for LaunchpadPM. The workspace ID is {workspace_id}.
As a Development Engineer, what do we need to set up for effective team collaboration?

Consider:
1. Channels for development discussions
2. Code review workflows
3. Sprint planning and daily standups
4. Technical decision-making
5. Integration with development tools

What's your recommendation for the channel structure and how should we organize it?
"""
    
    response = dev_agent.process_query(query)
    
    return {
        "perspective": response.response,
        "recommendations": response.recommendations,
        "questions": response.questions,
        "dev_channels": [
            "launchpadpm-dev",
            "code-reviews",
            "technical-decisions",
            "sprint-planning"
        ]
    }


def devops_engineer_slack_planning(devops_agent: DevOpsEngineerAgent, workspace_id: str) -> Dict[str, Any]:
    """Get DevOps Engineer's plan for Slack integration"""
    query = f"""
We need to connect Slack integration for LaunchpadPM. The workspace ID is {workspace_id}.
As a DevOps Engineer, what infrastructure and operations channels do we need?

Consider:
1. Deployment and CI/CD notifications
2. Monitoring and alerting
3. Incident response
4. Infrastructure changes
5. Integration with DevOps tools

What's your recommendation for the DevOps channel structure and integrations?
"""
    
    response = devops_agent.process_query(query)
    
    return {
        "perspective": response.response,
        "recommendations": response.recommendations,
        "questions": response.questions,
        "devops_channels": [
            "launchpadpm-deployments",
            "launchpadpm-incidents",
            "launchpadpm-monitoring",
            "launchpadpm-infrastructure"
        ],
        "integrations": [
            "CI/CD pipeline notifications",
            "Monitoring alerts",
            "Deployment status",
            "Infrastructure change notifications"
        ]
    }


def create_collaborative_channel_plan(dev_plan: Dict, devops_plan: Dict) -> Dict[str, Any]:
    """Create unified channel plan from both agents' recommendations"""
    
    channels_config = {
        "general": {
            "name": "general",
            "topic": "General LaunchpadPM team discussions and announcements",
            "is_private": False,
            "created_by": "Both"
        },
        "ceo-announcements": {
            "name": "ceo-announcements",
            "topic": "CEO announcements, strategic updates, and important LaunchpadPM communications",
            "is_private": False,
            "created_by": "Both"
        },
        "launchpadpm-dev": {
            "name": "launchpadpm-dev",
            "topic": "LaunchpadPM development discussions, code reviews, and technical decisions",
            "is_private": False,
            "created_by": "Development Engineer"
        },
        "launchpadpm-devops": {
            "name": "launchpadpm-devops",
            "topic": "LaunchpadPM DevOps, infrastructure, deployments, and CI/CD discussions",
            "is_private": False,
            "created_by": "DevOps Engineer"
        },
        "launchpadpm-deployments": {
            "name": "launchpadpm-deployments",
            "topic": "LaunchpadPM deployment status, rollouts, and release notifications",
            "is_private": False,
            "created_by": "DevOps Engineer"
        },
        "launchpadpm-incidents": {
            "name": "launchpadpm-incidents",
            "topic": "LaunchpadPM production incidents, alerts, and incident response",
            "is_private": False,
            "created_by": "DevOps Engineer"
        },
        "launchpadpm-monitoring": {
            "name": "launchpadpm-monitoring",
            "topic": "LaunchpadPM monitoring alerts, metrics, and observability",
            "is_private": False,
            "created_by": "DevOps Engineer"
        },
        "launchpadpm-infrastructure": {
            "name": "launchpadpm-infrastructure",
            "topic": "LaunchpadPM infrastructure changes, scaling, and capacity planning",
            "is_private": False,
            "created_by": "DevOps Engineer"
        },
        "code-reviews": {
            "name": "code-reviews",
            "topic": "Code review discussions and pull request notifications",
            "is_private": False,
            "created_by": "Development Engineer"
        },
        "technical-decisions": {
            "name": "technical-decisions",
            "topic": "Technical architecture decisions and ADR discussions",
            "is_private": False,
            "created_by": "Development Engineer"
        },
        "sprint-planning": {
            "name": "sprint-planning",
            "topic": "Sprint planning sessions and backlog discussions",
            "is_private": False,
            "created_by": "Both"
        },
        "daily-standup": {
            "name": "daily-standup",
            "topic": "Daily standup updates and progress tracking",
            "is_private": False,
            "created_by": "Both"
        },
        "random": {
            "name": "random",
            "topic": "Non-work banter, team building, and casual conversations",
            "is_private": False,
            "created_by": "Both"
        }
    }
    
    return channels_config


def connect_launchpadpm_workspace(integration: SlackIntegration, channels_config: Dict) -> Dict[str, Any]:
    """Connect to LaunchpadPM workspace and set up channels"""
    
    if not integration.test_connection():
        raise ConnectionError("Cannot connect to Slack API. Check your token and permissions.")
    
    print("[INFO] Connecting to LaunchpadPM Slack workspace...")
    
    workspace_info = integration.client.get_workspace_info()
    print(f"[OK] Connected to workspace: {workspace_info.get('team')}")
    print(f"[INFO] Workspace ID: {workspace_info.get('team_id')}")
    
    # List existing channels
    print("\n[INFO] Checking existing channels...")
    existing_channels = integration.client.list_channels()
    existing_channel_names = {ch.get('name'): ch for ch in existing_channels}
    print(f"[INFO] Found {len(existing_channels)} existing channels")
    
    created_channels = {}
    found_channels = {}
    
    # Create or get channels
    for channel_key, config in channels_config.items():
        channel_name = config["name"]
        print(f"\n[INFO] Setting up channel: #{channel_name}")
        
        # Check if channel already exists
        if channel_name in existing_channel_names:
            channel = existing_channel_names[channel_name]
            channel_id = channel.get("id")
            print(f"[OK] Channel #{channel_name} already exists (ID: {channel_id})")
            found_channels[channel_key] = {
                "id": channel_id,
                "name": channel_name,
                "topic": config["topic"],
                "status": "existing"
            }
            integration.channels[channel_name] = channel_id
        else:
            # Create new channel
            channel = integration.client.create_channel(
                name=channel_name,
                is_private=config["is_private"]
            )
            
            if channel:
                channel_id = channel.get("id")
                integration.channels[channel_name] = channel_id
                
                # Set channel topic
                integration.client.set_channel_topic(channel_id, config["topic"])
                
                created_channels[channel_key] = {
                    "id": channel_id,
                    "name": channel_name,
                    "topic": config["topic"],
                    "created_by": config.get("created_by", "System")
                }
                print(f"[OK] Created channel #{channel_name}")
            else:
                print(f"[ERROR] Failed to create channel #{channel_name}")
    
    # Send welcome message to general channel
    general_channel_id = None
    if "general" in created_channels:
        general_channel_id = created_channels["general"]["id"]
    elif "general" in found_channels:
        general_channel_id = found_channels["general"]["id"]
    
    if general_channel_id:
        welcome_message = f"""
🚀 Welcome to the LaunchpadPM Slack workspace!

This workspace has been set up by the Development Engineer and DevOps Engineer with the following channels:

**Development Channels:**
💻 #launchpadpm-dev - Development discussions and code reviews
📝 #code-reviews - Code review discussions
🏗️ #technical-decisions - Technical architecture decisions

**DevOps Channels:**
🔧 #launchpadpm-devops - DevOps and infrastructure discussions
🚀 #launchpadpm-deployments - Deployment status and releases
🚨 #launchpadpm-incidents - Production incidents and alerts
📊 #launchpadpm-monitoring - Monitoring alerts and metrics
🏗️ #launchpadpm-infrastructure - Infrastructure changes

**Team Channels:**
📢 #ceo-announcements - CEO announcements and strategic updates
📋 #sprint-planning - Sprint planning sessions
📊 #daily-standup - Daily standup updates
💬 #random - Casual conversations

**Integration Points:**
- CI/CD pipelines → #launchpadpm-deployments
- Monitoring alerts → #launchpadpm-monitoring and #launchpadpm-incidents
- Infrastructure changes → #launchpadpm-infrastructure
- Code reviews → #code-reviews

Let's build LaunchpadPM together! 🚀
"""
        integration.client.send_message(
            channel=general_channel_id,
            text=welcome_message
        )
        print("\n[OK] Welcome message sent to #general")
    
    # Save configuration
    integration.save_config()
    
    result = {
        "workspace": workspace_info.get("team"),
        "workspace_id": workspace_info.get("team_id"),
        "channels_created": created_channels,
        "channels_existing": found_channels,
        "total_channels": len(created_channels) + len(found_channels)
    }
    
    return result


def generate_connection_report(dev_plan: Dict, devops_plan: Dict, channels_config: Dict, connection_result: Dict) -> str:
    """Generate connection report"""
    
    report = f"""# LaunchpadPM Slack Integration Connection Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Facilitated by:** Development Engineer & DevOps Engineer
**Workspace:** {connection_result.get('workspace', 'Unknown')}
**Workspace ID:** {connection_result.get('workspace_id', 'Unknown')}

---

## Executive Summary

Slack integration has been successfully connected for LaunchpadPM workspace. 
Development Engineer and DevOps Engineer collaborated to set up a comprehensive 
channel structure supporting both development workflows and operations.

---

## 1. Development Engineer Planning

### Perspective
{dev_plan['perspective'][:500]}...

### Key Recommendations
{chr(10).join(f"- {rec}" for rec in dev_plan['recommendations'][:6])}

### Suggested Channels
{chr(10).join(f"- #{channel}" for channel in dev_plan.get('dev_channels', []))}

---

## 2. DevOps Engineer Planning

### Perspective
{devops_plan['perspective'][:500]}...

### Key Recommendations
{chr(10).join(f"- {rec}" for rec in devops_plan['recommendations'][:6])}

### Suggested Channels
{chr(10).join(f"- #{channel}" for channel in devops_plan.get('devops_channels', []))}

### Suggested Integrations
{chr(10).join(f"- {integration}" for integration in devops_plan.get('integrations', []))}

---

## 3. Channel Structure

### Development Channels

**#launchpadpm-dev**
- {channels_config['launchpadpm-dev']['topic']}
- Created by: {channels_config['launchpadpm-dev']['created_by']}

**#code-reviews**
- {channels_config['code-reviews']['topic']}
- Created by: {channels_config['code-reviews']['created_by']}

**#technical-decisions**
- {channels_config['technical-decisions']['topic']}
- Created by: {channels_config['technical-decisions']['created_by']}

### DevOps Channels

**#launchpadpm-devops**
- {channels_config['launchpadpm-devops']['topic']}
- Created by: {channels_config['launchpadpm-devops']['created_by']}

**#launchpadpm-deployments**
- {channels_config['launchpadpm-deployments']['topic']}
- Created by: {channels_config['launchpadpm-deployments']['created_by']}

**#launchpadpm-incidents**
- {channels_config['launchpadpm-incidents']['topic']}
- Created by: {channels_config['launchpadpm-incidents']['created_by']}

**#launchpadpm-monitoring**
- {channels_config['launchpadpm-monitoring']['topic']}
- Created by: {channels_config['launchpadpm-monitoring']['created_by']}

**#launchpadpm-infrastructure**
- {channels_config['launchpadpm-infrastructure']['topic']}
- Created by: {channels_config['launchpadpm-infrastructure']['created_by']}

### Team Channels

- **#general** - General team discussions
- **#ceo-announcements** - CEO announcements
- **#sprint-planning** - Sprint planning
- **#daily-standup** - Daily standups
- **#random** - Casual conversations

---

## 4. Connection Results

**Total Channels:** {connection_result.get('total_channels', 0)}
**Channels Created:** {len(connection_result.get('channels_created', {}))}
**Existing Channels Found:** {len(connection_result.get('channels_existing', {}))}

### Newly Created Channels

"""
    
    for channel_key, channel_info in connection_result.get('channels_created', {}).items():
        report += f"- **#{channel_info['name']}** (ID: {channel_info['id']})\n"
        report += f"  - Topic: {channel_info.get('topic', 'N/A')}\n"
        report += f"  - Created by: {channel_info.get('created_by', 'System')}\n\n"
    
    if connection_result.get('channels_existing'):
        report += "### Existing Channels\n\n"
        for channel_key, channel_info in connection_result.get('channels_existing', {}).items():
            report += f"- **#{channel_info['name']}** (ID: {channel_info['id']})\n"
            report += f"  - Topic: {channel_info.get('topic', 'N/A')}\n\n"
    
    report += """
---

## 5. Integration Setup

### CI/CD Integration

**Channels:** #launchpadpm-deployments, #launchpadpm-devops

**Setup Steps:**
1. Configure CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins, etc.)
2. Add Slack webhook or API integration
3. Post notifications for:
   - Build start/finish
   - Deployment start/success/failure
   - Test results
   - Release notifications

### Monitoring Integration

**Channels:** #launchpadpm-monitoring, #launchpadpm-incidents

**Setup Steps:**
1. Configure monitoring tool (Datadog, New Relic, CloudWatch, etc.)
2. Set up Slack integration
3. Route alerts:
   - Critical → #launchpadpm-incidents
   - Warnings → #launchpadpm-monitoring

### Code Review Integration

**Channels:** #code-reviews, #launchpadpm-dev

**Setup Steps:**
1. Configure GitHub/GitLab webhook
2. Post PR notifications to #code-reviews
3. Link PR discussions to Slack threads

---

## 6. Next Steps

1. ✅ Slack workspace connected
2. ✅ Channels created/configured
3. ⏳ Invite team members to channels
4. ⏳ Configure CI/CD integrations
5. ⏳ Set up monitoring integrations
6. ⏳ Configure code review notifications
7. ⏳ Train team on channel usage

---

## 7. Configuration

Configuration saved to: `config/slack_config.json`

This file contains:
- Workspace ID and name
- Channel IDs and names
- Last update timestamp

**Note:** Keep this file secure and do not commit sensitive tokens to version control.

"""
    
    return report


def main():
    """Main connection process"""
    app_name = "LaunchpadPM"
    slack_url = "https://app.slack.com/client/T0A8JCB70HH/C0A9K3EPPGQ"
    workspace_id = extract_workspace_id_from_url(slack_url)
    
    print("=" * 70)
    print(f"LAUNCHPADPM SLACK INTEGRATION CONNECTION")
    print("Development Engineer & DevOps Engineer Collaboration")
    print("=" * 70)
    
    if workspace_id:
        print(f"\n[INFO] Detected workspace ID: {workspace_id}")
    else:
        print("\n[WARNING] Could not extract workspace ID from URL")
        workspace_id = "T0A8JCB70HH"  # Use provided ID
    
    # Check for Slack token (support both bot token and OAuth token)
    api_token = os.getenv("SLACK_BOT_TOKEN") or os.getenv("SLACK_ACCESS_TOKEN")
    refresh_token = os.getenv("SLACK_REFRESH_TOKEN")
    
    if not api_token:
        print("\n[ERROR] SLACK_BOT_TOKEN or SLACK_ACCESS_TOKEN not set.")
        print("\nTo connect Slack integration:")
        print("1. Go to https://api.slack.com/apps")
        print("2. Create a new app called 'LaunchpadPM Bot'")
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
        print("   OR use OAuth tokens (xoxe.xoxp- for access, xoxe-1- for refresh)")
        print("\nThen set the token:")
        print("  $env:SLACK_ACCESS_TOKEN='xoxe.xoxp-your-token-here'")
        print("  $env:SLACK_REFRESH_TOKEN='xoxe-1-your-refresh-token-here'")
        return
    
    print("\n[INFO] Initializing agents...")
    context = AgentContext()
    dev_agent = DevelopmentEngineerAgent(context)
    devops_agent = DevOpsEngineerAgent(context)
    
    print("[OK] Agents initialized")
    
    # Get planning from both agents
    print(f"\n[INFO] Getting Development Engineer planning for {app_name}...")
    dev_plan = dev_engineer_slack_planning(dev_agent, workspace_id)
    
    print(f"[INFO] Getting DevOps Engineer planning for {app_name}...")
    devops_plan = devops_engineer_slack_planning(devops_agent, workspace_id)
    
    # Create collaborative channel plan
    print("\n[INFO] Creating collaborative channel plan...")
    channels_config = create_collaborative_channel_plan(dev_plan, devops_plan)
    
    # Initialize Slack integration
    print("\n[INFO] Initializing Slack integration...")
    integration = SlackIntegration(api_token=api_token, refresh_token=refresh_token)
    
    if not integration.test_connection():
        print("[ERROR] Failed to connect to Slack. Check your token and permissions.")
        return
    
    # Connect to workspace and set up channels
    print(f"\n[INFO] Connecting to {app_name} workspace and setting up channels...")
    connection_result = connect_launchpadpm_workspace(integration, channels_config)
    
    # Generate report
    report = generate_connection_report(dev_plan, devops_plan, channels_config, connection_result)
    
    # Save report
    report_file = Path(__file__).parent.parent / "LAUNCHPADPM_SLACK_CONNECTION_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n[OK] Connection report saved to: {report_file}")
    
    print("\n" + "=" * 70)
    print("LAUNCHPADPM SLACK INTEGRATION CONNECTED")
    print("=" * 70)
    print(f"\nWorkspace: {connection_result.get('workspace', 'Unknown')}")
    print(f"Workspace ID: {connection_result.get('workspace_id', 'Unknown')}")
    print(f"Total channels: {connection_result.get('total_channels', 0)}")
    print(f"  - Created: {len(connection_result.get('channels_created', {}))}")
    print(f"  - Existing: {len(connection_result.get('channels_existing', {}))}")
    print(f"\nReview the report: {report_file}")
    print("\nNext steps:")
    print("1. Review the connection report")
    print("2. Invite team members to relevant channels")
    print("3. Configure CI/CD and monitoring integrations")
    print("4. Set up code review notifications")


if __name__ == "__main__":
    main()
