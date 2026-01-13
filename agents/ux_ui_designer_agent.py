"""
UX/UI Designer Agent
Implements the UX/UI Designer role (part of Developers) with expertise in:
- User experience (UX) design and user research
- User interface (UI) design and visual design
- Interaction design and prototyping
- Usability testing and design validation
- Accessibility and inclusive design
- Design systems and component libraries
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class UXUIDesignerAgent(BaseAgent):
    """
    UX/UI Designer AI Agent
    
    Note: In Scrum, there is no separate "Designer" role - you are a Developer 
    who specializes in design. All Developers are accountable for creating value.
    
    Primary Accountability: Creating any aspect of a usable Increment each Sprint 
    (with UX/UI design expertise).
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="UX/UI Designer",
            name="Design",
            context=context
        )
        self.design_system = {}
        self.user_research_findings = []
        self.prototypes = []
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define UX/UI Designer's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Creating any aspect of a usable Increment each Sprint (with UX/UI design expertise)",
            "note": "In Scrum, there is no separate 'Designer' role - you are a Developer who specializes in design. All Developers are accountable for creating value.",
            "key_responsibilities": {
                "user_experience_design": [
                    "Understanding user needs through research and interviews",
                    "Creating user flows and journey maps",
                    "Designing intuitive, accessible interfaces",
                    "Prototyping and testing design solutions",
                    "Ensuring design supports user goals and business outcomes"
                ],
                "developer_responsibilities": [
                    "Participating in Sprint Planning",
                    "Contributing to Sprint Backlog",
                    "Adapting work daily toward Sprint Goal",
                    "Creating usable Increment (designs, prototypes, design systems)",
                    "Owning Sprint Backlog alongside fellow Developers"
                ],
                "design_system": [
                    "Maintaining design consistency",
                    "Creating reusable components",
                    "Documenting design patterns",
                    "Collaborating with engineers on implementation"
                ]
            },
            "design_process": {
                "problem_definition": "What user problem are we solving? What's the user's goal? What's the business outcome? What constraints exist?",
                "ideation": "Sketch multiple solutions, consider different approaches, don't fall in love with first idea, involve team in brainstorming",
                "prototyping": {
                    "low_fidelity": "Paper sketches, wireframes (quick, cheap testing)",
                    "mid_fidelity": "Clickable prototypes (workflow testing)",
                    "high_fidelity": "Visual design, animations (final validation)"
                },
                "testing": "Test with real users, specific tasks and scenarios, observe behavior not just opinions, iterate based on findings",
                "implementation_support": "Collaborate with developers, review implementation for design fidelity, make adjustments based on technical constraints"
            },
            "core_ux_principles": {
                "user_centered": "Design for real users, base decisions on user research, validate designs with actual users",
                "simplicity": "Remove unnecessary complexity, don't make users think more than needed, progressive disclosure, clear hierarchy",
                "consistency": "Consistent patterns across product, follow platform conventions, reuse established patterns, maintain design system",
                "accessibility": "Design for diverse abilities, follow WCAG 2.1 Level AA standards, keyboard navigation, color contrast, screen reader compatibility",
                "feedback": "Immediate response to user actions, clear error messages, loading states, success confirmation",
                "error_prevention": "Design to prevent errors, confirmation for destructive actions, clear constraints and validation, helpful error recovery"
            },
            "visual_design_principles": {
                "hierarchy": "Most important elements most prominent, size/color/position establish importance, guide user's eye",
                "contrast": "Sufficient contrast for readability, use contrast to draw attention, meet accessibility standards",
                "alignment": "Create visual connections, reduce cognitive load, professional appearance",
                "proximity": "Related items grouped together, white space separates sections, clear visual relationships",
                "repetition": "Consistent patterns, predictable interactions, brand consistency"
            },
            "accessibility": {
                "wcag_2_1_level_aa": {
                    "perceivable": "Text alternatives for images, captions for audio/video, color contrast minimum 4.5:1, resize text to 200%",
                    "operable": "All functionality via keyboard, no keyboard traps, sufficient time, no flashing content, clear focus indicators",
                    "understandable": "Clear simple language, predictable navigation, input assistance, clear error messages",
                    "robust": "Semantic HTML, ARIA labels, screen reader compatibility, cross-browser/device support"
                },
                "testing": "Keyboard-only navigation, screen reader testing (NVDA/JAWS/VoiceOver), color contrast checker, automated tools (aXe/WAVE), testing with users with disabilities"
            },
            "research_methods": {
                "interviews": "Story-based, focus on specific past experiences, 'Tell me about the last time you...', observe how users solve problems",
                "usability_testing": "Give users specific tasks, observe without guiding, think-aloud protocol, note confusion/errors/delights, measure success rates",
                "contextual_inquiry": "Watch users in actual environment, understand context and constraints, identify workarounds and pain points",
                "card_sorting": "Understand users' mental models, validate information architecture, test navigation structures",
                "surveys": "Quantitative validation, measure satisfaction (NPS/CSAT), prioritize features"
            },
            "anti_patterns": [
                "Design in Isolation - Collaborate early and often with developers and users",
                "Pixel Perfection Over Usability - Focus on user needs, not just aesthetics",
                "Designing Without Research - Base designs on user insights, not assumptions",
                "Designing Without Constraints - Understand technical and business limitations",
                "Handing Off and Disappearing - Support implementation and review fidelity",
                "Designing for Yourself - You are not the user; validate with real users",
                "Ignoring Accessibility - Accessibility is not optional, it's a requirement"
            ]
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a UX/UI Designer perspective.
        Focuses on user-centered design, research, and accessibility.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler
        if any(word in query_lower for word in ["design", "mockup", "wireframe", "prototype", "ui", "interface"]):
            return self._handle_design_query(query, **kwargs)
        elif any(word in query_lower for word in ["user research", "research", "interview", "usability", "test"]):
            return self._handle_research_query(query, **kwargs)
        elif any(word in query_lower for word in ["accessibility", "a11y", "wcag", "accessible", "screen reader"]):
            return self._handle_accessibility_query(query, **kwargs)
        elif any(word in query_lower for word in ["user flow", "flow", "journey", "workflow"]):
            return self._handle_user_flow_query(query, **kwargs)
        elif any(word in query_lower for word in ["design system", "component", "pattern", "style guide"]):
            return self._handle_design_system_query(query, **kwargs)
        elif any(word in query_lower for word in ["animation", "transition", "interaction", "hover", "click"]):
            return self._handle_interaction_query(query, **kwargs)
        elif any(word in query_lower for word in ["feasible", "possible", "can we", "implement", "technical"]):
            return self._handle_feasibility_query(query, **kwargs)
        elif any(word in query_lower for word in ["usability issue", "usability problem", "user struggle", "confusion"]):
            return self._handle_usability_issue_query(query, **kwargs)
        elif any(word in query_lower for word in ["mobile", "responsive", "device", "breakpoint"]):
            return self._handle_responsive_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_design_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about design and design process"""
        recommendations = [
            "Understand the user problem: What are users trying to accomplish?",
            "Reference user research: What have we learned from real users?",
            "Consider multiple solutions: Don't jump to first idea",
            "Explain design rationale: Why this design serves users and business",
            "Acknowledge constraints: Technical, business, timeline",
            "Suggest testing: How can we validate this design?",
            "Follow design process: Problem definition -> Ideation -> Prototyping -> Testing -> Implementation"
        ]
        
        questions = [
            "What user problem are we solving?",
            "What's the user's goal?",
            "What's the business outcome?",
            "What constraints exist?",
            "What have we learned from user research?",
            "How can we validate this design with users?",
            "What's the simplest design that solves the problem?"
        ]
        
        response_text = (
            "Let me help you approach this from a user-centered design perspective.\n\n"
            "**Design Process:**\n\n"
            "**1. Problem Definition:**\n"
            "- What user problem are we solving?\n"
            "- What's the user's goal?\n"
            "- What's the business outcome?\n"
            "- What constraints exist?\n\n"
            "**2. Ideation:**\n"
            "- Sketch multiple solutions\n"
            "- Consider different approaches\n"
            "- Don't fall in love with first idea\n"
            "- Involve team in brainstorming\n\n"
            "**3. Prototyping:**\n"
            "- **Low-fidelity:** Paper sketches, wireframes (quick, cheap testing)\n"
            "- **Mid-fidelity:** Clickable prototypes (workflow testing)\n"
            "- **High-fidelity:** Visual design, animations (final validation)\n\n"
            "**4. Testing:**\n"
            "- Test with real users\n"
            "- Specific tasks and scenarios\n"
            "- Observe behavior, not just opinions\n"
            "- Iterate based on findings\n\n"
            "**5. Implementation Support:**\n"
            "- Collaborate with developers\n"
            "- Review implementation for design fidelity\n"
            "- Make adjustments based on technical constraints\n\n"
            "**Core UX Principles:**\n"
            "- **User-Centered:** Design for real users based on research, not assumptions\n"
            "- **Simplicity:** Remove unnecessary complexity, clear hierarchy\n"
            "- **Consistency:** Consistent patterns, follow platform conventions\n"
            "- **Accessibility:** Follow WCAG 2.1 Level AA standards\n"
            "- **Feedback:** Immediate response to user actions\n"
            "- **Error Prevention:** Design to prevent errors\n\n"
            "**Key Principle:** Users first - Design for real users based on research, not assumptions."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_research_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about user research and usability testing"""
        recommendations = [
            "Participate in weekly customer interviews (with Product Owner)",
            "Conduct usability testing sessions with real users",
            "Use story-based interview questions: 'Tell me about the last time you...'",
            "Observe users without guiding them",
            "Measure success rates and time on task",
            "Synthesize findings immediately and share with team",
            "Combine quantitative data with qualitative insights"
        ]
        
        questions = [
            "What user problem are we trying to understand?",
            "What research method is most appropriate?",
            "Who are our users? How do we recruit them?",
            "What questions should we ask?",
            "What tasks should we test?",
            "How do we synthesize and share findings?",
            "What opportunities does this reveal?"
        ]
        
        response_text = (
            "User research is fundamental to good design. Here's my approach:\n\n"
            "**Research Methods:**\n\n"
            "**Interviews (Story-Based):**\n"
            "- Focus on specific past experiences, not hypotheticals\n"
            "- 'Tell me about the last time you...'\n"
            "- 'Walk me through how you...'\n"
            "- Observe how users currently solve problems\n\n"
            "**Usability Testing:**\n"
            "- Give users specific tasks\n"
            "- Observe without guiding\n"
            "- Think-aloud protocol\n"
            "- Note confusion, errors, delights\n"
            "- Measure success rates and time on task\n\n"
            "**Contextual Inquiry:**\n"
            "- Watch users in their actual environment\n"
            "- Understand context and constraints\n"
            "- Identify workarounds and pain points\n\n"
            "**Card Sorting:**\n"
            "- Understand users' mental models\n"
            "- Validate information architecture\n"
            "- Test navigation structures\n\n"
            "**Surveys:**\n"
            "- Quantitative validation of qualitative insights\n"
            "- Measure satisfaction (NPS, CSAT)\n"
            "- Prioritize features\n\n"
            "**My Approach:**\n"
            "- Participate in weekly customer interviews with Product Owner\n"
            "- Conduct usability testing sessions regularly\n"
            "- Synthesize findings immediately\n"
            "- Share insights with team\n"
            "- Update designs based on learnings\n"
            "- Add opportunities to Opportunity Solution Tree\n\n"
            "**Key Principle:** Base designs on user insights, not assumptions. "
            "You are not the user - validate with real users."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "data_metrics_analyst"]
        )
    
    def _handle_accessibility_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about accessibility"""
        recommendations = [
            "Follow WCAG 2.1 Level AA standards (required, not optional)",
            "Ensure keyboard navigation for all functionality",
            "Maintain color contrast minimum 4.5:1 for text",
            "Provide text alternatives for images (alt text)",
            "Ensure screen reader compatibility",
            "Test with keyboard-only navigation",
            "Test with screen readers (NVDA, JAWS, VoiceOver)",
            "Use automated tools (aXe, WAVE) for validation"
        ]
        
        questions = [
            "Does this meet WCAG 2.1 Level AA standards?",
            "Can all functionality be accessed via keyboard?",
            "Is color contrast sufficient?",
            "Are images properly labeled?",
            "Are form inputs properly labeled?",
            "Are error messages accessible to screen readers?",
            "Have we tested with actual assistive technologies?"
        ]
        
        response_text = (
            "Accessibility is not optional - it's a requirement. Here's my approach:\n\n"
            "**WCAG 2.1 Level AA Compliance:**\n\n"
            "**Perceivable:**\n"
            "- Text alternatives for images (alt text)\n"
            "- Captions for audio/video\n"
            "- Color contrast minimum 4.5:1 for text\n"
            "- Resize text to 200% without loss of function\n\n"
            "**Operable:**\n"
            "- All functionality via keyboard\n"
            "- No keyboard traps\n"
            "- Sufficient time to read/interact\n"
            "- No flashing content (seizure risk)\n"
            "- Clear focus indicators\n\n"
            "**Understandable:**\n"
            "- Clear, simple language\n"
            "- Predictable navigation\n"
            "- Input assistance and error prevention\n"
            "- Clear error messages with suggestions\n\n"
            "**Robust:**\n"
            "- Semantic HTML\n"
            "- ARIA labels where needed\n"
            "- Screen reader compatibility\n"
            "- Cross-browser/device support\n\n"
            "**Testing for Accessibility:**\n"
            "- Keyboard-only navigation\n"
            "- Screen reader testing (NVDA, JAWS, VoiceOver)\n"
            "- Color contrast checker\n"
            "- Automated tools (aXe, WAVE)\n"
            "- Testing with users with disabilities\n\n"
            "**My Role:**\n"
            "- Design with accessibility in mind from the start\n"
            "- Ensure designs meet WCAG 2.1 Level AA\n"
            "- Collaborate with QA Engineer on accessibility testing\n"
            "- Review implementation for accessibility compliance\n"
            "- Advocate for inclusive design\n\n"
            "**Key Principle:** Inclusive design benefits everyone. "
            "Accessibility is not a nice-to-have, it's a requirement."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "qa_engineer"]
        )
    
    def _handle_user_flow_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about user flows and journeys"""
        recommendations = [
            "Create step-by-step user journeys",
            "Include decision points and branches",
            "Document success and error paths",
            "Identify integration points",
            "Consider edge cases and error states",
            "Validate flows with user research",
            "Make flows visible and understandable"
        ]
        
        questions = [
            "What's the user's goal?",
            "What are the steps in the journey?",
            "Where are decision points?",
            "What are the success and error paths?",
            "What are the edge cases?",
            "Have we validated this flow with users?",
            "Where might users struggle?"
        ]
        
        response_text = (
            "User flows help us understand the complete user journey. Here's my approach:\n\n"
            "**User Flow Documentation:**\n"
            "- Step-by-step user journeys\n"
            "- Decision points and branches\n"
            "- Success and error paths\n"
            "- Integration points\n"
            "- Edge cases and error states\n\n"
            "**Example Flow Structure:**\n"
            "1. User action/trigger\n"
            "2. System response\n"
            "3. User decision point\n"
            "4. Branch A (success path)\n"
            "5. Branch B (error path)\n"
            "6. Final outcome\n\n"
            "**My Approach:**\n"
            "- Map complete user journeys\n"
            "- Identify pain points and friction\n"
            "- Consider all paths (happy, error, edge cases)\n"
            "- Validate flows with user research\n"
            "- Iterate based on findings\n"
            "- Make flows visible to team\n\n"
            "**Key Considerations:**\n"
            "- What's the user trying to accomplish?\n"
            "- Where might users struggle?\n"
            "- What are the decision points?\n"
            "- What happens in error cases?\n"
            "- How can we simplify the flow?\n\n"
            "User flows help identify opportunities for improvement and ensure we design "
            "for the complete user experience."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "business_analyst"]
        )
    
    def _handle_design_system_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about design systems"""
        recommendations = [
            "Maintain design consistency across product",
            "Create reusable components",
            "Document design patterns and usage guidelines",
            "Collaborate with developers on implementation",
            "Keep design system up to date",
            "Make design system accessible to team",
            "Include accessibility notes in component documentation"
        ]
        
        questions = [
            "What components do we need?",
            "What are the design patterns?",
            "How do components work together?",
            "What are the usage guidelines?",
            "How do we maintain consistency?",
            "What's the implementation approach?",
            "Are components accessible?"
        ]
        
        response_text = (
            "Design systems ensure consistency and efficiency. Here's my approach:\n\n"
            "**Design System Components:**\n"
            "- Component library (buttons, forms, navigation, etc.)\n"
            "- Usage guidelines for each component\n"
            "- Design patterns and best practices\n"
            "- Code snippets for developers\n"
            "- Accessibility notes\n"
            "- Responsive breakpoints\n"
            "- Animation and interaction details\n\n"
            "**Design System Benefits:**\n"
            "- Consistency across product\n"
            "- Faster development (reusable components)\n"
            "- Easier maintenance (update once, use everywhere)\n"
            "- Better collaboration (shared language)\n"
            "- Quality assurance (tested patterns)\n\n"
            "**My Role:**\n"
            "- Maintain design consistency\n"
            "- Create reusable components\n"
            "- Document design patterns\n"
            "- Collaborate with developers on implementation\n"
            "- Keep design system up to date\n\n"
            "**Key Principles:**\n"
            "- Consistency: Same patterns across product\n"
            "- Reusability: Components work in multiple contexts\n"
            "- Documentation: Clear usage guidelines\n"
            "- Collaboration: Work with developers on implementation\n"
            "- Evolution: Design system grows with product\n\n"
            "A good design system makes design and development faster and more consistent."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer"]
        )
    
    def _handle_interaction_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about interactions, animations, and transitions"""
        recommendations = [
            "Specify animation details: type, duration, easing",
            "Consider accessibility: support prefers-reduced-motion",
            "Use GPU-accelerated properties (transform, opacity)",
            "Test on lower-end devices for performance",
            "Document interaction states (hover, active, disabled, focus)",
            "Provide code examples for developers",
            "Consider edge cases (rapid clicks, back navigation, etc.)"
        ]
        
        questions = [
            "What's the animation type? (fade, slide, scale, etc.)",
            "What's the duration? (typically 200-500ms)",
            "What's the easing function? (ease-in-out, ease-out, etc.)",
            "Does it support prefers-reduced-motion?",
            "Is it performant on lower-end devices?",
            "What are the interaction states?",
            "What happens in edge cases?"
        ]
        
        response_text = (
            "Interactions and animations enhance user experience when done well. Here's my approach:\n\n"
            "**Animation Specifications:**\n"
            "- **Type:** Fade, slide, scale, etc.\n"
            "- **Duration:** Typically 200-500ms (fast enough to feel snappy, slow enough to track)\n"
            "- **Easing:** ease-in-out (smooth acceleration/deceleration)\n"
            "- **Trigger:** What user action starts the animation?\n"
            "- **States:** Initial state -> Transition -> Final state\n\n"
            "**Implementation Options:**\n"
            "1. **CSS Transitions** - Performant, smooth, GPU-accelerated\n"
            "2. **CSS Animations** - More control, no JavaScript needed\n"
            "3. **JavaScript Animation Library** - Maximum control, complex sequences\n\n"
            "**Accessibility:**\n"
            "Always support prefers-reduced-motion:\n"
            "```css\n"
            "@media (prefers-reduced-motion: reduce) {\n"
            "  .animation {\n"
            "    transition: none;\n"
            "  }\n"
            "}\n"
            "```\n\n"
            "**Performance:**\n"
            "- Use `transform` and `opacity` (GPU-accelerated)\n"
            "- Avoid animating `width`, `height`, `left`, `right` (reflow expensive)\n"
            "- Test on lower-end devices\n"
            "- Target 60fps for smooth animations\n\n"
            "**Edge Cases:**\n"
            "- What if user triggers action rapidly? (Debounce or disable during animation)\n"
            "- What if user navigates back? (Reverse animation direction)\n"
            "- What if content is taller than viewport? (Scroll to top on transition)\n\n"
            "**My Approach:**\n"
            "- Specify animation details clearly\n"
            "- Provide code examples for developers\n"
            "- Consider accessibility and performance\n"
            "- Test on actual devices\n"
            "- Review implementation for fidelity\n\n"
            "Want to pair on implementing this? I can review it in real-time and ensure it matches design intent."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer"]
        )
    
    def _handle_feasibility_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about design feasibility"""
        recommendations = [
            "Assess technical feasibility with developers",
            "Consider implementation complexity and effort",
            "Identify alternative approaches if needed",
            "Balance ideal design with pragmatic delivery",
            "Consider timeline and Sprint constraints",
            "Propose MVP approach if full design is too complex",
            "Collaborate on design vs. technical trade-offs"
        ]
        
        questions = [
            "Is this technically feasible?",
            "What's the implementation complexity?",
            "What's the effort estimate?",
            "Are there alternative approaches?",
            "Can we do an MVP version first?",
            "What are the technical constraints?",
            "How does this fit within Sprint timeline?"
        ]
        
        response_text = (
            "Let me assess design feasibility and work with developers on the best approach.\n\n"
            "**Feasibility Assessment:**\n"
            "1. **Technical Feasibility:** Can this be implemented? What are the options?\n"
            "2. **Complexity:** How complex is the implementation?\n"
            "3. **Effort:** What's the estimated effort?\n"
            "4. **Constraints:** What are the technical or business constraints?\n"
            "5. **Alternatives:** Are there simpler approaches that achieve the same goal?\n\n"
            "**My Approach:**\n"
            "- Collaborate with developers early on feasibility\n"
            "- Understand technical constraints\n"
            "- Propose alternative approaches if needed\n"
            "- Balance ideal design with pragmatic delivery\n"
            "- Consider MVP approach if full design is too complex\n"
            "- Work together on design vs. technical trade-offs\n\n"
            "**Design-Development Collaboration:**\n"
            "- **During Sprint Planning:** Clarify design scope, show mockups, discuss implementation\n"
            "- **During Sprint:** Pair with developers, daily check-ins, collaborate on trade-offs\n"
            "- **Design Handoff:** Walkthrough designs, explain rationale, be available for questions\n"
            "- **Review:** Review work-in-progress frequently, test on actual devices\n\n"
            "**Key Principle:** Don't design in isolation. Collaborate early and often with developers. "
            "Understand constraints and work together on solutions."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "product_owner"]
        )
    
    def _handle_usability_issue_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about usability issues"""
        recommendations = [
            "Investigate usability issues systematically",
            "Conduct usability testing to understand problems",
            "Review analytics data for drop-off points",
            "Perform heuristic evaluation",
            "Prioritize issues by severity",
            "Prototype improvements and test",
            "Measure improvement with A/B testing"
        ]
        
        questions = [
            "What specific usability issues were found?",
            "Where in the flow do issues occur?",
            "What tasks were users trying to accomplish?",
            "How many users are affected?",
            "What's the severity? (blocking vs. minor friction)",
            "What does analytics data show?",
            "How can we test improvements?"
        ]
        
        response_text = (
            "Let me help investigate and fix usability issues. Here's my systematic approach:\n\n"
            "**Usability Issue Investigation:**\n\n"
            "**1. Understand the Problem:**\n"
            "- What specific issues were found?\n"
            "- Where in the flow do they occur?\n"
            "- What tasks were users trying to accomplish?\n"
            "- How many users are affected?\n"
            "- What's the severity? (blocking task completion vs. minor friction)\n\n"
            "**2. Usability Testing:**\n"
            "- Recruit 3-5 users to test the current flow\n"
            "- Give them realistic tasks\n"
            "- Observe where they struggle\n"
            "- Record sessions for team review\n\n"
            "**3. Analytics Review (with Data Analyst):**\n"
            "- Where do users drop off? (funnel analysis)\n"
            "- How long do they spend on each step?\n"
            "- What errors are most common?\n\n"
            "**4. Heuristic Evaluation:**\n"
            "- Review flow against usability principles\n"
            "- Document specific issues with screenshots\n"
            "- Prioritize by severity\n\n"
            "**Common Usability Issues:**\n"
            "- **Unclear Next Steps:** Are call-to-action buttons obvious?\n"
            "- **Form Validation:** Are error messages clear and helpful?\n"
            "- **Information Overload:** Are we asking for too much at once?\n"
            "- **Mobile Experience:** Is the flow mobile-optimized?\n\n"
            "**5. Design Iteration:**\n"
            "- Prototype improvements based on findings\n"
            "- A/B test new design vs. current\n"
            "- Measure improvement\n\n"
            "**My Process:**\n"
            "- Investigate issues systematically\n"
            "- Test with real users\n"
            "- Analyze data and behavior\n"
            "- Prototype improvements\n"
            "- Validate fixes with testing\n\n"
            "Let's pair on usability testing? I'll recruit users, you can observe and take notes. "
            "Then we'll synthesize findings together and prioritize fixes."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["qa_engineer", "data_metrics_analyst", "product_owner"]
        )
    
    def _handle_responsive_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about responsive design and mobile"""
        recommendations = [
            "Design for mobile-first approach",
            "Define responsive breakpoints (mobile, tablet, desktop)",
            "Ensure touch targets are large enough (44×44px minimum)",
            "Test on actual devices, not just emulators",
            "Consider different screen sizes and orientations",
            "Optimize for performance on mobile devices",
            "Ensure keyboard behavior makes sense on mobile"
        ]
        
        questions = [
            "What are the target devices and screen sizes?",
            "What are the responsive breakpoints?",
            "Are touch targets large enough?",
            "How does the design work on different screen sizes?",
            "Is the mobile experience optimized?",
            "Have we tested on actual devices?",
            "How does keyboard behavior work on mobile?"
        ]
        
        response_text = (
            "Responsive design ensures the product works well on all devices. Here's my approach:\n\n"
            "**Responsive Design Principles:**\n\n"
            "**Mobile-First Approach:**\n"
            "- Design for mobile first, then enhance for larger screens\n"
            "- Ensures core functionality works on smallest screens\n"
            "- Progressive enhancement for larger devices\n\n"
            "**Breakpoints:**\n"
            "- Mobile: < 768px\n"
            "- Tablet: 768px - 1024px\n"
            "- Desktop: > 1024px\n"
            "- (Customize based on your product needs)\n\n"
            "**Mobile Considerations:**\n"
            "- **Touch Targets:** Minimum 44×44px for tap targets\n"
            "- **Spacing:** Adequate spacing between interactive elements\n"
            "- **Text Size:** Readable without zooming\n"
            "- **Navigation:** Mobile-friendly navigation patterns\n"
            "- **Forms:** Optimized for mobile input\n"
            "- **Performance:** Fast loading on mobile networks\n\n"
            "**Testing:**\n"
            "- Test on actual devices, not just emulators\n"
            "- Test different screen sizes and orientations\n"
            "- Test on different browsers and OS\n"
            "- Test with real users on their devices\n\n"
            "**My Approach:**\n"
            "- Design mobile-first\n"
            "- Define responsive breakpoints\n"
            "- Ensure touch targets are adequate\n"
            "- Test on actual devices\n"
            "- Optimize for mobile performance\n"
            "- Review implementation across devices\n\n"
            "**Key Principle:** The product should work well on all devices. "
            "Mobile is often the primary device for many users."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "qa_engineer"]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with UX/UI Designer perspective"""
        response_text = (
            f"As a UX/UI Designer (part of Developers), my primary accountability is creating a usable "
            f"Increment each Sprint with UX/UI design expertise. Let me address your question: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Understand the user need: What problem are users trying to solve?\n"
            f"- Reference research: What have we learned from real users?\n"
            f"- Explain design thinking: Why this design approach?\n"
            f"- Consider alternatives: What other options exist?\n"
            f"- Address constraints: How does this fit technical/business limits?\n"
            f"- Propose validation: How can we test this with users?\n\n"
            f"**Key Principles:**\n"
            f"- **Users First:** Design for real users based on research, not assumptions\n"
            f"- **Collaborate Constantly:** Design is a team sport, not a solo activity\n"
            f"- **Iterate Quickly:** Prototype fast, test early, improve continuously\n"
            f"- **Accessibility Matters:** Inclusive design benefits everyone\n"
            f"- **Data + Qualitative:** Combine analytics with user interviews\n\n"
            f"I'm committed to creating user-centered designs that are beautiful, usable, and accessible. "
            f"I research with users, collaborate with team, and iterate relentlessly."
        )
        
        recommendations = [
            "Understand user needs through research",
            "Design for real users, not assumptions",
            "Test designs with actual users",
            "Ensure accessibility (WCAG 2.1 Level AA)",
            "Collaborate with developers on implementation",
            "Iterate based on feedback and testing"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        if any(word in query_lower for word in ["product", "user", "customer", "feature", "priority"]):
            needs.append("product_owner")
        
        if any(word in query_lower for word in ["implement", "technical", "feasible", "code", "development", "animation"]):
            needs.append("development_engineer")
        
        if any(word in query_lower for word in ["test", "qa", "usability", "accessibility", "quality"]):
            needs.append("qa_engineer")
        
        if any(word in query_lower for word in ["data", "metrics", "analytics", "behavior", "usage"]):
            needs.append("data_metrics_analyst")
        
        if any(word in query_lower for word in ["requirement", "business", "flow", "process"]):
            needs.append("business_analyst")
        
        if any(word in query_lower for word in ["marketing", "onboarding", "launch"]):
            needs.append("product_marketing_executive")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "product_owner": "User needs, business goals, feature priorities, customer interview insights",
                "development_engineer": "Technical constraints, implementation questions, feasibility concerns, animation implementation",
                "qa_engineer": "Usability issues found during testing, edge cases discovered, accessibility findings",
                "business_analyst": "Business requirements, workflows, business rules, user flow context",
                "data_metrics_analyst": "Usage data, behavior patterns, A/B test results, funnel analysis",
                "scrum_master": "Facilitation, coaching, impediment removal, design process improvements",
                "product_marketing_executive": "Marketing requirements, messaging needs, target audience, onboarding needs"
            },
            "provides_to": {
                "product_owner": "Design insights, usability concerns, user research findings, design prototypes",
                "development_engineer": "Design specifications, interaction details, edge case designs, animation specs",
                "qa_engineer": "Expected behaviors, interaction specifications, accessibility requirements, design validation",
                "business_analyst": "User flows, interaction designs, requirement questions, design edge cases",
                "data_metrics_analyst": "Design hypotheses, experiment designs, qualitative insights, A/B test design",
                "scrum_master": "Design process blockers, user research access needs, design review process improvements",
                "all_team_members": "Design mockups, prototypes, user research insights, design system components, accessibility guidelines"
            }
        }
