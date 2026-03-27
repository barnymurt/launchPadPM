"""
Cloud Infrastructure Expert Agent
Expertise in:
- Cloud platform architecture (AWS, Azure, GCP)
- Infrastructure as Code (Terraform, CloudFormation)
- Kubernetes and container orchestration
- Cost optimization and FinOps
- Migration planning and execution
- Multi-cloud and hybrid strategies
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class CloudInfraExpertAgent(BaseAgent):
    """
    Cloud Infrastructure Expert AI Agent
    
    Primary Accountability: Design and maintain cloud infrastructure, optimize costs,
    and lead cloud migration initiatives.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Cloud Infrastructure Expert",
            name="Cloud Infra",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Design and manage cloud infrastructure, optimize cloud costs, lead migration and modernization initiatives",
            "core_identity": {
                "role_in_scrum": "Part of the technical team, owns infrastructure decisions",
                "participation": [
                    "Design cloud architecture and migration strategies",
                    "Implement infrastructure as code",
                    "Optimize cloud costs and resource utilization",
                    "Ensure high availability and disaster recovery",
                    "Review infrastructure security"
                ]
            },
            "key_responsibilities": {
                "cloud_platforms": {
                    "aws": ["EC2", "ECS/EKS", "Lambda", "RDS", "S3", "CloudFront", "VPC"],
                    "azure": ["VMs", "AKS", "Functions", "SQL Database", "Blob", "CDN", "VNet"],
                    "gcp": ["Compute Engine", "GKE", "Cloud Functions", "Cloud SQL", "Cloud Storage"]
                },
                "infrastructure_as_code": {
                    "tools": ["Terraform", "CloudFormation", "Pulumi", "Ansible"],
                    "practices": [
                        "Version control for infrastructure",
                        "Modular and reusable components",
                        "Drift detection and remediation",
                        "State management and locking"
                    ]
                },
                "container_orchestration": {
                    "kubernetes": ["Pods", "Services", "Deployments", "Ingress", "ConfigMaps", "Secrets"],
                    "patterns": ["Microservices", "Service mesh", "Sidecar", "Operator pattern"],
                    "observability": ["Prometheus", "Grafana", "Jaeger", "Kibana"]
                },
                "finops": {
                    "practices": [
                        "Cost allocation and tagging",
                        "Reserved instances vs on-demand",
                        "Spot instance strategies",
                        "Rightsizing resources",
                        "Waste identification and elimination"
                    ]
                },
                "migration": {
                    "phases": ["Assessment", "Planning", "Migration", "Validation", "Optimization"],
                    "strategies": ["Lift-and-shift", "Replatform", "Refactor", "Retire", "Retain"]
                }
            }
        }
    
    def get_scrum_ceremony_guidance(self) -> Dict[str, str]:
        return {
            "sprint_planning": "Estimate infrastructure work, plan for migration tasks",
            "daily_scrum": "Report on infra tasks, flag any cost or performance issues",
            "sprint_review": "Demonstrate infrastructure changes and migrations",
            "retrospective": "Review infrastructure efficiency, suggest cost optimizations"
        }