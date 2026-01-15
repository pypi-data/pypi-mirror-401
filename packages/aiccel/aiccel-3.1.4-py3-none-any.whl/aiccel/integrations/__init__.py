# aiccel/integrations/__init__.py
"""
Integrations Module
====================

Easy integrations with popular services and frameworks.
"""

from .langchain import LangChainAdapter
from .openai_functions import OpenAIFunctionsAdapter
from .fastapi_routes import create_agent_routes
from .webhooks import WebhookTrigger

__all__ = [
    'LangChainAdapter',
    'OpenAIFunctionsAdapter',
    'create_agent_routes',
    'WebhookTrigger',
]
