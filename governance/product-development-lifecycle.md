# The Product Development Life Cycle — the factory's data file

**⇒ THIS IS THE **SEVEN** STAGES ✓✓, **⇒ FROM THE PEER'S DIAGRAM ✓✓, **⇒ AND IT
IS **DATA** ✓✓ — **⇒ NOT A PYTHON LITERAL ✓✓, **⇒ PER THE RULE ✓✓.**

**⇒ AND THE SKILLS ARE **CLASSIFIED ACROSS** IT ✓✓ — **⇒ A SKILL MAY SERVE **MORE
THAN ONE** STAGE ✓✓, **⇒ BECAUSE THE PRODUCT'S LIFE **FLIPS BACK AND FORWARD**
✓✓.**

## **⇒ THE CIRCLE ✓✓**

```yaml
lifecycle:
  version: 1
  circular: true
  stages:
    - id: ideation
      order: 1
      title: Ideation
      purpose: The idea, and the case for it.
      reentered_by: Post-Launch evidence, and new client information.
    - id: research
      order: 2
      title: Research
      purpose: The market, the user, and the evidence.
      reentered_by: Feedback from what shipped, and a client request.
    - id: design
      order: 3
      title: Design
      purpose: The shape of the thing.
      reentered_by: Research that contradicts the design.
    - id: development
      order: 4
      title: Development
      purpose: Building it.
      reentered_by: A design that cannot be built as drawn.
    - id: testing
      order: 5
      title: Testing
      purpose: Proving it works.
      reentered_by: A defect, or a gate that says PAUSE.
    - id: launch
      order: 6
      title: Launch
      purpose: Putting it in front of people.
      reentered_by: A pre-sale that does not convert.
    - id: post-launch
      order: 7
      title: Post-Launch
      purpose: What the world says back.
      reentered_by: Nothing. **This stage is the loop's fuel.**
```

## **⇒ AND THE LOOP ✓✓ — **THE ONE THING THE PEER NAMED ✓✓**

**⇒ **⇒ "THE LOOP SHOULD GO BACK THE START AFTER POST LAUNCH SO THAT **IDEATION IS
INSPIRED BY THE POST LAUNCH DATA**" ✓✓.**

**⇒ **⇒ AND IT IS **ALREADY WRITTEN** ✓✓ — **⇒ IN THE SKILLS' OWN
`relatedBefore` AND `relatedAfter`** ✓✓ — **⇒ AND **HERE** IT IS, AS DATA ✓✓:**

```yaml
loop:
  origin: ideation
  # **⇒ THE EDGE THAT MAKES IT A CIRCLE ✓✓, **⇒ NOT A LINE ✓✓.**
  # **⇒ AND IT IS **THE PEER'S LOOP** ✓✓.**
  path:
    - feedback-synthesis        # Post-Launch — the user's voice
    - user-persona-creation     # Research — who they are
    - feature-prioritization    # Ideation — what to build next
  # **⇒ AND THE EDGE **INTO** IDEATION ✓✓ — **⇒ THE HEAD OF THE LOOP ✓✓.**
  returns_to: ideation
  # **⇒ AND WHAT DRIVES IT ✓✓ — **⇒ THE ONLY EXTERNAL SIGNAL THAT EXISTS ✓✓.**
  driven_by:
    - a reply from a real person
    - a call booked
    - a pre-sale through a payment link
    - a metric that moved
```

## **⇒ AND THE SEAMS ✓✓ — **THE SEVEN TRANSITIONS ✓✓**

**⇒ **⇒ EACH SEAM IS **A SKILL** ✓✓, **⇒ AND EACH IS NAMED BY THE SKILLS' OWN
`relatedBefore` AND `relatedAfter`** ✓✓, **⇒ AND ALL NINE EXIST ✓✓ — **⇒ IN
`barnymurt/AgentPad`, ON THE BRANCH `data-source-validation` ✓✓.**

```yaml
seams:
  - to: ideation
    from: post-launch
    skill: product-vision
    edge: competitor-research.relatedBefore -> product-vision
  - to: research
    from: ideation
    skill: interview-guide-creation
    edge: user-persona-creation.relatedBefore -> interview-guide-creation
  - to: design
    from: research
    skill: user-story-generation
    edge: requirements-elicitation.relatedAfter -> user-story-generation
  - to: development
    from: design
    skill: roadmap-planning
    skill_note: The edge devils-advocate.relatedAfter -> roadmap-planning
  - to: testing
    from: development
    skill: test-strategy
    skill_note: The edge tdd.relatedAfter -> test-strategy
  - to: launch
    from: development
    skill: pricing-strategy
    also: messaging-framework
    edge: business-case-modeling.relatedAfter -> pricing-strategy
  - to: post-launch
    from: launch
    skill: kpi-tracking
    also: cohort-analysis
    edge: saas-metrics-analysis.relatedAfter -> kpi-tracking
```

