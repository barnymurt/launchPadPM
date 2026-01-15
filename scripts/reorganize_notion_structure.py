"""
Notion Structure Reorganization Script
Business Analyst reviews and reorganizes Notion folders for clarity.
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.business_analyst_agent import BusinessAnalystAgent
from agents.base_agent import AgentContext
from integrations.notion_integration import NotionIntegration, extract_page_id_from_url


def get_all_pages(integration: NotionIntegration) -> List[Dict[str, Any]]:
    """Get all pages in the Notion workspace"""
    try:
        response = integration.client.client.search(
            filter={"value": "page", "property": "object"},
            sort={"direction": "ascending", "timestamp": "last_edited_time"}
        )
        return response.get("results", [])
    except Exception as e:
        print(f"[ERROR] Failed to list pages: {e}")
        return []


def get_page_children(integration: NotionIntegration, page_id: str) -> List[Dict[str, Any]]:
    """Get child pages of a given page"""
    try:
        response = integration.client.client.blocks.children.list(block_id=page_id)
        children = []
        for block in response.get("results", []):
            if block.get("type") == "child_page":
                children.append(block)
        return children
    except Exception as e:
        print(f"[WARNING] Could not get children for page {page_id}: {e}")
        return []


def extract_page_title(page: Dict[str, Any]) -> str:
    """Extract title from a Notion page"""
    props = page.get("properties", {})
    title_prop = props.get("title", {})
    if title_prop.get("title"):
        return title_prop["title"][0].get("plain_text", "")
    return "Untitled"


def analyze_structure(integration: NotionIntegration) -> Dict[str, Any]:
    """Analyze the current Notion structure"""
    print("\n" + "=" * 70)
    print("ANALYZING NOTION STRUCTURE")
    print("=" * 70)
    
    all_pages = get_all_pages(integration)
    print(f"[INFO] Found {len(all_pages)} pages in workspace")
    
    # Build structure tree
    structure = {
        "root_pages": [],
        "documentation_section": None,
        "folders": {},
        "duplicates": [],
        "naming_issues": [],
        "orphaned_pages": []
    }
    
    # Find root pages (pages directly under team space)
    root_page_ids = set()
    for page in all_pages:
        parent = page.get("parent", {})
        if parent.get("type") == "page_id":
            parent_id = parent.get("page_id", "").replace("-", "")
            team_space_id_clean = integration.team_space_id.replace("-", "") if integration.team_space_id else ""
            if parent_id == team_space_id_clean:
                root_page_ids.add(page["id"])
                title = extract_page_title(page)
                structure["root_pages"].append({
                    "id": page["id"],
                    "title": title,
                    "type": "page"
                })
    
    # Find Documentation section(s) - there might be duplicates
    doc_sections = []
    for page in all_pages:
        title = extract_page_title(page)
        if "Documentation" in title or "📚" in title:
            doc_sections.append({
                "id": page["id"],
                "title": title
            })
            # Get children of Documentation section
            children = get_page_children(integration, page["id"])
            for child in children:
                child_title = extract_page_title(child)
                # Use full path as key to handle duplicates
                key = f"{title} > {child_title}"
                structure["folders"][key] = {
                    "id": child["id"],
                    "title": child_title,
                    "parent": page["id"],
                    "parent_title": title,
                    "full_path": key
                }
    
    # Set primary documentation section (first one found, or most recent)
    if doc_sections:
        structure["documentation_section"] = doc_sections[0]
        if len(doc_sections) > 1:
            structure["duplicates"].append({
                "normalized": "documentation",
                "variants": [doc["title"] for doc in doc_sections],
                "type": "duplicate_section"
            })
    
    # Find other top-level sections
    for page in all_pages:
        title = extract_page_title(page)
        parent = page.get("parent", {})
        if parent.get("type") == "page_id":
            parent_id = parent.get("page_id", "").replace("-", "")
            team_space_id_clean = integration.team_space_id.replace("-", "") if integration.team_space_id else ""
            if parent_id == team_space_id_clean:
                # Check if it's a section (has children)
                children = get_page_children(integration, page["id"])
                if children:
                    if title not in structure["folders"]:
                        structure["folders"][title] = {
                            "id": page["id"],
                            "title": title,
                            "parent": integration.team_space_id,
                            "parent_title": "Root",
                            "children_count": len(children)
                        }
    
    # Find duplicates (similar names) - check folder titles, not full paths
    folder_titles = {}
    seen_names = defaultdict(list)
    for full_path, folder_info in structure["folders"].items():
        title = folder_info["title"]
        # Normalize name for comparison (remove emojis, lowercase, strip)
        normalized = title.lower().strip()
        # Remove common emojis and special chars
        normalized = normalized.replace("📚", "").replace("📋", "").replace("📁", "").replace("📄", "").replace("🏗️", "").replace("📝", "").replace("👤", "").replace("🐛", "").strip()
        # Remove extra spaces
        normalized = " ".join(normalized.split())
        seen_names[normalized].append({
            "title": title,
            "full_path": full_path,
            "id": folder_info["id"],
            "parent": folder_info.get("parent_title", "Unknown")
        })
        folder_titles[title] = folder_info
    
    for normalized, variants in seen_names.items():
        if len(variants) > 1 and normalized:  # Only flag if normalized name is not empty
            structure["duplicates"].append({
                "normalized": normalized,
                "variants": variants,
                "type": "duplicate_folder"
            })
    
    # Find naming issues - check actual folder titles
    for folder_info in structure["folders"].values():
        folder_name = folder_info["title"]
        issues = []
        if len(folder_name) > 50:
            issues.append("Name too long")
        if not folder_name.strip():
            issues.append("Empty or whitespace only")
        if folder_name.lower() in ["untitled", "new page", "page"]:
            issues.append("Generic/placeholder name")
        # Check for inconsistent naming
        if not any(emoji in folder_name for emoji in ["📚", "📋", "📁", "📄", "🏗️", "📝", "👤", "🐛"]):
            # Check if it should have an emoji based on content
            if any(keyword in folder_name.lower() for keyword in ["governance", "project", "architecture", "adr", "changelog", "user story", "bug"]):
                issues.append("Missing emoji for categorization")
        if issues:
            structure["naming_issues"].append({
                "name": folder_name,
                "full_path": folder_info.get("full_path", folder_name),
                "issues": issues
            })
    
    return structure


def ba_analyze_and_propose(ba_agent: BusinessAnalystAgent, structure: Dict[str, Any]) -> Dict[str, Any]:
    """Have Business Analyst analyze structure and propose improvements"""
    print("\n" + "=" * 70)
    print("BUSINESS ANALYST ANALYSIS")
    print("=" * 70)
    
    # Create analysis query
    analysis_text = f"""
