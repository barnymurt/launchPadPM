#!/usr/bin/env python3
"""
Generate QUALITY.md files for all skills.
Each QUALITY.md defines "What Good Looks Like" for that skill's outputs.
"""

import os
import re
from pathlib import Path

SKILLS_DIR = Path("skills")

QUALITY_TEMPLATE = """# Quality Rubric: {skill_name}

**Skill:** {skill_name}  
**Version:** 1.0  
**Last Updated:** {date}

---

## What Good Looks Like

{introduction}

---

## Quality Dimensions

### 1. Completeness

**Checklist:**
- [ ] All required sections present
- [ ] No placeholder text or TODOs
- [ ] All inputs acknowledged (even if not available)

**Signs of Quality:**
- Output is self-contained and fully developed
- Reader doesn't need to ask follow-up questions for basic understanding

---

### 2. Accuracy

**Checklist:**
- [ ] Facts are verifiable
- [ ] Methodology applied correctly
- [ ] No hallucinations or unsupported claims

**Signs of Quality:**
- Confidence levels are appropriately calibrated
- Uncertainty is acknowledged where present
- Evidence is cited for key claims

---

### 3. Actionability

**Checklist:**
- [ ] Recommendations are specific and implementable
- [ ] Next steps are clear
- [ ] Decision criteria are defined

**Signs of Quality:**
- A practitioner could act on the output without additional interpretation
- Prioritization is provided where multiple options exist

---

### 4. Structure & Format

**Checklist:**
- [ ] Follows output schema (if defined)
- [ ] Appropriate use of headers, tables, lists
- [ ] Length is proportional to complexity

**Signs of Quality:**
- Information is well-organized and easy to navigate
- Key findings are immediately visible
- Supporting detail is accessible but doesn't overwhelm

---

### 5. Domain Specificity

**Checklist:**
- [ ] Uses appropriate terminology
- [ ] Context is relevant to the domain
- [ ] SaaS/digital product context where applicable

**Signs of Quality:**
- Output demonstrates deep understanding of the domain
- Generic advice has been customized to the context

---

## Common Failure Modes

{common_failures}

---

## Quality Benchmarks

| Level | Description | Characteristics |
|-------|-------------|-----------------|
| **Exceptional** | Exceeds all criteria | Comprehensive, insightful, actionable, well-structured |
| **Good** | Meets all criteria | Complete, accurate, actionable, properly formatted |
| **Acceptable** | Most criteria met | Minor gaps in completeness or structure, but usable |
| **Poor** | Significant gaps | Missing key elements, inaccurate, or not actionable |
| **Reject** | Does not meet criteria | Fundamental problems that require rework |

---

## Review Checklist

Before marking a {skill_name} output as complete, verify:

- [ ] Completeness checklist passed
- [ ] Accuracy checklist passed  
- [ ] Actionability checklist passed
- [ ] Structure & Format checklist passed
- [ ] Domain Specificity checklist passed
- [ ] No common failure modes present
- [ ] Output meets "Good" or higher on quality benchmark

---

## Test Scenarios

{test_scenarios}

---

*This quality rubric should be used to evaluate outputs from the {skill_name} skill. 
For questions or suggested improvements, contact the skill maintainer.*
"""

COMMON_FAILURE_TEMPLATES = {
    "research": """
1. **Surface-level analysis** — Output lacks depth, doesn't apply methodology
2. **Missing context** — Recommendations don't account for constraints or context provided
3. **Unsupported claims** — Findings presented without evidence or attribution
4. **Generic output** — Could apply to any product, not domain-specific
5. **Incomplete coverage** — Key dimensions or stakeholders not addressed
""",
    "design": """
1. **Generic design decisions** — Not tailored to specific product context or users
2. **Missing rationale** — Design choices presented without explaining why
3. **Inconsistent patterns** — Doesn't follow established design system or conventions
4. **Accessibility ignored** — Doesn't account for a11y requirements
5. **Incomplete specifications** — Missing edge cases or state definitions
""",
    "technical": """
1. **Architecture not fit for purpose** — Doesn't account for scale, performance, or maintainability
2. **Security oversights** — Common vulnerabilities not addressed
3. **Missing error handling** — Edge cases and failure modes not considered
4. **Incomplete documentation** — Code or config without clear explanation
5. **Performance issues** — N+1 queries, inefficient algorithms, missing indexes
""",
    "strategy": """
1. **Vague recommendations** — "Improve UX" instead of specific, actionable changes
2. **Missing prioritization** — All recommendations treated as equal priority
3. **No success metrics** — Recommendations don't include how to measure success
4. **Ignores constraints** — Recommendations don't account for resources or timeline
5. **Generic strategy** — Could apply to any product, not tailored to specific market
""",
    "process": """
1. **One-size-fits-all** — Doesn't adapt to team size, maturity, or context
2. **Missing ownership** — No clear accountabilities defined
3. **No feedback loop** — Process doesn't include improvement mechanisms
4. **Over-engineered** — Unnecessarily complex for the situation
5. **Under-engineered** — Too simplistic to address the actual problem
""",
    "default": """
1. **Incomplete output** — Missing key sections or information
2. **Poor structure** — Difficult to navigate or understand
3. **Generic content** — Not tailored to the specific context
4. **Missing quality** — Accuracy, completeness, or actionability issues
5. **No evidence** — Claims not supported by data or reasoning
"""
}

