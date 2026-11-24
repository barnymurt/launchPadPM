"""
The factory's own tests ✓✓.

**=> THE FIVE RUNGS, MEETING ✓✓ — **=> AND **THE PROOF IS THAT IT RUNS** ✓✓.**
"""

import os
import sys

import pytest

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


def validation_pack(ratings, stated="GO"):
    """A validation pack, in the document's own shape."""
    lines = [
        "# Validation Pack: [Product Name]",
        "",
        "**Overall Recommendation:** {}".format(stated),
        "",
        "| # | Metric | Value | Rating | Source |",
        "|---|--------|-------|--------|--------|",
    ]
    for index, (metric, rating) in enumerate(zip(METRICS, ratings), start=1):
        lines.append("| {} | {} | [value] | {} | [source] |".format(index, metric, rating))
    lines.append("")
    lines.append("- Verdict: {}".format(stated))
    return "\n".join(lines)


@pytest.fixture(scope="module")
def factory():
    return Factory.build()


def test_the_factory_assembles_from_the_data(factory):
    """**=> AND EVERY PART IS **READ** ✓✓."""
    measure = factory.measure()
    assert measure["the stages"] == 7
    assert measure["the skills"] > 40
    assert measure["the loop returns to"] == "ideation"
    assert measure["the multi-stage skills"] > 0


def test_the_circuit_is_walkable(factory):
    """**=> AND **THE CIRCLE IS **WALKABLE** ✓✓ — **=> THE FACTORY'S SECOND
    MEASUREMENT ✓✓."""
    measure = factory.measure()
    ratio = measure["the live edges"] / measure["the total edges"]
    assert ratio > 0.9


def test_it_checks_its_own_output(factory):
    """**=> AND A VAGUE OUTPUT IS CAUGHT ✓✓."""
    result = factory.walk(
        "ideation",
        "I think this is a good idea and we should build it.",
        skills=["validation-pack"],
    )
    assert "validation-pack" in result["failed"]


def test_the_gate_sends_it_backwards(factory):
    """
    **=> THE PEER'S RULE ✓✓ — **=> "THE LOOP SHOULD GO BACK THE START" ✓✓.**
    """
    result = factory.walk(
        "ideation", validation_pack(["Good"] * 6 + ["Critical"]), skills=["validation-pack"]
    )
    assert result["gate"]["verdict"] == "PAUSE"
    assert result["backward"] is True
    assert result["next_stage"] == "ideation"


def test_a_kill_stops(factory):
    """**=> AND A KILL GOES NOWHERE ✓✓ — **=> NOT FORWARDS ✓✓, **⇒ NOT
    BACKWARDS ✓✓."""
    result = factory.walk(
        "ideation",
        validation_pack(["Good"] * 5 + ["Critical"] * 2),
        skills=["validation-pack"],
    )
    assert result["gate"]["verdict"] == "KILL"
    assert result["stopped"] is True
    assert result["next_stage"] == ""


def test_the_circle_closes(factory):
    """**=> POST-LAUNCH GOES BACK TO **IDEATION** ✓✓ — **=> THE PEER'S EXACT
    WORDS ✓✓."""
    result = factory.walk(
        "post-launch", validation_pack(["Good"] * 7), skills=["validation-pack"]
    )
    assert result["next_stage"] == "ideation"


def test_the_agent_cannot_grade_itself(factory):
    """
    **=> THE POINT OF THE WHOLE FACTORY ✓✓.**

    **=> AND IT IS **MEASURED** ✓✓.**
    """
    result = factory.walk(
        "ideation",
        validation_pack(["Good"] * 6 + ["Critical"], stated="GO"),
        skills=["validation-pack"],
    )
    assert result["gate"]["stated"] == "GO"
    assert result["gate"]["verdict"] == "PAUSE"
    assert result["gate"]["agrees"] is False
