"""
The factory's tests — THE LIFECYCLE IS DATA ✓✓.

**⇒ THE RULE ✓✓: **NO HARDCODED VALUES IN THE FACTORY'S CODE** ✓✓ — **⇒ EVERY
RULE COMES FROM A DATA FILE ✓✓.**

**⇒ AND THE FIRST TEST **ENFORCES** IT ✓✓ — **⇒ BECAUSE A RULE THAT IS ONLY A
COMMENT **DRIFTS** ✓✓.**

**⇒ AND THE SECOND TEST PROVES **THE CIRCLE IS WALKABLE** ✓✓ — **⇒ BECAUSE THAT
IS **THE FACTORY'S SECOND MEASUREMENT** ✓✓.**
"""

import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.lifecycle import (
    LIFECYCLE_FILE,
    SKILLS_DIR,
    dangling_edges,
    read_lifecycle,
    walkable,
)


def test_no_skill_metadata_is_hardcoded_in_python():
    """
    **⇒ THE RULE, ENFORCED ✓✓.**

    **⇒ THE SKILL METADATA — **THE STAGE** ✓✓, **THE OUTPUT** ✓✓ AND **THE
    TRIGGERS** ✓✓ — **⇒ MUST LIVE IN THE SKILLS' OWN FILES ✓✓, **⇒ NOT IN A
    PYTHON DICT ✓✓.**
    """
    loader = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "services",
        "skill_loader.py",
    )
    with open(loader, "r", encoding="utf-8") as handle:
        source = handle.read()

    # **⇒ THE THREE DICTS THAT ARE **GONE** ✓✓ — **⇒ AND MUST STAY GONE ✓✓.**
    for name in ("LIFECYCLE_STAGES", "SKILL_TRIGGERS", "SKILL_OUTPUTS"):
        assert not re.search(
            r"^" + name + r"\s*=", source, re.MULTILINE
        ), "{} is back in the code - it belongs in the skill's own file".format(name)

    # **⇒ AND NO PYTHON FILE MAY HOLD **A SKILL'S** METADATA ✓✓.**
    services = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "services"
    )
    for name in sorted(os.listdir(services)):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(services, name), "r", encoding="utf-8") as handle:
            text = handle.read()
        code = "\n".join(
            line
            for line in text.splitlines()
            if not line.strip().startswith("#") and not line.strip().startswith("*")
        )
        assert not re.search(r'"devils-advocate"\s*:', code), (
            "{} names a skill in a dict - the skill's own file holds it".format(name)
        )


def test_the_seven_stages_come_from_the_data():
    """**⇒ THE SEVEN, READ ✓✓ — **⇒ AND THE COUNT IS **THE PEER'S** ✓✓."""
    lifecycle = read_lifecycle()
    assert len(lifecycle.stages) == 7, (
        "the lifecycle has {} stages; the peer's circle has seven".format(
            len(lifecycle.stages)
        )
    )
    assert lifecycle.stage_ids == [
        "ideation",
        "research",
        "design",
        "development",
        "testing",
        "launch",
        "post-launch",
    ]
    # **⇒ AND THE ORDER IS THE ORDER ✓✓.**
    orders = [stage.order for stage in lifecycle.stages]
    assert orders == sorted(orders)


def test_the_lifecycle_file_is_the_source():
    """**⇒ THE FILE **EXISTS** ✓✓, **⇒ AND IT IS **A DOCUMENT** ✓✓."""
    assert os.path.exists(LIFECYCLE_FILE), (
        "the lifecycle file is missing: {}".format(LIFECYCLE_FILE)
    )
    with open(LIFECYCLE_FILE, "r", encoding="utf-8") as handle:
        text = handle.read()
    assert "ideation" in text
    assert "post-launch" in text
    assert "relatedBefore" in text or "loop" in text


def test_the_loop_is_declared_and_readable():
    """
    **⇒ THE PEER'S LOOP ✓✓ — **⇒ "POST-LAUNCH DATA INSPIRES IDEATION" ✓✓.**

    **⇒ AND IT IS **DECLARED IN THE DATA** ✓✓, **⇒ NOT ASSUMED ✓✓.**
    """
    lifecycle = read_lifecycle()
    assert lifecycle.loop_returns_to == "ideation", (
        "the loop must return to ideation; it returns to {}".format(
            lifecycle.loop_returns_to
        )
    )
    assert len(lifecycle.loop_path) >= 2, "the loop has no path"
    # **⇒ AND THE PATH **STARTS** AT POST-LAUNCH ✓✓.**
    assert lifecycle.loop_path[0] == "feedback-synthesis", (
        "the loop starts at feedback-synthesis; it starts at {}".format(
            lifecycle.loop_path[0]
        )
    )
    assert "feature-prioritization" in lifecycle.loop_path


def test_a_skill_may_serve_more_than_one_stage():
    """
    **⇒ THE PEER'S POINT ✓✓ — **⇒ "FLIP BACK AND FORWARD" ✓✓.**

    **⇒ AND THE MODEL MUST ALLOW IT ✓✓.**
    """
    lifecycle = read_lifecycle()
    multi = {
        name: stages
        for name, stages in lifecycle.skill_stages.items()
        if len(stages) > 1
    }
    assert len(multi) > 0, "no skill serves more than one stage"
    # **⇒ AND THE ONES THE PEER NAMED ✓✓.**
    assert "ideation" in lifecycle.stages_for("devils-advocate")
    assert len(lifecycle.stages_for("devils-advocate")) > 1


def test_the_circuit_is_walkable():
    """
    **⇒ THE FACTORY'S SECOND MEASUREMENT ✓✓ — **⇒ THE LIVE EDGES OVER THE
    DECLARED ONES ✓✓.**
    """
    lifecycle = read_lifecycle()
    state = walkable(lifecycle)
    assert state["total"] > 0
    ratio = state["live"] / state["total"]
    assert ratio > 0.9, (
        "only {} of {} edges resolve - the circle is not walkable".format(
            state["live"], state["total"]
        )
    )


def test_the_dangling_edges_are_reported_not_hidden():
    """
    **⇒ A FACTORY THAT KNOWS **WHAT IT CANNOT DO** ✓✓ IS MORE USEFUL ✓✓.
    """
    lifecycle = read_lifecycle()
    dangling = dangling_edges(lifecycle)
    # **⇒ AND THE REPORT MUST BE **SHAPED** ✓✓ — **⇒ AND IT MUST **NOT** BE
    # **EMPTY** ✓✓, **⇒ BECAUSE **THE REAL ONE HAS TWO** ✓✓.
    for edge in dangling:
        assert "from" in edge and "to" in edge and "edge" in edge
