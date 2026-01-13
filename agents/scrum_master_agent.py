"""
Scrum Master Agent
Implements the Scrum Master role with expertise in:
- Establishing and coaching Scrum framework adherence
- Servant leadership and facilitation
- Removing impediments and enabling team effectiveness
- Continuous improvement and team health
- Empirical process management
- Organizational change and Scrum adoption
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class ScrumMasterAgent(BaseAgent):
    """
    Scrum Master AI Agent
    
    Primary Accountability: The Scrum Team's effectiveness. 
    Establishing Scrum as defined in the Scrum Guide.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Scrum Master",
            name="SM",
            context=context
        )
        self.impediments = []
        self.team_health_indicators = {
            "sprint_goals_met": True,
            "definition_of_done_clear": True,
            "events_productive": True,
            "psychological_safety": True,
            "self_management": True
        }
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Scrum Master's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "The Scrum Team's effectiveness. Establishing Scrum as defined in the Scrum Guide.",
            "key_responsibilities": {
                "serving_scrum_team": [
                    "Coaching team members in self-management and cross-functionality",
                    "Helping Scrum Team focus on creating high-value Increments that meet Definition of Done",
                    "Causing the removal of impediments to the Scrum Team's progress",
                    "Ensuring all Scrum events take place and are positive, productive, and kept within timebox"
                ],
                "serving_product_owner": [
                    "Helping with effective Product Goal definition",
                    "Helping Scrum Team understand need for clear Product Backlog items",
                    "Helping establish empirical product planning for complex environments",
                    "Facilitating stakeholder collaboration as requested or needed"
                ],
                "serving_organization": [
                    "Leading, training, and coaching organization in Scrum adoption",
                    "Planning and advising Scrum implementations within organization",
                    "Helping employees and stakeholders understand and enact empirical approach",
                    "Removing barriers between stakeholders and Scrum Teams"
                ]
            },
            "servant_leadership": {
                "what_you_are_not": [
                    "Project Manager",
                    "Team secretary taking notes",
                    "Task assigner or work distributor",
                    "Status reporter to management",
                    "Decision maker for the team",
                    "Team 'manager' in traditional sense"
                ],
                "what_you_are": [
                    "Coach and facilitator",
                    "Impediment remover",
                    "Change agent",
                    "Teacher of Scrum principles",
                    "Guardian of empiricism",
                    "Advocate for team effectiveness"
                ]
            },
            "scrum_events": {
                "sprint": {
                    "description": "Fixed-length event (1 month or less) containing all other events",
                    "responsibilities": [
                        "Ensure no changes endanger Sprint Goal",
                        "Ensure quality does not decrease",
                        "Product Backlog refined as needed",
                        "Scope may be clarified/renegotiated with Product Owner"
                    ]
                },
                "sprint_planning": {
                    "timebox": "8 hours for 1-month Sprint",
                    "topics": [
                        "Topic 1: Why is this Sprint valuable? (Sprint Goal)",
                        "Topic 2: What can be Done this Sprint? (Sprint Backlog selection)",
                        "Topic 3: How will chosen work get done? (Decomposition and planning)"
                    ],
                    "output": "Sprint Goal, selected Product Backlog items, plan for delivering them"
                },
                "daily_scrum": {
                    "timebox": "15 minutes, every day",
                    "principle": "FOR Developers, BY Developers",
                    "purpose": "Developers inspect progress toward Sprint Goal and plan work for next 24 hours",
                    "note": "NOT a status update to Scrum Master or Product Owner"
                },
                "sprint_review": {
                    "timebox": "4 hours for 1-month Sprint",
                    "purpose": "Scrum Team presents results to stakeholders, review accomplishments, collaborate on what to do next",
                    "note": "NOT a demo - it's a working session"
                },
                "sprint_retrospective": {
                    "timebox": "3 hours for 1-month Sprint",
                    "purpose": "Inspect last Sprint regarding people, relationships, process, tools. Plan improvements.",
                    "note": "Most actionable improvement may become Sprint Backlog item"
                }
            },
            "coaching_patterns": {
                "self_management_over_direction": "Help team discover answers through Scrum principles, not give directives",
                "teaching_through_questions": "Use Socratic questioning instead of giving answers",
                "impediment_removal_process": [
                    "Identify: Notice or receive impediment reports",
                    "Assess urgency: Blocking Sprint Goal? Reducing effectiveness?",
                    "Determine ownership: Can team resolve? Needs organizational change?",
                    "Take action: Remove if organizational, coach team if within their control",
                    "Follow up: Verify impediment is truly removed"
                ]
            },
            "anti_patterns": [
                "Team Administrator - Taking notes, updating boards for team, doing their admin work",
                "Proxy PO - Making Product Backlog decisions on behalf of Product Owner",
                "Command & Control - Telling team how to do their work or assigning tasks",
                "Report Generator - Spending time creating status reports for management instead of coaching",
                "Blocker of Change - Rigid enforcement of process without understanding empiricism",
                "Always Present - Hovering over team instead of trusting their self-management",
                "Conflict Avoider - Ignoring team dysfunction or avoiding difficult conversations"
            ],
            "effectiveness_indicators": {
                "healthy_signs": [
                    "Team consistently meets Sprint Goals",
                    "Definition of Done is clear and followed",
                    "All Scrum events happen within timebox and are productive",
                    "Team members openly discuss challenges and ask for help",
                    "Product Owner and Developers collaborate effectively",
                    "Retrospective action items are implemented",
                    "Impediments are surfaced quickly and resolved",
                    "Team's velocity is predictable and sustainable"
                ],
                "warning_signs": [
                    "Sprint Goals frequently missed or changed",
                    "Scrum events are skipped, rushed, or ineffective",
                    "Tension between Product Owner and Developers",
                    "Team waits for instructions instead of self-organizing",
                    "Same impediments persist Sprint after Sprint",
                    "Low psychological safety (people afraid to speak up)",
                    "Overtime becoming the norm",
                    "Quality declining or Definition of Done ignored"
                ]
            }
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a Scrum Master perspective.
        Focuses on coaching, facilitation, impediment removal, and team effectiveness.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler (order matters - more specific first)
        if any(word in query_lower for word in ["governance", "kickoff", "working agreement", "team charter", "rice"]):
            return self._handle_governance_query(query, **kwargs)
        elif any(word in query_lower for word in ["impediment", "blocker", "blocking", "stuck", "can't"]):
            return self._handle_impediment_query(query, **kwargs)
        elif any(word in query_lower for word in ["sprint planning", "planning", "sprint goal"]):
            return self._handle_sprint_planning_query(query, **kwargs)
        elif any(word in query_lower for word in ["daily scrum", "standup", "daily standup"]):
            return self._handle_daily_scrum_query(query, **kwargs)
        elif any(word in query_lower for word in ["retrospective", "retro", "improvement"]):
            return self._handle_retrospective_query(query, **kwargs)
        elif any(word in query_lower for word in ["sprint review", "review", "demo"]):
            return self._handle_sprint_review_query(query, **kwargs)
        elif any(word in query_lower for word in ["definition of done", "done", "quality"]):
            return self._handle_definition_of_done_query(query, **kwargs)
        elif any(word in query_lower for word in ["team", "teamwork", "collaboration", "conflict"]):
            return self._handle_team_effectiveness_query(query, **kwargs)
        elif any(word in query_lower for word in ["velocity", "capacity", "estimate", "forecast"]):
            return self._handle_velocity_query(query, **kwargs)
        elif any(word in query_lower for word in ["coach", "coaching", "teach", "help"]):
            return self._handle_coaching_query(query, **kwargs)
        elif any(word in query_lower for word in ["organization", "stakeholder", "management", "executive"]):
            return self._handle_organizational_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_impediment_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about impediments"""
        recommendations = [
            "Follow the impediment removal process: Identify -> Assess urgency -> Determine ownership -> Take action -> Follow up",
            "Assess if the impediment is blocking the Sprint Goal or reducing team effectiveness",
            "Determine if the team can resolve it or if it requires organizational change",
            "If organizational, take action to remove it. If team-level, coach them to resolve it",
            "Follow up to verify the impediment is truly removed",
            "Document patterns - are the same impediments recurring?"
        ]
        
        questions = [
            "Is this blocking the Sprint Goal?",
            "Is this reducing team effectiveness?",
            "Can the team resolve this, or does it require organizational change?",
            "What's the root cause of this impediment?",
            "Have we seen this impediment before?",
            "What would need to change to remove this permanently?"
        ]
        
        response_text = (
            "Impediment removal is a core responsibility. Let me help you address this systematically.\n\n"
            "**Impediment Removal Process:**\n"
            "1. **Identify:** What exactly is the impediment? Be specific about what's blocking progress.\n"
            "2. **Assess Urgency:** Is this blocking the Sprint Goal? Is it reducing team effectiveness?\n"
            "3. **Determine Ownership:** Can the team resolve this themselves, or does it require organizational change?\n"
            "4. **Take Action:**\n"
            "   - If organizational: I'll work to remove it (coordinate with stakeholders, remove barriers)\n"
            "   - If team-level: I'll coach the team to resolve it themselves (self-management)\n"
            "5. **Follow Up:** Verify the impediment is truly removed, not just temporarily worked around.\n\n"
            "**Key Principles:**\n"
            "- Impediments that block Sprint Goals are highest priority\n"
            "- Organizational impediments are my responsibility to remove\n"
            "- Team-level impediments are opportunities to coach self-management\n"
            "- Document patterns - recurring impediments indicate systemic issues\n\n"
            "What specific impediment are you facing? Let's work through the process together."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_sprint_planning_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Sprint Planning"""
        recommendations = [
            "Facilitate the event - don't run it. The team owns the planning",
            "Ensure all three topics are covered: Why (Sprint Goal), What (Backlog items), How (plan)",
            "Timebox appropriately: 8 hours for 1-month Sprint, scale proportionally",
            "Ensure Developers select what they believe they can complete (self-management)",
            "Help Product Owner explain Product Backlog items clearly",
            "Ensure Sprint Goal is clear and valuable",
            "Output: Sprint Goal, selected Product Backlog items, plan for delivering them"
        ]
        
        questions = [
            "Is the Sprint Goal clear and valuable?",
            "Do Developers believe they can achieve the Sprint Goal?",
            "Are Product Backlog items clear enough for planning?",
            "Is the Definition of Done clear and achievable?",
            "What risks or dependencies need to be considered?",
            "How will the team know they've met the Sprint Goal?"
        ]
        
        response_text = (
            "Sprint Planning is a collaborative event that I facilitate. Here's how to ensure it's effective:\n\n"
            "**Sprint Planning Structure (Timeboxed to 8 hours for 1-month Sprint):**\n\n"
            "**Topic 1: Why is this Sprint valuable?**\n"
            "- Product Owner proposes a Sprint Goal\n"
            "- Scrum Team collaborates to define the Sprint Goal\n"
            "- Sprint Goal provides focus and flexibility\n\n"
            "**Topic 2: What can be Done this Sprint?**\n"
            "- Developers select Product Backlog items they believe they can complete\n"
            "- This is a forecast, not a commitment\n"
            "- Product Owner helps clarify items as needed\n\n"
            "**Topic 3: How will chosen work get done?**\n"
            "- Developers plan how to accomplish the Sprint Goal\n"
            "- They decompose work into tasks if needed\n"
            "- They create a plan for delivering the Increment\n\n"
            "**Output:**\n"
            "- Sprint Goal (why)\n"
            "- Selected Product Backlog items (what)\n"
            "- Plan for delivering them (how)\n\n"
            "**My Role:**\n"
            "- Facilitate the event, don't dictate\n"
            "- Ensure it stays within timebox\n"
            "- Help Product Owner explain items clearly\n"
            "- Coach team on self-management (they select, they plan)\n"
            "- Ensure Sprint Goal is clear and valuable"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_daily_scrum_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Daily Scrum"""
        recommendations = [
            "Daily Scrum is FOR Developers, BY Developers - you ensure it happens but don't run it",
            "Timebox: 15 minutes, every day, at the same time and place",
            "Focus: Inspect progress toward Sprint Goal, plan work for next 24 hours",
            "NOT a status update to Scrum Master or Product Owner",
            "If Developers need help, they can ask, but it's their event",
            "Protect the event from external interruptions"
        ]
        
        questions = [
            "Is the Daily Scrum happening every day?",
            "Are Developers using it to inspect progress toward Sprint Goal?",
            "Are they planning work for the next 24 hours?",
            "Is it being used as a status update (anti-pattern)?",
            "Are Developers self-organizing around the Sprint Goal?",
            "What impediments are being surfaced?"
        ]
        
        response_text = (
            "Daily Scrum is a critical event, but it's important to understand my role correctly.\n\n"
            "**Daily Scrum Principles:**\n"
            "- **FOR Developers, BY Developers** - This is their event\n"
            "- **Timebox:** 15 minutes, every day, same time and place\n"
            "- **Purpose:** Developers inspect progress toward Sprint Goal and plan work for next 24 hours\n"
            "- **NOT a status update** to me or the Product Owner\n\n"
            "**My Role:**\n"
            "- Ensure the event happens (schedule, protect time)\n"
            "- I don't run it or take notes for them\n"
            "- I may attend to listen, but I'm not the focus\n"
            "- Protect the event from external interruptions\n"
            "- If Developers need help, they can ask, but it's their event\n\n"
            "**Common Anti-Patterns to Avoid:**\n"
            "- Scrum Master running the Daily Scrum\n"
            "- Using it as a status update to management\n"
            "- Scrum Master taking notes or updating boards for the team\n"
            "- Making it longer than 15 minutes\n"
            "- Skipping it when 'there's nothing to report'\n\n"
            "**If Daily Scrum isn't working:**\n"
            "- Coach Developers on self-management\n"
            "- Help them understand the purpose (inspect progress, plan work)\n"
            "- Address impediments that surface\n"
            "- This might be a Retrospective topic"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_retrospective_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Sprint Retrospective"""
        recommendations = [
            "Facilitate as a peer team member, not as a manager",
            "Timebox: 3 hours for 1-month Sprint, scale proportionally",
            "Inspect: people, relationships, process, tools",
            "Identify what went well and what problems occurred",
            "Plan improvements to implement in next Sprint",
            "Most actionable improvement may become Sprint Backlog item",
            "Create psychological safety - everyone should feel safe to speak"
        ]
        
        questions = [
            "What went well in the last Sprint?",
            "What problems occurred?",
            "What improvements can we make?",
            "Are we addressing people, relationships, process, and tools?",
            "Is there psychological safety for honest feedback?",
            "Are retrospective action items being implemented?"
        ]
        
        response_text = (
            "Sprint Retrospective is where the team inspects itself and plans improvements. "
            "This is crucial for continuous improvement.\n\n"
            "**Sprint Retrospective Structure (Timeboxed to 3 hours for 1-month Sprint):**\n\n"
            "**Purpose:**\n"
            "- Inspect the last Sprint regarding people, relationships, process, and tools\n"
            "- Identify what went well and what problems occurred\n"
            "- Plan improvements to implement in next Sprint\n\n"
            "**My Role:**\n"
            "- Facilitate as a peer team member, not as a manager\n"
            "- Create psychological safety for honest feedback\n"
            "- Help team focus on improvements, not blame\n"
            "- Ensure action items are specific and actionable\n"
            "- Most actionable improvement may become Sprint Backlog item\n\n"
            "**Key Focus Areas:**\n"
            "- **People:** How are team members working together?\n"
            "- **Relationships:** Are there collaboration issues?\n"
            "- **Process:** Is Scrum working well? Are events effective?\n"
            "- **Tools:** Are tools helping or hindering?\n\n"
            "**Anti-Patterns to Avoid:**\n"
            "- Skipping Retrospective when 'everything is fine'\n"
            "- Focusing on blame instead of improvement\n"
            "- Not following up on action items\n"
            "- Making it a complaint session without solutions\n"
            "- Scrum Master dominating the conversation\n\n"
            "**Effectiveness Indicator:**\n"
            "Are retrospective action items being implemented? If not, why not?"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_sprint_review_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Sprint Review"""
        recommendations = [
            "Facilitate and ensure it happens",
            "Timebox: 4 hours for 1-month Sprint, scale proportionally",
            "Scrum Team presents results to stakeholders",
            "Review what was accomplished and what changed in environment",
            "Collaborate on what to do next (updates to Product Backlog)",
            "Working Increment is inspected",
            "NOT a demo - it's a working session"
        ]
        
        questions = [
            "What was accomplished in this Sprint?",
            "What changed in the environment?",
            "What feedback are stakeholders providing?",
            "What should we do next?",
            "Is the working Increment being inspected?",
            "Are Product Backlog updates happening based on feedback?"
        ]
        
        response_text = (
            "Sprint Review is where the Scrum Team and stakeholders inspect the Increment and adapt the Product Backlog.\n\n"
            "**Sprint Review Structure (Timeboxed to 4 hours for 1-month Sprint):**\n\n"
            "**Purpose:**\n"
            "- Scrum Team presents results to stakeholders\n"
            "- Review what was accomplished\n"
            "- Review what changed in the environment\n"
            "- Collaborate on what to do next (updates to Product Backlog)\n"
            "- Working Increment is inspected\n\n"
            "**Important:** This is NOT a demo - it's a working session where stakeholders provide feedback "
            "and the Product Backlog is adapted based on learnings.\n\n"
            "**My Role:**\n"
            "- Facilitate and ensure it happens\n"
            "- Help create an environment for honest feedback\n"
            "- Ensure it stays within timebox\n"
            "- Help Product Owner incorporate feedback into Product Backlog\n\n"
            "**Key Outcomes:**\n"
            "- Stakeholders understand what was accomplished\n"
            "- Stakeholders provide feedback\n"
            "- Product Backlog is updated based on feedback\n"
            "- Product Owner has input for next Sprint Planning\n\n"
            "**Anti-Patterns to Avoid:**\n"
            "- Making it a polished demo instead of a working session\n"
            "- Not allowing honest feedback\n"
            "- Skipping Product Backlog updates\n"
            "- Not inviting stakeholders\n"
            "- Going over timebox"
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
            "Definition of Done is a commitment to the Increment artifact",
            "It must be clear, understood, and achievable",
            "It's created by the entire Scrum Team (Developers, Product Owner, Scrum Master)",
            "It applies to all Product Backlog items",
            "If an item doesn't meet Definition of Done, it's not part of the Increment",
            "It should evolve as the team matures"
        ]
        
        questions = [
            "Is the Definition of Done clear and understood by everyone?",
            "Is it achievable within a Sprint?",
            "Is it being followed consistently?",
            "Does it ensure quality and releasability?",
            "When was it last reviewed or updated?",
            "Are there items that don't meet Definition of Done being called 'done'?"
        ]
        
        response_text = (
            "Definition of Done is a commitment to the Increment artifact. It's crucial for transparency and quality.\n\n"
            "**Definition of Done Principles:**\n"
            "- **Commitment to Increment:** It defines what 'Done' means for the Increment\n"
            "- **Team Agreement:** Created by the entire Scrum Team (Developers, Product Owner, Scrum Master)\n"
            "- **Applies to All Items:** Every Product Backlog item must meet Definition of Done\n"
            "- **Must Be Achievable:** It should be realistic within a Sprint\n"
            "- **Ensures Quality:** Items that meet Definition of Done are potentially releasable\n\n"
            "**My Role:**\n"
            "- Help team create a clear, achievable Definition of Done\n"
            "- Coach team to follow it consistently\n"
            "- Help identify when Definition of Done needs to evolve\n"
            "- Ensure it's not being ignored or bypassed\n\n"
            "**Common Issues:**\n"
            "- Definition of Done is too vague or unclear\n"
            "- It's not achievable within a Sprint\n"
            "- Team is calling items 'done' that don't meet it\n"
            "- It hasn't been reviewed or updated as team matures\n\n"
            "**If Definition of Done isn't working:**\n"
            "- This is a great Retrospective topic\n"
            "- Help team inspect what's happening\n"
            "- Coach them to create a Definition of Done they can actually achieve\n"
            "- Ensure it ensures quality without being unrealistic"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer", "qa_engineer"]
        )
    
    def _handle_team_effectiveness_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about team effectiveness and health"""
        recommendations = [
            "Assess team health using effectiveness indicators",
            "Look for healthy signs: Sprint Goals met, events productive, psychological safety",
            "Watch for warning signs: missed goals, skipped events, low safety",
            "Coach self-management - team should solve their own problems",
            "Address conflicts and dysfunction, don't avoid them",
            "Focus on effectiveness over efficiency"
        ]
        
        questions = [
            "Is the team consistently meeting Sprint Goals?",
            "Are Scrum events productive and within timebox?",
            "Is there psychological safety (people feel safe to speak up)?",
            "Is the team self-managing or waiting for instructions?",
            "Are impediments being surfaced quickly?",
            "Are retrospective action items being implemented?"
        ]
        
        response_text = (
            "Team effectiveness is my primary accountability. Let me help you assess and improve it.\n\n"
            "**Healthy Scrum Team Signs:**\n"
            "[OK] Team consistently meets Sprint Goals\n"
            "[OK] Definition of Done is clear and followed\n"
            "[OK] All Scrum events happen within timebox and are productive\n"
            "[OK] Team members openly discuss challenges and ask for help\n"
            "[OK] Product Owner and Developers collaborate effectively\n"
            "[OK] Retrospective action items are implemented\n"
            "[OK] Impediments are surfaced quickly and resolved\n"
            "[OK] Team's velocity is predictable and sustainable\n\n"
            "**Warning Signs:**\n"
            "[WARNING] Sprint Goals frequently missed or changed\n"
            "[WARNING] Scrum events are skipped, rushed, or ineffective\n"
            "[WARNING] Tension between Product Owner and Developers\n"
            "[WARNING] Team waits for instructions instead of self-organizing\n"
            "[WARNING] Same impediments persist Sprint after Sprint\n"
            "[WARNING] Low psychological safety (people afraid to speak up)\n"
            "[WARNING] Overtime becoming the norm\n"
            "[WARNING] Quality declining or Definition of Done ignored\n\n"
            "**My Approach:**\n"
            "- Coach self-management - help team solve their own problems\n"
            "- Address conflicts and dysfunction, don't avoid them\n"
            "- Focus on effectiveness over efficiency\n"
            "- Remove organizational impediments\n"
            "- Create psychological safety\n"
            "- Model Scrum values: Commitment, Courage, Focus, Openness, Respect\n\n"
            "What specific team effectiveness issue are you seeing? Let's address it through Scrum principles."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_velocity_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about velocity and capacity"""
        recommendations = [
            "Velocity is a forecast tool, not a target or commitment",
            "It helps with Sprint Planning - what can we likely complete?",
            "Focus on predictability and sustainability, not increasing velocity",
            "Velocity should be stable and sustainable",
            "Don't use velocity to compare teams or pressure for more",
            "If velocity is unpredictable, inspect why (impediments, unclear items, etc.)"
        ]
        
        questions = [
            "Is velocity being used as a target or commitment (anti-pattern)?",
            "Is velocity predictable and sustainable?",
            "What's causing velocity to be unpredictable?",
            "Are there impediments affecting velocity?",
            "Are Product Backlog items clear enough for accurate forecasting?",
            "Is the team working at a sustainable pace?"
        ]
        
        response_text = (
            "Velocity is a forecast tool to help with Sprint Planning, not a target or commitment.\n\n"
            "**Velocity Principles:**\n"
            "- **Forecast Tool:** Helps Developers forecast what they can likely complete\n"
            "- **Not a Target:** Don't use it to pressure teams to do more\n"
            "- **Not for Comparison:** Don't compare velocities across teams\n"
            "- **Focus on Predictability:** Stable, sustainable velocity is the goal\n"
            "- **Inspect When Unpredictable:** If velocity varies widely, inspect why\n\n"
            "**My Role:**\n"
            "- Help team understand velocity as a forecast tool\n"
            "- Coach against using it as a target or for comparison\n"
            "- Help inspect why velocity might be unpredictable\n"
            "- Focus on removing impediments that affect velocity\n"
            "- Ensure sustainable pace (no overtime, no burnout)\n\n"
            "**Common Anti-Patterns:**\n"
            "- Using velocity as a target ('we need to increase velocity')\n"
            "- Comparing velocities across teams\n"
            "- Pressuring team to commit to higher velocity\n"
            "- Ignoring impediments that affect velocity\n\n"
            "**If Velocity is Unpredictable:**\n"
            "- Inspect impediments\n"
            "- Check if Product Backlog items are clear enough\n"
            "- Look at Definition of Done - is it being followed?\n"
            "- Are there external dependencies?\n"
            "- This might be a Retrospective topic"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_coaching_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about coaching and teaching Scrum"""
        recommendations = [
            "Coach, don't dictate - help team discover answers through Scrum principles",
            "Use Socratic questioning instead of giving direct answers",
            "Teach 'why' not just 'what' - help understand Scrum principles",
            "Model Scrum values: Commitment, Courage, Focus, Openness, Respect",
            "Reference the Scrum Guide when appropriate",
            "Help team solve their own problems (self-management)"
        ]
        
        coaching_questions = [
            "What does the Scrum Guide say about this?",
            "How does this serve our Sprint Goal?",
            "What experiment could we try?",
            "What did we learn from last Sprint's retrospective?",
            "How does this align with Scrum values?",
            "What would self-management look like here?"
        ]
        
        response_text = (
            "Coaching is at the heart of my role. I help the team understand and apply Scrum principles.\n\n"
            "**Coaching Approach:**\n"
            "- **Coach, don't dictate:** Help team discover answers through Scrum principles\n"
            "- **Teaching through questions:** Use Socratic questioning instead of giving direct answers\n"
            "- **Teach 'why' not just 'what':** Help understand Scrum principles, not just follow rules\n"
            "- **Reference Scrum Guide:** Ground advice in official Scrum framework\n"
            "- **Promote self-management:** Help team solve their own problems\n\n"
            "**Coaching Patterns:**\n\n"
            "**Pattern: Self-Management Over Direction**\n"
            "When team asks: 'What should we work on?'\n"
            "Don't say: 'Work on items A, B, and C'\n"
            "Do say: 'What does the Sprint Backlog say? How does that align with the Sprint Goal? "
            "As Developers, you decide how to accomplish your Sprint Goal.'\n\n"
            "**Pattern: Teaching Through Questions**\n"
            "Instead of giving answers, use questions like:\n"
            "- 'What does the Scrum Guide say about this?'\n"
            "- 'How does this serve our Sprint Goal?'\n"
            "- 'What experiment could we try?'\n"
            "- 'What did we learn from last Sprint's retrospective?'\n\n"
            "**Key Principles:**\n"
            "- Model Scrum values: Commitment, Courage, Focus, Openness, Respect\n"
            "- Help team understand empiricism (transparency, inspection, adaptation)\n"
            "- Enable self-management and cross-functionality\n"
            "- Focus on effectiveness, not just following rules"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=coaching_questions
        )
    
    def _handle_organizational_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about organizational Scrum adoption and change"""
        recommendations = [
            "Lead, train, and coach organization in Scrum adoption",
            "Help employees and stakeholders understand empirical approach",
            "Remove barriers between stakeholders and Scrum Teams",
            "Plan and advise Scrum implementations within organization",
            "Help organization understand that 'faster' isn't always better - focus on value",
            "Address organizational impediments that affect team effectiveness"
        ]
        
        questions = [
            "What organizational barriers are affecting the Scrum Team?",
            "Do stakeholders understand the empirical approach?",
            "Are there organizational impediments I can help remove?",
            "What training or coaching does the organization need?",
            "How can we improve collaboration between stakeholders and Scrum Teams?",
            "What organizational changes would improve team effectiveness?"
        ]
        
        response_text = (
            "Serving the organization is one of my three service areas. I help with Scrum adoption "
            "and organizational change.\n\n"
            "**Serving the Organization Responsibilities:**\n"
            "- Leading, training, and coaching organization in Scrum adoption\n"
            "- Planning and advising Scrum implementations within organization\n"
            "- Helping employees and stakeholders understand and enact empirical approach\n"
            "- Removing barriers between stakeholders and Scrum Teams\n\n"
            "**Common Organizational Challenges:**\n"
            "- Pressure to 'go faster' without understanding value\n"
            "- Lack of understanding of empirical approach\n"
            "- Organizational impediments affecting teams\n"
            "- Stakeholders not engaged or available\n"
            "- Traditional management practices conflicting with Scrum\n\n"
            "**My Approach:**\n"
            "- Help organization understand empiricism (transparency, inspection, adaptation)\n"
            "- Focus on value, not just speed\n"
            "- Remove organizational barriers\n"
            "- Train and coach on Scrum principles\n"
            "- Help stakeholders understand their role\n\n"
            "**Key Message for Organization:**\n"
            "The question isn't 'how to go faster' - it's 'how to maximize value.' This might mean:\n"
            "- Better Product Backlog ordering (most valuable items first)\n"
            "- Clearer Product Goals (focus on outcomes)\n"
            "- Removing impediments (organizational barriers)\n"
            "- Smaller, more frequent releases (faster feedback)\n\n"
            "What specific organizational challenge are you facing? Let's address it through Scrum principles."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions
        )
    
    def _handle_governance_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about team governance, kickoff, and working agreements"""
        query_lower = query.lower()
        
        # Check if this is a governance kickoff request
        if any(word in query_lower for word in ["kickoff", "governance kickoff", "establish governance", "team kickoff"]):
            return self._handle_governance_kickoff(query, **kwargs)
        elif any(word in query_lower for word in ["team charter", "working agreement", "team values"]):
            return self._handle_team_charter_query(query, **kwargs)
        elif any(word in query_lower for word in ["rice", "prioritization", "prioritize"]):
            return self._handle_rice_prioritization_query(query, **kwargs)
        elif any(word in query_lower for word in ["definition of done", "dod"]):
            return self._handle_definition_of_done_query(query, **kwargs)
        else:
            return self._handle_general_governance_query(query, **kwargs)
    
    def _handle_governance_kickoff(self, query: str, **kwargs) -> AgentResponse:
        """Facilitate a governance kickoff meeting"""
        response_text = (
            "Welcome to our Team Governance Kickoff! I'm here to facilitate our agreement on "
            "how we'll work together as a self-contained product agency.\n\n"
            "**Purpose:** Establish governance for our Scrum team operating across multiple "
            "projects, requiring the ability to context-switch between repositories and problem domains.\n\n"
            "**Agenda (2-3 hours):**\n\n"
            "1. **Team Working Agreements** (15 min)\n"
            "   - Team Charter: Purpose, values, communication, decision-making\n"
            "   - Psychological safety commitments\n"
            "   - Conflict resolution approach\n\n"
            "2. **Definition of Done** (20 min)\n"
            "   - Universal DoD checklist (all projects)\n"
            "   - Project-specific additions\n"
            "   - Verification process\n\n"
            "3. **Prioritization Framework - RICE** (15 min)\n"
            "   - Formula: (Reach x Impact x Confidence) / Effort\n"
            "   - Scoring guidelines\n"
            "   - Process for using RICE\n\n"
            "4. **Testing & Quality Processes** (15 min)\n"
            "   - Test pyramid (70% unit, 20% integration, 10% E2E)\n"
            "   - Bug severity definitions\n"
            "   - Quality gates\n\n"
            "5. **Documentation Standards** (15 min)\n"
            "   - Required docs: README, PROJECT_BRIEF, ARCHITECTURE, ADRs, CHANGELOG\n"
            "   - Update triggers\n"
            "   - Storage locations\n\n"
            "6. **Ticketing & Workflow Process** (15 min)\n"
            "   - Workflow states: Backlog -> Ready -> In Progress -> In Review -> In Testing -> Done -> Released\n"
            "   - WIP limits\n"
            "   - Ticket templates\n\n"
            "7. **Review Cadences** (10 min)\n"
            "   - Code reviews (24-hour SLA)\n"
            "   - Design reviews\n"
            "   - Sprint Review\n"
            "   - Retrospective formats\n\n"
            "8. **Retrospective Practices** (10 min)\n"
            "   - Formats (Start-Stop-Continue, 4Ls, Sailboat)\n"
            "   - Action item framework\n"
            "   - Safe space creation\n\n"
            "9. **Continuous Learning** (10 min)\n"
            "   - Individual role learning (2 hours/Sprint)\n"
            "   - Team knowledge sharing (Learning Lunch)\n"
            "   - Cross-role shadowing\n\n"
            "10. **Context Switching Protocols** (15 min)\n"
            "    - Project onboarding checklist (30-45 min)\n"
            "    - Documentation requirements\n"
            "    - Best practices for multi-project work\n\n"
            "**My Role as Facilitator:**\n"
            "- Guide discussion through each area\n"
            "- Ensure all voices are heard\n"
            "- Summarize agreements after each section\n"
            "- Check for consensus before moving forward\n"
            "- Document all decisions\n\n"
            "**Let's Begin:**\n"
            "I'll start with Team Working Agreements. This establishes how we'll work together, "
            "communicate, make decisions, and resolve conflicts.\n\n"
            "**Team Charter Components:**\n"
            "- Our Purpose: Why we exist as a team\n"
            "- Core Values: What we stand for\n"
            "- Communication: How we'll communicate\n"
            "- Decision Making: Who decides what\n"
            "- Conflict Resolution: How we handle disagreements\n"
            "- Psychological Safety: Creating safe space for all\n\n"
            "What would you like to discuss first? Or shall I guide you through the Team Charter template?"
        )
        
        recommendations = [
            "Work through each governance area systematically",
            "Summarize agreements after each section",
            "Check for consensus before moving forward",
            "Document all decisions",
            "Create actionable agreements, not vague statements",
            "Ensure all team members participate",
            "Focus on what will help the team be effective"
        ]
        
        questions = [
            "What's our team purpose?",
            "What core values do we share?",
            "How will we communicate?",
            "How will we make decisions?",
            "How will we resolve conflicts?",
            "What does psychological safety mean to us?",
            "What working agreements will help us be effective?"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer", "qa_engineer", "business_analyst", "data_metrics_analyst", "ux_ui_designer"]
        )
    
    def _handle_team_charter_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Team Charter and working agreements"""
        response_text = (
            "The Team Charter establishes our working agreements and shared values. "
            "Here's what it should include:\n\n"
            "**Team Charter Components:**\n\n"
            "**Our Purpose:**\n"
            "We are a self-contained product agency that delivers high-quality products "
            "across multiple domains through empirical Scrum practices, continuous "
            "discovery, and cross-functional collaboration.\n\n"
            "**Core Values:**\n"
            "1. Evidence Over Assumptions - Base decisions on data and user research\n"
            "2. Quality Without Compromise - Definition of Done is sacred\n"
            "3. Transparent Collaboration - Make work visible, share openly\n"
            "4. Continuous Learning - Improve ourselves and our practices\n"
            "5. User-Centered - Always advocate for end users\n\n"
            "**Communication:**\n"
            "- Response Time: 4 hours during work hours\n"
            "- Async First: Default to async (tickets, docs, Slack)\n"
            "- Sync When Needed: Meetings for complex discussions\n"
            "- Documentation: All decisions documented\n"
            "- Transparency: Share work-in-progress early\n\n"
            "**Decision Making:**\n"
            "- Product Decisions: Product Owner (after input)\n"
            "- Technical Decisions: Developers decide collaboratively\n"
            "- Process Decisions: Team consensus (SM facilitates)\n"
            "- Escalation: PO breaks ties if no consensus\n\n"
            "**Conflict Resolution:**\n"
            "1. Address directly with person (assume good intent)\n"
            "2. If unresolved, involve Scrum Master\n"
            "3. Focus on behaviors/outcomes, not personalities\n"
            "4. Commit to agreed resolution\n\n"
            "**Psychological Safety:**\n"
            "- Safe to fail: Experiments may fail\n"
            "- Safe to speak: All voices heard\n"
            "- Safe to challenge: Ideas can be challenged\n"
            "- Safe to ask: No question is stupid\n"
            "- Safe to say no: Honesty encouraged\n\n"
            "Would you like to customize any of these for your team?"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=[
                "Customize the Team Charter to fit your team's specific needs",
                "Ensure all team members agree to the charter",
                "Make it visible (print and post, or in wiki)",
                "Review and update quarterly",
                "Use it as a reference for decision-making"
            ]
        )
    
    def _handle_rice_prioritization_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about RICE prioritization framework"""
        response_text = (
            "RICE is a prioritization framework that helps us make evidence-based decisions. "
            "Here's how it works:\n\n"
            "**RICE Formula:** (Reach x Impact x Confidence) / Effort\n\n"
            "**1. REACH (1-10):** How many users impacted per quarter?\n"
            "- 10 = All users (>90%)\n"
            "- 7 = Most users (50-90%)\n"
            "- 5 = Many users (25-50%)\n"
            "- 3 = Some users (10-25%)\n"
            "- 1 = Few users (<10%)\n"
            "**Who Scores:** Product Owner + Data Analyst\n\n"
            "**2. IMPACT (1-10):** How much impact per user?\n"
            "- 10 = Massive (3x improvement, critical pain)\n"
            "- 7 = High (2x improvement, major pain)\n"
            "- 5 = Medium (1.5x improvement, nice)\n"
            "- 3 = Low (minor improvement)\n"
            "- 1 = Minimal (cosmetic)\n"
            "**Who Scores:** Product Owner + UX Designer + Data Analyst\n\n"
            "**3. CONFIDENCE (50/80/100%):** How confident are we?\n"
            "- 100% = High (validated with research)\n"
            "- 80% = Medium (some evidence)\n"
            "- 50% = Low (hypothesis/assumption)\n"
            "**Who Scores:** Product Owner (based on evidence)\n\n"
            "**4. EFFORT (person-weeks):** Total team effort\n"
            "**Includes:** Design, Development, Testing, Documentation, Analytics, Marketing\n"
            "**Who Scores:** All Developers (sum estimates)\n\n"
            "**Example:**\n"
            "Feature: Auto-save functionality\n"
            "- Reach: 10 (all users)\n"
            "- Impact: 10 (prevents data loss)\n"
            "- Confidence: 100% (validated)\n"
            "- Effort: 1.5 weeks\n"
            "**RICE Score = (10 x 10 x 1.0) / 1.5 = 66.7**\n\n"
            "**Prioritization Process:**\n"
            "1. Score new items when added to backlog\n"
            "2. Order backlog by RICE score (highest first)\n"
            "3. Re-prioritize weekly based on new data\n"
            "4. PO adjusts for strategy, dependencies, deadlines\n"
            "5. Document rationale for deviations from RICE\n\n"
            "**Special Cases:**\n"
            "- Technical Debt: Reframe as enabler for user value\n"
            "- Bugs: Use Reach (users affected), Impact (severity), Confidence (100%), Effort (time to fix)\n"
            "- Critical bugs: Immediate fix regardless of RICE\n"
            "- Experiments: Value of learning, likelihood of learning\n\n"
            "Would you like help scoring a specific item?"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=[
                "Use RICE for all Product Backlog items",
                "Re-score items weekly based on new data",
                "Document rationale for deviations from RICE",
                "Calibrate quarterly: Did Reach/Impact/Effort match actual?",
                "Work with Product Owner and Data Analyst on scoring"
            ],
            requires_collaboration=True,
            collaborating_roles=["product_owner", "data_metrics_analyst"]
        )
    
    def _handle_general_governance_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general governance queries"""
        response_text = (
            f"Team governance establishes how we work together effectively. Let me address: '{query}'\n\n"
            f"**Governance Areas:**\n"
            f"- Team Working Agreements (Team Charter)\n"
            f"- Definition of Done (Universal + project-specific)\n"
            f"- Prioritization Framework (RICE)\n"
            f"- Testing & Quality Processes\n"
            f"- Documentation Standards\n"
            f"- Ticketing & Workflow Process\n"
            f"- Review Cadences\n"
            f"- Retrospective Practices\n"
            f"- Continuous Learning & Role Improvement\n"
            f"- Context Switching Protocols\n\n"
            f"**My Role:**\n"
            f"- Facilitate governance kickoff meetings\n"
            f"- Help team establish working agreements\n"
            f"- Ensure processes are followed\n"
            f"- Continuously improve governance based on team feedback\n\n"
            f"Would you like to:\n"
            f"- Start a governance kickoff?\n"
            f"- Review a specific governance area?\n"
            f"- Update existing governance agreements?"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=[
                "Start with a governance kickoff to establish all agreements",
                "Review governance quarterly and adjust as needed",
                "Make governance visible and accessible to all team members",
                "Use governance as a guide, not rigid rules"
            ]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with Scrum Master perspective"""
        response_text = (
            f"As Scrum Master, my primary accountability is the Scrum Team's effectiveness. "
            f"Let me address your question: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Coach and facilitate, don't dictate\n"
            f"- Focus on team effectiveness and Scrum framework adherence\n"
            f"- Remove impediments and enable self-management\n"
            f"- Ground advice in Scrum principles and empiricism\n\n"
            f"**Key Principles:**\n"
            f"- **Servant Leadership:** I serve the team, Product Owner, and organization\n"
            f"- **Empiricism:** Transparency, inspection, and adaptation\n"
            f"- **Self-Management:** Help team solve their own problems\n"
            f"- **Continuous Improvement:** Focus on effectiveness, not just following rules\n\n"
            f"Scrum is simple but difficult. My job is to help everyone navigate the difficulty "
            f"and enable the team to be effective."
        )
        
        recommendations = [
            "Coach through questions, not directives",
            "Focus on team effectiveness and Scrum framework adherence",
            "Remove impediments that block Sprint Goals",
            "Enable self-management and cross-functionality",
            "Ensure Scrum events are productive and within timebox",
            "Model Scrum values: Commitment, Courage, Focus, Openness, Respect"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        if any(word in query_lower for word in ["product", "backlog", "goal", "priority", "stakeholder"]):
            needs.append("product_owner")
        
        if any(word in query_lower for word in ["technical", "implementation", "development", "code", "sprint backlog"]):
            needs.append("development_engineer")
        
        if any(word in query_lower for word in ["quality", "test", "qa", "definition of done"]):
            needs.append("qa_engineer")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "product_owner": "Product Goal and Product Backlog health, stakeholder engagement challenges, need for facilitation or organizational barriers",
                "development_engineer": "Technical impediments and dependencies, process friction points, collaboration challenges, Definition of Done adherence, Sprint Goal confidence",
                "qa_engineer": "Quality standards and Definition of Done, testing impediments, integration challenges",
                "ux_ui_designer": "Design-development collaboration issues, user research integration needs, workflow impediments",
                "business_analyst": "Requirements clarity issues, stakeholder access problems, process bottlenecks",
                "data_metrics_analyst": "Data infrastructure impediments, metrics tracking challenges, analysis integration needs",
                "product_marketing_executive": "Go-to-market alignment issues, external communication barriers, launch coordination needs"
            },
            "provides_to": {
                "product_owner": "Facilitation support, organizational barrier removal, coaching on Scrum practices, stakeholder collaboration help",
                "development_engineer": "Impediment removal, coaching on self-management, facilitation of Scrum events, process improvement",
                "all_team_members": "Scrum framework coaching, impediment removal, facilitation, team effectiveness support"
            }
        }
