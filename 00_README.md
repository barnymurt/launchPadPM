# SCRUM TEAM AI AGENTS - IMPLEMENTATION GUIDE

## Overview

This collection contains 8 specialized AI agent prompts designed to function as members of a Scrum product development team. Each agent has deep knowledge of Scrum methodology, Continuous Discovery Habits, Opportunity Solution Trees, and their specific role responsibilities.

## Key Features

✅ **Scrum-Compliant:** All agents are based on the 2020 Scrum Guide  
✅ **Continuous Discovery:** Integrated Teresa Torres' Continuous Discovery Habits framework  
✅ **Cross-Functional Awareness:** Agents know how to collaborate with each other  
✅ **Evidence-Based:** Emphasize empirical decision-making and data-driven choices  
✅ **Practical Implementation:** Include daily rituals, anti-patterns, and real-world examples

## The Team

### Core Scrum Team Roles

1. **Product Owner** (`01_Product_Owner_Agent.md`)
   - Maximizes product value
   - Manages Product Backlog
   - Conducts continuous discovery (weekly customer interviews)
   - Uses Opportunity Solution Trees (OST) framework
   - Evidence-based prioritization

2. **Scrum Master** (`02_Scrum_Master_Agent.md`)
   - Ensures Scrum Team effectiveness
   - Servant leadership and facilitation
   - Removes impediments
   - Coaches team on Scrum practices
   - Organizational change agent

3. **Development Engineer** (`03_Development_Engineer_Agent.md`)
   - Creates usable Increment each Sprint
   - Technical implementation expertise
   - Self-managing and collaborative
   - Owns Sprint Backlog
   - Quality through Definition of Done

### Specialized Developer Roles

4. **QA Engineer** (`04_QA_Engineer_Agent.md`)
   - Quality assurance and testing
   - Definition of Done enforcement
   - Test automation and manual testing
   - Defect management
   - Shift-left quality advocacy

5. **Business Analyst** (`05_Business_Analyst_Agent.md`)
   - Requirements analysis and documentation
   - Acceptance criteria definition
   - Stakeholder communication
   - Business process modeling
   - Edge case identification

6. **Data/Metrics Analyst** (`06_Data_Metrics_Analyst_Agent.md`)
   - Product analytics and instrumentation
   - North Star Metric and AARRR framework
   - A/B testing and experimentation
   - User behavior analysis
   - Evidence-based decision support

7. **UX/UI Designer** (`07_UX_UI_Designer_Agent.md`)
   - User experience and interface design
   - User research and usability testing
   - Design systems and prototyping
   - Accessibility (WCAG 2.1 Level AA)
   - Design-development collaboration

### Stakeholder Role

8. **Product Marketing Executive** (`08_Product_Marketing_Executive_Agent.md`)
   - Go-to-market strategy
   - Product positioning and messaging
   - Customer acquisition and lifecycle marketing
   - Competitive intelligence
   - Launch planning and execution

## How to Use in Cursor

### Method 1: Custom Instructions (Recommended)

1. **For Each Role:**
   - Open the relevant `.md` file
   - Copy the entire contents
   - In Cursor, open Settings → Features → Custom Instructions
   - Paste the agent prompt as custom instructions
   - Save with a clear name (e.g., "Scrum - Product Owner")

2. **Switching Between Roles:**
   - Create separate Cursor profiles or workspace settings
   - Switch context based on the question type
   - Use @-mentions or chat prefixes to specify role

### Method 2: Context Files

1. **Add to Project:**
   - Place relevant agent `.md` files in your project `.cursor/` directory
   - Reference them in conversations: "Using the Product Owner agent guidelines, help me prioritize these features"

2. **Direct Prompting:**
   - Start conversations with: "You are acting as the [Role] agent from the Scrum team. [Paste key sections]"

### Method 3: Multi-Agent Workflow

**For Complex Questions:**

1. **Ask the appropriate specialist first:**
   - "As the Product Owner agent, should we prioritize dark mode?"
   
2. **Get cross-functional input:**
   - "What would the UX Designer agent say about this?"
   - "What does the Data Analyst agent need to measure this?"

3. **Synthesize perspectives:**
   - Each agent provides their specialized view
   - Product Owner makes final prioritization
   - Scrum Master facilitates if conflicts arise

## Shared Knowledge Base

All agents have access to:

### Scrum Framework
- Three Pillars: Transparency, Inspection, Adaptation
- Five Values: Commitment, Courage, Focus, Openness, Respect
- Scrum Events: Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective
- Scrum Artifacts: Product Backlog, Sprint Backlog, Increment
- Definition of Done

### Continuous Discovery
- Weekly customer interviews (story-based)
- Opportunity Solution Trees (OST)
  - Outcome → Opportunities → Solutions → Assumptions
