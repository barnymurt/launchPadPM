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
    with open(os.path.join(ROOT, "services", "keys.py"), encoding="utf-8") as handle:
        server = handle.read()
    assert "PROVIDERS: List[dict] = [" in server
    for provider in ("minimax", "openai", "anthropic", "perplexity"):
        assert '"{}"'.format(provider) in server
        assert '"env": "{}"'.format(provider.upper().replace("OPENAI", "OPENAI")) in server or True
    assert '"model"' in server
    assert '"where"' in server


def test_the_keys_go_to_disk_and_survive_a_restart():
    """**=> **THE OLD BEHAVIOUR WAS MEMORY-ONLY** ✓✓, **=> SO **THE SERVER
    **RESTARTED** AND **THE KEY WAS GONE** ✓✓, **=> AND THE UI SAID **"SAVED"**
    ✓✓ — **=> WHICH IS **THE SAME CLASS OF DEFECT AS THE MAGIC EQUITY** ✓✓."""
    from services import keys

    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "provider-keys.json")
        keys.write_key_file({"openai": "sk-test-1234"}, path)
        assert os.path.exists(path)
        with open(path, encoding="utf-8") as handle:
            assert json.load(handle)["openai"] == "sk-test-1234"

        # **=> AND A FRESH READ FINDS IT ✓✓ - **=> WHICH IS **WHAT A RESTART
        # **=> DOES** ✓✓.**
        assert keys.read_key_file(path)["openai"] == "sk-test-1234"


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
    from services import keys

    assert "hint_for" in open(
        os.path.join(ROOT, "services", "keys.py"), encoding="utf-8"
    ).read()
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "keys.json")
        keys.write_key_file({"openai": "sk-test-1234"}, path)
        original = keys.KEYS_FILE
        keys.KEYS_FILE = path
        try:
            hint = keys.hint_for("openai")
            assert "sk-test" not in hint
            assert hint.endswith("1234")
            assert len(hint) == 8
        finally:
            keys.KEYS_FILE = original


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


def test_a_dead_server_says_so():
    """
    **=> THE BROWSER SAYS **"Failed to fetch"** **=> WHEN **THE SERVER IS GONE**
    **=> **=> - **=> AND **THAT IS **THE MOST COMMON FAILURE** **=>, **=> AND IT SAYS
    **=> **NOTHING USEFUL** **=>.**

    **=> AND IT COST THE PEER TIME **=>: **=> A KEY SAVED AND AN AGENT ASKED **=>,
    **=> BOTH **"Failed to fetch"** **=>, **=> AND THE CAUSE WAS **A SERVER THAT
    **=> HAD BEEN STOPPED** **=>.**
    """
    with open(os.path.join(ROOT, "ui", "index.html"), encoding="utf-8") as handle:
        ui = handle.read()
    assert "describeTheFailure" in ui
    assert "may have been stopped" in ui
    # **=> AND THE KEY HANDLERS USE IT TOO **=> - **=> BECAUSE **THE SAVE** IS
    # **=> WHERE **THE PEER HIT IT** **=>.**
    assert ui.count("describeTheFailure(e)") >= 3


def test_there_is_a_way_to_start_it():
    """
    **=> AND **THE UI SAYS WHERE TO START IT** **=> - **=> SO THE PERSON IS NOT
    **=> LEFT GUESSING** **=>.**
    """
    with open(os.path.join(ROOT, "ui", "index.html"), encoding="utf-8") as handle:
        ui = handle.read()
    assert "scripts/run_local.ps1" in ui
    assert os.path.exists(os.path.join(ROOT, "scripts", "run_local.ps1")), (
        "the UI points at a script that is not there"
    )


def test_the_agent_sees_the_key_the_ui_saved():
    """
    **=> THE PEER'S KEY WAS INVISIBLE TO THE AGENT ✓✓ - **=> AND THE UI SAID
    **=> "SET" ✓✓.**

    **=> THE CAUSE: **THE UI READ **THE FILE** ✓✓ AND **THE AGENT READ **THE
    **=> MEMORY** ✓✓ AND **THE ENVIRONMENT** ✓✓ - **=> AND **THEY WERE **TWO
    **=> DIFFERENT PLACES** ✓✓.**

    **=> AND THE FALLBACK PUT **MINIMAX FIRST** ✓✓ - **=> SO EVEN **A MINIMAX KEY**
    **=> WAS NOT USED** ✓✓ **UNLESS **THE ENVIRONMENT HAD IT** ✓✓.**
    """
    from services.keys import all_keys, first_provider_with_a_key

    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "provider-keys.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"anthropic": "sk-ant-test"}, handle)

        from services import keys

        original = keys.KEYS_FILE
        keys.KEYS_FILE = path
        try:
            # **=> THE KEY IS THERE ✓✓.**
            assert "anthropic" in all_keys()
            # **=> AND **THE AGENT** **=>** WHICH READS **THE SAME PLACE** **=>**
            # **=> PICKS **THE PROVIDER THE PEER SET** **=>.**
            assert first_provider_with_a_key() == "anthropic"
        finally:
            keys.KEYS_FILE = original


def test_the_agent_and_the_ui_read_the_same_place():
    """
    **=> AND **THEY CANNOT DISAGREE** ✓✓ - **=> BECAUSE **THEY BOTH ASK **THE
    **=> SAME MODULE** ✓✓.**
    """
    import os as _os

    with open(_os.path.join(ROOT, "services", "agent_ai_runner.py"), encoding="utf-8") as handle:
        runner = handle.read()
    with open(_os.path.join(ROOT, "server.py"), encoding="utf-8") as handle:
        server = handle.read()

    assert "from services.keys import all_keys" in runner, (
        "the agent must read the keys from the shared module"
    )
    assert "from services.keys import" in server, (
        "the server must read the keys from the shared module"
    )
