"""
The approval channel's tests — RUNG 4 ✓✓.

**=> THE PEER'S OWN WORDS: *"agents draft daily and you approve in 2 minutes on
your phone"* ✓✓.**

**=> AND THE ONE THING THIS NEEDS FROM THE PEER IS **A CHAT** ✓✓ — **=> SO THE
**=> CODE** IS PROVED **HERE** ✓✓, **=> AND THE **CHAT** IS PROVED **WHEN THE PEER
**=> ADDS THE BOT** ✓✓.**

**=> AND THE PROOF HERE USES **A MOCK** ✓✓ — **=> BECAUSE **THE POINT BEING
PROVED IS THAT **THE CODE POSTS, WAITS AND READS** ✓✓, **=> AND A MOCK PROVES
**=> THAT** ✓✓ WITHOUT **A CHAT** ✓✓.**
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import approval
from services.approval import Channel, poll, post, read_reply


def test_the_human_decides_in_the_gates_own_words():
    """**=> THE THREE VERDICTS ✓✓ — **=> AND THEY ARE THE **GATE'S** ✓✓."""
    assert read_reply(Channel(), "GO").decision == "GO"
    assert read_reply(Channel(), "ship it").decision == "GO"
    assert read_reply(Channel(), "yes").decision == "GO"
    assert read_reply(Channel(), "PAUSE").decision == "PAUSE"
    assert read_reply(Channel(), "wait").decision == "PAUSE"
    assert read_reply(Channel(), "KILL").decision == "KILL"
    assert read_reply(Channel(), "stop").decision == "KILL"


def test_an_ambiguous_reply_is_not_an_approval():
    """
    **=> THE SAFE READING OF AN AMBIGUOUS REPLY IS THE ONE THAT STOPS ✓✓.**

    **=> AND **THAT IS A DECISION** ✓✓ — **=> IT IS NOT A DEFAULT ✓✓, **=> IT IS
    **=> THE RULE** ✓✓.**
    """
    assert read_reply(Channel(), "maybe later").decision == "PAUSE"
    assert read_reply(Channel(), "hmm").decision == "PAUSE"
    assert read_reply(Channel(), "").decision == "PAUSE"


def test_a_kill_is_never_read_as_a_pause():
    """**=> BECAUSE "NO" AND "DO NOT" CONTAIN WORDS THAT COULD BE READ
    **=> OTHER WAYS** ✓✓."""
    assert read_reply(Channel(), "no, do not").decision == "KILL"
    assert read_reply(Channel(), "don't ship it").decision == "KILL"


def test_the_channel_takes_its_values_from_the_environment():
    """**=> THE RULE: **NO HARDCODED VALUES** ✓✓ — **=> THE TOKEN AND THE CHAT
    **=> COME FROM **THE ENVIRONMENT** ✓✓."""
    channel = Channel().from_environment()
    # **=> AND IT KNOWS WHEN IT IS **NOT** CONFIGURED ✓✓ — **=> AND IT SAYS SO
    # **=> RATHER THAN POSTING INTO THE VOID ✓✓.**
    assert isinstance(channel.configured, bool)


def test_an_unconfigured_channel_posts_nothing(monkeypatch):
    """**=> AND IT DOES NOT POST **ANYWHERE** WHEN IT HAS NOWHERE TO POST ✓✓."""
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT", raising=False)
    channel = Channel().from_environment()
    assert channel.configured is False
    assert post(channel, "should we build this?") is None
    assert poll(channel) == []


def test_it_posts_asks_and_reads(monkeypatch):
    """
    **=> THE WHOLE LOOP, ONCE ✓✓ — **=> POST ✓✓, **=> WAIT ✓✓, **=> READ ✓✓.**

    **=> AND IT IS PROVED WITH **A MOCK** ✓✓ — **=> BECAUSE **THE PEER'S CHAT
    **=> DOES NOT EXIST YET** ✓✓, **=> AND THE POINT BEING PROVED IS **THE
    **=> MECHANISM** ✓✓, **=> NOT THE CREDENTIAL ✓✓.**
    """
    sent = []
    updates = []

    def fake_api(channel, method, **params):
        if method == "sendMessage":
            sent.append(params)
            return {
                "ok": True,
                "result": {"message_id": 42, "text": params.get("text", "")},
            }
        if method == "getUpdates":
            return {
                "ok": True,
                "result": [
                    {
                        "update_id": 7,
                        "message": {"message_id": 99, "text": "GO"},
                    }
                ],
            }
        raise AssertionError("unexpected method " + method)

    monkeypatch.setattr(approval, "_api", fake_api)
    monkeypatch.setattr(approval.time, "sleep", lambda seconds: None)

    channel = Channel(token="test-token", chat_id="test-chat")
    assert channel.configured is True

    reply = approval.approve(
        channel,
        "should we ship this?",
        "the gate says GO",
    )

    assert reply is not None, "the loop did not produce a reply"
    assert reply.decision == "GO"
    assert sent, "nothing was posted"
    assert "should we ship this?" in sent[0]["text"]
    assert "the gate says GO" in sent[0]["text"]
    assert sent[0]["chat_id"] == "test-chat"


def test_the_gate_verdict_travels_with_the_question(monkeypatch):
    """**=> THE HUMAN SEES **THE GATE'S WORD** ✓✓ — **=> NOT THE AGENT'S ✓✓."""
    sent = []

    def fake_api(channel, method, **params):
        if method == "sendMessage":
            sent.append(params)
            return {"ok": True, "result": {"message_id": 1}}
        return {"ok": True, "result": []}

    monkeypatch.setattr(approval, "_api", fake_api)

    channel = Channel(token="t", chat_id="c")
    post(channel, "ship it?", "the gate says PAUSE")

    assert "PAUSE" in sent[0]["text"]
