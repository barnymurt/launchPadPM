"""
Register Telegram Groups Script
Helper script to register Telegram groups with chat IDs after they're created.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.telegram_integration import TelegramIntegration


def main():
    """Register Telegram groups with their chat IDs"""
    
    print("=" * 70)
    print("REGISTER TELEGRAM GROUPS")
    print("=" * 70)
    
    # Check for Telegram bot token
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("\n[ERROR] TELEGRAM_BOT_TOKEN not set.")
        print("Set it with: $env:TELEGRAM_BOT_TOKEN='your-token'")
        return
    
    # Initialize integration
    print("\n[INFO] Initializing Telegram integration...")
    integration = TelegramIntegration(bot_token=bot_token)
    
    if not integration.test_connection():
        print("[ERROR] Failed to connect to Telegram. Check your bot token.")
        return
    
    bot_info = integration.client.get_bot_info()
    print(f"[OK] Connected as bot: @{bot_info.get('username')}")
    
    print("\n" + "=" * 70)
    print("HOW TO GET CHAT IDs")
    print("=" * 70)
    print("\n1. Create a Telegram group (or use an existing one)")
    print("2. Add the bot @{} to the group".format(bot_info.get('username')))
    print("3. Send a message in the group")
    print("4. Visit this URL in your browser:")
    print(f"   https://api.telegram.org/bot{bot_token}/getUpdates")
    print("5. Look for 'chat':{'id':-123456789} in the JSON response")
    print("6. Copy the chat ID (it will be a negative number for groups)")
    print("\n" + "=" * 70)
    
    # Group registration
    groups_to_register = {
        "general": {
            "name": "LaunchpadPM General",
            "description": "General team discussions and announcements"
        },
        "ceo-announcements": {
            "name": "LaunchpadPM CEO Announcements",
            "description": "CEO announcements, strategic updates, and important communications"
        },
        "dev": {
            "name": "LaunchpadPM Dev",
            "description": "Development discussions, code reviews, and technical decisions"
        },
        "devops": {
            "name": "LaunchpadPM DevOps",
            "description": "DevOps, infrastructure, deployments, and CI/CD discussions"
        },
        "deployments": {
            "name": "LaunchpadPM Deployments",
            "description": "Deployment status, rollouts, and release notifications"
        },
        "incidents": {
            "name": "LaunchpadPM Incidents",
            "description": "Production incidents, alerts, and incident response"
        },
        "monitoring": {
            "name": "LaunchpadPM Monitoring",
            "description": "Monitoring alerts, metrics, and observability"
        },
        "sprint-planning": {
            "name": "LaunchpadPM Sprint Planning",
            "description": "Sprint planning sessions and backlog discussions"
        },
        "daily-standup": {
            "name": "LaunchpadPM Daily Standup",
            "description": "Daily standup updates and progress tracking"
        }
    }
    
    print("\n[INFO] Register groups with their chat IDs")
    print("Enter chat IDs for each group (or press Enter to skip):\n")
    
    registered = 0
    for group_key, group_info in groups_to_register.items():
        chat_id = input(f"Chat ID for '{group_info['name']}': ").strip()
        
        if chat_id:
            try:
                # Validate chat ID format
                chat_id_int = int(chat_id)
                integration.register_group(
                    group_name=group_key,
                    chat_id=chat_id,
                    description=group_info['description']
                )
                print(f"[OK] Registered {group_info['name']} with chat ID: {chat_id}")
                registered += 1
            except ValueError:
                print(f"[ERROR] Invalid chat ID format: {chat_id}")
            except Exception as e:
                print(f"[ERROR] Failed to register {group_info['name']}: {e}")
        else:
            print(f"[SKIP] Skipped {group_info['name']}")
    
    print(f"\n[OK] Registered {registered} groups")
    print(f"[INFO] Configuration saved to: {integration.config_file}")
    
    if registered > 0:
        print("\n[INFO] You can now use the integration to send messages:")
        print("  from integrations.telegram_integration import TelegramIntegration")
        print("  integration = TelegramIntegration(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'))")
        print("  integration.send_ceo_message('ceo-announcements', 'Hello team!')")


if __name__ == "__main__":
    main()