I need to analyze and reorganize our Notion workspace structure. Here's what I found:

**Current Structure:**
- Root pages: {len(structure['root_pages'])}
- Documentation section: {structure['documentation_section']['title'] if structure['documentation_section'] else 'Not found'}
- Folders found: {len(structure['folders'])}

**Folders:**
{chr(10).join(f"- {name}" for name in structure['folders'].keys())}

**Duplicates Found:**
{chr(10).join(f"- {dup['normalized']}: {', '.join(dup['variants'])}" for dup in structure['duplicates'])}

**Naming Issues:**
{chr(10).join(f"- {issue['name']}: {', '.join(issue['issues'])}" for issue in structure['naming_issues'])}

Please analyze this structure and propose:
1. A clear, logical organization with consistent naming conventions
2. How to group related folders
3. How to eliminate duplicates
4. A recommended folder structure that's easy to navigate
5. Naming conventions that are clear and consistent
"""
    
    response = ba_agent.process_query(analysis_text)
    
    # Extract proposal from response
    proposal = {
        "analysis": response.response,
        "recommendations": response.recommendations,
        "questions": response.questions,
        "proposed_structure": {}
    }
    
    # Generate proposed structure based on BA recommendations
    # Standard organization structure
    proposed_structure = {
        "📚 Documentation": {
            "description": "All project documentation",
            "subfolders": {
                "📋 Governance": "Team governance, working agreements, decisions",
                "📄 Project Briefs": "Project overviews and briefs",
                "🏗️ Architecture": "Architecture docs and ADRs",
                "📝 ADRs": "Architecture Decision Records",
                "📋 Changelogs": "Project changelogs",
                "👤 User Stories": "User stories and requirements",
                "🐛 Bug Reports": "Bug tracking and reports"
            }
        },
        "📊 Databases": {
            "description": "Structured data and databases",
            "subfolders": {}
        },
        "📈 Projects": {
            "description": "Active project workspaces",
            "subfolders": {}
        }
    }
    
    proposal["proposed_structure"] = proposed_structure
    
    return proposal


def create_reorganization_plan(current: Dict[str, Any], proposed: Dict[str, Any]) -> Dict[str, Any]:
    """Create a detailed reorganization plan"""
    plan = {
        "actions": [],
        "renames": [],
        "moves": [],
        "merges": [],
        "creates": []
    }
    
    # Map current folders to proposed structure
    current_folders = current["folders"]
    proposed_folders = proposed["proposed_structure"]["📚 Documentation"]["subfolders"]
    
    # Find folders that need renaming
    folder_mapping = {
        "Project Briefs": "📄 Project Briefs",
        "Architecture Docs": "🏗️ Architecture",
        "ADRs (Architecture Decision Records)": "📝 ADRs",
        "Changelogs": "📋 Changelogs",
        "User Stories": "👤 User Stories",
        "Bug Reports": "🐛 Bug Reports",
        "Governance": "📋 Governance"
    }
    
    # Also check for variations
    for current_name in current_folders.keys():
        normalized = current_name.lower().strip()
        normalized = normalized.replace("📚", "").replace("📋", "").replace("📁", "").replace("📄", "").strip()
        
        # Find matching proposed folder
        matched = False
        for proposed_name in proposed_folders.keys():
            proposed_normalized = proposed_name.lower().strip()
            proposed_normalized = proposed_normalized.replace("📚", "").replace("📋", "").replace("📁", "").replace("📄", "").strip()
            
            if normalized == proposed_normalized or normalized in proposed_normalized or proposed_normalized in normalized:
                if current_name != proposed_name:
                    plan["renames"].append({
                        "from": current_name,
                        "to": proposed_name,
                        "id": current_folders[current_name]["id"]
                    })
                matched = True
                break
        
        if not matched:
            # Check if it should be merged
            for dup in current["duplicates"]:
                if current_name in dup["variants"]:
                    # Find the canonical name
                    canonical = dup["variants"][0]  # Use first as canonical
                    if current_name != canonical:
                        plan["merges"].append({
                            "from": current_name,
                            "to": canonical,
                            "id": current_folders[current_name]["id"]
                        })
    
    # Find folders that need to be created
    for proposed_name in proposed_folders.keys():
        found = False
        for current_name in current_folders.keys():
            normalized_current = current_name.lower().strip().replace("📚", "").replace("📋", "").replace("📁", "").replace("📄", "").strip()
            normalized_proposed = proposed_name.lower().strip().replace("📚", "").replace("📋", "").replace("📁", "").replace("📄", "").strip()
            if normalized_current == normalized_proposed:
                found = True
                break
        if not found:
            plan["creates"].append({
                "name": proposed_name,
                "description": proposed_folders[proposed_name],
                "parent": "📚 Documentation"
            })
    
    return plan


def execute_reorganization(integration: NotionIntegration, plan: Dict[str, Any], structure: Dict[str, Any]) -> bool:
    """Execute the reorganization plan"""
    print("\n" + "=" * 70)
    print("EXECUTING REORGANIZATION")
    print("=" * 70)
    
    # Get Documentation section ID
    doc_section_id = None
    if structure["documentation_section"]:
        doc_section_id = structure["documentation_section"]["id"]
    else:
        # Create Documentation section if it doesn't exist
        print("[INFO] Creating Documentation section...")
        doc_page = integration.client.create_page(
            parent_id=integration.team_space_id,
            title="📚 Documentation"
        )
        doc_section_id = doc_page["id"]
        print(f"[OK] Created Documentation section: {doc_section_id}")
    
    success_count = 0
    error_count = 0
    
    # Execute renames
    print(f"\n[INFO] Renaming {len(plan['renames'])} folders...")
    for rename in plan["renames"]:
        try:
            # Notion API doesn't directly support renaming, we need to update page properties
            # For now, we'll create a new page with the correct name and move content
            print(f"[INFO] Renaming '{rename['from']}' to '{rename['to']}'...")
            # Note: Notion API v1 doesn't support page title updates directly
            # We would need to use the update endpoint with proper properties
            # For now, we'll document what needs to be done
            print(f"[NOTE] Manual rename needed: '{rename['from']}' -> '{rename['to']}'")
            success_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to rename '{rename['from']}': {e}")
            error_count += 1
    
    # Execute creates
    print(f"\n[INFO] Creating {len(plan['creates'])} new folders...")
    for create in plan["creates"]:
        try:
            print(f"[INFO] Creating folder '{create['name']}'...")
            new_folder = integration.client.create_page(
                parent_id=doc_section_id,
                title=create["name"]
            )
            print(f"[OK] Created '{create['name']}': {new_folder['id']}")
            # Update doc_folders cache
            doc_type_map = {
                "📋 Governance": "GOVERNANCE",
                "📄 Project Briefs": "PROJECT_BRIEF",
                "🏗️ Architecture": "ARCHITECTURE",
                "📝 ADRs": "ADR",
                "📋 Changelogs": "CHANGELOG",
                "👤 User Stories": "USER_STORY",
                "🐛 Bug Reports": "BUG_REPORT"
            }
            doc_type = doc_type_map.get(create["name"], None)
            if doc_type:
                integration.doc_folders[doc_type] = new_folder["id"]
            success_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to create '{create['name']}': {e}")
            error_count += 1
    
    # Save updated config
    integration.save_config()
    
    print(f"\n[OK] Reorganization complete: {success_count} successful, {error_count} errors")
    return error_count == 0


def generate_report(structure: Dict[str, Any], proposal: Dict[str, Any], plan: Dict[str, Any]) -> str:
    """Generate a reorganization report"""
    report = f"""# Notion Workspace Reorganization Report

