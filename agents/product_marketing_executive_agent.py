"""
Product Marketing Executive Agent
Implements the Product Marketing Executive role (Key Stakeholder) with expertise in:
- Go-to-market (GTM) strategy and execution
- Product positioning and messaging
- Customer acquisition and growth marketing
- Launch planning and coordination
- Competitive analysis and market intelligence
- Customer lifecycle marketing (onboarding, engagement, retention)
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class ProductMarketingExecutiveAgent(BaseAgent):
    """
    Product Marketing Executive AI Agent
    
    Note: You are NOT part of the core Scrum Team (Product Owner, Scrum Master, Developers),
    but you are a Key Stakeholder who collaborates closely with the team.
    
    Your Role:
    - Translate product capabilities into customer value
    - Bring market and customer feedback to the team
    - Ensure successful product launches and adoption
    - Drive customer acquisition, activation, and retention
    - Connect product development to business outcomes
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Product Marketing Executive",
            name="Marketing",
            context=context
        )
        self.gtm_strategy = {}
        self.competitive_intelligence = {}
        self.launch_plans = []
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define Product Marketing Executive's specialized knowledge and responsibilities"""
        return {
            "relationship_to_scrum_team": "Key Stakeholder (NOT part of core Scrum Team)",
            "note": "You are NOT part of the core Scrum Team (Product Owner, Scrum Master, Developers), but you are a Key Stakeholder who collaborates closely with the team.",
            "key_responsibilities": {
                "translate_product_to_value": "Translate product capabilities into customer value",
                "bring_market_feedback": "Bring market and customer feedback to the team",
                "ensure_successful_launches": "Ensure successful product launches and adoption",
                "drive_acquisition_retention": "Drive customer acquisition, activation, and retention",
                "connect_to_business_outcomes": "Connect product development to business outcomes"
            },
            "collaboration_model": {
                "attend": ["Sprint Reviews (as stakeholder)", "Product Backlog Refinement (optional)"],
                "not_attend": ["Sprint Planning (unless specifically invited)", "Daily Scrum (never - Developers only)", "Sprint Retrospective (internal team improvement)"],
                "coordinate": ["Release planning", "Launch timing", "GTM approach"]
            },
            "gtm_framework": {
                "market_analysis": "TAM/SAM/SOM, customer segments, competitive landscape, market trends",
                "positioning": "Category, differentiation, value proposition, target audience",
                "messaging": "Core message, key messages, proof points, customer stories",
                "pricing_packaging": "Pricing model, price points, packaging, competitive pricing",
                "channels": "Acquisition channels (SEO, SEM, content, social, partnerships, direct sales, referrals), channel priority, CAC by channel",
                "launch_plan": "Launch timeline, deliverables, activities, success metrics"
            },
            "aarrr_framework": {
                "acquisition": "Getting users - landing pages, SEO, paid ads, partnerships, PR, referrals",
                "activation": "First value experience - onboarding, tours, welcome campaigns, aha moment",
                "retention": "Keeping users engaged - engagement emails, re-engagement, announcements, community",
                "revenue": "Monetization - free-to-paid conversion, upsell/cross-sell, pricing optimization",
                "referral": "Turning customers into advocates - referral programs, testimonials, reviews, ambassador programs"
            },
            "competitive_intelligence": {
                "product_comparison": "Features, pricing, target market, strengths, weaknesses",
                "positioning": "How competitors describe themselves, value props, messaging",
                "marketing": "Channels, content, SEO, social presence",
                "differentiation": "Why choose us, unique value, proof points"
            },
            "launch_planning": {
                "4_weeks_before": "Positioning/messaging finalized, launch plan documented, landing pages designed, content calendar, teams briefed, beta testers recruited",
                "2_weeks_before": "Landing pages developed, content written, email campaigns created, social content prepared, PR initiated, demo ready, analytics verified",
                "launch_week": "Final testing, announcement published, email sent, social posts, PR distribution, teams ready, monitor metrics",
                "post_launch": "Monitor adoption, gather feedback, adjust messaging, continue marketing, create success stories, iterate campaigns"
            },
            "messaging_framework": {
                "value_proposition_canvas": "Customer jobs (functional/social/emotional), pains, gains, pain relievers, gain creators",
                "message_testing": "A/B testing value props, feature emphases, CTAs, customer feedback, use customer language"
            },
            "anti_patterns": [
                "Dictating priorities to Product Owner - collaborate, don't dictate",
                "Ignoring technical constraints - understand what's feasible",
                "Launching without team alignment - coordinate with Product Owner",
                "Focusing only on acquisition - consider full customer lifecycle",
                "Ignoring customer feedback - bring market voice to team"
            ]
        }
    
    def _hardcoded_process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a Product Marketing Executive perspective.
        Focuses on GTM strategy, positioning, messaging, and customer acquisition.
        """
        query_lower = query.lower()
        
        # Route to appropriate handler
        if any(word in query_lower for word in ["launch", "release", "go-to-market", "gtm"]):
            return self._handle_launch_query(query, **kwargs)
        elif any(word in query_lower for word in ["positioning", "messaging", "value proposition", "message"]):
            return self._handle_messaging_query(query, **kwargs)
        elif any(word in query_lower for word in ["competitor", "competitive", "market", "competition"]):
            return self._handle_competitive_query(query, **kwargs)
        elif any(word in query_lower for word in ["acquisition", "customer", "growth", "channel", "marketing"]):
            return self._handle_acquisition_query(query, **kwargs)
        elif any(word in query_lower for word in ["pricing", "package", "tier", "plan"]):
            return self._handle_pricing_query(query, **kwargs)
        elif any(word in query_lower for word in ["onboarding", "activation", "retention", "aarrr", "lifecycle"]):
            return self._handle_lifecycle_query(query, **kwargs)
        elif any(word in query_lower for word in ["beta", "test", "bug", "delay", "quality"]):
            return self._handle_launch_decision_query(query, **kwargs)
        elif any(word in query_lower for word in ["api", "integration", "partner", "requirement"]):
            return self._handle_marketing_requirement_query(query, **kwargs)
        else:
            return self._handle_general_query(query, **kwargs)
    
    def _handle_launch_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about product launches and go-to-market"""
        recommendations = [
            "Coordinate launch timing with Product Owner and team",
            "Create comprehensive launch plan (4 weeks before launch)",
            "Prepare all marketing assets and content",
            "Brief sales and support teams",
            "Set up analytics and tracking",
            "Monitor metrics post-launch and iterate",
            "Align on success metrics before launch"
        ]
        
        questions = [
            "What's the launch date and Sprint timeline?",
            "What marketing assets do we need?",
            "What are the success metrics?",
            "Who are the target customers?",
            "What channels will we use?",
            "What's the positioning and messaging?",
            "What support do we need from the team?"
        ]
        
        response_text = (
            "Let me help you plan a successful product launch. Here's my approach:\n\n"
            "**Launch Planning Framework:**\n\n"
            "**4 Weeks Before Launch:**\n"
            "- Positioning and messaging finalized\n"
            "- Launch plan documented and shared\n"
            "- Landing pages designed\n"
            "- Marketing content calendar created\n"
            "- Sales/support teams briefed\n"
            "- Beta testers recruited\n\n"
            "**2 Weeks Before Launch:**\n"
            "- Landing pages developed and tested\n"
            "- Blog posts and content written\n"
            "- Email campaigns created\n"
            "- Social media content prepared\n"
            "- PR outreach initiated\n"
            "- Demo environment ready\n"
            "- Analytics and tracking verified\n\n"
            "**Launch Week:**\n"
            "- Final testing completed\n"
            "- Launch announcement published\n"
            "- Email campaign sent\n"
            "- Social media posts published\n"
            "- PR distribution\n"
            "- Sales/support teams ready\n"
            "- Monitor metrics and feedback\n\n"
            "**Post-Launch (Weeks 1-4):**\n"
            "- Monitor adoption metrics\n"
            "- Gather customer feedback\n"
            "- Adjust messaging based on response\n"
            "- Continue marketing activities\n"
            "- Create customer success stories\n"
            "- Iterate on campaigns\n\n"
            "**Launch Metrics:**\n"
            "- **Awareness:** Website traffic, social reach, PR coverage, email open rates\n"
            "- **Acquisition:** Sign-ups, trial starts, demo requests, MQLs\n"
            "- **Activation:** Onboarding completion, time to first value, feature adoption\n"
            "- **Revenue:** Free-to-paid conversion, ACV, revenue generated, ROI\n\n"
            "**My Role:**\n"
            "- Coordinate launch timing with Product Owner\n"
            "- Create all marketing materials\n"
            "- Brief stakeholders and teams\n"
            "- Execute launch activities\n"
            "- Monitor and optimize post-launch\n\n"
            "**Key Principle:** Collaborate with Product Owner on launch timing. "
            "Marketing supports the launch, but Product Owner owns the decision."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "scrum_master"]
        )
    
    def _handle_messaging_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about positioning and messaging"""
        recommendations = [
            "Define clear positioning statement (target customer, need, category, benefit, differentiation)",
            "Develop core message and 3-5 supporting key messages",
            "Identify proof points and customer stories",
            "Test messaging with A/B tests",
            "Use customer language in messaging",
            "Align messaging with Product Owner on value articulation",
            "Update messaging based on market feedback"
        ]
        
        questions = [
            "Who is the target customer?",
            "What problem are we solving?",
            "What category do we belong to?",
            "What makes us different/better?",
            "What's our value proposition?",
            "What proof points do we have?",
            "How do customers describe us?"
        ]
        
        response_text = (
            "Positioning and messaging are critical for product success. Here's my approach:\n\n"
            "**Positioning Framework:**\n\n"
            "**Positioning Statement Template:**\n"
            "For [target customer]\n"
            "Who [statement of need/opportunity]\n"
            "Our [product name] is a [product category]\n"
            "That [key benefit/compelling reason to buy]\n"
            "Unlike [primary competitive alternative]\n"
            "Our product [statement of primary differentiation]\n\n"
            "**Messaging Components:**\n"
            "- **Core Message:** One-sentence value proposition\n"
            "- **Key Messages:** 3-5 supporting messages\n"
            "- **Proof Points:** Evidence that supports claims\n"
            "- **Customer Stories:** Real examples and testimonials\n\n"
            "**Value Proposition Canvas:**\n"
            "- **Customer Jobs:** Functional, social, emotional tasks\n"
            "- **Customer Pains:** Frustrations, risks, obstacles\n"
            "- **Customer Gains:** Desired outcomes, delights, ease\n"
            "- **Pain Relievers:** How product eliminates pains\n"
            "- **Gain Creators:** How product creates desired outcomes\n\n"
            "**Message Testing:**\n"
            "- A/B test different value propositions\n"
            "- Test different feature emphases\n"
            "- Test different calls-to-action\n"
            "- Measure conversion impact\n"
            "- Gather customer feedback: 'What convinced you to try our product?'\n"
            "- Use customer language in messaging\n\n"
            "**My Approach:**\n"
            "- Work with Product Owner on positioning\n"
            "- Develop messaging that resonates with target customers\n"
            "- Test and iterate based on market response\n"
            "- Align messaging across all channels\n"
            "- Update messaging based on customer feedback\n\n"
            "**Key Principle:** Messaging should be clear, differentiated, and customer-focused. "
            "Test with real customers and use their language."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "ux_ui_designer"]
        )
    
    def _handle_competitive_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about competitive analysis"""
        recommendations = [
            "Analyze competitors' products, pricing, positioning, and marketing",
            "Identify differentiation opportunities",
            "Understand competitive landscape and market trends",
            "Monitor competitor launches and messaging",
            "Use competitive intelligence to inform positioning",
            "Share competitive insights with Product Owner",
            "Identify gaps and opportunities in the market"
        ]
        
        questions = [
            "Who are our main competitors?",
            "How do they position themselves?",
            "What are their strengths and weaknesses?",
            "What features do they have that we don't?",
            "How do their prices compare?",
            "What channels do they use?",
            "What makes us different/better?"
        ]
        
        response_text = (
            "Competitive intelligence helps inform positioning and strategy. Here's my approach:\n\n"
            "**Competitive Analysis Framework:**\n\n"
            "**For Each Competitor:**\n\n"
            "**Product Comparison:**\n"
            "- Features: What do they have that we don't?\n"
            "- Pricing: How do their prices compare?\n"
            "- Target Market: Who are they focused on?\n"
            "- Strengths: What are they good at?\n"
            "- Weaknesses: Where do they fall short?\n\n"
            "**Positioning:**\n"
            "- How do they describe themselves?\n"
            "- What value prop do they lead with?\n"
            "- What customer problems do they emphasize?\n"
            "- What messaging do they use?\n\n"
            "**Marketing:**\n"
            "- Channels: Where do they advertise/market?\n"
            "- Content: What content do they create?\n"
            "- SEO: What keywords do they rank for?\n"
            "- Social: What's their social presence?\n\n"
            "**Differentiation:**\n"
            "- Why would a customer choose us over them?\n"
            "- What unique value do we provide?\n"
            "- What proof points do we have?\n\n"
            "**My Approach:**\n"
            "- Regularly monitor competitive landscape\n"
            "- Analyze competitor launches and messaging\n"
            "- Share insights with Product Owner and team\n"
            "- Use competitive intelligence to inform positioning\n"
            "- Identify gaps and opportunities\n\n"
            "**Key Principle:** Understand the competition, but focus on customer needs. "
            "Differentiation should be meaningful to customers, not just different."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "business_analyst"]
        )
    
    def _handle_acquisition_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about customer acquisition and growth"""
        recommendations = [
            "Identify and prioritize acquisition channels (SEO, SEM, content, social, partnerships, direct sales, referrals)",
            "Measure CAC (Customer Acquisition Cost) by channel",
            "Focus on channels with best ROI",
            "Optimize landing pages and conversion funnels",
            "Test different acquisition strategies",
            "Track acquisition metrics (sign-ups, trials, MQLs)",
            "Collaborate with Data Analyst on attribution modeling"
        ]
        
        questions = [
            "What are our target customer segments?",
            "Which channels are most effective?",
            "What's our CAC by channel?",
            "What's our conversion funnel?",
            "Where do we lose potential customers?",
            "What channels should we prioritize?",
            "How do we measure acquisition success?"
        ]
        
        response_text = (
            "Customer acquisition is the foundation of growth. Here's my approach:\n\n"
            "**Acquisition Channels:**\n\n"
            "**Organic Channels:**\n"
            "- SEO (Search Engine Optimization)\n"
            "- Content marketing (blog, guides, resources)\n"
            "- Social media (organic posts, community)\n"
            "- Referrals and word-of-mouth\n\n"
            "**Paid Channels:**\n"
            "- SEM (Search Engine Marketing - Google Ads)\n"
            "- Social media advertising (Facebook, LinkedIn, Twitter)\n"
            "- Display advertising\n"
            "- Retargeting campaigns\n\n"
            "**Partnership Channels:**\n"
            "- Partner integrations and marketplaces\n"
            "- Co-marketing with partners\n"
            "- Affiliate programs\n"
            "- Reseller programs\n\n"
            "**Direct Channels:**\n"
            "- Direct sales (for enterprise)\n"
            "- Outbound outreach\n"
            "- Events and conferences\n"
            "- PR and media coverage\n\n"
            "**Channel Strategy:**\n"
            "- Measure CAC (Customer Acquisition Cost) by channel\n"
            "- Focus on channels with best ROI\n"
            "- Test and optimize continuously\n"
            "- Diversify across multiple channels\n"
            "- Scale what works\n\n"
            "**Acquisition Metrics:**\n"
            "- Sign-ups/registrations\n"
            "- Trial starts\n"
            "- Demo requests\n"
            "- Marketing Qualified Leads (MQLs)\n"
            "- Conversion rates by channel\n"
            "- CAC by channel\n\n"
            "**My Approach:**\n"
            "- Identify target customer segments\n"
            "- Test multiple acquisition channels\n"
            "- Measure and optimize CAC\n"
            "- Focus on channels with best ROI\n"
            "- Collaborate with Data Analyst on attribution\n"
            "- Continuously test and iterate\n\n"
            "**Key Principle:** Not all channels are equal. Focus on channels that reach "
            "your target customers efficiently and cost-effectively."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["data_metrics_analyst", "product_owner"]
        )
    
    def _handle_pricing_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about pricing and packaging"""
        recommendations = [
            "Define pricing model (subscription, one-time, freemium, usage-based)",
            "Set price points for each tier",
            "Package features appropriately in each tier",
            "Research competitive pricing",
            "Test pricing with customers",
            "Optimize pricing page for conversion",
            "Align pricing with value proposition"
        ]
        
        questions = [
            "What's our pricing model?",
            "What are our price points?",
            "What features are in each tier?",
            "How does our pricing compare to competitors?",
            "What's the value proposition for each tier?",
            "How do we test pricing?",
            "What's our free-to-paid conversion strategy?"
        ]
        
        response_text = (
            "Pricing and packaging are critical for monetization. Here's my approach:\n\n"
            "**Pricing Models:**\n\n"
            "**Subscription:**\n"
            "- Monthly or annual recurring revenue\n"
            "- Predictable revenue stream\n"
            "- Tiered pricing (Free, Basic, Pro, Enterprise)\n\n"
            "**One-Time:**\n"
            "- Single payment for lifetime access\n"
            "- Lower barrier to entry\n"
            "- May include maintenance fees\n\n"
            "**Freemium:**\n"
            "- Free tier with limited features\n"
            "- Paid tiers for advanced features\n"
            "- Focus on free-to-paid conversion\n\n"
            "**Usage-Based:**\n"
            "- Pay per use or per unit\n"
            "- Scales with customer usage\n"
            "- Common for APIs, storage, compute\n\n"
            "**Pricing Strategy:**\n"
            "- Research competitive pricing\n"
            "- Understand customer willingness to pay\n"
            "- Align pricing with value delivered\n"
            "- Test different price points\n"
            "- Optimize pricing page for conversion\n\n"
            "**Packaging:**\n"
            "- Package features to create value tiers\n"
            "- Make upgrade path clear\n"
            "- Highlight value at each tier\n"
            "- Use anchoring (show highest tier first)\n\n"
            "**My Approach:**\n"
            "- Research competitive pricing\n"
            "- Test pricing with customers\n"
            "- Optimize pricing page\n"
            "- Monitor conversion rates\n"
            "- Iterate based on data\n\n"
            "**Key Principle:** Pricing should reflect value delivered. "
            "Test pricing with real customers and optimize for conversion."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "data_metrics_analyst"]
        )
    
    def _handle_lifecycle_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about customer lifecycle (AARRR framework)"""
        recommendations = [
            "Focus on full customer lifecycle: Acquisition, Activation, Retention, Revenue, Referral",
            "Optimize onboarding for activation (first value experience)",
            "Create engagement campaigns for retention",
            "Develop upsell/cross-sell campaigns for revenue",
            "Build referral programs for advocacy",
            "Measure metrics at each stage",
            "Collaborate with team on lifecycle improvements"
        ]
        
        questions = [
            "What's our activation rate?",
            "What's our retention rate?",
            "What's our free-to-paid conversion?",
            "How do we improve onboarding?",
            "How do we re-engage inactive users?",
            "What's our referral rate?",
            "How do we measure lifecycle success?"
        ]
        
        response_text = (
            "Customer lifecycle marketing drives long-term growth. Here's my AARRR framework approach:\n\n"
            "**AARRR Framework (Pirate Metrics):**\n\n"
            "**Acquisition: Getting Users**\n"
            "- Landing pages and website\n"
            "- SEO and content marketing\n"
            "- Paid advertising (Google, Facebook, LinkedIn)\n"
            "- Partnerships and integrations\n"
            "- PR and media outreach\n"
            "- Referral programs\n\n"
            "**Activation: First Value Experience**\n"
            "- Onboarding emails and tutorials\n"
            "- Product tours and tooltips\n"
            "- Welcome campaigns\n"
            "- 'Aha moment' optimization\n"
            "- Time to value reduction\n\n"
            "**Retention: Keeping Users Engaged**\n"
            "- Engagement emails (feature tips, best practices)\n"
            "- Re-engagement campaigns (for inactive users)\n"
            "- Product announcements and updates\n"
            "- Community building (forums, events)\n"
            "- Customer success programs\n\n"
            "**Revenue: Monetization**\n"
            "- Free-to-paid conversion campaigns\n"
            "- Upsell and cross-sell campaigns\n"
            "- Pricing page optimization\n"
            "- Sales enablement materials\n"
            "- Case studies and ROI calculators\n\n"
            "**Referral: Turning Customers into Advocates**\n"
            "- Referral programs and incentives\n"
            "- Customer testimonials and case studies\n"
            "- Review generation (G2, Capterra, etc.)\n"
            "- Ambassador programs\n"
            "- Social proof and testimonials\n\n"
            "**Email Marketing Campaigns:**\n\n"
            "**Onboarding Series:**\n"
            "- Day 0: Welcome + first steps\n"
            "- Day 2: Feature introduction\n"
            "- Day 7: Tips for success\n"
            "- Day 14: Success story + next steps\n"
            "- Day 30: Upgrade path or retention\n\n"
            "**Engagement:**\n"
            "- Weekly newsletter (product tips, customer stories)\n"
            "- Feature announcements\n"
            "- Milestone celebrations\n"
            "- Educational content\n\n"
            "**Retention:**\n"
            "- Re-engagement for inactive users\n"
            "- Renewal reminders\n"
            "- Customer feedback requests\n"
            "- Product roadmap previews\n\n"
            "**My Approach:**\n"
            "- Measure metrics at each stage\n"
            "- Optimize each stage of the funnel\n"
            "- Create campaigns for each lifecycle stage\n"
            "- Collaborate with team on improvements\n"
            "- Focus on long-term customer value\n\n"
            "**Key Principle:** Focus on the full customer lifecycle, not just acquisition. "
            "Activation, retention, and referral are critical for sustainable growth."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "data_metrics_analyst", "ux_ui_designer"]
        )
    
    def _handle_launch_decision_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about launch decisions (bugs, delays, quality)"""
        recommendations = [
            "Assess bug severity and user impact",
            "Evaluate trade-off between quality and timing",
            "Consider soft launch option for controlled testing",
            "Coordinate with Product Owner on launch decision",
            "Support whatever decision protects users and quality",
            "Adjust marketing plans to support team decision",
            "Communicate clearly to stakeholders if launch is delayed"
        ]
        
        questions = [
            "What type of bugs? (Critical/High/Medium/Low)",
            "Do they block core functionality?",
            "Do they affect all users or edge cases?",
            "What's the user impact if we launch with these bugs?",
            "Can we work around them temporarily?",
            "What's the delay cost vs. quality risk?",
            "Is a soft launch an option?"
        ]
        
        response_text = (
            "Launch decisions should balance quality, timing, and user impact. Here's my approach:\n\n"
            "**Launch Decision Framework:**\n\n"
            "**If Bugs are CRITICAL (data loss, security, blocks core use):**\n"
            "- Delay launch - reputation damage > delay cost\n"
            "- Marketing can handle delay communication\n"
            "- Better to launch right than launch fast\n\n"
            "**If Bugs are HIGH (significant user experience issues):**\n"
            "- Evaluate trade-off:\n"
            "  - Will users encounter this often?\n"
            "  - Can we document workaround?\n"
            "  - Can we fix quickly post-launch?\n"
            "- Consider soft launch (limited users) to identify and fix\n\n"
            "**If Bugs are MEDIUM/LOW (minor issues, edge cases):**\n"
            "- Likely proceed - no product is perfect at launch\n"
            "- Document known issues\n"
            "- Prioritize fixes for next Sprint\n"
            "- Monitor user feedback\n\n"
            "**Launch Options:**\n\n"
            "**Option 1: Delay Launch**\n"
            "- Communicate to stakeholders\n"
            "- Reschedule campaigns\n"
            "- Adjust timeline with partners\n\n"
            "**Option 2: Soft Launch**\n"
            "- Launch to beta users only (controlled group)\n"
            "- Gather feedback, fix critical bugs\n"
            "- Full public launch in 1-2 weeks\n\n"
            "**Option 3: Launch with Known Issues**\n"
            "- Document known issues clearly\n"
            "- Set user expectations\n"
            "- Monitor closely and fix fast\n"
            "- Communicate fixes as improvements\n\n"
            "**Option 4: Partial Launch**\n"
            "- Launch features that work well\n"
            "- Hold back problematic parts\n"
            "- Phase release over 2-3 weeks\n\n"
            "**My Role:**\n"
            "- Provide marketing perspective on launch timing\n"
            "- Support Product Owner's decision\n"
            "- Adjust marketing plans to support team\n"
            "- Communicate clearly to stakeholders\n\n"
            "**Key Principle:** This is a Product Owner decision based on Definition of Done "
            "and Sprint Goal. Marketing can adapt to whatever path protects users and maintains quality."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "scrum_master", "qa_engineer"]
        )
    
    def _handle_marketing_requirement_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle queries about marketing requirements (APIs, integrations, features)"""
        recommendations = [
            "Provide business context and market opportunity",
            "Share customer feedback and competitive intelligence",
            "Estimate revenue/growth impact",
            "Defer to Product Owner on prioritization",
            "Collaborate with Product Owner on evaluation",
            "Identify marketing needs if prioritized",
            "Support Product Owner's prioritization decision"
        ]
        
        questions = [
            "What's the business opportunity?",
            "What's the customer demand?",
            "What's the competitive landscape?",
            "What's the revenue/growth impact?",
            "What marketing needs does this create?",
            "How does this fit with other priorities?",
            "What's the estimated effort?"
        ]
        
        response_text = (
            "Marketing requirements should be evaluated through the Product Owner's prioritization framework. "
            "Here's my approach:\n\n"
            "**Marketing Request Evaluation:**\n\n"
            "**I Provide Context:**\n"
            "- Business opportunity and market size\n"
            "- Customer feedback and demand\n"
            "- Competitive landscape and necessity\n"
            "- Revenue/growth impact estimates\n"
            "- Marketing value and GTM benefits\n\n"
            "**I Defer to Product Owner:**\n"
            "- Product Owner owns prioritization\n"
            "- Marketing requests evaluated like any other opportunity\n"
            "- Use prioritization framework: (User Value + Time Criticality + Risk Reduction) / Effort\n"
            "- Marketing can advocate, but Product Owner decides\n\n"
            "**If Prioritized, Marketing Needs:**\n"
            "- Feature documentation and screenshots\n"
            "- Marketing assets and content\n"
            "- Sales enablement materials\n"
            "- Launch planning and coordination\n"
            "- Analytics and tracking setup\n\n"
            "**My Approach:**\n"
            "- Provide business context and market intelligence\n"
            "- Share customer feedback and competitive insights\n"
            "- Estimate business impact\n"
            "- Collaborate with Product Owner on evaluation\n"
            "- Support Product Owner's decision\n"
            "- Execute marketing if prioritized\n\n"
            "**Key Principle:** Collaborate with Product Owner, don't dictate priorities. "
            "Marketing requests should be evaluated like any other opportunity using the prioritization framework."
        )
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations,
            questions=questions,
            requires_collaboration=True,
            collaborating_roles=["product_owner", "development_engineer"]
        )
    
    def _handle_general_query(self, query: str, **kwargs) -> AgentResponse:
        """Handle general queries with Product Marketing Executive perspective"""
        response_text = (
            f"As a Product Marketing Executive (Key Stakeholder), my role is to translate product capabilities "
            f"into customer value, bring market feedback to the team, and ensure successful launches. "
            f"Let me address your question: '{query}'\n\n"
            f"**My Perspective:**\n"
            f"- Market context: What's happening in the market/competition?\n"
            f"- Customer lens: How do customers perceive this?\n"
            f"- Business impact: What's the revenue/growth opportunity?\n"
            f"- GTM approach: How should we take this to market?\n"
            f"- Collaboration: Work with Product Owner, don't override their decisions\n"
            f"- Marketing needs: What do we need from the team?\n\n"
            f"**Key Principles:**\n"
            f"- **Customer Voice:** Bring real customer feedback to the team\n"
            f"- **Market Awareness:** Understand competition and market trends\n"
            f"- **Collaborate, Don't Dictate:** Work with Product Owner on priorities\n"
            f"- **Business Outcomes:** Connect features to revenue and growth\n"
            f"- **Data-Driven:** Use metrics to inform marketing strategy\n\n"
            f"I'm committed to successful product launches and customer acquisition. I bridge the gap between "
            f"product and market, amplify customer voice, and drive business growth."
        )
        
        recommendations = [
            "Connect to market context and customer needs",
            "Evaluate business impact and revenue opportunity",
            "Collaborate with Product Owner on priorities",
            "Plan go-to-market strategy",
            "Measure marketing success with metrics",
            "Bring customer feedback to the team"
        ]
        
        return self.format_response(
            response_text=response_text,
            recommendations=recommendations
        )
    
    def identify_collaboration_needs(self, query: str) -> List[str]:
        """Identify which roles should be consulted for this query"""
        query_lower = query.lower()
        needs = []
        
        # Product Marketing Executive collaborates with everyone
        if any(word in query_lower for word in ["product", "feature", "roadmap", "priority", "launch"]):
            needs.append("product_owner")
        
        if any(word in query_lower for word in ["technical", "api", "implementation", "development"]):
            needs.append("development_engineer")
        
        if any(word in query_lower for word in ["design", "ui", "ux", "onboarding", "user experience"]):
            needs.append("ux_ui_designer")
        
        if any(word in query_lower for word in ["data", "metrics", "analytics", "attribution", "conversion"]):
            needs.append("data_metrics_analyst")
        
        if any(word in query_lower for word in ["quality", "test", "bug", "qa"]):
            needs.append("qa_engineer")
        
        if any(word in query_lower for word in ["requirement", "business", "customer", "market"]):
            needs.append("business_analyst")
        
        if any(word in query_lower for word in ["process", "sprint", "release", "coordination"]):
            needs.append("scrum_master")
        
        return needs
    
    def get_cross_functional_awareness(self) -> Dict[str, str]:
        """Define what information this agent receives from and provides to other roles"""
        return {
            "receives_from": {
                "product_owner": "Product roadmap, feature priorities, business goals, launch timing",
                "development_engineer": "Technical capabilities, implementation constraints, release timelines, feature documentation",
                "ux_ui_designer": "User research insights, design prototypes, usability findings, onboarding experience",
                "data_metrics_analyst": "Product usage data, conversion metrics, user behavior insights, funnel analysis",
                "qa_engineer": "Product quality status, known issues, testing results, release readiness",
                "business_analyst": "Business requirements, customer workflows, competitive analysis, market sizing",
                "scrum_master": "Team capacity, process improvements, impediments, release planning"
            },
            "provides_to": {
                "product_owner": "Market insights, competitive intelligence, customer feedback, GTM requirements, launch planning",
                "development_engineer": "Marketing requirements (APIs, tracking, integrations), beta testing needs, feature documentation needs",
                "ux_ui_designer": "Marketing website requirements, landing page needs, brand guidelines, onboarding needs",
                "data_metrics_analyst": "Marketing attribution data, campaign performance, funnel metrics, experiment design",
                "qa_engineer": "Beta tester feedback, customer-reported issues, release readiness requirements",
                "business_analyst": "Market requirements, customer needs, competitive positioning, market intelligence",
                "scrum_master": "Organizational marketing needs, coordination requirements, stakeholder communication needs",
                "all_team_members": "Market context, competitive intelligence, customer feedback, launch plans, marketing metrics"
            }
        }
