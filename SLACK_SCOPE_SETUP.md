# Slack OAuth Token Scope Setup Guide

## Current Status

✅ **Connection Successful** - Connected to LaunchPadPM workspace (T0A8JCB70HH)
❌ **Missing Scopes** - The OAuth token needs additional permissions

## Current Scopes

Your current OAuth token has:
- `identify`
- `app_configurations:read`
- `app_configurations:write`

## Required Scopes

To enable channel creation and management, you need to add these scopes:

### Bot Token Scopes (Recommended)
1. `channels:read` - View basic information about public channels
2. `channels:write` - Create public channels
3. `channels:manage` - Manage public channels
4. `chat:write` - Send messages as the bot
5. `chat:write.public` - Send messages to channels the bot isn't a member of
6. `conversations:read` - View basic information about public and private channels
7. `conversations:write` - Start conversations and create channels

## How to Add Scopes

### Option 1: Add Scopes to Existing App (Recommended)

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Find your app (the one that generated the OAuth tokens)
3. Click on **"OAuth & Permissions"** in the left sidebar
4. Scroll to **"Scopes"** → **"Bot Token Scopes"**
5. Click **"Add an OAuth Scope"**
6. Add each of the required scopes listed above
7. Scroll to the top and click **"Reinstall to Workspace"**
8. Review permissions and click **"Allow"**
9. Copy the new **"Bot User OAuth Token"** (starts with `xoxb-`)
10. Update your environment variable:
    ```powershell
    $env:SLACK_BOT_TOKEN='xoxb-your-new-token-here'
    ```

### Option 2: Use OAuth Token Scopes

If you want to use OAuth tokens instead of bot tokens:

1. Go to your Slack app settings
2. Click on **"OAuth & Permissions"**
3. Scroll to **"Scopes"** → **"User Token Scopes"** (for OAuth tokens)
4. Add the required scopes:
   - `channels:read`
   - `channels:write`
   - `channels:manage`
   - `chat:write`
   - `conversations:read`
   - `conversations:write`
5. Reinstall the app to your workspace
6. Generate new OAuth tokens with the updated scopes

## After Adding Scopes

Once you've added the scopes and reinstalled the app:

1. **If using Bot Token:**
   ```powershell
   $env:SLACK_BOT_TOKEN='xoxb-your-new-bot-token'
   python scripts/connect_launchpadpm_slack.py
   ```

2. **If using OAuth Token:**
   ```powershell
   $env:SLACK_ACCESS_TOKEN='xoxe.xoxp-your-new-access-token'
   $env:SLACK_REFRESH_TOKEN='xoxe-1-your-new-refresh-token'
   python scripts/connect_launchpadpm_slack.py
   ```

## What Will Happen

After adding the scopes and running the script again, it will:

1. ✅ Connect to LaunchPadPM workspace
2. ✅ List existing channels
3. ✅ Create new channels:
   - #general
   - #ceo-announcements
   - #launchpadpm-dev
   - #launchpadpm-devops
   - #launchpadpm-deployments
   - #launchpadpm-incidents
   - #launchpadpm-monitoring
   - #launchpadpm-infrastructure
   - #code-reviews
   - #technical-decisions
   - #sprint-planning
   - #daily-standup
   - #random
4. ✅ Set channel topics
5. ✅ Send welcome message
6. ✅ Generate connection report

## Troubleshooting

### "missing_scope" Error

If you still get `missing_scope` errors:
1. Verify all scopes are added in the app settings
2. Make sure you reinstalled the app after adding scopes
3. Check that you're using the new token (not the old one)
4. Verify the token type matches (bot token vs OAuth token)

### Token Not Working

If the token doesn't work:
1. Generate a new token after adding scopes
2. Make sure the app is installed to the correct workspace (LaunchPadPM)
3. Check that the workspace ID matches: T0A8JCB70HH

## Next Steps

1. Add the required scopes to your Slack app
2. Reinstall the app to your workspace
3. Get the new token
4. Run the connection script again
5. Review the connection report

Once the scopes are added, the Development Engineer and DevOps Engineer will be able to set up all the LaunchpadPM channels successfully!
