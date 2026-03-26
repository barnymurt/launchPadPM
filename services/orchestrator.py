"""
Async Orchestrator for multi-agent collaboration.
Handles requires_collaboration + collaborating_roles from AgentResponse.
"""

import asyncio
from typing import Any, Dict, List, Optional

from dataclasses import dataclass

from agents.base_agent import AgentResponse, BaseAgent
from agents.agent_registry import AgentRegistry
from services.agent_ai_runner import run_agent_ai

MAX_DEPTH = 3


@dataclass
class OrchestrationResult:
    primary_response: AgentResponse
    all_responses: List[AgentResponse]
    depth_used: int


class Orchestrator:
    def __init__(self, provider: Optional[str] = None, use_web: bool = False):
        self.provider = provider
        self.use_web = use_web

    async def query(
        self,
        role: str,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        skills: Optional[List[str]] = None,
        depth: int = 0,
    ) -> OrchestrationResult:
        agent = AgentRegistry.get_agent(role)
        if not agent:
            raise ValueError(f"Agent '{role}' not found")

        primary_response = await self._run_agent(agent, query, context, skills=skills)
        all_responses = [primary_response]
        current_depth = depth

        if primary_response.requires_collaboration and current_depth < MAX_DEPTH:
            collab_tasks = []
            for collab_role in primary_response.collaborating_roles:
                collab_agent = AgentRegistry.get_agent(collab_role)
                if collab_agent:
                    collab_tasks.append(
                        self._run_agent(
                            collab_agent, query, context, skills=skills, parent_response=primary_response
                        )
                    )

            collab_responses = await asyncio.gather(*collab_tasks)
            all_responses.extend(collab_responses)
            current_depth += 1

            synthesis_query = self._build_synthesis_query(
                query, primary_response, collab_responses
            )
            primary_response = await self._run_agent(agent, synthesis_query, context, skills=skills)

        return OrchestrationResult(
            primary_response=primary_response,
            all_responses=all_responses,
            depth_used=current_depth,
        )

    async def _run_agent(
        self,
        agent: BaseAgent,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        skills: Optional[List[str]] = None,
        parent_response: Optional[AgentResponse] = None,
    ) -> AgentResponse:
        enriched_query = self._enrich_query(query, context, parent_response)
        return await asyncio.to_thread(
            run_agent_ai,
            agent,
            enriched_query,
            provider=self.provider,
            use_web=self.use_web,
            specific_skills=skills,
        )

    def _enrich_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]],
        parent_response: Optional[AgentResponse],
    ) -> str:
        if not context and not parent_response:
            return query

        parts = [query]
        if context:
            context_str = "\n".join(f"{k}: {v}" for k, v in context.items())
            parts.append(f"\n\nContext:\n{context_str}")
        if parent_response:
            parts.append(f"\n\nPrior analysis from {parent_response.role}:\n{parent_response.response}")

        return "".join(parts)

    def _build_synthesis_query(
        self,
        original: str,
        primary: AgentResponse,
        collab_responses: List[AgentResponse],
    ) -> str:
        collab_summary = "\n\n".join(
            f"[{r.role}]: {r.response}" for r in collab_responses
        )
        return (
            f"Original question: {original}\n\n"
            f"Your initial response:\n{primary.response}\n\n"
            f"Collaborating perspectives:\n{collab_summary}\n\n"
            f"Synthesize these perspectives into a coherent final answer that incorporates "
            f"all insights while maintaining your role as {primary.role}."
        )
