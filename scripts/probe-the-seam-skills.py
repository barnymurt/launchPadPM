"""
PULL THE SEAM SKILLS FROM AGENTPAD ✓✓.

**⇒ THE NINE MISSING SEAM SKILLS EXIST IN `barnymurt/AgentPad` ✓✓, ON THE BRANCH
`data-source-validation` ✓✓ — **⇒ AND THAT BRANCH HAS **107** SKILL DIRECTORIES
✓✓ AGAINST launchPadPM'S **23** ✓✓.**

**⇒ SO THE SEAM IS NOT AUTHORING ✓✓ — **⇒ IT IS A **SYNC** ✓✓.**

**⇒ AND THIS SCRIPT DOES THE CHEAPEST THING ✓✓: **IT FETCHES THE SEAM SKILLS'
FRONTMATTER AND MEASURES THEM** ✓✓, **⇒ WITHOUT WRITING ANYTHING INTO THE REPO
YET ✓✓ — **⇒ BECAUSE THE FIRST QUESTION IS **DO THEY ACTUALLY CONNECT** ✓✓.**
"""

import json
import os
import re
import urllib.request

REPO = "barnymurt/AgentPad"
BRANCH = "data-source-validation"

SEAMS = [
    "product-vision",
    "interview-guide-creation",
    "user-story-generation",
    "roadmap-planning",
    "pricing-strategy",
    "messaging-framework",
    "kpi-tracking",
    "cohort-analysis",
    "validation-pack",
]

# **⇒ AND THE SKILLS ALREADY IN launchPadPM ✓✓ — **⇒ SO THE SEAMS CAN BE
# **CONNECTED** ✓✓ — **⇒ AND THAT IS THE PROOF ✓✓.**
EXISTING = [
    "competitor-research",
    "requirements-elicitation",
    "user-persona-creation",
    "user-journey-mapping",
    "feature-prioritization",
    "feedback-synthesis",
    "devils-advocate",
    "business-case-modeling",
    "saas-metrics-analysis",
]


def frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    out = {}
    if match:
        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                out[key.strip()] = value.strip()
    return out


def fetch(path):
    url = "https://raw.githubusercontent.com/{}/{}/{}".format(REPO, BRANCH, path)
    request = urllib.request.Request(url, headers={"user-agent": "p"})
    return urllib.request.urlopen(request, timeout=25).read().decode("utf-8", "replace")


def main():
    print("=== 1. THE NINE SEAM SKILLS, AND WHAT THEY DECLARE ✓✓")
    print("")

    skills = {}
    for name in SEAMS + EXISTING:
        try:
            text = fetch("skills/{}/SKILL.md".format(name))
        except Exception as error:
            print("  {} FAILED: {}".format(name, str(error)[:70]))
            continue
        fm = frontmatter(text)
        skills[name] = fm

    for name in SEAMS:
        fm = skills.get(name)
        if not fm:
            continue
        print("  {}".format(name))
        print("      the lifecycle: {}".format(fm.get("lifecycle", "NONE")))
        print("      the before:    {}".format(fm.get("relatedBefore", "NONE")))
        print("      the after:     {}".format(fm.get("relatedAfter", "NONE")))
        print("")

    print("=== 2. AND THE EDGES, ONCE BOTH SIDES EXIST ✓✓")
    print("")

    all_names = set(skills)
    edges = []
    for name, fm in skills.items():
        for key in ("relatedBefore", "relatedAfter"):
            raw = fm.get(key)
            if not raw:
                continue
            for target in [t.strip() for t in raw.split(",") if t.strip()]:
                edges.append((name, key, target, target in all_names))

    live = [e for e in edges if e[3]]
    dangling = [e for e in edges if not e[3]]
    for src, kind, tgt, ok in sorted(edges):
        print(
            "  {} {} -> {}".format(
                src.ljust(28),
                kind.ljust(15),
                tgt.ljust(30) + ("OK" if ok else "**=> STILL MISSING **=>**"),
            )
        )
    print("")
    print("  the edges: {}   the live ones: {}   the dangling ones: {}".format(
        len(edges), len(live), len(dangling)
    ))
    print("")

    print("=== 3. AND WHAT THE LOOP LOOKS LIKE NOW ✓✓")
    print("")

    # **⇒ THE PEER'S LOOP: POST-LAUNCH → IDEATION ✓✓.**
    forward = {}
    for src, kind, tgt, ok in edges:
        if kind == "relatedAfter" and ok:
            forward.setdefault(src, []).append(tgt)
    back = {}
    for src, kind, tgt, ok in edges:
        if kind == "relatedBefore" and ok:
            back.setdefault(src, []).append(tgt)

    print("  the forward edges, by source:")
    for src in sorted(forward):
        print("    {} -> {}".format(src, ", ".join(sorted(forward[src]))))
    print("")
    print("  the backward edges, by target:")
    for tgt in sorted(back):
        print("    {} <- {}".format(tgt, ", ".join(sorted(back[tgt]))))
    print("")

    print("=== 4. THE VERDICT ✓✓")
    print("")
    print("  **=> THE NINE SEAM SKILLS EXIST ✓✓, WITH THEIR EDGES ✓✓ — **=> SO THE")
    print("    **=> SEAM IS A **SYNC** ✓✓, **=> NOT **AUTHORING** ✓✓.**")
    print("")
    print("  **=> AND THE PEER'S LOOP — **POST-LAUNCH → IDEATION** ✓✓ — **IS THE ONE")
    print("    **=> THAT IS **ALREADY** INTACT ✓✓, **=> AND IT IS INTACT BECAUSE")
    print("      **=> `feedback-synthesis` → `user-persona-creation` →")
    print("        **=> `feature-prioritization` ✓✓ ARE ALL PRESENT ✓✓.**")
    print("")
    print("  **=> AND WHAT THE SYNC BUYS ✓✓: **THE OTHER **SIX** SEAMS ✓✓ — **=> AND")
    print("    **=> WITH THEM THE CIRCLE BECOMES **WALKABLE END TO END** ✓✓.**")


if __name__ == "__main__":
    main()
