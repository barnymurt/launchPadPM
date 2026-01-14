"""
Hello World script for Notion integration.
Creates a simple "Hello World" page in your Notion workspace as proof of success.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.notion_integration import NotionIntegration, extract_page_id_from_url


def main():
    """Create Hello World page in Notion"""
    print("=" * 70)
    print("Notion Hello World - Proof of Success")
    print("=" * 70)
    print()
    
    # Get API token
    api_token = os.getenv("NOTION_API_TOKEN")
    if not api_token:
        print("[ERROR] NOTION_API_TOKEN environment variable not set")
        print("\nPlease set it first:")
        print("  PowerShell: $env:NOTION_API_TOKEN = 'your_token_here'")
        print("  CMD: set NOTION_API_TOKEN=your_token_here")
        print("\nOr run this script with the token:")
        print("  $env:NOTION_API_TOKEN='your_token'; python scripts/hello_world_notion.py")
        return
    
    # Get team space URL or ID
    team_space_url = os.getenv("NOTION_TEAM_SPACE_URL", "https://www.notion.so/LaunchPadPM-2e89cb246f1f80a0a5b1f15433b0855c")
    team_space_id = os.getenv("NOTION_TEAM_SPACE_ID")
    
    if not team_space_id:
        print(f"[INFO] Using workspace URL: {team_space_url}")
        team_space_id = extract_page_id_from_url(team_space_url)
        if team_space_id:
            print(f"[INFO] Extracted page ID: {team_space_id}")
        else:
            print("[ERROR] Could not extract page ID from URL")
            return
    
    # Initialize integration
    try:
        print("\n[INFO] Initializing Notion integration...")
        integration = NotionIntegration(
            api_token=api_token,
            team_space_id=team_space_id
        )
        
        # Test connection
        print("[INFO] Testing API connection...")
        if not integration.client.test_connection():
            print("[ERROR] Failed to connect to Notion API")
            print("\nTroubleshooting:")
            print("  1. Check that your API token is correct")
            print("  2. Verify the token starts with 'secret_'")
            print("  3. Make sure the integration is active in Notion")
            return
        
        print("[OK] API connection successful!")
        
        # Verify workspace access
        print("\n[INFO] Verifying workspace access...")
        if not integration.verify_workspace_access():
            print("\nTroubleshooting:")
            print("  1. Go to your Notion page: https://www.notion.so/LaunchPadPM-2e89cb246f1f80a0a5b1f15433b0855c")
            print("  2. Click 'Share' in the top-right corner")
            print("  3. Click 'Add connections' or 'Invite'")
            print("  4. Select your Notion integration")
            print("  5. Make sure the integration has 'Can edit' permissions")
            return
        
        print("[OK] Workspace access verified!")
        
        # Create Hello World page
        print("\n[INFO] Creating 'Hello World' page...")
        
        hello_world_content = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "🎉 Hello World from Cursor!"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "This page was created automatically by the Cursor-Notion integration as proof of successful connection!"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "✅ Your integration is working correctly!"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "What's Next?"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Run setup_notion.py to create the full workspace structure"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Sync your documentation with sync_docs_to_notion.py"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Start using the integration in your code"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "You can delete this page anytime - it was just created to prove the integration works! 🚀"
                            }
                        }
                    ]
                }
            }
        ]
        
        page = integration.client.create_page(
            parent_id=integration.team_space_id,
            title="🎉 Hello World from Cursor",
            content=hello_world_content
        )
        
        page_id = page["id"]
        page_url = f"https://www.notion.so/{page_id.replace('-', '')}"
        
        print("[OK] Hello World page created successfully!")
        print(f"\nPage ID: {page_id}")
        print(f"View page: {page_url}")
        print("\nSUCCESS! Your Cursor-Notion integration is working!")
        print("\nYou can now:")
        print("  - See the 'Hello World' page in your Notion workspace")
        print("  - Run setup_notion.py to create the full workspace structure")
        print("  - Sync documentation with sync_docs_to_notion.py")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to create Hello World page: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
