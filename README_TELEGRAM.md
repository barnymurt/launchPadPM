# Telegram Integration Setup Guide

This guide explains how to set up Telegram integration for team communication, replacing Slack to avoid pro feature costs. The CEO and team members can communicate effectively via Telegram groups.

## Overview

The Telegram integration provides:
- **Team Communication Groups** - Organized groups for different aspects of team collaboration
- **CEO Communication** - Dedicated group for CEO announcements and strategic updates
- **Question & Answer** - Easy way for team members to ask questions and receive instructions
- **Free Platform** - No pro feature costs, unlimited messages and history
- **Integration Ready** - Setup for CI/CD, monitoring, and other tool integrations

## Advantages Over Slack

✅ **Free** - No pro feature costs  
✅ **Unlimited History** - All messages stored forever  
✅ **Better Mobile App** - Native Telegram app  
✅ **File Sharing** - Up to 2GB files  
✅ **Voice/Video Calls** - Built-in  
✅ **No Message Limits** - Unlimited messages  
✅ **Bot API** - Full-featured bot API  

## Prerequisites

1. **Telegram Account** - You need a Telegram account
2. **Telegram Bot Creation** - Create a bot via @BotFather
3. **Python Dependencies** - Install required packages

## Step 1: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow prompts:
   - Enter bot name (e.g., "LaunchpadPM Bot")
   - Enter bot username (e.g., "LaunchpadPM_bot")
4. Copy the bot token provided (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Save the token securely

## Step 2: Set Environment Variable

### Windows (PowerShell)
```powershell
$env:TELEGRAM_BOT_TOKEN='your-bot-token-here'
```

### Linux/Mac
```bash
export TELEGRAM_BOT_TOKEN='your-bot-token-here'
```

### Permanent Setup (Optional)

Create a `.env` file in the project root:
```
TELEGRAM_BOT_TOKEN=your-bot-token-here
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `python-telegram-bot>=20.0` along with other dependencies.

## Step 4: Run Setup Script

```bash
python scripts/setup_telegram_workspace.py
```

The script will:
1. Test Telegram Bot API connection
2. Get recommendations from Development Engineer and DevOps Engineer agents
3. Generate setup instructions for creating groups
4. Generate setup report

## Step 5: Create Telegram Groups

The script will provide detailed instructions. For each group:

1. Open Telegram
2. Click "New Group"
3. Add team members
4. Name the group (use exact names from the setup report)
5. Add the bot to the group
6. Make bot an administrator (optional but recommended)

### Groups to Create

- **LaunchpadPM General** - General team discussions
- **LaunchpadPM CEO Announcements** - CEO announcements and strategic updates
- **LaunchpadPM Dev** - Development discussions and code reviews
- **LaunchpadPM DevOps** - DevOps and infrastructure discussions
- **LaunchpadPM Deployments** - Deployment status and releases
- **LaunchpadPM Incidents** - Production incidents and alerts
- **LaunchpadPM Monitoring** - Monitoring alerts and metrics
- **LaunchpadPM Sprint Planning** - Sprint planning sessions
- **LaunchpadPM Daily Standup** - Daily standup updates

## Step 6: Get Chat IDs

After creating groups:

1. Send a message in each group
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for `"chat":{"id":-123456789}` in the response
4. Save the chat ID (negative number for groups)

## Step 7: Register Groups

Update `config/telegram_config.json` with chat IDs:

```json
{
  "bot_username": "LaunchpadPM_bot",
  "bot_id": 123456789,
  "groups": {
    "general": "-123456789",
    "ceo-announcements": "-987654321",
    "dev": "-111222333",
    "devops": "-444555666",
    "deployments": "-777888999",
    "incidents": "-111222333",
    "monitoring": "-444555666",
    "sprint-planning": "-777888999",
    "daily-standup": "-111222333"
  },
  "last_updated": "2024-01-14T12:00:00"
}
```

Or use the Python API:

```python
from integrations.telegram_integration import TelegramIntegration
import os

integration = TelegramIntegration(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))
integration.register_group("general", "-123456789", "General team discussions")
integration.register_group("ceo-announcements", "-987654321", "CEO announcements")
# ... etc
```

## Usage

### For CEO

1. **Post Announcements** - Use "LaunchpadPM CEO Announcements" group
2. **Engage with Team** - Use "LaunchpadPM General" or specific groups
3. **Ask Questions** - Post questions in appropriate groups

### For Team Members

1. **Ask Questions** - Use appropriate groups:
   - Technical questions → LaunchpadPM Dev
   - Infrastructure questions → LaunchpadPM DevOps
   - Product questions → LaunchpadPM General
   - General questions → LaunchpadPM General

2. **Share Updates** - Use "LaunchpadPM Daily Standup" for daily progress

3. **Report Issues** - Use "LaunchpadPM Incidents" for production issues

## Integration with Python Code

### Basic Usage

```python
from integrations.telegram_integration import TelegramIntegration
import os

