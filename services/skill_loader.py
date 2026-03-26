"""
Skill loader for AgentPad skills.
Loads SKILL.md files, extracts rich metadata for skill discovery and guidance.
"""

import os
import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "skills")


@dataclass
class Skill:
    name: str
    description: str
    path: str
    skill_type: str

    lifecycle_stage: str = ""
    lifecycle_order: int = 0

    outputs: str = ""
    when_to_use: str = ""
    triggers: List[str] = field(default_factory=list)

    workflow_steps: List[str] = field(default_factory=list)
    quality_criteria: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)

    full_content: str = ""


LIFECYCLE_STAGES = {
    "Discovery": {
        "order": 1,
        "description": "Understand the problem, the market, and the customer before deciding what to build.",
        "skills": ["competitor-research", "user-persona-creation", "requirements-elicitation", "feedback-synthesis", "user-journey-mapping"],
    },
    "Strategy": {
        "order": 2,
        "description": "Define what to build and why. Score ideas, model business cases, challenge assumptions.",
        "skills": ["feature-prioritization", "business-case-modeling", "devils-advocate", "saas-metrics-analysis"],
    },
    "Build": {
        "order": 3,
        "description": "Design and build the product. From frontend to backend, testing to infrastructure.",
        "skills": ["frontend-design", "web-artifacts-builder", "mcp-builder", "webapp-testing"],
    },
    "Launch": {
        "order": 4,
        "description": "Position, package, and go to market. Branding, messaging, and launch planning.",
        "skills": ["brandguidelines", "theme-factory", "internalcomms", "docx", "pdf", "pptx"],
    },
    "Iteration": {
        "order": 5,
        "description": "Measure, learn, and improve. Metrics analysis, feedback synthesis, and roadmap updates.",
        "skills": ["saas-metrics-analysis", "feedback-synthesis", "feature-prioritization"],
    },
}

SKILL_TRIGGERS = {
    "competitor-research": ["who are our competitors", "competitive landscape", "vs", "alternative to", "market analysis"],
    "user-persona-creation": ["who is our customer", "user personas", "target audience", "customer profile"],
    "requirements-elicitation": ["requirements", "what should we build", "functional specs", "acceptance criteria"],
    "feedback-synthesis": ["customer feedback", "user research", "interview synthesis", "survey results"],
    "user-journey-mapping": ["user journey", "customer journey", "touchpoints", "experience mapping"],
    "feature-prioritization": ["prioritize", "rank features", "what to build next", "RICE", "ICE scoring"],
    "business-case-modeling": ["business case", "revenue model", "LTV", "CAC", "unit economics", "ROI"],
    "devils-advocate": ["challenge", "assumption", "objection", "why would customers", "is this a good idea"],
    "saas-metrics-analysis": ["churn", "MRR", "ARR", "LTV", "metrics", "cohort analysis", "funnel"],
    "frontend-design": ["design the UI", "frontend", "landing page", "mockup", "interface"],
    "web-artifacts-builder": ["build landing page", "React", "prototype", "web app"],
    "mcp-builder": ["MCP server", "model context protocol", "agent tool", "tool integration"],
    "webapp-testing": ["testing", "QA", "playwright", "E2E", "test coverage"],
    "brandguidelines": ["brand", "logo", "colors", "typography", "brand identity"],
    "theme-factory": ["theme", "design system", "consistent styling", "CSS variables"],
    "internalcomms": ["team update", "stakeholder communication", "internal messaging"],
    "docx": ["document", "Word", "spec document", "report"],
    "pdf": ["PDF", "report", "downloadable document"],
    "pptx": ["presentation", "pitch deck", "slides", "PowerPoint"],
    "algorithmic-art": ["visual", "art", "image", "generative", "canvas"],
    "canvasdesign": ["canvas", "graphic", "social media", "visual asset"],
    "doc-coauthor": ["co-author", "writing", "document collaboration"],
    "quality-checklist": ["quality", "checklist", "review", "audit"],
    "creator": ["create a skill", "new skill", "build a skill"],
}

