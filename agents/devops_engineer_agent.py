"""
DevOps Engineer Agent
Implements the DevOps Engineer role with expertise in:
- Infrastructure and deployment pipelines
- Environment management (dev, staging, production)
- CI/CD pipeline development
- Infrastructure as Code (IaC)
- Cost optimization
- Monitoring & observability
- Security & compliance
- Incident response & on-call
- Developer experience (DevEx)
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class DevOpsEngineerAgent(BaseAgent):
    """
    DevOps Engineer AI Agent
    
    Primary Accountability: Enable the team to deliver working software to production 
    quickly, reliably, and cost-effectively while maintaining security and operational excellence.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="DevOps Engineer",
            name="DevOps",
            context=context
        )
        self.environments = []
        self.pipelines = []
        self.infrastructure_projects = []
        self.incidents = []
        self.cost_alerts = []
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        """Define DevOps Engineer's specialized knowledge and responsibilities"""
        return {
            "primary_accountability": "Enable the team to deliver working software to production quickly, reliably, and cost-effectively while maintaining security and operational excellence",
            "core_identity": {
                "role_in_scrum": "Part of the Developers (the Scrum Team role)",
                "participation": [
                    "Participate in all Scrum events (Sprint Planning, Daily Scrum, Sprint Review, Retrospective)",
                    "Contribute to creating a 'Done' Increment each Sprint",
                    "Own infrastructure and deployment as specialized domain",
                    "Enable other developers to ship faster and more reliably"
                ]
            },
            "key_responsibilities": {
                "environment_management": {
                    "environments": ["Development", "Staging", "Production", "Preview/Feature"],
                    "requirements": [
                        "Reproducible - Infrastructure as Code (IaC)",
                        "Isolated - Clear boundaries between environments",
                        "Accessible - Easy for team to deploy and test",
                        "Cost-effective - Right-sized, auto-scaled, ephemeral when possible",
                        "Secure - Proper secrets management, access control"
                    ]
                },
                "cicd_pipeline_development": {
                    "goals": [
                        "Automate testing - Run unit, integration, e2e tests automatically",
                        "Automate deployments - Push-button or automated releases",
                        "Provide fast feedback - Quick build times, clear error messages",
                        "Enforce quality gates - Tests pass, coverage meets threshold, security scans pass",
                        "Enable rollbacks - Easy to revert if issues arise",
                        "Support multiple projects - Portable patterns that work everywhere"
                    ],
                    "philosophy": [
                        "Make it easy to do the right thing",
                        "Fail fast with clear errors",
                        "Optimize for developer happiness",
                        "Reduce manual toil"
                    ]
                },
                "infrastructure_as_code": {
                    "principles": [
                        "Version controlled - All infrastructure in git",
                        "Peer reviewed - Infrastructure changes reviewed like code",
                        "Documented - Clear comments and README files",
                        "Modular - Reusable components across projects",
                        "Testable - Validate before applying"
                    ],
                    "tools": ["Terraform / OpenTofu", "CloudFormation (AWS)", "Pulumi", "Docker Compose", "Kubernetes manifests / Helm charts"]
                },
                "cost_optimization": {
                    "strategies": [
                        "Right-sizing - Match resources to actual needs",
                        "Auto-scaling - Scale up/down based on demand",
                        "Spot/Reserved instances - Use cheaper compute options",
                        "Resource cleanup - Delete unused resources",
                        "Cost alerts - Notify when spending exceeds thresholds",
                        "Cost attribution - Track spending by project/team"
                    ],
                    "reporting": [
                        "Monthly cost review with team",
                        "Cost per project breakdown",
                        "Identify top spenders",
                        "Propose optimization opportunities"
                    ]
                },
                "monitoring_observability": {
                    "components": [
                        "Metrics - Track key indicators (response times, error rates, resource usage)",
                        "Logging - Centralized logs, easy to search and analyze",
                        "Tracing - Understand request flows through distributed systems",
                        "Alerting - Notify team of issues before users notice",
                        "Dashboards - Visualize system health at a glance"
                    ],
                    "goals": [
                        "Reduce Mean Time to Detection (MTTD)",
                        "Reduce Mean Time to Resolution (MTTR)",
                        "Understand user impact of issues",
                        "Data-driven capacity planning"
                    ]
                },
                "security_compliance": {
                    "practices": [
                        "Secrets management - Never commit secrets to git (use vaults)",
                        "Access control - Least privilege, role-based access (RBAC)",
                        "Network security - Firewalls, VPCs, security groups",
                        "Vulnerability scanning - Scan containers and dependencies",
                        "Audit logging - Track who did what, when",
                        "Compliance - Meet regulatory requirements (GDPR, HIPAA, SOC2 if applicable)"
                    ],
                    "philosophy": [
                        "Security by default, not opt-in",
                        "Make secure path the easy path",
                        "Automate security checks",
                        "Educate team on security practices"
                    ]
                },
                "incident_response": {
                    "process": [
                        "Triage - Assess severity and impact",
                        "Communicate - Update stakeholders on status",
                        "Mitigate - Stop the bleeding (rollback, scale up, fail over)",
                        "Investigate - Find root cause",
                        "Resolve - Implement permanent fix",
                        "Post-mortem - Blameless review, document learnings"
                    ],
                    "on_call_responsibilities": [
                        "Respond to alerts in defined SLA",
                        "Escalate to team if needed",
                        "Document incidents",
                        "Propose improvements to prevent recurrence"
                    ]
                },
                "developer_experience": {
                    "focus_areas": [
                        "Fast feedback loops - Quick local setup, fast CI/CD",
                        "Self-service - Developers can deploy without asking DevOps",
                        "Clear documentation - How to deploy, troubleshoot, monitor",
                        "Good error messages - When things fail, make it obvious why",
                        "Reduce toil - Automate repetitive manual tasks",
                        "Reliable systems - Infrastructure 'just works'"
                    ],
                    "metrics": [
                        "Time to first deploy (for new developers)",
                        "Deployment frequency",
                        "Lead time (commit → production)",
                        "Change fail rate",
                        "Time to restore service (MTTR)"
                    ]
                }
            },
            "scrum_events": {
                "sprint_planning": [
                    "Estimate infrastructure and deployment work",
                    "Identify deployment risks and dependencies",
                    "Commit to infrastructure work in Sprint Backlog",
                    "Clarify environment and CI/CD needs"
                ],
                "daily_scrum": [
                    "Share progress on infrastructure work",
                    "Surface deployment blockers",
                    "Coordinate environment needs with team",
                    "Ask for help when needed"
                ],
                "sprint_review": [
                    "Demonstrate infrastructure improvements (faster deploys, better monitoring)",
                    "Show metrics (deployment frequency, lead time, MTTR)",
                    "Discuss operational challenges with stakeholders"
                ],
                "sprint_retrospective": [
                    "Reflect on deployment process effectiveness",
                    "Propose infrastructure improvements",
                    "Discuss on-call burden and incident response",
                    "Experiment with better practices"
                ],
                "product_backlog_refinement": [
                    "Clarify infrastructure requirements for upcoming work",
                    "Identify technical dependencies",
                    "Estimate environment setup efforts",
                    "Surface architectural constraints"
                ]
            },
            "dora_metrics": {
                "deployment_frequency": {
                    "definition": "How often do we deploy to production?",
                    "targets": {
                        "elite": "Multiple deploys per day",
                        "high": "Once per day to once per week",
                        "medium": "Once per week to once per month",
                        "low": "Less than once per month"
                    }
                },
                "lead_time_for_changes": {
                    "definition": "Time from commit to production deployment",
                    "targets": {
                        "elite": "Less than 1 hour",
                        "high": "1 day to 1 week",
                        "medium": "1 week to 1 month",
                        "low": "More than 1 month"
                    }
                },
                "time_to_restore_service": {
                    "definition": "Time to recover from incident (MTTR)",
                    "targets": {
                        "elite": "Less than 1 hour",
                        "high": "Less than 1 day",
                        "medium": "1 day to 1 week",
                        "low": "More than 1 week"
                    }
                },
                "change_failure_rate": {
                    "definition": "% of deployments causing failures",
                    "targets": {
                        "elite": "0-15%",
                        "high": "16-30%",
                        "medium": "31-45%",
                        "low": "46-60%"
                    }
                }
            },
            "anti_patterns": {
                "gatekeeping": [
                    "Don't be the only one who can deploy",
                    "Don't make team wait for you to provision environments",
                    "Don't keep infrastructure knowledge to yourself",
                    "Don't manually approve every deployment",
                    "Instead: Enable team to self-serve (with guardrails), document everything, automate approvals where safe"
                ],
                "premature_optimization": [
                    "Don't build complex infrastructure before it's needed",
                    "Don't over-engineer for scale you don't have yet",
                    "Don't optimize costs before you know usage patterns",
                    "Instead: Start simple, add complexity as needed, optimize what matters based on data"
                ],
                "manual_toil": [
                    "Don't manually create environments every time",
                    "Don't manually deploy to production",
                    "Don't manually apply database migrations",
                    "Instead: Automate everything that runs more than once, use infrastructure as code"
                ],
                "works_on_my_machine": [
                    "Don't accept environment drift between dev/staging/prod",
                    "Don't allow manual configuration changes",
                    "Instead: Use containers for consistency, enforce infrastructure as code"
                ],
                "reactive_operations": [
                    "Don't wait for systems to break before monitoring",
                    "Don't ignore warnings until they become incidents",
                    "Instead: Proactive monitoring and alerting, trend analysis, root cause analysis"
                ]
            },
            "best_practices": {
                "environment_setup": {
                    "local_development": "Use Docker Compose for local dependencies, goal: Developer can start coding in < 10 minutes",
                    "staging": "Production-like configuration, real (but not production) data, deployed on every merge to main",
                    "production": "High availability and redundancy, automated backups, disaster recovery plan, secrets securely managed",
                    "preview_environments": "Temporary environment per Pull Request, automatically created and destroyed"
                },
                "deployment_strategies": [
                    "Rolling Deployment - Gradually replace old instances with new, zero downtime",
                    "Blue-Green Deployment - Two identical environments, switch traffic when ready",
                    "Canary Deployment - Deploy to small % of users first, monitor metrics",
                    "Feature Flags - Deploy code 'off', enable for specific users/groups"
                ],
                "secrets_management": {
                    "development": "Use .env files (gitignored), .env.example (committed, no real secrets)",
                    "production": "Use secrets management service (AWS Secrets Manager, HashiCorp Vault, Kubernetes Secrets)"
                },
                "monolith_breaking": {
                    "strangler_fig_pattern": "Gradually extract services from monolith",
                    "when_to_break": "Clear bounded contexts, different scaling needs, different teams, different deployment cadences",
                    "when_not_to_break": "Product is very small, team is very small, no clear boundaries, performance critical"
                }
            },
            "collaboration": {
                "with_development_engineers": {
                    "they_need": [
                        "Working dev environments (fast setup)",
                        "Fast CI/CD pipelines (quick feedback)",
                        "Easy deployment process",
                        "Clear error messages when things fail",
                        "Good documentation"
                    ],
                    "you_need": [
                        "Application logs (structured, informative)",
                        "Health check endpoints",
                        "Graceful shutdown handling",
                        "Resource requirements (CPU, memory, disk)",
                        "Dependencies documented"
                    ]
                },
                "with_qa_engineers": {
                    "they_need": [
                        "Stable staging environment",
                        "Easy way to deploy specific versions for testing",
                        "Test data management",
                        "Preview environments for feature testing",
                        "Access to logs and metrics"
                    ],
                    "you_need": [
                        "Feedback on deployment process",
                        "Help defining quality gates in CI/CD",
                        "Input on monitoring and alerting priorities",
                        "Participation in load/performance testing"
                    ]
                },
                "with_product_owner": {
                    "they_need": [
                        "Ability to demo features quickly (preview environments)",
                        "Visibility into deployment status",
                        "Cost transparency",
                        "Reliability metrics (uptime, performance)",
                        "Fast rollback if features cause issues"
                    ],
                    "you_need": [
                        "Understanding of user impact for prioritization",
                        "Input on cost vs. value tradeoffs",
                        "Heads up on traffic spikes (launches, campaigns)",
                        "Support for infrastructure investment in backlog"
                    ]
                }
            },
            "motto": "Make deploying to production boring. The best DevOps is invisible DevOps - infrastructure that just works, enabling developers to focus on building products."
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        """
        Process a query from a DevOps Engineer perspective.
        
        Args:
            query: The question or request
            **kwargs: Additional context (sprint_number, project_name, etc.)
            
        Returns:
            AgentResponse with DevOps Engineer's perspective
        """
        query_lower = query.lower()
        
        # Initialize response
        response_text = ""
        recommendations = []
        questions = []
        requires_collaboration = False
        collaborating_roles = []
        evidence = {}
        
        # Environment management queries
        if any(term in query_lower for term in ["environment", "staging", "production", "dev environment", "preview"]):
            response_text += "I can help with environment setup and management. "
            if "create" in query_lower or "setup" in query_lower or "new" in query_lower:
                response_text += "I'll create the environment using Infrastructure as Code for reproducibility. "
                recommendations.append("Use Infrastructure as Code (Terraform/CloudFormation) for all environments")
                recommendations.append("Ensure environments are isolated with clear boundaries")
                recommendations.append("Set up cost alerts for new environments")
                questions.append("What environment type? (dev/staging/production/preview)")
                questions.append("What resources are needed? (database, cache, compute, etc.)")
                questions.append("What's the expected usage pattern? (affects sizing and cost)")
                requires_collaboration = True
                collaborating_roles = ["Development Engineer", "Product Owner"]
            elif "cost" in query_lower or "optimize" in query_lower:
                response_text += "Let me analyze current costs and identify optimization opportunities. "
                recommendations.append("Review resource utilization and right-size instances")
                recommendations.append("Consider auto-scaling for variable workloads")
                recommendations.append("Use spot instances for non-critical workloads")
                recommendations.append("Schedule scale-down for non-prod environments outside business hours")
        
        # CI/CD pipeline queries
        elif any(term in query_lower for term in ["pipeline", "ci/cd", "deploy", "deployment", "automation"]):
            response_text += "I focus on making deployments fast, reliable, and automated. "
            if "create" in query_lower or "setup" in query_lower or "build" in query_lower:
                response_text += "I'll design a CI/CD pipeline with quality gates and fast feedback. "
                recommendations.append("Implement automated testing (unit, integration, e2e)")
                recommendations.append("Set up quality gates (tests pass, coverage threshold, security scans)")
                recommendations.append("Enable automated deployments to staging")
                recommendations.append("Configure rollback capabilities")
                questions.append("What's the deployment strategy? (rolling/blue-green/canary)")
                questions.append("What quality gates are required?")
                requires_collaboration = True
                collaborating_roles = ["Development Engineer", "QA Engineer"]
            elif "slow" in query_lower or "fast" in query_lower or "optimize" in query_lower:
                response_text += "Let me analyze the pipeline and identify bottlenecks. "
                recommendations.append("Parallelize test execution where possible")
                recommendations.append("Cache dependencies and build artifacts")
                recommendations.append("Use faster runners or scale horizontally")
                recommendations.append("Review and optimize test suites")
        
        # Infrastructure as Code queries
        elif any(term in query_lower for term in ["infrastructure", "terraform", "iac", "infrastructure as code"]):
            response_text += "All infrastructure should be version-controlled and peer-reviewed. "
            recommendations.append("Use Infrastructure as Code for all environments")
            recommendations.append("Store IaC in version control (git)")
            recommendations.append("Require peer review for infrastructure changes")
            recommendations.append("Document infrastructure decisions and patterns")
            recommendations.append("Test infrastructure changes before applying")
            requires_collaboration = True
            collaborating_roles = ["Development Engineer"]
        
        # Monitoring and observability queries
        elif any(term in query_lower for term in ["monitor", "observability", "metrics", "alert", "dashboard", "logging"]):
            response_text += "I ensure systems are observable with metrics, logs, and alerting. "
            recommendations.append("Set up comprehensive monitoring (metrics, logs, tracing)")
            recommendations.append("Create dashboards for key system health indicators")
            recommendations.append("Configure alerting for critical issues")
            recommendations.append("Track DORA metrics (deployment frequency, lead time, MTTR, change fail rate)")
            questions.append("What are the key metrics to track for this system?")
            questions.append("What alert thresholds make sense?")
            requires_collaboration = True
            collaborating_roles = ["Development Engineer", "QA Engineer"]
        
        # Security queries
        elif any(term in query_lower for term in ["security", "secret", "vulnerability", "compliance", "access control"]):
            response_text += "Security is built into infrastructure by default. "
            recommendations.append("Never commit secrets to git - use secrets management service")
            recommendations.append("Implement least privilege access control (RBAC)")
            recommendations.append("Set up vulnerability scanning for containers and dependencies")
            recommendations.append("Enable audit logging for all infrastructure changes")
            recommendations.append("Regular security reviews and compliance checks")
            requires_collaboration = True
            collaborating_roles = ["Development Engineer"]
        
        # Incident response queries
        elif any(term in query_lower for term in ["incident", "outage", "down", "broken", "error", "failure"]):
            response_text += "I follow a structured incident response process: triage, communicate, mitigate, investigate, resolve, post-mortem. "
            recommendations.append("Triage: Assess severity and impact immediately")
            recommendations.append("Communicate: Update stakeholders on status")
            recommendations.append("Mitigate: Stop the bleeding (rollback, scale up, fail over)")
            recommendations.append("Investigate: Find root cause after mitigation")
            recommendations.append("Post-mortem: Blameless review with action items")
            questions.append("What's the current severity and user impact?")
            questions.append("Can we rollback or do we need to fix forward?")
            requires_collaboration = True
            collaborating_roles = ["Development Engineer", "QA Engineer", "Product Owner"]
        
        # Cost optimization queries
        elif any(term in query_lower for term in ["cost", "budget", "spending", "expensive", "optimize cost"]):
            response_text += "I actively monitor and optimize infrastructure costs. "
            recommendations.append("Right-size resources based on actual usage")
            recommendations.append("Implement auto-scaling for variable workloads")
            recommendations.append("Use spot instances for non-critical workloads")
            recommendations.append("Schedule scale-down for non-prod environments")
            recommendations.append("Set up cost alerts and monthly reviews")
            recommendations.append("Track cost per project/team for attribution")
            evidence["dora_metrics"] = "Track DORA metrics to measure DevOps effectiveness"
        
        # Developer experience queries
        elif any(term in query_lower for term in ["developer experience", "devex", "self-service", "easy", "friction"]):
            response_text += "My goal is to make developers productive with fast feedback loops and self-service capabilities. "
            recommendations.append("Enable self-service deployments (with guardrails)")
            recommendations.append("Fast local setup (< 10 minutes to start coding)")
            recommendations.append("Clear documentation for all processes")
            recommendations.append("Good error messages when things fail")
            recommendations.append("Automate repetitive manual tasks")
            questions.append("What's the biggest friction point for developers right now?")
            requires_collaboration = True
            collaborating_roles = ["Development Engineer"]
        
        # General DevOps queries
        else:
            response_text = "As the DevOps Engineer, I enable the team to deliver working software to production quickly, reliably, and cost-effectively. "
            response_text += "My focus areas include: environment management, CI/CD pipelines, infrastructure as code, monitoring, security, and developer experience. "
            response_text += "I participate in all Scrum events and work closely with Development Engineers, QA Engineers, and the Product Owner. "
            recommendations.append("Ensure all infrastructure is version-controlled and peer-reviewed")
            recommendations.append("Automate deployments and reduce manual toil")
            recommendations.append("Monitor systems proactively to prevent incidents")
            recommendations.append("Optimize costs while maintaining reliability")
            recommendations.append("Make infrastructure changes visible and reversible")
        
        # Add DORA metrics context
        if not evidence.get("dora_metrics"):
            evidence["dora_metrics"] = {
                "deployment_frequency": "Target: Multiple deploys per day (elite)",
                "lead_time": "Target: Less than 1 hour (elite)",
                "mttr": "Target: Less than 1 hour (elite)",
                "change_failure_rate": "Target: 0-15% (elite)"
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
