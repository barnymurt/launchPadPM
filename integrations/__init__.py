"""
Integrations module
Handles external service integrations (Notion, etc.)
"""

from .notion_integration import NotionIntegration, NotionClient

__all__ = ['NotionIntegration', 'NotionClient']
