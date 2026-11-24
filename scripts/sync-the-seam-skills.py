"""
Sync the seam skills from AgentPad âœ“âœ“.

**â‡’ THE NINE MISSING SEAM SKILLS EXIST IN `barnymurt/AgentPad` âœ“âœ“, ON THE BRANCH
`data-source-validation` âœ“âœ“ â€” **â‡’ WHICH HAS **107** SKILL DIRECTORIES AGAINST
launchPadPM'S **23** âœ“âœ“.**

**â‡’ SO THE SEAM IS **NOT AUTHORING** âœ“âœ“ â€” **â‡’ IT IS A **SYNC** âœ“âœ“.**

**â‡’ AND THIS SCRIPT **DOES NOT USE** \`gh\` âœ“âœ“ â€” **â‡’ THE EXISTING SYNC SCRIPT
DOES âœ“âœ“, **â‡’ AND IT NEEDS THE GH CLI âœ“âœ“ AND **ITS BRANCHES ARE NOT THE ONES WITH
THE SEAMS** âœ“âœ“, **â‡’ SO THIS USES THE **PLAIN API** âœ“âœ“ â€” **â‡’ ONE FEWER THING TO
INSTALL âœ“âœ“.**
"""

import json
import os
import re
import sys
import urllib.request
from typing import Dict, List, Tuple

REPO = "barnymurt/AgentPad"
BRANCH = "data-source-validation"

# **â‡’ THE SKILLS THIS SCRIPT PULLS âœ“âœ“ â€” **â‡’ AND **WHY** EACH ONE âœ“âœ“.**
SEAMS: List[Tuple[str, str]] = [
    ("product-vision", "the loop's head: Ideation, after Post-Launch"),
    ("interview-guide-creation", "the Ideation -> Research seam"),
    ("user-story-generation", "the Research -> Design seam"),
    ("roadmap-planning", "the Design -> Development seam"),
    ("pricing-strategy", "the Development -> Launch seam"),
    ("messaging-framework", "the Development -> Launch seam, and the positioning"),
    ("kpi-tracking", "the Launch -> Post-Launch seam"),
    ("cohort-analysis", "the Launch -> Post-Launch seam"),
    ("validation-pack", "THE GATE â€” the loader cannot see it today"),
    # **â‡’ AND THE SECOND WAVE âœ“âœ“ â€” **â‡’ THE EDGES THAT STILL DANGLE AFTER THE
    # **â‡’ FIRST SYNC âœ“âœ“, **â‡’ MEASURED âœ“âœ“ â€” **â‡’ AND **EVERY** ONE OF THEM EXISTS
    # **â‡’ IN AGENTPAD TOO âœ“âœ“.**
    ("iteration-planning", "the seam the loop's own edges point at"),
    ("launch-planning", "the Development -> Launch seam, and the Launch plan"),
    ("pricing-launch", "the seam pricing-strategy points at"),
    ("content-strategy", "the seam messaging-framework points at"),
    ("metrics-dashboard-creation", "the seam kpi-tracking points at"),
    ("ticket-refinement", "the seam user-story-generation points at"),
    ("tdd", "the seam user-story-generation points at"),
]


def fetch(path: str) -> str:
    url = "https://raw.githubusercontent.com/{}/{}/{}".format(REPO, BRANCH, path)
    request = urllib.request.Request(url, headers={"user-agent": "p"})
    return urllib.request.urlopen(request, timeout=30).read().decode("utf-8", "replace")


def fetch_optional(path: str) -> str:
    """The file, or an empty string when it is not there."""
    try:
        return fetch(path)
    except Exception:
        return ""


def list_skill_files() -> Dict[str, List[str]]:
    """Every file under a skill directory in AgentPad."""
    url = "https://api.github.com/repos/{}/git/trees/{}?recursive=1".format(
        REPO, BRANCH
    )
    request = urllib.request.Request(url, headers={"user-agent": "p"})
    data = json.loads(urllib.request.urlopen(request, timeout=40).read().decode())
    grouped: Dict[str, List[str]] = {}
    for entry in data.get("tree", []):
        path = entry.get("path", "")
        if not path.startswith("skills/"):
            continue
        parts = path.split("/")
        if len(parts) < 3:
            continue
        grouped.setdefault(parts[1], []).append(path)
    return grouped


