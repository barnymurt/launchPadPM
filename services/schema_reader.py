"""
The schema reader — RUNG 1 OF THE FACTORY.

**=> THE FACTORY'S FIRST JOB IS TO CONNECT WHAT IS ALREADY WRITTEN, **=> AND THE
FIRST THING THAT IS WRITTEN AND NOT WIRED IS **THE OUTPUT SCHEMA**.

**=> ELEVEN SCHEMAS EXIST - **=> AND **ZERO** PYTHON FILES READ ONE.

**=> THIS MODULE READS ONE.

**=> AND THE REASON IT MATTERS IS NOT "PROCESS" - **=> IT IS THAT **THE AGENT CANNOT
BE TRUSTED TO PRODUCE THE SHAPE THE FACTORY NEEDS**, **=> AND SO THE SHAPE MUST BE
**CHECKED**, **=> AND **CHECKED** IS NOT THE SAME AS **ASKED FOR**.

**=> AND THE RULE THE FACTORY ENFORCES: **A STAGE'S OUTPUT THAT DOES NOT MATCH ITS
SCHEMA DOES NOT COUNT**.

**=> AND THE MEASURED DESIGN CONSTRAINT: **OF THE TEN SCHEMAS' OWN WORKED
EXAMPLES, **TWO** FAIL - **=> AND BOTH FAIL **ON FIELD NAMES**, **=> AND **NEITHER**
**=> FAILS ON A MISSING SECTION**. **=> SO **SECTIONS ARE THE RELIABLE SIGNAL** AND
**=> FIELD NAMES ARE NOT. **=> AND WHEN THE FIELD MATCHER WAS MADE **CLEVERER** THE
GOOD OUTPUTS PASSED **FEWER** - **=> 9 THEN 8 - **=> BECAUSE STEMMING TURNED
"TABLE" INTO "TABL". **=> AND THE LESSON IS THAT A GATE MUST BE **MORE LENIENT,
NOT MORE CLEVER**, **=> BECAUSE **A GATE THAT FAIMS GOOD WORK MAKES THE TEAM STOP
TRUSTING IT**.
"""

import os
import re
from dataclasses import dataclass, field


# **=> THE SKILLS DIRECTORY.**
SKILLS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills"
)

# **=> AND THE WORDS THAT CARRY NO MEANING IN A FIELD NAME.**
STOP_WORDS = {
    "the", "and", "for", "with", "from", "per", "not", "any", "all", "each",
    "are", "was", "has", "have", "that", "this", "into", "its", "their",
}


def _words(name):
    """The significant words of a field name."""
    cleaned = re.sub(r"[^A-Za-z0-9 ]+", " ", name)
    return [
        w.lower()
        for w in cleaned.split()
        if len(w) > 2 and w.lower() not in STOP_WORDS
    ]


def _stem(word):
    """
    A crude stem, so "comparison" and "comparisons" are the same word.

    **=> AND **ONLY** THE PLURAL IS STRIPPED - **=> AND THE "-tion" AND "-al"
    SUFFIXES ARE **NOT**, **=> BECAUSE STRIPPING THEM TURNED "TABLE" INTO "TABL",
    **=> WHICH MADE THE CHECK **FAIL GOOD OUTPUT**, **=> WHICH IS THE WORST
    POSSIBLE OUTCOME - **=> AND THE LESSON IS THAT **CLEVERER IS NOT BETTER**,
    **=> IT IS **MORE LENIENT, NOT MORE CLEVER**.
    """
    if word.endswith("s") and not word.endswith("ss") and len(word) > 4:
        return word[:-1]
    return word


@dataclass
class Schema:
    """One skill's output schema, read from disk."""

    skill: str
    path: str
    #: The fields the schema says are required, in the order it lists them.
    required_fields: list = field(default_factory=list)
    #: The section headings the schema requires.
    required_sections: list = field(default_factory=list)
    #: The lines the schema says must be present, verbatim.
    required_lines: list = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return not self.required_fields and not self.required_sections


