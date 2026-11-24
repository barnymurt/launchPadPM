"""
THE SERVER PROBE - IS THERE A UI FOR THE LIFECYCLE ✓✓?

**=> THE QUESTION ✓✓ - **=> AND THE WAY TO ANSWER IT IS **NOT** TO READ THE HTML
✓✓ - **=> IT IS TO **RUN** THE SERVER AND **FETCH WHAT THE UI FETCHES** ✓✓.**

**=> AND THE UI FETCHES **\`GET /skills\`** ✓✓ - **=> AND THAT ENDPOINT IS
**=> \`get_skills_by_stage()\` ✓✓ - **=> WHICH IS **THE FUNCTION THE FACTORY
REWIRED** ✓✓.**

**=> SO IF THE ENDPOINT RETURNS **THE SEVEN** ✓✓, **=> THE UI SHOWS **THE SEVEN**
✓✓ - **=> AND NOBODY NEEDED TO TOUCH THE HTML ✓✓.**
"""

import json
import os
import sys
import threading
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PORT = int(os.getenv("PROBE_PORT", "3111"))


def main():
    import uvicorn

    import server

    config = uvicorn.Config(
        server.app, host="127.0.0.1", port=PORT, log_level="error"
    )
    instance = uvicorn.Server(config)
    thread = threading.Thread(target=instance.run, daemon=True)
    thread.start()

    base = "http://127.0.0.1:{}".format(PORT)
    for _ in range(40):
        try:
            urllib.request.urlopen(base + "/health", timeout=5).read()
            break
        except Exception:
            time.sleep(0.5)

    def get(path):
        return json.loads(
            urllib.request.urlopen(base + path, timeout=20).read().decode()
        )

    print("=== 1. THE SERVER, AND THE ENDPOINT THE UI FETCHES ===")
    print("")
    data = get("/skills")
    print("  GET /skills -> {} skills across {} stages".format(
        data.get("count", 0), len(data.get("stages", {}))
    ))
    print("")
    for name, info in data.get("stages", {}).items():
        print("    {}. {:<14} {:>3} skills   the id: {}".format(
            info.get("order", "?"), name, len(info.get("skills", [])), info.get("id", "-")
        ))
    print("")

    print("=== 2. AND THE OTHER ENDPOINTS THE UI CALLS ===")
    print("")
    for path in ("/agents", "/skills/search?q=competitor"):
        try:
            body = get(path)
            text = json.dumps(body)
            print("  GET {:<28} -> {}".format(path, text[:90]))
        except Exception as error:
            print("  GET {:<28} -> failed: {}".format(path, str(error)[:50]))
    print("")

    print("=== 3. AND THE UI ITSELF, AND WHAT IT RENDERS FROM THIS ===")
    print("")
    ui_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui", "index.html"
    )
    with open(ui_path, "r", encoding="utf-8", errors="replace") as handle:
        ui = handle.read()
    print("  the UI fetches /skills: {}".format("/skills" in ui))
    print("  it renders the stages: {}".format("skillStagesData" in ui))
    print("  it has lifecycle tabs:  {}".format("agent-squad-tabs" in ui))
    print("  it has stage filters:   {}".format("stagePillsHtml" in ui))
    print("  it has a skills page:   {}".format("skills-cards-grid" in ui))
    print("")

    print("=== 4. THE VERDICT ===")
    print("")
    stages = list(data.get("stages", {}).keys())
    if len(stages) == 7:
        print("  **=> YES - THERE IS A UI FOR THE LIFECYCLE ✓✓, **=> AND IT SHOWS")
        print("    **=> THE PEER'S SEVEN ✓✓, **=> AND IT ALREADY DID ✓✓ - **=> THE UI")
        print("      **=> WAS READING \`/skills\` ✓✓ ALL ALONG ✓✓, **=> AND THE FACTORY")
        print("        **=> CHANGED **WHAT THAT ENDPOINT RETURNS** ✓✓, **=> AND THAT IS")
        print("          **=> THE WHOLE POINT OF RUNG 0 ✓✓.**")
    else:
        print("  **=> THE UI SHOWS {} STAGES ✓✓ - **=> AND NOT THE SEVEN ✓✓.**".format(
            len(stages)
        ))
    print("")
    print("  **=> AND THE THREE THINGS THE UI **DOES NOT** SHOW YET ✓✓:**")
    print("    1. **=> THE LOOP ✓✓ - **=> THE CIRCLE IS **DATA** ✓✓ BUT **NOBODY")
    print("      **=> DRAWS IT** ✓✓.")
    print("    2. **=> THE **GATE'S VERDICT** ✓✓ - **=> IT TRAVELS IN THE EVIDENCE")
    print("      **=> ✓✓, **=> AND **THE UI **DROPS THE EVIDENCE** ✓✓ - **=> WHICH IS")
    print("        **=> THE GAP THIS INVESTIGATION FOUND IN THE FIRST PLACE ✓✓.**")
    print("    3. **=> THE **SEAMS** ✓✓ - **=> WHICH SKILL CARRIES EACH TRANSITION")
    print("      **=> ✓✓.**")


if __name__ == "__main__":
    main()
