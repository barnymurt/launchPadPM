# Telegram Groups Setup Guide - Step by Step

This guide will walk you through creating Telegram groups, adding the bot, and registering them with the integration.

## Prerequisites

✅ Bot created: @LaunchPadPM_bot  
✅ Bot token: `8548448683:AAFRNepJ57VTvFEevqRBxLfn_HVz_2n2hMI`  
✅ Integration ready

## Step 1: Create Groups in Telegram

For each group below, follow these steps:

1. **Open Telegram** (mobile app or desktop)
2. **Click "New Group"** (or tap the pencil icon)
3. **Add team members** you want in the group
4. **Name the group** using the exact name below
5. **Create the group**

### Groups to Create

Create these 9 groups with these exact names:

1. **LaunchpadPM General**
   - Description: General team discussions and announcements

2. **LaunchpadPM CEO Announcements**
   - Description: CEO announcements, strategic updates, and important communications

3. **LaunchpadPM Dev**
   - Description: Development discussions, code reviews, and technical decisions

4. **LaunchpadPM DevOps**
   - Description: DevOps, infrastructure, deployments, and CI/CD discussions

5. **LaunchpadPM Deployments**
   - Description: Deployment status, rollouts, and release notifications

6. **LaunchpadPM Incidents**
   - Description: Production incidents, alerts, and incident response

7. **LaunchpadPM Monitoring**
   - Description: Monitoring alerts, metrics, and observability

8. **LaunchpadPM Sprint Planning**
   - Description: Sprint planning sessions and backlog discussions

9. **LaunchpadPM Daily Standup**
   - Description: Daily standup updates and progress tracking

## Step 2: Add Bot to Each Group

For each group you created:

1. **Open the group** in Telegram
2. **Tap on the group name** at the top
3. **Tap "Add Members"** (or "Add Participants")
4. **Search for** `@LaunchPadPM_bot`
5. **Add the bot** to the group
6. **Make bot an administrator** (optional but recommended):
   - Tap on group name → "Administrators"
   - Find @LaunchPadPM_bot
   - Enable admin permissions

## Step 3: Send Messages in Groups

For each group:

1. **Send at least one message** in the group
   - This can be any message, like "Hello" or "Test"
   - The bot doesn't need to respond, we just need activity

## Step 4: Get Chat IDs

After sending messages in all groups, get the chat IDs:

### Option A: Automatic (Recommended)

Run the auto-registration script:

```powershell
$env:TELEGRAM_BOT_TOKEN = "8548448683:AAFRNepJ57VTvFEevqRBxLfn_HVz_2n2hMI"
python scripts/auto_register_telegram_groups.py
```

This script will:
- Fetch all groups the bot is in
- Match them to expected group names
- Register them automatically

### Option B: Manual

1. **Visit this URL in your browser:**
   ```
   https://api.telegram.org/bot8548448683:AAFRNepJ57VTvFEevqRBxLfn_HVz_2n2hMI/getUpdates
   ```

2. **Look for chat IDs** in the JSON response
   - Find entries like: `"chat":{"id":-123456789,"title":"LaunchpadPM General"}`
   - The ID will be a **negative number** for groups (e.g., `-123456789`)

3. **Save the chat IDs** for each group

## Step 5: Register Groups

### Automatic Registration

If you used the auto-registration script (Option A above), groups are already registered! Skip to Step 6.

### Manual Registration

If you got chat IDs manually, register them:

**Option 1: Use the registration script**

```powershell
$env:TELEGRAM_BOT_TOKEN = "8548448683:AAFRNepJ57VTvFEevqRBxLfn_HVz_2n2hMI"
python scripts/register_telegram_groups.py
```

Then enter chat IDs when prompted.

**Option 2: Edit config file directly**

Edit `config/telegram_config.json`:

```json
{
  "bot_username": "LaunchPadPM_bot",
  "bot_id": 8548448683,
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

Replace the negative numbers with your actual chat IDs.

## Step 6: Verify Registration

Test the integration:

```python
from integrations.telegram_integration import TelegramIntegration
import os

integration = TelegramIntegration(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))

# Test sending a message
integration.send_ceo_message(
    group_name="ceo-announcements",
    message="🚀 LaunchpadPM Telegram integration is live!"
)
```

## Quick Reference

### Bot Information
- **Username:** @LaunchPadPM_bot
- **Bot ID:** 8548448683
- **Token:** `8548448683:AAFRNepJ57VTvFEevqRBxLfn_HVz_2n2hMI`

### Scripts Available

1. **Auto Register (Recommended):**
   ```bash
   python scripts/auto_register_telegram_groups.py
   ```

2. **Interactive Register:**
   ```bash
   python scripts/register_telegram_groups.py
   ```

3. **Get Updates URL:**
   ```
   https://api.telegram.org/bot8548448683:AAFRNepJ57VTvFEevqRBxLfn_HVz_2n2hMI/getUpdates
   ```

## Troubleshooting

### No Groups Found

**Problem:** Script says "No updates found"

**Solutions:**
1. Make sure groups are created
2. Verify bot is added to each group
3. Send a message in each group
4. Wait a few seconds and try again

### Chat ID Not Found

**Problem:** Can't find chat ID in getUpdates

**Solutions:**
1. Make sure you sent a message in the group
2. Check that bot is actually in the group
3. Try sending another message
4. Refresh the getUpdates URL

### Registration Failed

**Problem:** Error when registering group

**Solutions:**
1. Verify chat ID is correct (negative number for groups)
2. Check that bot has permission in the group
3. Make bot an administrator
4. Try again

## Next Steps After Registration

Once groups are registered:

1. ✅ **Test messaging** - Send a test message to each group
2. ✅ **Configure integrations** - Set up CI/CD and monitoring
3. ✅ **Train team** - Share group purposes with team
4. ✅ **Start using** - Begin team communication via Telegram

## Integration Usage

After setup, you can use the integration in your code:

```python
from integrations.telegram_integration import TelegramIntegration
import os

# Initialize
integration = TelegramIntegration(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))

# Send CEO announcement
integration.send_ceo_message(
    group_name="ceo-announcements",
    message="Important update: New product launch next week!"
)

# Create question thread
integration.create_question_thread(
    group_name="dev",
    question="What's the priority for this sprint?",
    context="We need to decide between feature A and feature B"
)

# Send to any registered group
integration.send_ceo_message(
    group_name="deployments",
    message="✅ Deployment successful!"
)
```

## Support

If you encounter issues:
1. Check the setup report: `LAUNCHPADPM_TELEGRAM_SETUP_REPORT.md`
2. Review Telegram Bot API docs: https://core.telegram.org/bots/api
3. Check integration code: `integrations/telegram_integration.py`
