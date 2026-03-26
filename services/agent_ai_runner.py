"""
AI-enabled agent runner with optional web search and skill context injection.
"""

import os
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional

from agents.base_agent import AgentResponse, BaseAgent
from integrations.ai_providers import call_anthropic, call_minimax, call_openai, call_perplexity
from integrations.web_search import search_duckduckgo

load_dotenv()

try:
    from services.skill_loader import get_relevant_skills, format_skills_for_prompt
    SKILLS_AVAILABLE = True
except Exception:
    SKILLS_AVAILABLE = False


def _build_system_prompt(agent: BaseAgent, web_results: Optional[List[Dict[str, Any]]]) -> str:
    prompt = [
        f"You are the {agent.role} agent named {agent.name}.",
        "Use the provided role knowledge and Scrum practices to answer.",
        "Be concise and actionable.",
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
    if provider:
        return provider
    if session_keys and session_keys.get("minimax"):
        return "minimax"
    if session_keys and session_keys.get("openai"):
        return "openai"
    if session_keys and session_keys.get("anthropic"):
        return "anthropic"
    if session_keys and session_keys.get("perplexity"):
        return "perplexity"
    if os.getenv("MINIMAX_API_KEY"):
        return "minimax"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("PERPLEXITY_API_KEY"):
        return "perplexity"
    return os.getenv("DEFAULT_AI_PROVIDER", "minimax")


def _call_provider(provider: str, messages: List[dict], session_keys: Optional[Dict[str, str]]) -> str:
    provider_key = provider.lower()
    if provider_key == "minimax":
        return call_minimax(messages, api_key=(session_keys or {}).get("minimax"))
    if provider_key == "openai":
        return call_openai(messages, api_key=(session_keys or {}).get("openai"))
    if provider_key == "anthropic":
        return call_anthropic(messages, api_key=(session_keys or {}).get("anthropic"))
    if provider_key == "perplexity":
        return call_perplexity(messages, api_key=(session_keys or {}).get("perplexity"))
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
            from services.skill_loader import get_skill
            for skill_name in specific_skills:
                skill = get_skill(skill_name)
                if skill:
                    skill_context += f"\n\n## {skill.name.replace('-', ' ').title()}\n{skill.description}\n"
                    skill_context += f"Key steps: {', '.join(skill.workflow_steps[:5]) if skill.workflow_steps else 'See skill details'}\n"
                    skill_names.append(skill.name)
        else:
            relevant_skills = get_relevant_skills(query, top_k=3)  # type: ignore
            if relevant_skills:
                skill_context = format_skills_for_prompt(relevant_skills)  # type: ignore
                skill_names = [s.name for s in relevant_skills]

    messages = [
        {"role": "system", "content": _build_system_prompt(agent, web_results)},
        {"role": "user", "content": _build_user_prompt(agent, query, web_results, skill_context)},
    ]

    response_text = _call_provider(selected_provider, messages, session_keys)
    evidence: Dict[str, Any] = {
        "provider": selected_provider,
        "web_results": web_results,
        "skills_used": skill_names,
    }

    return agent.format_response(
        response_text=response_text,
        recommendations=[],
        questions=[],
        requires_collaboration=False,
        collaborating_roles=[],
        evidence=evidence,
    )
