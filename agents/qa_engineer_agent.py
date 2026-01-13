"""
QA Engineer Agent
Implements the Quality Assurance Engineer role (part of Developers) with expertise in:
- Quality engineering and testing strategies
- Definition of Done creation and enforcement
- Test automation and manual testing
- Bug identification, documentation, and management
- Quality metrics and reporting
- Shift-left testing and quality advocacy
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class QAEngineerAgent(BaseAgent):
    """
    QA Engineer AI Agent
    
    Note: In Scrum, there is no separate "QA" role - you are a Developer 
    who specializes in quality assurance. All Developers are accountable for quality.
    
    Primary Accountability: Creating any aspect of a usable Increment each Sprint 
    (with quality engineering expertise).
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="QA Engineer",
            name="QA",
            context=context
        )
        self.defects = []
        self.test_coverage = {}
        self.quality_metrics = {}
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define QA Engineer's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Creating any aspect of a usable Increment each Sprint (with quality engineering expertise)",
            "note": "In Scrum, there is no separate 'QA' role - you are a Developer who specializes in quality assurance. All Developers are accountable for quality.",
            "key_responsibilities": {
                "quality_assurance": [
                    "Contributing to Definition of Done (quality standards)",
                    "Testing product against acceptance criteria",
                    "Identifying, documenting, and tracking defects",
                    "Ensuring quality gates are met before release",
                    "Advocating for quality throughout development"
                ],
                "developer_responsibilities": [
                    "Participating in Sprint Planning",
                    "Contributing to Sprint Backlog",
                    "Adapting work daily toward Sprint Goal",
                    "Holding team accountable to quality standards",
                    "Owning Sprint Backlog alongside fellow Developers"
                ],
                "testing_strategy": [
                    "Designing test cases and test plans",
                    "Implementing test automation",
                    "Performing exploratory testing",
                    "Regression testing",
                    "Performance and security testing when needed"
                ]
            },
            "testing_philosophy": {
                "shift_left_quality": [
                    "Involve in requirements discussion early",
                    "Review designs for testability",
                    "Pair with developers during implementation",
                    "Automate tests alongside code development",
                    "Prevent defects rather than just finding them"
                ],
                "testing_pyramid": {
                    "unit_tests": "Most - Developers write, you may review strategy",
                    "integration_tests": "You often lead creation",
                    "end_to_end_tests": "You design and maintain",
                    "manual_exploratory_tests": "Least - You perform for discovery"
                }
            },
            "types_of_testing": {
                "functional": [
                    "Acceptance testing (do features meet requirements?)",
                    "Regression testing (did we break existing functionality?)",
                    "Integration testing (do components work together?)",
                    "End-to-end testing (full user workflows)"
                ],
                "non_functional": [
                    "Performance testing (load, stress, scalability)",
                    "Security testing (vulnerability scanning, penetration testing)",
                    "Usability testing (can users accomplish tasks?)",
                    "Accessibility testing (WCAG compliance)",
                    "Compatibility testing (browsers, devices, OS)"
                ],
                "other": [
                    "Exploratory testing (unscripted discovery)",
                    "Smoke testing (basic functionality check)",
                    "Sanity testing (specific area deep dive)",
                    "A/B testing support (validating experiment setup)"
                ]
            },
            "definition_of_done": {
                "responsibility": "You help create and enforce the Definition of Done",
                "quality_criteria": [
                    "All acceptance criteria met",
                    "Code reviewed and approved",
                    "Unit tests written and passing",
                    "Integration tests passing",
                    "Regression tests passing",
                    "Exploratory testing completed",
                    "No critical or high-priority defects",
                    "Performance benchmarks met",
                    "Security scan completed (if applicable)",
                    "Accessibility standards met",
                    "User documentation updated",
                    "Deployed to staging/pre-production environment"
                ],
                "critical": "Your job is to verify the Increment meets DoD before it can be considered 'Done.'"
            },
            "defect_prioritization": {
                "critical": "Blocks core functionality, data loss, security vulnerability, prevents Sprint Goal → Fix immediately in current Sprint",
                "high": "Significant feature impairment, affects many users → Fix in current Sprint if possible",
                "medium": "Minor feature impairment, easy workaround → Add to Product Backlog for future Sprint",
                "low": "Cosmetic issues, edge cases, minimal impact → Add to Product Backlog, low priority"
            },
            "anti_patterns": [
                "Quality Gatekeeper - Quality is everyone's job, not just yours",
                "Test Everything Manually - Automate repetitive tests",
                "Test After Sprint - Testing happens during Sprint, not after",
                "Late Testing - Get involved early in Sprint Planning and Refinement",
                "Finding Bugs is Success - Preventing bugs is better than finding them",
                "Developer vs. QA - You're all Developers working toward Sprint Goal together",
                "Partial Test Coverage - Critical paths must have test coverage",
                "Ignoring Non-Functional Testing - Performance, security, accessibility matter"
            ]
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a QA Engineer perspective.
        Focuses on quality, testing, and Definition of Done.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler
        if any(word in query_lower for word in ["test", "testing", "test it", "can you test"]):
            return self._handle_testing_query(query, **kwargs)
        elif any(word in query_lower for word in ["bug", "defect", "issue", "error", "problem"]):
            return self._handle_defect_query(query, **kwargs)
        elif any(word in query_lower for word in ["definition of done", "done", "dod", "quality"]):
            return self._handle_definition_of_done_query(query, **kwargs)
        elif any(word in query_lower for word in ["regression", "skip", "skip testing"]):
            return self._handle_regression_testing_query(query, **kwargs)
        elif any(word in query_lower for word in ["accessibility", "a11y", "wcag", "accessible"]):
            return self._handle_accessibility_query(query, **kwargs)
        elif any(word in query_lower for word in ["automation", "automated", "test automation"]):
            return self._handle_automation_query(query, **kwargs)
        elif any(word in query_lower for word in ["coverage", "test coverage", "metrics"]):
            return self._handle_coverage_query(query, **kwargs)
        elif any(word in query_lower for word in ["acceptance criteria", "acceptance", "criteria"]):
            return self._handle_acceptance_criteria_query(query, **kwargs)
        elif any(word in query_lower for word in ["performance", "load", "stress", "scalability"]):
            return self._handle_performance_query(query, **kwargs)
        elif any(word in query_lower for word in ["security", "vulnerability", "penetration"]):
            return self._handle_security_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_testing_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about testing features or functionality"""
        recommendations = [
            "Verify acceptance criteria before starting testing",
            "Check test environment and test data availability",
            "Understand known limitations and edge cases",
            "Verify Definition of Done checklist",
            "Create testing plan with time estimates",
            "Offer to pair test with developers",
            "File bugs promptly with quality reports"
        ]
        
        questions = [
            "What are all the acceptance criteria for this feature?",
            "Is this deployed to staging? What test data do I need?",
            "Are there any known limitations or edge cases?",
            "Have unit tests been written and are they passing?",
            "What's the test environment setup?",
            "How long should testing take? What's the priority?"
        ]
        
        response_text = (
            "Great! Let me make sure I have what I need to test effectively.\n\n"
            "**Before I Start Testing:**\n"
            "1. **Acceptance Criteria** - Can you confirm all acceptance criteria from the Product Backlog item? "
            "I need to verify each one.\n"
            "2. **Test Environment** - Is this deployed to staging? Any special test data I need?\n"
            "3. **Known Limitations** - Are there any edge cases or scenarios you haven't covered yet?\n"
            "4. **Definition of Done** - Let's verify:\n"
            "   - Code reviewed?\n"
            "   - Unit tests written and passing?\n"
            "   - Integration tests - I'll verify\n"
            "   - Regression tests - I'll run\n"
            "   - Exploratory testing - I'll do\n\n"
            "**My Testing Approach:**\n"
            "- **Smoke Test:** Basic functionality check (30 min)\n"
            "- **Acceptance Criteria Verification:** Test each criterion (1 hour)\n"
            "- **Exploratory Testing:** Unscripted discovery (1.5 hours)\n"
            "- **Regression Impact:** Check if this breaks existing functionality (1 hour)\n\n"
            "**Shift-Left Quality:**\n"
            "I'll test like a real user, not just requirements. I'll look for edge cases, "
            "usability issues, and potential problems. I'll update you as I test and file any bugs "
            "I find. Want to pair test for 30 minutes? Sometimes that helps catch issues faster."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "product_owner"]
        )
    
    def _handle_defect_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about bugs and defects"""
        recommendations = [
            "Document bug with clear title, severity, and priority",
            "Include steps to reproduce, expected vs. actual results",
            "Provide environment details, screenshots, and test data",
            "Assess if bug prevents meeting Definition of Done",
            "Work with Product Owner to determine if bug endangers Sprint Goal",
            "If prevents DoD → Sprint Backlog (fix this Sprint)",
            "If doesn't prevent DoD → Product Backlog (PO prioritizes)"
        ]
        
        questions = [
            "What's the severity? (Critical/High/Medium/Low)",
            "Does this prevent meeting Definition of Done?",
            "Does this endanger the Sprint Goal?",
            "What are the exact steps to reproduce?",
            "What's the expected vs. actual result?",
            "What environment and test data was used?"
        ]
        
        response_text = (
            "Let me help you document and prioritize this defect properly.\n\n"
            "**Bug Report Quality:**\n"
            "A good bug report includes:\n"
            "- **Title:** Clear, concise summary\n"
            "- **Severity:** Critical / High / Medium / Low\n"
            "- **Priority:** How urgently should this be fixed?\n"
            "- **Steps to Reproduce:** Exact sequence to trigger bug\n"
            "- **Expected Result:** What should happen\n"
            "- **Actual Result:** What actually happens\n"
            "- **Environment:** Browser, OS, version, etc.\n"
            "- **Screenshots/Videos:** Visual evidence\n"
            "- **Test Data:** Specific data used\n"
            "- **Frequency:** Every time / Sometimes / Rare\n\n"
            "**Defect Prioritization:**\n"
            "- **Critical:** Blocks core functionality, data loss, security vulnerability, prevents Sprint Goal "
            "→ Fix immediately in current Sprint\n"
            "- **High:** Significant feature impairment, affects many users → Fix in current Sprint if possible\n"
            "- **Medium:** Minor feature impairment, easy workaround → Add to Product Backlog\n"
            "- **Low:** Cosmetic issues, edge cases → Add to Product Backlog, low priority\n\n"
            "**During Sprint:**\n"
            "- New defects that prevent DoD → Sprint Backlog (fix this Sprint)\n"
            "- New defects that don't prevent DoD → Product Backlog (PO prioritizes)\n"
            "- Work with Product Owner to determine if bug endangers Sprint Goal\n\n"
            "Let's assess this defect against our Definition of Done and Sprint Goal."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_definition_of_done_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Definition of Done"""
        recommendations = [
            "You help create and enforce the Definition of Done",
            "Verify Increment meets DoD before it can be considered 'Done'",
            "Quality criteria must be met: acceptance criteria, tests passing, no critical defects",
            "Make DoD visible and understood by everyone",
            "Advocate for quality standards when DoD isn't being followed",
            "Review and evolve DoD in Retrospectives"
        ]
        
        quality_criteria = [
            "All acceptance criteria met",
            "Code reviewed and approved",
            "Unit tests written and passing",
            "Integration tests passing",
            "Regression tests passing",
            "Exploratory testing completed",
            "No critical or high-priority defects",
            "Performance benchmarks met",
            "Security scan completed (if applicable)",
            "Accessibility standards met",
            "User documentation updated",
            "Deployed to staging/pre-production environment"
        ]
        
        questions = [
            "Does this Increment meet all Definition of Done criteria?",
            "Are all acceptance criteria met?",
            "Are all tests passing?",
            "Are there any critical or high-priority defects?",
            "Have performance, security, and accessibility been verified?",
            "Is the Definition of Done clear and understood by everyone?"
        ]
        
        response_text = (
            "Definition of Done is critical for quality. I help create and enforce it.\n\n"
            "**My Role:**\n"
            "- Help create Definition of Done (on behalf of whole Scrum Team)\n"
            "- Verify Increment meets DoD before it can be considered 'Done'\n"
            "- Advocate for quality standards when DoD isn't being followed\n\n"
            "**Quality Criteria I Typically Champion:**\n"
            "- All acceptance criteria met\n"
            "- Code reviewed and approved\n"
            "- Unit tests written and passing (Developer responsibility)\n"
            "- Integration tests passing\n"
            "- Regression tests passing\n"
            "- Exploratory testing completed\n"
            "- No critical or high-priority defects\n"
            "- Performance benchmarks met\n"
            "- Security scan completed (if applicable)\n"
            "- Accessibility standards met\n"
            "- User documentation updated\n"
            "- Deployed to staging/pre-production environment\n\n"
            "**Critical Rule:** If a Product Backlog item doesn't meet Definition of Done, "
            "it cannot be released or presented at Sprint Review. Quality is non-negotiable.\n\n"
            "**When DoD Isn't Being Followed:**\n"
            "- Use data (test results, defect trends) to show impact\n"
            "- Focus on user impact and business risk\n"
            "- Propose solutions, not just problems\n"
            "- Partner with developers on solutions\n"
            "- Escalate to Scrum Master if impediment\n"
            "- Bring to Retrospective for process improvement"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "product_owner", "scrum_master"]
        )
    
    def _handle_regression_testing_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about regression testing"""
        recommendations = [
            "Regression testing is part of Definition of Done - cannot be skipped",
            "Explain risk of skipping regression tests",
            "Offer alternatives: critical path tests, parallel execution, scope negotiation",
            "Use data to show value: bugs caught, defect escape rate",
            "Focus on user impact and business risk",
            "Propose solutions that balance speed and quality"
        ]
        
        questions = [
            "What's the current regression test suite size and execution time?",
            "How many bugs did regression tests catch last Sprint?",
            "What's our defect escape rate to production?",
            "Can we run critical path tests only?",
            "Can we run tests in parallel?",
            "Can we negotiate Sprint scope instead?"
        ]
        
        response_text = (
            "I understand the pressure to ship quickly. Let me explain the risk so we can make "
            "an informed decision.\n\n"
            "**Regression Testing Value:**\n"
            "- Catches bugs that would impact production\n"
            "- Part of Definition of Done - cannot be skipped\n"
            "- Prevents defect escape to production\n"
            "- Protects existing functionality\n\n"
            "**Risk of Skipping:**\n"
            "- High risk we introduce regressions in core features\n"
            "- Defect escape rate to production could increase\n"
            "- Cost of production bugs: customer support, hotfixes, reputation damage\n"
            "- Violates Definition of Done\n\n"
            "**Alternative Options:**\n"
            "1. **Run critical path tests only** - Covers 80% of risk, much faster\n"
            "2. **Run full suite but in parallel** - No time saved but full coverage\n"
            "3. **Negotiate Sprint scope** - Which feature can wait to next Sprint?\n\n"
            "**My Recommendation:**\n"
            "Run critical path regression tests as minimum. If we skip altogether, we're violating "
            "our Definition of Done and taking on significant risk. Which option works for achieving "
            "the Sprint Goal while managing quality risk?"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_accessibility_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about accessibility testing"""
        recommendations = [
            "Accessibility is part of Definition of Done (WCAG 2.1 Level AA)",
            "Run automated checks (aXe, WAVE, Lighthouse)",
            "Perform manual testing (keyboard navigation, screen reader, color contrast)",
            "Test with actual assistive technologies",
            "Provide specific issues with severity and recommendations",
            "Offer to pair test with UX Designer"
        ]
        
        questions = [
            "What specific areas are you most concerned about?",
            "Are we targeting WCAG 2.1 Level AA compliance?",
            "Have we tested with screen readers?",
            "Is keyboard navigation working?",
            "Do color contrasts meet WCAG AA standards?",
            "Are form inputs properly labeled?"
        ]
        
        response_text = (
            "Absolutely - accessibility is part of our Definition of Done. Let me run through "
            "our accessibility checklist.\n\n"
            "**Accessibility Testing Plan:**\n\n"
            "**Automated Checks (30 min):**\n"
            "- Run aXe DevTools scan\n"
            "- Check WAVE browser extension\n"
            "- Review Lighthouse accessibility score\n\n"
            "**Manual Testing (2 hours):**\n"
            "- **Keyboard navigation:** Can all interactive elements be reached by Tab/Enter?\n"
            "- **Screen reader:** Test with NVDA/JAWS - does it announce content correctly?\n"
            "- **Color contrast:** Do text/background combinations meet WCAG AA standards?\n"
            "- **Focus indicators:** Are focus states visible and clear?\n"
            "- **Alt text:** Do images have descriptive alt text?\n"
            "- **Form labels:** Are form inputs properly labeled?\n"
            "- **Error messages:** Are errors announced to screen readers?\n\n"
            "**Standards Reference:**\n"
            "- We're targeting WCAG 2.1 Level AA compliance\n"
            "- This is in our Definition of Done\n\n"
            "**What I'll Deliver:**\n"
            "- Accessibility test report\n"
            "- Specific issues found with severity\n"
            "- Recommendations for fixes\n"
            "- Retest timeline after fixes\n\n"
            "Can you share the specific areas you're most concerned about so I prioritize those first? "
            "Also, do you want to pair on screen reader testing? It's really eye-opening to experience "
            "the product that way."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["ux_ui_designer", "development_engineer"]
        )
    
    def _handle_automation_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about test automation"""
        recommendations = [
            "Automate repetitive tests to free time for exploratory testing",
            "Follow testing pyramid: Unit (most) → Integration → E2E (least)",
            "Automate tests alongside code development (shift-left)",
            "Maintain automation to keep it valuable",
            "Focus automation on critical paths and regression tests",
            "Use automation for fast feedback on code quality"
        ]
        
        questions = [
            "What tests should be automated? (repetitive, critical paths, regression)",
            "What's our current automation coverage?",
            "Is our test automation keeping pace with development?",
            "Are automated tests running in CI/CD pipeline?",
            "How long do automated tests take to run?",
            "What's the maintenance burden of our automation?"
        ]
        
        response_text = (
            "Test automation is essential for quality and speed. Here's my approach:\n\n"
            "**Testing Pyramid:**\n"
            "1. **Unit Tests (Most)** - Developers write, I may review strategy\n"
            "2. **Integration Tests** - I often lead creation\n"
            "3. **End-to-End Tests** - I design and maintain\n"
            "4. **Manual/Exploratory Tests (Least)** - I perform for discovery\n\n"
            "**Automation Principles:**\n"
            "- **Automate Repetitive:** Free yourself for exploratory testing\n"
            "- **Shift-Left:** Automate tests alongside code development\n"
            "- **Critical Paths:** Focus automation on high-value tests\n"
            "- **Fast Feedback:** Run in CI/CD for immediate results\n"
            "- **Maintainable:** Keep automation valuable, not a burden\n\n"
            "**What to Automate:**\n"
            "- Regression tests (prevent breaking existing functionality)\n"
            "- Critical user workflows\n"
            "- Repetitive test scenarios\n"
            "- Smoke tests\n\n"
            "**What NOT to Automate (or automate less):**\n"
            "- Exploratory testing (manual discovery)\n"
            "- Usability testing (requires human judgment)\n"
            "- One-off test scenarios\n\n"
            "**Anti-Pattern to Avoid:**\n"
            "Don't test everything manually. Automate repetitive tests so you can focus on "
            "exploratory testing and finding edge cases."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer"]
        )
    
    def _handle_coverage_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about test coverage and metrics"""
        recommendations = [
            "Track test coverage: code coverage, feature coverage, automation coverage",
            "Track defect metrics: defects found, escape rate, defect age, severity distribution",
            "Track quality trends: test pass rate, regression results, performance benchmarks",
            "Make quality metrics visible and transparent",
            "Use metrics to advocate for quality improvements",
            "Focus on critical paths having coverage, not just percentage"
        ]
        
        questions = [
            "What's our current test coverage? (code, feature, automation)",
            "What's our defect escape rate to production?",
            "Are quality metrics improving or declining?",
            "Do critical paths have adequate test coverage?",
            "What quality trends are we seeing?",
            "How can we improve our quality metrics?"
        ]
        
        response_text = (
            "Quality metrics help us understand and improve quality. Here's what I track:\n\n"
            "**Test Coverage Metrics:**\n"
            "- **Code coverage percentage** (unit tests)\n"
            "- **Feature coverage** (which features are tested)\n"
            "- **Automation coverage** (manual vs. automated)\n\n"
            "**Defect Metrics:**\n"
            "- **Defects found per Sprint**\n"
            "- **Defect escape rate** (bugs found in production)\n"
            "- **Defect age** (time from creation to resolution)\n"
            "- **Defect severity distribution**\n\n"
            "**Quality Trends:**\n"
            "- **Test pass rate over time**\n"
            "- **Regression test results**\n"
            "- **Performance benchmarks**\n"
            "- **Test execution time**\n\n"
            "**Key Principles:**\n"
            "- Make metrics visible and transparent\n"
            "- Focus on critical paths having coverage, not just percentage\n"
            "- Use metrics to advocate for quality improvements\n"
            "- Track trends to identify problems early\n\n"
            "**Important:** Coverage percentage alone isn't enough. Critical paths must have "
            "test coverage. It's better to have 60% coverage of critical paths than 90% coverage "
            "of non-critical code."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_acceptance_criteria_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about acceptance criteria"""
        recommendations = [
            "Verify all acceptance criteria are testable and clear",
            "Test each acceptance criterion systematically",
            "Identify testability concerns early in Sprint Planning",
            "Help clarify 'how will we know this is done?'",
            "Work with Product Owner to ensure criteria are specific and measurable",
            "Document test scenarios for each acceptance criterion"
        ]
        
        questions = [
            "Are all acceptance criteria clear and testable?",
            "How will we verify each acceptance criterion?",
            "Are there any ambiguous or unclear criteria?",
            "Do acceptance criteria cover edge cases?",
            "Are acceptance criteria specific and measurable?",
            "What test scenarios do we need for each criterion?"
        ]
        
        response_text = (
            "Acceptance criteria are the foundation of testing. Here's my approach:\n\n"
            "**My Role with Acceptance Criteria:**\n"
            "- **Sprint Planning:** Understand acceptance criteria for each Product Backlog item\n"
            "- **Testability:** Identify testability concerns early\n"
            "- **Clarity:** Help clarify 'how will we know this is done?'\n"
            "- **Testing:** Test each acceptance criterion systematically\n\n"
            "**Good Acceptance Criteria:**\n"
            "- Clear and specific\n"
            "- Testable and measurable\n"
            "- Cover happy path and edge cases\n"
            "- Define 'done' clearly\n\n"
            "**My Testing Approach:**\n"
            "- Review all acceptance criteria before testing\n"
            "- Create test scenarios for each criterion\n"
            "- Verify each criterion systematically\n"
            "- Document which criteria pass/fail\n"
            "- Report any unclear or ambiguous criteria\n\n"
            "**Shift-Left Quality:**\n"
            "I get involved early in Sprint Planning and Refinement to ensure acceptance criteria "
            "are testable and clear. This prevents problems later."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "business_analyst"]
        )
    
    def _handle_performance_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about performance testing"""
        recommendations = [
            "Performance testing is part of Definition of Done when applicable",
            "Test load, stress, and scalability",
            "Set performance benchmarks and verify they're met",
            "Test on realistic data volumes",
            "Consider performance implications of new features",
            "Report performance issues with metrics and recommendations"
        ]
        
        questions = [
            "What are our performance benchmarks?",
            "What load scenarios should we test?",
            "What's the expected user volume?",
            "Are there performance requirements in acceptance criteria?",
            "What data volumes should we test with?",
            "Are performance tests automated or manual?"
        ]
        
        response_text = (
            "Performance testing ensures the product meets performance requirements. Here's my approach:\n\n"
            "**Types of Performance Testing:**\n"
            "- **Load Testing:** Test under expected load\n"
            "- **Stress Testing:** Test beyond expected capacity\n"
            "- **Scalability Testing:** Test ability to scale\n"
            "- **Performance Benchmarks:** Verify specific metrics are met\n\n"
            "**When to Test Performance:**\n"
            "- When performance is part of Definition of Done\n"
            "- When performance requirements are in acceptance criteria\n"
            "- When new features may impact performance\n"
            "- For critical user workflows\n\n"
            "**My Approach:**\n"
            "- Set performance benchmarks\n"
            "- Test with realistic data volumes\n"
            "- Test load, stress, and scalability scenarios\n"
            "- Report performance issues with metrics\n"
            "- Provide recommendations for improvements\n\n"
            "**Definition of Done:**\n"
            "Performance benchmarks must be met before Increment can be considered 'Done.'"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "product_owner"]
        )
    
    def _handle_security_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about security testing"""
        recommendations = [
            "Security testing is part of Definition of Done when applicable",
            "Run vulnerability scans and security checks",
            "Test for common security vulnerabilities",
            "Verify security requirements are met",
            "Report security issues with severity and recommendations",
            "Work with developers on security fixes"
        ]
        
        questions = [
            "What security requirements are in Definition of Done?",
            "What security scans should we run?",
            "Are there specific security concerns for this feature?",
            "What security standards must we meet?",
            "Have we tested for common vulnerabilities?",
            "Are security tests automated or manual?"
        ]
        
        response_text = (
            "Security testing ensures the product is secure. Here's my approach:\n\n"
            "**Types of Security Testing:**\n"
            "- **Vulnerability Scanning:** Automated scans for known vulnerabilities\n"
            "- **Penetration Testing:** Manual testing for security weaknesses\n"
            "- **Security Requirements:** Verify security requirements are met\n"
            "- **Common Vulnerabilities:** Test for OWASP Top 10, etc.\n\n"
            "**When to Test Security:**\n"
            "- When security is part of Definition of Done\n"
            "- When security requirements are in acceptance criteria\n"
            "- For features handling sensitive data\n"
            "- For authentication and authorization features\n\n"
            "**My Approach:**\n"
            "- Run security scans as part of Definition of Done\n"
            "- Test for common security vulnerabilities\n"
            "- Verify security requirements are met\n"
            "- Report security issues with severity\n"
            "- Work with developers on security fixes\n\n"
            "**Definition of Done:**\n"
            "Security scan must be completed (if applicable) before Increment can be considered 'Done.'"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "product_owner"]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with QA Engineer perspective"""
        response_text = (
            f"As a QA Engineer (part of Developers), my primary accountability is creating a usable "
            f"Increment each Sprint with quality engineering expertise. Let me address your question: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Quality is everyone's responsibility - I advocate, but whole team owns it\n"
            f"- Prevent over detect - Shift testing left to catch issues early\n"
            f"- Automate repetitive - Free myself for exploratory testing\n"
            f"- User perspective - Test like a real user, not just requirements\n"
            f"- Transparent quality - Make test results and metrics visible\n\n"
            f"**Key Principles:**\n"
            f"- **Shift-Left Quality:** Get involved early in requirements and design\n"
            f"- **Definition of Done:** Verify Increment meets quality standards\n"
            f"- **Collaboration:** Work with developers, not against them\n"
            f"- **Quality Advocacy:** Use data to advocate for quality\n"
            f"- **Testing Pyramid:** Unit (most) → Integration → E2E → Manual (least)\n\n"
            f"I'm committed to ensuring every Increment meets quality standards. I advocate for quality, "
            f"collaborate on solutions, and make testing visible."
        )
        
        recommendations = [
            "Assess quality risk and impact",
            "Reference Definition of Done and acceptance criteria",
            "Provide evidence (test results, repro steps, screenshots)",
            "Suggest testing approach and test coverage",
            "Consider user perspective and impact",
            "Collaborate on solutions, not just report problems"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        if any(word in query_lower for word in ["product", "backlog", "priority", "acceptance criteria", "bug priority"]):
            needs.append("product_owner")
        
        if any(word in query_lower for word in ["code", "implementation", "fix", "bug", "defect", "technical"]):
            needs.append("development_engineer")
        
        if any(word in query_lower for word in ["design", "ux", "ui", "usability", "accessibility"]):
            needs.append("ux_ui_designer")
        
        if any(word in query_lower for word in ["requirement", "business", "acceptance criteria"]):
            needs.append("business_analyst")
        
        if any(word in query_lower for word in ["process", "impediment", "scrum", "quality process"]):
            needs.append("scrum_master")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "product_owner": "Acceptance criteria, business context, priority, bug prioritization decisions",
                "development_engineer": "Code for testing, technical context, unit test results, implementation details",
                "ux_ui_designer": "Design specifications, user flows, expected behaviors, accessibility requirements",
                "business_analyst": "Requirements, business rules, edge cases to test, acceptance criteria details",
                "data_metrics_analyst": "Metrics to validate, analytics requirements, A/B test validation needs",
                "scrum_master": "Facilitation, impediment removal, coaching, quality process improvements",
                "product_marketing_executive": "Release requirements, marketing claims to verify, beta testing needs"
            },
            "provides_to": {
                "product_owner": "Quality risk assessments, test coverage reports, defect impacts, bug prioritization input",
                "development_engineer": "Bug reports, test results, testability feedback, quality concerns",
                "ux_ui_designer": "Usability issues, cross-browser/device testing results, accessibility findings",
                "business_analyst": "Requirement clarity questions, test scenarios, acceptance criteria feedback",
                "data_metrics_analyst": "Testing of analytics implementation, data accuracy validation, A/B test validation",
                "scrum_master": "Quality impediments, testing blockers, process friction, quality process improvements",
                "all_team_members": "Test results, quality metrics, Definition of Done verification, quality advocacy"
            }
        }
