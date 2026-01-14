"""
Notion Integration
Handles connection to Notion.io and team workspace management.
"""

import os
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json

try:
    from notion_client import Client
    NOTION_AVAILABLE = True
except ImportError:
    NOTION_AVAILABLE = False
    Client = None


def extract_page_id_from_url(url: str) -> Optional[str]:
    """
    Extract Notion page ID from a Notion URL.
    
    Notion URLs can be in formats like:
    - https://www.notion.so/Page-Name-2e89cb246f1f80a0a5b1f15433b0855c
    - https://www.notion.so/2e89cb246f1f80a0a5b1f15433b0855c
    - 2e89cb246f1f80a0a5b1f15433b0855c (already just the ID)
    
    Args:
        url: Notion page URL or page ID
        
    Returns:
        Page ID (32-character hex string) or None if not found
    """
    if not url:
        return None
    
    # If it's already just a 32-character hex string (with or without hyphens)
    clean_id = re.sub(r'[^a-f0-9]', '', url.lower())
    if len(clean_id) == 32:
        # Format as Notion expects: add hyphens
        return f"{clean_id[:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:]}"
    
    # Try to extract from URL
    # Pattern: 32 hex characters at the end (possibly with hyphens)
    match = re.search(r'([a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12})', url.lower())
    if match:
        page_id = match.group(1).replace('-', '')
        if len(page_id) == 32:
            return f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"
    
    return None


