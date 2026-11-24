"""
The lifecycle reader — THE SEVEN STAGES, READ FROM DATA.

**⇒ THIS REPLACES \`LIFECYCLE_STAGES\` IN \`skill_loader.py\` ✓✓ — **⇒ AND THE
REASON IS NOT TIDINESS ✓✓, **⇒ IT IS THAT THE FIVE STAGES WERE **FLAT** ✓✓ AND
THE PRODUCT'S LIFE IS **CIRCULAR** ✓✓, **⇒ AND THE SKILLS SERVE **MORE THAN ONE**
STAGE ✓✓, **⇒ AND ALL OF THAT IS **NOWHERE** IN THE CODE ✓✓.**

**⇒ AND THE RULE ✓✓: **NO HARDCODED VALUES IN THE CODE** ✓✓ — **⇒ EVERY STAGE,
**⇒ EVERY SEAM, **⇒ EVERY LOOP EDGE AND **⇒ EVERY SKILL'S CLASSIFICATION COMES
FROM \`governance/product-development-lifecycle.md\` ✓✓.**

**⇒ AND THE LOADER **ALREADY PARSES** THE SKILLS' FRONTMATTER ✓✓ — **⇒ AND IT
**THROWS AWAY** THE THREE FIELDS THAT MATTER ✓✓: \`lifecycle\` ✓✓,
\`relatedBefore\` ✓✓ AND \`relatedAfter\` ✓✓. **⇒ THIS READS THEM ✓✓.**
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# **⇒ THE SKILLS DIRECTORY ✓✓.**
SKILLS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills"
)

# **⇒ THE LIFECYCLE FILE ✓✓.**
LIFECYCLE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "governance",
    "product-development-lifecycle.md",
)


@dataclass
class Stage:
    """One stage of the circle."""

    id: str
    order: int
    title: str
    purpose: str = ""
    reentered_by: str = ""


@dataclass
class Lifecycle:
    """The circle, read from the data file."""

    stages: List[Stage] = field(default_factory=list)
    #: The skills and the stages they serve — read from the frontmatter.
    skill_stages: Dict[str, List[str]] = field(default_factory=dict)
    #: The forward edges: skill -> the skills it feeds.
    edges_after: Dict[str, List[str]] = field(default_factory=dict)
    #: The backward edges: skill -> the skills that feed it.
    edges_before: Dict[str, List[str]] = field(default_factory=dict)
    #: The loop, as declared.
    loop_path: List[str] = field(default_factory=list)
    loop_returns_to: str = ""
    #: The seams: the stage transitions and the skill that carries each.
    seams: List[dict] = field(default_factory=list)

    @property
    def stage_ids(self) -> List[str]:
        return [stage.id for stage in self.stages]

    def stages_for(self, skill: str) -> List[str]:
        return self.skill_stages.get(skill, [])

    def stage(self, stage_id: str) -> Optional[Stage]:
        for stage in self.stages:
            if stage.id == stage_id:
                return stage
        return None


def _parse_yaml_block(text: str, key: str) -> str:
    """
    The block under a top-level key, as raw lines.

    **⇒ AND THE PARSER IS **DELIBERATELY SMALL** ✓✓ — **⇒ THE FILE IS **DATA**
    ✓✓, **⇒ AND A FULL YAML PARSER WOULD BE **A DEPENDENCY** ✓✓, **⇒ AND THE
    FILE IS **WRITTEN** TO BE READ THIS WAY ✓✓.**
    """
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"{key}:":
            start = index + 1
            break
    if start is None:
        return ""
    block: List[str] = []
    base_indent = None
    for line in lines[start:]:
        if not line.strip():
            block.append("")
            continue
        indent = len(line) - len(line.lstrip())
        if base_indent is None:
            base_indent = indent
        if indent < base_indent:
            break
        block.append(line)
    return "\n".join(block)


def _parse_stages(text: str) -> List[Stage]:
    """The stages, in order."""
    block = _parse_yaml_block(text, "stages")
    stages: List[Stage] = []
    current: Dict[str, str] = {}

    def flush() -> None:
        if current.get("id"):
            stages.append(
                Stage(
                    id=current["id"],
                    order=int(current.get("order", "0") or 0),
                    title=current.get("title", current["id"]),
                    purpose=current.get("purpose", ""),
                    reentered_by=current.get("reentered_by", ""),
                )
            )
        current.clear()

    for line in block.splitlines():
        match = re.match(r"^\s*-\s+id:\s*(\S+)\s*$", line)
        if match:
            flush()
            current["id"] = match.group(1)
            continue
        match = re.match(r"^\s+(\w+):\s*(.+?)\s*$", line)
        if match and current:
            current[match.group(1)] = match.group(2).strip('"').strip("'")
    flush()
    return stages


def _parse_loop(text: str) -> tuple:
    """The loop's path and where it returns to."""
    block = _parse_yaml_block(text, "loop")
    path: List[str] = []
    returns_to = ""
    in_path = False
    for line in block.splitlines():
        if re.match(r"^\s*path:\s*$", line):
            in_path = True
            continue
        if re.match(r"^\s*returns_to:\s*(\S+)\s*$", line):
            returns_to = line.split(":", 1)[1].strip()
            in_path = False
            continue
        if in_path:
            # AND THE LINE MAY CARRY A TRAILING COMMENT - AND THE COMMENT
            # IS NOT PART OF THE VALUE - SO IT IS STRIPPED FIRST.
            #
            value = line.split("#")[0].strip()
            match = re.match(r"^-\s+(\S+)\s*$", value)
            if match:
                path.append(match.group(1))
    return path, returns_to


