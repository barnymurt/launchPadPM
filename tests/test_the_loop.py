"""
The factory's loop tests — RUNG 3 ✓✓.

**=> THE PEER, 2026-11-24: *"the loop should go back the start after post launch
so that **ideation is inspired by the post launch data**"* ✓✓ — **=> AND THE
LOOP IS **THE MECHANISM** ✓✓, **=> NOT A DIAGRAM ✓✓.**
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gate import read_gate
from services.loop import (
    Signal,
    backward_edge,
    read_loop,
    route,
    stage_for_signal,
)


@pytest.fixture(scope="module")
def loop():
    return read_loop()


def test_the_loop_returns_to_ideation(loop):
    """**=> THE PEER'S EXACT WORDS ✓✓."""
    assert loop.lifecycle.loop_returns_to == "ideation"
    assert loop.stages == [
        "ideation",
        "research",
        "design",
        "development",
        "testing",
        "launch",
        "post-launch",
    ]


def test_the_loop_path_is_the_post_launch_to_ideation_path(loop):
    """**=> POST-LAUNCH DATA → RESEARCH → IDEATION ✓✓."""
    path = loop.lifecycle.loop_path
    assert path[0] == "feedback-synthesis"
    assert "feature-prioritization" in path


def test_a_reply_from_a_real_person_re_enters_at_ideation(loop):
    """
    **=> THE PEER'S POINT 2 ✓✓ — **=> *"A REPLY FROM A REAL PERSON"* IS PROGRESS
    ✓✓ — **=> AND IT IS **WHAT DRIVES THE CIRCLE** ✓✓.**
    """
    for text in (
        "a reply from a real person: it is missing the thing we need",
        "a call booked with a client who wants reporting",
        "a pre-sale through a payment link",
    ):
        assert stage_for_signal(text) == "ideation", text

    result = route(Signal(text="a reply from a real person: it is missing X"), loop)
    assert result["stage"] == "ideation"
    # **=> AND THE SEAM SKILL FOR IDEATION IS **THE LOOP'S HEAD** ✓✓.**
    assert result["seam_skill"] == "product-vision"
    assert len(result["skills"]) > 0


def test_a_metric_re_enters_at_post_launch(loop):
    """**=> THE NUMBERS COME FROM **AFTER** THE LAUNCH ✓✓."""
    assert stage_for_signal("a metric that moved: churn doubled") == "post-launch"


def test_an_unknown_signal_returns_to_the_origin(loop):
    """
    **=> AND THE FALLBACK IS **THE ORIGIN** ✓✓ — **=> AND THAT IS NOT A GUESS
    ✓✓: **=> NEW INFORMATION ALWAYS **STARTS** A NEW IDEA ✓✓.**
    """
    assert stage_for_signal("something entirely unexpected") == "ideation"


def test_pause_is_the_backward_edge():
    """
    **=> THE DOCUMENT'S OWN VERDICT IS **THE LOOP'S ENGINE** ✓✓ — **=> AND IT WAS
    **=> ALREADY WRITTEN** ✓✓.**
    """
    gate = read_gate()
    assert backward_edge("PAUSE", gate.rules) is True
    assert backward_edge("GO", gate.rules) is False
    assert backward_edge("KILL", gate.rules) is False


def test_every_stage_has_a_seam_skill(loop):
    """**=> AND EVERY STAGE **CAN BE RE-ENTERED** ✓✓ — **=> BECAUSE EVERY SEAM
    **=> HAS A SKILL** ✓✓."""
    for stage in loop.stages:
        assert loop.seam_skill(stage), "the stage {} has no seam skill".format(stage)


def test_the_seam_skills_are_in_the_library(loop):
    """**=> AND THE SEAM SKILLS **EXIST** ✓✓ — **=> OTHERWISE THE LOOP IS
    **DECLARED** AND NOT **WALKABLE** ✓✓."""
    from services.lifecycle import _skill_paths

    present = set(_skill_paths())
    for stage in loop.stages:
        skill = loop.seam_skill(stage)
        assert skill in present, "{} is not in the library".format(skill)
