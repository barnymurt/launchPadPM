"""
Telegram Workspace Setup Script
Development Engineer and DevOps Engineer collaborate to set up Telegram workspace
for CEO and team communication (replacing Slack).
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
from integrations.telegram_integration import TelegramIntegration


def dev_engineer_telegram_planning(dev_agent: DevelopmentEngineerAgent) -> Dict[str, Any]:
    """Get Development Engineer's perspective on Telegram setup"""
    query = """
We're setting up Telegram for team communication instead of Slack (to avoid pro feature costs).
The CEO wants to easily communicate with the team via Telegram, and team members should be able 
to ask questions and receive instructions.

As a Development Engineer, what Telegram groups and structure would you recommend? 
What would help the development team collaborate effectively on Telegram?
"""
    
    response = dev_agent.process_query(query)
    
    return {
        "perspective": response.response,
        "recommendations": response.recommendations,
        "questions": response.questions,
        "groups_suggested": [
            "dev",
            "code-reviews",
            "technical-decisions",
            "sprint-planning"
        ]
    }


def devops_engineer_telegram_planning(devops_agent: DevOpsEngineerAgent) -> Dict[str, Any]:
    """Get DevOps Engineer's perspective on Telegram setup"""
    query = """
We're setting up Telegram for team communication instead of Slack (to avoid pro feature costs).
The CEO wants to easily communicate with the team via Telegram, and team members should be able 
to ask questions and receive instructions.

As a DevOps Engineer, what Telegram groups and integrations would you recommend? 
What would help with infrastructure, deployments, monitoring, and incident response on Telegram?
"""
    
    response = devops_agent.process_query(query)
    
    return {
        "perspective": response.response,
        "recommendations": response.recommendations,
        "questions": response.questions,
        "groups_suggested": [
            "devops",
            "deployments",
            "incidents",
            "monitoring"
        ],
        "integrations_suggested": [
            "CI/CD pipeline notifications",
            "Monitoring alerts",
            "Deployment status",
            "Incident notifications"
        ]
    }


def create_telegram_setup_plan(dev_plan: Dict, devops_plan: Dict) -> Dict[str, Any]:
    """Create comprehensive Telegram setup plan"""
    
    # Combine group suggestions
    all_groups = set()
    all_groups.update(dev_plan.get("groups_suggested", []))
    all_groups.update(devops_plan.get("groups_suggested", []))
    
    # Standard groups that should always exist
    groups_config = {
        "general": {
            "name": "LaunchpadPM General",
            "description": "General team discussions and announcements",
            "created_by": "Both"
        },
        "ceo-announcements": {
            "name": "LaunchpadPM CEO Announcements",
            "description": "CEO announcements, strategic updates, and important communications",
            "created_by": "Both"
        },
        "dev": {
            "name": "LaunchpadPM Dev",
            "description": "Development discussions, code reviews, and technical decisions",
            "created_by": "Development Engineer"
        },
        "devops": {
            "name": "LaunchpadPM DevOps",
            "description": "DevOps, infrastructure, deployments, and CI/CD discussions",
            "created_by": "DevOps Engineer"
        },
        "deployments": {
            "name": "LaunchpadPM Deployments",
            "description": "Deployment status, rollouts, and release notifications",
            "created_by": "DevOps Engineer"
        },
        "incidents": {
            "name": "LaunchpadPM Incidents",
            "description": "Production incidents, alerts, and incident response",
            "created_by": "DevOps Engineer"
        },
        "monitoring": {
            "name": "LaunchpadPM Monitoring",
            "description": "Monitoring alerts, metrics, and observability",
            "created_by": "DevOps Engineer"
        },
        "sprint-planning": {
            "name": "LaunchpadPM Sprint Planning",
            "description": "Sprint planning sessions and backlog discussions",
            "created_by": "Both"
        },
        "daily-standup": {
            "name": "LaunchpadPM Daily Standup",
            "description": "Daily standup updates and progress tracking",
            "created_by": "Both"
        }
    }
    
    plan = {
        "groups": groups_config,
        "dev_recommendations": dev_plan.get("recommendations", []),
        "devops_recommendations": devops_plan.get("recommendations", []),
        "integrations": devops_plan.get("integrations_suggested", []),
        "setup_steps": [
            "1. Create Telegram bot via @BotFather",
            "2. Get bot token",
            "3. Create Telegram groups manually",
            "4. Add bot to each group",
            "5. Get chat IDs for each group",
            "6. Register groups with integration",
            "7. Send welcome messages"
        ]
    }
    
    return plan