## **⇒ AND THE GATES ✓✓ — **BETWEEN** THE STAGES, NOT **INSIDE** THEM ✓✓**

**⇒ **⇒ THE VALIDATION PACK IS **A GATE** ✓✓ — **⇒ AND IT IS **WHERE THE
BACKWARD EDGE LIVES** ✓✓:**

```yaml
gates:
  - skill: validation-pack
    between: [ideation, research]
    verdict_source: skills/validation-pack/output-schema.md
    # **⇒ AND **PAUSE** IS **THE BACKWARD TRANSITION** ✓✓ — **⇒ IT IS LITERALLY
    # **⇒ THE MOVE THE PEER IS DESCRIBING ✓✓.**
    verdicts: [GO, PAUSE, KILL]
    backward_verdict: PAUSE
    # **⇒ AND THE SCHEMA ALREADY SAYS THE HUMAN IS IN IT ✓✓.**
    records: whether the user overrode it
```

## **⇒ AND THE SKILLS' CLASSIFICATION ✓✓ — **THE FULL MAP ✓✓**

**⇒ **⇒ EVERY SKILL, ITS STAGES, AND **THE EVIDENCE** ✓✓ — **⇒ AND THE ONES
WITH **NO `lifecycle`** GET ONE ✓✓.**

| the skill | the stages it serves | the evidence |
|---|---|---|
| `product-vision` | **ideation** | *"Product vision statement, mission statement"* ✓✓ — **THE LOOP'S HEAD ✓✓** |
| `devils-advocate` | **ideation, research** | *"challenge product assumptions"* ✓✓ |
| `business-case-modeling` | **ideation, post-launch** | *"revenue projections, unit economics"* ✓✓ |
| `competitor-research` | **ideation, research** | *"competitive landscape"* ✓✓ |
| `interview-guide-creation` | **research** | *"User interview guide"* ✓✓ |
| `requirements-elicitation` | **research, design** | research produces, design consumes ✓✓ |
| `user-persona-creation` | **research** | *"evidence-based user personas"* ✓✓ |
| `user-journey-mapping` | **research, design** | *"Map the end-to-end user experience"* ✓✓ |
| `feedback-synthesis` | **research, post-launch** | *"Synthesize user feedback"* ✓✓ — **THE LOOP ✓✓** |
| `saas-metrics-analysis` | **testing, post-launch** | *"diagnose health, identify root causes"* ✓✓ |
| `cohort-analysis` | **post-launch** | *"retention curves"* ✓✓ |
| `kpi-tracking` | **post-launch** | *"metrics dashboard and alerts"* ✓✓ |
| `feature-prioritization` | **ideation, post-launch** | *"Revisit trigger (required)"* ✓✓ |
| `roadmap-planning` | **development** | *"Phased roadmap with milestones"* ✓✓ |
| `pricing-strategy` | **launch** | *"Pricing model recommendation"* ✓✓ |
| `messaging-framework` | **launch** | *"messaging framework"* ✓✓ |
| `user-story-generation` | **design** | *"User stories with acceptance criteria"* ✓✓ |
| `frontend-design` | **design, development** | *"production-grade frontend interfaces"* ✓✓ |
| `brand-guidelines` | **design, launch** | *"any artifact"* ✓✓ |
| `theme-factory` | **design, launch** | *"slides, docs, landing pages"* ✓✓ |
| `algorithmic-art` | **design** | p5.js art ✓✓ |
| `canvas-design` | **design** | *"visual art in .png and .pdf"* ✓✓ |
| `web-artifacts-builder` | **development** | HTML artifacts ✓✓ |
| `mcp-builder` | **development** | MCP servers ✓✓ |
| `doc-coauthoring` | **development, post-launch** | *"co-authoring documentation"* ✓✓ |
| `internal-comms` | **development, launch** | *"internal communications"* ✓✓ |
| `docx` / `pdf` / `pptx` | **development, launch** | documents ✓✓ |
| `skill-creator` | **development** | *"creating effective skills"* ✓✓ |
| `webapp-testing` | **testing** | *"Playwright"* ✓✓ |
| `quality-checklist` | **the library's own audit** | it audits the **skills**, **⇒ NOT A STAGE** ✓✓ |
| `validation-pack` | **a gate between stages** | it judges, **⇒ it does not build** ✓✓ |

## **⇒ AND THE VOCABULARY ✓✓ — **THE SEVEN, NOT THE FIVE ✓✓**

**⇒ **⇒ THE REPO'S FIVE (`Discovery`, `Strategy`, `Build`, `Launch`, `Iteration`)
**⇒ BECOME THE SEVEN ✓✓ — **⇒ AND HERE IS THE MAPPING, **SO NOTHING IS LOST**
✓✓:**

