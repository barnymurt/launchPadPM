"""
Script to sync documentation to Notion.
Reads documentation files and syncs them to the team workspace.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.notion_integration import NotionIntegration, extract_page_id_from_url


def find_documentation_files(root_dir: Path) -> List[tuple]:
    """
    Find all documentation files in the repository.
    
    Returns:
        List of (file_path, doc_type) tuples
    """
    doc_files = []
    
    # Documentation patterns
    patterns = {
        "README": ["README.md", "README_FRAMEWORK.md", "README_TESTING.md"],
        "PROJECT_BRIEF": ["PROJECT_BRIEF.md"],
        "ARCHITECTURE": ["ARCHITECTURE.md"],
        "ADR": ["adr/*.md", "docs/adr/*.md"],
        "CHANGELOG": ["CHANGELOG.md"],
        "GOVERNANCE": ["CODE_REVIEW_REPORT.md", "PRODUCT_DOCUMENTATION.md", "IMPROVEMENTS_BACKLOG.md"]
    }
    
    for doc_type, patterns_list in patterns.items():
        for pattern in patterns_list:
            # Handle glob patterns
            if '*' in pattern:
                for file_path in root_dir.glob(pattern):
                    if file_path.is_file():
                        doc_files.append((file_path, doc_type))
            else:
                file_path = root_dir / pattern
                if file_path.exists() and file_path.is_file():
                    doc_files.append((file_path, doc_type))
    
    return doc_files


def sync_documentation(
    integration: NotionIntegration,
    file_path: Path,
    doc_type: str
) -> Optional[str]:
    """
    Sync a single documentation file to Notion.
    
    Args:
        integration: NotionIntegration instance
        file_path: Path to documentation file
        doc_type: Type of documentation
    
    Returns:
        Created page ID if successful, None otherwise
    """
    try:
        # Read file content with proper UTF-8 encoding and error handling
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Extract title from first line or filename
        title = file_path.stem.replace('_', ' ').title()
        if content.startswith('# '):
            title = content.split('\n')[0][2:].strip()
        
        # Sync to Notion
        page_id = integration.sync_documentation(
            doc_type=doc_type,
            title=title,
            content=content
        )
        
        return page_id
    
    except Exception as e:
        error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
        print(f"[ERROR] Failed to sync {file_path.name}: {error_msg}")
        return None


def main():
    """Main sync function"""
    print("=" * 60)
    print("Sync Documentation to Notion")
    print("=" * 60)
    print()
    
    # Load configuration
    integration = NotionIntegration()
    
    try:
        integration.load_config()
    except Exception as e:
        print(f"[WARNING] Could not load config: {e}")
        print("[INFO] Using environment variables or manual setup")
    
    # Get API token if not in config
    if not integration.client.api_token:
        api_token = os.getenv("NOTION_API_TOKEN")
        if api_token:
            integration.client.api_token = api_token
            integration.client.client.auth = api_token
        else:
            print("[ERROR] NOTION_API_TOKEN not found")
            print("Set it as environment variable or in notion_config.json")
            return
    
    # Get team space ID if not in config
    if not integration.team_space_id:
        team_space_id = os.getenv("NOTION_TEAM_SPACE_ID")
        team_space_url = os.getenv("NOTION_TEAM_SPACE_URL")
        
        if team_space_url:
            team_space_id = extract_page_id_from_url(team_space_url)
            if team_space_id:
                print(f"[INFO] Extracted page ID from URL: {team_space_id}")
        
        if team_space_id:
            integration.team_space_id = team_space_id
        else:
            print("[ERROR] NOTION_TEAM_SPACE_ID or NOTION_TEAM_SPACE_URL not found")
            print("Set it as environment variable or in notion_config.json")
            print("Example: NOTION_TEAM_SPACE_URL=https://www.notion.so/LaunchPadPM-2e89cb246f1f80a0a5b1f15433b0855c")
            return
    
    # Test connection
    if not integration.client.test_connection():
        print("[ERROR] Cannot connect to Notion API")
        return
    
    # Find documentation files
    root_dir = Path(__file__).parent.parent
    print(f"[INFO] Scanning for documentation in: {root_dir}")
    
    doc_files = find_documentation_files(root_dir)
    
    if not doc_files:
        print("[WARNING] No documentation files found")
        return
    
    print(f"[INFO] Found {len(doc_files)} documentation file(s)")
    print()
    
    # Sync each file
    synced_count = 0
    for file_path, doc_type in doc_files:
        print(f"[INFO] Syncing: {file_path.name} ({doc_type})...")
        page_id = sync_documentation(integration, file_path, doc_type)
        if page_id:
            synced_count += 1
            print(f"  [OK] Synced to Notion (Page ID: {page_id[:8]}...)")
        else:
            print(f"  [ERROR] Failed to sync")
        print()
    
    print("=" * 60)
    print(f"Sync Complete: {synced_count}/{len(doc_files)} files synced")
    print("=" * 60)


if __name__ == "__main__":
    main()
