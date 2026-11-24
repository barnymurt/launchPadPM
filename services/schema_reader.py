"""
The schema reader - RUNG 1 OF THE FACTORY.

**=> THE FACTORY'S FIRST JOB IS TO CONNECT WHAT IS ALREADY WRITTEN, **=> AND THE
FIRST THING THAT IS WRITTEN AND NOT WIRED IS **THE OUTPUT SCHEMA**.

**=> ELEVEN SCHEMAS EXIST - **=> AND **ZERO** PYTHON FILES READ ONE.

**=> THIS MODULE READS ONE.

**=> AND THE REASON IT MATTERS IS NOT "PROCESS" - **=> IT IS THAT **THE AGENT CANNOT
BE TRUSTED TO PRODUCE THE SHAPE THE FACTORY NEEDS**, **=> AND SO THE SHAPE MUST BE
**CHECKED**, **=> AND **CHECKED** IS NOT THE SAME AS **ASKED FOR**.

**=> AND THE RULE THE FACTORY ENFORCES: **A STAGE'S OUTPUT THAT DOES NOT MATCH ITS
SCHEMA DOES NOT COUNT**.

**=> AND THE HARD PART IS **THE MATCH** - **=> BECAUSE A FIELD NAMED
*"Benchmark comparison"* MAY BE WRITTEN **THIRTEEN** WAYS - **=> AS A HEADING,
**=> AS A **BOLD** LABEL, **=> INSIDE A TABLE ROW, **=> OR UNDER A DIFFERENT BUT
EQUIVALENT NAME Ã¢Å“â€œÃ¢Å“â€œ - **=> AND THE SCHEMAS' **OWN WORKED EXAMPLES** DO EXACTLY
THAT Ã¢Å“â€œÃ¢Å“â€œ, **=> WHICH IS WHY THE MATCH MUST BE **LENIENT** Ã¢Å“â€œÃ¢Å“â€œ - **=> BECAUSE A
CHECK THAT FAILS ON THE SCHEMA'S OWN EXAMPLE IS A CHECK NOBODY WILL TRUST Ã¢Å“â€œÃ¢Å“â€œ.**
"""

import os
import re
from dataclasses import dataclass, field


# **=> THE SKILLS DIRECTORY.**
SKILLS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills"
)

# **=> AND THE WORDS THAT CARRY NO MEANING IN A FIELD NAME Ã¢Å“â€œÃ¢Å“â€œ.**
STOP_WORDS = {
    "the", "and", "for", "with", "from", "per", "not", "any", "all", "each",
    "are", "was", "has", "have", "that", "this", "into", "its", "their",
}


def _words(name: str) -> list:
    """The significant words of a field name."""
    cleaned = re.sub(r"[^A-Za-z0-9 ]+", " ", name)
    return [
        w.lower()
        for w in cleaned.split()
        if len(w) > 2 and w.lower() not in STOP_WORDS
    ]


def _stem(word: str) -> str:
    """
    A crude stem, so "comparison" and "comparisons" are the same word.

    **=> AND "request" AND "requests" Ã¢Å“â€œÃ¢Å“â€œ - **=> AND THIS MATTERS Ã¢Å“â€œÃ¢Å“â€œ BECAUSE THE
    SCHEMA AND THE OUTPUT GENERALLY AGREE ON THE NUMBER Ã¢Å“â€œÃ¢Å“â€œ.**
    """
    # **=> AND **ONLY** THE PLURAL IS STRIPPED ✓✓ - **=> THE "-tion" AND
    # **=> "-al" SUFFIXES ARE **NOT** ✓✓, **=> BECAUSE STRIPPING THEM TURNED
    # **=> "TABLE" INTO "TABL" ✓✓, **=> WHICH MADE THE CHECK **FAIL GOOD
    # **=> OUTPUT** ✓✓, **=> AND THE LESSON IS THAT **CLEVERER IS NOT BETTER**
    # **=> ✓✓ - **=> IT IS **MORE LENIENT, NOT MORE CLEVER** ✓✓.**
    if word.endswith("s") and not word.endswith("ss") and len(word) > 4:
        return word[:-1]
    return word
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


def _parse_required_fields(text: str) -> list:
    """
    The required fields, from lines like:

        - Benchmark comparison (required): vs. SaaS industry standard

    **=> AND A FIELD MAY BE MARKED ONCE AND USED MANY TIMES Ã¢Å“â€œÃ¢Å“â€œ - **=> AND IT IS
    LISTED ONCE Ã¢Å“â€œÃ¢Å“â€œ, **=> BECAUSE THE CHECK IS ABOUT **WHETHER THE FIELD IS THERE
    AT ALL** Ã¢Å“â€œÃ¢Å“â€œ, **=> NOT ABOUT HOW MANY TIMES Ã¢Å“â€œÃ¢Å“â€œ.**
    """
    found: list = []
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