TEST_SCENARIO_TEMPLATES = {
    "research": """
| Scenario | Input | Expected Quality Level |
|----------|-------|----------------------|
| Happy path | Full context with multiple competitors | Exceptional |
| Thin data | Only 1-2 competitors available | Good |
| Vague request | "Analyze competitors" with no specifics | Good |
| Fast mode | 2 sentence input | Acceptable |
| No competitors | New market, no direct competitors | Good (gap is finding) |
""",
    "design": """
| Scenario | Input | Expected Quality Level |
|----------|-------|----------------------|
| Standard feature | Clear requirements, established product | Exceptional |
| Redesign | Existing product with legacy constraints | Good |
| New product | Minimal context, greenfield | Good |
| Mobile-first | Explicit mobile requirement | Good |
| Accessibility-critical | Healthcare/product with a11y needs | Exceptional |
""",
    "technical": """
| Scenario | Input | Expected Quality Level |
|----------|-------|----------------------|
| Greenfield | New service, no legacy constraints | Exceptional |
| Migration | Existing system with data to preserve | Good |
| Performance-critical | Low-latency requirements | Exceptional |
| Cost-optimization | Budget constraints explicit | Good |
| Security-sensitive | PII or financial data | Exceptional |
""",
    "strategy": """
| Scenario | Input | Expected Quality Level |
|----------|-------|----------------------|
| Full context | Clear product, market, constraints | Exceptional |
| Early stage | New product, undefined market | Good |
| Turnaround | Struggling product | Good |
|高速 growth | Scaling constraints explicit | Good |
| Competitive threat | Disruptive competitor entered | Good |
""",
    "process": """
| Scenario | Input | Expected Quality Level |
|----------|-------|----------------------|
| Startup | Small team, fast pace | Good |
| Enterprise | Large org, compliance needs | Good |
| Remote-first | Distributed team | Good |
| Recovery | Team struggling with current process | Exceptional |
| Scaling | Team growing rapidly | Good |
""",
    "default": """
| Scenario | Input | Expected Quality Level |
|----------|-------|----------------------|
| Standard | Normal inputs, clear context | Good |
| Minimal | Limited information provided | Acceptable |
| Edge case | Unusual constraints or requirements | Good |
| Complex | Multiple competing priorities | Good |
| Quick | Fast turnaround requested | Acceptable |
"""
}

def get_skill_category(skill_name: str) -> str:
    """Determine skill category for appropriate failure modes."""
    name_lower = skill_name.lower()
    
    if any(x in name_lower for x in ['research', 'analysis', 'competitive', 'market', 'user', 'journey', 'persona']):
        return "research"
    elif any(x in name_lower for x in ['design', 'ui', 'ux', 'brand', 'canvas', 'wireframe', 'visual']):
        return "design"
    elif any(x in name_lower for x in ['architect', 'technical', 'api', 'database', 'schema', 'security', 'devops', 'infrastructure', 'cloud', 'backend']):
        return "technical"
    elif any(x in name_lower for x in ['strategy', 'business', 'roadmap', 'planning', 'go-to-market', 'gtm', 'launch', 'messaging', 'pricing']):
        return "strategy"
    elif any(x in name_lower for x in ['process', 'scrum', 'agile', 'sprint', 'retrospective', 'ceremony', 'velocity', 'backlog']):
        return "process"
    else:
        return "default"

def get_skill_description(skill_path: Path) -> str:
    """Extract skill description from SKILL.md."""
    skill_name = skill_path.name.replace('SKILL-', '')
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        skill_file = SKILLS_DIR / f"SKILL-{skill_name}.md"
    
    if not skill_file.exists():
        return f"The {skill_path.name} skill produces outputs for {skill_path.name.replace('-', ' ')}."
    
    content = skill_file.read_text(encoding='utf-8')
    
    # Try to extract description from frontmatter
    match = re.search(r'description:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if match:
        return match.group(1).strip().rstrip('.') + "."
    
    # Try first line after frontmatter
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('---') and not line.startswith('#'):
            return line[:200].rstrip('.') + "."
    
    return f"The {skill_path.name} skill produces outputs for {skill_path.name.replace('-', ' ')}."

def generate_quality_md(skill_path: Path) -> str:
    """Generate QUALITY.md content for a skill."""
    skill_name = skill_path.name.replace('SKILL-', '')
    category = get_skill_category(skill_name)
    description = get_skill_description(skill_path)
    failures = COMMON_FAILURE_TEMPLATES.get(category, COMMON_FAILURE_TEMPLATES["default"])
    test_scenarios = TEST_SCENARIO_TEMPLATES.get(category, TEST_SCENARIO_TEMPLATES["default"])
    
    return QUALITY_TEMPLATE.format(
        skill_name=skill_name,
        introduction=f"This rubric defines quality standards for outputs from the **{skill_name}** skill. {description}",
        common_failures=failures,
        test_scenarios=test_scenarios,
        date="2026-03-27"
    )

def main():
    """Generate QUALITY.md for all skills."""
    generated = 0
    skipped = 0
    
    # Process directory-based skills
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('_'):
            continue
        
        quality_file = skill_dir / "QUALITY.md"
        if quality_file.exists():
            skipped += 1
            continue
        
        content = generate_quality_md(skill_dir)
        quality_file.write_text(content, encoding='utf-8')
        print(f"Created: {quality_file}")
        generated += 1
    
    # Process single-file skills (SKILL-*.md)
    for skill_file in sorted(SKILLS_DIR.glob("SKILL-*.md")):
        if skill_file.stem == "quality-checklist":
            continue
        
        skill_name = skill_file.stem.replace('SKILL-', '')
        quality_file = SKILLS_DIR / f"QUALITY-{skill_name}.md"
        
        if quality_file.exists():
            skipped += 1
            continue
        
        skill_path = skill_file.parent / skill_name
        content = generate_quality_md(skill_path)
        quality_file.write_text(content, encoding='utf-8')
        print(f"Created: {quality_file}")
        generated += 1
    
    print(f"\nGenerated: {generated} QUALITY.md files")
    print(f"Skipped (already exist): {skipped}")

if __name__ == "__main__":
    main()
