"""
Notion Integration
Handles connection to Notion.io and team workspace management.
"""

import os
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
            self.client.users.me()
            return True
        except Exception as e:
            print(f"[ERROR] Notion connection failed: {e}")
            return False
    
    def create_page(self, parent_id: str, title: str, content: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a new page in Notion.
        
        Args:
            parent_id: ID of parent page/database
            title: Page title
            content: Optional page content blocks
        
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
        
        page_data = {
            "parent": {"page_id": parent_id},
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
        database_data = {
            "parent": {"page_id": parent_id},
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
    
    def __init__(self, api_token: Optional[str] = None, team_space_id: Optional[str] = None):
        """
        Initialize Notion integration.
        
        Args:
            api_token: Notion integration token
            team_space_id: Optional team space page ID (if already exists)
        """
        self.client = NotionClient(api_token)
        self.team_space_id = team_space_id
        self.databases: Dict[str, str] = {}  # Maps database name to ID
    
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
            self.client.create_page(
                parent_id=doc_section["id"],
                title=page_name
            )
        
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
    
    def sync_documentation(
        self,
        doc_type: str,
        title: str,
        content: str,
        project_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Sync documentation to Notion.
        
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
            # Find or create documentation section
            # For now, create page directly in team space
            # In production, you'd want to organize by doc_type
            
            # Convert markdown to Notion blocks
            blocks = self._markdown_to_notion_blocks(content)
            
            page = self.client.create_page(
                parent_id=self.team_space_id,
                title=title,
                content=blocks
            )
            
            print(f"[OK] Documentation synced to Notion: {title}")
            return page["id"]
        
        except Exception as e:
            print(f"[ERROR] Failed to sync documentation: {e}")
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
        """Save Notion configuration (database IDs, etc.)"""
        config = {
            "team_space_id": self.team_space_id,
            "databases": self.databases
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
                self.team_space_id = config.get("team_space_id")
                self.databases = config.get("databases", {})
                print(f"[OK] Notion configuration loaded from {config_path}")
        else:
            print(f"[WARNING] Configuration file not found: {config_path}")