# Initialize integration
integration = TelegramIntegration(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))

# Test connection
if integration.test_connection():
    print("Connected to Telegram!")

# Send a message
integration.send_ceo_message(
    group_name="ceo-announcements",
    message="Important announcement: New product launch next week!"
)

# Create a question thread
integration.create_question_thread(
    group_name="dev",
    question="What's the priority for this sprint?",
    context="We need to decide between feature A and feature B"
)
```

### Using the Telegram Client Directly

```python
from integrations.telegram_integration import TelegramClient

client = TelegramClient(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))

# Send a message
client.send_message(
    chat_id="-123456789",
    text="Hello team! 👋"
)

# Get chat info
chat_info = client.get_chat_info(chat_id="-123456789")
print(f"Group: {chat_info['title']}")
```

## CI/CD Integration

### Setup Webhook

Configure your CI/CD pipeline to send messages to Telegram:

```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=-123456789" \
  -d "text=Deployment successful! 🚀"
```

### GitHub Actions Example

```yaml
- name: Notify Telegram
  run: |
    curl -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
      -d "chat_id=${{ secrets.TELEGRAM_DEPLOYMENTS_CHAT_ID }}" \
      -d "text=✅ Deployment successful!"
```

## Monitoring Integration

### Setup Alerts

Configure monitoring tools to send alerts to Telegram:

```python
import requests

def send_alert(message, chat_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": f"🚨 Alert: {message}"
    }
    requests.post(url, data=data)
```

## Configuration

Configuration is saved to `config/telegram_config.json`:

```json
{
  "bot_username": "LaunchpadPM_bot",
  "bot_id": 123456789,
  "groups": {
    "general": "-123456789",
    "ceo-announcements": "-987654321",
    ...
  },
  "last_updated": "2024-01-14T12:00:00"
}
```

## Troubleshooting

### Connection Failed

**Error:** `Telegram connection failed`

**Solutions:**
1. Verify your `TELEGRAM_BOT_TOKEN` is set correctly
2. Check that the token is valid (get new one from @BotFather if needed)
3. Ensure bot is not deleted or disabled

### Bot Not Responding

**Error:** Bot doesn't respond in groups

**Solutions:**
1. Make sure bot is added to the group
2. Check that bot has permission to send messages
3. Make bot an administrator for full features

### Chat ID Not Found

**Error:** `Group 'group_name' not registered`

**Solutions:**
1. Get the chat ID using getUpdates API
2. Register the group using `register_group()` method
3. Update `config/telegram_config.json` manually

## Next Steps

1. **Create Groups** - Follow setup instructions to create all groups
2. **Register Groups** - Get chat IDs and register with integration
3. **Set Up Integrations** - Configure CI/CD and monitoring integrations
4. **Train Team** - Share group purposes and usage guidelines

## Support

For issues or questions:
1. Check the setup report: `LAUNCHPADPM_TELEGRAM_SETUP_REPORT.md`
2. Review Telegram Bot API docs: https://core.telegram.org/bots/api
3. Check the integration code: `integrations/telegram_integration.py`
4. Contact @BotFather for bot issues
