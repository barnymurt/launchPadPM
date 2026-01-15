"""
Telegram Integration
Handles connection to Telegram and team group management.
Enables CEO and team communication via Telegram groups.
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json

try:
    from telegram import Bot
    from telegram.error import TelegramError
    import asyncio
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    Bot = None
    asyncio = None


class TelegramClient:
    """Wrapper around Telegram Bot API client"""
    
    def __init__(self, bot_token: Optional[str] = None):
        """
        Initialize Telegram client.
        
        Args:
            bot_token: Telegram Bot Token. If None, reads from TELEGRAM_BOT_TOKEN env var.
        
        Raises:
            ImportError: If python-telegram-bot is not installed
            ValueError: If bot token is not provided
        """
        if not TELEGRAM_AVAILABLE:
            raise ImportError(
                "python-telegram-bot library is not installed. "
                "Install it with: pip install python-telegram-bot"
            )
        
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError(
                "Telegram bot token is required. "
                "Set TELEGRAM_BOT_TOKEN environment variable or pass bot_token parameter."
            )
        
        self.bot = Bot(token=self.bot_token)
        self.bot_info: Optional[Dict[str, Any]] = None
    
    def _run_async(self, coro):
        """Helper to run async coroutines"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(coro)
        finally:
            if not loop.is_closed():
                pass  # Don't close, might be reused
    
    def test_connection(self) -> bool:
        """
        Test connection to Telegram API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.bot_info = self._run_async(self.bot.get_me())
            return True
        except Exception as e:
            print(f"[ERROR] Telegram connection failed: {e}")
            return False
    
    def get_bot_info(self) -> Optional[Dict[str, Any]]:
        """
        Get bot information.
        
        Returns:
            Bot info dict or None if failed
        """
        try:
            if not self.bot_info:
                self.bot_info = self._run_async(self.bot.get_me())
            return {
                "id": self.bot_info.id,
                "username": self.bot_info.username,
                "first_name": self.bot_info.first_name,
                "is_bot": self.bot_info.is_bot
            }
        except Exception as e:
            print(f"[ERROR] Failed to get bot info: {e}")
            return None
    
    def send_message(self, chat_id: str, text: str, parse_mode: Optional[str] = "Markdown") -> bool:
        """
        Send a message to a chat.
        
        Args:
            chat_id: Chat ID (group ID or user ID)
            text: Message text
            parse_mode: Parse mode for formatting (Markdown, HTML, or None)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._run_async(self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode
            ))
            return True
        except TelegramError as e:
            print(f"[ERROR] Failed to send message: {e}")
            return False
    
    def get_chat_info(self, chat_id: str) -> Optional[Dict[str, Any]]:
        """
        Get chat information.
        
        Args:
            chat_id: Chat ID
        
        Returns:
            Chat info dict or None if failed
        """
        try:
            chat = self._run_async(self.bot.get_chat(chat_id=chat_id))
            return {
                "id": chat.id,
                "title": chat.title,
                "type": chat.type,
                "username": chat.username,
                "description": chat.description
            }
        except TelegramError as e:
            print(f"[ERROR] Failed to get chat info: {e}")
            return None
    
    def set_chat_description(self, chat_id: str, description: str) -> bool:
        """
        Set chat description.
        
        Args:
            chat_id: Chat ID
            description: Description text
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._run_async(self.bot.set_chat_description(chat_id=chat_id, description=description))
            return True
        except TelegramError as e:
            print(f"[ERROR] Failed to set chat description: {e}")
            return False
    
    def pin_message(self, chat_id: str, message_id: int) -> bool:
        """
        Pin a message in a chat.
        
        Args:
            chat_id: Chat ID
            message_id: Message ID to pin
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._run_async(self.bot.pin_chat_message(chat_id=chat_id, message_id=message_id))
            return True
        except TelegramError as e:
            print(f"[ERROR] Failed to pin message: {e}")
            return False


