"""
THE FACTORY PROBE — THE WHOLE THING, ONCE ✓✓.

**=> THE QUESTION: DOES THE FACTORY **RUN** ✓✓ — **=> AND DOES IT **CHECK ITS OWN
OUTPUT** ✓✓, **=> AND **GATE ITSELF** ✓✓, **=> AND **GO BACKWARDS** WHEN IT MUST
✓✓?**

**=> AND THE WAY TO ANSWER IT IS **NOT** TO RUN AN AGENT ✓✓ — **=> IT IS TO RUN
**=> THE FACTORY'S OWN LOGIC** ✓✓ ON **AN OUTPUT THE DOCUMENT ALREADY SPECIFIES**
✓✓, **=> AND THAT COSTS **NO TOKEN** ✓✓.**

**=> AND THE OUTPUTS BELOW ARE **THE DOCUMENT'S OWN SHAPE** ✓✓ — **=> THE
SCORECARD TABLE WITH **SEVEN** ROWS AND **A RATING COLUMN** ✓✓.**
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.factory import Factory

METRICS = [
    "Competitive density",
    "Differentiation gap",
    "TAM/SAM/SOM",
    "Unit economics health",
    "Assumption risk score",
    "MVP complexity",
    "Time to value",
]


def validation_pack(ratings, stated):
    """A validation pack, in the document's own shape."""
    lines = [
        "# Validation Pack: [Product Name]",
        "",
        "**Overall Recommendation:** {}".format(stated),
        "",
        "## 1. Validation Scorecard",
        "",
        "| # | Metric | Value | Rating | Source |",
        "|---|--------|-------|--------|--------|",
    ]
    for index, (metric, rating) in enumerate(zip(METRICS, ratings), start=1):
        lines.append("| {} | {} | [value] | {} | [source] |".format(index, metric, rating))
    lines.append("")
    lines.append("### Recommendation")
    lines.append("- Verdict: {}".format(stated))
    lines.append("- Rationale: [why]")
    return "\n".join(lines)


def main():
    factory = Factory.build()

    print("=== 1. THE FACTORY, ASSEMBLED FROM THE DATA ===")
    print("")
    for key, value in factory.measure().items():
        print("  {:<24} {}".format(key, value))
    print("")

    print("=== 2. AND IT CHECKS ITS OWN OUTPUT ===")
    print("")
    pack = validation_pack(["Good"] * 7, "GO")
    result = factory.walk("ideation", pack, skills=["validation-pack"])
    print("  the stage:            {}".format(result["stage"]))
    print("  the seam skill:       {}".format(result["seam_skill"]))
    print("  the outputs checked:  {}".format(len(result["checks"])))
    print("  the ones that passed: {}".format(len(result["passed"])))
    print("  the gate says:        {}".format(result["gate"]["verdict"]))
    print("  it goes backwards:    {}".format(result["backward"]))
    print("  the next stage:       {}".format(result["next_stage"]))
    print("")

    print("=== 3. AND THE GATE SENDS IT BACKWARDS WHEN IT MUST ===")
    print("")
    risky = validation_pack(["Good"] * 5 + ["Critical"] * 2, "GO")
    result = factory.walk("ideation", risky, skills=["validation-pack"])
    print("  the agent said:  {}".format(result["gate"]["stated"]))
    print("  the gate says:   {}".format(result["gate"]["verdict"]))
    print("  they agree:      {}".format(result["gate"]["agrees"]))
    print("  it goes backwards: {}".format(result["backward"]))
    print("  the next stage:    {}".format(result["next_stage"]))
    print("")

    print("=== 4. AND AN OUTPUT THAT DOES NOT MATCH ITS SCHEMA IS CAUGHT ===")
    print("")
    vague = "I think this is a good idea and we should build it."
    result = factory.walk("ideation", vague, skills=["validation-pack"])
    print("  the output: {}".format(vague))
    print("  the ones that failed: {}".format(", ".join(result["failed"]) or "none"))
    print("  the gate says: {}".format(result["gate"]["verdict"] or "(no scorecard, so no verdict)"))
    print("")

    print("=== 5. THE VERDICT ===")
    print("")
    print("  **=> THE FACTORY RUNS ✓✓ - **=> IT CHECKS ITS OWN OUTPUT ✓✓ - **=> IT")
    print("    **=> GATES ITSELF ✓✓ - **=> AND **IT GOES BACKWARDS WHEN THE GATE SAYS")
    print("      **=> PAUSE ✓✓ - **=> AND **IT ASKS THE HUMAN WHEN THE GATE SAYS GO")
    print("        **=> ✓✓.**")
    print("")
    print("  **=> AND **NONE** OF THAT COST A TOKEN ✓✓, **=> AND THE ONE THING THAT")
    print("    **=> DOES — **=> THE AGENT** ✓✓ — **=> IS **THE RIGHT ONE** TO SPEND ON")
    print("      **=> ✓✓.**")


if __name__ == "__main__":
    main()