def generate_setup_report(app_name: str, dev_plan: Dict, devops_plan: Dict, plan: Dict, setup_result: Dict) -> str:
    """Generate comprehensive setup report"""
    
    report = f"""# {app_name} Telegram Workspace Setup Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Facilitated by:** Development Engineer & DevOps Engineer
**Platform:** Telegram (replacing Slack to avoid pro feature costs)

---

## Executive Summary

Telegram workspace has been set up for {app_name} with a focus on DevOps best practices, 
infrastructure management, monitoring, and CI/CD integration. The setup enables 
seamless communication between the CEO, development team, and operations - all without 
requiring paid Slack features.

---

## 1. Development Engineer Planning

### Perspective
{dev_plan['perspective'][:500]}...

### Key Recommendations
{chr(10).join(f"- {rec}" for rec in dev_plan['recommendations'][:6])}

### Suggested Groups
{chr(10).join(f"- {group}" for group in dev_plan.get('groups_suggested', []))}

---

## 2. DevOps Engineer Planning

### Perspective
{devops_plan['perspective'][:500]}...

### Key Recommendations
{chr(10).join(f"- {rec}" for rec in devops_plan['recommendations'][:6])}

### Suggested Groups
{chr(10).join(f"- {group}" for group in devops_plan.get('groups_suggested', []))}

### Suggested Integrations
{chr(10).join(f"- {integration}" for integration in devops_plan.get('integrations_suggested', []))}

---

## 3. Group Structure

### Development Groups

**LaunchpadPM Dev**
- {plan['groups']['dev']['description']}
- Created by: {plan['groups']['dev']['created_by']}

### DevOps Groups

**LaunchpadPM DevOps**
- {plan['groups']['devops']['description']}
- Created by: {plan['groups']['devops']['created_by']}

**LaunchpadPM Deployments**
- {plan['groups']['deployments']['description']}
- Created by: {plan['groups']['deployments']['created_by']}

**LaunchpadPM Incidents**
- {plan['groups']['incidents']['description']}
- Created by: {plan['groups']['incidents']['created_by']}

**LaunchpadPM Monitoring**
- {plan['groups']['monitoring']['description']}
- Created by: {plan['groups']['monitoring']['created_by']}

### Team Groups

- **LaunchpadPM General** - General team discussions
- **LaunchpadPM CEO Announcements** - CEO announcements
- **LaunchpadPM Sprint Planning** - Sprint planning
- **LaunchpadPM Daily Standup** - Daily standups

---

## 4. Setup Instructions

### Step 1: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow prompts to name your bot (e.g., "LaunchpadPM Bot")
4. Copy the bot token provided
5. Set environment variable:
   ```powershell
   $env:TELEGRAM_BOT_TOKEN='your-bot-token-here'
   ```

### Step 2: Create Telegram Groups

For each group listed above:

1. Open Telegram
2. Click "New Group"
3. Add team members
4. Name the group (use exact names from the list above)
5. Add the bot to the group
6. Make bot an administrator (optional but recommended)

### Step 3: Get Chat IDs

After creating groups:

1. Send a message in each group
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for `"chat":{{"id":-123456789}}` in the response
4. Save the chat ID (negative number for groups)

### Step 4: Register Groups

Use the `register_group()` method or update `config/telegram_config.json`:

```json
{{
  "groups": {{
    "general": "-123456789",
    "ceo-announcements": "-987654321",
    "dev": "-111222333",
    ...
  }}
}}
```

---

## 5. Integration Setup Guide

### CI/CD Integration

**Groups:** LaunchpadPM Deployments, LaunchpadPM DevOps

**Setup:**
1. Configure CI/CD pipeline to send HTTP requests to Telegram Bot API
2. Use endpoint: `https://api.telegram.org/bot<TOKEN>/sendMessage`
3. Post to chat_id of Deployments or DevOps group

**Example:**
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \\
  -d "chat_id=-123456789" \\
  -d "text=Deployment successful!"
```

### Monitoring Integration

**Groups:** LaunchpadPM Monitoring, LaunchpadPM Incidents

**Setup:**
1. Configure monitoring tool to send webhooks to Telegram
2. Route alerts:
   - Critical → Incidents group
   - Warnings → Monitoring group

---

## 6. Usage Guidelines

### For CEO

1. **CEO Announcements Group** - Post important announcements
2. **General Group** - Engage with the team
3. Use @mentions for specific team members

### For Team Members

1. **Dev Group** - Technical discussions
2. **DevOps Group** - Infrastructure discussions
3. **Daily Standup Group** - Progress updates
4. Use threads (reply to messages) for organized discussions

---

## 7. Advantages Over Slack

✅ **Free** - No pro feature costs
✅ **Unlimited History** - All messages stored
✅ **Better Mobile App** - Native Telegram app
✅ **File Sharing** - Up to 2GB files
✅ **Voice/Video Calls** - Built-in
✅ **No Message Limits** - Unlimited messages
✅ **Bot API** - Full-featured bot API

---

## 8. Configuration

Configuration saved to: `config/telegram_config.json`

**Bot Information:**
- Username: @{setup_result.get('bot_username', 'Unknown')}
- Bot ID: {setup_result.get('bot_id', 'Unknown')}

---

## 9. Next Steps

1. ✅ Telegram bot created
2. ⏳ Create Telegram groups manually
3. ⏳ Add bot to groups
4. ⏳ Get chat IDs
5. ⏳ Register groups with integration
6. ⏳ Configure CI/CD integrations
7. ⏳ Set up monitoring integrations

---

## 10. Support

For issues or questions:
1. Check Telegram Bot API docs: https://core.telegram.org/bots/api
2. Review integration code: `integrations/telegram_integration.py`
3. Contact @BotFather for bot issues

"""
    
    return report