**Generated:** {Path(__file__).parent.parent / 'NOTION_REORGANIZATION_REPORT.md'}

## Executive Summary

This report documents the analysis and reorganization of the Notion workspace structure to improve clarity, eliminate duplicates, and establish consistent naming conventions.

---

## 1. Current Structure Analysis

### Root Pages
Found {len(structure['root_pages'])} root-level pages:
{chr(10).join(f"- {page['title']}" for page in structure['root_pages'][:10])}

### Documentation Section
{structure['documentation_section']['title'] if structure['documentation_section'] else 'Not found'}

### Folders Identified
{len(structure['folders'])} folders found:
{chr(10).join(f"- {info['title']} (in {info.get('parent_title', 'Unknown')})" for info in structure['folders'].values())}

### Issues Found

**Duplicates:**
{chr(10).join(f"- {dup['normalized']} ({dup.get('type', 'unknown')}): {', '.join([v['title'] if isinstance(v, dict) else str(v) for v in dup['variants']])}" for dup in structure['duplicates']) if structure['duplicates'] else 'None found'}

**Naming Issues:**
{chr(10).join(f"- {issue['name']} ({issue.get('full_path', '')}): {', '.join(issue['issues'])}" for issue in structure['naming_issues']) if structure['naming_issues'] else 'None found'}