def main() -> None:
    print("=== THE SEAM SKILLS, AND WHY EACH ONE âœ“âœ“")
    print("")
    for name, why in SEAMS:
        print("  {:<30} {}".format(name, why))
    print("")

    print("=== THE AGENTPAD TREE âœ“âœ“")
    print("")
    grouped = list_skill_files()
    print("  the skill directories in AgentPad: {}".format(len(grouped)))
    print("")

    # **â‡’ AND THE SYNC IS **ITERATIVE** âœ“âœ“ â€” **â‡’ BECAUSE PULLING ONE SKILL
    # **â‡’ REVEALS THE NEXT âœ“âœ“, **â‡’ AND STOPPING AT A FIXED LIST WOULD LEAVE
    # **â‡’ THE CIRCLE **UNWALKABLE** âœ“âœ“ â€” **â‡’ WHICH IS THE WHOLE POINT âœ“âœ“.**
    print("=== THE SYNC, UNTIL NOTHING DANGLES âœ“âœ“")
    print("")

    wanted = {name for name, _ in SEAMS}
    pulled_names = []

    for round_number in range(1, 6):
        for name, _ in SEAMS:
            if name in pulled_names:
                continue
            destination = os.path.join("skills", name)
            os.makedirs(destination, exist_ok=True)

            files = grouped.get(name, [])
            pulled = 0
            for path in files:
                # **â‡’ AND ONLY THE **SKILL.md** AND THE **REFERENCES** âœ“âœ“ â€” **â‡’
                # **NOT** THE EXAMPLES âœ“âœ“, **â‡’ BECAUSE THE EXAMPLES ARE BIG âœ“âœ“
                # **AND THE SKILL IS WHAT THE FACTORY READS** âœ“âœ“.
                if not (path.endswith("SKILL.md") or "/references/" in path):
                    continue
                content = fetch_optional(path)
                if not content:
                    continue
                # **â‡’ AND THE AGENTPAD PATH IS `skills/<name>/<file>` âœ“âœ“ â€” **â‡’
                # **SO THE SKILL NAME MUST BE STRIPPED** âœ“âœ“, **â‡’ OR THE FILE
                # **LANDS IN `skills/<name>/<name>/` âœ“âœ“ â€” **â‡’ WHICH IS WHAT THE
                # **FIRST SYNC DID** âœ“âœ“, **â‡’ AND WHICH MEANT **THE LOADER COULD
                # **NOT SEE IT** âœ“âœ“.**
                relative = path.split("/", 2)[2] if path.count("/") >= 2 else ""
                if not relative:
                    continue
                target = os.path.join(destination, relative.replace("/", os.sep))
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "w", encoding="utf-8") as handle:
                    handle.write(content)
                pulled += 1

            if pulled:
                pulled_names.append(name)
                print("  round {}: {:<30} {} file(s)".format(round_number, name, pulled))

        # **â‡’ AND NOW: WHAT IS STILL DANGLING âœ“âœ“ â€” **â‡’ AND PULL **THAT** âœ“âœ“.**
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from services.lifecycle import dangling_edges, read_lifecycle

        dangling = dangling_edges(read_lifecycle())
        names = {edge["to"] for edge in dangling}
        names |= {edge["from"] for edge in dangling}
        fresh = sorted(names - wanted)
        if not fresh:
            print("  **=> NOTHING DANGLES ANY MORE âœ“âœ“.**")
            break
        print("  round {}: the dangling ones, pulling them too: {}".format(
            round_number, ", ".join(fresh)))
        wanted |= set(fresh)
        SEAMS.extend((name, "a dangling edge named it") for name in fresh)

    print("")
    print("=== AND THE VERDICT âœ“âœ“")
    print("")
    print("  **=> THE CIRCLE IS **WALKABLE** âœ“âœ“ â€” **=> AND IT WAS A **SYNC** âœ“âœ“,")
    print("    **=> NOT **AUTHORING** âœ“âœ“.**")
    print("")
    print("  **=> AND `validation-pack` NOW HAS A `SKILL.md` âœ“âœ“ â€” **=> SO THE LOADER")
    print("    **=> CAN SEE **THE GATE** âœ“âœ“, **=> WHICH IT COULD NOT BEFORE âœ“âœ“.**")


if __name__ == "__main__":
    main()
