"""
DevOps Engineer Slack Setup Script
DevOps Engineer sets up Slack integration for LaunchpadPM app
with focus on infrastructure, monitoring, and CI/CD integrations.
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.devops_engineer_agent import DevOpsEngineerAgent
from agents.base_agent import AgentContext
from integrations.slack_integration import SlackIntegration


def devops_slack_analysis(devops_agent: DevOpsEngineerAgent, app_name: str) -> Dict[str, Any]:
    """Get DevOps Engineer's perspective on Slack setup for the app"""
    query = f"""
We need to set up Slack integration for our {app_name} application. 
As a DevOps Engineer, I need to:

1. Set up channels for infrastructure and operations
2. Configure monitoring and alerting integrations
3. Set up CI/CD pipeline notifications
4. Enable incident response workflows
5. Create channels for deployment status and infrastructure discussions

What channels, integrations, and workflows would you recommend? 
How should we structure Slack to support DevOps best practices?
"""
    
    response = devops_agent.process_query(query)
    
    return {
        "perspective": response.response,
        "recommendations": response.recommendations,
        "questions": response.questions,
        "channels_suggested": [
            "deployments",
            "infrastructure",
            "monitoring-alerts",
            "incidents",
            "ci-cd-pipeline",
            "devops-ops"
        ],
        "integrations_suggested": [
            "CI/CD pipeline notifications",
            "Monitoring alerts (Datadog, New Relic, CloudWatch)",
            "Deployment status updates",
            "Incident notifications",
            "Infrastructure change notifications"
        ]
    }


def create_devops_channels_config(app_name: str, devops_analysis: Dict) -> Dict[str, Any]:
    """Create channel configuration based on DevOps recommendations"""
    
    # Base channels for LaunchpadPM
    channels_config = {
        "general": {
            "name": "general",
            "topic": f"General {app_name} team discussions and announcements",
            "is_private": False
        },
        "ceo-announcements": {
            "name": "ceo-announcements",
            "topic": f"CEO announcements, strategic updates, and important {app_name} communications",
            "is_private": False
        },
        "launchpadpm-dev": {
            "name": "launchpadpm-dev",
            "topic": f"{app_name} development discussions, code reviews, and technical decisions",
            "is_private": False
        },
        "launchpadpm-devops": {
            "name": "launchpadpm-devops",
            "topic": f"{app_name} DevOps, infrastructure, deployments, and CI/CD discussions",
            "is_private": False
        },
        "launchpadpm-deployments": {
            "name": "launchpadpm-deployments",
            "topic": f"{app_name} deployment status, rollouts, and release notifications",
            "is_private": False
        },
        "launchpadpm-incidents": {
            "name": "launchpadpm-incidents",
            "topic": f"{app_name} production incidents, alerts, and incident response",
            "is_private": False
        },
        "launchpadpm-monitoring": {
            "name": "launchpadpm-monitoring",
            "topic": f"{app_name} monitoring alerts, metrics, and observability",
            "is_private": False
        },
        "launchpadpm-infrastructure": {
            "name": "launchpadpm-infrastructure",
            "topic": f"{app_name} infrastructure changes, scaling, and capacity planning",
            "is_private": False
        },
        "sprint-planning": {
            "name": "sprint-planning",
            "topic": "Sprint planning sessions and backlog discussions",
            "is_private": False
        },
        "daily-standup": {
            "name": "daily-standup",
            "topic": "Daily standup updates and progress tracking",
            "is_private": False
        },
        "random": {
            "name": "random",
            "topic": "Non-work banter, team building, and casual conversations",
            "is_private": False
        }
    }
    
    return channels_config


def generate_devops_setup_plan(app_name: str, devops_analysis: Dict, channels_config: Dict) -> Dict[str, Any]:
    """Generate comprehensive DevOps setup plan"""
    
    plan = {
        "app_name": app_name,
        "channels": channels_config,
        "devops_recommendations": devops_analysis.get("recommendations", []),
        "integrations": devops_analysis.get("integrations_suggested", []),
        "setup_steps": [
            "1. Test Slack API connection",
            "2. Create LaunchpadPM-specific channels",
            "3. Set channel topics and descriptions",
            "4. Configure channel permissions",
            "5. Set up welcome message with DevOps focus",
            "6. Document integration points",
            "7. Save configuration"
        ],
        "integration_setup": {
            "ci_cd": {
                "channels": ["launchpadpm-deployments", "launchpadpm-devops"],
                "notifications": [
                    "Build start/finish",
                    "Deployment start/success/failure",
                    "Test results",
                    "Release notifications"
                ]
            },
            "monitoring": {
                "channels": ["launchpadpm-monitoring", "launchpadpm-incidents"],
                "alerts": [
                    "Error rate thresholds",
                    "Response time degradation",
                    "Resource utilization",
                    "Service health checks"
                ]
            },
            "infrastructure": {
                "channels": ["launchpadpm-infrastructure", "launchpadpm-devops"],
                "notifications": [
                    "Infrastructure changes",
                    "Scaling events",
                    "Capacity planning",
                    "Cost alerts"
                ]
            }
        }
    }
    
    return plan