class NotionClient:
    """Wrapper around Notion API client"""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize Notion client.
        
        Args:
            api_token: Notion integration token. If None, reads from NOTION_API_TOKEN env var.
        
        Raises:
            ImportError: If notion-client is not installed
            ValueError: If API token is not provided
        """
        if not NOTION_AVAILABLE:
            raise ImportError(
                "notion-client library is not installed. "
                "Install it with: pip install notion-client"
            )
        
        self.api_token = api_token or os.getenv("NOTION_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "Notion API token is required. "
                "Set NOTION_API_TOKEN environment variable or pass api_token parameter."
            )
        
        self.client = Client(auth=self.api_token)
        self.workspace_id: Optional[str] = None
        self.team_space_id: Optional[str] = None
    
    def test_connection(self) -> bool:
        """
        Test connection to Notion API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to list users to verify connection
            user = self.client.users.me()
            return True
        except Exception as e:
            print(f"[ERROR] Notion connection failed: {e}")
            return False
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """
        Get current user information.
        
        Returns:
            User information dict or None if failed
        """
        try:
            return self.client.users.me()
        except Exception as e:
            print(f"[ERROR] Failed to get user info: {e}")
            return None
    
    def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a page by ID.
        
        Args:
            page_id: Page ID (with or without hyphens)
        
        Returns:
            Page object or None if not found
        """
        try:
            # Normalize page ID (remove hyphens if present)
            clean_id = page_id.replace('-', '')
            formatted_id = f"{clean_id[:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:]}"
            return self.client.pages.retrieve(page_id=formatted_id)
        except Exception as e:
            print(f"[ERROR] Failed to retrieve page: {e}")
            return None
    
    def list_databases(self, page_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List databases accessible to the integration.
        
        Args:
            page_id: Optional parent page ID to search within
        
        Returns:
            List of database objects
        """
        try:
            if page_id:
                # Search for databases within a specific page
                clean_id = page_id.replace('-', '')
                formatted_id = f"{clean_id[:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:]}"
                response = self.client.search(
                    filter={"value": "database", "property": "object"},
                    parent={"page_id": formatted_id}
                )
            else:
                # Search all accessible databases
                response = self.client.search(
                    filter={"value": "database", "property": "object"}
                )
            return response.get("results", [])
        except Exception as e:
            print(f"[ERROR] Failed to list databases: {e}")
            return []
    
    def create_page(self, parent_id: str, title: str, content: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Create a new page in Notion.
        
        Args:
            parent_id: ID of parent page/database
            title: Page title
            content: Optional list of page content blocks
        
        Returns:
            Created page object
        """
        page_properties = {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }
        
        # Normalize page ID
        clean_id = parent_id.replace('-', '')
        formatted_id = f"{clean_id[:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:]}"
        
        page_data = {
            "parent": {"type": "page_id", "page_id": formatted_id},
            "properties": page_properties
        }
        
        if content:
            page_data["children"] = content
        
        return self.client.pages.create(**page_data)
    
    def create_database(
        self,
        parent_id: str,
        title: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new database in Notion.
        
        Args:
            parent_id: ID of parent page
            title: Database title
            properties: Database property definitions
        
        Returns:
            Created database object
        """
        # Normalize page ID (remove hyphens if present, then format)
        clean_id = parent_id.replace('-', '')
        formatted_id = f"{clean_id[:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:]}"
        
        database_data = {
            "parent": {"type": "page_id", "page_id": formatted_id},
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ],
            "properties": properties
        }
        
        return self.client.databases.create(**database_data)
    
    def add_page_to_database(
        self,
        database_id: str,
        properties: Dict[str, Any],
        content: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Add a page (row) to a database.
        
        Args:
            database_id: Database ID
            properties: Property values for the page
            content: Optional page content blocks
        
        Returns:
            Created page object
        """
        page_data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        
        if content:
            page_data["children"] = content
        
        return self.client.pages.create(**page_data)
    
    def update_page(
        self,
        page_id: str,
        properties: Optional[Dict[str, Any]] = None,
        content: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing page.
        
        Args:
            page_id: Page ID to update
            properties: Property values to update
            content: Content blocks to update
        
        Returns:
            Updated page object
        """
        update_data = {}
        
        if properties:
            update_data["properties"] = properties
        
        if content:
            update_data["children"] = content
        
        return self.client.pages.update(page_id, **update_data)
    
    def append_blocks(self, page_id: str, blocks: List[Dict]) -> Dict[str, Any]:
        """
        Append content blocks to a page.
        
        Args:
            page_id: Page ID
            blocks: List of block objects to append
        
        Returns:
            API response
        """
        return self.client.blocks.children.append(block_id=page_id, children=blocks)


class NotionIntegration:
    """
    Notion Integration for team workspace management.
    Handles creating team space structure and syncing documentation.
    """
    
    def __init__(self, api_token: Optional[str] = None, team_space_id: Optional[str] = None, team_space_url: Optional[str] = None):
        """
        Initialize Notion integration.
        
        Args:
            api_token: Notion integration token
            team_space_id: Optional team space page ID (if already exists)
            team_space_url: Optional Notion URL (will extract page ID from it)
        """
        self.client = NotionClient(api_token)
        
        # Extract page ID from URL if provided
        if team_space_url and not team_space_id:
            team_space_id = extract_page_id_from_url(team_space_url)
            if team_space_id:
                print(f"[INFO] Extracted page ID from URL: {team_space_id}")
        
        self.team_space_id = team_space_id
        self.databases: Dict[str, str] = {}  # Maps database name to ID
        self.doc_folders: Dict[str, str] = {}  # Maps doc type to folder ID
    
    def create_team_space(self, workspace_name: str = "Product Team Workspace") -> str:
        """
        Create the team workspace structure in Notion.
        
        This creates:
        - Main team space page
        - Projects database
        - Executive Summaries database
        - Key Decisions Log database
        - OKRs/Goals database
        - Key Results database
        - Documentation pages
        
        Args:
            workspace_name: Name for the team workspace
        
        Returns:
            Team space page ID
        """
        if not self.client.test_connection():
            raise ConnectionError("Cannot connect to Notion API. Check your API token.")
        
        print(f"[INFO] Creating team workspace: {workspace_name}")
        
        # Note: Notion API doesn't support creating top-level pages directly.
        # The user needs to create a page manually and share it with the integration,
        # or we use an existing page ID.
        # For now, we'll assume team_space_id is provided or create structure within it.
        
        if not self.team_space_id:
            raise ValueError(
                "team_space_id is required. "
                "Create a page in Notion, share it with your integration, and provide the page ID."
            )
        
        # Create main documentation structure
        self._create_documentation_structure()
        
        # Create databases for Head of Product/CEO oversight
        self._create_projects_database()
        self._create_executive_summaries_database()
        self._create_decisions_log_database()
        self._create_okrs_database()
        self._create_key_results_database()
        
        print(f"[OK] Team workspace created successfully!")
        print(f"[INFO] Team Space ID: {self.team_space_id}")
        
        return self.team_space_id
    
    def _create_documentation_structure(self):
        """Create documentation pages structure"""
        print("[INFO] Creating documentation structure...")
        
        # Create Documentation section
        doc_section = self.client.create_page(
            parent_id=self.team_space_id,
            title="📚 Documentation"
        )
        
        # Create sub-pages for different documentation types
        doc_pages = {
            "Project Briefs": "PROJECT_BRIEF",
            "Architecture Docs": "ARCHITECTURE",
            "ADRs (Architecture Decision Records)": "ADR",
            "Changelogs": "CHANGELOG",
            "User Stories": "USER_STORY",
            "Bug Reports": "BUG_REPORT"
        }
        
        for page_name, doc_type in doc_pages.items():
            folder_page = self.client.create_page(
                parent_id=doc_section["id"],
                title=page_name
            )
            # Cache folder ID for later use
            self.doc_folders[doc_type] = folder_page["id"]
            # Also cache by folder name for README and GOVERNANCE
            if doc_type == "PROJECT_BRIEF":
                self.doc_folders["README"] = folder_page["id"]
            if doc_type == "ARCHITECTURE":
                self.doc_folders["GOVERNANCE"] = folder_page["id"]
        
        print("[OK] Documentation structure created")
    
    def _create_projects_database(self):
        """Create Projects database"""
        print("[INFO] Creating Projects database...")
        
        properties = {
            "Project Name": {"title": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Discovery", "color": "blue"},
                        {"name": "Active", "color": "green"},
                        {"name": "On Hold", "color": "yellow"},
                        {"name": "Complete", "color": "gray"},
                        {"name": "Cancelled", "color": "red"}
                    ]
                }
            },
            "Product Owner": {"people": {}},
            "Start Date": {"date": {}},
            "Target Completion": {"date": {}},
            "Product Goal": {"rich_text": {}},
            "North Star Metric": {"rich_text": {}},
            "Current Metric Value": {"number": {}},
            "Target Metric Value": {"number": {}},
            "RICE Score": {"number": {}},
            "Strategic Priority": {
                "select": {
                    "options": [
                        {"name": "Critical", "color": "red"},
                        {"name": "High", "color": "orange"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "Low", "color": "gray"}
                    ]
                }
            },
            "Resources Allocated": {"number": {}},
            "Last Updated": {"last_edited_time": {}}
        }
        
        db = self.client.create_database(
            parent_id=self.team_space_id,
            title="📊 Projects",
            properties=properties
        )
        
        self.databases["projects"] = db["id"]
        print("[OK] Projects database created")
    
    def _create_executive_summaries_database(self):
        """Create Executive Summaries database"""
        print("[INFO] Creating Executive Summaries database...")
        
        properties = {
            "Summary Title": {"title": {}},
            "Project": {
                "relation": {
                    "database_id": self.databases.get("projects", ""),
                    "type": "dual_property",
                    "dual_property": {}
                }
            },
            "Sprint Number": {"number": {}},
            "Report Date": {"date": {}},
            "Sprint Goal": {"rich_text": {}},
            "Sprint Goal Achieved": {"checkbox": {}},
            "Key Accomplishments": {"rich_text": {}},
            "Metrics Update": {"rich_text": {}},
            "Challenges & Risks": {"rich_text": {}},
            "Decisions Made": {"rich_text": {}},
            "Help Needed": {"rich_text": {}},
            "Next Sprint Focus": {"rich_text": {}},
            "Confidence Level": {
                "select": {
                    "options": [
                        {"name": "High", "color": "green"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "Low", "color": "red"}
                    ]
                }
            },
            "Product Owner": {"people": {}},
            "Created By": {"created_by": {}}
        }
        
        db = self.client.create_database(
            parent_id=self.team_space_id,
            title="📋 Executive Summaries",
            properties=properties
        )
        
        self.databases["executive_summaries"] = db["id"]
        print("[OK] Executive Summaries database created")
    
    def _create_decisions_log_database(self):
        """Create Key Decisions Log database"""
        print("[INFO] Creating Key Decisions Log database...")
        
        properties = {
            "Decision": {"title": {}},
            "Project": {
                "relation": {
                    "database_id": self.databases.get("projects", ""),
                    "type": "dual_property",
                    "dual_property": {}
                }
            },
            "Date": {"date": {}},
            "Decision Type": {
                "select": {
                    "options": [
                        {"name": "Strategic", "color": "red"},
                        {"name": "Product", "color": "orange"},
                        {"name": "Technical", "color": "blue"},
                        {"name": "Resource Allocation", "color": "yellow"},
                        {"name": "Go/No-Go", "color": "purple"}
                    ]
                }
            },
            "Decision Maker(s)": {"people": {}},
            "Context": {"rich_text": {}},
            "Options Considered": {"rich_text": {}},
            "Decision Rationale": {"rich_text": {}},
            "Expected Outcome": {"rich_text": {}},
            "Actual Outcome": {"rich_text": {}},
            "Review Date": {"date": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Pending", "color": "yellow"},
                        {"name": "Implemented", "color": "green"},
                        {"name": "Under Review", "color": "blue"},
                        {"name": "Reversed", "color": "red"}
                    ]
                }
            },
            "Related ADR": {"url": {}}
        }
        
        db = self.client.create_database(
            parent_id=self.team_space_id,
            title="📝 Key Decisions Log",
            properties=properties
        )
        
        self.databases["decisions"] = db["id"]
        print("[OK] Key Decisions Log database created")
    
    def _create_okrs_database(self):
        """Create OKRs/Goals database"""
        print("[INFO] Creating OKRs/Goals database...")
        
        properties = {
            "Objective": {"title": {}},
            "Quarter": {
                "select": {
                    "options": [
                        {"name": "Q1 2026", "color": "blue"},
                        {"name": "Q2 2026", "color": "green"},
                        {"name": "Q3 2026", "color": "yellow"},
                        {"name": "Q4 2026", "color": "orange"}
                    ]
                }
            },
            "Owner": {"people": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "On Track", "color": "green"},
                        {"name": "At Risk", "color": "yellow"},
                        {"name": "Off Track", "color": "red"},
                        {"name": "Complete", "color": "gray"}
                    ]
                }
            },
            "Progress": {"number": {}},
            "Last Updated": {"last_edited_time": {}}
        }
        
        db = self.client.create_database(
            parent_id=self.team_space_id,
            title="🎯 OKRs/Goals",
            properties=properties
        )
        
        self.databases["okrs"] = db["id"]
        print("[OK] OKRs/Goals database created")
    
    def _create_key_results_database(self):
        """Create Key Results database"""
        print("[INFO] Creating Key Results database...")
        
        properties = {
            "Key Result": {"title": {}},
            "Objective": {
                "relation": {
                    "database_id": self.databases.get("okrs", ""),
                    "type": "dual_property",
                    "dual_property": {}
                }
            },
            "Target": {"number": {}},
            "Current": {"number": {}},
            "Unit": {"rich_text": {}},
            "Due Date": {"date": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "On Track", "color": "green"},
                        {"name": "At Risk", "color": "yellow"},
                        {"name": "Off Track", "color": "red"},
                        {"name": "Complete", "color": "gray"}
                    ]
                }
            },
            "Update Frequency": {
                "select": {
                    "options": [
                        {"name": "Weekly", "color": "blue"},
                        {"name": "Bi-weekly", "color": "green"},
                        {"name": "Monthly", "color": "yellow"}
                    ]
                }
            },
            "Last Updated": {"last_edited_time": {}}
        }
        
        db = self.client.create_database(
            parent_id=self.team_space_id,
            title="📈 Key Results",
            properties=properties
        )
        
        self.databases["key_results"] = db["id"]
        print("[OK] Key Results database created")
    
    def _find_documentation_folders(self):
        """Find documentation folders by searching the workspace"""
        if not self.team_space_id or self.doc_folders:
            return  # Already have folders or no workspace
        
        try:
            # Search for pages in the workspace
            response = self.client.client.search(
                filter={"value": "page", "property": "object"},
                sort={"direction": "ascending", "timestamp": "last_edited_time"}
            )
            
            # Map of folder names to doc types
            folder_mapping = {
                "Project Briefs": ["PROJECT_BRIEF", "README"],
                "Architecture Docs": ["ARCHITECTURE", "GOVERNANCE"],
                "ADRs (Architecture Decision Records)": ["ADR"],
                "Changelogs": ["CHANGELOG"],
                "User Stories": ["USER_STORY"],
                "Bug Reports": ["BUG_REPORT"]
            }
            
            # Find Documentation section first
            doc_section_id = None
            for page in response.get("results", []):
                props = page.get("properties", {})
                title_prop = props.get("title", {})
                if title_prop.get("title"):
                    title = title_prop["title"][0].get("plain_text", "")
                    if "Documentation" in title:
                        doc_section_id = page["id"]
                        break
            
            if not doc_section_id:
                return  # Documentation section not found
            
            # Find folders within Documentation section
            children_response = self.client.client.blocks.children.list(block_id=doc_section_id)
            for child in children_response.get("results", []):
                if child.get("type") == "child_page":
                    child_id = child.get("id")
                    child_page = self.client.get_page(child_id)
                    if child_page:
                        props = child_page.get("properties", {})
                        title_prop = props.get("title", {})
                        if title_prop.get("title"):
                            folder_name = title_prop["title"][0].get("plain_text", "")
                            for doc_types in folder_mapping.get(folder_name, []):
                                self.doc_folders[doc_types] = child_id
        except Exception as e:
            print(f"[WARNING] Could not find documentation folders: {e}")
    
    def _get_documentation_folder_id(self, doc_type: str) -> Optional[str]:
        """
        Get the folder ID for a specific documentation type.
        Uses cached folder IDs from setup, or searches for them, or falls back to team space.
        
        Args:
            doc_type: Type of documentation (PROJECT_BRIEF, ADR, CHANGELOG, etc.)
        
        Returns:
            Folder page ID or team_space_id as fallback
        """
        # Try to find folders if not cached
        if not self.doc_folders:
            self._find_documentation_folders()
        
        # Return cached folder ID if available
        folder_id = self.doc_folders.get(doc_type)
        if folder_id:
            return folder_id
        
        # Fallback to team space if folder not found
        return self.team_space_id
    
    def sync_documentation(
        self,
        doc_type: str,
        title: str,
        content: str,
        project_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Sync documentation to Notion, organized by type.
        
        Args:
            doc_type: Type of documentation (PROJECT_BRIEF, ADR, CHANGELOG, etc.)
            title: Document title
            content: Document content (markdown)
            project_name: Optional project name for organization
        
        Returns:
            Created page ID if successful, None otherwise
        """
        if not self.team_space_id:
            print("[WARNING] Team space not initialized. Cannot sync documentation.")
            return None
        
        try:
            # Get the appropriate parent folder for this doc type
            parent_id = self._get_documentation_folder_id(doc_type)
            
            # Convert markdown to Notion blocks
            blocks = self._markdown_to_notion_blocks(content)
            
            # Add metadata block at the top (simplified - no annotations in callout)
            metadata_blocks = [
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"Document Type: {doc_type} | Synced from Cursor"
                                }
                            }
                        ],
                        "icon": {"emoji": "📄"}
                    }
                }
            ]
            
            # Combine metadata with content
            all_blocks = metadata_blocks + blocks
            
            # Notion API limit: max 100 blocks per page creation
            # Create page with first 100 blocks, then append the rest
            initial_blocks = all_blocks[:100]
            remaining_blocks = all_blocks[100:]
            
            # Create page with initial blocks
            page = self.client.create_page(
                parent_id=parent_id,
                title=title,
                content=initial_blocks
            )
            
            # Append remaining blocks in chunks of 100
            if remaining_blocks:
                chunk_size = 100
                for i in range(0, len(remaining_blocks), chunk_size):
                    chunk = remaining_blocks[i:i + chunk_size]
                    self.client.append_blocks(page["id"], chunk)
            
            print(f"[OK] Documentation synced to Notion: {title} ({doc_type})")
            return page["id"]
        
        except Exception as e:
            print(f"[ERROR] Failed to sync documentation: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _markdown_to_notion_blocks(self, markdown: str) -> List[Dict]:
        """
        Convert markdown content to Notion blocks.
        
        This is a simplified converter. For production, consider using
        a more robust markdown-to-Notion converter library.
        
        Args:
            markdown: Markdown content
        
        Returns:
            List of Notion block objects
        """
        blocks = []
        lines = markdown.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Headers
            if line.startswith('# '):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]
                    }
                })
            elif line.startswith('## '):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:].strip()}}]
                    }
                })
            elif line.startswith('### '):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:].strip()}}]
                    }
                })
            # Bullet lists
            elif line.startswith('- ') or line.startswith('* '):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]
                    }
                })
            # Code blocks (simplified)
            elif line.startswith('```'):
                # Skip code block markers for now
                continue
            # Regular paragraphs
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": line}}]
                    }
                })
        
        return blocks
    
    def get_database_id(self, database_name: str) -> Optional[str]:
        """Get database ID by name"""
        return self.databases.get(database_name)
    
    def save_config(self, config_path: str = "notion_config.json"):
        """Save Notion configuration (database IDs, folder IDs, etc.)"""
        config = {
            "team_space_id": self.team_space_id,
            "databases": self.databases,
            "doc_folders": self.doc_folders
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"[OK] Notion configuration saved to {config_path}")
    
    def load_config(self, config_path: str = "notion_config.json"):
        """Load Notion configuration"""
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                team_space_id = config.get("team_space_id")
                # Handle URL in config
                if team_space_id and team_space_id.startswith("http"):
                    team_space_id = extract_page_id_from_url(team_space_id)
                self.team_space_id = team_space_id
                self.databases = config.get("databases", {})
                self.doc_folders = config.get("doc_folders", {})
                print(f"[OK] Notion configuration loaded from {config_path}")
        else:
            print(f"[WARNING] Configuration file not found: {config_path}")
    
    def verify_workspace_access(self) -> bool:
        """
        Verify that the integration has access to the team workspace.
        
        Returns:
            True if access is verified, False otherwise
        """
        if not self.team_space_id:
            print("[ERROR] Team space ID not set")
            return False
        
        page = self.client.get_page(self.team_space_id)
        if page:
            print(f"[OK] Successfully accessed workspace: {page.get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'Unknown')}")
            return True
        else:
            print("[ERROR] Cannot access workspace. Make sure:")
            print("  1. The page is shared with your Notion integration")
            print("  2. The page ID is correct")
            print("  3. Your integration has the necessary permissions")
            return False
    
    def list_existing_databases(self) -> Dict[str, str]:
        """
        List all databases in the team workspace and match them by name.
        
        Returns:
            Dictionary mapping database names to IDs
        """
        if not self.team_space_id:
            return {}
        
        databases = self.client.list_databases(self.team_space_id)
        db_map = {}
        
        for db in databases:
            # Notion database titles are in title array
            title_prop = db.get("title", [])
            if title_prop:
                db_name = title_prop[0].get("plain_text", "")
                db_map[db_name] = db["id"]
        
        return db_map
    
    def get_database_by_name(self, database_name: str) -> Optional[str]:
        """
        Get database ID by name from existing databases.
        
        Args:
            database_name: Name of the database to find
        
        Returns:
            Database ID if found, None otherwise
        """
        existing_dbs = self.list_existing_databases()
        return existing_dbs.get(database_name)
    
    def sync_from_notion(self, database_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Read data from a Notion database (bidirectional sync).
        
        Args:
            database_name: Name of the database to read from
            limit: Maximum number of records to retrieve
        
        Returns:
            List of database entries
        """
        database_id = self.get_database_id(database_name) or self.get_database_by_name(database_name)
        if not database_id:
            print(f"[ERROR] Database '{database_name}' not found")
            return []
        
        try:
            response = self.client.client.databases.query(
                database_id=database_id,
                page_size=min(limit, 100)  # Notion API limit is 100
            )
            return response.get("results", [])
        except Exception as e:
            print(f"[ERROR] Failed to read from database: {e}")
            return []