SKILL_OUTPUTS = {
    "competitor-research": "Competitive landscape matrix with 8-dimension scoring, ranked competitor list, strategic gap analysis, positioning recommendations",
    "user-persona-creation": "3-5 detailed personas with jobs-to-be-done, pain points, goals, and behavior patterns",
    "requirements-elicitation": "Structured requirements document with functional/non-functional specs, acceptance criteria, and traceability matrix",
    "feedback-synthesis": "Themed insight report with sentiment analysis, priority issue list, and actionable recommendations",
    "user-journey-mapping": "End-to-end journey map with pain points, moments of delight, and improvement opportunities",
    "feature-prioritization": "Prioritized backlog with RICE/ICE scores, ranking rationale, confidence levels, and build/validate/park tiers",
    "business-case-modeling": "Financial model with TAM/SAM/SOM, revenue projections, LTV/CAC/payback period, and scenario analysis",
    "devils-advocate": "Assumption challenge report with top objections, switching cost analysis, and value proposition gap map",
    "saas-metrics-analysis": "Metrics dashboard with MRR/ARR trends, churn analysis, cohort retention curves, and growth recommendations",
    "frontend-design": "Component architecture, design system specifications, responsive layout wireframes, and interaction patterns",
    "web-artifacts-builder": "Production-ready React/Tailwind landing page or web app prototype",
    "mcp-builder": "Working MCP server with tool definitions, JSON schema, and integration examples",
    "webapp-testing": "Playwright E2E test suite with coverage report, bug list, and quality assessment",
    "brandguidelines": "Brand identity document with logo usage, color palette, typography scale, and tone of voice",
    "theme-factory": "CSS theme with design tokens, component styles, and dark/light mode variants",
    "internalcomms": "Stakeholder update template, team announcement, and communication cadence playbook",
    "docx": "Formatted Word document — business plan, product spec, or proposal with proper heading hierarchy",
    "pdf": "Print-ready PDF — one-pager, report, or polished deliverable",
    "pptx": "PowerPoint presentation — pitch deck, stakeholder update, or sales collateral",
    "algorithmic-art": "Generated visual/illustration for marketing or UI use",
    "canvasdesign": "Social media graphics, banners, or visual content assets",
    "doc-coauthor": "Co-written document with structured outline, key arguments, and editorial notes",
    "quality-checklist": "Skill quality audit with pass/fail criteria and improvement recommendations",
    "creator": "New SKILL.md file with frontmatter, workflow, and reference templates",
}


@dataclass
class SkillStage:
    name: str
    order: int
    description: str
    skills: List["Skill"]


def _parse_frontmatter(content: str) -> Dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm


def _determine_skill_type(name: str, path: str) -> str:
    if name == "quality-checklist":
        return "checklist"
    if "/_template" in path or name.startswith("SKILL-"):
        return "standalone"
    return "workflow"


def _extract_workflow_steps(content: str) -> List[str]:
    steps = []
    pattern = r"### Step \d+[:|]?\s*(.+?)(?:\n|$)"
    for match in re.finditer(pattern, content, re.MULTILINE):
        step = match.group(1).strip()
        if step:
            steps.append(step)
    if not steps:
        h2_pattern = r"## Core Workflow"
        m = re.search(h2_pattern, content)
        if m:
            steps = ["Multi-step structured workflow — see skill content for details"]
    return steps


def _extract_section(content: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}\s*\n(.*?)(?=\n## |$)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


def _extract_list(content: str, heading: str) -> List[str]:
    text = _extract_section(content, heading)
    if not text:
        return []
    items = re.findall(r"^\d+\.\s+(.+?)(?:\n|$)", text, re.MULTILINE)
    if not items:
        items = re.findall(r"^[-*]\s+(.+?)(?:\n|$)", text, re.MULTILINE)
    return [item.strip() for item in items if item.strip()]


def _get_lifecycle_stage(skill_name: str) -> tuple:
    for stage_name, stage_info in LIFECYCLE_STAGES.items():
        if skill_name in stage_info["skills"]:
            return stage_name, stage_info["order"]
    fallback_order = 2
    fallback_stage = "Strategy"
    return fallback_stage, fallback_order


def _load_skill_file(skill_path: str) -> Optional[Skill]:
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, IOError):
        return None

    fm = _parse_frontmatter(content)
    if not fm.get("name"):
        return None

    raw_name = fm["name"]
    name = raw_name.replace("SKILL-", "")

    stage_name, stage_order = _get_lifecycle_stage(name)

    skill = Skill(
        name=name,
        description=fm.get("description", ""),
        path=skill_path,
        skill_type=_determine_skill_type(raw_name, skill_path),
        lifecycle_stage=stage_name,
        lifecycle_order=stage_order,
        outputs=SKILL_OUTPUTS.get(name, "Structured output — see skill content for details"),
        triggers=SKILL_TRIGGERS.get(name, []),
        workflow_steps=_extract_workflow_steps(content),
        quality_criteria=_extract_list(content, "Quality Criteria"),
        common_mistakes=_extract_list(content, "Common Mistakes"),
        full_content=content,
    )
    return skill


