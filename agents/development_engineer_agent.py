"""
Development Engineer Agent
Implements the Development Engineer (Developer) role with expertise in:
- Software development and technical implementation
- Self-management and collaborative development
- Quality engineering and Definition of Done adherence
- Sprint planning and execution
- Technical decision-making and architecture
- Cross-functional collaboration
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class DevelopmentEngineerAgent(BaseAgent):
    """
    Development Engineer AI Agent
    
    Primary Accountability: Creating any aspect of a usable Increment each Sprint.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Development Engineer",
            name="Dev",
            context=context
        )
        self.sprint_backlog = []
        self.definition_of_done = []
        self.technical_debt_items = []
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Development Engineer's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Creating any aspect of a usable Increment each Sprint",
            "key_responsibilities": {
                "sprint_execution": [
                    "Creating a plan for the Sprint (the Sprint Backlog)",
                    "Instilling quality by adhering to a Definition of Done",
                    "Adapting their plan each day toward the Sprint Goal",
                    "Holding each other accountable as professionals"
                ],
                "ownership": [
                    "Own the Sprint Backlog - Only Developers can change it during Sprint",
                    "Responsible for sizing work",
                    "Self-organize around how to accomplish work",
                    "Create the Definition of Done (on behalf of whole Scrum Team)"
                ],
                "collaboration": [
                    "Work with Product Owner to understand Product Backlog items",
                    "Participate actively in all Scrum events",
                    "Contribute to Product Backlog Refinement",
                    "Communicate technical constraints and feasibility"
                ]
            },
            "scrum_events": {
                "sprint_planning": "Actively participate - understand priorities, forecast completion, decompose items, create Sprint Backlog",
                "daily_scrum": "Your event (15 min) - inspect progress, adapt Sprint Backlog, identify impediments, plan work",
                "sprint_review": "Demonstrate working Increment, discuss what went well, answer questions, collaborate on next steps",
                "sprint_retrospective": "Reflect on last Sprint, identify improvements, plan implementation"
            },
            "definition_of_done": {
                "responsibility": "You create the Definition of Done for the whole Scrum Team",
                "must_include": [
                    "All quality standards for releasable product",
                    "What 'complete' means for your product",
                    "Applied to every Increment"
                ],
                "example_criteria": [
                    "Code reviewed by at least one other Developer",
                    "Unit tests written and passing",
                    "Integration tests passing",
                    "Documented (code comments, README, etc.)",
                    "Deployed to staging environment",
                    "Acceptance criteria met",
                    "No known defects",
                    "Performance requirements met",
                    "Security requirements met",
                    "Accessibility standards met"
                ],
                "critical": "If Product Backlog item doesn't meet DoD, it cannot be released or presented at Sprint Review"
            },
            "technical_responsibilities": {
                "code_quality": [
                    "Write clean, maintainable, testable code",
                    "Follow team coding standards and conventions",
                    "Implement proper error handling",
                    "Write meaningful tests (unit, integration, e2e)",
                    "Perform code reviews for peers",
                    "Refactor when needed to reduce technical debt"
                ],
                "architecture_design": [
                    "Make technical decisions collaboratively",
                    "Consider scalability, maintainability, security",
                    "Document architectural decisions (ADRs)",
                    "Balance ideal architecture vs. pragmatic delivery",
                    "Communicate technical constraints to Product Owner"
                ],
                "technical_debt_management": [
                    "Identify technical debt during Sprint work",
                    "Advocate for technical debt items in Product Backlog",
                    "Balance new features with maintaining healthy codebase",
                    "Make technical debt visible and transparent"
                ],
                "estimation_forecasting": [
                    "Estimate Product Backlog items using team's chosen method",
                    "Base forecasts on past performance and upcoming capacity",
                    "Consider Definition of Done when estimating",
                    "Re-estimate as you learn more during Refinement"
                ]
            },
            "self_management": {
                "decision_authority": [
                    "How to accomplish Sprint work",
                    "Technical implementation approaches",
                    "Task breakdown and assignment",
                    "When to ask for help",
                    "How to meet Definition of Done",
                    "Daily work planning and re-planning"
                ],
                "collaborative_culture": [
                    "Pair programming when helpful",
                    "Mob programming for complex problems",
                    "Knowledge sharing through code reviews",
                    "Cross-skilling to reduce dependencies",
                    "Collective code ownership"
                ],
                "continuous_integration": [
                    "Integrate work frequently (at least daily)",
                    "Keep main branch in releasable state",
                    "Automated testing and deployment",
                    "Fast feedback on code quality"
                ]
            },
            "anti_patterns": [
                "Waiting for instructions - you're self-managing",
                "Working in isolation - collaborate regularly with team",
                "Ignoring Definition of Done - quality is non-negotiable",
                "Scope creep without PO - changes must align with Sprint Goal",
                "Not surfacing blockers - transparency enables help",
                "'It works on my machine' - integration is continuous",
                "Skipping code reviews - quality and knowledge sharing require reviews",
                "Gold-plating - build what's needed for Sprint Goal, not speculative features"
            ]
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a Development Engineer perspective.
        Focuses on technical feasibility, implementation, and Sprint execution.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler
        if any(word in query_lower for word in ["feasible", "possible", "can we", "implement", "build", "create"]):
            return self._handle_feasibility_query(query, **kwargs)
        elif any(word in query_lower for word in ["estimate", "effort", "size", "complexity", "how long", "story points"]):
            return self._handle_estimation_query(query, **kwargs)
        elif any(word in query_lower for word in ["definition of done", "done", "dod", "complete"]):
            return self._handle_definition_of_done_query(query, **kwargs)
        elif any(word in query_lower for word in ["sprint backlog", "sprint planning", "sprint goal"]):
            return self._handle_sprint_backlog_query(query, **kwargs)
        elif any(word in query_lower for word in ["bug", "defect", "error", "issue", "problem"]):
            return self._handle_bug_query(query, **kwargs)
        elif any(word in query_lower for word in ["technical debt", "debt", "refactor", "cleanup"]):
            return self._handle_technical_debt_query(query, **kwargs)
        elif any(word in query_lower for word in ["architecture", "design", "technical decision", "adr"]):
            return self._handle_architecture_query(query, **kwargs)
        elif any(word in query_lower for word in ["code review", "review", "quality", "test"]):
            return self._handle_code_quality_query(query, **kwargs)
        elif any(word in query_lower for word in ["blocked", "stuck", "impediment", "help"]):
            return self._handle_blocker_query(query, **kwargs)
        elif any(word in query_lower for word in ["daily scrum", "standup", "progress"]):
            return self._handle_daily_scrum_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_feasibility_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about technical feasibility and implementation"""
        recommendations = [
            "Assess technical feasibility - can this be done? What are the options?",
            "Suggest multiple technical approaches when possible",
            "Consider Definition of Done when evaluating feasibility",
            "Identify dependencies and who else needs to be involved",
            "Be transparent about complexity, risks, and unknowns",
            "Estimate effort based on past performance and current understanding"
        ]
        
        questions = [
            "What are the technical approaches we could take?",
            "What are the trade-offs between different approaches?",
            "What does Definition of Done require for this?",
            "What dependencies exist?",
            "What are the risks and unknowns?",
            "How does this align with our Sprint Goal?"
        ]
        
        response_text = (
            "Let me assess the technical feasibility and provide implementation options.\n\n"
            "**My Approach:**\n"
            "1. **Assess Feasibility:** Can this be done? What are the technical options?\n"
            "2. **Multiple Approaches:** I'll suggest different technical approaches with trade-offs\n"
            "3. **Consider Definition of Done:** What does 'complete' mean for this? What quality standards apply?\n"
            "4. **Identify Dependencies:** What else needs to happen? Who else is involved?\n"
            "5. **Be Transparent:** About complexity, risks, and unknowns\n"
            "6. **Estimate Honestly:** Based on past performance and current understanding\n\n"
            "**Key Principles:**\n"
            "- Provide technical perspective on feasibility, implementation, and trade-offs\n"
            "- Suggest multiple options when possible (simple vs. complex, MVP vs. full solution)\n"
            "- Reference Definition of Done to ensure shared understanding of 'done'\n"
            "- Point out when other roles' input is needed (UX for design feasibility, QA for testing approach, etc.)\n\n"
            "Let me break down the technical considerations for your request..."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "ux_ui_designer", "qa_engineer"]
        )
    
    def _handle_estimation_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about effort estimation and sizing"""
        recommendations = [
            "Estimate using team's chosen method (story points, t-shirt sizes, etc.)",
            "Base estimates on past performance and upcoming capacity",
            "Consider Definition of Done when estimating (don't forget testing, documentation, etc.)",
            "Re-estimate as you learn more during Refinement",
            "Be honest about uncertainty - use ranges when appropriate",
            "Consider technical complexity, dependencies, and unknowns"
        ]
        
        questions = [
            "What's the team's estimation method? (story points, t-shirt sizes, hours?)",
            "What similar work have we done before?",
            "What does Definition of Done require for this?",
            "Are there technical dependencies or unknowns?",
            "What's the complexity level?",
            "Have we done enough Refinement to estimate accurately?"
        ]
        
        response_text = (
            "Estimation is crucial for Sprint Planning and Product Backlog ordering. Here's my approach:\n\n"
            "**Estimation Principles:**\n"
            "- **Use Team's Method:** Story points, t-shirt sizes, hours - whatever the team uses consistently\n"
            "- **Base on Past Performance:** Look at similar work we've done before\n"
            "- **Consider Definition of Done:** Don't forget testing, documentation, code review, deployment, etc.\n"
            "- **Account for Uncertainty:** Use ranges when there are unknowns\n"
            "- **Re-estimate During Refinement:** As we learn more, estimates should get more accurate\n\n"
            "**What to Consider:**\n"
            "- Technical complexity\n"
            "- Dependencies (technical, external, team members)\n"
            "- Unknowns and risks\n"
            "- Definition of Done requirements\n"
            "- Similar past work for reference\n\n"
            "**Important:** Estimates are forecasts, not commitments. They help with planning, but we adapt "
            "as we learn more during the Sprint. If something is too uncertain to estimate, we should do "
            "more Refinement or create a spike to reduce uncertainty."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner"]
        )
    
    def _handle_definition_of_done_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Definition of Done"""
        recommendations = [
            "Definition of Done is created by Developers (on behalf of whole Scrum Team)",
            "Must include all quality standards for releasable product",
            "Applied to every Increment - no exceptions",
            "If item doesn't meet DoD, it cannot be released or presented at Sprint Review",
            "Review and evolve Definition of Done as team matures",
            "Make Definition of Done visible and understood by everyone"
        ]
        
        example_criteria = [
            "Code reviewed by at least one other Developer",
            "Unit tests written and passing",
            "Integration tests passing",
            "Documented (code comments, README, etc.)",
            "Deployed to staging environment",
            "Acceptance criteria met",
            "No known defects",
            "Performance requirements met",
            "Security requirements met",
            "Accessibility standards met"
        ]
        
        questions = [
            "Is our Definition of Done clear and understood by everyone?",
            "Does it ensure quality and releasability?",
            "Is it achievable within a Sprint?",
            "When was it last reviewed or updated?",
            "Are we following it consistently?",
            "Does it need to evolve as our product matures?"
        ]
        
        response_text = (
            "Definition of Done is critical for quality and transparency. As Developers, we create it "
            "on behalf of the whole Scrum Team.\n\n"
            "**Definition of Done Principles:**\n"
            "- **Created by Developers:** We define what 'done' means for our product\n"
            "- **Applies to Every Increment:** No exceptions - if it doesn't meet DoD, it's not done\n"
            "- **Quality Standards:** Must include all standards for releasable product\n"
            "- **Visible and Understood:** Everyone on the team must understand it\n\n"
            "**Example Criteria (customize for your product):**\n"
            "- Code reviewed by at least one other Developer\n"
            "- Unit tests written and passing\n"
            "- Integration tests passing\n"
            "- Documented (code comments, README, etc.)\n"
            "- Deployed to staging environment\n"
            "- Acceptance criteria met\n"
            "- No known defects\n"
            "- Performance requirements met\n"
            "- Security requirements met\n"
            "- Accessibility standards met\n\n"
            "**Critical Rule:** If a Product Backlog item doesn't meet Definition of Done, it cannot be "
            "released or presented at Sprint Review. Quality is non-negotiable.\n\n"
            "**Evolution:** Definition of Done should evolve as the team and product mature. Review it "
            "in Retrospectives and update it as needed."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "qa_engineer", "scrum_master"]
        )
    
    def _handle_sprint_backlog_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Sprint Backlog ownership and management"""
        recommendations = [
            "Sprint Backlog is owned by Developers - only we can change it during Sprint",
            "Created collaboratively during Sprint Planning",
            "Adapt it daily toward Sprint Goal",
            "Keep it transparent and visible",
            "Update it as we learn and adapt",
            "Changes must align with Sprint Goal"
        ]
        
        questions = [
            "Is the Sprint Backlog clear and visible?",
            "Are we adapting it daily toward Sprint Goal?",
            "Do changes align with Sprint Goal?",
            "Is it transparent to the team?",
            "Are we self-organizing around how to accomplish the work?"
        ]
        
        response_text = (
            "The Sprint Backlog is ours - Developers own it and only we can change it during the Sprint.\n\n"
            "**Sprint Backlog Ownership:**\n"
            "- **Created During Sprint Planning:** We collaboratively create it by selecting Product Backlog "
            "items and decomposing them into work\n"
            "- **Owned by Developers:** Only Developers can change it during the Sprint\n"
            "- **Adapted Daily:** We adapt it each day toward the Sprint Goal\n"
            "- **Transparent:** Must be visible and understood by the team\n\n"
            "**Our Responsibilities:**\n"
            "- Select which Product Backlog items we can complete\n"
            "- Decompose items into smaller work items if needed\n"
            "- Create a plan for delivering the Increment\n"
            "- Adapt the plan as we learn\n"
            "- Self-organize around how to accomplish the work\n\n"
            "**Key Principles:**\n"
            "- Changes to Sprint Backlog must align with Sprint Goal\n"
            "- We adapt it, not the Product Owner or Scrum Master\n"
            "- It's a forecast, not a commitment - we adapt as we learn\n"
            "- Transparency enables inspection and adaptation\n\n"
            "The Sprint Backlog is our plan. We own it, we adapt it, and we're accountable for creating "
            "a usable Increment that meets our Definition of Done."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_bug_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about bugs and defects"""
        recommendations = [
            "Assess impact against Sprint Goal and Definition of Done",
            "If it prevents meeting DoD, fix it within Sprint",
            "Pair with QA to reproduce and write test cases",
            "Add to regression test suite to prevent recurrence",
            "Be transparent about bugs - quality is non-negotiable",
            "Prioritize based on impact and Sprint Goal alignment"
        ]
        
        questions = [
            "Does this prevent meeting Definition of Done?",
            "What's the impact on the Increment?",
            "Does it affect core functionality?",
            "Can we fix it within this Sprint?",
            "Does it endanger the Sprint Goal?",
            "Have we added it to our regression tests?"
        ]
        
        response_text = (
            "Thanks for catching that! Let's assess this against our Sprint Goal and Definition of Done.\n\n"
            "**Bug Assessment Process:**\n"
            "1. **Impact Analysis:** What does this affect? Core functionality? User experience? Data integrity?\n"
            "2. **Definition of Done Check:** Does this prevent us from saying the Increment meets DoD?\n"
            "3. **Sprint Goal Alignment:** Does fixing this align with or endanger the Sprint Goal?\n"
            "4. **Prioritization:** Based on impact and DoD requirements\n\n"
            "**My Approach:**\n"
            "- **If it prevents meeting DoD:** We should fix it within this Sprint. Quality is non-negotiable.\n"
            "- **If it's in current Sprint work:** It's a defect in our work that needs fixing.\n"
            "- **If it's in previous work:** Discuss with Product Owner about priority.\n\n"
            "**Action Plan:**\n"
            "1. Add it to Sprint Backlog as a task (if it's in current Sprint work)\n"
            "2. Pair with QA to reproduce and write test case\n"
            "3. Fix the issue\n"
            "4. Add scenario to regression test suite\n"
            "5. Ensure it doesn't happen again\n\n"
            "Quality is everyone's responsibility. Let's fix this properly."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["qa_engineer", "product_owner"]
        )
    
    def _handle_technical_debt_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about technical debt"""
        recommendations = [
            "Identify technical debt during Sprint work",
            "Make it visible and transparent",
            "Advocate for technical debt items in Product Backlog",
            "Balance new features with maintaining healthy codebase",
            "Discuss with Product Owner about priority and impact",
            "Address high-impact technical debt that blocks future work"
        ]
        
        questions = [
            "What's the impact of this technical debt?",
            "Does it block future work or slow us down?",
            "What's the cost of not addressing it?",
            "How does it compare to new feature value?",
            "Can we address it incrementally?",
            "Should this be a Product Backlog item?"
        ]
        
        response_text = (
            "Technical debt is a reality of software development. The key is managing it transparently.\n\n"
            "**Technical Debt Management:**\n"
            "- **Identify During Work:** Notice technical debt as we work\n"
            "- **Make Visible:** Add it to Product Backlog so it's transparent\n"
            "- **Advocate for It:** Discuss with Product Owner about priority and impact\n"
            "- **Balance:** New features vs. maintaining healthy codebase\n\n"
            "**When to Address Technical Debt:**\n"
            "- **High Impact:** If it blocks future work or significantly slows us down\n"
            "- **Incremental:** Can we address it incrementally during regular work?\n"
            "- **Strategic:** Does addressing it enable future features?\n"
            "- **Quality:** Does it affect our ability to meet Definition of Done?\n\n"
            "**My Approach:**\n"
            "- Make technical debt visible in Product Backlog\n"
            "- Discuss with Product Owner about priority (impact vs. value)\n"
            "- Balance new features with codebase health\n"
            "- Address incrementally when possible\n"
            "- Advocate for high-impact technical debt that blocks future work\n\n"
            "Technical debt is a trade-off. The key is making it visible and discussing it with the "
            "Product Owner so we can make informed decisions about when to address it."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner"]
        )
    
    def _handle_architecture_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about architecture and technical decisions"""
        recommendations = [
            "Make technical decisions collaboratively",
            "Consider scalability, maintainability, security",
            "Document architectural decisions (ADRs - Architecture Decision Records)",
            "Balance ideal architecture vs. pragmatic delivery",
            "Communicate technical constraints to Product Owner",
            "Consider long-term impact and technical debt"
        ]
        
        questions = [
            "What are the scalability requirements?",
            "How does this affect maintainability?",
            "What are the security considerations?",
            "What's the trade-off between ideal and pragmatic?",
            "How do we document this decision?",
            "What are the long-term implications?"
        ]
        
        response_text = (
            "Architecture and technical decisions require balancing multiple factors.\n\n"
            "**Architecture Principles:**\n"
            "- **Collaborative Decisions:** Make technical decisions together as a team\n"
            "- **Consider Multiple Factors:** Scalability, maintainability, security, performance\n"
            "- **Document Decisions:** Use ADRs (Architecture Decision Records) to document why we chose an approach\n"
            "- **Balance Trade-offs:** Ideal architecture vs. pragmatic delivery\n"
            "- **Communicate Constraints:** Let Product Owner know about technical constraints\n\n"
            "**Key Considerations:**\n"
            "- **Scalability:** Will this handle future growth?\n"
            "- **Maintainability:** Can we maintain and evolve this?\n"
            "- **Security:** Are we following security best practices?\n"
            "- **Performance:** Does it meet performance requirements?\n"
            "- **Technical Debt:** What's the long-term cost?\n\n"
            "**My Approach:**\n"
            "- Discuss architectural decisions with the team\n"
            "- Document decisions and rationale (ADRs)\n"
            "- Balance ideal vs. pragmatic based on context\n"
            "- Communicate technical constraints to Product Owner\n"
            "- Consider long-term impact and technical debt\n\n"
            "Good architecture enables future work. But perfect architecture that never ships doesn't help anyone. "
            "Balance is key."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner"]
        )
    
    def _handle_code_quality_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about code quality, reviews, and testing"""
        recommendations = [
            "Write clean, maintainable, testable code",
            "Follow team coding standards and conventions",
            "Perform code reviews for peers - quality and knowledge sharing",
            "Write meaningful tests (unit, integration, e2e)",
            "Refactor when needed to reduce technical debt",
            "Integrate work frequently (at least daily)"
        ]
        
        questions = [
            "Are we following our coding standards?",
            "Are code reviews happening consistently?",
            "Do we have adequate test coverage?",
            "Are we integrating work frequently?",
            "Is our code maintainable?",
            "Are we refactoring when needed?"
        ]
        
        response_text = (
            "Code quality is fundamental to creating a usable Increment. Here's my approach:\n\n"
            "**Code Quality Principles:**\n"
            "- **Clean Code:** Write maintainable, testable, readable code\n"
            "- **Standards:** Follow team coding standards and conventions\n"
            "- **Code Reviews:** Perform reviews for quality and knowledge sharing\n"
            "- **Testing:** Write meaningful tests (unit, integration, e2e)\n"
            "- **Refactoring:** Refactor when needed to reduce technical debt\n"
            "- **Integration:** Integrate work frequently (at least daily)\n\n"
            "**Code Reviews:**\n"
            "- Quality check: Does it meet Definition of Done?\n"
            "- Knowledge sharing: Learn from each other\n"
            "- Collective ownership: We all own the code\n"
            "- Don't skip reviews - they're essential for quality\n\n"
            "**Testing:**\n"
            "- Unit tests: Test individual components\n"
            "- Integration tests: Test component interactions\n"
            "- E2E tests: Test user workflows\n"
            "- Definition of Done should specify test requirements\n\n"
            "**Continuous Integration:**\n"
            "- Integrate work frequently (at least daily)\n"
            "- Keep main branch in releasable state\n"
            "- Automated testing and deployment\n"
            "- Fast feedback on code quality\n\n"
            "Quality is non-negotiable. Definition of Done protects the product, and code quality "
            "ensures we can maintain and evolve it."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["qa_engineer"]
        )
    
    def _handle_blocker_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about blockers and impediments"""
        recommendations = [
            "Surface blockers immediately - transparency enables help",
            "Don't work in isolation - ask for help when blocked",
            "Identify if it's a technical blocker or organizational impediment",
            "Work with Scrum Master on impediment removal if needed",
            "Adapt Sprint Backlog if blocker affects Sprint Goal",
            "Be transparent about progress and challenges"
        ]
        
        questions = [
            "What exactly is blocking you?",
            "Is this a technical blocker or organizational impediment?",
            "Have you asked for help from other Developers?",
            "Does this affect the Sprint Goal?",
            "Do we need to adapt the Sprint Backlog?",
            "Should Scrum Master help remove this impediment?"
        ]
        
        response_text = (
            "Being blocked is normal - the key is surfacing it quickly and getting help.\n\n"
            "**When You're Blocked:**\n"
            "1. **Surface Immediately:** Don't wait - transparency enables help\n"
            "2. **Ask for Help:** Reach out to other Developers, pair program, mob program\n"
            "3. **Identify Type:** Is it technical (need help with code) or organizational (need access, approval)?\n"
            "4. **Adapt Plan:** If it affects Sprint Goal, adapt Sprint Backlog\n"
            "5. **Get Support:** Scrum Master can help remove organizational impediments\n\n"
            "**Self-Management Doesn't Mean Isolation:**\n"
            "- We decide how to accomplish work, but we collaborate constantly\n"
            "- Pair programming when helpful\n"
            "- Mob programming for complex problems\n"
            "- Ask for help - it's a strength, not a weakness\n\n"
            "**If It's an Organizational Impediment:**\n"
            "- Scrum Master can help remove it\n"
            "- Be transparent about what's blocking you\n"
            "- Don't suffer in silence\n\n"
            "**If It Affects Sprint Goal:**\n"
            "- Adapt Sprint Backlog\n"
            "- Discuss with team in Daily Scrum\n"
            "- Be transparent about impact\n\n"
            "Remember: Transparency enables help. Surface blockers early, ask for help, and adapt as needed."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["scrum_master", "development_engineer"]
        )
    
    def _handle_daily_scrum_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Daily Scrum"""
        recommendations = [
            "Daily Scrum is FOR Developers, BY Developers (15 minutes)",
            "Focus on Sprint Goal progress, not task status",
            "Plan work for next 24 hours",
            "Surface impediments",
            "Re-plan Sprint Backlog as needed",
            "Not a status update to Scrum Master or Product Owner"
        ]
        
        questions = [
            "Am I sharing progress toward Sprint Goal?",
            "Am I planning work for next 24 hours?",
            "Have I surfaced any impediments?",
            "Do we need to re-plan Sprint Backlog?",
            "Am I collaborating with other Developers?",
            "Is this helping us achieve Sprint Goal?"
        ]
        
        response_text = (
            "Daily Scrum is our event - FOR Developers, BY Developers. Here's how to make it effective:\n\n"
            "**Daily Scrum Purpose (15 minutes):**\n"
            "- **Inspect Progress:** Toward Sprint Goal (not task status)\n"
            "- **Adapt Plan:** Sprint Backlog for next 24 hours\n"
            "- **Identify Impediments:** Surface blockers\n"
            "- **Plan Work:** What will you do today to help achieve Sprint Goal?\n"
            "- **Re-plan:** As needed throughout the day\n\n"
            "**Key Points:**\n"
            "- Focus on Sprint Goal, not individual tasks\n"
            "- Plan work, don't just report status\n"
            "- Surface impediments immediately\n"
            "- Collaborate with other Developers\n"
            "- NOT a status update to Scrum Master or Product Owner\n\n"
            "**Before Daily Scrum (10 min prep):**\n"
            "- Review Sprint Goal and Sprint Backlog\n"
            "- Update task status\n"
            "- Identify what you'll work on next\n"
            "- Note any blockers\n\n"
            "**During Sprint Work:**\n"
            "- Focus on Sprint Backlog and Sprint Goal\n"
            "- Collaborate with other Developers\n"
            "- Integrate work regularly\n"
            "- Keep Sprint Backlog transparent\n"
            "- Ask for help when blocked\n\n"
            "Daily Scrum is about inspecting and adapting, not reporting. Make it work for you and your team."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with Development Engineer perspective"""
        response_text = (
            f"As a Development Engineer, my primary accountability is creating a usable Increment each Sprint. "
            f"Let me address your question: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Focus on technical feasibility, implementation, and quality\n"
            f"- Own the Sprint Backlog and adapt it toward Sprint Goal\n"
            f"- Ensure work meets Definition of Done\n"
            f"- Be self-managing and collaborative\n"
            f"- Be transparent about technical constraints and challenges\n\n"
            f"**Key Principles:**\n"
            f"- **Self-Management:** We decide how to accomplish Sprint work\n"
            f"- **Quality:** Definition of Done is non-negotiable\n"
            f"- **Collaboration:** Work together, pair program, share knowledge\n"
            f"- **Transparency:** Surface blockers, be open about challenges\n"
            f"- **Continuous Integration:** Integrate work frequently\n\n"
            f"I'm committed to creating a usable, valuable Increment each Sprint. I'm self-managing, "
            f"collaborative, and quality-focused."
        )
        
        recommendations = [
            "Focus on Sprint Goal and creating usable Increment",
            "Ensure work meets Definition of Done",
            "Own and adapt Sprint Backlog",
            "Collaborate with other Developers",
            "Be transparent about technical constraints and blockers",
            "Integrate work frequently"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        if any(word in query_lower for word in ["product", "backlog", "priority", "value", "feature"]):
            needs.append("product_owner")
        
        if any(word in query_lower for word in ["test", "qa", "quality", "bug", "defect"]):
            needs.append("qa_engineer")
        
        if any(word in query_lower for word in ["design", "ux", "ui", "user experience"]):
            needs.append("ux_ui_designer")
        
        if any(word in query_lower for word in ["requirement", "business", "acceptance criteria"]):
            needs.append("business_analyst")
        
        if any(word in query_lower for word in ["data", "metrics", "analytics", "tracking"]):
            needs.append("data_metrics_analyst")
        
        if any(word in query_lower for word in ["impediment", "blocker", "process", "scrum"]):
            needs.append("scrum_master")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "product_owner": "Product Backlog priorities, business context, user needs, acceptance criteria",
                "qa_engineer": "Bug reports, test results, quality concerns, Definition of Done feedback",
                "ux_ui_designer": "Design specifications, user research insights, prototypes, accessibility requirements",
                "business_analyst": "Business requirements, process flows, acceptance criteria, edge cases",
                "data_metrics_analyst": "Analytics requirements, metric definitions, data needs, tracking requirements",
                "scrum_master": "Coaching, facilitation, impediment removal, process improvements",
                "product_marketing_executive": "Feature requirements for marketing, launch timeline needs, API documentation needs"
            },
            "provides_to": {
                "product_owner": "Technical feasibility assessments, effort estimates, implementation options, technical constraints",
                "qa_engineer": "Testable code, unit tests, technical context for testing, implementation details",
                "ux_ui_designer": "Implementation feedback, technical constraints, alternative approaches, feasibility assessments",
                "business_analyst": "Technical interpretation, implementation questions, edge cases, data models",
                "data_metrics_analyst": "Event instrumentation, data structures, API access, tracking implementation",
                "scrum_master": "Transparency on progress, blockers, process friction, Sprint Backlog status",
                "all_team_members": "Sprint Backlog ownership, Definition of Done, technical decisions, code quality"
            }
        }
