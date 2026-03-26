"""
FastAPI server for local staging/live environments.
"""

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


@app.get("/keys/status")
def key_status() -> Dict[str, bool]:
    return {
        "openai": bool(_session_keys.get("openai") or os.getenv("OPENAI_API_KEY")),
        "anthropic": bool(_session_keys.get("anthropic") or os.getenv("ANTHROPIC_API_KEY")),
        "perplexity": bool(_session_keys.get("perplexity") or os.getenv("PERPLEXITY_API_KEY")),
        "minimax": bool(_session_keys.get("minimax") or os.getenv("MINIMAX_API_KEY")),
    }


@app.post("/keys")
def set_keys(payload: KeyRequest) -> Dict[str, bool]:
    if payload.openai is not None:
        _session_keys["openai"] = payload.openai.strip()
    if payload.anthropic is not None:
        _session_keys["anthropic"] = payload.anthropic.strip()
    if payload.perplexity is not None:
        _session_keys["perplexity"] = payload.perplexity.strip()
    if payload.minimax is not None:
        _session_keys["minimax"] = payload.minimax.strip()

    return {
        "openai": bool(_session_keys.get("openai")),
        "anthropic": bool(_session_keys.get("anthropic")),
        "perplexity": bool(_session_keys.get("perplexity")),
        "minimax": bool(_session_keys.get("minimax")),
    }


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
    use_web: bool = False
    provider: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


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