def setup_launchpadpm_slack(integration: SlackIntegration, app_name: str, channels_config: Dict) -> Dict[str, Any]:
    """Set up Slack workspace for LaunchpadPM"""
    
    if not integration.test_connection():
        raise ConnectionError("Cannot connect to Slack API. Check your token and permissions.")
    
    print(f"[INFO] Setting up Slack workspace for {app_name}...")
    
    workspace_info = integration.client.get_workspace_info()
    print(f"[INFO] Connected to workspace: {workspace_info.get('team')}")
    
    created_channels = {}
    existing_channels = {}
    
    # Create or get channels
    for channel_key, config in channels_config.items():
        print(f"[INFO] Setting up channel: #{config['name']}")
        channel = integration.client.get_or_create_channel(
            name=config["name"],
            is_private=config["is_private"]
        )
        
        if channel:
            channel_id = channel.get("id")
            integration.channels[config["name"]] = channel_id
            
            # Set channel topic
            integration.client.set_channel_topic(channel_id, config["topic"])
            
            if channel.get("is_archived"):
                print(f"[WARNING] Channel #{config['name']} exists but is archived")
                existing_channels[channel_key] = {
                    "id": channel_id,
                    "name": config["name"],
                    "status": "archived"
                }
            else:
                created_channels[channel_key] = {
                    "id": channel_id,
                    "name": config["name"],
                    "topic": config["topic"]
                }
                print(f"[OK] Channel #{config['name']} ready")
        else:
            print(f"[ERROR] Failed to create channel #{config['name']}")
    
    # Send welcome message to general channel
    if "general" in created_channels:
        welcome_message = f"""
🚀 Welcome to the {app_name} Slack workspace!

This workspace has been set up by the DevOps Engineer with the following channels:

📢 **#ceo-announcements** - CEO announcements and strategic updates
💻 **#launchpadpm-dev** - {app_name} development discussions and code reviews
🔧 **#launchpadpm-devops** - DevOps, infrastructure, and CI/CD discussions
🚀 **#launchpadpm-deployments** - Deployment status and release notifications
🚨 **#launchpadpm-incidents** - Production incidents and alerts
📊 **#launchpadpm-monitoring** - Monitoring alerts and metrics
🏗️ **#launchpadpm-infrastructure** - Infrastructure changes and capacity planning
📋 **#sprint-planning** - Sprint planning sessions
📊 **#daily-standup** - Daily standup updates
💬 **#random** - Casual conversations

**DevOps Integration Points:**
- CI/CD pipelines can post to #launchpadpm-deployments
- Monitoring alerts should post to #launchpadpm-monitoring and #launchpadpm-incidents
- Infrastructure changes should be posted to #launchpadpm-infrastructure

Feel free to explore and start collaborating!
"""
        integration.client.send_message(
            channel=created_channels["general"]["id"],
            text=welcome_message
        )
    
    # Save configuration
    integration.save_config()
    
    result = {
        "app_name": app_name,
        "workspace": workspace_info.get("team"),
        "workspace_id": workspace_info.get("team_id"),
        "channels": created_channels,
        "existing_channels": existing_channels,
        "total_channels": len(created_channels) + len(existing_channels)
    }
    
    print(f"[OK] {app_name} workspace setup complete! Created {len(created_channels)} channels")
    return result