def _parse_seams(text: str) -> List[dict]:
    """The seams — the stage transitions and the skill that carries each."""
    block = _parse_yaml_block(text, "seams")
    seams: List[dict] = []
    current: Dict[str, str] = {}

    def flush() -> None:
        if current.get("skill"):
            seams.append(dict(current))
        current.clear()

    for line in block.splitlines():
        match = re.match(r"^\s*-\s+(\w+):\s*(\S+)\s*$", line)
        if match:
            flush()
            current[match.group(1)] = match.group(2)
            continue
        match = re.match(r"^\s+(\w+):\s*(.+?)\s*$", line)
        if match and current:
            current[match.group(1)] = match.group(2).strip('"').strip("'")
    flush()
    return seams


def _frontmatter(path: str) -> Dict[str, str]:
    """
    The frontmatter, read from the skill's own file.

    **⇒ AND THE LOADER **ALREADY** HAS THIS PARSER ✓✓ — **⇒ THIS IS **THE SAME
    SHAPE** ✓✓, **⇒ AND THE FACTORY NEEDS **ONE** READER ✓✓, **⇒ NOT TWO ✓✓.**
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            content = handle.read()
    except OSError:
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.S)
    if not match:
        return {}
    fields: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def _skill_paths(skills_dir: str = SKILLS_DIR) -> Dict[str, str]:
    """Every skill's file, keyed by its frontmatter name."""
    found: Dict[str, str] = {}
    if not os.path.isdir(skills_dir):
        return found
    for entry in sorted(os.listdir(skills_dir)):
        full = os.path.join(skills_dir, entry)
        if os.path.isdir(full):
            candidate = os.path.join(full, "SKILL.md")
            if not os.path.exists(candidate):
                continue
        elif entry.endswith(".md") and entry.startswith("SKILL-"):
            candidate = full
        else:
            continue
        fields = _frontmatter(candidate)
        name = fields.get("name")
        if name:
            found[name] = candidate
    return found


def _parse_translation(text: str) -> Dict[str, List[str]]:
    """
    The old words, translated into the seven.

    **⇒ AND THE TRANSLATION IS **DATA** ✓✓ — **⇒ IT LIVES IN THE LIFECYCLE FILE
    ✓✓, **⇒ NOT IN THIS MODULE ✓✓ — **⇒ BECAUSE **A WORD** IS A **DECISION** ✓✓,
    **⇒ AND A DECISION BELONGS IN A DOCUMENT ✓✓, **⇒ WHERE IT CAN BE ARGUED WITH
    ✓✓.**
    """
    block = _parse_yaml_block(text, "translation")
    translation: Dict[str, List[str]] = {}
    for line in block.splitlines():
        match = re.match(r"^\s*(\w+):\s*\[(.*?)\]\s*$", line)
        if match:
            translation[match.group(1)] = [
                piece.strip() for piece in match.group(2).split(",") if piece.strip()
            ]
    return translation