class TelegramIntegration:
    """
    Telegram Integration for team workspace management.
    Handles creating team groups and communication setup.
    """
    
    def __init__(self, bot_token: Optional[str] = None):
        """
        Initialize Telegram integration.
        
        Args:
            bot_token: Telegram Bot Token
        """
        self.client = TelegramClient(bot_token=bot_token)
        self.groups: Dict[str, str] = {}  # Maps group name to chat ID
        self.config_file = Path(__file__).parent.parent / "config" / "telegram_config.json"
    
    def test_connection(self) -> bool:
        """Test connection to Telegram"""
        return self.client.test_connection()
    
    def setup_team_workspace(self, workspace_name: str = "LaunchpadPM Team") -> Dict[str, Any]:
        """
        Set up team workspace with standard groups.
        
        Note: Telegram groups must be created manually. This function provides
        instructions and templates for group setup.
        
        Args:
            workspace_name: Name of the team workspace
        
        Returns:
            Dictionary with setup results and instructions
        """
        if not self.test_connection():
            raise ConnectionError("Cannot connect to Telegram API. Check your bot token.")
        
        print(f"[INFO] Setting up Telegram workspace: {workspace_name}")
        
        bot_info = self.client.get_bot_info()
        print(f"[OK] Connected as bot: @{bot_info.get('username')}")
        
        # Define standard groups (these need to be created manually in Telegram)
        groups_config = {
            "general": {
                "name": "LaunchpadPM General",
                "description": "General team discussions and announcements",
                "instructions": "Create a group called 'LaunchpadPM General' and add the bot"
            },
            "ceo-announcements": {
                "name": "LaunchpadPM CEO Announcements",
                "description": "CEO announcements, strategic updates, and important communications",
                "instructions": "Create a group called 'LaunchpadPM CEO Announcements' and add the bot"
            },
            "dev": {
                "name": "LaunchpadPM Dev",
                "description": "Development discussions, code reviews, and technical decisions",
                "instructions": "Create a group called 'LaunchpadPM Dev' and add the bot"
            },
            "devops": {
                "name": "LaunchpadPM DevOps",
                "description": "DevOps, infrastructure, deployments, and CI/CD discussions",
                "instructions": "Create a group called 'LaunchpadPM DevOps' and add the bot"
            },
            "deployments": {
                "name": "LaunchpadPM Deployments",
                "description": "Deployment status, rollouts, and release notifications",
                "instructions": "Create a group called 'LaunchpadPM Deployments' and add the bot"
            },
            "incidents": {
                "name": "LaunchpadPM Incidents",
                "description": "Production incidents, alerts, and incident response",
                "instructions": "Create a group called 'LaunchpadPM Incidents' and add the bot"
            },
            "monitoring": {
                "name": "LaunchpadPM Monitoring",
                "description": "Monitoring alerts, metrics, and observability",
                "instructions": "Create a group called 'LaunchpadPM Monitoring' and add the bot"
            },
            "sprint-planning": {
                "name": "LaunchpadPM Sprint Planning",
                "description": "Sprint planning sessions and backlog discussions",
                "instructions": "Create a group called 'LaunchpadPM Sprint Planning' and add the bot"
            },
            "daily-standup": {
                "name": "LaunchpadPM Daily Standup",
                "description": "Daily standup updates and progress tracking",
                "instructions": "Create a group called 'LaunchpadPM Daily Standup' and add the bot"
            }
        }
        
        result = {
            "bot_username": bot_info.get("username"),
            "bot_id": bot_info.get("id"),
            "groups_config": groups_config,
            "setup_instructions": self._generate_setup_instructions(groups_config, bot_info)
        }
        
        print(f"[OK] Workspace setup instructions generated!")
        return result
    
    def _generate_setup_instructions(self, groups_config: Dict, bot_info: Dict) -> str:
        """Generate setup instructions for creating Telegram groups"""
        instructions = f"""
# Telegram Group Setup Instructions

## Bot Information
- Bot Username: @{bot_info.get('username')}
- Bot ID: {bot_info.get('id')}

## Step 1: Create Groups in Telegram

For each group below, follow these steps:

1. Open Telegram
2. Click "New Group" (or "New Channel" for announcements)
3. Add team members
4. Add the bot @{bot_info.get('username')} to the group
5. Make the bot an administrator (optional, but recommended for features)
6. Set the group description as specified below

## Step 2: Get Group Chat IDs

After creating each group:

1. Send a message in the group
2. Use this URL to get the chat ID: https://api.telegram.org/bot{self.client.bot_token}/getUpdates
3. Look for "chat":{{"id":-123456789}} in the response
4. Save the chat ID (negative number for groups)

## Groups to Create

"""
        for group_key, config in groups_config.items():
            instructions += f"""
### {config['name']}
- **Description:** {config['description']}
- **Instructions:** {config['instructions']}
- **Chat ID:** (Get this after creating the group)

"""
        
        return instructions
    
    def register_group(self, group_name: str, chat_id: str, description: Optional[str] = None):
        """
        Register an existing Telegram group with the integration.
        
        Args:
            group_name: Internal group name (e.g., "general", "ceo-announcements")
            chat_id: Telegram chat ID (negative number for groups)
            description: Optional group description
        """
        self.groups[group_name] = chat_id
        if description:
            self.client.set_chat_description(chat_id=chat_id, description=description)
        self.save_config()
    
    def send_ceo_message(self, group_name: str, message: str) -> bool:
        """
        Send a message from CEO to a group.
        
        Args:
            group_name: Internal group name (e.g., "ceo-announcements")
            message: Message text
        
        Returns:
            True if successful, False otherwise
        """
        chat_id = self.groups.get(group_name)
        if not chat_id:
            print(f"[ERROR] Group '{group_name}' not registered. Use register_group() first.")
            return False
        
        return self.client.send_message(chat_id=chat_id, text=message)
    
    def create_question_thread(self, group_name: str, question: str, context: Optional[str] = None) -> bool:
        """
        Create a question thread in a group.
        
        Args:
            group_name: Internal group name
            question: Question text
            context: Optional context or additional information
        
        Returns:
            True if successful, False otherwise
        """
        message = f"❓ **Question:** {question}"
        if context:
            message += f"\n\n📋 **Context:** {context}"
        
        return self.send_ceo_message(group_name, message)
    
    def send_welcome_message(self, group_name: str = "general") -> bool:
        """Send welcome message to a group"""
        welcome_message = f"""
🚀 Welcome to LaunchpadPM Team on Telegram!

This workspace has been set up with the following groups:

📢 **CEO Announcements** - CEO announcements and strategic updates
💻 **Dev** - Development discussions and code reviews
🔧 **DevOps** - DevOps and infrastructure discussions
🚀 **Deployments** - Deployment status and releases
🚨 **Incidents** - Production incidents and alerts
📊 **Monitoring** - Monitoring alerts and metrics
📋 **Sprint Planning** - Sprint planning sessions
📊 **Daily Standup** - Daily standup updates

**Integration Points:**
- CI/CD pipelines can post to Deployments group
- Monitoring alerts should post to Monitoring and Incidents groups
- Infrastructure changes should be posted to DevOps group

Let's build LaunchpadPM together! 🚀
"""
        return self.send_ceo_message(group_name, welcome_message)
    
    def save_config(self):
        """Save Telegram configuration to file"""
        config = {
            "bot_username": self.client.bot_info.username if self.client.bot_info else None,
            "bot_id": self.client.bot_info.id if self.client.bot_info else None,
            "groups": self.groups,
            "last_updated": datetime.now().isoformat()
        }
        
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_config(self) -> Dict[str, Any]:
        """Load Telegram configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
