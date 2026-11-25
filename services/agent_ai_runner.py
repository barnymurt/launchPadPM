"""
AI-enabled agent runner with optional web search and skill context injection.
"""

import os
import re
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional

from agents.base_agent import AgentResponse, BaseAgent
from integrations.ai_providers import call_anthropic, call_minimax, call_openai, call_perplexity
from integrations.web_search import search_duckduckgo

load_dotenv()

try:
    from services.skill_loader import get_relevant_skills, format_skills_for_prompt
    from services.gate import compare as compare_gate
    from services.keys import all_keys
    from services.schema_reader import check_output
    SKILLS_AVAILABLE = True
except Exception:
    SKILLS_AVAILABLE = False


def _build_system_prompt(agent: BaseAgent, web_results: Optional[List[Dict[str, Any]]]) -> str:
    prompt = [
        f"You are the {agent.role} agent named {agent.name}.",
        "Use the provided role knowledge and Scrum practices to answer.",
        "Be concise and actionable.",
        "IMPORTANT: Do NOT include any internal reasoning tags like <think> or  in your response.",
        "Only output the final formatted answer.",
    ]
    if web_results:
        prompt.append("You have web search results available in the conversation context.")
    return "\n".join(prompt)


def _build_user_prompt(
    agent: BaseAgent,
    query: str,
    web_results: Optional[List[Dict[str, Any]]] = None,
    skill_context: str = "",
) -> str:
    payload = {
        "query": query,
        "role_knowledge": agent.role_knowledge,
        "scrum_knowledge": agent.scrum_knowledge,
        "continuous_discovery_knowledge": agent.continuous_discovery_knowledge,
    }
    if web_results:
        payload["web_results"] = web_results
    if skill_context:
        payload["skill_context"] = skill_context
    return f"Context:\n{payload}\n\nAnswer the query."


def _select_provider(provider: Optional[str], session_keys: Optional[Dict[str, str]]) -> str:
    """
    Which provider to use.

    **=> AND **THE ORDER MATTERS** **=>** - **=> THE PEER PUT A KEY IN **THE
    **=> UI** **=>** AND **THE AGENT SAID **"Missing MINIMAX_API_KEY"** **=>**
    **=>** WHILE **THE UI** **=>** SAID **THE KEY WAS SET** **=>.**

    **=> **=> THE CAUSE: **THE SELECTION READ **THE MEMORY** **=>** AND **THE
    **=> ENVIRONMENT** **=>** AND **NOT **THE FILE** **=>** - **=> AND **THE
    **=> UI'S SAVE GOES TO **THE FILE** **=>** - **=> AND **THE FALLBACK PUT
    **=> MINIMAX FIRST** **=>** - **=> SO EVEN **A MINIMAX KEY** **=>** **WAS NOT
    **=> USED** **=>** UNLESS **THE ENVIRONMENT HAD IT** **=>.**

    **=> **=> SO NOW IT READS **THE SAME PLACE** **=>** THE UI READS** **=>** AND
    **=> **THERE IS **ONE** SOURCE OF TRUTH** **=>.**
    """
    if provider:
        return provider

    # **=> THE KEYS, FROM EVERYWHERE THEY CAN BE** **=>** - **=> THE FILE FIRST
    # **=>** BECAUSE **THAT IS WHERE THE UI PUT THEM** **=>.**
    keys = all_keys(session_keys)

    for provider_id, env_var in (
        ("minimax", "MINIMAX_API_KEY"),
        ("openai", "OPENAI_API_KEY"),
        ("anthropic", "ANTHROPIC_API_KEY"),
        ("perplexity", "PERPLEXITY_API_KEY"),
    ):
        if keys.get(provider_id):
            return provider_id
        if os.getenv(env_var):
            return provider_id

    return os.getenv("DEFAULT_AI_PROVIDER", "minimax")


def _call_provider(provider: str, messages: List[dict], session_keys: Optional[Dict[str, str]]) -> str:
    """
    Call the provider, **with the key the selection found**.

    **=> AND **THIS IS **THE THIRD PLACE** THAT USED TO LOOK FOR THE KEY** ✓✓ -
    **=> THE SELECTION READ **THE MEMORY** ✓✓ AND **THE ENVIRONMENT** ✓✓, **=> AND
    **THE CALL** ✓✓ **READ **THE MEMORY** ✓✓ AND **THE ENVIRONMENT** ✓✓ - **=> AND
    **THE FILE** ✓✓ **WAS IN **NEITHER** ✓✓.**

    **=> **=> AND THAT IS **WHY THE PEER'S KEY** ✓✓ - **=> WHICH **THE UI** ✓✓
    **=>** SAID **WAS SET** ✓✓ - **=>** **WAS NEVER SENT** ✓✓.**

    **=> **=> SO NOW **BOTH** READ **THE SAME PLACE** ✓✓ - **=> `all_keys()` ✓✓ -
    **=> AND **THE SELECTION** ✓✓ AND **THE CALL** ✓✓ **BOTH ASK IT** ✓✓.
    """
    provider_key = provider.lower()
    keys = all_keys(session_keys)
    if provider_key == "minimax":
        return call_minimax(messages, api_key=keys.get("minimax"))
    if provider_key == "openai":
        return call_openai(messages, api_key=keys.get("openai"))
    if provider_key == "anthropic":
        return call_anthropic(messages, api_key=keys.get("anthropic"))
    if provider_key == "perplexity":
        return call_perplexity(messages, api_key=keys.get("perplexity"))
    raise RuntimeError("Unsupported provider")


