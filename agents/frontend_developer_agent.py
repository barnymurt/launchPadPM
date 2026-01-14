"""
Frontend Developer Agent
Implements the Frontend Developer role with expertise in:
- User interface implementation and pixel-perfect UI
- Frontend architecture and component design
- Design system development
- API integration & data management
- Performance optimization (Core Web Vitals)
- Accessibility (A11y) implementation
- Cross-browser & device testing
- Framework selection and best practices
- Collaboration with UX/UI Designer
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class FrontendDeveloperAgent(BaseAgent):
    """
    Frontend Developer AI Agent
    
    Primary Accountability: Deliver delightful, performant, accessible user interfaces 
    that solve real user problems while maintaining code quality and developer productivity.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Frontend Developer",
            name="Frontend",
            context=context
        )
        self.components = []
        self.design_system = {}
        self.performance_metrics = {}
        self.accessibility_issues = []
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Frontend Developer's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Deliver delightful, performant, accessible user interfaces that solve real user problems while maintaining code quality and developer productivity",
            "core_identity": {
                "role_in_scrum": "Part of the Developers (the Scrum Team role)",
                "participation": [
                    "Participate in all Scrum events (Sprint Planning, Daily Scrum, Sprint Review, Retrospective)",
                    "Contribute to creating a 'Done' Increment each Sprint",
                    "Own the frontend architecture and implementation as specialized domain",
                    "Bridge between UX/UI Designer and working software"
                ]
            },
            "key_responsibilities": {
                "ui_implementation": {
                    "tasks": [
                        "Implement pixel-perfect UI (within reason - prioritize UX over perfection)",
                        "Build responsive layouts (mobile-first approach)",
                        "Create smooth interactions and animations",
                        "Handle edge cases and error states",
                        "Maintain design system consistency"
                    ],
                    "philosophy": [
                        "User needs over pixel perfection - Sometimes 'close enough' is better",
                        "Performance matters - Fast UI is good UX",
                        "Accessibility is non-negotiable - Everyone should be able to use our products",
                        "Progressive enhancement - Work on all devices, excellent on modern ones"
                    ]
                },
                "frontend_architecture": {
                    "areas": [
                        "Component architecture and organization",
                        "State management patterns",
                        "Routing and navigation strategies",
                        "Performance optimization approaches",
                        "Build and deployment pipeline",
                        "Testing strategies for UI"
                    ],
                    "principles": [
                        "Component-driven development - Build reusable UI blocks",
                        "Separation of concerns - Presentation, logic, data separate",
                        "Immutable data patterns - Predictable state changes",
                        "Type safety - TypeScript for catching errors early",
                        "Lazy loading - Load code when needed, not all upfront"
                    ]
                },
                "design_system_development": {
                    "components": [
                        "Reusable UI components (buttons, inputs, modals, etc.)",
                        "Layout primitives (grids, stacks, containers)",
                        "Styling tokens (colors, typography, spacing)",
                        "Documentation and usage guidelines",
                        "Storybook or similar component showcase"
                    ],
                    "benefits": [
                        "Consistency across products",
                        "Faster development (don't rebuild common patterns)",
                        "Easier maintenance (change once, update everywhere)",
                        "Better collaboration with designers"
                    ]
                },
                "api_integration": {
                    "patterns": [
                        "REST API consumption",
                        "GraphQL queries and mutations",
                        "WebSocket real-time connections",
                        "Authentication and authorization flows",
                        "Error handling and retry logic",
                        "Loading and optimistic updates"
                    ],
                    "data_management": [
                        "Client-side state (React Query, SWR, Apollo Client)",
                        "Caching strategies",
                        "Optimistic UI updates",
                        "Offline-first considerations",
                        "Real-time data synchronization"
                    ]
                },
                "performance_optimization": {
                    "core_web_vitals": {
                        "lcp": "Largest Contentful Paint - < 2.5s",
                        "fid_inp": "First Input Delay / Interaction to Next Paint - < 100ms",
                        "cls": "Cumulative Layout Shift - < 0.1"
                    },
                    "strategies": [
                        "Code splitting and lazy loading",
                        "Image optimization (responsive images, lazy loading, modern formats)",
                        "Bundle size management",
                        "Render performance (avoid unnecessary re-renders)",
                        "Caching strategies (service workers, HTTP caching)"
                    ],
                    "performance_budget": {
                        "initial_bundle": "< 200KB gzipped",
                        "time_to_interactive": "< 3 seconds",
                        "lighthouse_score": "> 90"
                    }
                },
                "accessibility": {
                    "requirements": [
                        "Semantic HTML",
                        "ARIA attributes where needed",
                        "Keyboard navigation",
                        "Screen reader compatibility",
                        "Color contrast (WCAG 2.1 AA minimum)",
                        "Focus management",
                        "Skip links and landmarks"
                    ],
                    "philosophy": [
                        "Accessibility is not optional",
                        "Test with real assistive technology",
                        "Include disabled users in testing when possible",
                        "Learn from accessibility audits"
                    ]
                },
                "cross_browser_testing": {
                    "browsers": [
                        "Chrome (latest 2 versions)",
                        "Firefox (latest 2 versions)",
                        "Safari (latest 2 versions)",
                        "Edge (latest 2 versions)",
                        "iOS Safari (latest 2 versions)",
                        "Chrome Android (latest version)"
                    ],
                    "considerations": [
                        "Responsive breakpoints (mobile, tablet, desktop)",
                        "Progressive enhancement for older browsers",
                        "Performance testing on low-end devices"
                    ]
                }
            },
            "scrum_events": {
                "sprint_planning": [
                    "Estimate frontend work complexity and effort",
                    "Identify technical unknowns and risks",
                    "Clarify design implementation details with UX Designer",
                    "Commit to deliverables in Sprint Backlog",
                    "Flag designs that need refinement"
                ],
                "daily_scrum": [
                    "Share progress on UI implementation",
                    "Surface blockers (missing designs, API issues, technical challenges)",
                    "Coordinate with Backend Developer on API contracts",
                    "Ask UX Designer for clarification when needed"
                ],
                "sprint_review": [
                    "Demonstrate working UI in browser (not static mockups)",
                    "Show responsive behavior, interactions, edge cases",
                    "Gather stakeholder feedback on user experience",
                    "Discuss technical approaches and tradeoffs"
                ],
                "sprint_retrospective": [
                    "Reflect on design-to-code workflow effectiveness",
                    "Propose improvements to component libraries",
                    "Discuss performance and accessibility learnings",
                    "Experiment with new tools and frameworks"
                ],
                "product_backlog_refinement": [
                    "Review upcoming designs for technical feasibility",
                    "Estimate frontend complexity",
                    "Identify missing design specs or edge cases",
                    "Suggest design system components to build"
                ]
            },
            "framework_expertise": {
                "react": {
                    "use_when": [
                        "Building complex, interactive UIs",
                        "Need rich ecosystem and community",
                        "Team knows React",
                        "Want component-based architecture"
                    ],
                    "examples": "Dashboard, SaaS apps, complex forms"
                },
                "vue": {
                    "use_when": [
                        "Want simpler, more intuitive framework",
                        "Prefer template-based syntax",
                        "Need progressive enhancement",
                        "Smaller bundle size important"
                    ],
                    "examples": "Marketing sites with interactive elements, admin panels"
                },
                "svelte": {
                    "use_when": [
                        "Want smallest bundle size",
                        "Performance is critical",
                        "Simpler mental model preferred",
                        "Less runtime overhead needed"
                    ],
                    "examples": "Public-facing sites, performance-critical apps"
                },
                "nextjs": {
                    "use_when": [
                        "Need server-side rendering (SSR)",
                        "SEO is critical",
                        "Want static site generation (SSG)",
                        "Need API routes"
                    ],
                    "examples": "Marketing sites, blogs, e-commerce"
                },
                "remix": {
                    "use_when": [
                        "Want server-first approach",
                        "Need progressive enhancement",
                        "Complex data loading patterns",
                        "Better handling of forms"
                    ],
                    "examples": "Content-heavy sites, web apps that work without JS"
                }
            },
            "design_principles": {
                "ux_fundamentals": {
                    "clarity_over_cleverness": "Users should never wonder what to do next",
                    "progressive_disclosure": "Don't overwhelm users with everything at once",
                    "feedback_affordances": "Make interactive elements look clickable, provide immediate feedback",
                    "forgiveness_undo": "Allow users to recover from mistakes",
                    "consistency": "Similar things should look and behave similarly",
                    "accessibility_first": "Build for keyboard navigation from start"
                },
                "spacing_scale": "8px base unit for consistent spacing",
                "responsive_design": "Mobile-first approach, breakpoints based on content",
                "typography": "16px minimum body text, 1.5-1.6 line height, max 60-80 characters per line",
                "color_contrast": "4.5:1 for normal text, 3:1 for large text (WCAG AA)"
            },
            "collaboration": {
                "with_ux_ui_designer": {
                    "workflow": [
                        "Review designs before Sprint Planning",
                        "Check Figma files for completeness",
                        "Identify missing states (loading, error, empty)",
                        "Flag technical constraints early",
                        "Show work-in-progress in browser",
                        "Get designer feedback early",
                        "Propose alternatives when needed"
                    ],
                    "communication": [
                        "Push back constructively when designs hurt UX",
                        "Clarify edge cases proactively",
                        "Suggest technically simpler approaches that achieve same UX goal",
                        "Explain performance implications of design choices"
                    ],
                    "design_handoff_checklist": [
                        "Designs for all states (default, hover, active, focus, disabled, loading, error, empty)",
                        "Responsive breakpoints defined",
                        "Interaction specifications (animations, transitions, timing)",
                        "Content (copy, labels, error messages)",
                        "Assets exported (icons, images, in correct formats)",
                        "Design tokens (colors, typography, spacing) in code format",
                        "Accessibility requirements specified",
                        "User flows documented"
                    ]
                },
                "with_backend_developer": {
                    "you_need": [
                        "API documentation (endpoints, request/response shapes)",
                        "Error response formats",
                        "Authentication requirements",
                        "Rate limiting information",
                        "Websocket connection details"
                    ],
                    "they_need": [
                        "Frontend requirements (what data you need)",
                        "Edge cases to handle",
                        "Performance expectations",
                        "Real-world usage patterns"
                    ]
                },
                "with_qa_engineer": {
                    "you_need": [
                        "Testing feedback on UI",
                        "Bug reports with reproduction steps",
                        "Input on test strategy",
                        "Accessibility testing"
                    ],
                    "they_need": [
                        "Testable UI (data-testid attributes)",
                        "Clear component states",
                        "Help writing automated tests",
                        "Access to development tools"
                    ]
                },
                "with_devops_engineer": {
                    "you_need": [
                        "Build pipeline setup",
                        "Environment configuration",
                        "Preview environments",
                        "Performance monitoring setup"
                    ],
                    "they_need": [
                        "Build requirements (Node version, env vars)",
                        "Dockerfile / build config",
                        "Asset optimization requirements",
                        "Help debugging performance issues"
                    ]
                }
            },
            "testing_strategy": {
                "testing_pyramid": {
                    "unit_tests": "70% - Test individual functions and components",
                    "integration_tests": "20% - Test user interactions and component integration (React Testing Library)",
                    "e2e_tests": "10% - Test complete user flows (Playwright, Cypress)"
                },
                "visual_regression": "Catch unintended UI changes with screenshot comparison",
                "accessibility_testing": "Use axe-core, test with screen readers, keyboard navigation"
            },
            "anti_patterns": [
                "Pixel-perfect obsession over user needs",
                "Ignoring accessibility until the end",
                "Not testing on real devices and browsers",
                "Over-engineering with complex frameworks when simple would work",
                "Not collaborating with designers early",
                "Ignoring performance until it's a problem",
                "Building custom components when design system has them",
                "Not handling error and loading states"
            ],
            "motto": "Build interfaces that users love, with code that developers don't hate. Delight is in the details - smooth animations, instant feedback, and experiences that just work."
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a Frontend Developer perspective.
        
        Args:
            query: The question or request
            **kwargs: Additional context (sprint_number, project_name, etc.)
            
        Returns:
            AgentResponse with Frontend Developer's perspective
        """
        query_lower = query.lower()
        
        # Initialize response
        response_text = ""
        recommendations = []
        questions = []
        requires_collaboration = False
        collaborating_roles = []
        evidence = {}
        
        # UI Implementation queries
        if any(term in query_lower for term in ["ui", "interface", "component", "design", "implement", "build"]):
            response_text += "I focus on delivering delightful, performant, and accessible user interfaces. "
            if "component" in query_lower or "build" in query_lower:
                response_text += "I'll build reusable, well-tested components following our design system. "
                recommendations.append("Use component-driven development for reusability")
                recommendations.append("Follow design system patterns and tokens")
                recommendations.append("Handle all states: default, loading, error, empty")
                recommendations.append("Ensure responsive design (mobile-first approach)")
                recommendations.append("Test with keyboard navigation and screen readers")
                questions.append("Do we have design specs for all states?")
                questions.append("What's the responsive behavior for different screen sizes?")
                requires_collaboration = True
                collaborating_roles = ["UX/UI Designer"]
        
        # Performance queries
        elif any(term in query_lower for term in ["performance", "slow", "optimize", "bundle", "lighthouse", "core web vitals"]):
            response_text += "Performance is critical for user experience. I optimize for Core Web Vitals. "
            recommendations.append("Target: LCP < 2.5s, FID/INP < 100ms, CLS < 0.1")
            recommendations.append("Code split and lazy load non-critical components")
            recommendations.append("Optimize images (responsive, modern formats, lazy loading)")
            recommendations.append("Keep initial bundle < 200KB gzipped")
            recommendations.append("Use React.memo, useMemo, useCallback to prevent unnecessary re-renders")
            recommendations.append("Implement virtual scrolling for long lists")
            questions.append("What's the current Lighthouse score?")
            questions.append("What are the biggest performance bottlenecks?")
            evidence["performance_budget"] = {
                "initial_bundle": "< 200KB gzipped",
                "time_to_interactive": "< 3 seconds",
                "lighthouse_score": "> 90"
            }
        
        # Accessibility queries
        elif any(term in query_lower for term in ["accessibility", "a11y", "wcag", "screen reader", "keyboard", "aria"]):
            response_text += "Accessibility is non-negotiable - everyone should be able to use our products. "
            recommendations.append("Use semantic HTML (not div soup)")
            recommendations.append("Ensure keyboard navigation works for all interactive elements")
            recommendations.append("Test with screen readers (NVDA, JAWS, VoiceOver)")
            recommendations.append("Meet WCAG 2.1 AA standards (4.5:1 contrast for text)")
            recommendations.append("Add ARIA attributes only when semantic HTML isn't enough")
            recommendations.append("Provide skip links and proper focus management")
            questions.append("Have we tested with real assistive technology?")
            questions.append("What's our current accessibility audit score?")
            requires_collaboration = True
            collaborating_roles = ["QA Engineer", "UX/UI Designer"]
        
        # Framework selection queries
        elif any(term in query_lower for term in ["framework", "react", "vue", "svelte", "nextjs", "remix", "which framework"]):
            response_text += "Framework selection depends on project requirements, team skills, and constraints. "
            recommendations.append("Evaluate: complexity, scale, team skills, performance budget, SEO needs")
            recommendations.append("Consider: React (complex UIs), Vue (simpler), Svelte (performance), Next.js (SSR/SEO)")
            recommendations.append("Prototype critical features in candidate frameworks")
            recommendations.append("Measure bundle size and performance")
            recommendations.append("Document decision in ADR (Architecture Decision Record)")
            questions.append("What are the project requirements? (complexity, scale, SEO?)")
            questions.append("What does the team know?")
            questions.append("What's the performance budget?")
            requires_collaboration = True
            collaborating_roles = ["Development Engineer", "Product Owner"]
        
        # Design system queries
        elif any(term in query_lower for term in ["design system", "component library", "storybook", "tokens"]):
            response_text += "A design system ensures consistency and speeds up development. "
            recommendations.append("Build reusable UI components (buttons, inputs, modals)")
            recommendations.append("Create layout primitives (grids, stacks, containers)")
            recommendations.append("Define styling tokens (colors, typography, spacing)")
            recommendations.append("Document components with Storybook or similar")
            recommendations.append("Maintain usage guidelines and examples")
            questions.append("Do we have design tokens defined?")
            questions.append("What components should we build first?")
            requires_collaboration = True
            collaborating_roles = ["UX/UI Designer"]
        
        # API integration queries
        elif any(term in query_lower for term in ["api", "fetch", "graphql", "websocket", "data", "integration"]):
            response_text += "I connect the frontend to backend services with proper error handling and loading states. "
            recommendations.append("Use modern data fetching libraries (React Query, SWR, Apollo Client)")
            recommendations.append("Implement optimistic UI updates for better UX")
            recommendations.append("Handle all error states gracefully")
            recommendations.append("Show loading states for async operations")
            recommendations.append("Implement retry logic for failed requests")
            recommendations.append("Cache data appropriately to reduce API calls")
            questions.append("What's the API contract? (endpoints, request/response shapes)")
            questions.append("How should we handle authentication?")
            requires_collaboration = True
            collaborating_roles = ["Development Engineer"]
        
        # Testing queries
        elif any(term in query_lower for term in ["test", "testing", "unit", "integration", "e2e", "playwright"]):
            response_text += "I follow the testing pyramid: 70% unit, 20% integration, 10% E2E. "
            recommendations.append("Unit tests for individual functions and components")
            recommendations.append("Integration tests with React Testing Library (test user interactions)")
            recommendations.append("E2E tests with Playwright or Cypress (test complete flows)")
            recommendations.append("Visual regression testing to catch unintended UI changes")
            recommendations.append("Accessibility testing with axe-core")
            recommendations.append("Test with keyboard navigation and screen readers")
            questions.append("What's our current test coverage?")
            questions.append("Which critical user flows need E2E tests?")
            requires_collaboration = True
            collaborating_roles = ["QA Engineer"]
        
        # Cross-browser queries
        elif any(term in query_lower for term in ["browser", "cross-browser", "safari", "chrome", "firefox", "mobile", "responsive"]):
            response_text += "I ensure consistent experience across modern browsers and devices. "
            recommendations.append("Test on Chrome, Firefox, Safari, Edge (latest 2 versions)")
            recommendations.append("Test on iOS Safari and Chrome Android")
            recommendations.append("Use progressive enhancement for older browsers")
            recommendations.append("Test performance on low-end devices")
            recommendations.append("Use mobile-first responsive design")
            questions.append("What browsers/devices do our users primarily use?")
            questions.append("Do we need to support older browsers?")
        
        # Collaboration with Designer queries
        elif any(term in query_lower for term in ["designer", "figma", "design", "handoff", "collaboration"]):
            response_text += "I work closely with UX/UI Designer from design review to implementation. "
            recommendations.append("Review designs before Sprint Planning for technical feasibility")
            recommendations.append("Identify missing states (loading, error, empty) early")
            recommendations.append("Show work-in-progress in browser (not wait until perfect)")
            recommendations.append("Flag design challenges proactively and constructively")
            recommendations.append("Propose alternatives when designs hurt UX or performance")
            recommendations.append("Ensure design handoff includes all states, breakpoints, and tokens")
            questions.append("Do we have designs for all states?")
            questions.append("Are responsive breakpoints defined?")
            questions.append("Do we have design tokens in code format?")
            requires_collaboration = True
            collaborating_roles = ["UX/UI Designer"]
        
        # General Frontend queries
        else:
            response_text = "As the Frontend Developer, I deliver delightful, performant, accessible user interfaces. "
            response_text += "My focus areas include: UI implementation, frontend architecture, design systems, "
            response_text += "performance optimization, accessibility, and close collaboration with UX/UI Designer. "
            response_text += "I participate in all Scrum events and work closely with Backend Developers, "
            response_text += "QA Engineers, and DevOps Engineers. "
            recommendations.append("Prioritize user experience in all technical decisions")
            recommendations.append("Build accessible interfaces from the start (not as an afterthought)")
            recommendations.append("Optimize for Core Web Vitals (LCP, FID/INP, CLS)")
            recommendations.append("Use component-driven development and design systems")
            recommendations.append("Test thoroughly (unit, integration, E2E, accessibility)")
            recommendations.append("Collaborate closely with designers from design to implementation")
        
        # Add performance context
        if not evidence.get("performance_budget"):
            evidence["core_web_vitals"] = {
                "lcp": "Largest Contentful Paint - < 2.5s",
                "fid_inp": "First Input Delay / Interaction to Next Paint - < 100ms",
                "cls": "Cumulative Layout Shift - < 0.1"
            }
        
        return AgentResponse(
            role=self.role,
            response=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=requires_collaboration,
            collaborating_roles=collaborating_roles,
            evidence=evidence
        )
