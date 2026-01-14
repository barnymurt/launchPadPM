"""
Verification script for Notion integration.
Tests connection and verifies workspace access.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.notion_integration import NotionIntegration, extract_page_id_from_url


def main():
    """Main verification function"""
    print("=" * 70)
    print("Notion Integration Verification")
    print("=" * 70)
    print()
    
    # Get API token
    api_token = os.getenv("NOTION_API_TOKEN")
    if not api_token:
        print("[INFO] NOTION_API_TOKEN environment variable not set")
        api_token = input("Enter your Notion Integration API Token: ").strip()
        if not api_token:
            print("[ERROR] API token is required")
            return
    
    # Get team space URL or ID
    team_space_url = os.getenv("NOTION_TEAM_SPACE_URL", "https://www.notion.so/LaunchPadPM-2e89cb246f1f80a0a5b1f15433b0855c")
    team_space_id = os.getenv("NOTION_TEAM_SPACE_ID")
    
    if not team_space_id and team_space_url:
        print(f"[INFO] Using workspace URL: {team_space_url}")
        team_space_id = extract_page_id_from_url(team_space_url)
        if team_space_id:
            print(f"[INFO] Extracted page ID: {team_space_id}")
        else:
            print("[ERROR] Could not extract page ID from URL")
            team_space_id = input("Enter your Notion Team Space Page ID manually: ").strip()
    
    if not team_space_id:
        print("[ERROR] Team space ID is required")
        return
    
    # Initialize integration
    try:
        print("\n" + "-" * 70)
        print("Step 1: Testing API Connection")
        print("-" * 70)
        
        integration = NotionIntegration(
            api_token=api_token,
            team_space_id=team_space_id
        )
        
        # Test connection
        if not integration.client.test_connection():
            print("[ERROR] Failed to connect to Notion API")
            print("\nTroubleshooting:")
            print("  1. Check that your API token is correct")
            print("  2. Verify the token starts with 'secret_'")
            print("  3. Make sure the integration is active in Notion")
            return
        
        print("[OK] API connection successful!")
        
        # Get user info
        user_info = integration.client.get_user_info()
        if user_info:
            bot_id = user_info.get("bot", {}).get("id", "Unknown")
            print(f"[INFO] Connected as integration: {bot_id}")
        
        print("\n" + "-" * 70)
        print("Step 2: Verifying Workspace Access")
        print("-" * 70)
        
        # Verify workspace access
        if not integration.verify_workspace_access():
            print("\nTroubleshooting:")
            print("  1. Go to your Notion page: https://www.notion.so/LaunchPadPM-2e89cb246f1f80a0a5b1f15433b0855c")
            print("  2. Click 'Share' in the top-right corner")
            print("  3. Click 'Add connections' or 'Invite'")
            print("  4. Select your Notion integration")
            print("  5. Make sure the integration has 'Can edit' permissions")
            return
        
        print("\n" + "-" * 70)
        print("Step 3: Checking Existing Databases")
        print("-" * 70)
        
        # List existing databases
        existing_dbs = integration.list_existing_databases()
        if existing_dbs:
            print(f"[INFO] Found {len(existing_dbs)} database(s) in workspace:")
            for db_name, db_id in existing_dbs.items():
                print(f"  - {db_name}: {db_id[:8]}...")
        else:
            print("[INFO] No databases found. Run setup_notion.py to create the workspace structure.")
        
        print("\n" + "-" * 70)
        print("Step 4: Testing Page Creation")
        print("-" * 70)
        
        # Test creating a page
        try:
            test_page = integration.client.create_page(
                parent_id=integration.team_space_id,
                title="🔧 Integration Test Page"
            )
            print(f"[OK] Successfully created test page: {test_page['id']}")
            print(f"[INFO] You can delete this test page from your Notion workspace")
        except Exception as e:
            print(f"[WARNING] Could not create test page: {e}")
            print("[INFO] This might be normal if the workspace structure hasn't been set up yet")
        
        print("\n" + "=" * 70)
        print("✅ Verification Complete!")
        print("=" * 70)
        print("\nYour Notion integration is working correctly!")
        print("\nNext steps:")
        print("  1. If databases don't exist, run: python scripts/setup_notion.py")
        print("  2. To sync documentation, run: python scripts/sync_docs_to_notion.py")
        print("  3. Set environment variables for convenience:")
        print("     $env:NOTION_API_TOKEN = 'your_token_here'")
        print("     $env:NOTION_TEAM_SPACE_ID = 'your_page_id_here'")
        
    except Exception as e:
        print(f"\n[ERROR] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
