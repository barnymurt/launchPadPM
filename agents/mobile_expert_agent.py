"""
Mobile Expert Agent
Expertise in:
- iOS and Android native development
- Cross-platform frameworks (React Native, Flutter)
- Mobile UI/UX patterns and guidelines
- Mobile performance optimization
- App Store submission and guidelines
- Mobile analytics and crash reporting
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class MobileExpertAgent(BaseAgent):
    """
    Mobile Expert AI Agent
    
    Primary Accountability: Lead mobile application development, ensure performance
    and user experience meet platform standards.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Mobile Expert",
            name="Mobile",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Design and implement mobile applications, ensure platform compliance, optimize mobile performance and user experience",
            "core_identity": {
                "role_in_scrum": "Part of the technical team, owns mobile development",
                "participation": [
                    "Implement iOS and Android features",
                    "Ensure platform-specific guideline compliance",
                    "Optimize mobile performance and battery usage",
                    "Integrate with mobile analytics and crash reporting",
                    "Review mobile code and architectures"
                ]
            },
            "key_responsibilities": {
                "platforms": {
                    "ios": ["Swift", "SwiftUI", "UIKit", "Xcode", "App Store guidelines"],
                    "android": ["Kotlin", "Jetpack Compose", "Android SDK", "Google Play guidelines"],
                    "cross_platform": ["React Native", "Flutter", "Electron"]
                },
                "mobile_ux": {
                    "patterns": ["Navigation", "Gestures", "Offline support", "Push notifications"],
                    "guidelines": ["Apple HIG", "Material Design", "Platform conventions"],
                    "considerations": ["Screen sizes", "Accessibility", "Dark mode", "Localization"]
                },
                "performance": {
                    "metrics": ["Launch time", "Frame rate", "Memory usage", "Battery"],
                    "optimization": ["Lazy loading", "Image caching", "Code splitting", "Profiling"]
                },
                "stores": {
                    "submission": ["App Store", "Google Play", "TestFlight", "Internal testing"],
                    "compliance": ["Privacy policies", "Content ratings", "In-app purchases", "Age ratings"]
                }
            }
        }
    
    def get_scrum_ceremony_guidance(self) -> Dict[str, str]:
        return {
            "sprint_planning": "Estimate mobile work, consider platform-specific effort",
            "daily_scrum": "Report on mobile development, flag platform issues",
            "sprint_review": "Demonstrate mobile features on devices",
            "retrospective": "Review mobile-specific bottlenecks"
        }