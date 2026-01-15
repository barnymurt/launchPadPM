"""
Integrations module
Handles external service integrations (Notion, Slack, Telegram, etc.)
"""

from .notion_integration import NotionIntegration, NotionClient

try:
    from .slack_integration import SlackIntegration, SlackClient
    __all__ = ['NotionIntegration', 'NotionClient', 'SlackIntegration', 'SlackClient']
except ImportError:
    __all__ = ['NotionIntegration', 'NotionClient']

try:
    from .telegram_integration import TelegramIntegration, TelegramClient
    if 'SlackIntegration' in __all__:
        __all__.extend(['TelegramIntegration', 'TelegramClient'])
    else:
        __all__ = ['NotionIntegration', 'NotionClient', 'TelegramIntegration', 'TelegramClient']
except ImportError:
    pass