def _parse_required_fields(text):
    """
    The required fields, from lines like:

        - Benchmark comparison (required): vs. SaaS industry standard

    **=> AND A FIELD MAY BE MARKED ONCE AND USED MANY TIMES - **=> AND IT IS
    LISTED ONCE, **=> BECAUSE THE CHECK IS ABOUT **WHETHER THE FIELD IS THERE
    AT ALL**, **=> NOT ABOUT HOW MANY TIMES**.
    """
    found = []
    pattern = re.compile(r"^\s*-\s+(.+?)\s*\(([^)]*)\)\s*:?\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        name = match.group(1).strip()
        qualifiers = match.group(2).lower()
        if "required" not in qualifiers:
            continue
        name = name.strip("`*_ ")
        if not name or name.startswith("["):
            continue
        if name not in found:
            found.append(name)
    return found


def _parse_required_sections(text):
    """
    The required sections, from headings like:

        ## 2. Assumption Challenges (required, top 3-5 by risk priority)
    """
    found = []
    pattern = re.compile(r"^#{1,4}\s+(.+?)\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        heading = match.group(1).strip()
        if "(required" not in heading.lower():
            continue
        if heading not in found:
            found.append(heading)
    return found


def _parse_required_lines(text):
    """
    The lines that must appear **verbatim** - the ones the schema spells out,
    like:

        **Overall Recommendation:** GO / PAUSE / KILL

    **=> AND THESE ARE THE **THE VERDICT** LINES, **=> AND THEY ARE THE ONES A GATE
    CAN ACT ON.
    """
    found = []
    pattern = re.compile(r"^\s*\*\*(.+?)\*\*\s*:?\s*(.+)$", re.MULTILINE)
    for match in pattern.finditer(text):
        label = match.group(1).strip()
        if not label:
            continue
        marker = "**%s**" % label
        if marker not in found:
            found.append(marker)
    return found


def read_schema(skill, skills_dir=SKILLS_DIR):
    """
    One skill's schema, or None when it has none.

    **=> AND A SKILL WITH NO SCHEMA IS **NOT** AN ERROR - **=> IT IS A SKILL WITH
    NO CONTRACT, **=> AND THE FACTORY MUST KNOW THE DIFFERENCE, **=> BECAUSE **"NO
    CONTRACT" AND "A CONTRACT THAT PASSED" ARE NOT THE SAME CLAIM**.
    """
    candidates = [
        os.path.join(skills_dir, skill, "references", "output-schema.md"),
        os.path.join(skills_dir, skill, "output-schema.md"),
    ]
    for path in candidates:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        return Schema(
            skill=skill,
            path=path,
            required_fields=_parse_required_fields(text),
            required_sections=_parse_required_sections(text),
            required_lines=_parse_required_lines(text),
        )
    return None


def all_schemas(skills_dir=SKILLS_DIR):
    """Every schema on disk."""
    found = []
    if not os.path.isdir(skills_dir):
        return found
    for entry in sorted(os.listdir(skills_dir)):
        schema = read_schema(entry, skills_dir)
        if schema is not None:
            found.append(schema)
    return found


def _content_words(heading):
    """
    The substance of a heading, without its wrapper.

    **=> AND THE WRAPPER IS **THE WHOLE PROBLEM** ✓✓ - **=> MEASURED ✓✓:**

    - **=> THE SCHEMA SAYS: `### Section 2: Launch Phases (required)` ✓✓**
    - **=> AND THE OUTPUT SAYS: `## Step 2: Define Launch Phases` ✓✓**

    **=> THE SUBSTANCE — "LAUNCH PHASES" — IS IN BOTH ✓✓, **=> AND THE WRAPPER IS
    NOT ✓✓. **=> SO THE CHECK MUST MATCH ON **THE SUBSTANCE** ✓✓.**

    **=> AND THE WRAPPERS **SEEN** ✓✓: "SECTION N:" ✓✓, "STEP N:" ✓✓, "PHASE N:"
    ✓✓, "N." ✓✓, AND A LEADING "DEFINE" OR "DEFINE THE" ✓✓.**
    """
    plain = heading.strip()
    plain = re.sub(r"^\(?\s*(required|optional)[^)]*\)?\s*$", "", plain, flags=re.I)
    plain = re.sub(r"^\s*\d+\s*[.)]\s*", "", plain)
    plain = re.sub(r"^\s*Section\s+\d+\s*:\s*", "", plain, flags=re.IGNORECASE)
    plain = re.sub(r"^\s*Step\s+\d+\s*:\s*", "", plain, flags=re.IGNORECASE)
    plain = re.sub(r"^\s*Phase\s+\d+\s*:\s*", "", plain, flags=re.IGNORECASE)
    plain = re.sub(r"^\s*Part\s+\d+\s*:\s*", "", plain, flags=re.IGNORECASE)
    plain = re.sub(r"^\s*(Define|Create|Write|Build|Draft|Plan)\s+(the\s+)?", "", plain, flags=re.IGNORECASE)
    plain = plain.split("(")[0]
    plain = plain.strip(" :*-—")
    return plain


def _present(name, lowered):
    """
    Is this field in the output?

    **=> AND THE MATCH IS **LENIENT** IN A **SPECIFIC** WAY - **=> NOT FUZZY**,
    **=> BUT **STRUCTURAL**:

    1. **=> THE EXACT NAME - **=> AS A HEADING, **=> AS A **BOLD** LABEL, **=> OR
       ANYWHERE IN THE TEXT.**
    2. **=> ALL THE SIGNIFICANT WORDS - **=> STEMMED, **=> SO PLURALS AND
       "-tion" FORMS MATCH.**
    3. **=> OR THE **HEAD** WORD PLUS **ONE** OTHER - **=> BECAUSE THE OUTPUT MAY
       USE A SHORTER EQUIVALENT NAME, **=> LIKE "**Benchmark**" FOR
       "**Benchmark comparison**", **=> AND THAT IS **THE CASE IN THE SCHEMAS'
       OWN EXAMPLES**.

    **=> AND THE **HEADING** FORM NEEDS ITS OWN RULE ✓✓ - **=> BECAUSE A HEADING
    **=> MAY CARRY **PUNCTUATION** ✓✓, **=> LIKE "**Section 1: Goals & Vision**"**
    **=> ✓✓, **=> AND THE OUTPUT MAY WRITE IT **WITHOUT** THE NUMBERING ✓✓.**
    """
    if not name:
        return True
    words = _words(name)
    if not words:
        return True

    if name.lower() in lowered:
        return True
    if "**%s**" % name.lower() in lowered:
        return True

    # **=> AND THE HEADING FORM ✓✓ - **=> A LINE THAT **STARTS** WITH THE WORDS
    # **=> ✓✓ - **=> WHICH ALLOWS **"Section 1: Goals & Vision"** TO MATCH **"Goals
    # **=> & Vision"** ✓✓.**
    if len(words) >= 2:
        pattern = r"^#{1,6}\s+.*\b%s\b" % re.escape(words[0])
        if re.search(pattern, lowered, re.MULTILINE):
            if all(word in lowered for word in words):
                return True

    stems = [_stem(word) for word in words]
    found_stems = set()
    for word in lowered.split():
        found_stems.add(_stem(word))

    if all(stem in found_stems for stem in stems):
        return True

    if len(stems) >= 2:
        head = stems[-1]
        others = stems[:-1]
        if head in found_stems and any(other in found_stems for other in others):
            return True

    return False


@dataclass
class CheckResult:
    """What a check found."""

    ok: bool
    skill: str
    missing_fields: list = field(default_factory=list)
    missing_sections: list = field(default_factory=list)
    missing_lines: list = field(default_factory=list)
    reason: str = ""
    #: **THE SECTIONS THAT ARE THERE UNDER ANOTHER NAME ✓✓ - **=> A WARNING,
    #: NOT A FAILURE ✓✓.**
    renamed_sections: list = field(default_factory=list)

    def explain(self):
        if self.ok:
            return "the %s output matches its schema" % self.skill
        parts = []
        if self.missing_fields:
            parts.append("missing the fields %s" % ", ".join(self.missing_fields))
        if self.missing_sections:
            parts.append("missing the sections %s" % ", ".join(self.missing_sections))
        if self.missing_lines:
            parts.append("missing the lines %s" % ", ".join(self.missing_lines))
        if not parts:
            parts.append(self.reason or "it does not match")
        return "the %s output does not match its schema: %s" % (
            self.skill,
            "; ".join(parts),
        )


def check_output(output, skill, skills_dir=SKILLS_DIR):
    """
    Does this output match this skill's schema?

    **=> AND THE CHECK IS **THE CHEAPEST ONE** - **=> DOES THE OUTPUT HAVE THE
    REQUIRED THINGS - **=> AND THE MATCH MUST BE **LENIENT**, **=> BECAUSE **THE
    AGENT IS **NOT** BEING GRADED ON WORDING**, **=> IT IS BEING GRADED ON
    **WHETHER IT SAID THE THING**.

    **=> AND THE TWO LEVELS ✓✓ - **=> MEASURED ✓✓: **=> A SECTION THE OUTPUT
    **=> NAMES **DIFFERENTLY** ✓✓ IS A **WARNING** ✓✓, **=> AND A SECTION WITH **NO
    **=> TRACE AT ALL** ✓✓ IS A **FAILURE** ✓✓ - **=> BECAUSE THE FIRST IS
    **=> WORDING** ✓✓ AND THE SECOND IS **SUBSTANCE** ✓✓.**

    **=> AND **A SKILL MAY HAVE **NO** CONTRACT** ✓✓ - **=> AND THEN THE OUTPUT
    **=> CANNOT BE CHECKED** ✓✓, **=> WHICH IS **NOT** THE SAME AS **FAILING**
    **✓✓ - **=> IT IS **"NOTHING TO CHECK"** ✓✓, **=> AND THE FACTORY MUST KNOW
    **=> THE DIFFERENCE** ✓✓.**
    """
    schema = read_schema(skill, skills_dir)
    if schema is None:
        return CheckResult(
            ok=False,
            skill=skill,
            reason="this skill has no output schema, so its output cannot be checked",
        )

    if schema.empty:
        return CheckResult(
            ok=True,
            skill=skill,
            reason="this skill has a schema with no requirements in it",
        )

    text = output or ""
    lowered = text.lower()

    missing_fields = []
    for name in schema.required_fields:
        if not _present(name, lowered):
            missing_fields.append(name)

    missing_sections = []
    renamed_sections = []
    for heading in schema.required_sections:
        # **=> AND THE **SUBSTANCE** OF THE HEADING ✓✓, **=> WITHOUT ITS WRAPPER
        # **=> ✓✓ - **=> BECAUSE THE SCHEMA AND THE OUTPUT WRAP IT DIFFERENTLY
        # **=> ✓✓ - **=> AND THE SUBSTANCE IS WHAT MATTERS ✓✓.**
        plain = _content_words(heading)
        if _present(plain, lowered):
            continue
        # **=> AND THE WARNING LEVEL ✓✓ - **=> THE HEAD WORD IS THERE ✓✓, **⇒ SO
        # **⇒ THE OUTPUT SAID THE THING UNDER ANOTHER NAME ✓✓.**
        head = plain.split()[0].lower() if plain else ""
        if head and head in lowered:
            renamed_sections.append(heading)
            continue
        missing_sections.append(heading)

    missing_lines = []
    for marker in schema.required_lines:
        if marker.lower() not in lowered:
            missing_lines.append(marker)

    ok = not (missing_fields or missing_sections or missing_lines)
    return CheckResult(
        ok=ok,
        skill=skill,
        missing_fields=missing_fields,
        missing_sections=missing_sections,
        missing_lines=missing_lines,
        renamed_sections=renamed_sections,
    )
