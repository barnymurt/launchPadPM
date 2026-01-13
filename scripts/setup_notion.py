"""
Setup script for Notion integration.
Creates team workspace structure in Notion.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.notion_integration import NotionIntegration


def main():
    """Main setup function"""
    print("=" * 60)
    print("Notion Team Workspace Setup")
    print("=" * 60)
    print()
    
    # Get API token
    api_token = os.getenv("NOTION_API_TOKEN")
    if not api_token:
        api_token = input("Enter your Notion Integration API Token: ").strip()
        if not api_token:
            print("[ERROR] API token is required")
            return
    
    # Get team space ID
    team_space_id = os.getenv("NOTION_TEAM_SPACE_ID")
    if not team_space_id:
        print("\nTo create the team workspace, you need to:")
        print("1. Create a page in Notion (or use an existing page)")
        print("2. Share the page with your Notion integration")
        print("3. Copy the page ID from the page URL")
        print("   (The ID is the 32-character string in the URL)")
        print()
        team_space_id = input("Enter your Notion Team Space Page ID: ").strip()
        if not team_space_id:
            print("[ERROR] Team space ID is required")
            return
    
    # Initialize integration
    try:
        integration = NotionIntegration(
            api_token=api_token,
            team_space_id=team_space_id
        )
        
        # Test connection
        print("\n[INFO] Testing Notion connection...")
        if not integration.client.test_connection():
            print("[ERROR] Failed to connect to Notion. Check your API token.")
            return
        
        print("[OK] Connection successful!")
        
        # Create team workspace
        print("\n[INFO] Creating team workspace structure...")
        integration.create_team_space()
        
        # Save configuration
        integration.save_config()
        
        print("\n" + "=" * 60)
        print("Setup Complete!")
        print("=" * 60)
        print("\nYour team workspace has been created in Notion.")
        print("Configuration saved to: notion_config.json")
        print("\nNext steps:")
        print("1. Visit your Notion workspace to see the structure")
        print("2. Set NOTION_API_TOKEN and NOTION_TEAM_SPACE_ID environment variables")
        print("3. Start syncing documentation using the integration")
        
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