def read_lifecycle(
    lifecycle_file: str = LIFECYCLE_FILE,
    skills_dir: str = SKILLS_DIR,
) -> Lifecycle:
    """
    The whole circle, read from the data.

    **⇒ AND EVERYTHING COMES FROM **THE FILES** ✓✓ — **⇒ THE STAGES ✓✓, **⇒ THE
    SKILLS' CLASSIFICATION ✓✓, **⇒ THE EDGES ✓✓, **⇒ THE LOOP ✓✓, **⇒ AND THE
    SEAMS ✓✓ — **⇒ AND **NOTHING** IS A PYTHON LITERAL ✓✓.**
    """
    lifecycle = Lifecycle()

    try:
        with open(lifecycle_file, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    except OSError:
        return lifecycle

    lifecycle.stages = _parse_stages(text)
    lifecycle.loop_path, lifecycle.loop_returns_to = _parse_loop(text)
    lifecycle.seams = _parse_seams(text)
    translation = _parse_translation(text)

    # **⇒ THE SKILLS' OWN FILES ✓✓ — **⇒ THE CLASSIFICATION AND THE EDGES ✓✓.**
    for name, path in _skill_paths(skills_dir).items():
        fields = _frontmatter(path)

        # **⇒ THE STAGES, **AS A LIST** ✓✓ — **⇒ BECAUSE A SKILL MAY SERVE MORE
        # **⇒ THAN ONE ✓✓, **⇒ AND THE PEER'S WHOLE POINT ✓✓.**
        #
        # **⇒ AND THE FILE MAY NAME **THE SEVEN DIRECTLY** ✓✓, **⇒ OR THE **OLD
        # **FOUR** ✓✓ — **⇒ AND THE OLD ONES ARE TRANSLATED **BY THE DATA**
        # **⇒ ✓✓, **⇒ NOT BY THE CODE ✓✓.**
        raw = fields.get("stage", "") or fields.get("lifecycle", "") or fields.get("stages", "")
        pieces = [piece.strip().lower() for piece in raw.split(",") if piece.strip()]

        stages: List[str] = []
        for piece in pieces:
            if piece in lifecycle.stage_ids:
                # **⇒ ALREADY ONE OF THE SEVEN ✓✓ — **⇒ AND **THE SEVEN** IS THE
                # **⇒ PEER'S VOCABULARY ✓✓ — **⇒ SO IT IS TAKEN AS IT IS ✓✓.
                if piece not in stages:
                    stages.append(piece)
            else:
                # **⇒ ONE OF THE OLD FOUR ✓✓ — **⇒ TRANSLATED BY THE DATA ✓✓.
                for stage in translation.get(piece, []):
                    if stage not in stages:
                        stages.append(stage)
        if stages:
            lifecycle.skill_stages[name] = stages

        before = [
            piece.strip()
            for piece in fields.get("relatedBefore", "").split(",")
            if piece.strip() and piece.strip() != "[]"
        ]
        after = [
            piece.strip()
            for piece in fields.get("relatedAfter", "").split(",")
            if piece.strip() and piece.strip() != "[]"
        ]
        if before:
            lifecycle.edges_before[name] = before
        if after:
            lifecycle.edges_after[name] = after

    return lifecycle


def dangling_edges(lifecycle: Lifecycle, skills_dir: str = SKILLS_DIR) -> List[dict]:
    """
    The edges that point at skills the library does not have.

    **⇒ AND THIS IS A **FEATURE** ✓✓, **⇒ NOT A BUG REPORT ✓✓ — **⇒ BECAUSE A
    FACTORY THAT KNOWS **WHAT IT CANNOT DO** ✓✓ IS MORE USEFUL THAN ONE THAT
    PRETENDS ✓✓.**
    """
    present = set(_skill_paths(skills_dir))
    found: List[dict] = []
    for source, targets in lifecycle.edges_after.items():
        for target in targets:
            if target not in present:
                found.append({"from": source, "to": target, "edge": "relatedAfter"})
    for target, sources in lifecycle.edges_before.items():
        for source in sources:
            if source not in present:
                found.append({"from": source, "to": target, "edge": "relatedBefore"})
    return found


def walkable(lifecycle: Lifecycle, skills_dir: str = SKILLS_DIR) -> dict:
    """
    How much of the circle can actually be walked.

    **⇒ AND THIS IS THE FACTORY'S SECOND MEASUREMENT ✓✓ — **⇒ THE LIVE EDGES OVER
    THE DECLARED ONES ✓✓.**
    """
    present = set(_skill_paths(skills_dir))
    live = 0
    total = 0
    for targets in lifecycle.edges_after.values():
        for target in targets:
            total += 1
            if target in present:
                live += 1
    for sources in lifecycle.edges_before.values():
        for source in sources:
            total += 1
            if source in present:
                live += 1
    return {"live": live, "total": total, "skills": len(present)}
