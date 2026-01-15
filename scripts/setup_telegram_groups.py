"""
Telegram Groups Setup Script
Automatically gets chat IDs and registers groups with the integration.
"""

import sys
import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.telegram_integration import TelegramIntegration


def get_updates(bot_token: str) -> List[Dict[str, Any]]:
    """Get recent updates from Telegram Bot API"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("ok"):
            return data.get("result", [])
        return []
    except Exception as e:
        print(f"[ERROR] Failed to get updates: {e}")
        return []


def extract_chat_ids(updates: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Extract chat IDs and group names from updates"""
    chat_ids = {}
    
    for update in updates:
        if "message" in update:
            message = update["message"]
            if "chat" in message:
                chat = message["chat"]
                chat_id = str(chat.get("id"))
                chat_title = chat.get("title", "")
                chat_type = chat.get("type", "")
                
                if chat_type in ["group", "supergroup"]:
                    if chat_id not in chat_ids:
                        chat_ids[chat_id] = {
                            "id": chat_id,
                            "title": chat_title,
                            "type": chat_type
                        }
    
    return chat_ids


def match_groups_to_config(found_chats: Dict[str, Dict], expected_groups: Dict[str, Dict]) -> Dict[str, str]:
    """Match found Telegram groups to expected group configuration"""
    matches = {}
    
    for chat_id, chat_info in found_chats.items():
        chat_title = chat_info.get("title", "").lower()
        
        # Try to match by name
        for group_key, group_config in expected_groups.items():
            expected_name = group_config["name"].lower()
            
            # Check if chat title contains key words from expected name
            if "launchpadpm" in chat_title:
                # Extract the group type
                if "general" in chat_title or "general" in expected_name:
                    if "general" in chat_title and "general" in expected_name:
                        matches[group_key] = chat_id
                        break
                elif "ceo" in chat_title or "announcement" in chat_title:
                    if "ceo" in expected_name or "announcement" in expected_name:
                        matches["ceo-announcements"] = chat_id
                        break
                elif "dev" in chat_title and "devops" not in chat_title:
                    if "dev" in expected_name and "devops" not in expected_name:
                        matches["dev"] = chat_id
                        break
                elif "devops" in chat_title:
                    if "devops" in expected_name:
                        matches["devops"] = chat_id
                        break
                elif "deployment" in chat_title:
                    if "deployment" in expected_name:
                        matches["deployments"] = chat_id
                        break
                elif "incident" in chat_title:
                    if "incident" in expected_name:
                        matches["incidents"] = chat_id
                        break
                elif "monitor" in chat_title:
                    if "monitor" in expected_name:
                        matches["monitoring"] = chat_id
                        break
                elif "sprint" in chat_title and "plan" in chat_title:
                    if "sprint" in expected_name and "plan" in expected_name:
                        matches["sprint-planning"] = chat_id
                        break
                elif "standup" in chat_title or "stand-up" in chat_title:
                    if "standup" in expected_name or "stand-up" in expected_name:
                        matches["daily-standup"] = chat_id
                        break
    
    return matches


def main():
    """Main setup process"""
    print("=" * 70)
    print("TELEGRAM GROUPS SETUP & REGISTRATION")
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
    
    # Expected groups configuration
    expected_groups = {
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
    
    print("\n" + "=" * 70)
    print("STEP 1: CREATE GROUPS IN TELEGRAM")
    print("=" * 70)
    print("\nPlease create the following groups in Telegram:")
    print("(Make sure to add the bot @{} to each group)\n".format(bot_info.get('username')))
    
    for group_key, group_info in expected_groups.items():
        print(f"  • {group_info['name']}")
        print(f"    {group_info['description']}")
    
    print("\n" + "=" * 70)
    print("STEP 2: GET CHAT IDs")
    print("=" * 70)
    print("\nAfter creating groups and adding the bot:")
    print("1. Send a message in each group")
    print("2. Press Enter here to fetch chat IDs from Telegram API...")
    input()
    
    print("\n[INFO] Fetching updates from Telegram API...")
    updates = get_updates(bot_token)
    
    if not updates:
        print("[WARNING] No updates found. Make sure:")
        print("  1. Groups are created")
        print("  2. Bot is added to each group")
        print("  3. At least one message was sent in each group")
        print("\nYou can also manually get chat IDs by visiting:")
        print(f"   https://api.telegram.org/bot{bot_token}/getUpdates")
        return
    
    print(f"[OK] Found {len(updates)} updates")
    
    # Extract chat IDs
    found_chats = extract_chat_ids(updates)
    print(f"[OK] Found {len(found_chats)} groups/chats")
    
    if found_chats:
        print("\n[INFO] Found groups:")
        for chat_id, chat_info in found_chats.items():
            print(f"  • {chat_info['title']} (ID: {chat_id})")
    
    # Match groups to configuration
    print("\n[INFO] Matching groups to configuration...")
    matches = match_groups_to_config(found_chats, expected_groups)
    
    if matches:
        print(f"[OK] Matched {len(matches)} groups:")
        for group_key, chat_id in matches.items():
            group_name = expected_groups[group_key]["name"]
            print(f"  • {group_name} → {chat_id}")
    
    # Register matched groups
    print("\n" + "=" * 70)
    print("STEP 3: REGISTER GROUPS")
    print("=" * 70)
    
    if matches:
        print(f"\n[INFO] Registering {len(matches)} groups...")
        registered = 0
        
        for group_key, chat_id in matches.items():
            group_info = expected_groups[group_key]
            try:
                integration.register_group(
                    group_name=group_key,
                    chat_id=chat_id,
                    description=group_info["description"]
                )
                print(f"[OK] Registered: {group_info['name']} ({chat_id})")
                registered += 1
            except Exception as e:
                print(f"[ERROR] Failed to register {group_info['name']}: {e}")
        
        print(f"\n[OK] Successfully registered {registered} groups")
    else:
        print("\n[WARNING] No groups matched automatically.")
        print("You can register groups manually:")
        print("  1. Get chat IDs from: https://api.telegram.org/bot{}/getUpdates".format(bot_token))
        print("  2. Run: python scripts/register_telegram_groups.py")
        print("  3. Enter chat IDs when prompted")
    
    # Check for missing groups
    missing = set(expected_groups.keys()) - set(matches.keys())
    if missing:
        print(f"\n[INFO] {len(missing)} groups not yet registered:")
        for group_key in missing:
            group_name = expected_groups[group_key]["name"]
            print(f"  • {group_name}")
        print("\nTo register manually:")
        print("  python scripts/register_telegram_groups.py")
    
    # Send welcome message to general group if registered
    if "general" in matches:
        print("\n[INFO] Sending welcome message to General group...")
        if integration.send_welcome_message("general"):
            print("[OK] Welcome message sent!")
        else:
            print("[WARNING] Failed to send welcome message")
    
    print("\n" + "=" * 70)
    print("SETUP COMPLETE")
    print("=" * 70)
    print(f"\nConfiguration saved to: {integration.config_file}")
    print("\nYou can now use the integration:")
    print("  from integrations.telegram_integration import TelegramIntegration")
    print("  integration = TelegramIntegration(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'))")
    print("  integration.send_ceo_message('ceo-announcements', 'Hello team!')")


if __name__ == "__main__":
    main()
