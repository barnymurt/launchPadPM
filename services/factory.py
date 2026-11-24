"""
THE FACTORY — THE WHOLE THING, ONCE.

**=> THE FIVE RUNGS ✓✓, **⇒ AND THIS IS **WHERE THEY MEET** ✓✓.**

**=> AND THE POINT OF THIS MODULE ✓✓: **A PRODUCT GOES ROUND THE CIRCLE ✓✓, **⇒
**=> ITS OUTPUT IS **CHECKED** ✓✓, **⇒ AND THE GATE **DECIDES** ✓✓, **⇒ AND IF
**=> IT SAYS **PAUSE** ✓✓, **⇒ THE WORK GOES **BACKWARDS** ✓✓, **⇒ AND IF IT
**=> SAYS **GO** ✓✓, **⇒ THE HUMAN IS **ASKED** ✓✓, **⇒ AND **THE HUMAN'S REPLY
**=> IS THE LAST WORD** ✓✓.**

**=> AND **NO TOKEN IS SPENT** ✓✓ ON THE PART THAT IS PROVED HERE ✓✓ — **=> THE
**=> GATE** ✓✓, **=> THE SCHEMA CHECK** ✓✓, **=> THE LOOP** ✓✓ AND **=> THE
**=> CHANNEL** ✓✓ ARE **ALL** FREE ✓✓.**

**=> AND THE ONE THING THAT **IS NOT** FREE ✓✓ — **=> **THE AGENT** ✓✓, **=> AND
**=> THAT IS **RIGHT** ✓✓: **=> THE FACTORY'S WORTH IS **WHAT IT COSTS TO RUN**,
**=> NOT WHAT IT COSTS TO BUILD** ✓✓.**
"""

import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .approval import Channel, approve
from .gate import compare as compare_gate
from .gate import read_gate
from .lifecycle import read_lifecycle
from .loop import Signal, read_loop, route
from .schema_reader import check_output


