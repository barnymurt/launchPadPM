"""
Slack Integration
Handles connection to Slack and team workspace management.
Enables CEO and team communication via Slack channels.
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False
    WebClient = None


class SlackClient:
    """Wrapper around Slack API client"""
    
    def __init__(self, api_token: Optional[str] = None, refresh_token: Optional[str] = None):
        """
        Initialize Slack client.
        
        Args:
            api_token: Slack Bot User OAuth Token (xoxb-) or OAuth Access Token (xoxe.xoxp-).
                       If None, reads from SLACK_BOT_TOKEN or SLACK_ACCESS_TOKEN env var.
            refresh_token: OAuth Refresh Token (xoxe-1-). If None, reads from SLACK_REFRESH_TOKEN env var.
        
        Raises:
            ImportError: If slack-sdk is not installed
            ValueError: If API token is not provided
        """
        if not SLACK_AVAILABLE:
            raise ImportError(
                "slack-sdk library is not installed. "
                "Install it with: pip install slack-sdk"
            )
        
        # Try to get token from parameter, then environment variables
        self.api_token = api_token or os.getenv("SLACK_BOT_TOKEN") or os.getenv("SLACK_ACCESS_TOKEN")
        self.refresh_token = refresh_token or os.getenv("SLACK_REFRESH_TOKEN")
        
        if not self.api_token:
            raise ValueError(
                "Slack API token is required. "
                "Set SLACK_BOT_TOKEN or SLACK_ACCESS_TOKEN environment variable or pass api_token parameter."
            )
        
        # Initialize client with token
        self.client = WebClient(token=self.api_token)
        self.workspace_id: Optional[str] = None
        self.workspace_name: Optional[str] = None
    
    def test_connection(self) -> bool:
        """
        Test connection to Slack API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.client.auth_test()
            self.workspace_id = response.get("team_id")
            self.workspace_name = response.get("team")
            return True
        except Exception as e:
            print(f"[ERROR] Slack connection failed: {e}")
            return False
    
    def get_workspace_info(self) -> Optional[Dict[str, Any]]:
        """
        Get workspace information.
        
        Returns:
            Workspace info dict or None if failed
        """
        try:
            response = self.client.auth_test()
            return {
                "team_id": response.get("team_id"),
                "team": response.get("team"),
                "user_id": response.get("user_id"),
                "user": response.get("user"),
                "bot_id": response.get("bot_id")
            }
        except Exception as e:
            print(f"[ERROR] Failed to get workspace info: {e}")
            return None
    
    def list_channels(self, types: str = "public_channel,private_channel") -> List[Dict[str, Any]]:
        """
        List channels in the workspace.
        
        Args:
            types: Comma-separated list of channel types (public_channel, private_channel, mpim, im)
        
        Returns:
            List of channel objects
        """
        try:
            response = self.client.conversations_list(types=types)
            return response.get("channels", [])
        except SlackApiError as e:
            print(f"[ERROR] Failed to list channels: {e}")
            return []
    
    def create_channel(self, name: str, is_private: bool = False) -> Optional[Dict[str, Any]]:
        """
        Create a new channel.
        
        Args:
            name: Channel name (lowercase, no spaces, max 80 chars)
            is_private: Whether channel should be private
        
        Returns:
            Channel object or None if failed
        """
        try:
            response = self.client.conversations_create(
                name=name,
                is_private=is_private
            )
            return response.get("channel")
        except SlackApiError as e:
            if e.response.get("error") == "name_taken":
                # Channel already exists, try to get it
                channels = self.list_channels()
                for channel in channels:
                    if channel.get("name") == name:
                        return channel
            print(f"[ERROR] Failed to create channel '{name}': {e}")
            return None
    
    def get_or_create_channel(self, name: str, is_private: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get existing channel or create if it doesn't exist.
        
        Args:
            name: Channel name
            is_private: Whether channel should be private
        
        Returns:
            Channel object or None if failed
        """
        # Check if channel exists
        channels = self.list_channels()
        for channel in channels:
            if channel.get("name") == name:
                return channel
        
        # Create if doesn't exist
        return self.create_channel(name, is_private)
    
    def send_message(self, channel: str, text: str, blocks: Optional[List[Dict]] = None) -> bool:
        """
        Send a message to a channel.
        
        Args:
            channel: Channel ID or name (with # prefix)
            text: Message text
            blocks: Optional Slack Block Kit blocks for rich formatting
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove # prefix if present
            if channel.startswith("#"):
                channel = channel[1:]
            
            # Get channel ID if name provided
            if not channel.startswith("C"):
                channels = self.list_channels()
                for ch in channels:
                    if ch.get("name") == channel:
                        channel = ch.get("id")
                        break
            
            response = self.client.chat_postMessage(
                channel=channel,
                text=text,
                blocks=blocks
            )
            return response.get("ok", False)
        except SlackApiError as e:
            print(f"[ERROR] Failed to send message: {e}")
            return False
    
    def set_channel_topic(self, channel: str, topic: str) -> bool:
        """
        Set channel topic.
        
        Args:
            channel: Channel ID or name
            topic: Topic text
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove # prefix if present
            if channel.startswith("#"):
                channel = channel[1:]
            
            # Get channel ID if name provided
            if not channel.startswith("C"):
                channels = self.list_channels()
                for ch in channels:
                    if ch.get("name") == channel:
                        channel = ch.get("id")
                        break
            
            response = self.client.conversations_setTopic(
                channel=channel,
                topic=topic
            )
            return response.get("ok", False)
        except SlackApiError as e:
            print(f"[ERROR] Failed to set channel topic: {e}")
            return False
    
    def invite_users_to_channel(self, channel: str, users: List[str]) -> bool:
        """
        Invite users to a channel.
        
        Args:
            channel: Channel ID or name
            users: List of user IDs to invite
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove # prefix if present
            if channel.startswith("#"):
                channel = channel[1:]
            
            # Get channel ID if name provided
            if not channel.startswith("C"):
                channels = self.list_channels()
                for ch in channels:
                    if ch.get("name") == channel:
                        channel = ch.get("id")
                        break
            
            response = self.client.conversations_invite(
                channel=channel,
                users=users
            )
            return response.get("ok", False)
        except SlackApiError as e:
            print(f"[ERROR] Failed to invite users: {e}")
            return False


class SlackIntegration:
    """
    Slack Integration for team workspace management.
    Handles creating team channels and communication setup.
    """
    
    def __init__(self, api_token: Optional[str] = None, refresh_token: Optional[str] = None):
        """
        Initialize Slack integration.
        
        Args:
            api_token: Slack Bot User OAuth Token (xoxb-) or OAuth Access Token (xoxe.xoxp-)
            refresh_token: OAuth Refresh Token (xoxe-1-), optional
        """
        self.client = SlackClient(api_token=api_token)
        self.refresh_token = refresh_token
        self.channels: Dict[str, str] = {}  # Maps channel name to ID
        self.config_file = Path(__file__).parent.parent / "config" / "slack_config.json"
    
    def test_connection(self) -> bool:
        """Test connection to Slack"""
        return self.client.test_connection()
    
    def setup_team_workspace(self, workspace_name: str = "Product Team") -> Dict[str, Any]:
        """
        Set up team workspace with standard channels.
        
        Args:
            workspace_name: Name of the team workspace
        
        Returns:
            Dictionary with setup results
        """
        if not self.test_connection():
            raise ConnectionError("Cannot connect to Slack API. Check your API token.")
        
        print(f"[INFO] Setting up Slack workspace: {workspace_name}")
        
        workspace_info = self.client.get_workspace_info()
        print(f"[INFO] Connected to workspace: {workspace_info.get('team')}")
        
        # Define standard channels
        channels_config = {
            "general": {
                "name": "general",
                "topic": "General team discussions and announcements",
                "is_private": False
            },
            "ceo-announcements": {
                "name": "ceo-announcements",
                "topic": "CEO announcements, strategic updates, and important communications",
                "is_private": False
            },
            "product-team": {
                "name": "product-team",
                "topic": "Product team discussions, sprint planning, and daily standups",
                "is_private": False
            },
            "dev-engineering": {
                "name": "dev-engineering",
                "topic": "Development engineering discussions, code reviews, technical decisions",
                "is_private": False
            },
            "devops-infrastructure": {
                "name": "devops-infrastructure",
                "topic": "DevOps, infrastructure, deployments, and CI/CD discussions",
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
            "incidents": {
                "name": "incidents",
                "topic": "Production incidents, alerts, and incident response",
                "is_private": False
            },
            "random": {
                "name": "random",
                "topic": "Non-work banter, team building, and casual conversations",
                "is_private": False
            }
        }
        
        created_channels = {}
        existing_channels = {}
        
        # Create or get channels
        for channel_key, config in channels_config.items():
            print(f"[INFO] Setting up channel: #{config['name']}")
            channel = self.client.get_or_create_channel(
                name=config["name"],
                is_private=config["is_private"]
            )
            
            if channel:
                channel_id = channel.get("id")
                self.channels[config["name"]] = channel_id
                
                # Set channel topic
                self.client.set_channel_topic(channel_id, config["topic"])
                
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
🎉 Welcome to the {workspace_name} Slack workspace!

This workspace has been set up with the following channels:

📢 **#ceo-announcements** - CEO announcements and strategic updates
👥 **#product-team** - Product team discussions and sprint activities
💻 **#dev-engineering** - Development engineering discussions
🔧 **#devops-infrastructure** - DevOps and infrastructure discussions
📋 **#sprint-planning** - Sprint planning sessions
📊 **#daily-standup** - Daily standup updates
🚨 **#incidents** - Production incidents and alerts
💬 **#random** - Casual conversations

Feel free to explore and start collaborating!
"""
            self.client.send_message(
                channel=created_channels["general"]["id"],
                text=welcome_message
            )
        
        # Save configuration
        self.save_config()
        
        result = {
            "workspace": workspace_info.get("team"),
            "workspace_id": workspace_info.get("team_id"),
            "channels": created_channels,
            "existing_channels": existing_channels,
            "total_channels": len(created_channels) + len(existing_channels)
        }
        
        print(f"[OK] Workspace setup complete! Created {len(created_channels)} channels")
        return result
    
    def save_config(self):
        """Save Slack configuration to file"""
        config = {
            "workspace_id": self.client.workspace_id,
            "workspace_name": self.client.workspace_name,
            "channels": self.channels,
            "last_updated": datetime.now().isoformat()
        }
        
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_config(self) -> Dict[str, Any]:
        """Load Slack configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def send_ceo_message(self, channel: str, message: str) -> bool:
        """
        Send a message from CEO to a channel.
        
        Args:
            channel: Channel name or ID
            message: Message text
        
        Returns:
            True if successful, False otherwise
        """
        return self.client.send_message(channel=channel, text=message)
    
    def create_question_thread(self, channel: str, question: str, context: Optional[str] = None) -> Optional[str]:
        """
        Create a question thread in a channel.
        
        Args:
            channel: Channel name or ID
            question: Question text
            context: Optional context or additional information
        
        Returns:
            Thread timestamp if successful, None otherwise
        """
        message = f"❓ **Question:** {question}"
        if context:
            message += f"\n\n📋 **Context:** {context}"
        
        # Send initial message
        if self.client.send_message(channel=channel, text=message):
            # Return a placeholder timestamp (in real implementation, would get from response)
            return datetime.now().isoformat()
        return None
