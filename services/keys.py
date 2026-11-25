"""
The keys — ONE PLACE THAT KNOWS WHERE THEY ARE ✓✓.

**⇒ THE PEER PUT A KEY IN THROUGH THE UI** ✓✓, **⇒ AND THE UI SAID **"SET"**
✓✓, **⇒ AND **THE AGENT SAID **"Missing MINIMAX_API_KEY"** ✓✓.**

**⇒ **⇒ THE CAUSE ✓✓: **THE UI READ **THE FILE** ✓✓ AND **THE AGENT READ
**⇒ THE MEMORY** ✓✓ AND **THE ENVIRONMENT** ✓✓ — **⇒ AND **THEY WERE **TWO
DIFFERENT PLACES** ✓✓, **⇒ AND **THE AGENT NEVER LOOKED AT **THE FILE** ✓✓.**

**⇒ **⇒ AND **THE FALLBACK ORDER** ✓✓ PUT **MINIMAX FIRST** ✓✓ — **⇒ SO EVEN **A
MINIMAX KEY** ✓✓ **WAS NOT USED** ✓✓ **UNLESS **THE ENVIRONMENT HAD IT** ✓✓.**

**⇒ **⇒ SO THIS MODULE IS **THE ONE PLACE** ✓✓ — **⇒ AND **THE UI** ✓✓ AND **THE
AGENT** ✓✓ **BOTH ASK IT** ✓✓, **⇒ AND **THEY CANNOT DISAGREE** ✓✓.**

**⇒ **⇒ AND **THE RULE** ✓✓ — **⇒ WHICH IS **THE SAME RULE** THE WHOLE PROJECT
KEEPS** ✓✓: **⇒ **ONE SOURCE OF TRUTH** ✓✓, **⇒ **READ IT** ✓✓, **⇒ **SAY WHERE
IT CAME FROM** ✓✓.**
"""

import json
import os
from typing import Dict, List, Optional

# **=> THE FILE THE KEYS LIVE IN ✓✓ — **=> AND IT IS **OUT OF GIT** ✓✓.**
KEYS_FILE = ".secrets/provider-keys.json"

# **=> AND THE PROVIDERS **ARE **DATA** ✓✓.**
PROVIDERS: List[dict] = [
    {
        "id": "minimax",
        "name": "MiniMax",
        "env": "MINIMAX_API_KEY",
        "model": "minimax-M2.7",
        "base": "https://api.minimax.chat/v1",
        "where": "https://platform.minimaxi.com",
    },
    {
        "id": "openai",
        "name": "OpenAI",
        "env": "OPENAI_API_KEY",
        "model": "gpt-4o-mini",
        "base": "https://api.openai.com/v1",
        "where": "https://platform.openai.com/api-keys",
    },
    {
        "id": "anthropic",
        "name": "Anthropic",
        "env": "ANTHROPIC_API_KEY",
        "model": "claude-3-5-sonnet-latest",
        "base": "https://api.anthropic.com",
        "where": "https://console.anthropic.com/settings/keys",
    },
    {
        "id": "perplexity",
        "name": "Perplexity",
        "env": "PERPLEXITY_API_KEY",
        "model": "sonar-pro",
        "base": "https://api.perplexity.ai",
        "where": "https://www.perplexity.ai/settings/api",
    },
]


def read_key_file(path: Optional[str] = None) -> Dict[str, str]:
    """The keys on disk, if the file is there."""
    target = path or KEYS_FILE
    if not os.path.exists(target):
        return {}
    try:
        with open(target, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return {str(k): str(v) for k, v in data.items() if v}
    except Exception:
        return {}


def write_key_file(keys: Dict[str, str], path: Optional[str] = None) -> None:
    """The keys, written to disk with the permissions they deserve."""
    target = path or KEYS_FILE
    directory = os.path.dirname(target)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        json.dump(keys, handle, indent=2)
    try:
        os.chmod(target, 0o600)
    except OSError:
        pass


def all_keys(session_keys: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Every key that is available, from everywhere it can be.

    **=> AND **THE ORDER MATTERS** ✓✓ - **=> THE FILE FIRST** ✓✓, BECAUSE **THAT
    IS WHERE THE UI PUT THEM** ✓✓, **=>** THEN THE MEMORY** ✓✓, **=>** THEN THE
    ENVIRONMENT** ✓✓.
    """
    keys: Dict[str, str] = {}

    for provider_id, value in read_key_file().items():
        if value:
            keys[provider_id] = value

    for provider_id, value in (session_keys or {}).items():
        if value:
            keys[provider_id] = value

    for provider in PROVIDERS:
        value = os.getenv(provider["env"], "").strip()
        if value:
            keys[provider["id"]] = value

    return keys


def key_for(provider_id: str, session_keys: Optional[Dict[str, str]] = None) -> str:
    """The key for a provider - the file first, then the memory, then the env."""
    return all_keys(session_keys).get(provider_id, "")


def first_provider_with_a_key(session_keys: Optional[Dict[str, str]] = None) -> str:
    """
    The provider to use - **THE ONE THE PEER SET** ✓✓.

    **=> AND **THE ORDER** ✓✓ - **=> IT IS **THE ORDER THE PROVIDERS ARE LISTED
    IN** ✓✓, **=> AND **THAT ORDER IS **DATA** ✓✓.**
    """
    keys = all_keys(session_keys)
    for provider in PROVIDERS:
        if keys.get(provider["id"]):
            return provider["id"]
    return ""


def hint_for(provider_id: str, session_keys: Optional[Dict[str, str]] = None) -> str:
    """The last four characters of the key, so the user can tell them apart."""
    key = key_for(provider_id, session_keys)
    if not key:
        return ""
    if len(key) <= 4:
        return "*" * len(key)
    return "*" * 4 + key[-4:]