def main():
    """Main Telegram setup process"""
    app_name = "LaunchpadPM"
    
    print("=" * 70)
    print(f"TELEGRAM WORKSPACE SETUP FOR {app_name.upper()}")
    print("Development Engineer & DevOps Engineer Collaboration")
    print("=" * 70)
    
    # Check for Telegram bot token
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("\n[ERROR] TELEGRAM_BOT_TOKEN not set.")
        print("\nTo set up Telegram integration:")
        print("1. Open Telegram and search for @BotFather")
        print("2. Send /newbot command")
        print("3. Follow prompts to name your bot (e.g., 'LaunchpadPM Bot')")
        print("4. Copy the bot token provided")
        print("5. Set environment variable:")
        print("   $env:TELEGRAM_BOT_TOKEN='your-bot-token-here'")
        print("\nThen run this script again.")
        return
    
    print(f"\n[INFO] Setting up Telegram for {app_name}...")
    print("[INFO] Initializing agents...")
    context = AgentContext()
    dev_agent = DevelopmentEngineerAgent(context)
    devops_agent = DevOpsEngineerAgent(context)
    
    print("[OK] Agents initialized")
    
    # Get planning from both agents
    print(f"\n[INFO] Getting Development Engineer planning for {app_name}...")
    dev_plan = dev_engineer_telegram_planning(dev_agent)
    
    print(f"[INFO] Getting DevOps Engineer planning for {app_name}...")
    devops_plan = devops_engineer_telegram_planning(devops_agent)
    
    # Create setup plan
    print("\n[INFO] Creating setup plan...")
    plan = create_telegram_setup_plan(dev_plan, devops_plan)
    
    # Initialize Telegram integration
    print("\n[INFO] Initializing Telegram integration...")
    integration = TelegramIntegration(bot_token=bot_token)
    
    if not integration.test_connection():
        print("[ERROR] Failed to connect to Telegram. Check your bot token.")
        return
    
    # Set up workspace (generates instructions)
    print(f"\n[INFO] Setting up {app_name} Telegram workspace...")
    setup_result = integration.setup_team_workspace("LaunchpadPM Team")
    
    # Generate report
    report = generate_setup_report(app_name, dev_plan, devops_plan, plan, setup_result)
    
    # Save report
    report_file = Path(__file__).parent.parent / f"{app_name.upper()}_TELEGRAM_SETUP_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n[OK] Setup report saved to: {report_file}")
    
    # Print setup instructions
    print("\n" + "=" * 70)
    print("SETUP INSTRUCTIONS")
    print("=" * 70)
    print(setup_result.get("setup_instructions", ""))
    
    print("\n" + "=" * 70)
    print(f"{app_name.upper()} TELEGRAM SETUP COMPLETE")
    print("=" * 70)
    print(f"\nBot Username: @{setup_result.get('bot_username', 'Unknown')}")
    print(f"Bot ID: {setup_result.get('bot_id', 'Unknown')}")
    print(f"\nReview the report: {report_file}")
    print("\nNext steps:")
    print("1. Create Telegram groups manually (see instructions above)")
    print("2. Add bot to each group")
    print("3. Get chat IDs and register groups")
    print("4. Configure CI/CD and monitoring integrations")


if __name__ == "__main__":
    main()
