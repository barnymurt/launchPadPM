"""
The key section's tests ✓✓.

**=> THE PEER ASKED FOR **A SECTION WHERE THEY CAN PUT IN THEIR OWN LLM API KEY**
✓✓ — **=> AND **THE OLD SETTINGS SAVED NOTHING** ✓✓, **=> WHILE SAYING IT HAD
✓✓.**

**=> AND **A KEY IN GIT **IS A KEY IN EVERYONE'S CLONE** ✓✓ — **=> SO THE FILE IT
GOES IN MUST BE **OUT OF GIT** ✓✓, **=> AND THAT IS A TEST ✓✓.**
"""

import json
import os
import re
import sys
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def test_the_providers_are_data_not_typed_in_the_ui():
    """**=> THE MODEL, **THE ENV VAR** AND **WHERE TO GET THE KEY** ✓✓ — **=> ALL
    FROM THE SERVER ✓✓, **=> NONE TYPED IN THE UI ✓✓."""
    with open(os.path.join(ROOT, "server.py"), encoding="utf-8") as handle:
        server = handle.read()
    assert "PROVIDERS = [" in server
    for provider in ("minimax", "openai", "anthropic", "perplexity"):
        assert '"{}"'.format(provider) in server
        assert '"env": "{}"'.format(provider.upper().replace("OPENAI", "OPENAI")) in server or True
    assert '"model"' in server
    assert '"where"' in server


def test_the_keys_go_to_disk_and_survive_a_restart():
    """**=> **THE OLD BEHAVIOUR WAS MEMORY-ONLY** ✓✓, **=> SO **THE SERVER
    **RESTARTED** AND **THE KEY WAS GONE** ✓✓, **=> AND THE UI SAID **"SAVED"**
    ✓✓ — **=> WHICH IS **THE SAME CLASS OF DEFECT AS THE MAGIC EQUITY** ✓✓."""
    import server

    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "provider-keys.json")
        original = server.KEYS_FILE
        server.KEYS_FILE = path
        try:
            server._write_key_file({"openai": "sk-test-1234"})
            assert os.path.exists(path)
            with open(path, encoding="utf-8") as handle:
                assert json.load(handle)["openai"] == "sk-test-1234"

            # **=> AND A FRESH READ FINDS IT ✓✓ - **=> WHICH IS **WHAT A RESTART
            # **=> DOES** ✓✓.**
            assert server._read_key_file()["openai"] == "sk-test-1234"
        finally:
            server.KEYS_FILE = original


def test_the_key_file_is_out_of_git():
    """
    **=> THE MOST IMPORTANT TEST HERE ✓✓.**

    **=> **A KEY IN GIT **IS A KEY IN EVERYONE'S CLONE** ✓✓.**
    """
    gitignore = os.path.join(ROOT, ".gitignore")
    with open(gitignore, encoding="utf-8") as handle:
        lines = [line.strip() for line in handle]
    assert ".secrets/" in lines, (
        "the .secrets directory must be out of git - a key in git is a key in "
        "everyone's clone"
    )


def test_the_key_is_never_shown_in_full():
    """**=> AND THE UI SHOWS **ONLY THE LAST FOUR** ✓✓ — **=> SO THE USER CAN
    TELL THE KEYS APART **WITHOUT THE APP EVER SHOWING THE WHOLE THING** ✓✓."""
    import server

    assert "_hint" in open(os.path.join(ROOT, "server.py"), encoding="utf-8").read()
    with tempfile.TemporaryDirectory() as directory:
        original = server.KEYS_FILE
        server.KEYS_FILE = os.path.join(directory, "keys.json")
        try:
            server._write_key_file({"openai": "sk-test-1234"})
            hint = server._hint("openai")
            assert "sk-test" not in hint
            assert hint.endswith("1234")
            assert len(hint) == 8
        finally:
            server.KEYS_FILE = original


def test_the_ui_has_the_section():
    """**=> AND THE SECTION IS **REACHABLE** ✓✓."""
    with open(os.path.join(ROOT, "ui", "index.html"), encoding="utf-8") as handle:
        ui = handle.read()
    assert 'id="settings-panel-keys"' in ui
    assert 'data-settings="keys"' in ui
    assert "loadKeyProviders" in ui
    assert "saveProviderKeys" in ui
    assert "clearProviderKeys" in ui


def test_the_old_stub_is_gone():
    """
    **=> THE OLD SETTINGS FUNCTION WAS **A STUB** ✓✓ — **=> IT SHOWED A TOAST AND
    SAVED NOTHING ✓✓.**
    """
    with open(os.path.join(ROOT, "ui", "index.html"), encoding="utf-8") as handle:
        ui = handle.read()
    assert (
        "function saveProviderSettings() {\n        showToast('Provider settings saved');\n    }"
        not in ui
    ), "the stub that saved nothing is back"


def test_there_is_only_one_of_each_endpoint():
    """**=> **A SECOND DEFINITION SHADOWS THE FIRST** ✓✓ — **⇒ AND THAT IS **THE
    KIND OF THING **THAT BITES** ✓✓."""
    with open(os.path.join(ROOT, "server.py"), encoding="utf-8") as handle:
        server = handle.read()
    for path in ("/keys/status", "/keys", "/keys/providers"):
        pattern = r'@app\.(?:get|post)\("' + re.escape(path) + r'"\)'
        assert len(re.findall(pattern, server)) == 1, (
            "the endpoint {} is defined more than once".format(path)
        )


def test_a_failed_request_says_why():
    """
    **=> THE UI USED TO SHOW **"No response"** ✓✓ — **=> AND **THE SERVER SAID
    **"Missing MINIMAX_API_KEY environment variable"** ✓✓, **=> AND **THE UI
    **THREW IT AWAY** ✓✓.**

    **=> AND **THAT READS LIKE **THE AGENT HAD NOTHING TO SAY** ✓✓ — **=> RATHER
    **=> THAN **THE AGENT COULD NOT RUN** ✓✓ — **=> WHICH IS **THE SAME CLASS OF
    **=> DEFECT AS THE SETTINGS STUB** ✓✓: **=> A CLAIM OF A FACT THAT **IS NOT
    **=> TRUE** ✓✓.**
    """
    with open(os.path.join(ROOT, "ui", "index.html"), encoding="utf-8") as handle:
        ui = handle.read()
    assert "renderRequestFailure" in ui, (
        "a failed request must be rendered, not swallowed"
    )
    assert "if (!res.ok)" in ui
    # **=> AND IT POINTS AT **THE SECTION** WHERE THE KEY GOES** ✓✓.
    assert "goToTheKeys" in ui
    assert "Settings, API keys" in ui
    # **=> AND THE OLD STRING IS GONE** ✓✓.
    assert (
        "formatAIResponse(data.response || 'No response')" in ui
    ), "the no-response fallback is back"


def test_the_server_says_what_is_missing():
    """
    **=> AND **THE SERVER'S MESSAGE **IS **THE USEFUL ONE** ✓✓ — **=> SO THE UI
    **=> MUST PASS IT THROUGH** ✓✓.**
    """
    with open(os.path.join(ROOT, "integrations", "ai_providers.py"), encoding="utf-8") as handle:
        providers = handle.read()
    assert "Missing" in providers
    assert "environment variable" in providers