def _parse_required_sections(text: str) -> list:
    """
    The required sections, from headings like:

        ## 2. Assumption Challenges (required, top 3-5 by risk priority)
    """
    found: list = []
    pattern = re.compile(r"^#{1,4}\s+(.+?)\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        heading = match.group(1).strip()
        if "(required" not in heading.lower():
            continue
        if heading not in found:
            found.append(heading)
    return found


def _parse_required_lines(text: str) -> list:
    """
    The lines that must appear **verbatim** - the ones the schema spells out,
    like:

        **Overall Recommendation:** GO / PAUSE / KILL

    **=> AND THESE ARE THE **THE VERDICT** LINES, **=> AND THEY ARE THE ONES A GATE
    CAN ACT ON.**
    """
    found: list = []
    pattern = re.compile(r"^\s*\*\*(.+?)\*\*\s*:?\s*(.+)$", re.MULTILINE)
    for match in pattern.finditer(text):
        label = match.group(1).strip()
        if not label:
            continue
        marker = "**%s**" % label
        if marker not in found:
            found.append(marker)
    return found


def read_schema(skill: str, skills_dir: str = SKILLS_DIR):
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


def all_schemas(skills_dir: str = SKILLS_DIR) -> list:
    """Every schema on disk."""
    found: list = []
    if not os.path.isdir(skills_dir):
        return found
    for entry in sorted(os.listdir(skills_dir)):
        schema = read_schema(entry, skills_dir)
        if schema is not None:
            found.append(schema)
    return found


def _present(name: str, lowered: str) -> bool:
    """
    Is this field in the output?

    **=> AND THE MATCH IS **LENIENT** IN A **SPECIFIC** WAY Ã¢Å“â€œÃ¢Å“â€œ - **=> NOT
    FUZZY Ã¢Å“â€œÃ¢Å“â€œ, **=> BUT **STRUCTURAL** Ã¢Å“â€œÃ¢Å“â€œ:**

    1. **Ã¢â€¡â€™ THE EXACT NAME Ã¢Å“â€œÃ¢Å“â€œ - **=> AS A HEADING Ã¢Å“â€œÃ¢Å“â€œ, **=> AS A **BOLD** LABEL
       Ã¢Å“â€œÃ¢Å“â€œ, **=> OR ANYWHERE IN THE TEXT Ã¢Å“â€œÃ¢Å“â€œ.**
    2. **Ã¢â€¡â€™ ALL THE SIGNIFICANT WORDS Ã¢Å“â€œÃ¢Å“â€œ - **=> STEMMED, **=> SO PLURALS AND
       "-tion" FORMS MATCH Ã¢Å“â€œÃ¢Å“â€œ.**
    3. **Ã¢â€¡â€™ OR THE **HEAD** WORD PLUS **ONE** OTHER Ã¢Å“â€œÃ¢Å“â€œ - **Ã¢â€¡â€™ BECAUSE THE OUTPUT
       MAY USE A SHORTER EQUIVALENT NAME Ã¢Å“â€œÃ¢Å“â€œ, **=> LIKE "**Benchmark**" FOR
       "**Benchmark comparison**" Ã¢Å“â€œÃ¢Å“â€œ, **=> AND THAT IS **THE CASE IN THE
       SCHEMAS' OWN EXAMPLES** Ã¢Å“â€œÃ¢Å“â€œ.**

    **=> AND THE POINT IS NOT TO BE FUZZY Ã¢Å“â€œÃ¢Å“â€œ - **Ã¢â€¡â€™ IT IS TO **NOT FAIL GOOD
    OUTPUT** Ã¢Å“â€œÃ¢Å“â€œ, **Ã¢â€¡â€™ BECAUSE A GATE THAT FAIMS GOOD WORK MAKES THE TEAM STOP
    TRUSTING THE GATE Ã¢Å“â€œÃ¢Å“â€œ, **Ã¢â€¡â€™ AND A GATE NOBODY TRUSTS IS WORTH NOTHING Ã¢Å“â€œÃ¢Å“â€œ.**
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

    stems = [_stem(word) for word in words]
    found_stems = {stem for word in lowered.split() for stem in [_stem(word)]}

    # **=> ALL THE WORDS Ã¢Å“â€œÃ¢Å“â€œ.**
    if all(stem in found_stems for stem in stems):
        return True

    # **=> THE HEAD WORD PLUS ONE MORE Ã¢Å“â€œÃ¢Å“â€œ - **=> AND THE HEAD WORD IS THE **LAST**
    # **=> WORD, **=> BECAUSE THE SCHEMA NAMES THE FIELD **AT THE END** Ã¢Å“â€œÃ¢Å“â€œ, LIKE
    # "**Benchmark comparison**" Ã¢Å“â€œÃ¢Å“â€œ.**
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

    def explain(self) -> str:
        if self.ok:
            return "the %s output matches its schema" % self.skill
        parts: list = []
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


def check_output(output: str, skill: str, skills_dir: str = SKILLS_DIR) -> CheckResult:
    """
    Does this output match this skill's schema?

    **=> AND THE CHECK IS **THE CHEAPEST ONE** - **=> DOES THE OUTPUT HAVE THE
    REQUIRED THINGS - **=> AND THE MATCH MUST BE **LENIENT**, **=> BECAUSE **THE
    AGENT IS **NOT** BEING GRADED ON WORDING**, **=> IT IS BEING GRADED ON
    **WHETHER IT SAID THE THING**.
    """
    schema = read_schema(skill, skills_dir)
    if schema is None:
        return CheckResult(
            ok=False,
            skill=skill,
            reason="this skill has no output schema, so its output cannot be checked",
        )

    text = output or ""
    lowered = text.lower()

    missing_fields: list = []
    for name in schema.required_fields:
        if not _present(name, lowered):
            missing_fields.append(name)

    missing_sections: list = []
    for heading in schema.required_sections:
        # **=> A SECTION MAY APPEAR WITHOUT ITS NUMBERING Ã¢Å“â€œÃ¢Å“â€œ.**
        plain = re.sub(r"^\d+\.\s*", "", heading).strip()
        plain = plain.split("(")[0].strip()
        if _present(plain, lowered):
            continue
        missing_sections.append(heading)

    missing_lines: list = []
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
    )
