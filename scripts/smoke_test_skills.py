#!/usr/bin/env python3
"""
Automated smoke test for all skills.
Tests that each skill can be invoked via the API and returns a valid response.
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.skill_loader import get_all_skills
from services.agent_ai_runner import run_agent_ai
from agents.base_agent import AgentContext
from agents.agent_registry import AgentRegistry
from config.settings import load_settings


TEST_QUERIES = {
    "research": "Analyze the competitive landscape for a B2B SaaS project management tool. Identify 3-5 competitors and their key differentiators.",
    "design": "Design a user onboarding flow for a mobile-first note-taking app. Include key screens and user decision points.",
    "technical": "Design an API architecture for a real-time collaboration feature in a document editing app.",
    "strategy": "Develop a go-to-market strategy for a new AI-powered code review tool targeting enterprise teams.",
    "process": "Outline a sprint retrospective format for a team transitioning from waterfall to agile.",
    "default": "Explain the key considerations for implementing user authentication in a modern web application."
}

SKILL_CATEGORY_RESEARCH = [
    "analyze", "competitive", "market", "user", "journey", "persona", 
    "research", "survey", "interview", "feedback", "metrics", "cohort", "funnel",
    "analyst", "community", "heuristic", "gap", "usability", "accessibility",
    "benchmark", "landscape", "positioning"
]

SKILL_CATEGORY_DESIGN = [
    "design", "ui", "ux", "brand", "canvas", "wireframe", "visual",
    "animation", "motion", "theme", "color", "typography", "layout", "responsive",
    "pattern", "component", "system", "prototype", "mockup", "sketch"
]

SKILL_CATEGORY_TECHNICAL = [
    "architect", "technical", "api", "database", "schema", "security",
    "devops", "infrastructure", "cloud", "backend", "frontend", "serverless",
    "container", "kubernetes", "deployment", "pipeline", "monitoring", "performance",
    "migration", "backup", "recovery", "scale", "observability"
]

SKILL_CATEGORY_STRATEGY = [
    "strategy", "business", "roadmap", "planning", "go-to-market", "gtm",
    "launch", "messaging", "pricing", "channel", "partner", "sales", "acquisition",
    "retention", "referral", "growth", "market", "competitive", "okr", "kpi"
]

SKILL_CATEGORY_PROCESS = [
    "process", "scrum", "agile", "sprint", "retrospective", "ceremony",
    "velocity", "backlog", "refinement", "planning", "review", "daily", "standup",
    "iteration", "delivery", "stakeholder"
]


def get_skill_category(skill_name: str) -> str:
    """Determine the appropriate test query category for a skill."""
    name_lower = skill_name.lower()
    
    for kw in SKILL_CATEGORY_RESEARCH:
        if kw in name_lower:
            return "research"
    
    for kw in SKILL_CATEGORY_DESIGN:
        if kw in name_lower:
            return "design"
    
    for kw in SKILL_CATEGORY_TECHNICAL:
        if kw in name_lower:
            return "technical"
    
    for kw in SKILL_CATEGORY_STRATEGY:
        if kw in name_lower:
            return "strategy"
    
    for kw in SKILL_CATEGORY_PROCESS:
        if kw in name_lower:
            return "process"
    
    return "default"


class SmokeTestResult:
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.category = get_skill_category(skill_name)
        self.query = TEST_QUERIES[self.category]
        self.passed = False
        self.error: Optional[str] = None
        self.response_time_ms: Optional[float] = None
        self.response_length: Optional[int] = None


async def test_skill(skill_name: str, context: AgentContext) -> SmokeTestResult:
    """Test a single skill with a standardized query."""
    result = SmokeTestResult(skill_name)
    
    # Create a minimal agent for testing
    class TestAgent:
        role = "Test Agent"
        name = "Test"
        role_knowledge = ""
        scrum_knowledge = ""
        continuous_discovery_knowledge = ""
        
        def format_response(self, **kwargs):
            from agents.base_agent import AgentResponse
            return AgentResponse(**kwargs)
    
    agent = TestAgent()
    
    start_time = time.time()
    try:
        response = await asyncio.to_thread(
            run_agent_ai,
            agent,
            result.query,
            provider="minimax",
            use_web=True,
            specific_skills=[skill_name],
        )
        
        result.response_time_ms = (time.time() - start_time) * 1000
        result.response_length = len(response.response) if response.response else 0
        
        # Check if response is valid
        if response.response and len(response.response) > 50:
            # Check for error indicators
            error_indicators = ["error", "failed", "could not", "unable to", "exception"]
            has_error = any(err in response.response.lower() for err in error_indicators)
            
            if has_error and result.response_length < 200:
                result.error = "Response appears to be an error message"
            else:
                result.passed = True
        else:
            result.error = f"Response too short or empty ({result.response_length} chars)"
            
    except Exception as e:
        result.error = str(e)[:200]
    
    return result


async def run_all_tests() -> Dict[str, SmokeTestResult]:
    """Run smoke tests for all skills."""
    # Initialize
    settings = load_settings()
    context = AgentContext(
        product_name=settings.product_name,
        sprint_number=0,
        current_phase="planning",
    )
    AgentRegistry.set_context(context)
    
    # Get all skills
    skills = get_all_skills()
    print(f"Testing {len(skills)} skills...\n")
    
    results: Dict[str, SmokeTestResult] = {}
    
    # Run tests with concurrency limit
    semaphore = asyncio.Semaphore(5)  # Max 5 concurrent tests
    
    async def bounded_test(skill_name: str):
        async with semaphore:
            return await test_skill(skill_name, context)
    
    tasks = [bounded_test(skill.name) for skill in skills]
    
    for i, coro in enumerate(asyncio.as_completed(tasks)):
        result = await coro
        results[result.skill_name] = result
        
        status = "[PASS]" if result.passed else "[FAIL]"
        time_str = f"{result.response_time_ms:.0f}ms" if result.response_time_ms else "N/A"
        error_str = f" - {result.error[:50]}" if result.error else ""
        
        print(f"{status:8} | {result.category:12} | {time_str:8} | {result.skill_name}{error_str}")
        
        if (i + 1) % 20 == 0:
            print(f"\n--- Progress: {i + 1}/{len(skills)} ---\n")
    
    return results


def print_summary(results: Dict[str, SmokeTestResult]):
    """Print test summary."""
    passed = sum(1 for r in results.values() if r.passed)
    failed = len(results) - passed
    
    print("\n" + "=" * 60)
    print("SMOKE TEST SUMMARY")
    print("=" * 60)
    print(f"Total skills tested: {len(results)}")
    print(f"Passed: {passed} ({100*passed/len(results):.1f}%)")
    print(f"Failed: {failed} ({100*failed/len(results):.1f}%)")
    
    if failed > 0:
        print("\n" + "-" * 60)
        print("FAILED SKILLS:")
        for name, result in sorted(results.items()):
            if not result.passed:
                print(f"  - {name}: {result.error}")
    
    # Category breakdown
    print("\n" + "-" * 60)
    print("BY CATEGORY:")
    categories = {}
    for r in results.values():
        if r.category not in categories:
            categories[r.category] = {"passed": 0, "failed": 0}
        if r.passed:
            categories[r.category]["passed"] += 1
        else:
            categories[r.category]["failed"] += 1
    
    for cat in sorted(categories.keys()):
        stats = categories[cat]
        total = stats["passed"] + stats["failed"]
        print(f"  {cat:12}: {stats['passed']}/{total} passed")
    
    # Slowest tests
    print("\n" + "-" * 60)
    print("SLOWEST TESTS (top 10):")
    sorted_by_time = sorted(
        [r for r in results.values() if r.response_time_ms],
        key=lambda x: x.response_time_ms,
        reverse=True
    )[:10]
    
    for r in sorted_by_time:
        print(f"  {r.response_time_ms:.0f}ms - {r.skill_name}")
    
    return failed == 0


async def main():
    """Run smoke tests."""
    print("=" * 60)
    print("SKILL SMOKE TEST - Automated Quality Check")
    print("=" * 60)
    print()
    
    results = await run_all_tests()
    all_passed = print_summary(results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed - see details above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
