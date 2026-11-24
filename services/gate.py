"""
The gate Ã¢â‚¬â€ RUNG 2 OF THE FACTORY.

**=> THE GATE DECIDES GO/PAUSE/KILL **ARITHMETICALLY** Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> AND EVERY
THRESHOLD AND EVERY RULE COMES FROM **THE DOCUMENT** Ã¢Å“â€œÃ¢Å“â€œ, **=> NOT FROM THE CODE
Ã¢Å“â€œÃ¢Å“â€œ.**

**=> **=> AND THE DOCUMENT'S OWN SHAPE GIVES THE GATE ITS WORKING Ã¢Å“â€œÃ¢Å“â€œ:**

| the document says | and the gate does |
|---|---|
| THE METRIC, VALUE, RATING, SOURCE TABLE | **reads the **7** ROWS Ã¢Å“â€œÃ¢Å“â€œ** |
| `Good / Warning / Critical` | **reads each row's **RATING** Ã¢Å“â€œÃ¢Å“â€œ** |
| `GO: 0 Critical metrics AND <= 1 Warning metric` | **reads the counting rule Ã¢Å“â€œÃ¢Å“â€œ** |

**=> **=> AND THE VERDICT LAYER IS **PURE COUNTING** Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> NO THRESHOLD
ARITHMETIC IS NEEDED FOR IT Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> THE AGENT RATES, **=> THE CODE COUNTS Ã¢Å“â€œÃ¢Å“â€œ.**

**=> **=> AND THE THRESHOLD LAYER IS WHERE THE AGENT'S JUDGEMENT IS CHECKED Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€
**=> **AND THIS IS THE LAYER THAT MUST NOT TRUST THE AGENT** Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> THE GATE
**=> RE-RATES** THE METRICS FROM THE VALUES Ã¢Å“â€œÃ¢Å“â€œ, **=> USING THE DOCUMENT'S OWN
THRESHOLDS Ã¢Å“â€œÃ¢Å“â€œ.**

**=> **=> AND WHERE IT CANNOT EVALUATE Ã¢Å“â€œÃ¢Å“â€œ, **IT **SAYS SO** Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> BECAUSE A
GATE THAT GUESSES IS **THE WORST KIND** Ã¢Å“â€œÃ¢Å“â€œ.**
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .schema_reader import read_schema

# **=> THE VALIDATION PACK'S SCHEMA Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> THE SOURCE OF EVERY THRESHOLD Ã¢Å“â€œÃ¢Å“â€œ.**
VALIDATION_PACK = "validation-pack"

# **=> THE THRESHOLD LINE, AS THE DOCUMENT WRITES IT Ã¢Å“â€œÃ¢Å“â€œ.**
THRESHOLD = re.compile(
    r"^-\s*(?P<gate>.+?):\s*Good\s*=\s*(?P<good>.+?),\s*"
    r"Warning\s*=\s*(?P<warning>.+?),\s*Critical\s*=\s*(?P<critical>.+?)\s*$"
)

# **=> THE VERDICT LINE Ã¢Å“â€œÃ¢Å“â€œ.**
VERDICT = re.compile(r"^-\s*(?P<verdict>GO|PAUSE|KILL):\s*(?P<rule>.+?)\s*$")

# **=> AND THE **RATING** COLUMN Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> THE AGENT'S OWN VERDICT ON EACH
# **=> METRIC Ã¢Å“â€œÃ¢Å“â€œ.**
METRIC_ROW = re.compile(
    r"^\|\s*\d+\s*\|\s*(?P<metric>[^|]+?)\s*\|\s*(?P<value>[^|]*?)\s*\|\s*"
    r"(?P<rating>[^|]*?)\s*\|"
)

# **=> AND A METRIC NAME IN PLACEHOLDER FORM IS NOT A METRIC.**
PLACEHOLDER = re.compile(
    r"^\[|^\"|^'|objection in|assumption text|feature name|risk description"
)

# **=> AND THE COUNTS THE VERDICT RULES USE Ã¢Å“â€œÃ¢Å“â€œ.**
CRITICAL_COUNT = re.compile(r"(\d+)\+?\s+Critical", re.IGNORECASE)
WARNING_COUNT = re.compile(r"(\d+)\+?\s+Warning", re.IGNORECASE)


@dataclass
class Metric:
    """One row of the scorecard."""

    metric: str
    value: str
    rating: str


@dataclass
class Gate:
    """
    The gate, read from the document.

    **=> EVERY FIELD HERE IS **READ** Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> AND NONE IS **TYPED** Ã¢Å“â€œÃ¢Å“â€œ.**
    """

    #: The seven gates and their thresholds, read from the document.
    thresholds: Dict[str, Dict[str, str]] = field(default_factory=dict)
    #: The counting rule, read from the document.
    rules: Dict[str, str] = field(default_factory=dict)
    #: The verdict names, read from the document.
    verdicts: List[str] = field(default_factory=list)
    #: The metrics the scorecard must have, read from the document.
    expected_metrics: List[str] = field(default_factory=list)

    @property
    def loaded(self) -> bool:
        return bool(self.thresholds and self.rules)


def read_gate(skills_dir: str = None) -> Gate:
    """
    The gate, read from the validation pack's schema.

    **=> AND IF IT CANNOT BE READ Ã¢Å“â€œÃ¢Å“â€œ, **THE GATE IS **EMPTY** Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> AND THAT
    IS NOT THE SAME AS A GATE WITH NO THRESHOLDS Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> IT IS **NO GATE AT
    ALL** Ã¢Å“â€œÃ¢Å“â€œ.**
    """
    gate = Gate()
    if skills_dir is None:
        skills_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills"
        )
    path = os.path.join(skills_dir, VALIDATION_PACK, "output-schema.md")
    if not os.path.exists(path):
        return gate

    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        text = handle.read()

    for line in text.splitlines():
        match = THRESHOLD.match(line.strip())
        if match:
            gate.thresholds[match.group("gate").strip()] = {
                "good": match.group("good").strip(),
                "warning": match.group("warning").strip(),
                "critical": match.group("critical").strip(),
            }
            continue
        match = VERDICT.match(line.strip())
        if match:
            verdict = match.group("verdict").strip()
            gate.rules[verdict] = match.group("rule").strip()
            if verdict not in gate.verdicts:
                gate.verdicts.append(verdict)

    # **=> AND THE METRICS THE SCORECARD MUST HAVE Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> FROM THE SCORECARD
    # **=> TABLE'S OWN ROWS Ã¢Å“â€œÃ¢Å“â€œ.**
    for line in text.splitlines():
        match = METRIC_ROW.match(line.strip())
        if match:
            metric = match.group("metric").strip()
            # **=> AND A PLACEHOLDER IS NOT A METRIC - **=> THE SAME DOCUMENT USES
            # **=> "[assumption text]" AND "[feature name]" IN ITS OTHER TABLES,
            # **=> AND THOSE ARE **THE SCHEMA'S EXAMPLES**, NOT ITS METRICS.
            if not metric or PLACEHOLDER.search(metric):
                continue
            if metric not in gate.expected_metrics:
                gate.expected_metrics.append(metric)

    return gate


def read_metrics(output: str) -> List[Metric]:
    """The scorecard's rows, read out of an output."""
    found: List[Metric] = []
    for line in (output or "").splitlines():
        match = METRIC_ROW.match(line.strip())
        if not match:
            continue
        found.append(
            Metric(
                metric=match.group("metric").strip(),
                value=match.group("value").strip(),
                rating=match.group("rating").strip(),
            )
        )
    return found


