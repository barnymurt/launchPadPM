"""
Business Analyst Agent
Implements the Business Analyst role (part of Developers) with expertise in:
- Requirements analysis and elicitation
- Business process modeling and documentation
- Stakeholder communication and management
- Acceptance criteria definition
- User story refinement and decomposition
- Domain knowledge and business rules
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class BusinessAnalystAgent(BaseAgent):
    """
    Business Analyst AI Agent
    
    Note: In Scrum, there is no separate "Business Analyst" role - you are a Developer 
    who specializes in business analysis. All Developers are accountable for creating value.
    
    Primary Accountability: Creating any aspect of a usable Increment each Sprint 
    (with business analysis expertise).
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Business Analyst",
            name="BA",
            context=context
        )
        self.business_rules = {}
        self.stakeholders = []
        self.requirements_documentation = {}
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Business Analyst's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Creating any aspect of a usable Increment each Sprint (with business analysis expertise)",
            "note": "In Scrum, there is no separate 'Business Analyst' role - you are a Developer who specializes in business analysis. All Developers are accountable for creating value.",
            "key_responsibilities": {
                "requirements_analysis": [
                    "Eliciting and documenting business requirements",
                    "Translating business needs into clear Product Backlog items",
                    "Defining acceptance criteria in collaboration with Product Owner",
                    "Identifying edge cases and business rules",
                    "Validating requirements with stakeholders"
                ],
                "developer_responsibilities": [
                    "Participating in Sprint Planning",
                    "Contributing to Sprint Backlog",
                    "Adapting work daily toward Sprint Goal",
                    "Creating usable Increment",
                    "Owning Sprint Backlog alongside fellow Developers"
                ],
                "business_context": [
                    "Understanding business domain and processes",
                    "Documenting business rules and workflows",
                    "Facilitating communication between business and technical teams",
                    "Supporting Product Owner with Product Backlog refinement"
                ]
            },
            "user_story_format": {
                "structure": "As a [specific user type] I want to [do something specific] So that [I get this specific value/benefit]",
                "invest_criteria": [
                    "Independent: Can be developed in any order",
                    "Negotiable: Details can be discussed and refined",
                    "Valuable: Delivers value to user or business",
                    "Estimable: Team can estimate size/effort",
                    "Small: Fits within a Sprint",
                    "Testable: Clear acceptance criteria exist"
                ]
            },
            "acceptance_criteria": {
                "given_when_then": "Given [initial context/precondition] When [action/event occurs] Then [expected outcome]",
                "checklist_style": "Alternative format using checkboxes for criteria"
            },
            "business_rules": {
                "format": "Rule ID, Name, Description, Formula, Conditions, Examples, Exceptions",
                "purpose": "Document business logic and constraints clearly"
            },
            "anti_patterns": [
                "Requirements Waterfall - Don't try to document everything up front; refine iteratively",
                "The Middleman - Don't prevent direct communication between developers and stakeholders",
                "Assumption Documentation - Don't write requirements without validating with stakeholders",
                "Technical Design - Focus on WHAT and WHY, not HOW (that's for developers)",
                "Perfect Requirements - Requirements will evolve; embrace change over perfection",
                "Solo Analysis - Collaborate with team on requirements, don't work in isolation",
                "Scope Creep Enabler - Help Product Owner say 'no' or 'later,' not 'yes' to everything"
            ],
            "stakeholder_management": {
                "stakeholder_matrix": {
                    "high_power_high_interest": "Manage Closely (Key Stakeholders)",
                    "high_power_low_interest": "Keep Satisfied",
                    "low_power_high_interest": "Keep Informed",
                    "low_power_low_interest": "Monitor"
                },
                "elicitation_techniques": [
                    "Interviews (one-on-one or small group, story-based)",
                    "Workshops (collaborative requirements sessions)",
                    "Observation (watch users perform tasks)",
                    "Document Analysis (review existing processes)",
                    "Prototyping (show mockups to gather feedback)"
                ]
            }
        }
    
    def _hardcoded_process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a Business Analyst perspective.
        Focuses on requirements, business context, and acceptance criteria.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler
        if any(word in query_lower for word in ["requirement", "requirements", "need", "feature", "user story"]):
            return self._handle_requirements_query(query, **kwargs)
        elif any(word in query_lower for word in ["acceptance criteria", "criteria", "acceptance"]):
            return self._handle_acceptance_criteria_query(query, **kwargs)
        elif any(word in query_lower for word in ["business rule", "rule", "business logic", "edge case"]):
            return self._handle_business_rule_query(query, **kwargs)
        elif any(word in query_lower for word in ["stakeholder", "user", "customer", "who"]):
            return self._handle_stakeholder_query(query, **kwargs)
        elif any(word in query_lower for word in ["process", "workflow", "flow", "modeling"]):
            return self._handle_process_query(query, **kwargs)
        elif any(word in query_lower for word in ["refinement", "refine", "decompose", "break down"]):
            return self._handle_refinement_query(query, **kwargs)
        elif any(word in query_lower for word in ["clarify", "clarification", "unclear", "ambiguous"]):
            return self._handle_clarification_query(query, **kwargs)
        elif any(word in query_lower for word in ["data model", "entity", "relationship", "data"]):
            return self._handle_data_model_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_requirements_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about requirements analysis"""
        recommendations = [
            "Clarify the business need: What problem are we solving? For whom?",
            "Reference business context: Connect to business processes and domain knowledge",
            "Define acceptance criteria: How will we know when this is complete?",
            "Identify stakeholders: Who needs to be consulted or informed?",
            "Consider edge cases: What happens in unusual scenarios?",
            "Document decisions: Capture key business rules and rationale",
            "Use INVEST criteria: Independent, Negotiable, Valuable, Estimable, Small, Testable"
        ]
        
        questions = [
            "What problem are we solving? For whom?",
            "What's the business value?",
            "Who are the stakeholders?",
            "What are the acceptance criteria?",
            "What are the edge cases?",
            "What business rules apply?",
            "Are there dependencies or constraints?"
        ]
        
        response_text = (
            "Let me help analyze the requirements so we can build this right.\n\n"
            "**Requirements Analysis Approach:**\n"
            "1. **Understand Business Context:** Why is this needed? What's the business value?\n"
            "2. **Clarify Business Need:** What problem are we solving? For whom?\n"
            "3. **Identify Stakeholders:** Who needs to be consulted or informed?\n"
            "4. **Define Acceptance Criteria:** How will we verify this is correct?\n"
            "5. **Consider Edge Cases:** What happens in unusual scenarios?\n"
            "6. **Document Business Rules:** Capture key logic and constraints\n\n"
            "**User Story Format:**\n"
            "As a [specific user type]\n"
            "I want to [do something specific]\n"
            "So that [I get this specific value/benefit]\n\n"
            "**INVEST Criteria for Good User Stories:**\n"
            "- **Independent:** Can be developed in any order\n"
            "- **Negotiable:** Details can be discussed and refined\n"
            "- **Valuable:** Delivers value to user or business\n"
            "- **Estimable:** Team can estimate size/effort\n"
            "- **Small:** Fits within a Sprint\n"
            "- **Testable:** Clear acceptance criteria exist\n\n"
            "**Key Principles:**\n"
            "- Clarity over completeness - Clear, testable requirements beat comprehensive documentation\n"
            "- Collaborate, don't dictate - Requirements emerge through team collaboration\n"
            "- Iterative refinement - Requirements evolve; refine continuously\n"
            "- Business value focus - Always connect requirements to business outcomes\n\n"
            "Let me help you think through the requirements systematically..."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_acceptance_criteria_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about acceptance criteria"""
        recommendations = [
            "Define acceptance criteria in collaboration with Product Owner",
            "Use Given-When-Then format for behavior-driven criteria",
            "Use checklist style as alternative format",
            "Ensure criteria are clear, testable, and measurable",
            "Cover happy path and edge cases",
            "Validate criteria with stakeholders",
            "Make criteria visible and understood by team"
        ]
        
        questions = [
            "What are the acceptance criteria?",
            "Are criteria clear and testable?",
            "Do criteria cover happy path and edge cases?",
            "Have criteria been validated with stakeholders?",
            "Are criteria specific and measurable?",
            "How will we verify each criterion?"
        ]
        
        response_text = (
            "Acceptance criteria define 'done' and are crucial for quality. Here's my approach:\n\n"
            "**Acceptance Criteria Formats:**\n\n"
            "**Given-When-Then (Behavior-Driven):**\n"
            "Given [initial context/precondition]\n"
            "When [action/event occurs]\n"
            "Then [expected outcome]\n\n"
            "**Example:**\n"
            "Given I have tracked 10 hours on Project A at $100/hour\n"
            "When I generate an invoice for Project A\n"
            "Then the invoice shows:\n"
            "  - 10 hours itemized by date\n"
            "  - Total of $1,000\n"
            "  - My business information\n"
            "  - Client information\n"
            "  - Invoice number and date\n\n"
            "**Checklist Style (Alternative):**\n"
            "□ User can select project and date range\n"
            "□ System calculates hours automatically\n"
            "□ Invoice includes all tax/business info required\n"
            "□ Invoice can be exported as PDF\n"
            "□ User can preview before finalizing\n\n"
            "**Key Principles:**\n"
            "- Clear and testable\n"
            "- Specific and measurable\n"
            "- Cover happy path and edge cases\n"
            "- Validated with stakeholders\n"
            "- Visible and understood by team\n\n"
            "**My Role:**\n"
            "- Define acceptance criteria in collaboration with Product Owner\n"
            "- Ensure criteria are clear and testable\n"
            "- Help team understand criteria during Sprint Planning\n"
            "- Validate implemented features against criteria\n\n"
            "Acceptance criteria are the bridge between business needs and technical implementation."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "qa_engineer"]
        )
    
    def _handle_business_rule_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about business rules and edge cases"""
        recommendations = [
            "Document business rules clearly with ID, name, description, formula",
            "Include conditions, examples, and exceptions",
            "Identify edge cases and document how to handle them",
            "Validate business rules with stakeholders",
            "Make rules visible and accessible to team",
            "Update rules as business evolves"
        ]
        
        questions = [
            "What are the business rules for this?",
            "What are the edge cases?",
            "What conditions apply?",
            "Are there exceptions to the rule?",
            "Have rules been validated with stakeholders?",
            "How should edge cases be handled?"
        ]
        
        response_text = (
            "Business rules define the logic and constraints that govern how the system behaves. "
            "Let me help document them clearly.\n\n"
            "**Business Rule Documentation Format:**\n"
            "Rule ID: BR-001\n"
            "Name: [Descriptive name]\n"
            "Description: [What the rule does]\n"
            "Formula: [If applicable]\n"
            "Conditions: [When this applies]\n"
            "Examples: [Concrete examples]\n"
            "Exceptions: [When rule doesn't apply]\n\n"
            "**Example:**\n"
            "Rule ID: BR-001\n"
            "Name: Invoice Total Calculation\n"
            "Description: Invoice total must include base amount + applicable taxes\n"
            "Formula: Total = (Hours × Rate) + (Hours × Rate × Tax Rate)\n"
            "Conditions:\n"
            "  - Tax rate varies by client location\n"
            "  - Must handle multiple tax rates\n"
            "  - Must round to 2 decimal places\n"
            "Examples:\n"
            "  - 10 hours × $100/hr × 1.08 (8% tax) = $1,080.00\n"
            "Exceptions:\n"
            "  - Tax-exempt clients: Total = Hours × Rate only\n\n"
            "**Edge Cases:**\n"
            "Always identify and document edge cases:\n"
            "- What if input is zero or negative?\n"
            "- What if multiple conditions apply?\n"
            "- What if data is missing?\n"
            "- What if limits are exceeded?\n"
            "- What if exceptions apply?\n\n"
            "**My Approach:**\n"
            "- Document rules clearly with examples\n"
            "- Identify edge cases systematically\n"
            "- Validate rules with stakeholders\n"
            "- Make rules visible to team\n"
            "- Update rules as business evolves"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_stakeholder_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about stakeholders"""
        recommendations = [
            "Identify all stakeholders: funders, users, maintainers, impacted parties",
            "Use stakeholder matrix: Power vs. Interest",
            "Manage closely: High Power, High Interest",
            "Keep satisfied: High Power, Low Interest",
            "Keep informed: Low Power, High Interest",
            "Monitor: Low Power, Low Interest",
            "Use elicitation techniques: interviews, workshops, observation"
        ]
        
        questions = [
            "Who funds the product?",
            "Who uses the product?",
            "Who maintains the product?",
            "Who is impacted by the product?",
            "Who has decision authority?",
            "What are their interests and power levels?"
        ]
        
        response_text = (
            "Stakeholder management is crucial for understanding requirements. Here's my approach:\n\n"
            "**Stakeholder Identification:**\n"
            "- Who funds the product?\n"
            "- Who uses the product?\n"
            "- Who maintains the product?\n"
            "- Who is impacted by the product?\n"
            "- Who has decision authority?\n\n"
            "**Stakeholder Matrix (Power vs. Interest):**\n"
            "- **High Power, High Interest** -> Manage Closely (Key Stakeholders)\n"
            "- **High Power, Low Interest** -> Keep Satisfied\n"
            "- **Low Power, High Interest** -> Keep Informed\n"
            "- **Low Power, Low Interest** -> Monitor\n\n"
            "**Elicitation Techniques:**\n"
            "- **Interviews:** One-on-one or small group, story-based questions\n"
            "- **Workshops:** Collaborative requirements sessions, user story mapping\n"
            "- **Observation:** Watch users perform tasks, shadow users\n"
            "- **Document Analysis:** Review existing processes and systems\n"
            "- **Prototyping:** Show mockups to gather feedback\n\n"
            "**Key Principles:**\n"
            "- Don't be a middleman - facilitate direct communication when appropriate\n"
            "- Validate requirements with actual stakeholders\n"
            "- Focus on story-based questions, not hypotheticals\n"
            "- Document stakeholder insights and decisions\n\n"
            "Understanding stakeholders helps ensure we build the right thing for the right people."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner"]
        )
    
    def _handle_process_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about business process modeling"""
        recommendations = [
            "Document process flows: name, actors, trigger, preconditions, flow, postconditions",
            "Include business rules and edge cases in process documentation",
            "Model current state and desired state",
            "Identify pain points and improvement opportunities",
            "Make processes visible and understandable",
            "Update processes as business evolves"
        ]
        
        questions = [
            "What's the process name?",
            "Who are the actors?",
            "What triggers the process?",
            "What are the preconditions?",
            "What's the flow?",
            "What are the postconditions?",
            "What business rules apply?",
            "What are the edge cases?"
        ]
        
        response_text = (
            "Business process modeling helps us understand how work flows and where value is created.\n\n"
            "**Process Flow Documentation Format:**\n"
            "Process Name: [Name]\n"
            "Actors: [Who participates]\n"
            "Trigger: [What starts the process]\n"
            "Preconditions: [What must be true before starting]\n\n"
            "Flow:\n"
            "1. [Step 1]\n"
            "2. [Step 2]\n"
            "3. [Step 3]\n"
            "...\n\n"
            "Postconditions: [What's true after completion]\n"
            "Business Rules: [Rule IDs that apply]\n"
            "Edge Cases: [Unusual scenarios]\n\n"
            "**Example:**\n"
            "Process Name: Customer Invoice Generation\n"
            "Actors: Freelancer, Client, System\n"
            "Trigger: Freelancer completes project work\n"
            "Preconditions: Time tracked in system\n\n"
            "Flow:\n"
            "1. Freelancer selects project and date range\n"
            "2. System calculates total hours and amount\n"
            "3. System populates invoice template\n"
            "4. Freelancer reviews invoice\n"
            "5. Freelancer finalizes invoice\n"
            "6. System generates PDF\n"
            "7. Freelancer sends invoice to client\n\n"
            "Postconditions: Invoice sent, payment tracked\n"
            "Business Rules: BR-001, BR-002\n"
            "Edge Cases: Multiple tax rates, partial hours, currency conversion\n\n"
            "**My Approach:**\n"
            "- Document current state and desired state\n"
            "- Identify pain points and improvement opportunities\n"
            "- Include business rules and edge cases\n"
            "- Make processes visible and understandable\n"
            "- Update processes as business evolves"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "ux_ui_designer"]
        )
    
    def _handle_refinement_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about Product Backlog refinement"""
        recommendations = [
            "Refinement is usually ≤10% of Sprint capacity",
            "Analyze upcoming Product Backlog items with Product Owner",
            "Break down large items into smaller, clearer pieces",
            "Define acceptance criteria",
            "Identify dependencies and constraints",
            "Clarify business rules and edge cases",
            "Ensure items meet INVEST criteria"
        ]
        
        questions = [
            "Is this item too large? Can we break it down?",
            "Are acceptance criteria clear?",
            "What are the dependencies?",
            "What business rules apply?",
            "What are the edge cases?",
            "Does this meet INVEST criteria?",
            "Is this estimable and testable?"
        ]
        
        response_text = (
            "Product Backlog Refinement is where I make my primary contribution (usually ≤10% of Sprint capacity).\n\n"
            "**Refinement Activities:**\n"
            "- Analyze upcoming Product Backlog items with Product Owner\n"
            "- Break down large items into smaller, clearer pieces\n"
            "- Define acceptance criteria\n"
            "- Identify dependencies and constraints\n"
            "- Clarify business rules and edge cases\n"
            "- Ensure items meet INVEST criteria\n\n"
            "**INVEST Criteria Check:**\n"
            "- **Independent:** Can be developed in any order?\n"
            "- **Negotiable:** Can details be discussed and refined?\n"
            "- **Valuable:** Delivers value to user or business?\n"
            "- **Estimable:** Can team estimate size/effort?\n"
            "- **Small:** Fits within a Sprint?\n"
            "- **Testable:** Clear acceptance criteria exist?\n\n"
            "**Breaking Down Large Items:**\n"
            "- Split by user type (different users, different stories)\n"
            "- Split by workflow step (each step can be a story)\n"
            "- Split by business rule (each rule can be a story)\n"
            "- Split by data (different data types, different stories)\n\n"
            "**My Role in Refinement:**\n"
            "- Present business context for upcoming items\n"
            "- Facilitate discussion of requirements\n"
            "- Capture questions and action items\n"
            "- Update Product Backlog items with clarity\n"
            "- Ensure team understands business context\n\n"
            "Good refinement makes Sprint Planning smoother and development more effective."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_clarification_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about requirement clarification"""
        recommendations = [
            "Ask clarifying questions to probe for details",
            "Reference domain knowledge and existing processes",
            "Identify what's unclear or ambiguous",
            "Document clarifications and decisions",
            "Validate understanding with stakeholders",
            "Update requirements documentation with clarifications"
        ]
        
        questions = [
            "What specifically is unclear?",
            "What details are missing?",
            "What are the assumptions?",
            "Have we validated this with stakeholders?",
            "What questions need answers?",
            "What edge cases haven't been considered?"
        ]
        
        response_text = (
            "Clarification is a core part of my role. Let me help identify what needs to be clarified.\n\n"
            "**Clarification Approach:**\n"
            "1. **Identify Ambiguity:** What specifically is unclear?\n"
            "2. **Ask Probing Questions:** What details are missing?\n"
            "3. **Reference Context:** What do we know from existing processes?\n"
            "4. **Validate Assumptions:** What are we assuming?\n"
            "5. **Document Decisions:** Capture clarifications and rationale\n\n"
            "**Common Areas Needing Clarification:**\n"
            "- Business rules and logic\n"
            "- Edge cases and exceptions\n"
            "- Data requirements and constraints\n"
            "- User workflows and interactions\n"
            "- Acceptance criteria specifics\n"
            "- Stakeholder expectations\n\n"
            "**My Approach:**\n"
            "- Ask specific, probing questions\n"
            "- Use examples to clarify understanding\n"
            "- Reference existing business rules and processes\n"
            "- Validate with stakeholders when needed\n"
            "- Document clarifications clearly\n"
            "- Update requirements documentation\n\n"
            "**Anti-Pattern to Avoid:**\n"
            "Don't make assumptions. If something is unclear, ask. It's better to clarify "
            "now than to build the wrong thing."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_data_model_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about data modeling"""
        recommendations = [
            "Document entities, attributes, and relationships",
            "Identify primary keys and foreign keys",
            "Define data constraints and business rules",
            "Consider data relationships and dependencies",
            "Validate data model with stakeholders",
            "Make data model visible to team"
        ]
        
        questions = [
            "What entities are involved?",
            "What are the attributes of each entity?",
            "What are the relationships between entities?",
            "What are the primary keys and foreign keys?",
            "What data constraints apply?",
            "What business rules govern the data?"
        ]
        
        response_text = (
            "Data modeling helps us understand the information structure. Here's my approach:\n\n"
            "**Entity-Relationship Documentation:**\n"
            "Entity: [Name]\n"
            "Attributes:\n"
            "  - attribute_name (type, constraints)\n"
            "  - attribute_name (PK/FK if applicable)\n"
            "Relationships:\n"
            "  - Entity relates to other Entity (one-to-one, one-to-many, many-to-many)\n\n"
            "**Example:**\n"
            "Entity: Invoice\n"
            "Attributes:\n"
            "  - invoice_id (PK)\n"
            "  - invoice_number\n"
            "  - invoice_date\n"
            "  - client_id (FK)\n"
            "  - freelancer_id (FK)\n"
            "  - subtotal\n"
            "  - tax_amount\n"
            "  - total_amount\n"
            "  - status\n"
            "  - due_date\n\n"
            "Relationships:\n"
            "  - Invoice belongs to one Client\n"
            "  - Invoice belongs to one Freelancer\n"
            "  - Invoice has many LineItems\n\n"
            "**My Approach:**\n"
            "- Document entities and their attributes\n"
            "- Identify relationships and cardinality\n"
            "- Define data constraints and business rules\n"
            "- Validate with stakeholders\n"
            "- Make data model visible to team\n\n"
            "**Key Principles:**\n"
            "- Focus on business data needs, not technical implementation\n"
            "- Document business rules that govern data\n"
            "- Consider data relationships and dependencies\n"
            "- Validate with stakeholders who understand the domain"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with Business Analyst perspective"""
        response_text = (
            f"As a Business Analyst (part of Developers), my primary accountability is creating a usable "
            f"Increment each Sprint with business analysis expertise. Let me address your question: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Understand business context: Why is this needed? What's the business value?\n"
            f"- Clarify requirements: What problem are we solving? For whom?\n"
            f"- Define acceptance criteria: How will we know when this is complete?\n"
            f"- Bridge business and technical: Translate business needs into clear requirements\n"
            f"- Document business rules: Capture logic and constraints clearly\n\n"
            f"**Key Principles:**\n"
            f"- **Clarity over completeness:** Clear, testable requirements beat comprehensive documentation\n"
            f"- **Collaborate, don't dictate:** Requirements emerge through team collaboration\n"
            f"- **Iterative refinement:** Requirements evolve; refine continuously\n"
            f"- **Business value focus:** Always connect requirements to business outcomes\n"
            f"- **Stakeholder partnership:** Represent stakeholders, but you're part of the team\n\n"
            f"I'm committed to ensuring the team understands what to build and why. I bridge business and "
            f"technical perspectives, clarify requirements, and enable informed decisions."
        )
        
        recommendations = [
            "Clarify business need and value",
            "Define clear acceptance criteria",
            "Identify stakeholders and validate requirements",
            "Document business rules and edge cases",
            "Facilitate communication between business and technical teams",
            "Support Product Owner with Product Backlog refinement"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        if any(word in query_lower for word in ["product", "backlog", "priority", "value", "stakeholder"]):
            needs.append("product_owner")
        
        if any(word in query_lower for word in ["technical", "implementation", "feasibility", "code", "development"]):
            needs.append("development_engineer")
        
        if any(word in query_lower for word in ["test", "qa", "acceptance criteria", "testable"]):
            needs.append("qa_engineer")
        
        if any(word in query_lower for word in ["design", "ux", "ui", "user experience", "user flow"]):
            needs.append("ux_ui_designer")
        
        if any(word in query_lower for word in ["data", "metrics", "analytics", "reporting"]):
            needs.append("data_metrics_analyst")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "product_owner": "Product vision, business priorities, stakeholder needs, value articulation",
                "development_engineer": "Technical constraints, feasibility questions, implementation questions, edge cases discovered",
                "qa_engineer": "Test scenarios, edge cases discovered, ambiguity in requirements, testability concerns",
                "ux_ui_designer": "User research insights, user flows, design constraints, user experience requirements",
                "data_metrics_analyst": "User behavior patterns, metrics insights, data analysis, analytics requirements",
                "scrum_master": "Facilitation, coaching, impediment removal, requirements process improvements",
                "product_marketing_executive": "Market requirements, competitive insights, positioning needs, feature documentation needs"
            },
            "provides_to": {
                "product_owner": "Requirements analysis, acceptance criteria, stakeholder insights, Product Backlog refinement support",
                "development_engineer": "Requirements clarification, business context, edge cases, data models, business rules",
                "qa_engineer": "Requirements clarification, expected behaviors, business rules, acceptance criteria details",
                "ux_ui_designer": "Business requirements, process flows, business rules, data requirements, user journey context",
                "data_metrics_analyst": "Business metrics requirements, reporting needs, KPI definitions, data requirements",
                "scrum_master": "Requirements-related impediments, stakeholder access issues, requirements process improvements",
                "all_team_members": "Business context, requirements clarity, acceptance criteria, business rules, stakeholder insights"
            }
        }
