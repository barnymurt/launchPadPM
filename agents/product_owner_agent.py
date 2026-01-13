"""
Product Owner Agent
Implements the Product Owner role with expertise in:
- Maximizing product value through evidence-based decision making
- Product Backlog management and prioritization
- Continuous discovery habits and customer research
- Opportunity Solution Trees (OST) framework
- Stakeholder engagement and value articulation
"""

from typing import Dict, List, Any, Optional, Tuple
from .base_agent import BaseAgent, AgentResponse, AgentContext
import re


class ProductOwnerAgent(BaseAgent):
    """
    Product Owner AI Agent
    
    Primary Accountability: Maximizing the value of the product resulting 
    from the work of the Scrum Team.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Product Owner",
            name="PO",
            context=context
        )
        self.product_goal = ""
        self.ost_state = {
            "outcome": "",
            "opportunities": [],
            "solutions": [],
            "assumptions": []
        }
        self.customer_interviews_count = 0
        self.last_interview_week = 0
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Product Owner's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Maximizing the value of the product resulting from the work of the Scrum Team",
            "key_responsibilities": [
                "Product Backlog Management (developing Product Goal, creating/ordering items, ensuring transparency)",
                "Value Maximization (understanding customer needs, making release decisions, optimizing Sprint value)",
                "Stakeholder Engagement (identifying stakeholders, representing needs, leading collaboration)"
            ],
            "scrum_events": {
                "sprint_planning": "Ensure team understands most important Product Backlog items and how they map to Product Goal",
                "daily_scrum": "Optional attendance - may attend to listen",
                "sprint_review": "Explain what has been 'Done' and what hasn't, discuss Product Backlog",
                "sprint_retrospective": "Inspect last Sprint and plan improvements"
            },
            "continuous_discovery": {
                "weekly_minimum": "At least one customer interview per week (story-based, not hypothetical)",
                "interview_technique": "Story-based: Ask for specific stories, not opinions",
                "follow_up_questions": [
                    "What happened before that?",
                    "What were you trying to accomplish?",
                    "What made that difficult?",
                    "How did you solve that?",
                    "What would have made it easier?"
                ]
            },
            "opportunity_solution_trees": {
                "structure": "Outcome → Opportunities → Solutions → Assumptions",
                "principles": [
                    "Outcome-oriented (focus on results, not features)",
                    "Based on real customer stories, not assumptions",
                    "Test assumptions before building",
                    "Continuous discovery and regular tree updates",
                    "Makes strategy visible and enables evidence-based decisions"
                ]
            },
            "prioritization_model": {
                "formula": "(User Value + Time Criticality + Risk Reduction) / Effort",
                "factors": {
                    "user_value": "1-10: How much users benefit immediately",
                    "time_criticality": "1-10: Cost of delay",
                    "risk_reduction": "1-10: How much this reduces uncertainty",
                    "effort": "1-10: Size/complexity (higher = more effort)"
                },
                "rule": "Highest score = highest priority"
            },
            "anti_patterns": [
                "Don't become a 'requirements provider' - maximize value, not just write requirements",
                "Don't accept 'everything is high priority' - ordering is your superpower",
                "Don't go 3+ weeks without customer contact - continuous discovery is mandatory",
                "Don't make assumptions without evidence - base decisions on data, not opinions",
                "Don't let features pile up in backlog without ordering",
                "Don't create 'displacive' summaries - point to sources, don't replace them"
            ],
            "wisdom_patterns": {
                "product_goal_connection_test": "For every Product Backlog item, ask: 'How does this item move us toward the Product Goal?'",
                "evidence_over_opinions": "Data beats HiPPO (Highest Paid Person's Opinion)",
                "small_bets_before_big_builds": "Test cheaply before building expensively"
            }
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a Product Owner perspective.
        Focuses on value, priority, customer needs, and evidence-based decision making.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler
        if any(word in query_lower for word in ["prioritize", "priority", "prioritization", "order", "ranking"]):
            return self._handle_prioritization_query(query, **kwargs)
        elif any(word in query_lower for word in ["ost", "opportunity solution tree", "opportunity", "solution tree"]):
            return self._handle_ost_query(query, **kwargs)
        elif any(word in query_lower for word in ["interview", "customer", "discovery", "user research"]):
            return self._handle_discovery_query(query, **kwargs)
        elif any(word in query_lower for word in ["backlog", "product backlog", "pbi", "backlog item"]):
            return self._handle_backlog_query(query, **kwargs)
        elif any(word in query_lower for word in ["product goal", "goal", "outcome"]):
            return self._handle_product_goal_query(query, **kwargs)
        elif any(word in query_lower for word in ["should we", "add", "build", "feature", "implement"]):
            return self._handle_feature_decision_query(query, **kwargs)
        elif any(word in query_lower for word in ["estimate", "effort", "size", "complexity"]):
            return self._handle_estimation_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_prioritization_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about prioritization"""
        recommendations = [
            "Use the prioritization framework: (User Value + Time Criticality + Risk Reduction) / Effort",
            "For each item, score User Value (1-10) based on customer research - how many users need this? How painful is the problem?",
            "Score Time Criticality (1-10) - what's the cost of delay?",
            "Score Risk Reduction (1-10) - does this validate a key assumption?",
            "Get Effort estimates (1-10) from Development Team - higher = more effort",
            "Calculate Priority Score = (User Value + Time Criticality + Risk Reduction) / Effort",
            "Highest score = highest priority",
            "Verify each item connects to the Product Goal - if not, it shouldn't be on the backlog right now"
        ]
        
        questions = [
            "What evidence do we have from customer interviews about user value?",
            "What's the cost of delay for each item?",
            "Which items reduce the most uncertainty or risk?",
            "What are the effort estimates from the Development Team?",
            "How does each item connect to our Product Goal?"
        ]
        
        response_text = (
            "As Product Owner, prioritization is one of my core responsibilities. Let's use our "
            "evidence-based prioritization framework.\n\n"
            "**Prioritization Formula:**\n"
            "Priority Score = (User Value + Time Criticality + Risk Reduction) / Effort\n\n"
            "For each Product Backlog item, we need to score:\n"
            "1. **User Value (1-10):** Based on customer research - how many users need this? "
            "How painful is the problem they're experiencing?\n"
            "2. **Time Criticality (1-10):** What's the cost of delay? Is there a deadline or "
            "market window?\n"
            "3. **Risk Reduction (1-10):** Does this validate a key assumption? How much does "
            "this reduce uncertainty?\n"
            "4. **Effort (1-10):** Get estimates from the Development Team - higher number = more effort\n\n"
            "**Important:** Before prioritizing, verify that each item connects to our Product Goal. "
            "If you can't clearly explain how an item moves us toward the Product Goal, it shouldn't "
            "be on the backlog right now.\n\n"
            "The highest score = highest priority. But remember: ordering is my superpower - "
            "don't accept 'everything is high priority'!"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "data_metrics_analyst", "ux_ui_designer"]
        )
    
    def _handle_ost_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Opportunity Solution Trees"""
        recommendations = [
            "Maintain a four-layer OST structure: Outcome → Opportunities → Solutions → Assumptions",
            "Base opportunities on real customer stories from interviews, not assumptions",
            "Test assumptions before building solutions",
            "Update the OST regularly with new discovery findings",
            "Use the OST to make strategy visible and enable evidence-based decisions"
        ]
        
        questions = [
            "What is our Product Goal or business outcome?",
            "What opportunities have we discovered from customer interviews?",
            "What solutions are we considering for each opportunity?",
            "What assumptions need to be tested before building?",
            "When did we last update the OST?"
        ]
        
        response_text = (
            "The Opportunity Solution Tree (OST) is a key framework for continuous discovery. "
            "It helps us visualize our product strategy and make evidence-based decisions.\n\n"
            "**OST Four-Layer Structure:**\n"
            "1. **Outcome** (top) - The business outcome or Product Goal\n"
            "2. **Opportunities** - Customer needs, pain points, desires (from interviews)\n"
            "3. **Solutions** - Possible ways to address opportunities\n"
            "4. **Assumptions/Tests** - Experiments to validate solutions\n\n"
            "**OST Principles:**\n"
            "- Outcome-oriented (focus on results, not features)\n"
            "- Based on real customer stories, not assumptions\n"
            "- Test assumptions before building\n"
            "- Continuous discovery and regular tree updates\n"
            "- Makes strategy visible and enables evidence-based decisions\n\n"
            "The OST should be updated regularly as we conduct customer interviews and run experiments. "
            "It's a living document that reflects our current understanding of customer needs and "
            "our strategy for addressing them."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_discovery_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about continuous discovery and customer interviews"""
        recommendations = [
            "Conduct at least one customer interview per week (story-based, not hypothetical)",
            "Use story-based interview technique: Ask for specific stories, not opinions",
            "Document opportunities and insights from interviews",
            "Update Opportunity Solution Tree with findings",
            "Synthesize learnings and share with team"
        ]
        
        interview_questions = [
            "Tell me about the last time you [relevant activity]",
            "What happened before that?",
            "What were you trying to accomplish?",
            "What made that difficult?",
            "How did you solve that?",
            "What would have made it easier?"
        ]
        
        questions = [
            "When was our last customer interview?",
            "What opportunities have we discovered recently?",
            "What assumptions need validation through interviews?",
            "How are we sharing discovery insights with the team?"
        ]
        
        response_text = (
            "Continuous discovery is mandatory for effective product development. As Product Owner, "
            "I must conduct at least one customer interview per week.\n\n"
            "**Story-Based Interview Technique:**\n"
            "❌ Don't ask: 'Would you use a feature that does X?' (hypothetical)\n"
            "✅ Do ask: 'Tell me about the last time you [relevant activity]' (story-based)\n\n"
            "**Follow-up Questions:**\n"
            "- What happened before that?\n"
            "- What were you trying to accomplish?\n"
            "- What made that difficult?\n"
            "- How did you solve that?\n"
            "- What would have made it easier?\n\n"
            "**Weekly Minimum:**\n"
            "- At least one customer interview per week\n"
            "- Document opportunities and insights\n"
            "- Update Opportunity Solution Tree with findings\n"
            "- Synthesize learnings and share with team\n\n"
            "**Anti-Pattern to Avoid:** Don't go 3+ weeks without customer contact. "
            "Continuous discovery is mandatory, not optional."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations + interview_questions,
            questions=questions
        )
    
    def _handle_backlog_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Product Backlog management"""
        recommendations = [
            "Ensure Product Backlog is transparent, visible, and understood",
            "Top 5-10 items should always be clear and well-defined",
            "Every item must connect to the Product Goal",
            "Apply Product Goal Connection Test: 'How does this item move us toward the Product Goal?'",
            "Order items using prioritization framework",
            "You may delegate writing items, but remain accountable for content and ordering"
        ]
        
        questions = [
            "What is our Product Goal?",
            "How does each backlog item connect to the Product Goal?",
            "Are the top 5-10 items clear and well-defined?",
            "When did we last review and order the backlog?",
            "Is the backlog transparent and visible to stakeholders?"
        ]
        
        response_text = (
            "Product Backlog management is a core responsibility. The Product Backlog must be:\n\n"
            "**Characteristics:**\n"
            "- Transparent: Visible to all stakeholders\n"
            "- Visible: Easy to access and understand\n"
            "- Understood: Clear what each item means and why it's there\n"
            "- Ordered: Items are prioritized based on value\n\n"
            "**Key Practices:**\n"
            "1. **Product Goal Connection:** Every item must connect to the Product Goal. "
            "If you can't explain how an item moves us toward the Product Goal, it shouldn't "
            "be on the backlog right now.\n"
            "2. **Top Items Clarity:** The top 5-10 items should always be clear and well-defined. "
            "Don't let features pile up without ordering.\n"
            "3. **Ordering:** Use the prioritization framework to order items. "
            "Don't accept 'everything is high priority' - ordering is my superpower.\n"
            "4. **Accountability:** You may delegate the responsibility of writing items, "
            "but you remain accountable for the Product Backlog content and ordering."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_product_goal_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Product Goal"""
        recommendations = [
            "Develop and explicitly communicate the Product Goal",
            "Ensure all Product Backlog items connect to the Product Goal",
            "Regularly inspect progress toward the Product Goal",
            "Use Product Goal Connection Test for every backlog item"
        ]
        
        questions = [
            "What is our Product Goal?",
            "How do current backlog items connect to the Product Goal?",
            "Are we making progress toward the Product Goal?",
            "Do stakeholders understand the Product Goal?"
        ]
        
        response_text = (
            "The Product Goal is the long-term objective for the product. It describes the future "
            "state of the product and serves as a target for the Scrum Team to plan against.\n\n"
            "**Product Goal Connection Test:**\n"
            "For every Product Backlog item, ask: 'How does this item move us toward the Product Goal?'\n"
            "- If you can't answer clearly → not in backlog right now\n"
            "- Everything must connect to the Product Goal\n\n"
            "**Responsibilities:**\n"
            "- Develop and explicitly communicate the Product Goal\n"
            "- Ensure all backlog items align with the Product Goal\n"
            "- Regularly inspect progress toward the Product Goal\n"
            "- Adapt the Product Goal based on learnings and market changes\n\n"
            "The Product Goal provides focus and direction. Without a clear Product Goal, "
            "prioritization becomes arbitrary and value maximization becomes impossible."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_feature_decision_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about whether to add/build a feature"""
        recommendations = [
            "Apply prioritization framework: (User Value + Time Criticality + Risk Reduction) / Effort",
            "Check for evidence from customer interviews - does this solve a real pain point?",
            "Verify the feature connects to the Product Goal",
            "Check Opportunity Solution Tree to see if this addresses a validated opportunity",
            "Get effort estimate from Development Team",
            "Consider small bets before big builds - test cheaply before building expensively"
        ]
        
        questions = [
            "Do we have evidence from customer interviews that this solves a real pain point?",
            "How many customers mentioned this in recent interviews?",
            "Does this address a validated opportunity in our OST?",
            "What's the effort estimate from the Development Team?",
            "How does this connect to our Product Goal?",
            "Can we test this assumption cheaply before building?"
        ]
        
        response_text = (
            "That's a great question, but let's apply our evidence-based decision-making framework. "
            "Before deciding to build, we need to validate the value and feasibility.\n\n"
            "**Decision Framework:**\n"
            "1. **Evidence Check:** Do we have evidence from customer interviews that this solves "
            "a real pain point? How many customers mentioned this? What stories did they share?\n"
            "2. **OST Alignment:** Does this address a validated opportunity in our Opportunity "
            "Solution Tree? If not, we may need more discovery.\n"
            "3. **Product Goal Connection:** How does this feature move us toward the Product Goal?\n"
            "4. **Effort Assessment:** What's the effort estimate from the Development Team?\n"
            "5. **Prioritization Score:** Calculate (User Value + Time Criticality + Risk Reduction) / Effort\n\n"
            "**Small Bets Before Big Builds:**\n"
            "Consider testing cheaply before building expensively:\n"
            "- Pretotype before prototype\n"
            "- Fake door tests\n"
            "- Landing pages\n"
            "- Concierge MVPs\n"
            "- Validate assumptions systematically\n\n"
            "It might be a 'nice to have' vs. a 'must have' for our Product Goal. Let's gather "
            "the evidence first, then prioritize accordingly."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "data_metrics_analyst", "ux_ui_designer"]
        )
    
    def _handle_estimation_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about effort estimation"""
        recommendations = [
            "Effort estimates should come from the Development Team",
            "Use effort (1-10 scale) in prioritization: higher = more effort",
            "Consider technical complexity, dependencies, and technical debt",
            "Break down large items into smaller, estimable tasks"
        ]
        
        questions = [
            "What is the scope of this work?",
            "Are there technical dependencies?",
            "What's the technical complexity?",
            "Does this require architecture changes?",
            "What similar work have we done before?"
        ]
        
        response_text = (
            "As Product Owner, I don't provide effort estimates - that's the Development Team's "
            "responsibility. However, I need effort estimates to properly prioritize.\n\n"
            "**For Prioritization:**\n"
            "Effort is scored 1-10 in our prioritization framework, where higher = more effort.\n"
            "Priority Score = (User Value + Time Criticality + Risk Reduction) / Effort\n\n"
            "**What I Need from Development Team:**\n"
            "- Effort estimates for backlog items\n"
            "- Technical feasibility assessments\n"
            "- Complexity and dependency information\n"
            "- Technical debt considerations\n\n"
            "**Best Practices:**\n"
            "- Break down large items into smaller, estimable tasks\n"
            "- Consider dependencies and technical complexity\n"
            "- Review similar past work for reference\n"
            "- Discuss in Backlog Refinement sessions\n\n"
            "Once I have effort estimates, I can properly prioritize items using our framework."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer"]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with Product Owner perspective"""
        response_text = (
            f"As Product Owner, my primary accountability is maximizing the value of the product. "
            f"Let me address your question: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Focus on value, priority, and customer needs\n"
            f"- Base decisions on evidence, not opinions\n"
            f"- Connect everything back to the Product Goal\n"
            f"- Emphasize continuous discovery and customer research\n\n"
            f"**Key Principles:**\n"
            f"- Evidence over opinions: Data beats HiPPO (Highest Paid Person's Opinion)\n"
            f"- Small bets before big builds: Test cheaply before building expensively\n"
            f"- Product Goal Connection: Every backlog item must move us toward the Product Goal\n\n"
            f"Product development is empirical - every product is an experiment. I stay "
            f"evidence-based, customer-focused, and outcome-oriented."
        )
        
        recommendations = [
            "Base decisions on evidence from customer interviews and data",
            "Connect all work to the Product Goal",
            "Use prioritization framework for ordering backlog",
            "Conduct continuous discovery (at least one interview per week)",
            "Test assumptions before building solutions"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        if any(word in query_lower for word in ["technical", "implementation", "feasibility", "architecture", "code"]):
            needs.append("development_engineer")
        
        if any(word in query_lower for word in ["data", "metrics", "analytics", "a/b test", "user behavior"]):
            needs.append("data_metrics_analyst")
        
        if any(word in query_lower for word in ["design", "ux", "ui", "usability", "user experience"]):
            needs.append("ux_ui_designer")
        
        if any(word in query_lower for word in ["test", "quality", "qa", "defect", "bug"]):
            needs.append("qa_engineer")
        
        if any(word in query_lower for word in ["requirement", "business", "stakeholder", "process"]):
            needs.append("business_analyst")
        
        if any(word in query_lower for word in ["velocity", "capacity", "impediment", "process", "scrum"]):
            needs.append("scrum_master")
        
        if any(word in query_lower for word in ["marketing", "gtm", "launch", "positioning", "competitive"]):
            needs.append("product_marketing_executive")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "development_engineer": "Technical constraints, feasibility assessments, implementation complexity, technical debt, architecture decisions",
                "qa_engineer": "Quality issues discovered during testing, acceptance criteria clarification needs, risk areas requiring additional specification",
                "ux_ui_designer": "User research findings, usability testing results, design feasibility, user experience implications",
                "business_analyst": "Business requirements, process flows, stakeholder needs, market analysis, competitive insights",
                "data_metrics_analyst": "User behavior patterns, metrics, A/B test results, statistical significance, outcome metric trends (North Star Metric, AARRR)",
                "scrum_master": "Team capacity, velocity trends, process impediments affecting delivery, team health, collaboration issues",
                "product_marketing_executive": "Go-to-market strategy, positioning, customer feedback, market reception, competitive landscape, messaging needs"
            },
            "provides_to": {
                "development_engineer": "Prioritized requirements, acceptance criteria, Product Goal context, user value insights",
                "scrum_master": "Product backlog updates, sprint goals, stakeholder needs, value priorities",
                "all_team_members": "Product Goal, backlog priorities, customer insights, discovery findings, OST updates"
            }
        }
    
    def calculate_priority_score(self, user_value: float, time_criticality: float, 
                                 risk_reduction: float, effort: float) -> float:
        """
        Calculate priority score using the PO prioritization formula.
        
        Args:
            user_value: 1-10 scale
            time_criticality: 1-10 scale
            risk_reduction: 1-10 scale
            effort: 1-10 scale (higher = more effort)
            
        Returns:
            Priority score (higher = higher priority)
        """
        if effort == 0:
            return 0.0
        return (user_value + time_criticality + risk_reduction) / effort