def generate_setup_report(app_name: str, devops_analysis: Dict, plan: Dict, setup_result: Dict) -> str:
    """Generate comprehensive setup report"""
    
    report = f"""# {app_name} Slack Workspace Setup Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Facilitated by:** DevOps Engineer
**Application:** {app_name}

---

## Executive Summary

Slack workspace has been set up for {app_name} with a focus on DevOps best practices, 
infrastructure management, monitoring, and CI/CD integration. The setup enables 
seamless communication between the CEO, development team, and operations.

---

## 1. DevOps Engineer Analysis

### Perspective
{devops_analysis['perspective'][:600]}...

### Key Recommendations
{chr(10).join(f"- {rec}" for rec in devops_analysis['recommendations'][:8])}

### Suggested Channels
{chr(10).join(f"- #{channel}" for channel in devops_analysis.get('channels_suggested', []))}

### Suggested Integrations
{chr(10).join(f"- {integration}" for integration in devops_analysis.get('integrations_suggested', []))}

---

## 2. Channel Structure

### Application-Specific Channels

**#launchpadpm-dev**
- {plan['channels']['launchpadpm-dev']['topic']}

**#launchpadpm-devops**
- {plan['channels']['launchpadpm-devops']['topic']}

**#launchpadpm-deployments**
- {plan['channels']['launchpadpm-deployments']['topic']}

**#launchpadpm-incidents**
- {plan['channels']['launchpadpm-incidents']['topic']}

**#launchpadpm-monitoring**
- {plan['channels']['launchpadpm-monitoring']['topic']}

**#launchpadpm-infrastructure**
- {plan['channels']['launchpadpm-infrastructure']['topic']}

### General Team Channels

- **#general** - General team discussions
- **#ceo-announcements** - CEO announcements and strategic updates
- **#sprint-planning** - Sprint planning sessions
- **#daily-standup** - Daily standup updates
- **#random** - Casual conversations

---

## 3. Setup Results

**Application:** {app_name}
**Workspace:** {setup_result.get('workspace', 'Unknown')}
**Workspace ID:** {setup_result.get('workspace_id', 'Unknown')}
**Total Channels:** {setup_result.get('total_channels', 0)}

### Channels Created

"""
    
    for channel_key, channel_info in setup_result.get('channels', {}).items():
        report += f"- **#{channel_info['name']}** (ID: {channel_info['id']})\n"
        report += f"  - Topic: {channel_info.get('topic', 'N/A')}\n\n"
    
    report += f"""
---

## 4. Integration Setup Guide

### CI/CD Integration

**Channels:** #launchpadpm-deployments, #launchpadpm-devops

**Notifications to Configure:**
{chr(10).join(f"- {notif}" for notif in plan['integration_setup']['ci_cd']['notifications'])}

**Implementation:**
1. Configure your CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins, etc.)
2. Add Slack webhook or use Slack API to post to channels
3. Post build start/finish, deployment status, test results

**Example Webhook URL Setup:**
- Go to Slack App Settings → Incoming Webhooks
- Enable Incoming Webhooks
- Add webhook to #launchpadpm-deployments
- Use webhook URL in CI/CD pipeline

### Monitoring Integration

**Channels:** #launchpadpm-monitoring, #launchpadpm-incidents

**Alerts to Configure:**
{chr(10).join(f"- {alert}" for alert in plan['integration_setup']['monitoring']['alerts'])}

**Implementation:**
1. Configure monitoring tool (Datadog, New Relic, CloudWatch, etc.)
2. Set up Slack integration in monitoring tool
3. Route alerts to appropriate channels:
   - Critical alerts → #launchpadpm-incidents
   - Warning alerts → #launchpadpm-monitoring

### Infrastructure Integration

**Channels:** #launchpadpm-infrastructure, #launchpadpm-devops

**Notifications to Configure:**
{chr(10).join(f"- {notif}" for notif in plan['integration_setup']['infrastructure']['notifications'])}

**Implementation:**
1. Configure infrastructure tools (Terraform Cloud, AWS, etc.)
2. Set up Slack notifications for:
   - Infrastructure changes (Terraform apply)
   - Auto-scaling events
   - Cost threshold alerts

---

## 5. Usage Guidelines

### For CEO

1. **#ceo-announcements** - Post important announcements and strategic updates
2. **#launchpadpm-dev** - Engage with development team on priorities
3. **#launchpadpm-devops** - Monitor infrastructure and deployment status

### For Development Team

1. **#launchpadpm-dev** - Technical discussions, code reviews, architecture decisions
2. **#launchpadpm-deployments** - Monitor deployment status and releases
3. **#daily-standup** - Daily progress updates

### For DevOps Team

1. **#launchpadpm-devops** - Infrastructure discussions, CI/CD pipeline management
2. **#launchpadpm-deployments** - Deployment coordination and status
3. **#launchpadpm-incidents** - Incident response and resolution
4. **#launchpadpm-monitoring** - Monitoring alerts and metrics review
5. **#launchpadpm-infrastructure** - Infrastructure changes and capacity planning

---

## 6. Next Steps

1. ✅ Slack workspace setup complete
2. ⏳ Invite team members to workspace and relevant channels
3. ⏳ Configure CI/CD pipeline integrations
4. ⏳ Set up monitoring tool integrations
5. ⏳ Configure infrastructure change notifications
6. ⏳ Set up webhook integrations for automated notifications
7. ⏳ Train team on channel purposes and usage

---

## 7. Configuration

Configuration saved to: `config/slack_config.json`

This file contains:
- Workspace ID and name
- Channel IDs and names for {app_name}
- Last update timestamp

**Note:** Keep this file secure and do not commit sensitive tokens to version control.

---

## 8. DevOps Best Practices

### Channel Naming Convention
- Application-specific channels prefixed with app name (e.g., #launchpadpm-dev)
- Clear, descriptive names
- Consistent naming across all channels

### Alert Routing
- **Critical/Incidents** → #launchpadpm-incidents
- **Warnings/Monitoring** → #launchpadpm-monitoring
- **Deployments** → #launchpadpm-deployments
- **Infrastructure Changes** → #launchpadpm-infrastructure

### Integration Principles
- All automated notifications should include context
- Use thread replies for follow-up discussions
- Set up proper alert severity levels
- Configure quiet hours for non-critical alerts

---

## 9. Support

For issues or questions:
1. Check this setup report
2. Review Slack API documentation: [https://api.slack.com](https://api.slack.com)
3. Check the integration code: `integrations/slack_integration.py`
4. Consult DevOps Engineer for integration setup

"""
    
    return report


