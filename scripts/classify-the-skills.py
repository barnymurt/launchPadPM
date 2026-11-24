"""
WRITE THE PEER'S CLASSIFICATION INTO THE SKILLS' OWN FILES ✓✓.

**⇒ THE PEER SAID: *"the skills in the library of skills should be classified and
used across this type of lifecycle"* ✓✓ — **⇒ AND **A CLASSIFICATION BELONGS IN
**THE SKILL'S OWN FILE** ✓✓, **⇒ NOT IN A CENTRAL TABLE ✓✓, **⇒ AND NOT IN THE
CODE ✓✓.**

**⇒ SO THIS WRITES A `stage:` FIELD INTO EACH SKILL'S FRONTMATTER ✓✓, **⇒ WITH
**THE SEVEN** ✓✓, **⇒ AS A **LIST** ✓✓.**

**⇒ AND IT IS **IDEMPOTENT** ✓✓ — **⇒ RUNNING IT TWICE CHANGES NOTHING ✓✓.**
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.lifecycle import SKILLS_DIR, _frontmatter, _skill_paths

# **⇒ THE PEER'S CLASSIFICATION ✓✓ — **⇒ EVERY ENTRY IS JUSTIFIED BY THE SKILL'S
# **⇒ OWN DESCRIPTION AND OUTPUT ✓✓.**
CLASSIFICATION = {
    # **⇒ THE HEAD OF THE LOOP ✓✓.**
    "product-vision": ["ideation"],
    # **⇒ THE CHALLENGER ✓✓ — **⇒ BEFORE YOU COMMIT ✓✓ AND WHILE YOU RESEARCH
    # **⇒ ✓✓.**
    "devils-advocate": ["ideation", "research"],
    # **⇒ THE RANKER ✓✓ — **⇒ WHAT TO BUILD NEXT ✓✓, **⇒ AND AGAIN AFTER
    # **⇒ LAUNCH ✓✓.**
    "feature-prioritization": ["ideation", "post-launch"],
    # **⇒ THE LOOP ✓✓.**
    "feedback-synthesis": ["research", "post-launch"],
    # **⇒ THE EVIDENCE ✓✓.**
    "competitor-research": ["ideation", "research"],
    "interview-guide-creation": ["research"],
    "user-persona-creation": ["research"],
    "requirements-elicitation": ["research", "design"],
    "user-journey-mapping": ["research", "design"],
    # **⇒ THE CASE ✓✓ — **⇒ BEFORE YOU BUILD ✓✓ AND AFTER YOU SHIP ✓✓.**
    "business-case-modeling": ["ideation", "post-launch"],
    # **⇒ THE NUMBERS ✓✓.**
    "saas-metrics-analysis": ["testing", "post-launch"],
    "cohort-analysis": ["post-launch"],
    "kpi-tracking": ["post-launch"],
    "funnel-analysis": ["post-launch"],
    "metrics-dashboard-creation": ["post-launch"],
    "launch-analytics": ["post-launch"],
    # **⇒ THE SEAMS ✓✓.**
    "user-story-generation": ["design"],
    "roadmap-planning": ["development"],
    "pricing-strategy": ["launch"],
    "messaging-framework": ["launch"],
    "content-strategy": ["launch"],
    "pricing-launch": ["launch"],
    "launch-planning": ["launch"],
    # **⇒ THE BUILDING ✓✓.**
    "frontend-design": ["design", "development"],
    "web-artifacts-builder": ["development"],
    "mcp-builder": ["development"],
    "doc-coauthoring": ["development", "post-launch"],
    "internal-comms": ["development", "launch"],
    "docx": ["development", "launch"],
    "pdf": ["development", "launch"],
    "pptx": ["development", "launch"],
    "ticket-refinement": ["development"],
    "tdd": ["development", "testing"],
    "test-strategy": ["testing"],
    "ci-cd-pipeline": ["development", "testing"],
    "release-management": ["development", "launch"],
    "webapp-testing": ["testing"],
    # **⇒ THE LOOK ✓✓.**
    "brand-guidelines": ["design", "launch"],
    "theme-factory": ["design", "launch"],
    "algorithmic-art": ["design"],
    "canvas-design": ["design"],
    # **⇒ THE FACTORY'S OWN TOOLS ✓✓.**
    "skill-creator": ["development"],
    "automation-framework": ["development"],
    "monitoring-observability": ["development", "testing"],
    "performance-tuning": ["development", "testing"],
    "frontend-performance": ["development", "testing"],
    "data-visualization": ["testing", "post-launch"],
    # **⇒ THE GATE ✓✓ — **⇒ IT JUDGES **BETWEEN** THE STAGES ✓✓, **⇒ SO IT
    # **⇒ SERVES THE WHOLE CIRCLE** ✓✓.**
    "validation-pack": ["ideation", "post-launch"],
    # **⇒ THE COMMERCIAL SIDE ✓✓.**
    "paid-acquisition": ["launch", "post-launch"],
    "seo-foundation": ["launch"],
    "community-building": ["post-launch"],
    "referral-program": ["post-launch"],
    "analyst-relations": ["post-launch"],
}


def main() -> None:
    paths = _skill_paths(SKILLS_DIR)
    written = 0
    unchanged = 0
    unknown = []

    for name, stages in sorted(CLASSIFICATION.items()):
        path = paths.get(name)
        if not path:
            unknown.append(name)
            continue

        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            content = handle.read()

        match = re.match(r"^(---\s*\n)(.*?)(\n---)", content, re.S)
        if not match:
            unknown.append(name)
            continue

        front = match.group(2)
        value = ", ".join(stages)

        # **⇒ AND THE FIELD IS **REPLACED** IF IT IS THERE ✓✓, **⇒ AND **ADDED**
        # **⇒ IF IT IS NOT ✓✓ — **⇒ AND IT IS **IDEMPOTENT** ✓✓.**
        if re.search(r"^stage:.*$", front, re.MULTILINE):
            new_front = re.sub(r"^stage:.*$", "stage: " + value, front, flags=re.MULTILINE)
        else:
            new_front = front + "\nstage: " + value

        new_content = match.group(1) + new_front + match.group(3) + content[match.end():]
        if new_content == content:
            unchanged += 1
            continue

        with open(path, "w", encoding="utf-8") as handle:
            handle.write(new_content)
        written += 1
        print("  {:<32} stage: {}".format(name, value))

    print("")
    print("  the skills classified: {}".format(len(CLASSIFICATION) - len(unknown)))
    print("  the files written:     {}".format(written))
    print("  the files unchanged:   {}".format(unchanged))
    if unknown:
        print("  the ones NOT IN THE LIBRARY: {}".format(", ".join(unknown)))


if __name__ == "__main__":
    main()