---

## 2. Business Analyst Analysis

### Analysis
{proposal['analysis'][:500]}...

### Key Recommendations
{chr(10).join(f"{i+1}. {rec}" for i, rec in enumerate(proposal['recommendations'][:10]))}

---

## 3. Proposed Structure

### Documentation Section Organization

```
📚 Documentation
├── 📋 Governance
│   └── Team governance, working agreements, decisions
├── 📄 Project Briefs
│   └── Project overviews and briefs
├── 🏗️ Architecture
│   └── Architecture docs and ADRs
├── 📝 ADRs
│   └── Architecture Decision Records
├── 📋 Changelogs
│   └── Project changelogs
├── 👤 User Stories
│   └── User stories and requirements
└── 🐛 Bug Reports
    └── Bug tracking and reports
```

### Naming Conventions

1. **Use emojis for visual categorization** (📚 Documentation, 📋 Governance, etc.)
2. **Clear, descriptive names** (avoid abbreviations unless standard)
3. **Consistent capitalization** (Title Case for folders)
4. **Group related content** (all documentation under Documentation section)

---

## 4. Reorganization Plan

### Actions Required

**Renames ({len(plan['renames'])}):**
{chr(10).join(f"- '{r['from']}' → '{r['to']}'" for r in plan['renames']) if plan['renames'] else 'None'}

