#!/usr/bin/env python3
"""
Enhance SKILL.md files with quality rubric references.
Adds reference to QUALITY.md in the Quality Criteria section.
"""

import os
import re
from pathlib import Path

SKILLS_DIR = Path("skills")

QUALITY_REFERENCE_ADDITION = """
## Quality Rubric

For detailed quality standards and "What Good Looks Like" criteria, see [QUALITY.md](QUALITY.md).

"""

def enhance_skill_md(skill_dir: Path) -> bool:
    """Add quality rubric reference to SKILL.md."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return False
    
    quality_file = skill_dir / "QUALITY.md"
    if not quality_file.exists():
        return False
    
    content = skill_file.read_text(encoding='utf-8')
    
    # Check if already has quality rubric reference
    if "QUALITY.md" in content:
        return False
    
    # Find the Quality Criteria section and add reference after it
    pattern = r'(## Quality Criteria\n\n.*?)(\n## |\n## References|\n## Common Mistakes|$)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Insert after Quality Criteria section
        quality_section_end = match.end(1)
        new_content = content[:quality_section_end] + QUALITY_REFERENCE_ADDITION + content[quality_section_end:]
    else:
        # Find References section and insert before it
        ref_pattern = r'(\n## References\n)'
        ref_match = re.search(ref_pattern, content)
        if ref_match:
            pos = ref_match.start()
            new_content = content[:pos] + QUALITY_REFERENCE_ADDITION + content[pos:]
        else:
            # Append at the end
            new_content = content + QUALITY_REFERENCE_ADDITION
    
    skill_file.write_text(new_content, encoding='utf-8')
    return True

def main():
    """Enhance all SKILL.md files with quality rubric references."""
    enhanced = 0
    skipped = 0
    
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('_'):
            continue
        
        if enhance_skill_md(skill_dir):
            print(f"Enhanced: {skill_dir / 'SKILL.md'}")
            enhanced += 1
        else:
            skipped += 1
    
    print(f"\nEnhanced: {enhanced} SKILL.md files")
    print(f"Skipped: {skipped} (already have reference or missing QUALITY.md)")

if __name__ == "__main__":
    main()