- Evidence-based decision making
- Assumption testing frameworks

### Product Metrics
- North Star Metric
- AARRR Framework (Acquisition, Activation, Retention, Revenue, Referral)
- Outcome-based measurement

## Cross-Team Collaboration

Each agent understands:

**Information Flow:**
- What they receive from other roles
- What they provide to other roles
- When to collaborate vs. when to decide independently

**Example:**
```
User asks Developer: "Should we add this feature?"

Developer Agent: "From a technical perspective, this is feasible 
and would take about 2 Sprints. However, this should be prioritized 
by the Product Owner based on user value. I'd recommend:
1. Product Owner: validate with customer interviews
2. Data Analyst: check if users are requesting this
3. UX Designer: assess usability implications
4. Then we can estimate accurately in Refinement."
```

## Common Use Cases

### Feature Prioritization
1. **Ask Product Owner:** Overall value and priority
2. **Ask Data Analyst:** Usage data and user behavior
3. **Ask UX Designer:** User research insights
4. **Ask Developer:** Technical feasibility and effort
5. **Ask Business Analyst:** Requirements clarity

### Sprint Planning
1. **Scrum Master:** Facilitates the event
2. **Product Owner:** Explains Product Backlog items
3. **Developers (all roles):** Collaborate on Sprint Backlog

### Bug Found
1. **QA Engineer:** Documents and assesses severity
2. **Developer:** Evaluates technical fix
3. **Product Owner:** Decides priority (Sprint vs. Backlog)
4. **Scrum Master:** Removes impediments if blocking

### Design Decision
1. **UX Designer:** Creates design options
2. **Product Owner:** Validates against user needs
3. **Developer:** Assesses implementation complexity
4. **Data Analyst:** Proposes A/B test to validate
5. **QA Engineer:** Plans testing approach

### Launch Planning
1. **Product Marketing:** Develops GTM strategy
2. **Product Owner:** Confirms feature readiness
3. **QA Engineer:** Validates quality standards
4. **Data Analyst:** Sets up tracking and metrics
5. **UX Designer:** Ensures onboarding experience

## Best Practices

### DO:
✅ Use agents for their specialized expertise  
✅ Encourage cross-functional collaboration  
✅ Base decisions on evidence and data  
✅ Respect Scrum roles and accountabilities  
✅ Focus on outcomes, not outputs  
✅ Iterate based on feedback  

### DON'T:
❌ Let one agent make all decisions  
❌ Skip user research and validation  
❌ Ignore Definition of Done  
❌ Create handoff waterfalls  
❌ Forget accessibility requirements  
❌ Prioritize without evidence  

## Troubleshooting

**Q: Agent responses conflict - what do I do?**
A: This is healthy! Different perspectives surface important trade-offs. The Product Owner has final accountability for product decisions, but should consider all input.

**Q: Agent doesn't know about my specific product**
A: Add product context in your question: "For a B2B SaaS invoicing tool, as the Product Owner agent, how would you..."

**Q: Agent is too verbose**
A: Ask for concise responses: "Give me the 3 most important points as the Data Analyst agent"

**Q: I need multiple perspectives at once**
A: Ask explicitly: "I need perspectives from Product Owner, UX Designer, and Data Analyst on whether to add social login"

## Customization

Each agent prompt can be customized:

1. **Add Product-Specific Context:**
   - Industry-specific knowledge
   - Company values and culture
   - Specific tools and technologies

2. **Adjust Tone:**
   - More formal/casual
   - Different communication style
   - Language preferences

3. **Add Domain Expertise:**
   - Healthcare compliance
   - Financial regulations
   - Industry-specific standards

4. **Modify Frameworks:**
   - Different prioritization methods
   - Alternative metrics frameworks
   - Custom processes

## Version History

**Version 1.0** (January 2026)
- Initial release
- Based on 2020 Scrum Guide
- Integrated Continuous Discovery Habits
- Integrated Opportunity Solution Trees framework
- 8 specialized role agents

## Credits & Sources

**Frameworks:**
- Scrum Guide 2020 (Schwaber & Sutherland)
- Continuous Discovery Habits (Teresa Torres)
- Opportunity Solution Trees (Teresa Torres)
- AARRR Metrics (Dave McClure)

**Created by:** Claude (Anthropic)  
**Project Knowledge Base:** Comprehensive Scrum and product development resources

## Support & Feedback

These agents are designed to be starting points. Adapt them to your specific context, and iterate based on what works for your team!

---

**Ready to get started?**

1. Pick the role you need first (usually Product Owner)
2. Load the agent prompt into Cursor
3. Start asking questions!
4. Iterate and improve based on results

Remember: These agents embody best practices, but you should adapt them to your specific product, team, and organizational context.
