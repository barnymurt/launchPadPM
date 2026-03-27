"""
API Expert Agent
Expertise in:
- API design (REST, GraphQL, gRPC, WebSocket)
- Mobile backend architecture
- Serverless computing
- Integration patterns and webhooks
- API versioning and documentation
- Edge computing
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class APIExpertAgent(BaseAgent):
    """
    API Expert AI Agent
    
    Primary Accountability: Design and implement robust APIs, ensure mobile backend scalability,
    and create seamless integration experiences.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="API Expert",
            name="API Expert",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Design scalable APIs and mobile backends, implement serverless functions, ensure seamless third-party integrations",
            "core_identity": {
                "role_in_scrum": "Part of the technical team, owns API architecture",
                "participation": [
                    "Design API contracts and specifications",
                    "Implement API endpoints and middleware",
                    "Review integration implementations",
                    "Define webhook and event-driven patterns",
                    "Optimize API performance and response times"
                ]
            },
            "key_responsibilities": {
                "api_design": {
                    "styles": ["REST", "GraphQL", "gRPC", "WebSocket", "Webhook"],
                    "principles": [
                        "Consumer-first design",
                        "Consistent naming and structure",
                        "Proper error handling and status codes",
                        "Versioning strategy",
                        "Pagination and filtering"
                    ],
                    "artifacts": ["OpenAPI/Swagger specs", "API contracts", "Integration guides"]
                },
                "mobile_backend": {
                    "considerations": [
                        "Offline-first architecture",
                        "Push notification infrastructure",
                        "Background sync",
                        "Rate limiting per device/user",
                        "Battery-efficient polling strategies"
                    ]
                },
                "serverless": {
                    "providers": ["AWS Lambda", "Azure Functions", "Google Cloud Functions"],
                    "patterns": ["FaaS", "Edge functions", "Microservices"],
                    "considerations": ["Cold starts", "Statelessness", "Timeout management"]
                },
                "integrations": {
                    "patterns": ["Webhook", "Polling", "Streaming", "OAuth flows"],
                    "best_practices": [
                        "Idempotent operations",
                        "Retry with exponential backoff",
                        "Event ordering guarantees",
                        "Payload size optimization"
                    ]
                }
            }
        }
    
    def get_scrum_ceremony_guidance(self) -> Dict[str, str]:
        return {
            "sprint_planning": "Estimate API work, identify integration dependencies",
            "daily_scrum": "Report on API development, flag integration blockers",
            "sprint_review": "Demonstrate new API endpoints and integrations",
            "retrospective": "Review API-related pain points, suggest improvements"
        }