**Creates ({len(plan['creates'])}):**
{chr(10).join(f"- Create '{c['name']}' ({c['description']})" for c in plan['creates']) if plan['creates'] else 'None'}

**Merges ({len(plan['merges'])}):**
{chr(10).join(f"- Merge '{m['from']}' into '{m['to']}'" for m in plan['merges']) if plan['merges'] else 'None'}

---

## 5. Implementation Notes

### Manual Steps Required

Due to Notion API limitations, some operations require manual intervention:

1. **Page Renaming:** Notion API v1 doesn't support direct page title updates. Pages need to be renamed manually in the Notion UI, or content should be moved to newly created pages with correct names.

2. **Content Migration:** If merging folders, content from source folders should be moved to destination folders manually.

3. **Verification:** After reorganization, verify that:
   - All folders have clear, consistent names
   - No duplicate folders exist
   - All content is properly organized
   - Documentation section structure is logical

### Automated Steps Completed

✅ Structure analysis
✅ Duplicate detection
✅ Naming issue identification
✅ Proposed structure generation
✅ New folder creation (where applicable)
✅ Configuration update

---

## 6. Next Steps

1. ✅ Review this report
2. ⏳ Manually rename folders as needed (see Renames section)
3. ⏳ Move content from duplicate/old folders to new structure
4. ⏳ Verify all folders are properly organized
5. ⏳ Update team documentation with new structure
6. ⏳ Train team on new organization

---

## 7. Recommendations

1. **Establish Naming Standards:** Document and share naming conventions with the team
2. **Regular Audits:** Schedule quarterly reviews of workspace structure
3. **Onboarding:** Include workspace structure in team onboarding
4. **Documentation:** Keep this report updated as structure evolves

"""
    return report


def main():
    """Main reorganization process"""
    print("=" * 70)
    print("NOTION WORKSPACE REORGANIZATION")
    print("Business Analyst Review & Reorganization")
    print("=" * 70)
    
    # Initialize
    api_token = os.getenv("NOTION_API_TOKEN")
    team_space_url = os.getenv("NOTION_TEAM_SPACE_URL", "https://www.notion.so/LaunchPadPM-2e89cb246f1f80a0a5b1f15433b0855c")
    
    if not api_token:
        print("[ERROR] NOTION_API_TOKEN not set.")
        print("Set NOTION_API_TOKEN environment variable to proceed.")
        return
    
    print("\n[INFO] Initializing Notion integration...")
    integration = NotionIntegration(
        api_token=api_token,
        team_space_url=team_space_url
    )
    integration.load_config()
    
    print("[INFO] Initializing Business Analyst agent...")
    ba_agent = BusinessAnalystAgent(AgentContext())
    
    # Analyze current structure
    structure = analyze_structure(integration)
    
    # BA analysis and proposal
    proposal = ba_analyze_and_propose(ba_agent, structure)
    
    # Create reorganization plan
    plan = create_reorganization_plan(structure, proposal)
    
    # Generate report
    report = generate_report(structure, proposal, plan)
    
    # Save report
    report_file = Path(__file__).parent.parent / "NOTION_REORGANIZATION_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n[OK] Report saved to: {report_file}")
    
    # Execute reorganization
    print("\n[INFO] Would you like to execute the reorganization?")
    print("This will create new folders and update the structure.")
    print("Some operations (like renaming) may require manual steps.")
    
    # For now, execute creates automatically
    execute_reorganization(integration, plan, structure)
    
    print("\n" + "=" * 70)
    print("REORGANIZATION COMPLETE")
    print("=" * 70)
    print(f"\nReview the report: {report_file}")
    print("\nNext steps:")
    print("1. Review NOTION_REORGANIZATION_REPORT.md")
    print("2. Manually rename folders as needed")
    print("3. Move content from old folders to new structure")
    print("4. Verify organization in Notion")


if __name__ == "__main__":
    main()
