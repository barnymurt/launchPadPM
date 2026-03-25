"""
Data/Metrics Analyst Agent
Implements the Data/Metrics Analyst role (part of Developers) with expertise in:
- Product analytics and data instrumentation
- Metrics definition and tracking (North Star Metric, AARRR framework)
- A/B testing and experimentation
- User behavior analysis
- Data visualization and reporting
- Evidence-based decision making
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class DataMetricsAnalystAgent(BaseAgent):
    """
    Data/Metrics Analyst AI Agent
    
    Note: In Scrum, there is no separate "Data Analyst" role - you are a Developer 
    who specializes in data and metrics. All Developers are accountable for creating value.
    
    Primary Accountability: Creating any aspect of a usable Increment each Sprint 
    (with data analytics expertise).
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Data/Metrics Analyst",
            name="Data",
            context=context
        )
        self.metrics = {}
        self.experiments = []
        self.dashboards = {}
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Data/Metrics Analyst's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Creating any aspect of a usable Increment each Sprint (with data analytics expertise)",
            "note": "In Scrum, there is no separate 'Data Analyst' role - you are a Developer who specializes in data and metrics. All Developers are accountable for creating value.",
            "key_responsibilities": {
                "metrics_analytics": [
                    "Defining and tracking product metrics (North Star Metric, KPIs)",
                    "Implementing analytics instrumentation",
                    "Analyzing user behavior and product usage",
                    "Supporting outcome-based product decisions",
                    "Creating dashboards and reports"
                ],
                "developer_responsibilities": [
                    "Participating in Sprint Planning",
                    "Contributing to Sprint Backlog",
                    "Adapting work daily toward Sprint Goal",
                    "Creating usable Increment (analytics features, dashboards, instrumentation)",
                    "Owning Sprint Backlog alongside fellow Developers"
                ],
                "experimentation": [
                    "Designing A/B tests and experiments",
                    "Analyzing experiment results",
                    "Determining statistical significance",
                    "Providing recommendations based on data"
                ]
            },
            "north_star_metric": {
                "definition": "The single metric that best captures the core value your product delivers to customers",
                "characteristics": [
                    "Measures value delivered, not just activity",
                    "Leading indicator of sustainable growth",
                    "Actionable by the team",
                    "Connected to business outcomes"
                ],
                "framework": [
                    "What's the core value your product provides?",
                    "What user action represents getting that value?",
                    "How often should users get that value to be successful?",
                    "How do we measure that action?"
                ]
            },
            "aarrr_framework": {
                "acquisition": "How do users discover your product? (traffic sources, sign-up rate, CPA, conversion rate)",
                "activation": "Do users have a great first experience? (onboarding completion, time to first value, aha moment)",
                "retention": "Do users come back? (Day 1/7/30 retention, churn rate, cohort analysis)",
                "revenue": "How do you make money? (conversion to paid, ARPU, LTV, MRR)",
                "referral": "Do users tell others? (viral coefficient, NPS, referral rate)"
            },
            "event_tracking": {
                "structure": "Event Name: [Object]_[Action] with properties (user_id, timestamp, object_type, object_id, action_context, metadata)",
                "key_events": [
                    "User Authentication: signed_up, logged_in, logged_out",
                    "Core Feature Usage: [feature]_viewed, [feature]_started, [feature]_completed, [feature]_abandoned",
                    "Business Actions: purchase_completed, subscription_started, payment_failed",
                    "Errors: error_occurred (with error type, message, context)"
                ]
            },
            "data_quality": {
                "principles": [
                    "Accuracy: Events fire when they should, data is correct",
                    "Completeness: All important user actions are tracked",
                    "Consistency: Event naming and structure follows standards",
                    "Timeliness: Data available for analysis without excessive delay",
                    "Validity: Data passes validation rules"
                ]
            },
            "ab_testing": {
                "hypothesis_format": "We believe that [making this change] For [these users] Will result in [this outcome] We'll know we're right when we see [this measurable signal]",
                "statistical_significance": "p < 0.05, minimum sample size, minimum duration (1-2 weeks), consistent results",
                "when_to_call": "Statistical significance reached, minimum sample size achieved, test ran for minimum duration, results are consistent",
                "when_not_to_call_early": "Results look good but not significant yet, sample size too small, high variance, external factors affecting test"
            },
            "anti_patterns": [
                "Vanity Metrics Focus - Track meaningful metrics (outcomes), not just activity (outputs)",
                "Analysis Paralysis - Perfect data beats timely insights; balance accuracy with speed",
                "Data Without Context - Always provide business interpretation, not just numbers",
                "Confirmation Bias - Let data speak; don't cherry-pick to support preferences",
                "Tracking Everything - Focus on actionable metrics aligned with Product Goal",
                "Ignoring Qualitative Data - Combine quantitative data with user interviews and feedback",
                "Calling Tests Early - Wait for statistical significance and minimum duration"
            ]
        }
    
    def _hardcoded_process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a Data/Metrics Analyst perspective.
        Focuses on metrics, analytics, and evidence-based insights.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler
        if any(word in query_lower for word in ["metric", "metrics", "kpi", "track", "measure"]):
            return self._handle_metrics_query(query, **kwargs)
        elif any(word in query_lower for word in ["north star", "northstar", "core metric"]):
            return self._handle_north_star_query(query, **kwargs)
        elif any(word in query_lower for word in ["aarrr", "acquisition", "activation", "retention", "revenue", "referral"]):
            return self._handle_aarrr_query(query, **kwargs)
        elif any(word in query_lower for word in ["a/b test", "ab test", "experiment", "testing", "hypothesis"]):
            return self._handle_experiment_query(query, **kwargs)
        elif any(word in query_lower for word in ["track", "tracking", "event", "instrumentation", "analytics"]):
            return self._handle_tracking_query(query, **kwargs)
        elif any(word in query_lower for word in ["dashboard", "report", "visualization", "chart"]):
            return self._handle_dashboard_query(query, **kwargs)
        elif any(word in query_lower for word in ["funnel", "drop", "drop-off", "abandon", "conversion"]):
            return self._handle_funnel_query(query, **kwargs)
        elif any(word in query_lower for word in ["user behavior", "behavior", "usage", "adoption"]):
            return self._handle_behavior_query(query, **kwargs)
        elif any(word in query_lower for word in ["data quality", "accuracy", "validation", "data"]):
            return self._handle_data_quality_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_metrics_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about metrics definition and tracking"""
        recommendations = [
            "Define metrics aligned with Product Goal and Sprint Goal",
            "Focus on outcome metrics, not just activity metrics",
            "Make metrics visible and accessible to the team",
            "Track trends over time, not just point-in-time values",
            "Include targets and thresholds for context",
            "Connect metrics to business outcomes",
            "Balance accuracy with timeliness"
        ]
        
        questions = [
            "What's the Product Goal? What metrics indicate success?",
            "Are we measuring outcomes or just activity?",
            "What's the target or threshold for this metric?",
            "How does this metric connect to business value?",
            "What's the trend over time?",
            "What's the confidence level in the data?"
        ]
        
        response_text = (
            "Metrics help us understand if we're achieving our goals. Here's my approach:\n\n"
            "**Metrics Principles:**\n"
            "- **Outcomes over Outputs:** Measure value delivered, not features shipped\n"
            "- **Aligned with Goals:** Metrics should connect to Product Goal and Sprint Goal\n"
            "- **Actionable:** Every metric should inform a decision\n"
            "- **Visible:** Make metrics accessible to the whole team\n"
            "- **Trends Matter:** Track over time, not just point-in-time\n\n"
            "**Key Metrics Categories:**\n"
            "- **North Star Metric:** The single metric that best captures core value\n"
            "- **AARRR Metrics:** Acquisition, Activation, Retention, Revenue, Referral\n"
            "- **Product Goal Metrics:** Specific metrics tied to Product Goal\n"
            "- **Sprint Goal Metrics:** Metrics indicating Sprint Goal achievement\n\n"
            "**My Approach:**\n"
            "- Define metrics in collaboration with Product Owner\n"
            "- Ensure metrics are measurable and trackable\n"
            "- Set targets and thresholds\n"
            "- Create dashboards for visibility\n"
            "- Analyze trends and provide insights\n"
            "- Support evidence-based decision making\n\n"
            "**Anti-Patterns to Avoid:**\n"
            "- Vanity metrics (activity without value)\n"
            "- Tracking everything (focus on what matters)\n"
            "- Data without context (always interpret)\n"
            "- Confirmation bias (let data speak)\n\n"
            "Let me help you define and track the right metrics for your goals."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner"]
        )
    
    def _handle_north_star_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about North Star Metric"""
        recommendations = [
            "North Star Metric is the single metric that best captures core value",
            "Measures value delivered, not just activity",
            "Leading indicator of sustainable growth",
            "Actionable by the team",
            "Connected to business outcomes",
            "Use framework: What's core value? What action represents it? How often? How measure?"
        ]
        
        questions = [
            "What's the core value your product provides?",
            "What user action represents getting that value?",
            "How often should users get that value to be successful?",
            "How do we measure that action?",
            "Is this a leading indicator of growth?",
            "Is this actionable by the team?"
        ]
        
        response_text = (
            "The North Star Metric is the single metric that best captures the core value "
            "your product delivers to customers.\n\n"
            "**North Star Metric Characteristics:**\n"
            "- **Measures Value Delivered:** Not just activity, but actual value\n"
            "- **Leading Indicator:** Predicts sustainable growth\n"
            "- **Actionable:** Team can influence it\n"
            "- **Connected to Business Outcomes:** Links to business success\n\n"
            "**Framework for Defining North Star Metric:**\n"
            "1. What's the core value your product provides?\n"
            "2. What user action represents getting that value?\n"
            "3. How often should users get that value to be successful?\n"
            "4. How do we measure that action?\n\n"
            "**Examples by Product Type:**\n"
            "- **SaaS Productivity Tool:** Weekly Active Users completing core workflow\n"
            "- **E-commerce:** Number of orders per month\n"
            "- **Media/Content:** Hours of content consumed per user per week\n"
            "- **Marketplace:** Successful transactions per week\n\n"
            "**My Role:**\n"
            "- Help Product Owner define the North Star Metric\n"
            "- Ensure it's measurable and trackable\n"
            "- Create dashboards to monitor it\n"
            "- Analyze trends and provide insights\n"
            "- Connect other metrics to the North Star\n\n"
            "The North Star Metric provides focus and direction for the entire product team."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner"]
        )
    
    def _handle_aarrr_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about AARRR framework (Pirate Metrics)"""
        recommendations = [
            "Use AARRR framework to understand user journey: Acquisition, Activation, Retention, Revenue, Referral",
            "Track metrics for each stage of the funnel",
            "Identify where users drop off in the journey",
            "Focus improvement efforts on stages with highest impact",
            "Connect AARRR metrics to Product Goal",
            "Create dashboards for each stage"
        ]
        
        questions = [
            "What's our acquisition strategy? How do users discover us?",
            "What's the activation experience? Do users have a great first experience?",
            "What's our retention rate? Do users come back?",
            "How do we make money? What's our revenue model?",
            "Do users refer others? What's our referral rate?",
            "Where are users dropping off in the funnel?"
        ]
        
        response_text = (
            "The AARRR framework (Pirate Metrics) helps us understand the user journey from "
            "discovery to advocacy.\n\n"
            "**AARRR Framework:**\n\n"
            "**Acquisition:** How do users discover your product?\n"
            "- Traffic sources\n"
            "- Sign-up rate\n"
            "- Cost per acquisition (CPA)\n"
            "- Conversion rate from visitor to sign-up\n\n"
            "**Activation:** Do users have a great first experience?\n"
            "- Onboarding completion rate\n"
            "- Time to first value\n"
            "- Features used in first session\n"
            "- 'Aha moment' rate\n\n"
            "**Retention:** Do users come back?\n"
            "- Day 1, Day 7, Day 30 retention rates\n"
            "- Churn rate\n"
            "- Cohort analysis\n"
            "- Feature engagement over time\n\n"
            "**Revenue:** How do you make money?\n"
            "- Conversion to paid\n"
            "- Average revenue per user (ARPU)\n"
            "- Lifetime value (LTV)\n"
            "- Monthly recurring revenue (MRR)\n\n"
            "**Referral:** Do users tell others?\n"
            "- Viral coefficient\n"
            "- Net Promoter Score (NPS)\n"
            "- Referral rate\n"
            "- Share/invite actions\n\n"
            "**My Approach:**\n"
            "- Track metrics for each stage\n"
            "- Identify drop-off points\n"
            "- Analyze trends and patterns\n"
            "- Provide insights for improvement\n"
            "- Connect to Product Goal\n\n"
            "Understanding the AARRR funnel helps identify where to focus improvement efforts."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "product_marketing_executive"]
        )
    
    def _handle_experiment_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about A/B testing and experimentation"""
        recommendations = [
            "Use hypothesis format: We believe [change] For [users] Will result in [outcome] We'll know when [signal]",
            "Calculate sample size: baseline conversion, minimum detectable effect, statistical power (80%), significance (95%)",
            "Run for minimum duration: 1-2 weeks (full user behavior cycle)",
            "Wait for statistical significance: p < 0.05, minimum sample size, consistent results",
            "Don't call tests early: wait for significance, avoid high variance, account for external factors",
            "Provide recommendations based on results"
        ]
        
        questions = [
            "What's the hypothesis?",
            "What's the baseline conversion rate?",
            "What's the minimum detectable effect?",
            "What's the sample size needed?",
            "How long should the test run?",
            "What's the statistical significance?",
            "Are results consistent?"
        ]
        
        response_text = (
            "A/B testing helps us validate hypotheses with data. Here's my approach:\n\n"
            "**Experiment Design:**\n\n"
            "**Hypothesis Format:**\n"
            "We believe that [making this change]\n"
            "For [these users]\n"
            "Will result in [this outcome]\n"
            "We'll know we're right when we see [this measurable signal]\n\n"
            "**Example:**\n"
            "We believe that adding one-click invoice templates\n"
            "For freelancers creating their first 5 invoices\n"
            "Will result in higher invoice completion rates\n"
            "We'll know we're right when we see completion rate increase from 70% to 85%\n\n"
            "**Experiment Components:**\n"
            "- **Control Group (A):** Current experience\n"
            "- **Treatment Group (B):** New experience with change\n\n"
            "**Sample Size Calculation:**\n"
            "- Baseline conversion rate\n"
            "- Minimum detectable effect\n"
            "- Statistical power (typically 80%)\n"
            "- Significance level (typically 95%)\n\n"
            "**Duration:**\n"
            "- Run until statistical significance achieved\n"
            "- Minimum: 1-2 weeks (full user behavior cycle)\n"
            "- Account for day-of-week and seasonal effects\n\n"
            "**When to Call a Test:**\n"
            "- Statistical significance reached (p < 0.05)\n"
            "- Minimum sample size achieved\n"
            "- Test ran for minimum duration\n"
            "- Results are consistent (not fluctuating wildly)\n\n"
            "**When NOT to Call Early:**\n"
            "- Results look good but not significant yet\n"
            "- Sample size too small\n"
            "- High variance in results\n"
            "- External factors affecting test (marketing campaign, outage, etc.)\n\n"
            "**My Role:**\n"
            "- Design experiments with clear hypotheses\n"
            "- Calculate sample sizes and duration\n"
            "- Analyze results for statistical significance\n"
            "- Provide recommendations based on data\n"
            "- Document learnings and insights"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "ux_ui_designer"]
        )
    
    def _handle_tracking_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about event tracking and instrumentation"""
        recommendations = [
            "Use event structure: [Object]_[Action] with properties (user_id, timestamp, object_type, object_id, context, metadata)",
            "Track key events: authentication, core feature usage, business actions, errors",
            "Follow data quality principles: accuracy, completeness, consistency, timeliness, validity",
            "Track on backend for reliability",
            "Send to analytics platform for real-time analysis",
            "Validate events fire correctly and capture correct data"
        ]
        
        questions = [
            "What events should we track?",
            "What properties should each event have?",
            "Where should events be tracked? (frontend, backend, both)",
            "How do we validate events are firing correctly?",
            "What's the event naming convention?",
            "How do we ensure data quality?"
        ]
        
        response_text = (
            "Event tracking is the foundation of analytics. Here's my approach:\n\n"
            "**Event Structure:**\n"
            "Event Name: [Object]_[Action]\n"
            "Properties:\n"
            "  - user_id\n"
            "  - timestamp\n"
            "  - object_type\n"
            "  - object_id\n"
            "  - action_context\n"
            "  - relevant_metadata\n\n"
            "**Example:**\n"
            "Event: invoice_created\n"
            "Properties:\n"
            "  - user_id: 'user_12345'\n"
            "  - timestamp: '2026-01-12T10:30:00Z'\n"
            "  - invoice_id: 'inv_789'\n"
            "  - invoice_amount: 1500.00\n"
            "  - line_item_count: 5\n"
            "  - generation_method: 'automatic'\n"
            "  - time_to_create_seconds: 180\n\n"
            "**Key Events to Track:**\n"
            "- **User Authentication:** signed_up, logged_in, logged_out\n"
            "- **Core Feature Usage:** [feature]_viewed, [feature]_started, [feature]_completed, [feature]_abandoned\n"
            "- **Business Actions:** purchase_completed, subscription_started, payment_failed\n"
            "- **Errors:** error_occurred (with error type, message, context)\n\n"
            "**Data Quality Principles:**\n"
            "1. **Accuracy:** Events fire when they should, data is correct\n"
            "2. **Completeness:** All important user actions are tracked\n"
            "3. **Consistency:** Event naming and structure follows standards\n"
            "4. **Timeliness:** Data available for analysis without excessive delay\n"
            "5. **Validity:** Data passes validation rules\n\n"
            "**Implementation Notes:**\n"
            "- Track on backend (more reliable than frontend)\n"
            "- Include event in database for historical analysis\n"
            "- Send to analytics platform (Mixpanel/Amplitude) for real-time\n"
            "- Log errors separately for debugging\n\n"
            "**Testing:**\n"
            "After implementation, validate:\n"
            "- Events fire at right times\n"
            "- Properties capture correct data\n"
            "- No duplicate events\n"
            "- Events appear in analytics dashboard"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "qa_engineer"]
        )
    
    def _handle_dashboard_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about dashboards and reporting"""
        recommendations = [
            "Design dashboards for specific audiences: executive, product team, engineering",
            "Make dashboards actionable: every metric should inform a decision",
            "Use visual hierarchy: most important metrics prominent",
            "Include targets and thresholds for context",
            "Show trends over time",
            "Update frequency matches decision needs",
            "Alert on significant changes"
        ]
        
        questions = [
            "Who is the audience for this dashboard?",
            "What decisions will this dashboard inform?",
            "What are the most important metrics?",
            "What are the targets or thresholds?",
            "How often should it update?",
            "What trends should be visible?"
        ]
        
        response_text = (
            "Dashboards make data accessible and actionable. Here's my approach:\n\n"
            "**Dashboard Design Principles:**\n\n"
            "1. **Audience-Specific:**\n"
            "   - Executive dashboard: High-level metrics, trends, business outcomes\n"
            "   - Product team dashboard: Feature usage, user behavior, experiment results\n"
            "   - Engineering dashboard: Technical metrics, errors, performance\n\n"
            "2. **Actionable:**\n"
            "   - Every metric should inform a decision\n"
            "   - Include targets and thresholds\n"
            "   - Show trends over time\n\n"
            "3. **Visual Hierarchy:**\n"
            "   - Most important metrics prominent\n"
            "   - Use colors meaningfully (red = bad, green = good)\n"
            "   - Minimize clutter\n\n"
            "4. **Real-Time or Refreshed:**\n"
            "   - Update frequency matches decision needs\n"
            "   - Show last updated timestamp\n"
            "   - Alert on significant changes\n\n"
            "**Report Structure:**\n"
            "- **Executive Summary:** Key metric performance, major insights, recommended actions\n"
            "- **Detailed Analysis:** Trend charts, cohort analysis, segment breakdowns, statistical tests\n"
            "- **Appendix:** Methodology, data quality notes, detailed tables, additional context\n\n"
            "**My Approach:**\n"
            "- Design dashboards for specific audiences\n"
            "- Focus on actionable metrics\n"
            "- Make data accessible and understandable\n"
            "- Provide context and interpretation\n"
            "- Update regularly and alert on changes"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "business_analyst"]
        )
    
    def _handle_funnel_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about funnel analysis and drop-offs"""
        recommendations = [
            "Analyze funnel step-by-step to identify drop-off points",
            "Compare time spent on steps between completers and abandoners",
            "Analyze error events at each step",
            "Break down by user segments (new vs. returning, device, etc.)",
            "Identify where users struggle most",
            "Suggest experiments to improve conversion",
            "Set up alerts for significant drop-off increases"
        ]
        
        questions = [
            "What are the steps in the funnel?",
            "Where are users dropping off?",
            "What's the drop-off rate at each step?",
            "How long do users spend on each step?",
            "What errors occur at each step?",
            "How does drop-off vary by user segment?",
            "What can we test to improve conversion?"
        ]
        
        response_text = (
            "Funnel analysis helps us understand where users struggle and drop off. "
            "Here's my approach:\n\n"
            "**Funnel Analysis Process:**\n"
            "1. **Map the Funnel:** Identify all steps in the user journey\n"
            "2. **Calculate Conversion:** Measure drop-off at each step\n"
            "3. **Identify Drop-Off Points:** Where are users leaving?\n"
            "4. **Deep Dive:** Analyze time spent, errors, user segments\n"
            "5. **Recommend Actions:** Suggest improvements and experiments\n\n"
            "**Key Metrics to Analyze:**\n"
            "- Conversion rate at each step\n"
            "- Drop-off rate between steps\n"
            "- Time spent on each step (completers vs. abandoners)\n"
            "- Error events at each step\n"
            "- User segment breakdown (new vs. returning, device, etc.)\n\n"
            "**Example Analysis:**\n"
            "Step 1: Started → 100% (500 users)\n"
            "Step 2: Added info → 92% (460 users) - 8% drop-off\n"
            "Step 3: Added items → 85% (425 users) - 7% drop-off\n"
            "Step 4: Payment details → 70% (350 users) - 15% drop-off ⚠️\n"
            "Step 5: Previewed → 68% (340 users) - 2% drop-off\n"
            "Step 6: Finalized → 65% (325 users) - 3% drop-off\n\n"
            "**Key Finding:** 15% drop-off at Step 4 (payment details)\n\n"
            "**Deep Dive on Drop-Offs:**\n"
            "- Time spent: Abandoners spend 3x longer (suggests confusion)\n"
            "- Errors: 45 validation errors (invalid format, tax ID issues)\n"
            "- Segments: New users 4x higher drop-off than power users\n"
            "- Device: Mobile 2x higher drop-off than desktop\n\n"
            "**My Recommendations:**\n"
            "- Improve validation messaging\n"
            "- Add inline help for new users\n"
            "- Optimize mobile experience\n"
            "- A/B test improvements\n\n"
            "Funnel analysis helps identify where to focus improvement efforts."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "ux_ui_designer", "development_engineer"]
        )
    
    def _handle_behavior_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about user behavior analysis"""
        recommendations = [
            "Analyze user behavior patterns and trends",
            "Segment users by behavior (power users, regular users, struggling users)",
            "Track feature adoption and usage frequency",
            "Analyze retention and engagement",
            "Compare behavior across user segments",
            "Identify patterns that indicate success or struggle",
            "Provide insights for product improvements"
        ]
        
        questions = [
            "What user behaviors are we analyzing?",
            "How are users segmented?",
            "What's the adoption rate?",
            "What's the usage frequency?",
            "What's the retention rate?",
            "How does behavior vary by segment?",
            "What patterns indicate success or struggle?"
        ]
        
        response_text = (
            "User behavior analysis helps us understand how users actually use the product. "
            "Here's my approach:\n\n"
            "**User Behavior Analysis:**\n\n"
            "**Key Metrics:**\n"
            "- **Adoption Rate:** % of users who have used a feature\n"
            "- **Frequency:** How often users use features\n"
            "- **Completion Rate:** % who complete workflows\n"
            "- **Time to Value:** How long until users get value\n"
            "- **Retention:** Do users come back?\n"
            "- **Engagement:** How actively users interact\n\n"
            "**User Segmentation:**\n"
            "- **Power Users:** High frequency, high engagement\n"
            "- **Regular Users:** Moderate frequency, consistent usage\n"
            "- **Struggling Users:** Low frequency, low completion\n"
            "- **New Users:** Recently onboarded\n"
            "- **Returning Users:** Coming back after time away\n\n"
            "**Analysis Approach:**\n"
            "- Track feature usage over time\n"
            "- Compare behavior across segments\n"
            "- Identify patterns that indicate success\n"
            "- Find where users struggle\n"
            "- Correlate behavior with outcomes (retention, revenue)\n\n"
            "**Example Insights:**\n"
            "- Users who create 1 invoice are 3x more likely to create a 2nd\n"
            "- Users who create invoices have 40% higher Day-30 retention\n"
            "- 35% of users start but don't complete (need investigation)\n"
            "- Power users (10%) create 5+ invoices/week with 95% completion\n\n"
            "**My Role:**\n"
            "- Analyze user behavior patterns\n"
            "- Segment users by behavior\n"
            "- Provide insights for product improvements\n"
            "- Support evidence-based decisions\n"
            "- Identify opportunities for improvement"
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "ux_ui_designer"]
        )
    
    def _handle_data_quality_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about data quality"""
        recommendations = [
            "Ensure accuracy: events fire when they should, data is correct",
            "Ensure completeness: all important user actions are tracked",
            "Ensure consistency: event naming and structure follows standards",
            "Ensure timeliness: data available for analysis without excessive delay",
            "Ensure validity: data passes validation rules",
            "Validate events fire correctly and capture correct data",
            "Monitor data quality continuously"
        ]
        
        questions = [
            "Are events firing when they should?",
            "Is the data accurate?",
            "Are all important actions tracked?",
            "Is event naming consistent?",
            "Is data available in a timely manner?",
            "Does data pass validation rules?",
            "How do we monitor data quality?"
        ]
        
        response_text = (
            "Data quality is fundamental to trustworthy analytics. Here's my approach:\n\n"
            "**Data Quality Principles:**\n\n"
            "1. **Accuracy:**\n"
            "   - Events fire when they should\n"
            "   - Data is correct and reflects reality\n"
            "   - No duplicate or missing events\n\n"
            "2. **Completeness:**\n"
            "   - All important user actions are tracked\n"
            "   - No gaps in tracking\n"
            "   - Coverage of key workflows\n\n"
            "3. **Consistency:**\n"
            "   - Event naming follows standards\n"
            "   - Event structure is consistent\n"
            "   - Properties are standardized\n\n"
            "4. **Timeliness:**\n"
            "   - Data available for analysis without excessive delay\n"
            "   - Real-time or near-real-time when needed\n"
            "   - Historical data accessible\n\n"
            "5. **Validity:**\n"
            "   - Data passes validation rules\n"
            "   - Values are within expected ranges\n"
            "   - No corrupted or invalid data\n\n"
            "**Validation Process:**\n"
            "- Test events fire at right times\n"
            "- Verify properties capture correct data\n"
            "- Check for duplicate events\n"
            "- Validate data ranges and formats\n"
            "- Monitor data quality continuously\n\n"
            "**My Role:**\n"
            "- Define data quality standards\n"
            "- Validate tracking implementation\n"
            "- Monitor data quality continuously\n"
            "- Identify and fix data quality issues\n"
            "- Ensure trustworthy analytics\n\n"
            "**Remember:** Garbage in, garbage out. Data quality matters."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["development_engineer", "qa_engineer"]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with Data/Metrics Analyst perspective"""
        response_text = (
            f"As a Data/Metrics Analyst (part of Developers), my primary accountability is creating a usable "
            f"Increment each Sprint with data analytics expertise. Let me address your question: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Start with the metric: What does the data actually show?\n"
            f"- Provide context: How does this compare? What's the trend?\n"
            f"- Interpret: What does this mean for the product/business?\n"
            f"- Recommend: What action does the data suggest?\n"
            f"- Suggest experiments: How could we validate further?\n"
            f"- Acknowledge uncertainty: What don't we know? What's the confidence level?\n\n"
            f"**Key Principles:**\n"
            f"- **Outcomes over Outputs:** Measure value delivered, not features shipped\n"
            f"- **Evidence-Based Decisions:** Let data inform, but not dictate, decisions\n"
            f"- **Data Quality Matters:** Garbage in, garbage out\n"
            f"- **Experimentation Mindset:** Everything is a hypothesis to be tested\n"
            f"- **Transparency:** Make metrics visible and accessible to whole team\n\n"
            f"I'm committed to enabling evidence-based product decisions. I make data accessible, "
            f"insights actionable, and experimentation rigorous."
        )
        
        recommendations = [
            "Provide data context and confidence levels",
            "Quantify impact with numbers and percentages",
            "Visualize trends and patterns when helpful",
            "Acknowledge data limitations and confounding factors",
            "Recommend actions based on data",
            "Suggest experiments to test hypotheses"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        if any(word in query_lower for word in ["product", "goal", "metric", "outcome", "priority"]):
            needs.append("product_owner")
        
        if any(word in query_lower for word in ["track", "event", "instrumentation", "implementation", "technical"]):
            needs.append("development_engineer")
        
        if any(word in query_lower for word in ["test", "qa", "validation", "data quality", "accuracy"]):
            needs.append("qa_engineer")
        
        if any(word in query_lower for word in ["design", "ux", "ui", "user experience", "ab test"]):
            needs.append("ux_ui_designer")
        
        if any(word in query_lower for word in ["requirement", "business", "report", "dashboard"]):
            needs.append("business_analyst")
        
        if any(word in query_lower for word in ["marketing", "campaign", "acquisition", "attribution"]):
            needs.append("product_marketing_executive")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "product_owner": "Product Goals, outcome metrics, prioritization questions, success criteria",
                "development_engineer": "Technical constraints, implementation questions, event tracking implementation",
                "qa_engineer": "Testing needs for analytics, data accuracy questions, validation requirements",
                "ux_ui_designer": "User research insights, design hypotheses, A/B test design needs",
                "business_analyst": "Business rules, reporting requirements, KPI definitions, dashboard needs",
                "scrum_master": "Coaching, facilitation, impediment removal, data infrastructure blockers",
                "product_marketing_executive": "Marketing campaign tracking needs, conversion goals, attribution requirements"
            },
            "provides_to": {
                "product_owner": "User behavior data, metrics performance, experiment results, ROI analysis, evidence-based insights",
                "development_engineer": "Event tracking requirements, analytics specifications, data access needs, instrumentation guidance",
                "qa_engineer": "Test data, expected analytics outputs, validation criteria, data quality standards",
                "ux_ui_designer": "Quantitative user behavior data, usage patterns, feature adoption metrics, A/B test results",
                "business_analyst": "Data models, metric calculations, business intelligence, report specifications",
                "scrum_master": "Team performance metrics, data infrastructure blockers, analytics process improvements",
                "product_marketing_executive": "Attribution data, campaign performance, user segment analysis, conversion funnel analysis",
                "all_team_members": "Metrics dashboards, user behavior insights, experiment results, evidence-based recommendations"
            }
        }