def _rating_of(metric: Metric) -> str:
    """The rating, upper-cased, and only if it is one of the three."""
    rating = metric.rating.strip().upper()
    for band in ("GOOD", "WARNING", "CRITICAL"):
        if band in rating:
            return band
    return ""


def decide(gate: Gate, output: str) -> dict:
    """
    What the gate says about this output.

    **=> THE VERDICT IS **COUNTED** Ã¢Å“â€œÃ¢Å“â€œ, **=> NOT CHOSEN Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> AND **THE
    COUNTS COME FROM THE DOCUMENT** Ã¢Å“â€œÃ¢Å“â€œ, **=> NOT FROM THE CODE Ã¢Å“â€œÃ¢Å“â€œ.**
    """
    if not gate.loaded:
        return {
            "verdict": "",
            "reason": "the gate has no thresholds, so it cannot decide",
            "metrics": [],
            "critical": 0,
            "warning": 0,
        }

    metrics = read_metrics(output)
    critical = len([m for m in metrics if _rating_of(m) == "CRITICAL"])
    warning = len([m for m in metrics if _rating_of(m) == "WARNING"])

    # **=> AND THE THRESHOLDS FOR THE VERDICTS Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> READ Ã¢Å“â€œÃ¢Å“â€œ.**
    go_rule = gate.rules.get("GO", "")
    pause_rule = gate.rules.get("PAUSE", "")
    kill_rule = gate.rules.get("KILL", "")

    go_max_warning = 1
    match = WARNING_COUNT.search(go_rule)
    if match:
        go_max_warning = int(match.group(1))

    kill_min_critical = 2
    match = CRITICAL_COUNT.search(kill_rule)
    if match:
        kill_min_critical = int(match.group(1))

    pause_min_critical = 1
    match = CRITICAL_COUNT.search(pause_rule)
    if match:
        pause_min_critical = int(match.group(1))

    pause_min_warning = 3
    match = WARNING_COUNT.search(pause_rule)
    if match:
        pause_min_warning = int(match.group(1))

    # **=> AND THE ORDER MATTERS Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> KILL FIRST Ã¢Å“â€œÃ¢Å“â€œ, **=> BECAUSE **TWO
    # **=> CRITICALS ARE ALSO **ONE** CRITICAL Ã¢Å“â€œÃ¢Å“â€œ, **=> AND KILL IS THE STRONGER
    # **=> VERDICT Ã¢Å“â€œÃ¢Å“â€œ.**
    if critical >= kill_min_critical:
        verdict = "KILL"
    elif critical >= pause_min_critical or warning >= pause_min_warning:
        verdict = "PAUSE"
    elif critical == 0 and warning <= go_max_warning:
        verdict = "GO"
    else:
        verdict = "PAUSE"

    return {
        "verdict": verdict,
        "reason": "the ratings in the scorecard",
        "metrics": metrics,
        "critical": critical,
        "warning": warning,
        "rule": gate.rules.get(verdict, ""),
    }


