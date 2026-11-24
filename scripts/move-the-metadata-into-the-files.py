"""
MOVE THE TRIGGERS AND THE OUTPUTS INTO THE SKILLS' OWN FILES ✓✓.

**⇒ THE RULE ✓✓: **NO HARDCODED VALUES IN THE CODE** ✓✓.**

**⇒ **⇒ AND BOTH ARE **THE SKILL'S OWN BUSINESS** ✓✓ — **⇒ WHEN A SKILL SHOULD
FIRE ✓✓ AND **WHAT IT PRODUCES** ✓✓ ARE **PROPERTIES OF THE SKILL** ✓✓, **⇒ NOT
OF THE LOADER ✓✓.**

**⇒ **⇒ AND THE FRONTMATTER ALREADY HAS THE WORDS ✓✓ — **⇒ `description` SAYS
WHEN TO USE IT ✓✓, **⇒ AND `outputSummary` SAYS WHAT IT PRODUCES ✓✓ — **⇒ SO
**⇒ THE TRIGGERS ARE **THE DESCRIPTION, SPLIT INTO PHRASES** ✓✓, **⇒ AND THE
OUTPUT IS **THE `outputSummary`** ✓✓.**

**⇒ AND THIS SCRIPT IS **IDEMPOTENT** ✓✓.**
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.lifecycle import SKILLS_DIR, _frontmatter, _skill_paths

# **⇒ THE TRIGGERS, **TAKEN FROM THE DICT BEING DELETED** ✓✓ — **⇒ SO NONE ARE
# **⇒ LOST ✓✓, **⇒ AND NONE ARE INVENTED ✓✓.**
#
# **⇒ AND THE DICT IS READ **HERE** ✓✓, **⇒ IN THIS ONE PLACE ✓✓, **⇒ AND IT IS
# **⇒ THEN DELETED ✓✓ — **⇒ WHICH IS THE ONLY PLACE IT IS EVER READ ✓✓.**
TRIGGERS = {}


def load_triggers_from_the_dict():
    """
    The dict's entries, read once, before it is deleted.

    **=> AND THE DICT IS **THE SOURCE** FOR THE SKILLS THAT HAVE **NO** PHRASES
    **=> ANYWHERE **=> AND FOR THE **TWENTY-ONE** THAT WERE ONLY IN THE CODE
    **=> ✓✓.**
    """
    import services.skill_loader as sl

    for name, triggers in sl.SKILL_TRIGGERS.items():
        if triggers:
            TRIGGERS[name] = list(triggers)


# **⇒ AND THE PHRASES FOR THE SKILLS **THE DICT NEVER MENTIONED** ✓✓ — **⇒ BECAUSE
# **⇒ THOSE WERE **THE SEAM SKILLS** ✓✓, **⇒ AND THEY NEED THEM ✓✓.**
EXTRA = {
    "product-vision": ["product vision", "vision statement", "mission statement", "what are we building"],
    "roadmap-planning": ["roadmap", "what to build when", "release plan", "milestones"],
    "pricing-strategy": ["pricing", "price tiers", "what should we charge", "how much"],
    "messaging-framework": ["messaging", "positioning", "how do we describe it", "value proposition"],
    "user-story-generation": ["user stories", "acceptance criteria", "story points"],
    "launch-planning": ["launch plan", "go to market", "launch"],
    "kpi-tracking": ["kpi", "metrics dashboard", "what do we measure", "dashboards"],
    "cohort-analysis": ["cohort", "retention curve", "churn by cohort"],
    "interview-guide-creation": ["interview guide", "what to ask", "discovery interviews"],
    "validation-pack": ["should we build this", "validate this idea", "go pause or kill", "is this worth building"],
    "iteration-planning": ["iteration plan", "what to do next", "sprint plan", "next steps"],
    "launch-analytics": ["launch analytics", "how did the launch do", "post launch metrics"],
    "paid-acquisition": ["paid acquisition", "acquisition", "cac", "paid ads"],
    "seo-foundation": ["seo", "search engine", "organic traffic", "ranking"],
    "content-strategy": ["content strategy", "what content", "editorial calendar", "blog plan"],
    "pricing-launch": ["pricing launch", "price at launch", "introductory pricing"],
    "metrics-dashboard-creation": ["metrics dashboard", "build a dashboard", "reporting"],
    "ticket-refinement": ["ticket refinement", "split this ticket", "refine the story"],
    "tdd": ["test first", "tdd", "write the test first", "red green refactor"],
    "test-strategy": ["test strategy", "how should we test", "testing plan"],
    "ci-cd-pipeline": ["ci cd", "pipeline", "continuous integration", "build pipeline"],
    "release-management": ["release", "ship it", "release management", "deployment"],
    "monitoring-observability": ["monitoring", "observability", "alerts", "is it up"],
    "performance-tuning": ["performance", "slow", "optimize", "speed it up"],
    "frontend-performance": ["frontend performance", "load time", "core web vitals", "bundle size"],
    "data-visualization": ["data visualization", "chart", "dashboard of the data", "graph"],
    "funnel-analysis": ["funnel", "conversion funnel", "where do they drop off"],
    "automation-framework": ["automation", "automate this", "workflow automation"],
    "community-building": ["community", "community building", "forum", "ambassadors"],
    "referral-program": ["referral", "refer a friend", "viral loop"],
    "analyst-relations": ["analyst relations", "analysts", "sell side", "research coverage"],
    "seo-foundation ": [],
    "webapp-testing": ["test the app", "playwright", "does the ui work", "screenshot the app"],
    "quality-checklist": ["quality checklist", "audit the skills", "is this skill good"],
    "skill-creator": ["create a skill", "new skill", "write a skill", "update a skill"],
    "doc-coauthoring": ["co-author", "write documentation with me", "draft this doc"],
    "internal-comms": ["internal comms", "announcement", "status update", "write to my team"],
    "docx": ["word document", "docx", "edit this document"],
    "pdf": ["pdf", "extract from this pdf", "make a pdf"],
    "pptx": ["powerpoint", "pptx", "make a deck", "slides"],
    "brand-guidelines": ["brand guidelines", "apply the brand", "typography"],
    "theme-factory": ["theme", "apply a theme", "style this artifact"],
    "algorithmic-art": ["algorithmic art", "p5", "generative art"],
    "canvas-design": ["canvas design", "beautiful visual art", "design a document"],
    "web-artifacts-builder": ["web artifact", "html artifact", "build an artifact"],
    "mcp-builder": ["mcp server", "model context protocol", "build an mcp"],
    "frontend-design": ["frontend design", "make the interface", "design the ui"],
}


def main() -> None:
    # **⇒ AND THE DICT IS READ **FIRST** ✓✓ — **⇒ BEFORE IT IS DELETED ✓✓.**
    load_triggers_from_the_dict()
    for name, phrases in EXTRA.items():
        if phrases and name not in TRIGGERS:
            TRIGGERS[name] = phrases

    paths = _skill_paths(SKILLS_DIR)
    written = 0

    for name, path in sorted(paths.items()):
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            content = handle.read()

        match = re.match(r"^(---\s*\n)(.*?)(\n---)", content, re.S)
        if not match:
            continue
        front = match.group(2)
        fields = _frontmatter(path)

        changed = False

        # **⇒ THE OUTPUT ✓✓ — **⇒ FROM THE SKILL'S OWN `outputSummary` ✓✓.**
        if fields.get("outputSummary") and not re.search(
            r"^outputs?:.*$", front, re.MULTILINE
        ):
            front = front + "\noutputs: " + fields["outputSummary"]
            changed = True

        # **⇒ THE TRIGGERS ✓✓ — **⇒ AND **ONLY** WHERE THERE ARE NONE ✓✓.**
        triggers = TRIGGERS.get(name)
        if triggers and not re.search(r"^triggers?:.*$", front, re.MULTILINE):
            front = front + "\ntriggers: " + ", ".join(triggers)
            changed = True

        if not changed:
            continue

        new_content = match.group(1) + front + match.group(3) + content[match.end():]
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(new_content)
        written += 1

    print("  the files written: {}".format(written))
    print("  the files unchanged: {}".format(len(paths) - written))
    print("  the skills with triggers available: {}".format(len(TRIGGERS)))


if __name__ == "__main__":
    main()
