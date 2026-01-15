"""
Auto Register Telegram Groups
Automatically fetches chat IDs and registers groups.
"""

import sys
import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Any

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


def match_groups(found_chats: Dict[str, Dict], expected_groups: Dict[str, Dict]) -> Dict[str, str]:
    """Match found Telegram groups to expected group configuration"""
    matches = {}
    
    # Create mapping keywords
    keywords_map = {
        "general": ["general"],
        "ceo-announcements": ["ceo", "announcement"],
        "dev": ["dev", "development"],
        "devops": ["devops", "dev ops"],
        "deployments": ["deployment", "deploy"],
        "incidents": ["incident"],
        "monitoring": ["monitor", "alert"],
        "sprint-planning": ["sprint", "planning", "plan"],
        "daily-standup": ["standup", "stand-up", "daily"]
    }
    
    for chat_id, chat_info in found_chats.items():
        chat_title = chat_info.get("title", "").lower()
        
        # Only process LaunchpadPM groups
        if "launchpadpm" not in chat_title:
            continue
        
        # Try to match by keywords
        best_match = None
        best_score = 0
        
        for group_key, keywords in keywords_map.items():
            score = sum(1 for keyword in keywords if keyword in chat_title)
            if score > best_score:
                best_score = score
                best_match = group_key
        
        if best_match and best_match not in matches:
            matches[best_match] = chat_id
    
    return matches


def main():
    """Main auto-registration process"""
    print("=" * 70)
    print("AUTO REGISTER TELEGRAM GROUPS")
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
    print("FETCHING CHAT IDs FROM TELEGRAM API")
    print("=" * 70)
    print("\n[INFO] Fetching updates...")
    print("[NOTE] Make sure you've:")
    print("  1. Created the groups in Telegram")
    print("  2. Added the bot @{} to each group".format(bot_info.get('username')))
    print("  3. Sent at least one message in each group")
    
    updates = get_updates(bot_token)
    
    if not updates:
        print("\n[WARNING] No updates found.")
        print("\nTo get chat IDs manually:")
        print("  1. Send a message in each group")
        print("  2. Visit: https://api.telegram.org/bot{}/getUpdates".format(bot_token))
        print("  3. Look for 'chat':{'id':-123456789} in the JSON")
        print("  4. Run: python scripts/register_telegram_groups.py")
        return
    
    print(f"[OK] Found {len(updates)} updates")
    
    # Extract chat IDs
    found_chats = extract_chat_ids(updates)
    print(f"[OK] Found {len(found_chats)} groups/chats")
    
    if found_chats:
        print("\n[INFO] Groups found:")
        for chat_id, chat_info in found_chats.items():
            print(f"  • {chat_info['title']} (ID: {chat_id})")
    
    # Match groups to configuration
    print("\n[INFO] Matching groups to configuration...")
    matches = match_groups(found_chats, expected_groups)
    
    if matches:
        print(f"[OK] Matched {len(matches)} groups:")
        for group_key, chat_id in matches.items():
            group_name = expected_groups[group_key]["name"]
            print(f"  • {group_name} → {chat_id}")
    else:
        print("[WARNING] No groups matched automatically.")
        if found_chats:
            print("\nFound groups (manual matching needed):")
            for chat_id, chat_info in found_chats.items():
                print(f"  • {chat_info['title']} (ID: {chat_id})")
    
    # Register matched groups
    print("\n" + "=" * 70)
    print("REGISTERING GROUPS")
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
        
        # Send welcome message to general group if registered
        if "general" in matches:
            print("\n[INFO] Sending welcome message to General group...")
            if integration.send_welcome_message("general"):
                print("[OK] Welcome message sent!")
            else:
                print("[WARNING] Failed to send welcome message")
    else:
        print("\n[INFO] No groups to register automatically.")
        print("You can register manually using:")
        print("  python scripts/register_telegram_groups.py")
    
    # Check for missing groups
    missing = set(expected_groups.keys()) - set(matches.keys())
    if missing:
        print(f"\n[INFO] {len(missing)} groups not yet registered:")
        for group_key in missing:
            group_name = expected_groups[group_key]["name"]
            print(f"  • {group_name}")
        print("\nTo register these groups:")
        print("  1. Create them in Telegram")
        print("  2. Add bot to each group")
        print("  3. Send a message in each group")
        print("  4. Run this script again")
    
    print("\n" + "=" * 70)
    print("REGISTRATION COMPLETE")
    print("=" * 70)
    print(f"\nConfiguration saved to: {integration.config_file}")
    
    if matches:
        print("\n[OK] Integration is ready to use!")
        print("\nExample usage:")
        print("  from integrations.telegram_integration import TelegramIntegration")
        print("  import os")
        print("  integration = TelegramIntegration(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'))")
        print("  integration.send_ceo_message('ceo-announcements', 'Hello team!')")


if __name__ == "__main__":
    main()
