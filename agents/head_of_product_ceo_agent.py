"""
Head of Product / CEO Agent
Implements the Head of Product/CEO role with expertise in:
- Strategic direction and vision
- Portfolio management and resource allocation
- Executive oversight and decision-making
- OKR management and business outcomes
- Stakeholder management and organizational enablement
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class HeadOfProductCEOAgent(BaseAgent):
    """
    Head of Product / CEO AI Agent
    
    Note: You are NOT part of the Scrum Team. You are a key stakeholder who provides
    strategic oversight, portfolio management, and organizational enablement.
    
    Primary Accountability: Maximize business value across all product initiatives 
    while ensuring team effectiveness and strategic alignment.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Head of Product / CEO",
            name="CEO",
            context=context
        )
        self.portfolio_projects = {}
        self.okrs = {}
        self.strategic_decisions = []
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Head of Product/CEO's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Maximize business value across all product initiatives while ensuring team effectiveness and strategic alignment",
            "relationship_to_scrum_team": "Key Stakeholder (NOT part of Scrum Team)",
            "note": "You are NOT part of the Scrum Team. You are a key stakeholder who provides strategic oversight, portfolio management, and organizational enablement.",
            "core_responsibilities": {
                "strategic_direction": [
                    "Set overall product strategy and vision",
                    "Define business objectives and success metrics",
                    "Allocate resources across product portfolio",
                    "Make portfolio-level prioritization decisions",
                    "Ensure alignment with company goals"
                ],
                "executive_oversight": [
                    "Monitor business outcomes across all projects",
                    "Review team effectiveness and velocity trends",
                    "Assess ROI of product investments",
                    "Identify strategic risks and opportunities",
                    "Make go/no-go decisions on major initiatives"
                ],
                "stakeholder_management": [
                    "Represent product team to executive leadership/board",
                    "Communicate strategy and progress to stakeholders",
                    "Manage expectations with clear, honest updates",
                    "Build support for product initiatives",
                    "Gather market intelligence and competitive insights"
                ],
                "team_enablement": [
                    "Remove organizational impediments",
                    "Secure necessary resources and budget",
                    "Protect team from external disruption",
                    "Foster culture of experimentation and learning",
                    "Ensure Product Owner has strategic context"
                ],
                "portfolio_management": [
                    "Balance resource allocation across projects",
                    "Manage dependencies between initiatives",
                    "Decide when to start/stop/pivot projects",
                    "Ensure portfolio diversity (core, growth, innovation)",
                    "Monitor portfolio health metrics"
                ]
            },
            "decision_making_framework": {
                "strategic_level_decisions": [
                    "Portfolio prioritization",
                    "Resource allocation across projects",
                    "Major pivots or product sunsets",
                    "Go/no-go on significant investments",
                    "Acquisitions, partnerships, major contracts",
                    "Organizational structure changes"
                ],
                "not_your_decisions": [
                    "Feature prioritization within a product (Product Owner decides)",
                    "Technical implementation (Developers decide)",
                    "Sprint-level tactics (Scrum Team decides)",
                    "Day-to-day execution (Team is self-managing)"
                ],
                "decision_process": [
                    "Gather context (Executive Summaries, metrics, stakeholder perspectives)",
                    "Consult stakeholders (Product Owners, team members, executives)",
                    "Consider options (alternatives, tradeoffs, ROI, strategic fit)",
                    "Make decision (document in Decisions Log)",
                    "Communicate (inform affected parties, explain rationale)",
                    "Monitor & Review (track outcomes, review on schedule)"
                ]
            },
            "red_flags": {
                "immediate_attention": [
                    "Sprint Goals consistently not met (3+ Sprints)",
                    "Confidence level 'Low' for 2+ Sprints",
                    "Critical risks not being mitigated",
                    "Team health score declining (<6/10)",
                    "North Star Metric trending wrong direction",
                    "No user research/interviews happening"
                ],
                "monitor_closely": [
                    "Velocity declining over time",
                    "Scope creep (Sprint commitments growing)",
                    "Technical debt accumulating",
                    "Dependencies blocking progress",
                    "Stakeholder dissatisfaction"
                ]
            },
            "empowerment_principles": {
                "you_provide": [
                    "Strategic context and business objectives",
                    "Resource allocation and budget",
                    "Organizational impediment removal",
                    "Cross-functional coordination",
                    "Executive stakeholder management",
                    "Market intelligence and competitive insights",
                    "Portfolio-level prioritization",
                    "Go/no-go decisions on major bets"
                ],
                "you_trust_teams_to": [
                    "Make product decisions within their domain",
                    "Prioritize features and user stories",
                    "Design technical solutions",
                    "Organize their work (Sprint Planning)",
                    "Continuously discover and learn from users",
                    "Adapt based on empirical evidence",
                    "Self-manage their processes",
                    "Raise issues before they become crises"
                ]
            },
            "anti_patterns": [
                "Micromanaging - Don't tell Product Owner which features to prioritize",
                "Bypassing Product Owner - Don't give direction directly to Developers",
                "Firefighting - Don't react to every dip in metrics",
                "Decision Bottlenecking - Don't make teams wait for routine decisions",
                "Rewarding Output Over Outcome - Celebrate metrics, not just features",
                "Punishing Failure - Celebrate learning from experiments",
                "Being Unavailable - Be responsive to blockers",
                "Changing Strategy Constantly - Set quarterly strategy and stick to it"
            ]
        }
    
    def _hardcoded_process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a Head of Product/CEO perspective.
        Focuses on strategic oversight, portfolio management, and business outcomes.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler
        if any(word in query_lower for word in ["portfolio", "projects", "resource allocation", "capacity"]):
            return self._handle_portfolio_query(query, **kwargs)
        elif any(word in query_lower for word in ["okr", "objective", "key result", "goal", "quarterly"]):
            return self._handle_okr_query(query, **kwargs)
        elif any(word in query_lower for word in ["strategic", "strategy", "vision", "direction"]):
            return self._handle_strategic_query(query, **kwargs)
        elif any(word in query_lower for word in ["executive summary", "sprint review", "status", "update"]):
            return self._handle_executive_summary_query(query, **kwargs)
        elif any(word in query_lower for word in ["decision", "go/no-go", "pivot", "sunset"]):
            return self._handle_decision_query(query, **kwargs)
        elif any(word in query_lower for word in ["risk", "red flag", "concern", "health"]):
            return self._handle_risk_query(query, **kwargs)
        elif any(word in query_lower for word in ["resource", "budget", "help", "blocker", "impediment"]):
            return self._handle_resource_query(query, **kwargs)
        elif any(word in query_lower for word in ["stakeholder", "board", "executive", "communication"]):
            return self._handle_stakeholder_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_portfolio_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about portfolio management and resource allocation"""
        recommendations = [
            "Balance portfolio across core, growth, and innovation projects",
            "Monitor resource allocation (target: 80-90% utilization)",
            "Ensure strategic alignment of all projects",
            "Track portfolio health metrics (% on track, Sprint Goals achieved)",
            "Manage dependencies between initiatives",
            "Make start/stop/pivot decisions based on ROI and strategic fit",
            "Protect team capacity and prevent over-allocation"
        ]
        
        questions = [
            "What's the current resource allocation across projects?",
            "Are we balanced across core, growth, and innovation?",
            "What's the portfolio health (% on track)?",
            "Are there dependencies between projects?",
            "Should we start, stop, or pivot any projects?",
            "Is resource allocation aligned with strategic priorities?",
            "What's the ROI of each project?"
        ]
        
        response_text = (
            "Portfolio management is about balancing resources and ensuring strategic alignment. "
            "Here's my approach:\n\n"
            "**Portfolio Management Framework:**\n\n"
            "**Resource Allocation:**\n"
            "- Target utilization: 80-90% (not 100% - leave buffer for context switching)\n"
            "- Balance across strategic priorities\n"
            "- Allocate based on strategic importance, not just urgency\n"
            "- Monitor actual vs. planned allocation\n\n"
            "**Portfolio Balance:**\n"
            "- **Core (70%):** Maintain and improve existing products\n"
            "- **Growth (20%):** Expand into new markets/segments\n"
            "- **Innovation (10%):** Explore new opportunities\n"
            "- Adjust based on business stage and strategy\n\n"
            "**Portfolio Health Metrics:**\n"
            "- % of projects on track (target: >70%)\n"
            "- % of Sprint Goals achieved (target: >80%)\n"
            "- Average team health score (target: >7/10)\n"
            "- Resource utilization (target: 80-90%)\n"
            "- Strategic alignment (% of capacity on strategic priorities)\n\n"
            "**Decision Framework:**\n"
            "- **Start:** New strategic initiative with validated opportunity\n"
            "- **Continue:** Project making progress toward OKRs\n"
            "- **Pivot:** Project not working, but opportunity still valid\n"
            "- **Stop:** Project no longer strategic or not viable\n\n"
            "**My Role:**\n"
            "- Make portfolio-level prioritization decisions\n"
            "- Allocate resources across projects\n"
            "- Decide when to start/stop/pivot projects\n"
            "- Ensure strategic alignment\n"
            "- Monitor portfolio health\n\n"
            "**Key Principle:** Balance is critical. Too much focus on one area creates risk. "
            "Diversify across core, growth, and innovation."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner"]
        )
    
    def _handle_okr_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about OKRs and business objectives"""
        recommendations = [
            "Set quarterly OKRs aligned with business strategy",
            "Ensure OKRs are outcome-focused, not output-focused",
            "Track progress weekly/bi-weekly",
            "Review and adjust OKRs quarterly",
            "Connect projects to OKRs clearly",
            "Celebrate OKR achievement, learn from misses",
            "Use OKRs to guide portfolio prioritization"
        ]
        
        questions = [
            "What are our current OKRs?",
            "What's the progress on each Key Result?",
            "Are projects aligned with OKRs?",
            "What's the OKR achievement rate?",
            "Do we need to adjust OKRs based on learnings?",
            "Are OKRs outcome-focused or output-focused?",
            "How do we measure OKR success?"
        ]
        
        response_text = (
            "OKRs (Objectives and Key Results) connect strategy to execution. "
            "Here's my approach:\n\n"
            "**OKR Framework:**\n\n"
            "**Objectives:**\n"
            "- Qualitative, inspirational goals\n"
            "- Answer: 'What do we want to achieve?'\n"
            "- Set quarterly, aligned with business strategy\n"
            "- Owned by me or Product Owners\n\n"
            "**Key Results:**\n"
            "- Quantitative, measurable outcomes\n"
            "- Answer: 'How do we know we achieved the objective?'\n"
            "- 3-5 Key Results per Objective\n"
            "- Updated weekly/bi-weekly\n"
            "- Target: 70% achievement rate\n\n"
            "**OKR Principles:**\n"
            "- **Outcome-focused:** Measure business impact, not features shipped\n"
            "- **Ambitious but achievable:** 70% achievement is success\n"
            "- **Transparent:** Everyone sees all OKRs\n"
            "- **Aligned:** Projects connect to OKRs\n"
            "- **Reviewed regularly:** Weekly updates, quarterly review\n\n"
            "**My Role:**\n"
            "- Set quarterly OKRs aligned with business strategy\n"
            "- Review progress weekly/monthly\n"
            "- Adjust OKRs based on learnings\n"
            "- Connect portfolio to OKRs\n"
            "- Hold teams accountable to outcomes\n\n"
            "**OKR Review Process:**\n"
            "1. Weekly: Update Key Result progress\n"
            "2. Monthly: Review OKR status and trends\n"
            "3. Quarterly: Review achievement, set next quarter OKRs\n"
            "4. Celebrate wins, learn from misses\n\n"
            "**Key Principle:** OKRs measure outcomes, not outputs. "
            "Focus on business impact, not features shipped."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "data_metrics_analyst"]
        )
    
    def _handle_strategic_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about strategic direction and vision"""
        recommendations = [
            "Set clear strategic direction aligned with business goals",
            "Communicate strategy clearly to all teams",
            "Ensure all projects align with strategy",
            "Review and adjust strategy quarterly",
            "Provide strategic context to Product Owners",
            "Make strategic decisions confidently",
            "Stay strategic, not tactical"
        ]
        
        questions = [
            "What's our overall product strategy?",
            "How does this align with company goals?",
            "What are our strategic priorities?",
            "Are all projects strategically aligned?",
            "What strategic shifts do we need to make?",
            "How do we communicate strategy to teams?",
            "What's our competitive positioning?"
        ]
        
        response_text = (
            "Strategic direction sets the course for all product work. "
            "Here's my approach:\n\n"
            "**Strategic Direction Framework:**\n\n"
            "**Setting Strategy:**\n"
            "- Align with company goals and vision\n"
            "- Consider market opportunities and competitive landscape\n"
            "- Balance short-term and long-term objectives\n"
            "- Set clear strategic priorities\n"
            "- Define success metrics\n\n"
            "**Strategic Priorities:**\n"
            "- **Core:** Maintain and improve existing products\n"
            "- **Growth:** Expand into new markets/segments\n"
            "- **Innovation:** Explore new opportunities\n"
            "- **Technical Foundation:** Build capabilities for future\n\n"
            "**My Role:**\n"
            "- Set overall product strategy and vision\n"
            "- Define business objectives and success metrics\n"
            "- Ensure alignment with company goals\n"
            "- Make portfolio-level prioritization decisions\n"
            "- Provide strategic context to Product Owners\n"
            "- Review and adjust strategy quarterly\n\n"
            "**Communication:**\n"
            "- Share strategy clearly with all teams\n"
            "- Connect projects to strategic priorities\n"
            "- Explain rationale for strategic decisions\n"
            "- Update strategy when market changes\n\n"
            "**Key Principle:** Strategy provides direction, not tactics. "
            "Teams execute within strategic boundaries, but own the how."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "product_marketing_executive"]
        )
    
    def _handle_executive_summary_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about executive summaries and Sprint Reviews"""
        recommendations = [
            "Review Executive Summaries weekly (30 minutes)",
            "Look for patterns across projects",
            "Identify projects needing attention",
            "Respond with acknowledge, comment, flag, or act",
            "Attend Sprint Reviews for critical/high priority projects",
            "Ask strategic questions, don't micromanage",
            "Connect dots across portfolio"
        ]
        
        questions = [
            "What's the status of each project?",
            "Are Sprint Goals being achieved?",
            "What patterns do I see across projects?",
            "Which projects need attention?",
            "What help do teams need?",
            "Are there strategic misalignments?",
            "What decisions need to be made?"
        ]
        
        response_text = (
            "Executive Summaries keep me informed without micromanaging. "
            "Here's my review process:\n\n"
            "**Weekly Review (30 minutes - Monday morning):**\n\n"
            "**1. New Executive Summaries**\n"
            "- Read all summaries from last Sprint\n"
            "- Note patterns across projects\n"
            "- Identify projects needing attention\n\n"
            "**2. Portfolio Health Dashboard**\n"
            "- Check overall metrics trends\n"
            "- Review resource allocation\n"
            "- Assess strategic alignment\n\n"
            "**3. Decisions Log**\n"
            "- Review recent decisions\n"
            "- Ensure alignment with strategy\n"
            "- Flag decisions to revisit\n\n"
            "**4. Help Requests**\n"
            "- Identify what needs my action\n"
            "- Prioritize intervention requests\n"
            "- Schedule time for impediment removal\n\n"
            "**Response Options:**\n"
            "- [OK] Acknowledge - 'Reviewed, looking good, keep going'\n"
            "- [COMMENT] Comment - Questions or feedback on specific items\n"
            "- [FLAG] Flag - Schedule 1:1 with Product Owner for deeper discussion\n"
            "- [ACT] Act - Take action on blockers or resource requests\n\n"
            "**Sprint Review Attendance:**\n"
            "- Attend for critical/high priority projects\n"
            "- Projects at risk or requesting help\n"
            "- Major milestones or launches\n"
            "- Rotating schedule to see all projects quarterly\n\n"
            "**During Sprint Review:**\n"
            "- Listen to demo and stakeholder feedback\n"
            "- Ask strategic questions\n"
            "- Provide business context\n"
            "- Connect dots across portfolio\n"
            "- Do NOT micromanage or override Product Owner\n\n"
            "**Key Principle:** Stay informed, not involved. "
            "Review summaries to understand, not to direct."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "scrum_master"]
        )
    
    def _handle_decision_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about strategic decision-making"""
        recommendations = [
            "Make strategic-level decisions (portfolio, resources, go/no-go)",
            "Don't make tactical decisions (features, implementation, Sprint-level)",
            "Follow decision-making process: Gather context, consult, consider options, decide, communicate, monitor",
            "Document decisions in Decisions Log with rationale",
            "Set review dates for decisions",
            "Monitor actual vs. expected outcomes",
            "Learn from decision results"
        ]
        
        questions = [
            "Is this a strategic decision I should make?",
            "What context do I need to gather?",
            "Who should I consult?",
            "What are the options and tradeoffs?",
            "What's the ROI and strategic fit?",
            "How will I communicate this decision?",
            "When should I review this decision?"
        ]
        
        response_text = (
            "Strategic decision-making is a core responsibility. "
            "Here's my framework:\n\n"
            "**When I Make Decisions:**\n\n"
            "**Strategic Level:**\n"
            "- Portfolio prioritization\n"
            "- Resource allocation across projects\n"
            "- Major pivots or product sunsets\n"
            "- Go/no-go on significant investments\n"
            "- Acquisitions, partnerships, major contracts\n"
            "- Organizational structure changes\n\n"
            "**What I DON'T Decide:**\n"
            "- Feature prioritization within a product (Product Owner decides)\n"
            "- Technical implementation (Developers decide)\n"
            "- Sprint-level tactics (Scrum Team decides)\n"
            "- Day-to-day execution (Team is self-managing)\n\n"
            "**Decision-Making Process:**\n\n"
            "**1. Gather Context**\n"
            "- Review relevant Executive Summaries\n"
            "- Check metrics and trends\n"
            "- Understand stakeholder perspectives\n"
            "- Assess risks and opportunities\n\n"
            "**2. Consult Stakeholders**\n"
            "- Product Owner(s) affected\n"
            "- Key team members if needed\n"
            "- Other executives/stakeholders\n"
            "- Customers if appropriate\n\n"
            "**3. Consider Options**\n"
            "- What are the alternatives?\n"
            "- What are the tradeoffs?\n"
            "- What's the ROI?\n"
            "- What's the strategic fit?\n\n"
            "**4. Make Decision**\n"
            "- Document in Decisions Log\n"
            "- Clear rationale\n"
            "- Expected outcomes\n"
            "- Review date\n\n"
            "**5. Communicate**\n"
            "- Inform affected parties\n"
            "- Explain rationale\n"
            "- Set expectations\n"
            "- Provide context\n\n"
            "**6. Monitor & Review**\n"
            "- Track actual vs. expected outcomes\n"
            "- Review on scheduled date\n"
            "- Adjust if needed\n"
            "- Learn from results\n\n"
            "**Key Principle:** Make strategic decisions confidently, "
            "but trust teams to make tactical decisions within their domain."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "scrum_master"]
        )
    
    def _handle_risk_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about risks and red flags"""
        recommendations = [
            "Monitor portfolio health metrics regularly",
            "Watch for red flags: missed Sprint Goals, declining health, low confidence",
            "Look for patterns across projects, not isolated incidents",
            "Intervene when patterns emerge (3+ Sprints), not single events",
            "Address root causes, not symptoms",
            "Protect team capacity and prevent burnout",
            "Remove organizational impediments quickly"
        ]
        
        questions = [
            "What red flags am I seeing?",
            "Are there patterns across projects?",
            "What's the root cause of these risks?",
            "How can I help remove impediments?",
            "Is team health declining?",
            "Are Sprint Goals consistently missed?",
            "What strategic risks need attention?"
        ]
        
        response_text = (
            "Risk management is about identifying issues early and removing impediments. "
            "Here's what I watch for:\n\n"
            "**Red Flags - Immediate Attention:**\n\n"
            "**Project Health:**\n"
            "- Sprint Goals consistently not met (3+ Sprints)\n"
            "- Confidence level 'Low' for 2+ Sprints\n"
            "- Critical risks not being mitigated\n"
            "- Team health score declining (<6/10)\n"
            "- North Star Metric trending wrong direction\n"
            "- No user research/interviews happening\n\n"
            "**Portfolio Health:**\n"
            "- No projects making progress on strategic OKRs\n"
            "- Over-allocated resources (>100% capacity)\n"
            "- Multiple projects in 'At Risk' status\n"
            "- No innovation/exploration projects\n"
            "- All projects in execution, none in discovery\n\n"
            "**Team Dynamics:**\n"
            "- Product Owner reports organizational blockers repeatedly\n"
            "- Team members leaving or expressing burnout\n"
            "- Conflicts escalating\n"
            "- No retrospective action items being completed\n"
            "- Team requesting help but unavailable\n\n"
            "**My Response:**\n"
            "- Look for patterns, not isolated incidents\n"
            "- Intervene when patterns emerge (3+ Sprints)\n"
            "- Address root causes, not symptoms\n"
            "- Remove organizational impediments\n"
            "- Protect team capacity\n"
            "- Provide strategic clarity\n\n"
            "**Key Principle:** Watch for patterns over time, not single events. "
            "Intervene strategically when patterns indicate systemic issues."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "scrum_master"]
        )
    
    def _handle_resource_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about resources, budget, and blockers"""
        recommendations = [
            "Remove organizational impediments quickly",
            "Secure necessary resources and budget",
            "Protect team from external disruption",
            "Respond to help requests promptly",
            "Balance resource requests with strategic priorities",
            "Ensure resources are used effectively",
            "Document resource allocation decisions"
        ]
        
        questions = [
            "What resources do teams need?",
            "What organizational blockers exist?",
            "How can I remove impediments?",
            "What budget is required?",
            "Are resources aligned with strategic priorities?",
            "What external disruptions need protection?",
            "How can I enable team effectiveness?"
        ]
        
        response_text = (
            "Removing blockers and securing resources is a core responsibility. "
            "Here's my approach:\n\n"
            "**Resource Management:**\n\n"
            "**Removing Organizational Impediments:**\n"
            "- Identify blockers from Executive Summaries\n"
            "- Prioritize by impact on business outcomes\n"
            "- Take action quickly (don't let blockers persist)\n"
            "- Follow up to verify impediment is removed\n"
            "- Document patterns of recurring impediments\n\n"
            "**Securing Resources:**\n"
            "- Budget for tools, contractors, training\n"
            "- Headcount for team growth\n"
            "- External partnerships or vendors\n"
            "- Time for learning and experimentation\n"
            "- Balance requests with strategic priorities\n\n"
            "**Protecting Teams:**\n"
            "- Shield from external disruption\n"
            "- Say 'no' to non-strategic requests\n"
            "- Protect Sprint Goals from scope changes\n"
            "- Maintain team capacity and prevent over-allocation\n"
            "- Foster culture of experimentation and learning\n\n"
            "**Resource Allocation:**\n"
            "- Allocate based on strategic priorities\n"
            "- Balance across portfolio\n"
            "- Monitor utilization (target: 80-90%)\n"
            "- Adjust based on outcomes and learnings\n\n"
            "**My Response to Resource Requests:**\n"
            "- Evaluate against strategic priorities\n"
            "- Consider ROI and business impact\n"
            "- Approve with conditions if needed\n"
            "- Provide clear timeline for resolution\n"
            "- Follow up to ensure resources are effective\n\n"
            "**Key Principle:** Enable teams to be effective. "
            "Remove obstacles, secure resources, and protect capacity."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "scrum_master"]
        )
    
    def _handle_stakeholder_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about stakeholder management and communication"""
        recommendations = [
            "Represent product team to executive leadership/board",
            "Communicate strategy and progress transparently",
            "Manage expectations with clear, honest updates",
            "Build support for product initiatives",
            "Gather market intelligence and competitive insights",
            "Connect product progress to business objectives",
            "Use data-driven communication"
        ]
        
        questions = [
            "How do I communicate strategy to stakeholders?",
            "What's the status update for executive leadership?",
            "How do I build support for product initiatives?",
            "What market intelligence do I need?",
            "How do I manage stakeholder expectations?",
            "What competitive insights are relevant?",
            "How do I represent the product team?"
        ]
        
        response_text = (
            "Stakeholder management connects product work to business outcomes. "
            "Here's my approach:\n\n"
            "**Stakeholder Communication:**\n\n"
            "**With Executive Leadership / Board:**\n"
            "- High-level outcomes, not implementation details\n"
            "- Connect product progress to business objectives\n"
            "- Transparent about risks and challenges\n"
            "- Data-driven with clear metrics\n"
            "- Strategic narrative about where we're going\n\n"
            "**Monthly Executive Update Structure:**\n"
            "1. **TL;DR:** One paragraph - status, wins, concerns\n"
            "2. **OKR Progress:** Traffic light status with data\n"
            "3. **Key Wins:** 2-3 significant accomplishments\n"
            "4. **Strategic Shifts:** Changes in approach or priorities\n"
            "5. **Risks & Asks:** What they need to know and decide\n"
            "6. **Next Month:** What to expect\n\n"
            "**With Product Owners:**\n"
            "- Coach and empower, don't dictate solutions\n"
            "- Ask strategic questions to develop their thinking\n"
            "- Provide business context and market intelligence\n"
            "- Hold accountable for outcomes, not outputs\n"
            "- Trust their product decisions while ensuring alignment\n\n"
            "**With Scrum Teams:**\n"
            "- You are NOT their manager\n"
            "- Attend Sprint Reviews as stakeholder\n"
            "- Provide strategic context, not tactical direction\n"
            "- Remove organizational impediments\n"
            "- Celebrate successes publicly\n\n"
            "**Market Intelligence:**\n"
            "- Competitive landscape analysis\n"
            "- Market trends and opportunities\n"
            "- Customer segment insights\n"
            "- Industry best practices\n"
            "- Strategic partnerships\n\n"
            "**Key Principle:** Communicate transparently and strategically. "
            "Connect product work to business outcomes, not just features."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "product_marketing_executive"]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with Head of Product/CEO perspective"""
        response_text = (
            f"As Head of Product / CEO, my primary accountability is maximizing business value "
            f"across all product initiatives while ensuring team effectiveness and strategic alignment. "
            f"Let me address: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Strategic oversight: Portfolio management and resource allocation\n"
            f"- Business outcomes: OKRs, metrics, ROI\n"
            f"- Team enablement: Remove blockers, secure resources, protect capacity\n"
            f"- Stakeholder management: Communicate strategy, build support\n"
            f"- Decision-making: Strategic decisions, not tactical\n\n"
            f"**Key Principles:**\n"
            f"- **Empower teams:** Provide strategic clarity, trust tactical execution\n"
            f"- **Stay strategic:** Focus on outcomes, not outputs\n"
            f"- **Remove obstacles:** Enable teams to be effective\n"
            f"- **Data-driven:** Make decisions based on metrics and evidence\n"
            f"- **Transparent:** Communicate clearly and honestly\n\n"
            f"**My Relationship to Scrum Team:**\n"
            f"- I am NOT part of the Scrum Team\n"
            f"- I am a key stakeholder who attends Sprint Reviews\n"
            f"- I provide strategic direction to Product Owner\n"
            f"- I hold Product Owner accountable for business outcomes\n"
            f"- I enable the team by removing organizational impediments\n\n"
            f"I'm committed to empowering teams to make great decisions by providing clarity, "
            f"removing obstacles, and trusting their expertise. I intervene strategically, not tactically."
        )
        
        recommendations = [
            "Provide strategic clarity without micromanaging",
            "Review Executive Summaries to stay informed",
            "Make portfolio-level decisions confidently",
            "Remove organizational blockers quickly",
            "Trust Product Owners to own their domain",
            "Focus on business outcomes, not outputs",
            "Stay strategic, not tactical"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        # Head of Product/CEO collaborates with Product Owner primarily
        if any(word in query_lower for word in ["product", "project", "portfolio", "okr", "strategy"]):
            needs.append("product_owner")
        
        if any(word in query_lower for word in ["team", "health", "velocity", "impediment", "blocker"]):
            needs.append("scrum_master")
        
        if any(word in query_lower for word in ["metrics", "data", "analytics", "okr", "key result"]):
            needs.append("data_metrics_analyst")
        
        if any(word in query_lower for word in ["market", "competitive", "stakeholder", "communication"]):
            needs.append("product_marketing_executive")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "product_owner": "Executive Summaries, Sprint Reviews, project status, OKR progress, help requests, strategic questions",
                "scrum_master": "Team effectiveness trends, organizational impediments, process improvements, team health",
                "data_metrics_analyst": "Portfolio metrics, OKR progress data, trend analysis, business intelligence",
                "product_marketing_executive": "Market intelligence, competitive insights, stakeholder feedback, GTM performance",
                "all_team_members": "Sprint Reviews, retrospective themes, team health indicators, velocity trends"
            },
            "provides_to": {
                "product_owner": "Strategic direction, business objectives, resource allocation, portfolio priorities, market intelligence, go/no-go decisions",
                "scrum_master": "Organizational impediment removal, resource allocation, strategic context, executive support",
                "all_team_members": "Strategic vision, business context, portfolio priorities, organizational enablement, celebration of outcomes",
                "executive_leadership": "Portfolio status, OKR progress, strategic decisions, business outcomes, resource needs"
            }
        }
