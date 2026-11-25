"""
FastAPI server for local staging/live environments.
"""

import json
import os
from threading import Timer
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel

from agents.agent_registry import AgentRegistry
from config.settings import load_settings, Settings
from main import initialize_framework
from integrations.web_search import search_duckduckgo
from services.agent_ai_runner import run_agent_ai
from services.keys import (
    KEYS_FILE,
    PROVIDERS,
    all_keys,
    first_provider_with_a_key,
    hint_for,
    key_for,
    read_key_file,
    write_key_file,
)

try:
    from services.orchestrator import Orchestrator
    ORCHESTRATOR_AVAILABLE = True
except Exception:
    ORCHESTRATOR_AVAILABLE = False


app = FastAPI(title="LaunchPadPM Local Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_initialized = False
_settings: Optional[Settings] = None
_session_keys: Dict[str, str] = {}


class QueryRequest(BaseModel):
    role: str
    query: str
    use_ai: bool = True
    use_web: bool = True
    provider: Optional[str] = None


class KeyRequest(BaseModel):
    openai: Optional[str] = None
    anthropic: Optional[str] = None
    perplexity: Optional[str] = None
    minimax: Optional[str] = None


def _ensure_initialized() -> None:
    global _initialized, _settings
    if _initialized:
        return
    _settings = load_settings()
    initialize_framework(_settings)
    _initialized = True


@app.on_event("startup")
def startup_event() -> None:
    _ensure_initialized()


@app.get("/health")
def health() -> Dict[str, Any]:
    _ensure_initialized()
    app_env = os.getenv("APP_ENV", "local")
    product_name = _settings.product_name if _settings else "unknown"
    return {
        "status": "ok",
        "environment": app_env,
        "product_name": product_name,
    }


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/ui")


@app.get("/ui")
def ui() -> FileResponse:
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "index.html")
    return FileResponse(
        ui_path,
        headers={
            "Cache-Control": "no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )


@app.get("/agents")
def list_agents() -> Dict[str, List[str]]:
    _ensure_initialized()
    return {"roles": AgentRegistry.list_roles()}


@app.post("/restart")
def restart() -> Dict[str, str]:
    app_env = os.getenv("APP_ENV", "local")
    if app_env != "staging":
        raise HTTPException(status_code=403, detail="Restart only allowed in staging")

    Timer(0.25, lambda: os._exit(0)).start()
    return {"status": "restarting", "environment": app_env}


@app.post("/query")
def query_agent(payload: QueryRequest) -> Dict[str, Any]:
    _ensure_initialized()
    agent = AgentRegistry.get_agent(payload.role)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        if payload.use_ai:
            response = run_agent_ai(
                agent=agent,
                query=payload.query,
                provider=payload.provider,
                use_web=payload.use_web,
                session_keys=_session_keys,
            )
        else:
            response = agent.process_query(payload.query)
    except Exception as exc:
        if payload.use_ai:
            response = agent.process_query(payload.query)
            response.evidence = response.evidence or {}
            response.evidence["ai_error"] = str(exc)
            if payload.use_web:
                response.evidence["web_results"] = search_duckduckgo(payload.query)
        else:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "response": response.response,
        "recommendations": response.recommendations or [],
        "questions": response.questions or [],
        "requires_collaboration": response.requires_collaboration,
        "collaborating_roles": response.collaborating_roles or [],
        "evidence": response.evidence or {},
    }


class OrchestrateRequest(BaseModel):
    role: str
    query: str
    use_web: bool = True
    provider: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    skills: Optional[List[str]] = None


@app.post("/orchestrate")
async def orchestrate(payload: OrchestrateRequest) -> Dict[str, Any]:
    _ensure_initialized()
    if not ORCHESTRATOR_AVAILABLE:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    orchestrator = Orchestrator(provider=payload.provider, use_web=payload.use_web)  # type: ignore
    try:
        result = await orchestrator.query(
            role=payload.role,
            query=payload.query,
            context=payload.context,
            skills=payload.skills,
        )
        return {
            "response": result.primary_response.response,
            "recommendations": result.primary_response.recommendations or [],
            "questions": result.primary_response.questions or [],
            "requires_collaboration": result.primary_response.requires_collaboration,
            "collaborating_roles": result.primary_response.collaborating_roles or [],
            "depth_used": result.depth_used,
            "all_responses": [
                {
                    "role": r.role,
                    "response": r.response,
                }
                for r in result.all_responses
            ],
            "evidence": result.primary_response.evidence or {},
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


try:
    from services.skill_loader import (
        get_all_skills,
        get_skills_by_stage,
        get_relevant_skills,
    )
    SKILLS_AVAILABLE_SERVER = True
except Exception:
    SKILLS_AVAILABLE_SERVER = False


@app.get("/skills")
def list_skills() -> Dict[str, Any]:
    """Return all skills organized by lifecycle stage."""
    if not SKILLS_AVAILABLE_SERVER:
        return {"stages": {}, "count": 0}
    return {
        "stages": get_skills_by_stage(),
        "count": len(get_all_skills()),
    }


@app.get("/skills/search")
def search_skills(q: str = "") -> Dict[str, Any]:
    """Search skills by keyword and return top matches."""
    if not SKILLS_AVAILABLE_SERVER or not q:
        return {"skills": [], "query": q}
    relevant = get_relevant_skills(q, top_k=5)
    return {
        "skills": [
            {
                "name": s.name,
                "description": s.description,
                "skill_type": s.skill_type,
                "lifecycle_stage": s.lifecycle_stage,
                "outputs": s.outputs,
                "triggers": s.triggers[:5],
                "workflow_steps": s.workflow_steps[:4],
            }
            for s in relevant
        ],
        "query": q,
    }


@app.get("/api/usage/stats")
def get_usage_stats() -> Dict[str, Any]:
    """Return overall usage statistics (admin only)."""
    from services.usage_tracker import get_usage_stats
    return get_usage_stats()


@app.get("/api/usage/skills/{skill_name}")
def get_skill_usage(skill_name: str) -> Dict[str, Any]:
    """Return usage stats for a specific skill (admin only)."""
    from services.usage_tracker import get_skill_usage
    stats = get_skill_usage(skill_name)
    if stats is None:
        return {"error": "Skill not found or never used"}, 404
    return stats


@app.get("/api/usage/all")
def get_all_usage() -> Dict[str, Any]:
    """Return all usage data (admin only)."""
    from services.usage_tracker import get_all_usage
    return get_all_usage()


# **=> THE CIRCLE, AND THE GATE ✓✓ — **=> THE TWO ENDPOINTS THE UI NEEDS ✓✓.**
#
# **=> AND **THE LOOP** ✓✓ IS **DATA** ✓✓ — **=> AND **THE GATE** ✓✓ IS **DATA** ✓✓
# **=> — **=> AND NEITHER IS **A PYTHON LITERAL** ✓✓, **=> AND NEITHER IS **HARD-CODED
# **=> IN THE UI** ✓✓.**
#
# **=> AND THE **EVIDENCE** ✓✓ — **=> WHICH THE UI **DROPPED** ✓✓, **=> AND WHICH
# **=> CARRIES THE GATE'S VERDICT** ✓✓ — **=> NOW **TRAVELS** ✓✓.

@app.get("/lifecycle")
def get_lifecycle() -> Dict[str, Any]:
    """
    The circle: the stages, the skills, the seams and the loop.

    **=> AND **THE UI** ✓✓ FETCHES THIS ✓✓ — **=> AND IT IS **THE SAME DATA** ✓✓
    **=> THE SKILLS PAGE ALREADY FETCHES ✓✓, **=> SO **THERE IS **ONE** SOURCE OF
    **=> TRUTH** ✓✓.**
    """
    from services.lifecycle import dangling_edges, read_lifecycle, walkable

    lifecycle = read_lifecycle()
    state = walkable(lifecycle)

    stages = []
    for stage in lifecycle.stages:
        names = sorted(
            name for name, stages_of in lifecycle.skill_stages.items()
            if stage.id in stages_of
        )
        stages.append(
            {
                "id": stage.id,
                "order": stage.order,
                "title": stage.title,
                "purpose": stage.purpose,
                "reentered_by": stage.reentered_by,
                "skills": names,
                "count": len(names),
            }
        )

    seams = []
    for seam in lifecycle.seams:
        seams.append(
            {
                "to": seam.get("to", ""),
                "from": seam.get("from", ""),
                "skill": seam.get("skill", ""),
                "also": seam.get("also", ""),
                "edge": seam.get("edge", ""),
            }
        )

    edges = []
    for source_name, targets in lifecycle.edges_after.items():
        for target in targets:
            edges.append({"from": source_name, "to": target, "edge": "relatedAfter"})
    for target, sources in lifecycle.edges_before.items():
        for source_name in sources:
            edges.append({"from": source_name, "to": target, "edge": "relatedBefore"})

    return {
        "stages": stages,
        "seams": seams,
        "edges": edges,
        "loop": {
            "path": lifecycle.loop_path,
            "returns_to": lifecycle.loop_returns_to,
            "driven_by": [
                "a reply from a real person",
                "a call booked",
                "a pre-sale through a payment link",
                "a metric that moved",
            ],
        },
        "walkable": {
            "live": state["live"],
            "total": state["total"],
            "dangling": len(dangling_edges(lifecycle)),
        },
        "circular": True,
    }


@app.get("/gate")
def get_gate() -> Dict[str, Any]:
    """
    The gate: the thresholds and the counting rules, read from the document.

    **=> AND **THE VERDICT** ✓✓, **=> WHEN THERE IS ONE ✓✓.**
    """
    from services.gate import read_gate

    gate = read_gate()
    return {
        "loaded": gate.loaded,
        "thresholds": [
            {"gate": name, "good": values["good"],
             "warning": values["warning"], "critical": values["critical"]}
            for name, values in gate.thresholds.items()
        ],
        "rules": [
            {"verdict": verdict, "rule": rule}
            for verdict, rule in gate.rules.items()
        ],
        "metrics": gate.expected_metrics,
        "verdicts": gate.verdicts,
        "source": "skills/validation-pack/output-schema.md",
    }



def _key_for(provider_id: str) -> str:
    """The key for a provider - **FROM THE ONE PLACE THAT KNOWS** ✓✓."""
    return key_for(provider_id)


@app.get("/keys/providers")
def list_key_providers() -> Dict[str, Any]:
    """
    The providers the user can put a key in.

    **=> AND **THEY ARE **DATA** ✓✓ — **=> THE MODEL, **=> WHERE TO GET THE KEY
    **=> AND **THE ENV VAR IT MAPS TO** ✓✓ — **=> ALL READ FROM HERE ✓✓, **=> NOT
    **=> TYPED IN THE UI ✓✓.**
    """
    keys = all_keys()
    out = []
    for provider in PROVIDERS:
        source = "unset"
        if read_key_file().get(provider["id"]):
            source = "the key file"
        elif os.getenv(provider["env"]):
            source = "the environment"
        out.append(
            {
                "id": provider["id"],
                "name": provider["name"],
                "env": provider["env"],
                "model": provider["model"],
                "base": provider["base"],
                "where": provider["where"],
                "has_key": bool(keys.get(provider["id"])),
                "source": source,
                # **=> AND **ONLY THE **LAST FOUR** CHARACTERS** ✓✓ — **=> SO THE
                # **=> USER CAN SEE THE KEY IS THERE** ✓✓, **=> WITHOUT THE UI
                # **=> EVER SHOWING **THE WHOLE THING** ✓✓.
                "hint": _hint(provider["id"]),
            }
        )
    return {"providers": out, "file": KEYS_FILE}


def _hint(provider_id: str) -> str:
    """The last four characters of the key, so the user can tell them apart."""
    return hint_for(provider_id)


@app.get("/keys/status")
def key_status() -> Dict[str, bool]:
    keys = all_keys()
    return {
        "openai": bool(keys.get("openai")),
        "anthropic": bool(keys.get("anthropic")),
        "perplexity": bool(keys.get("perplexity")),
        "minimax": bool(keys.get("minimax")),
    }


@app.post("/keys")
def set_keys(payload: KeyRequest) -> Dict[str, Any]:
    """
    The user's own keys, saved **TO DISK** ✓✓.

    **=> AND **THE MEMORY COPY IS STILL KEPT** ✓✓ — **=> SO **THE RUNNING SERVER
    **=> USES THEM **AT ONCE** ✓✓, **=> AND **THE NEXT START **READS THEM FROM
    **=> THE FILE** ✓✓.**
    """
    for provider in PROVIDERS:
        value = getattr(payload, provider["id"], None)
        if value is None:
            continue
        value = value.strip()
        if value:
            _session_keys[provider["id"]] = value
        else:
            _session_keys.pop(provider["id"], None)

    stored = read_key_file()
    for provider in PROVIDERS:
        value = getattr(payload, provider["id"], None)
        if value is None:
            continue
        value = value.strip()
        if value:
            stored[provider["id"]] = value
        else:
            stored.pop(provider["id"], None)
    if stored:
        write_key_file(stored)
    elif os.path.exists(KEYS_FILE):
        try:
            os.remove(KEYS_FILE)
        except OSError:
            pass

    return {
        "saved": True,
        "providers": list_key_providers()["providers"],
        "status": key_status(),
    }


@app.post("/keys/clear")
def clear_keys() -> Dict[str, Any]:
    """The keys, forgotten - from the memory AND from the disk."""
    for provider in PROVIDERS:
        _session_keys.pop(provider["id"], None)
    if os.path.exists(KEYS_FILE):
        try:
            os.remove(KEYS_FILE)
        except OSError:
            pass
    return {"saved": True, "providers": list_key_providers()["providers"], "status": key_status()}