_skills_index: List[Skill] = []
_index_ready = False


def _ensure_index() -> None:
    global _skills_index, _index_ready
    if _index_ready:
        return

    skills_dir = Path(SKILLS_DIR)
    if not skills_dir.exists():
        _index_ready = True
        return

    _skills_index = []
    for root, _, files in os.walk(skills_dir):
        if "_template" in root:
            continue
        for file in files:
            if file == "SKILL.md":
                skill_path = os.path.join(root, file)
                skill = _load_skill_file(skill_path)
                if skill:
                    _skills_index.append(skill)
            elif file.endswith(".md") and file.startswith("SKILL-"):
                skill_path = os.path.join(root, file)
                skill = _load_skill_file(skill_path)
                if skill:
                    _skills_index.append(skill)

    _skills_index.sort(key=lambda s: (s.lifecycle_order, s.name))
    _index_ready = True


def get_all_skills() -> List[Skill]:
    _ensure_index()
    return _skills_index


def get_skill(name: str) -> Optional[Skill]:
    _ensure_index()
    for skill in _skills_index:
        if skill.name == name or skill.name == f"SKILL-{name}":
            return skill
    return None


def get_skills_by_stage() -> Dict[str, Dict[str, Any]]:
    _ensure_index()
    result: Dict[str, Dict[str, Any]] = {}
    for stage_name, stage_info in sorted(LIFECYCLE_STAGES.items(), key=lambda x: x[1]["order"]):
        skills_in_stage = [s for s in _skills_index if s.lifecycle_stage == stage_name]
        if skills_in_stage:
            result[stage_name] = {
                "order": stage_info["order"],
                "description": stage_info["description"],
                "skills": [_skill_to_dict(s) for s in skills_in_stage],
            }
    return result


def get_skills_by_type(skill_type: str) -> List[Skill]:
    _ensure_index()
    return [s for s in _skills_index if s.skill_type == skill_type]


def get_relevant_skills(query: str, top_k: int = 3) -> List[Skill]:
    _ensure_index()
    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored = []
    for skill in _skills_index:
        score = 0
        name_lower = skill.name.lower().replace("-", " ")
        desc_lower = skill.description.lower()

        if query_lower in name_lower:
            score += 10
        if query_lower in desc_lower:
            score += 5

        name_words = set(name_lower.split())
        score += len(query_words & name_words) * 2

        desc_words = set(desc_lower.split())
        score += len(query_words & desc_words)

        for trigger in skill.triggers:
            if trigger.lower() in query_lower:
                score += 8

        if score > 0:
            scored.append((score, skill))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in scored[:top_k]]


def get_skill_context(skill_name: str) -> str:
    skill = get_skill(skill_name)
    if not skill:
        return ""
    return skill.full_content


def format_skills_for_prompt(skills: List[Skill]) -> str:
    if not skills:
        return ""
    parts = ["## Available Skills\n"]
    for skill in skills:
        steps = "\n  ".join(f"- {s}" for s in skill.workflow_steps[:5])
        parts.append(
            f"### {skill.name.replace('-', ' ').title()}\n"
            f"{skill.description}\n"
            f"Key steps: {skill.workflow_steps[0] if skill.workflow_steps else 'Multi-step workflow'}\n"
        )
    return "\n".join(parts)


def _skill_to_dict(skill: Skill) -> Dict[str, Any]:
    return {
        "name": skill.name,
        "description": skill.description,
        "skill_type": skill.skill_type,
        "lifecycle_stage": skill.lifecycle_stage,
        "outputs": skill.outputs,
        "triggers": skill.triggers[:5],
        "workflow_steps": skill.workflow_steps[:4],
        "quality_criteria_count": len(skill.quality_criteria),
        "common_mistakes_count": len(skill.common_mistakes),
    }
