"""
The UI's tests — THE CIRCLE AND THE GATE ✓✓.

**=> THE UI IS **ONE HTML FILE** ✓✓, **=> SO IT IS TESTED **BY READING IT** ✓✓ —
**=> AND BY **THE SERVER** ✓✓, **=> WHICH IS **WHAT ACTUALLY SERVES IT** ✓✓.**
"""

import json
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI = os.path.join(ROOT, "ui", "index.html")


@pytest.fixture(scope="module")
def ui():
    with open(UI, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def test_the_lifecycle_page_exists(ui):
    """**=> THE CIRCLE HAS A PAGE ✓✓."""
    assert 'id="page-lifecycle"' in ui
    assert 'data-page="lifecycle"' in ui


def test_the_page_is_in_the_navigation(ui):
    """**=> AND IT IS **REACHABLE** ✓✓ — **=> A PAGE NOBODY CAN GET TO IS NOT A
    PAGE ✓✓."""
    assert re.search(r'data-page="lifecycle"', ui)


def test_the_ui_reads_the_stages_from_the_server(ui):
    """**=> AND **NOT** FROM A HARD-CODED LIST ✓✓ — **=> THE WHOLE POINT ✓✓."""
    assert "loadLifecycle" in ui
    assert "/lifecycle" in ui
    assert "/gate" in ui
    # **=> AND **NO STAGE NAME IS TYPED IN THE UI** ✓✓ — **=> THE STAGES COME FROM
    # **=> THE DATA** ✓✓.
    for stage in ("ideation", "post-launch"):
        assert stage not in ui, (
            "the stage name {} is typed in the UI - it belongs in the data".format(
                stage
            )
        )


def test_the_evidence_is_no_longer_dropped(ui):
    """
    **=> THE PEER'S ORIGINAL QUESTION ✓✓ — *"WHERE CAN OUTPUTS BE FLAGGED FOR
    EXTERNAL REVIEW"* ✓✓ — **=> AND THE ANSWER IS **THIS LINE** ✓✓.**
    """
    assert "renderAnswerVerdict(data)" in ui
    # **=> AND **THE OLD LINE — **WHICH DROPPED THE EVIDENCE** ✓✓ — IS GONE ✓✓.
    assert (
        "innerHTML = formatAIResponse(data.response || 'No response');" not in ui
    ), "the evidence is dropped again"


def test_the_gate_verdict_is_shown_with_its_rule(ui):
    """**=> AND THE HUMAN SEES **THE GATE'S WORD** ✓✓ — **=> NOT THE AGENT'S
    ✓✓."""
    assert "the gate says" in ui
    assert "verdict-rule" in ui
    assert "the agent said" in ui


def test_the_hardcoded_port_is_gone(ui):
    """
    **=> THE SAME DEFECT AS THE MAGIC EQUITY ✓✓ — **=> A HARDCODED VALUE IN THE
    CODE ✓✓.**

    **=> AND IT WAS **A REAL BUG** ✓✓: **=> THE UI NAMED **PORT 3000** ✓✓, **=> AND
    **=> THE SERVER'S OWN PORTS** ✓✓ ARE **8000** ✓✓ AND **8001** ✓✓ — **=> SO **THE
    **=> UI'S FETCHES WERE **GOING TO A PORT NOTHING SERVED** ✓✓.**
    """
    assert "localhost:3000" not in ui
    assert "const API_BASE = '';" in ui, (
        "the API base must be relative, so it works on any port and any host - "
        "including the peer's phone"
    )


def test_the_javascript_balances(ui):
    """**=> AND THE JAVASCRIPT IS **NOT** BROKEN ✓✓ — **=> A SYNTAX ERROR IN ONE
    BLOCK **BREAKS THE WHOLE PAGE** ✓✓."""
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", ui, re.S)
    assert scripts
    js = "\n".join(scripts)
    for opener, closer in (("{", "}"), ("(", ")"), ("[", "]")):
        assert js.count(opener) == js.count(closer), (
            "the javascript has unbalanced {} () []"
        )


def test_the_server_serves_the_endpoints_the_ui_calls():
    """**=> AND THE ENDPOINTS **EXIST** ✓✓ — **=> THE UI CALLS **\`/lifecycle\`** ✓✓
    AND **\`/gate\`** ✓✓."""
    with open(os.path.join(ROOT, "server.py"), "r", encoding="utf-8") as handle:
        server = handle.read()
    assert '@app.get("/lifecycle")' in server
    assert '@app.get("/gate")' in server