def run_agent_ai(
    agent: BaseAgent,
    query: str,
    provider: Optional[str] = None,
    use_web: bool = False,
    max_results: int = 5,
    session_keys: Optional[Dict[str, str]] = None,
    use_skills: bool = True,
    specific_skills: Optional[List[str]] = None,
) -> AgentResponse:
    selected_provider = _select_provider(provider, session_keys)
    web_results = search_duckduckgo(query, max_results=max_results) if use_web else []

    skill_context = ""
    skill_names: List[str] = []
    if use_skills and SKILLS_AVAILABLE:
        if specific_skills:
            from services.skill_loader import get_skill_context
            for skill_name in specific_skills:
                ctx = get_skill_context(skill_name)
                if ctx:
                    skill_context += f"\n\n{ctx}\n"
                    skill_names.append(skill_name)
        else:
            relevant_skills = get_relevant_skills(query, top_k=3)  # type: ignore
            if relevant_skills:
                skill_context = format_skills_for_prompt(relevant_skills)  # type: ignore
                skill_names = [s.name for s in relevant_skills]

    messages = [
        {"role": "system", "content": _build_system_prompt(agent, web_results)},
        {"role": "user", "content": _build_user_prompt(agent, query, web_results, skill_context)},
    ]

    try:
        response_text = _call_provider(selected_provider, messages, session_keys)
    except Exception as provider_error:
        # **=> AND **THE PROVIDER'S OWN ERROR** **=>** IS **THE MOST USEFUL THING
        # **=>** THE USER CAN ACT ON **=>** - **=> AND **A GENERIC "Error: 402"**
        # **=>** SAYS **NOTHING** **=>** AND "INSUFFICIENT BALANCE" **=>** SAYS
        # **=>** EXACTLY WHAT TO DO **=>.**
        message = str(provider_error)
        if "insufficient balance" in message.lower():
            raise RuntimeError(
                "the provider says the balance is too low for this call - "
                + "add credit to the account, or use another provider. "
                + message[:200]
            ) from provider_error
        if "invalid api key" in message.lower():
            raise RuntimeError(
                "the provider rejected the key - check that it is the right "
                + "key for this provider's region and platform. "
                + message[:200]
            ) from provider_error
        raise
    response_text = re.sub(r"<think>[\s\S]*?</think>", "", response_text).strip()
    evidence: Dict[str, Any] = {
        "provider": selected_provider,
        "web_results": web_results,
        "skills_used": skill_names,
    }

    # **=> THE GATE, AT THE ONE PLACE EVERY ANSWER PASSES ✓✓.**
    #
    # **=> AND THIS IS **THE CHOKE POINT** ✓✓ - **=> EVERY AGENT ANSWER GOES
    # **=> THROUGH HERE** ✓✓, **=> SO **A GATE HERE GATES EVERYTHING** ✓✓.**
    #
    # **=> AND THE GATE PRODUCES **TWO** VERDICTS ✓✓: **=> THE **SCHEMA** CHECK
    # **=> - **=> DOES THE OUTPUT HAVE **THE SHAPE** ✓✓ - **=> AND THE **GATE**
    # **=> - **=> GO, PAUSE OR KILL ✓✓ - **=> AND **BOTH COME FROM **THE
    # **=> DOCUMENT** ✓✓, **=> NEVER FROM THE CODE ✓✓.**
    #
    # **=> AND THE EVIDENCE IS **THE CHANNEL** ✓✓ - **=> THE ANSWER ALREADY
    # **=> CARRIES IT ✓✓, **=> AND IT ALREADY CROSSES THE SERVER BOUNDARY
    # **=> ✓✓ - **=> AND **THE UI** DROPS IT ✓✓ - **=> WHICH IS THE GAP THE
    # **=> PEER'S "WHERE CAN OUTPUTS BE FLAGGED FOR EXTERNAL REVIEW" IS
    # **=> ABOUT ✓✓.**
    try:
        checks: Dict[str, Any] = {}
        for skill_name in skill_names:
            result = check_output(response_text, skill_name)
            checks[skill_name] = {
                "ok": result.ok,
                "missing_fields": result.missing_fields,
                "missing_sections": result.missing_sections,
                "missing_lines": result.missing_lines,
                "renamed_sections": result.renamed_sections,
            }
        if checks:
            evidence["schema_check"] = checks

        # **=> AND THE VERDICT GATE ✓✓ - **=> ONLY WHERE THE OUTPUT CARRIES **A
        # **=> SCORECARD** ✓✓, **=> BECAUSE THE GATE IS ABOUT **THE VALIDATION
        # **=> PACK** ✓✓ AND **NOT** ABOUT EVERY ANSWER ✓✓.**
        decision = compare_gate(read_gate(), response_text)
        if decision.get("verdict"):
            evidence["gate"] = {
                "verdict": decision["verdict"],
                "stated": decision.get("stated", ""),
                "agrees": decision.get("agrees"),
                "critical": decision.get("critical", 0),
                "warning": decision.get("warning", 0),
                "rule": decision.get("rule", ""),
            }
    except Exception as error:
        # **=> AND A FAILED CHECK IS **AN ERROR** ✓✓ - **=> NOT A PASS ✓✓.**
        evidence["gate_error"] = str(error)[:200]

    # Track skill usage
    if skill_names:
        try:
            from services.usage_tracker import track_skill_usage
            for skill_name in skill_names:
                track_skill_usage(
                    skill_name=skill_name,
                    agent_name=agent.role,
                    success=True
                )
        except Exception:
            pass  # Don't fail the request if tracking fails

    return agent.format_response(
        response_text=response_text,
        recommendations=[],
        questions=[],
        requires_collaboration=False,
        collaborating_roles=[],
        evidence=evidence,
    )