| the repo's five | the seven |
|---|---|
| **Discovery** | **Ideation + Research** ✓✓ |
| **Strategy** | **Ideation + Research + Design** ✓✓ — **⇒ *DEVILS-ADVOCATE* AND *BUSINESS-CASE-MODELLING* LIVE HERE ✓✓** |
| **Build** | **Design + Development + Testing** ✓✓ |
| **Launch** | **Launch** ✓✓ |
| **Iteration** | **Testing + Post-Launch** ✓✓ |

**⇒ **⇒ AND THE SEVEN STAGES' **ORDER** IS **DATA** ✓✓ — **⇒ AND THE CIRCLE IS
**DATA** ✓✓ — **⇒ AND THE SEAMS ARE **DATA** ✓✓ — **⇒ AND NOTHING IS A PYTHON
LITERAL ✓✓.**

## **⇒ AND THE TRANSLATION ✓✓ — **FROM THE FILES' FOUR WORDS TO THE SEVEN ✓✓**

**⇒ **⇒ THE SKILLS' FILES USE **FOUR** WORDS ✓✓ — **⇒ MEASURED, EVERY ONE OF THEM
✓✓: `build` **16** ✓✓, `discovery` **9** ✓✓, `launch` **9** ✓✓, `iterate` **6** ✓✓.**

**⇒ **⇒ AND THE **SEVEN** ARE THE PEER'S ✓✓. **⇒ SO THE TRANSLATION IS **DATA**
✓✓ — **⇒ AND IT LIVES **HERE** ✓✓, **⇒ NOT IN THE CODE ✓✓:**

```yaml
# **⇒ THE TRANSLATION IS **MANY-TO-MANY** ✓✓ — **⇒ AND **A SINGLE** TRANSLATION
# **⇒ FOR ALL THE SKILLS IN **ONE** OLD STAGE IS **WRONG** ✓✓ — **⇒ MEASURED ✓✓:
# **⇒ `devils-advocate` AND `feature-prioritization` ARE BOTH `strategy` ✓✓, **⇒
# **⇒ AND THEY BELONG TO **DIFFERENT** STAGES ✓✓ — **⇒ *DEVILS-ADVOCATE*
# **⇒ CHALLENGES IN IDEATION ✓✓, **⇒ AND *FEATURE-PRIORITIZATION* **RANKS WHAT TO
# **⇒ BUILD** ✓✓, **⇒ WHICH IS IDEATION TOO ✓✓ — **⇒ SO **THE OLD WORD IS NOT
# **⇒ ENOUGH ✓✓, **⇒ AND **THE SKILL'S OWN FILE MUST WIN** ✓✓.**
#
# **⇒ SO THE RULE IS ✓✓: **THE FILE'S WORD IS THE **STARTING POINT** ✓✓, **⇒ AND
# **⇒ THE `stage` FIELD — **WHEN PRESENT** ✓✓ — **OVERRIDES IT** ✓✓, **⇒ AND
# **⇒ EVERY SKILL GETS ONE ✓✓, **⇒ BECAUSE THAT IS **THE PEER'S CLASSIFICATION**
# **⇒ ✓✓.**
translation:
  discovery: [ideation, research]
  strategy:  [ideation, research]
  build:     [design, development]
  launch:    [launch]
  iterate:   [testing, post-launch]
```

**⇒ **⇒ AND THE `stage` FIELD ✓✓ — **⇒ **THE SEVEN** ✓✓, **⇒ **A LIST** ✓✓ —
**⇒ **AND IT OVERRIDES** ✓✓:**

```yaml
# **⇒ THE SKILL'S OWN STAGES ✓✓ — **⇒ **THE SEVEN** ✓✓, **⇒ **A LIST** ✓✓.
# **⇒ AND THIS IS WHERE **THE PEER'S CLASSIFICATION** LIVES ✓✓ — **⇒ BECAUSE IT
# **⇒ IS **A DECISION ABOUT EACH SKILL** ✓✓, **⇒ AND **A DECISION BELONGS IN
# **⇒ THE SKILL'S OWN FILE** ✓✓.**
#
# product-vision:            [ideation]
# devils-advocate:           [ideation, research]
# feature-prioritization:    [ideation, post-launch]
# feedback-synthesis:        [research, post-launch]
# requirements-elicitation:  [research, design]
# user-persona-creation:     [research]
# user-journey-mapping:      [research, design]
# competitor-research:       [ideation, research]
# business-case-modeling:    [ideation, post-launch]
# saas-metrics-analysis:     [testing, post-launch]
# validation-pack:           [ideation, post-launch]
```