def main():
    """Main DevOps Slack setup process"""
    app_name = "LaunchpadPM"
    
    print("=" * 70)
    print(f"DEVOPS SLACK SETUP FOR {app_name.upper()}")
    print("DevOps Engineer Configuration")
    print("=" * 70)
    
    # Check for Slack token
    api_token = os.getenv("SLACK_BOT_TOKEN")
    if not api_token:
        print("\n[ERROR] SLACK_BOT_TOKEN not set.")
        print("\nTo set up Slack integration:")
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
        print("\nExample:")
        print("  export SLACK_BOT_TOKEN='xoxb-your-token-here'")
        print("  # or on Windows:")
        print("  $env:SLACK_BOT_TOKEN='xoxb-your-token-here'")
        return
    
    print(f"\n[INFO] Setting up Slack for {app_name}...")
    print("[INFO] Initializing DevOps Engineer agent...")
    context = AgentContext()
    devops_agent = DevOpsEngineerAgent(context)
    
    print("[OK] DevOps Engineer agent initialized")
    
    # Get DevOps perspective
    print(f"\n[INFO] Getting DevOps Engineer recommendations for {app_name}...")
    devops_analysis = devops_slack_analysis(devops_agent, app_name)
    
    # Create channel configuration
    print("\n[INFO] Creating channel configuration...")
    channels_config = create_devops_channels_config(app_name, devops_analysis)
    
    # Generate setup plan
    print("\n[INFO] Generating setup plan...")
    plan = generate_devops_setup_plan(app_name, devops_analysis, channels_config)
    
    # Initialize Slack integration
    print("\n[INFO] Initializing Slack integration...")
    integration = SlackIntegration(api_token=api_token)
    
    if not integration.test_connection():
        print("[ERROR] Failed to connect to Slack. Check your token and permissions.")
        return
    
    # Set up workspace
    print(f"\n[INFO] Setting up {app_name} Slack workspace...")
    setup_result = setup_launchpadpm_slack(integration, app_name, channels_config)
    
    # Generate report
    report = generate_setup_report(app_name, devops_analysis, plan, setup_result)
    
    # Save report
    report_file = Path(__file__).parent.parent / f"{app_name.upper()}_SLACK_SETUP_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n[OK] Setup report saved to: {report_file}")
    
    print("\n" + "=" * 70)
    print(f"{app_name.upper()} SLACK SETUP COMPLETE")
    print("=" * 70)
    print(f"\nApplication: {app_name}")
    print(f"Workspace: {setup_result.get('workspace', 'Unknown')}")
    print(f"Channels created: {setup_result.get('total_channels', 0)}")
    print(f"\nReview the report: {report_file}")
    print("\nNext steps:")
    print("1. Review the setup report")
    print("2. Invite team members to the workspace")
    print("3. Configure CI/CD pipeline integrations")
    print("4. Set up monitoring tool integrations")
    print("5. Configure infrastructure change notifications")


if __name__ == "__main__":
    main()
