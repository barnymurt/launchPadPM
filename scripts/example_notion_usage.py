"""
Example script demonstrating Notion integration usage.
Shows how to sync data bidirectionally between Cursor and Notion.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.notion_integration import NotionIntegration


def example_sync_documentation():
    """Example: Sync documentation to Notion"""
    print("=" * 70)
    print("Example: Syncing Documentation to Notion")
    print("=" * 70)
    
    integration = NotionIntegration()
    integration.load_config()
    
    # Example markdown content
    markdown_content = """# Example Document

This is an example document synced from Cursor to Notion.

## Features

- Automatic markdown conversion
- Bidirectional data sharing
- Organized by document type

## Code Example

```python
from integrations.notion_integration import NotionIntegration

integration = NotionIntegration()
integration.sync_documentation(
    doc_type="PROJECT_BRIEF",
    title="My Project",
    content="# Project Title\n\nProject description..."
)
```
"""
    
    page_id = integration.sync_documentation(
        doc_type="PROJECT_BRIEF",
        title="Example: Cursor to Notion Sync",
        content=markdown_content
    )
    
    if page_id:
        print(f"✅ Document synced successfully! Page ID: {page_id}")
    else:
        print("❌ Failed to sync document")


def example_read_from_notion():
    """Example: Read data from Notion database"""
    print("\n" + "=" * 70)
    print("Example: Reading Data from Notion")
    print("=" * 70)
    
    integration = NotionIntegration()
    integration.load_config()
    
    # Read projects from Notion
    projects = integration.sync_from_notion("projects", limit=10)
    
    if projects:
        print(f"✅ Found {len(projects)} project(s) in Notion:")
        for i, project in enumerate(projects, 1):
            props = project.get("properties", {})
            project_name = props.get("Project Name", {})
            if project_name.get("title"):
                name = project_name["title"][0].get("plain_text", "Unknown")
                print(f"  {i}. {name}")
    else:
        print("ℹ️  No projects found (database may not exist yet)")


def example_add_to_database():
    """Example: Add a project to the Projects database"""
    print("\n" + "=" * 70)
    print("Example: Adding Data to Notion Database")
    print("=" * 70)
    
    integration = NotionIntegration()
    integration.load_config()
    
    # Get database ID
    projects_db_id = integration.get_database_id("projects")
    if not projects_db_id:
        print("❌ Projects database not found. Run setup_notion.py first.")
        return
    
    # Create a new project entry
    project_properties = {
        "Project Name": {
            "title": [{"text": {"content": "Example Project from Cursor"}}]
        },
        "Status": {"select": {"name": "Discovery"}},
        "Strategic Priority": {"select": {"name": "Medium"}},
        "Product Goal": {
            "rich_text": [{"text": {"content": "Demonstrate Notion integration"}}]
        }
    }
    
    try:
        page = integration.client.add_page_to_database(
            database_id=projects_db_id,
            properties=project_properties
        )
        print(f"✅ Project added successfully! Page ID: {page['id']}")
    except Exception as e:
        print(f"❌ Failed to add project: {e}")


def main():
    """Run all examples"""
    print("\nNotion Integration Examples")
    print("=" * 70)
    print("\nThese examples demonstrate bidirectional data sharing between")
    print("Cursor and Notion. Make sure you have:")
    print("  1. Set NOTION_API_TOKEN environment variable")
    print("  2. Run setup_notion.py to create the workspace structure")
    print("  3. Shared your workspace with the integration")
    print()
    
    try:
        # Example 1: Sync documentation
        example_sync_documentation()
        
        # Example 2: Read from Notion
        example_read_from_notion()
        
        # Example 3: Add to database
        # Uncomment to test:
        # example_add_to_database()
        
        print("\n" + "=" * 70)
        print("Examples Complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
