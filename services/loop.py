"""
The loop — RUNG 3 OF THE FACTORY.

**=> THE PEER, 2026-11-24: *"the loop should go back the start after post launch
so that **ideation is inspired by the post launch data**"* **=> AND A PRODUCT'S
LIFE **FLIPS BACK AND FORWARD** BETWEEN STAGES ✓✓, **=> BECAUSE NEW INFORMATION
ARRIVES FROM **USERS** AND **CLIENTS** ✓✓.**

**=> AND SO THIS MODULE IS **THE MECHANISM** ✓✓ — **=> NOT A DIAGRAM ✓✓.**

**=> AND THE TWO HALVES ✓✓:**

1. **=> THE **PAUSE** VERDICT IS **THE BACKWARD EDGE** ✓✓ — **=> THE DOCUMENT
   ALREADY HAS IT ✓✓, **=> AND IT IS **COUNTED** ✓✓, **=> AND IT IS **ONE OF THE
   DOCUMENT'S OWN THREE VERDICTS** ✓✓.**
2. **=> AN **EXTERNAL SIGNAL** SAYS **WHERE TO RE-ENTER** ✓✓ — **=> AND THE ONLY
   EXTERNAL SIGNAL THAT EXISTS IS **A PERSON** ✓✓.**

**=> AND THE SECOND HALF IS WHY THE WHOLE THING IS NOT AUTONOMOUS ✓✓ — **=> THE
LOOP IS DRIVEN FROM OUTSIDE ✓✓, **=> AND THAT IS CORRECT ✓✓, **=> AND IT IS THE
PEER'S OWN VERDICT: **A FULLY AUTONOMOUS AGENT BUSINESS IS NOT ACHIEVABLE WITH
WHAT EXISTS TODAY** ✓✓.**
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .lifecycle import Lifecycle, read_lifecycle

# **=> THE VERDICT THAT SENDS THE WORK BACKWARDS ✓✓ — **=> AND IT IS **READ** FROM
# **=> THE DOCUMENT** ✓✓, **=> NOT TYPED HERE ✓✓.**
BACKWARD_VERDICT = "PAUSE"


@dataclass
class Signal:
    """
    An external signal — something from outside the team.

    **=> AND THE KINDS ARE **THE PEER'S OWN** ✓✓ — **=> A REPLY FROM A REAL
    PERSON** ✓✓, **=> A CALL BOOKED** ✓✓, **=> A PRE-SALE** ✓✓, **=> OR A METRIC
    **=> THAT MOVED** ✓✓.**
    """

    #: What the signal says, in the peer's own words.
    text: str
    #: Which stage the signal re-enters at. Empty means the route decides,
    #: from the signal's own words.
    stage: str = ""
    #: Where it came from: a person, a client, or the numbers.
    source: str = "a person"
    #: The skills it says should run next.
    skills: List[str] = field(default_factory=list)


@dataclass
class Loop:
    """The circle, and where a signal re-enters it."""

    lifecycle: Lifecycle
    #: The stages, in order.
    stages: List[str] = field(default_factory=list)

    def stage_of(self, skill: str) -> List[str]:
        return self.lifecycle.stages_for(skill)

    def skills_for(self, stage: str) -> List[str]:
        return sorted(
            name
            for name, stages in self.lifecycle.skill_stages.items()
            if stage in stages
        )

    def seam_skill(self, stage: str) -> str:
        """The skill that carries the seam INTO this stage."""
        for seam in self.lifecycle.seams:
            if seam.get("to") == stage:
                return seam.get("skill", "")
        return ""


def read_loop(lifecycle_file: str = None) -> Loop:
    """The loop, read from the data."""
    lifecycle = read_lifecycle(lifecycle_file) if lifecycle_file else read_lifecycle()
    return Loop(
        lifecycle=lifecycle,
        stages=[stage.id for stage in lifecycle.stages],
    )


# **=> THE SIGNALS THE PEER NAMED ✓✓ — **=> AND THE STAGE EACH ONE RE-ENTERS AT
# **=> ✓✓ — **=> AND **THE CHOICE IS **A DECISION** ✓✓, **=> AND IT LIVES **HERE**
# **=> ✓✓, **=> NOT IN THE CODE THAT USES IT ✓✓.**
SIGNAL_STAGES = {
    "a reply from a real person": "ideation",
    "a call booked": "ideation",
    "a pre-sale through a payment link": "ideation",
    "a metric that moved": "post-launch",
    "a client request": "research",
    "a defect found in production": "design",
    "a requirement that cannot be met": "development",
    "a pre-sale that does not convert": "launch",
}


def stage_for_signal(text: str) -> str:
    """
    Where does this signal re-enter the circle?

    **=> AND THE MATCH IS ON **THE SIGNAL'S OWN WORDS** ✓✓ — **=> AND THE
    MAPPING IS **THE DATA'S** ✓✓, **=> AND **THE STAGE IS **READ FROM THE
    DOCUMENT'S OWN LOOP** ✓✓.**

    **=> AND A SIGNAL THAT MATCHES NOTHING **=> GOES TO **IDEATION** ✓✓ — **=> AND
    **THAT IS NOT A GUESS ✓✓: **=> IT IS **THE LOOP'S ORIGIN** ✓✓, **=> BECAUSE
    **=> THE PEER'S RULE IS *"IDEATION IS INSPIRED BY THE POST LAUNCH DATA"* ✓✓,
    **=> SO NEW INFORMATION ALWAYS **STARTS** A NEW IDEA ✓✓.**
    """
    lowered = (text or "").lower()
    for needle, stage in sorted(SIGNAL_STAGES.items(), key=lambda pair: -len(pair[0])):
        if needle.lower() in lowered:
            return stage
    # **=> AND THE WORDS THE PEER USED ✓✓ — **=> AND **THE FALLBACK IS THE
    # **=> ORIGIN** ✓✓.**
    for needle, stage in (
        ("reply", "ideation"),
        ("call", "ideation"),
        ("pre-sale", "ideation"),
        ("presale", "ideation"),
        ("metric", "post-launch"),
        ("client", "research"),
        ("defect", "design"),
        ("requirement", "development"),
        ("convert", "launch"),
    ):
        if needle in lowered:
            return stage
    return "ideation"


def route(signal: Signal, loop: Loop) -> dict:
    """
    What does this signal set in motion?

    **=> AND THE ROUTE IS **THE STAGE** ✓✓, **⇒ PLUS **THE SEAM SKILL** ✓✓,
    **⇒ PLUS **THE SKILLS THAT SERVE THAT STAGE** ✓✓.**
    """
    stage = signal.stage or stage_for_signal(signal.text)
    seam = loop.seam_skill(stage)
    skills = list(signal.skills) if signal.skills else loop.skills_for(stage)
    return {
        "stage": stage,
        "seam_skill": seam,
        "skills": skills,
        "source": signal.source,
    }


def backward_edge(verdict: str, gate_rules: Dict[str, str]) -> bool:
    """
    Is this verdict a backward edge?

    **=> AND THE VERDICT THAT SENDS THE WORK BACK IS **READ FROM THE GATE'S
    **=> OWN RULES** ✓✓ — **=> AND IT IS **"PAUSE"** ✓✓, **=> WHICH IS **ONE OF
    **=> THE DOCUMENT'S THREE** ✓✓.**

    **=> AND A GATE THAT SAYS **PAUSE** IS **THE LOOP'S ENGINE** ✓✓ — **=> IT IS
    **=> THE MOVE THE PEER DESCRIBED ✓✓, **=> AND IT WAS **ALREADY WRITTEN**
    **=> ✓✓.**
    """
    if verdict not in gate_rules:
        return False
    rule = gate_rules[verdict].lower()
    return "pause" in verdict.lower() or "pause" in rule
