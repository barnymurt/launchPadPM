# Slack Integration Setup Guide

This guide explains how to set up Slack integration for team communication, enabling the CEO and team members to communicate effectively via Slack.

## Overview

The Slack integration provides:
- **Team Communication Channels** - Organized channels for different aspects of team collaboration
- **CEO Communication** - Dedicated channel for CEO announcements and strategic updates
- **Question & Answer** - Easy way for team members to ask questions and receive instructions
- **Integration Ready** - Setup for CI/CD, monitoring, and other tool integrations

## Prerequisites

1. **Slack Workspace** - You need access to a Slack workspace
2. **Slack App Creation** - Create a Slack app with appropriate permissions
3. **Python Dependencies** - Install required packages

## Step 1: Create Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Enter app name (e.g., "Product Team Bot") and select your workspace
4. Click **"Create App"**

## Step 2: Configure Bot Permissions

1. In your app settings, go to **"OAuth & Permissions"** (left sidebar)
2. Scroll to **"Scopes"** → **"Bot Token Scopes"**
3. Add the following scopes:
   - `channels:read` - View basic information about public channels
   - `channels:write` - Create public channels
   - `channels:manage` - Manage public channels
   - `chat:write` - Send messages as the bot
   - `chat:write.public` - Send messages to channels the bot isn't a member of
   - `conversations:read` - View basic information about public and private channels
   - `conversations:write` - Start conversations and create channels

## Step 3: Install App to Workspace

1. Still in **"OAuth & Permissions"**, scroll to the top
2. Click **"Install to Workspace"**
3. Review permissions and click **"Allow"**
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)

## Step 4: Set Environment Variable

### Windows (PowerShell)
```powershell
$env:SLACK_BOT_TOKEN='xoxb-your-token-here'
```

### Linux/Mac
```bash
export SLACK_BOT_TOKEN='xoxb-your-token-here'
```

### Permanent Setup (Optional)

Create a `.env` file in the project root:
```
SLACK_BOT_TOKEN=xoxb-your-token-here
```

Then load it in your script or use `python-dotenv`.

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `slack-sdk>=3.27.0` along with other dependencies.

## Step 6: Run Setup Script

```bash
python scripts/setup_slack_workspace.py
```

The script will:
1. Test Slack API connection
2. Get recommendations from Development Engineer and DevOps Engineer agents
3. Create standard team channels
4. Set channel topics and descriptions
5. Send welcome message
6. Generate setup report

## Channels Created

The setup script creates the following channels:

- **#general** - General team discussions and announcements
- **#ceo-announcements** - CEO announcements, strategic updates, and important communications
- **#product-team** - Product team discussions, sprint planning, and daily standups
- **#dev-engineering** - Development engineering discussions, code reviews, technical decisions
- **#devops-infrastructure** - DevOps, infrastructure, deployments, and CI/CD discussions
- **#sprint-planning** - Sprint planning sessions and backlog discussions
- **#daily-standup** - Daily standup updates and progress tracking
- **#incidents** - Production incidents, alerts, and incident response
- **#random** - Non-work banter, team building, and casual conversations

## Usage

### For CEO

1. **Post Announcements** - Use `#ceo-announcements` for important announcements and strategic updates
2. **Engage with Team** - Use `#product-team` to engage with the product team on priorities
3. **Ask Questions** - Post questions in appropriate channels and team members will respond

### For Team Members

1. **Ask Questions** - Use appropriate channels:
   - Technical questions → `#dev-engineering`
   - Infrastructure questions → `#devops-infrastructure`
   - Product questions → `#product-team`
   - General questions → `#general`

2. **Share Updates** - Use `#daily-standup` for daily progress updates

3. **Report Issues** - Use `#incidents` for production issues

## Integration with Python Code

### Basic Usage

```python
from integrations.slack_integration import SlackIntegration
import os

# Initialize integration
integration = SlackIntegration(api_token=os.getenv("SLACK_BOT_TOKEN"))

# Test connection
if integration.test_connection():
    print("Connected to Slack!")

# Send a message
integration.send_ceo_message(
    channel="#ceo-announcements",
    message="Important announcement: New product launch next week!"
)

# Create a question thread
integration.create_question_thread(
    channel="#product-team",
    question="What's the priority for this sprint?",
    context="We need to decide between feature A and feature B"
)
```

### Using the Slack Client Directly

```python
from integrations.slack_integration import SlackClient

client = SlackClient(api_token=os.getenv("SLACK_BOT_TOKEN"))

# List channels
channels = client.list_channels()
for channel in channels:
    print(f"#{channel['name']}")

# Create a channel
new_channel = client.create_channel("new-feature-discussion")

# Send a message
client.send_message(
    channel="#general",
    text="Hello team! 👋"
)
```

## Configuration

Configuration is saved to `config/slack_config.json`:

```json
{
  "workspace_id": "T1234567890",
  "workspace_name": "Product Team",
  "channels": {
    "general": "C1234567890",
    "ceo-announcements": "C0987654321",
    ...
  },
  "last_updated": "2024-01-14T12:00:00"
}
```

## Troubleshooting

### Connection Failed

**Error:** `Slack connection failed`

**Solutions:**
1. Verify your `SLACK_BOT_TOKEN` is set correctly
2. Check that the token starts with `xoxb-`
3. Ensure the app is installed to your workspace
4. Verify all required scopes are added

### Permission Denied

**Error:** `missing_scope` or `not_authed`

**Solutions:**
1. Go to your Slack app settings → OAuth & Permissions
2. Verify all required scopes are added
3. Reinstall the app to your workspace
4. Generate a new token if needed

### Channel Creation Failed

**Error:** `name_taken` or `invalid_name`

**Solutions:**
1. Channel name must be lowercase, no spaces, max 80 characters
2. Use hyphens instead of spaces (e.g., `dev-engineering` not `dev engineering`)
3. Check if channel already exists - the script will use existing channels

### Message Sending Failed

**Error:** `channel_not_found` or `not_in_channel`

**Solutions:**
1. Ensure the bot is invited to the channel
2. For private channels, the bot must be a member
3. Use channel ID instead of name if name resolution fails

## Next Steps

1. **Invite Team Members** - Add team members to the workspace and relevant channels
2. **Set Up Integrations** - Configure CI/CD, monitoring, and other tool integrations
3. **Configure Webhooks** - Set up webhook integrations for automated notifications
4. **Train Team** - Share channel purposes and usage guidelines with the team

## Integration Opportunities

### CI/CD Integration

Configure your CI/CD pipeline to post to Slack:
- Deployment status → `#deployments` or `#devops-infrastructure`
- Build failures → `#dev-engineering`
- Test results → `#dev-engineering`

### Monitoring Integration

Set up monitoring alerts:
- Production alerts → `#incidents`
- Performance metrics → `#devops-infrastructure`
- Error tracking → `#incidents`

### Project Management Integration

Connect project management tools:
- Jira/Linear → Post updates to `#product-team`
- GitHub/GitLab → Post PR notifications to `#dev-engineering`

## Support

For issues or questions:
1. Check the setup report: `SLACK_SETUP_REPORT.md`
2. Review Slack API documentation: [https://api.slack.com](https://api.slack.com)
3. Check the integration code: `integrations/slack_integration.py`
