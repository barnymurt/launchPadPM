"""
THE GATE PROBE - RUNG 2 PROOF.

**=> THE QUESTION: DOES THE GATE DECIDE ARITHMETICALLY ✓✓, **=> AND DOES IT
CATCH AN AGENT THAT RATES ITSELF GENEROUSLY ✓✓?**

**=> AND THE WAY TO ANSWER IT IS TO BUILD **THE OUTPUTS THE DOCUMENT ALREADY
SPECIFIES** ✓✓ — **=> THE SCORECARD TABLE WITH **SEVEN** ROWS AND **A RATING
COLUMN** ✓✓ — **=> AND THEN CHANGE **THE RATINGS** ✓✓ AND SEE WHAT THE GATE
SAYS ✓✓.**

**=> AND NO TOKEN IS SPENT ✓✓ — **=> THE CHECK IS FREE ✓✓.**
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gate import compare, decide, read_gate


def scorecard(ratings):
    """
    A scorecard, in the document's own shape.

    **=> AND THE HEADER IS THE DOCUMENT'S HEADER ✓✓ — **=> THE METRIC NAMES ARE
    **=> THE DOCUMENT'S OWN** ✓✓ — **=> AND THE RATINGS ARE WHAT WE CHANGE ✓✓.**
    """
    rows = [
        "Competitive density",
        "Differentiation gap",
        "TAM/SAM/SOM",
        "Unit economics health",
        "Assumption risk score",
        "MVP complexity",
        "Time to value",
    ]
    lines = [
        "# Validation Pack: [Product Name]",
        "",
        "**Overall Recommendation:** PLACEHOLDER",
        "",
        "## 1. Validation Scorecard",
        "",
        "| # | Metric | Value | Rating | Source |",
        "|---|--------|-------|--------|--------|",
    ]
    for index, (metric, rating) in enumerate(zip(rows, ratings), start=1):
        lines.append(
            "| {} | {} | [value] | {} | [source] |".format(index, metric, rating)
        )
    lines.append("")
    lines.append("## 2. Recommendation")
    lines.append("")
    lines.append("### Recommendation")
    lines.append("- Verdict: PLACEHOLDER")
    lines.append("- Rationale: [why]")
    return "\n".join(lines)


def main():
    gate = read_gate()
    print("=== 1. THE GATE, READ FROM THE DOCUMENT ===")
    print("")
    print("  the gates:  {}".format(len(gate.thresholds)))
    print("  the rules:  {}".format(len(gate.rules)))
    print("  the metrics: {}".format(len(gate.expected_metrics)))
    print("")

    print("=== 2. AND IT COUNDS, IT DOES NOT CHOOSE ===")
    print("")
    cases = [
        ("all good", ["Good"] * 7),
        ("one warning", ["Good"] * 6 + ["Warning"]),
        ("one critical", ["Good"] * 6 + ["Critical"]),
        ("two criticals", ["Good"] * 5 + ["Critical"] * 2),
        ("three warnings", ["Good"] * 4 + ["Warning"] * 3),
    ]
    for label, ratings in cases:
        output = scorecard(ratings)
        decision = decide(gate, output)
        print(
            "  {:<16} {:<3} critical, {:<3} warning -> {}".format(
                label,
                decision["critical"],
                decision["warning"],
                decision["verdict"],
            )
        )
    print("")

    print("=== 3. AND THE DOCUMENT'S OWN RULES, READ BACK ===")
    for verdict, rule in gate.rules.items():
        print("  {:<6} {}".format(verdict, rule))
    print("")

    print("=== 4. AND IT CATCHES AN AGENT THAT RATES ITSELF GENEROUSLY ===")
    print("")
    print("  **=> AN AGENT THAT SAYS **GO** BUT RATES ONE METRIC CRITICAL **=>**")
    print("      **=> THE GATE SAYS **PAUSE** - **=> AND THAT IS THE POINT - **=>**")
    print("")

    dishonest = scorecard(["Good"] * 6 + ["Critical"])
    dishonest = dishonest.replace("**Overall Recommendation:** PLACEHOLDER",
                                  "**Overall Recommendation:** GO")
    dishonest = dishonest.replace("- Verdict: PLACEHOLDER", "- Verdict: GO")
    result = compare(gate, dishonest)
    print("    the agent says:  {}".format(result["stated"]))
    print("    the gate says:   {}".format(result["verdict"]))
    print("    they agree:      {}".format(result["agrees"]))
    print("")

    honest = scorecard(["Good"] * 7)
    honest = honest.replace("**Overall Recommendation:** PLACEHOLDER",
                            "**Overall Recommendation:** GO")
    honest = honest.replace("- Verdict: PLACEHOLDER", "- Verdict: GO")
    result = compare(gate, honest)
    print("    and when the agent is honest:")
    print("      the agent says:  {}".format(result["stated"]))
    print("      the gate says:   {}".format(result["verdict"]))
    print("      they agree:      {}".format(result["agrees"]))
    print("")

    print("=== 5. THE VERDICT ===")
    print("")
    print("  **=> THE GATE COUNTS THE RATINGS ✓✓ - **=> AND THE COUNTS COME FROM")
    print("    **=> THE DOCUMENT ✓✓ - **=> AND THE AGENT'S VERDICT IS COMPARED")
    print("      **=> AGAINST IT ✓✓ - **=> SO **THE AGENT CANNOT DECIDE ITS OWN")
    print("        **=> VERDICT** ✓✓ - **=> WHICH IS THE STRUCTURAL ANSWER TO")
    print("          **=> \"THEY ARE JUST REVIEWING EACH OTHER IN A VACUUM\" ✓✓.**")


if __name__ == "__main__":
    main()
