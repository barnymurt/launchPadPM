# Notion Integration Guide

This guide explains how to set up and use the Notion integration for the Product Team workspace.

## Overview

The Notion integration allows the team to:
- Create a structured team workspace in Notion
- Sync all documentation automatically
- Maintain databases for projects, executive summaries, decisions, and OKRs
- Keep documentation organized and accessible

## Prerequisites

1. **Notion Account**: You need a Notion account with workspace access
2. **Notion Integration**: Create a Notion integration to get an API token
3. **Python Package**: Install the `notion-client` library

## Setup Instructions

### Step 1: Create Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Give it a name (e.g., "Product Team Integration")
4. Select your workspace
5. Copy the "Internal Integration Token" (starts with `secret_`)
6. Keep this token secure - you'll need it for setup

### Step 2: Create Team Space Page

1. In Notion, create a new page (or use an existing page)
2. Name it "Product Team Workspace" (or your preferred name)
3. Click "Share" in the top-right
4. Click "Add connections" and select your integration
5. Copy the page ID from the URL:
   - The URL looks like: `https://www.notion.so/Your-Page-Name-{32-char-id}`
   - Copy the 32-character ID (remove any hyphens)

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `notion-client` and other dependencies.

### Step 4: Run Setup Script

```bash
python scripts/setup_notion.py
```

The script will:
- Ask for your Notion API token (or use `NOTION_API_TOKEN` env var)
- Ask for your team space page ID (or use `NOTION_TEAM_SPACE_ID` env var)
- Test the connection
- Create the team workspace structure:
  - Projects database
  - Executive Summaries database
  - Key Decisions Log database
  - OKRs/Goals database
  - Key Results database
  - Documentation pages structure
- Save configuration to `notion_config.json`

### Step 5: Set Environment Variables (Optional)

For convenience, set these environment variables:

```bash
# Windows (PowerShell)
$env:NOTION_API_TOKEN = "secret_your_token_here"
$env:NOTION_TEAM_SPACE_ID = "your_page_id_here"

# Linux/Mac
export NOTION_API_TOKEN="secret_your_token_here"
export NOTION_TEAM_SPACE_ID="your_page_id_here"
```

## Using the Integration

### Sync Documentation

To sync all documentation files to Notion:

```bash
python scripts/sync_docs_to_notion.py
```

This script:
- Scans the repository for documentation files
- Syncs them to the Notion workspace
- Organizes them by type (README, ADR, CHANGELOG, etc.)

### Programmatic Usage

You can also use the integration in your code:

```python
from integrations.notion_integration import NotionIntegration

# Initialize (uses env vars or config file)
integration = NotionIntegration()

# Sync a document
page_id = integration.sync_documentation(
    doc_type="ADR",
    title="ADR-001: Use Python for Backend",
    content="# ADR-001: Use Python for Backend\n\n...",
    project_name="My Project"
)

# Add a project to the Projects database
project_properties = {
    "Project Name": {"title": [{"text": {"content": "My Project"}}]},
    "Status": {"select": {"name": "Active"}},
    "Strategic Priority": {"select": {"name": "High"}},
    # ... other properties
}

integration.client.add_page_to_database(
    database_id=integration.get_database_id("projects"),
    properties=project_properties
)
```

## Workspace Structure

The setup script creates the following structure:

```
Product Team Workspace
├── 📚 Documentation
│   ├── Project Briefs
│   ├── Architecture Docs
│   ├── ADRs (Architecture Decision Records)
│   ├── Changelogs
│   ├── User Stories
│   └── Bug Reports
├── 📊 Projects (Database)
├── 📋 Executive Summaries (Database)
├── 📝 Key Decisions Log (Database)
├── 🎯 OKRs/Goals (Database)
└── 📈 Key Results (Database)
```

## Database Schemas

### Projects Database

Tracks all active and planned product initiatives:
- Project Name (Title)
- Status (Select: Discovery, Active, On Hold, Complete, Cancelled)
- Product Owner (Person)
- Start Date, Target Completion (Date)
- Product Goal, North Star Metric (Text)
- Current/Target Metric Values (Number)
- RICE Score (Number)
- Strategic Priority (Select: Critical, High, Medium, Low)
- Resources Allocated (Number - %)
- Last Updated (Auto)

### Executive Summaries Database

Weekly/Sprint summaries for each project:
- Summary Title (Title)
- Project (Relation)
- Sprint Number (Number)
- Report Date (Date)
- Sprint Goal, Sprint Goal Achieved (Text, Checkbox)
- Key Accomplishments, Metrics Update (Text)
- Challenges & Risks, Decisions Made (Text)
- Help Needed, Next Sprint Focus (Text)
- Confidence Level (Select: High, Medium, Low)
- Product Owner (Person)

### Key Decisions Log Database

Records significant strategic and tactical decisions:
- Decision (Title)
- Project (Relation)
- Date (Date)
- Decision Type (Select: Strategic, Product, Technical, Resource Allocation, Go/No-Go)
- Decision Maker(s) (People)
- Context, Options Considered, Decision Rationale (Text)
- Expected Outcome, Actual Outcome (Text)
- Review Date (Date)
- Status (Select: Pending, Implemented, Under Review, Reversed)
- Related ADR (URL)

### OKRs/Goals Database

Tracks company/product objectives:
- Objective (Title)
- Quarter (Select: Q1-Q4 2026)
- Owner (Person)
- Status (Select: On Track, At Risk, Off Track, Complete)
- Progress (Number - %)
- Last Updated (Auto)

### Key Results Database

Measurable outcomes for each objective:
- Key Result (Title)
- Objective (Relation)
- Target, Current (Number)
- Unit (Text)
- Due Date (Date)
- Status (Select: On Track, At Risk, Off Track, Complete)
- Update Frequency (Select: Weekly, Bi-weekly, Monthly)
- Last Updated (Auto)

## Configuration File

The setup script creates `notion_config.json`:

```json
{
  "team_space_id": "your-page-id-here",
  "databases": {
    "projects": "database-id-1",
    "executive_summaries": "database-id-2",
    "decisions": "database-id-3",
    "okrs": "database-id-4",
    "key_results": "database-id-5"
  }
}
```

This file stores the IDs of created databases for easy reference.

## Troubleshooting

### Connection Errors

- **"Cannot connect to Notion API"**: Check your API token is correct
- **"Page not found"**: Ensure the page is shared with your integration
- **"Permission denied"**: Make sure the integration has access to the page

### Database Creation Errors

- **"Database already exists"**: The database may have been created previously. Check your Notion workspace.
- **"Invalid property type"**: The Notion API may have changed. Check the latest API documentation.

### Documentation Sync Errors

- **"Markdown conversion failed"**: The markdown converter is simplified. Complex markdown may not convert perfectly.
- **"Page creation failed"**: Check that the team space ID is correct and the integration has write access.

## Security Best Practices

1. **Never commit API tokens**: Add `notion_config.json` to `.gitignore` if it contains tokens
2. **Use environment variables**: Store tokens in environment variables, not in code
3. **Limit integration access**: Only share necessary pages with the integration
4. **Rotate tokens**: If a token is compromised, create a new integration

## Next Steps

1. **Customize the workspace**: Add views, filters, and templates to the databases
2. **Automate syncing**: Set up CI/CD to sync documentation automatically
3. **Integrate with agents**: Update agents to automatically create Notion pages when generating documentation
4. **Add more databases**: Extend the integration to support additional databases as needed

## Support

For issues or questions:
- Check the [Notion API Documentation](https://developers.notion.com/)
- Review the integration code in `integrations/notion_integration.py`
- Check the setup script in `scripts/setup_notion.py`
