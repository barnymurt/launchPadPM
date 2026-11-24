"""
The factory's gate tests — RUNG 2 ✓✓.

**=> THE GATE MUST DECIDE **ARITHMETICALLY** ✓✓ — **=> AND EVERY THRESHOLD AND
EVERY RULE MUST COME FROM **THE DOCUMENT** ✓✓ — **=> AND THE AGENT MUST NOT BE
ABLE TO DECIDE ITS OWN VERDICT** ✓✓.**
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gate import compare, decide, read_gate

METRICS = [
    "Competitive density",
    "Differentiation gap",
    "TAM/SAM/SOM",
    "Unit economics health",
    "Assumption risk score",
    "MVP complexity",
    "Time to value",
]


def scorecard(ratings, stated=None):
    """A scorecard in the document's own shape."""
    lines = [
        "# Validation Pack: [Product Name]",
        "",
        "**Overall Recommendation:** {}".format(stated or "PLACEHOLDER"),
        "",
        "| # | Metric | Value | Rating | Source |",
        "|---|--------|-------|--------|--------|",
    ]
    for index, (metric, rating) in enumerate(zip(METRICS, ratings), start=1):
        lines.append("| {} | {} | [value] | {} | [source] |".format(index, metric, rating))
    lines.append("")
    lines.append("- Verdict: {}".format(stated or "PLACEHOLDER"))
    return "\n".join(lines)


@pytest.fixture(scope="module")
def gate():
    return read_gate()


def test_the_gate_reads_the_document(gate):
    """**=> EVERY THRESHOLD COMES FROM THE DOCUMENT ✓✓."""
    assert gate.loaded, "the gate read no thresholds and no rules"
    assert len(gate.thresholds) == 7
    assert len(gate.rules) == 3
    assert len(gate.expected_metrics) == 7


def test_the_counting_rules_are_the_documents_own(gate):
    """**=> AND THE RULES ARE **THE DOCUMENT'S WORDS** ✓✓."""
    assert "0 Critical" in gate.rules.get("GO", "")
    assert "2+ Critical" in gate.rules.get("KILL", "")
    assert "3+ Warning" in gate.rules.get("PAUSE", "")


def test_no_threshold_is_typed_in_python():
    """**=> THE RULE: **NO HARDCODED VALUES** ✓✓ — **=> SO A PYTHON FILE MAY NOT
    CONTAIN **THE DOCUMENT'S** THRESHOLDS ✓✓."""
    services = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "services"
    )
    for name in sorted(os.listdir(services)):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(services, name), "r", encoding="utf-8") as handle:
            code = handle.read()
        code = "\n".join(
            line
            for line in code.splitlines()
            if not line.strip().startswith("#") and not line.strip().startswith("*")
        )
        # **=> THE THRESHOLD VALUES **THAT ARE IN THE DOCUMENT** ✓✓ — **⇒ THEY MAY
        # **NOT** BE TYPED IN THE CODE ✓✓.**
        for value in ("1-3", "4-6", "7+", "1-2 gaps", "0 gaps"):
            assert value not in code, (
                "{} types the threshold {}".format(name, value)
                + " - it belongs in the document"
            )


def test_the_gate_counts_rather_than_chooses(gate):
    """**=> THE VERDICT FOLLOWS FROM THE COUNT ✓✓ — **=> AND EVERY CASE ✓✓."""
    assert decide(gate, scorecard(["Good"] * 7))["verdict"] == "GO"
    assert decide(gate, scorecard(["Good"] * 6 + ["Warning"]))["verdict"] == "GO"
    assert decide(gate, scorecard(["Good"] * 6 + ["Critical"]))["verdict"] == "PAUSE"
    assert decide(gate, scorecard(["Good"] * 5 + ["Critical"] * 2))["verdict"] == "KILL"
    assert decide(gate, scorecard(["Good"] * 4 + ["Warning"] * 3))["verdict"] == "PAUSE"


def test_the_agent_cannot_decide_its_own_verdict(gate):
    """
    **=> THE POINT OF THE WHOLE FACTORY ✓✓.**

    **=> AND IT IS **THE MEASUREMENT** OF IT ✓✓.**
    """
    dishonest = scorecard(["Good"] * 6 + ["Critical"], stated="GO")
    result = compare(gate, dishonest)
    assert result["stated"] == "GO"
    assert result["verdict"] == "PAUSE"
    assert result["agrees"] is False, (
        "the gate must disagree with an agent that rates one metric critical and "
        "then says GO"
    )

    honest = scorecard(["Good"] * 7, stated="GO")
    result = compare(gate, honest)
    assert result["agrees"] is True


def test_pause_is_the_backward_edge(gate):
    """
    **=> THE PEER'S CORRECTION ✓✓ — **=> "THE LOOP SHOULD GO BACK THE START" ✓✓.**

    **=> AND **PAUSE** IS **THE BACKWARD TRANSITION** ✓✓ — **=> AND IT IS **ONE OF
    **=> THE DOCUMENT'S OWN VERDICTS** ✓✓, **=> AND IT IS **COUNTED** ✓✓.**
    """
    assert "PAUSE" in gate.verdicts
    assert decide(gate, scorecard(["Good"] * 6 + ["Critical"]))["verdict"] == "PAUSE"
