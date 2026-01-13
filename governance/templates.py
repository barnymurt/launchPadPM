"""
Governance Templates
Documentation templates for all governance requirements.
"""

# README.md Template
README_TEMPLATE = """# [Project Name]

## Overview
[One paragraph: what this does and why]

## Quick Start
```bash
git clone [repo-url]
npm install
cp .env.example .env
npm run dev
npm test
```

## Architecture
- Frontend: [Tech]
- Backend: [Tech]
- Database: [Tech]
[Link to ARCHITECTURE.md]

## Development
### Prerequisites
- Node.js v18+
- PostgreSQL 14+

### Environment Variables
See `.env.example`

### Common Commands
```bash
npm run dev          # Start dev
npm run build        # Build
npm run test         # Test
npm run lint         # Lint
```

## Deployment
[Link to docs or describe]

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [API](docs/API.md)
- [ADRs](docs/adr/)
"""

# PROJECT_BRIEF.md Template
PROJECT_BRIEF_TEMPLATE = """# Project Brief: [Name]

**Last Updated:** [Date]

## Business Context
- Problem: [What we're solving]
- Users: [Who for]
- Business Model: [How we make money]
- Competition: [Key competitors]

## Product Goal
[One sentence goal]

Progress: [Current vs. Target]

Key Metrics:
- North Star: [Metric] = [Value]
- Acquisition: [Metric]
- Retention: [Metric]

## Current Sprint
Sprint [#]: [Dates]
Sprint Goal: [Goal]

Top Priorities:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Key Stakeholders
- Product Owner: [Name]
- Tech Lead: [Name]

## Technical Context
- Stack: [Technologies]
- Integrations: [Key integrations]
- Constraints: [Major constraints]

## Quick Links
- Production: [URL]
- Staging: [URL]
- Metrics: [URL]
- Designs: [URL]

## Recent Changes
Last Sprint:
- [Change 1]
- [Change 2]

Last Retro Insights:
- Went well: [Point]
- To improve: [Point]
"""

# ADR Template (MADR format)
ADR_TEMPLATE = """# [Decision Title]

- Status: [accepted/rejected/deprecated]
- Date: [YYYY-MM-DD]
- Deciders: [People involved]

## Context and Problem
[2-3 sentences describing problem]

## Decision Drivers
* [Driver 1: cost, performance, etc.]
* [Driver 2]

## Considered Options
* [Option 1]
* [Option 2]

## Decision Outcome
Chosen: "[Option 1]" because [justification]

### Consequences
* Good: [Positive]
* Bad: [Negative]

## Pros and Cons

### [Option 1]
* Good: [Argument]
* Bad: [Argument]

### [Option 2]
* Good: [Argument]
* Bad: [Argument]
"""

# CHANGELOG.md Template
CHANGELOG_TEMPLATE = """# Changelog

## [Unreleased]
### Added
- [Feature]

### Changed
- [Change]

### Fixed
- [Fix]

## [1.2.0] - 2026-01-15
### Added
- Invoice discount feature
- Bulk operations

### Fixed
- Tax calculation rounding
"""

# User Story Ticket Template
USER_STORY_TEMPLATE = """## User Story
As a [user type]
I want to [action]
So that [benefit]

## Business Context
Why valuable: [Explanation]
RICE Score: [Calculated score]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Design
Mockups: [Link]

## Technical Notes
Approach: [High-level]
Dependencies: [List]
Edge cases: [List]

## Estimate
Story Points: [Estimate]
Breakdown:
- Design: [time]
- Dev: [time]
- Test: [time]

## Definition of Done
- [ ] Code reviewed
- [ ] Tests passing (>80%)
- [ ] Accessibility tested
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] QA approved
"""

# Bug Report Template
BUG_REPORT_TEMPLATE = """## Bug Report

### Severity
[Critical/High/Medium/Low]

### Environment
- [ ] Production
- [ ] Staging
Browser: [Chrome 118]
OS: [macOS 14]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Result
[What should happen]

### Actual Result
[What actually happens]

### Evidence
Screenshots: [Attach]
Console errors: [Paste]
Logs: [Paste]

### Impact
Users affected: [Number]
Workaround: [Yes/No - describe]

### Proposed Fix
[If known]
"""

# Project Onboarding Checklist
ONBOARDING_CHECKLIST = """# Project Onboarding Checklist

**Time Budget: 30-45 minutes**

When starting work on ANY project (even returning):

- [ ] Read PROJECT_BRIEF.md (current state, goals, context)
- [ ] Review current Sprint Goal
- [ ] Check Product Backlog top 5 items
- [ ] Review Definition of Done (universal + project-specific)
- [ ] Read recent Retrospective notes
- [ ] Check ARCHITECTURE.md (system structure)
- [ ] Review recent ADRs (recent decisions)
- [ ] Check CHANGELOG.md (what changed)
- [ ] Skim open tickets/PRs (current work)
- [ ] Review key metrics dashboard (current state)
"""