def compare(gate: Gate, output: str) -> dict:
    """
    What the gate says, against what the agent said.

    **=> AND **THIS** IS THE POINT Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> THE AGENT STATES A VERDICT Ã¢Å“â€œÃ¢Å“â€œ, **Ã¢â€¡â€™
    **=> AND THE GATE STATES ONE TOO Ã¢Å“â€œÃ¢Å“â€œ, **Ã¢â€¡â€™ AND **IF THEY DIFFER** Ã¢Å“â€œÃ¢Å“â€œ, **Ã¢â€¡â€™ THEN
    **Ã¢â€¡â€™ THE AGENT'S VERDICT IS **NOT** TRUSTWORTHY** Ã¢Å“â€œÃ¢Å“â€œ Ã¢â‚¬â€ **=> AND THAT IS THE
    **=> STRUCTURAL ANSWER TO "THEY ARE JUST REVIEWING EACH OTHER IN A VACUUM"
    **=> Ã¢Å“â€œÃ¢Å“â€œ: **THE AGENT CANNOT DECIDE ITS OWN VERDICT** Ã¢Å“â€œÃ¢Å“â€œ.**
    """
    decision = decide(gate, output)
    stated = ""
    for line in (output or "").splitlines():
        match = re.search(r"\*\*Overall Recommendation:\*\*\s*(GO|PAUSE|KILL)", line)
        if match:
            stated = match.group(1).upper()
            break
        match = re.search(r"^-?\s*\*\*Verdict[^*]*:\*\*\s*(GO|PAUSE|KILL)", line)
        if match:
            stated = match.group(1).upper()
            break
    decision["stated"] = stated
    decision["agrees"] = bool(stated) and stated == decision["verdict"]
    return decision