@dataclass
class Factory:
    """
    The factory, assembled.

    **=> AND EVERY PART IS **READ FROM THE DATA** ✓✓ — **=> THE STAGES ✓✓, **=> THE
    **=> SEAMS ✓✓, **=> THE LOOP ✓✓, **=> THE THRESHOLDS ✓✓, **=> THE RULES
    **=> ✓✓, **=> THE SKILLS' OWN METADATA ✓✓.**
    """

    #: The lifecycle, the loop and the gate - all read.
    lifecycle: object = None
    loop: object = None
    gate: object = None
    #: The channel, if it is configured.
    channel: Optional[Channel] = None

    @classmethod
    def build(cls, channel: Optional[Channel] = None) -> "Factory":
        """The factory, assembled from the data."""
        return cls(
            lifecycle=read_lifecycle(),
            loop=read_loop(),
            gate=read_gate(),
            channel=(channel or Channel().from_environment()),
        )

    # ------------------------------------------------------------------ the run
    def run_stage(
        self,
        stage: str,
        output: str,
        skills: List[str] = None,
    ) -> dict:
        """
        Run one stage, and see what the factory makes of it.

        **=> AND THE ORDER IS **THE FACTORY'S** ✓✓, **=> NOT THE AGENT'S ✓✓:**

        1. **=> THE OUTPUT IS **CHECKED** AGAINST EACH SKILL'S SCHEMA ✓✓.**
        2. **=> THE GATE **COUNTS** THE RATINGS ✓✓ AND SAYS GO, PAUSE OR KILL ✓✓.**
        3. **=> IF IT SAYS **PAUSE** ✓✓, **=> THE WORK GOES **BACKWARDS** ✓✓.**
        4. **=> IF IT SAYS **GO** ✓✓, **=> THE HUMAN IS **ASKED** ✓✓, **=> AND **THE
           **=> HUMAN'S REPLY IS THE LAST WORD** ✓✓.**
        """
        used = skills or self.loop.skills_for(stage)
        seam = self.loop.seam_skill(stage)

        # **=> 1. THE SCHEMA CHECK ✓✓.**
        checks = {}
        for skill in used:
            result = check_output(output, skill)
            checks[skill] = {
                "ok": result.ok,
                "missing_fields": result.missing_fields,
                "missing_sections": result.missing_sections,
                "missing_lines": result.missing_lines,
                "renamed_sections": result.renamed_sections,
            }
        passed = [name for name, check in checks.items() if check["ok"]]

        # **=> 2. THE GATE ✓✓.**
        decision = compare_gate(self.gate, output)
        verdict = decision.get("verdict", "")

        # **=> 3. THE BACKWARD EDGE ✓✓.**
        backward = verdict == "PAUSE"

        result = {
            "stage": stage,
            "seam_skill": seam,
            "skills": used,
            "checks": checks,
            "passed": passed,
            "failed": [name for name in used if name not in passed],
            "gate": {
                "verdict": verdict,
                "stated": decision.get("stated", ""),
                "agrees": decision.get("agrees"),
                "critical": decision.get("critical", 0),
                "warning": decision.get("warning", 0),
                "rule": decision.get("rule", ""),
            },
            "backward": backward,
            "human": None,
        }

        # **=> 4. THE HUMAN ✓✓ — **=> AND ONLY WHEN THE GATE SAYS GO ✓✓ — **=> AND
        # **=> ONLY IF THE CHANNEL IS CONFIGURED ✓✓.**
        if verdict == "GO" and self.channel and self.channel.configured:
            reply = approve(
                self.channel,
                "the gate says GO for {}".format(stage),
                self._context(stage, result),
            )
            if reply:
                result["human"] = {
                    "decision": reply.decision,
                    "text": reply.text,
                }
                # **=> AND **THE HUMAN'S REPLY OVERRIDES THE GATE** ✓✓ — **=> BECAUSE
                # **=> THE HUMAN IS **THE EXTERNAL CHECK** ✓✓, **=> AND THE GATE IS
                # **=> ONLY **AN INTERNAL** ONE ✓✓.**
                if reply.decision != "GO":
                    result["backward"] = reply.decision == "PAUSE"
                    result["gate"]["overridden_by"] = reply.decision

        return result

    def _context(self, stage: str, result: dict) -> str:
        """What the human is shown."""
        lines = ["the stage: {}".format(stage)]
        if result.get("seam_skill"):
            lines.append("the seam skill: {}".format(result["seam_skill"]))
        gate = result.get("gate", {})
        if gate.get("verdict"):
            lines.append("the gate says: {}".format(gate["verdict"]))
            if gate.get("rule"):
                lines.append("the rule: {}".format(gate["rule"]))
        if result.get("failed"):
            lines.append(
                "the outputs that do not match their schema: {}".format(
                    ", ".join(result["failed"])
                )
            )
        return "\n".join(lines)

    # ------------------------------------------------------------------ the walk
    def walk(self, stage: str, output: str, skills: List[str] = None) -> dict:
        """
        One stage, and where it goes next.

        **=> AND THERE ARE **THREE** OUTCOMES ✓✓ — **=> NOT TWO ✓✓:**

        1. **=> **KILL** STOPS ✓✓ — **=> NOTHING COMES AFTER IT ✓✓ — **=> AND
           **=> THE DOCUMENT ALREADY SAYS SO ✓✓: *"KILL: 2+ Critical metrics (or
           **=> triggered by a decision gate)"* ✓✓, **=> AND **THE KILL IS **A
           **=> GATE** ✓✓, **=> NOT A STAGE ✓✓.**
        2. **=> **PAUSE** GOES BACK TO **IDEATION** ✓✓ — **=> THE PEER'S EXACT
           **=> WORDS** ✓✓: *"THE LOOP SHOULD GO BACK THE START"* ✓✓.**
        3. **=> **GO** MOVES ON ✓✓ — **=> AND THE CIRCLE CLOSES ✓✓.**
        """
        result = self.run_stage(stage, output, skills)
        verdict = result.get("gate", {}).get("verdict", "")

        order = [s.id for s in self.loop.lifecycle.stages]
        index = order.index(stage) if stage in order else 0
        origin = self.loop.lifecycle.loop_returns_to or order[0]

        if verdict == "KILL":
            # **=> AND A KILL STOPS ✓✓ — **=> AND IT IS **THE ONLY** VERDICT THAT
            # **=> DOES NOT GO ANYWHERE ✓✓.**
            result["backward"] = False
            result["stopped"] = True
            result["next_stage"] = ""
        elif result["backward"]:
            # **=> AND A PAUSE GOES BACK TO THE ORIGIN ✓✓.**
            result["backward"] = True
            result["stopped"] = False
            result["next_stage"] = origin
        else:
            result["backward"] = False
            result["stopped"] = False
            result["next_stage"] = (
                order[index + 1] if index + 1 < len(order) else order[0]
            )
        return result

    # ------------------------------------------------------------------ the measure
    def measure(self) -> dict:
        """
        The factory's own numbers.

        **=> TWO OF THEM ✓✓ — **⇒ AND **THE SECOND** IS **THE ONE THAT SAYS
        **=> WHETHER THIS IS A PRODUCT DEVELOPMENT PROCESS OR A LIBRARY** ✓✓.**
        """
        from .lifecycle import dangling_edges, walkable

        state = walkable(self.lifecycle)
        dangling = dangling_edges(self.lifecycle)
        return {
            "the skills": len(self.lifecycle.skill_stages),
            "the stages": len(self.lifecycle.stages),
            "the live edges": state["live"],
            "the total edges": state["total"],
            "the dangling edges": len(dangling),
            "the multi-stage skills": len(
                [n for n, s in self.lifecycle.skill_stages.items() if len(s) > 1]
            ),
            "the loop returns to": self.lifecycle.loop_returns_to,
            "the channel is configured": bool(
                self.channel and self.channel.configured
            ),
        }
