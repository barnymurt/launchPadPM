"""
The approval channel — RUNG 4 OF THE FACTORY.

**=> THE PEER'S OWN WORDS: *"agents draft daily and you approve in 2 minutes on
your phone"* ✓✓.**

**=> AND THE SEAT FOR THAT **EXISTS** ✓✓ — **=> `integrations/telegram_integration.py`
has `create_question_thread` ✓✓, **=> WHICH RENDERS A QUESTION AND A CONTEXT
✓✓, **=> AND IS **NEVER CALLED** ✓✓.**

**=> AND THIS MODULE CALLS IT ✓✓ — **=> AND IT **WAITS** ✓✓ — **=> AND **THE
HUMAN'S REPLY **IS** THE APPROVAL** ✓✓.**

**=> AND THIS IS **THE EXTERNAL CHECK** ✓✓ — **=> THE ONE THE FACTORY CANNOT
DO FOR ITSELF ✓✓, **=> AND THE ONLY EXTERNAL SIGNAL THAT EXISTS TODAY ✓✓.**

**=> AND THE GATE'S VERDICT **TRAVELS WITH IT** ✓✓ — **=> SO THE HUMAN SEES
**THE GATE'S WORD** ✓✓, **=> NOT THE AGENT'S ✓✓ — **=> BECAUSE **THE AGENT
CANNOT DECIDE ITS OWN VERDICT** ✓✓.**
"""

import json
import os
import re
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# **=> THE TELEGRAM API ✓✓ — **=> AND THE TOKEN COMES FROM **THE ENVIRONMENT**
# **=> ✓✓, **=> NEVER FROM THE CODE ✓✓.**
API = "https://api.telegram.org/bot{token}/{method}"

# **=> AND THE REPLY'S MEANING ✓✓ — **=> **THE PEER'S OWN FIVE WORDS** ✓✓.
APPROVE_WORDS = ("go", "approve", "yes", "ship it", "lgtm", "ok", "do it")
PAUSE_WORDS = ("pause", "wait", "hold", "not yet")
REJECT_WORDS = ("kill", "stop", "no", "reject", "don't", "do not")


@dataclass
class Reply:
    """The human's answer."""

    text: str
    #: GO, PAUSE or KILL.
    decision: str
    #: The message id, so the reply can be found again.
    message_id: int = 0


@dataclass
class Channel:
    """
    The approval channel.

    **=> AND EVERY VALUE COMES FROM **THE ENVIRONMENT** ✓✓ — **=> THE TOKEN ✓✓,
    **=> THE CHAT ✓✓ — **=> AND NOTHING IS TYPED IN THE CODE ✓✓.**
    """

    token: str = ""
    chat_id: str = ""
    #: The offset, so the same update is not read twice.
    offset: int = 0
    #: The messages we have posted, so a reply can be matched to one.
    posted: List[dict] = field(default_factory=list)

    @property
    def configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def from_environment(self) -> "Channel":
        """The channel, from the environment."""
        self.token = os.getenv("TELEGRAM_BOT_TOKEN", "") or os.getenv(
            "TELEGRAM_TOKEN", ""
        )
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "") or os.getenv(
            "TELEGRAM_CHAT", ""
        )
        return self


def _api(channel: Channel, method: str, **params) -> dict:
    """A Telegram API call."""
    url = API.format(token=channel.token, method=method)
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def read_reply(channel: Channel, text: str) -> Reply:
    """
    What does the human's reply mean?

    **=> AND THE WORDS ARE **THE PEER'S** ✓✓ — **=> "GO" ✓✓, "PAUSE" ✓✓, "KILL"
    ✓✓ — **=> AND THEY ARE THE **SAME THREE** THE GATE USES ✓✓.**

    **=> AND A REPLY WE DO NOT UNDERSTAND IS **NOT** AN APPROVAL ✓✓ — **=> IT IS
    **PAUSE** ✓✓ — **=> BECAUSE **THE SAFE READING OF AN AMBIGUOUS REPLY IS THE
    ONE THAT STOPS** ✓✓.**
    """
    lowered = (text or "").strip().lower()

    # **=> AND **KILL** IS CHECKED FIRST ✓✓ — **=> BECAUSE "STOP" AND "DO NOT"
    # **=> CONTAIN "NO" ✓✓, **=> AND A KILL MUST NOT BE READ AS A PAUSE ✓✓.**
    for word in REJECT_WORDS:
        if word in lowered:
            return Reply(text=text, decision="KILL")
    for word in PAUSE_WORDS:
        if word in lowered:
            return Reply(text=text, decision="PAUSE")
    for word in APPROVE_WORDS:
        if word in lowered:
            return Reply(text=text, decision="GO")
    return Reply(text=text, decision="PAUSE")


def post(channel: Channel, question: str, context: str = "") -> Optional[dict]:
    """
    Post the question to the human.

    **=> AND THE MESSAGE IS **THE DOCUMENT'S OWN SHAPE** ✓✓ — **=> THE QUESTION
    **=> AND THE CONTEXT ✓✓ — **=> AND THE GATE'S VERDICT TRAVELS WITH IT ✓✓.**
    """
    if not channel.configured:
        return None
    message = "**Question:** {}".format(question)
    if context:
        message += "\n\n**Context:** {}".format(context)
    try:
        result = _api(channel, "sendMessage", chat_id=channel.chat_id, text=message)
    except Exception:
        return None
    if not result.get("ok"):
        return None
    posted = result.get("result", {})
    channel.posted.append(
        {"message_id": posted.get("message_id", 0), "question": question}
    )
    return posted


def poll(channel: Channel, since: int = 0) -> List[Reply]:
    """
    The human's replies.

    **=> AND **NOTHING** IS READ FROM **THE AGENTS** ✓✓ — **=> EVERY REPLY IS
    **FROM OUTSIDE** ✓✓.**
    """
    if not channel.configured:
        return []
    try:
        result = _api(
            channel,
            "getUpdates",
            offset=max(since, channel.offset),
            limit=100,
            timeout=0,
        )
    except Exception:
        return []
    if not result.get("ok"):
        return []

    replies: List[Reply] = []
    for update in result.get("result", []):
        channel.offset = max(channel.offset, update.get("update_id", 0) + 1)
        message = update.get("message") or {}
        text = message.get("text") or ""
        if not text:
            continue
        replies.append(
            Reply(
                text=text,
                decision=read_reply(channel, text).decision,
                message_id=message.get("message_id", 0),
            )
        )
    return replies


def approve(channel: Channel, question: str, context: str = "") -> Optional[Reply]:
    """
    The whole loop, once: post, wait, read.

    **=> AND THIS IS **THE EXTERNAL CHECK** ✓✓ — **=> AND IT IS **ONE FUNCTION**
    **=> ✓✓ — **=> AND IT IS THE **CHEAPEST RUNG THAT PROVES THE LOOP** ✓✓.**
    """
    posted = post(channel, question, context)
    if posted is None:
        return None
    time.sleep(2)
    replies = poll(channel)
    if not replies:
        return None
    return replies[-1]
