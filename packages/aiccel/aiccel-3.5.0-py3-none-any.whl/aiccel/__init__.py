# aiccel/__init__.py
"""
AICCEL - Fast, Production-Ready AI Agent Framework
===================================================

Version 3.1.2 - Performance & Reliability Update
- Lazy imports for sub-100ms startup
- Environment variable support
- Full type hints
- Comprehensive test coverage

Basic Usage:
    from aiccel import Agent, GeminiProvider
    
    agent = Agent(provider=GeminiProvider())  # Uses GOOGLE_API_KEY env var
    result = agent.run("Hello!")

Fast Import (recommended for production):
    from aiccel.fast import Agent, GeminiProvider
"""

import os as _os
import importlib as _importlib
from typing import TYPE_CHECKING

# Version
__version__ = "3.5.0"

# Lazy loading registry
_LAZY_IMPORTS = {
    # Core
    'Agent': ('aiccel.agent', 'Agent'),
    'SlimAgent': ('aiccel.agent', 'Agent'),
    'create_agent': ('aiccel.agent', 'create_agent'),
    'AgentManager': ('aiccel.manager', 'AgentManager'),
    'ConversationMemory': ('aiccel.conversation_memory', 'ConversationMemory'),
    
    # Providers
    'LLMProvider': ('aiccel.providers', 'LLMProvider'),
    'GeminiProvider': ('aiccel.providers', 'GeminiProvider'),
    'GroqProvider': ('aiccel.providers', 'GroqProvider'),
    
    # Embeddings
    'EmbeddingProvider': ('aiccel.embeddings', 'EmbeddingProvider'),
    'OpenAIEmbeddingProvider': ('aiccel.embeddings', 'OpenAIEmbeddingProvider'),
    'GeminiEmbeddingProvider': ('aiccel.embeddings', 'GeminiEmbeddingProvider'),
    
    # Core Agent
    'Agent': ('aiccel.agent', 'Agent'),
    'SlimAgent': ('aiccel.agent', 'Agent'),
    
    # Unified Tools (from aiccel.tools)
    'Tool': ('aiccel.tools', 'BaseTool'),
    'BaseTool': ('aiccel.tools', 'BaseTool'),
    'SearchTool': ('aiccel.tools', 'SearchTool'),
    'WeatherTool': ('aiccel.tools', 'WeatherTool'),
    'ToolRegistry': ('aiccel.tools', 'ToolRegistry'),
    'ToolResult': ('aiccel.tools', 'ToolResult'),
    'ParameterSchema': ('aiccel.tools', 'ParameterSchema'),
    
    # Providers
    'GeminiProvider': ('aiccel.providers', 'GeminiProvider'),
    'OpenAIProvider': ('aiccel.providers', 'OpenAIProvider'),
    'AnthropicProvider': ('aiccel.providers', 'AnthropicProvider'),
    
    # Privacy
    'EntityMasker': ('aiccel.privacy', 'EntityMasker'),
    'mask_text': ('aiccel.privacy', 'mask_text'),
    'unmask_text': ('aiccel.privacy', 'unmask_text'),
    
    # Logging
    'AILogger': ('aiccel.logger', 'AILogger'),
    'configure_logging': ('aiccel.logging_config', 'configure_logging'),
    'get_logger': ('aiccel.logging_config', 'get_logger'),
    'AgentLogger': ('aiccel.logging_config', 'AgentLogger'),
    
    # Tracing
    'init_tracing': ('aiccel.tracing', 'init_tracing'),
    
    # Workflows
    'Workflow': ('aiccel.workflows', 'Workflow'),
    'WorkflowBuilder': ('aiccel.workflows', 'WorkflowBuilder'),
    'WorkflowExecutor': ('aiccel.workflows', 'WorkflowExecutor'),
    'WorkflowState': ('aiccel.workflows', 'WorkflowState'),
    
    # Autonomous
    'GoalAgent': ('aiccel.autonomous', 'GoalAgent'),
    'Goal': ('aiccel.autonomous', 'Goal'),
    'TaskPlanner': ('aiccel.autonomous', 'TaskPlanner'),
    'SelfReflection': ('aiccel.autonomous', 'SelfReflection'),
    
    # Pipeline
    'MiddlewarePipeline': ('aiccel.pipeline', 'MiddlewarePipeline'),
    'create_default_pipeline': ('aiccel.pipeline', 'create_default_pipeline'),
    
    # DI
    'Container': ('aiccel.di', 'Container'),
    'get_container': ('aiccel.di', 'get_container'),
    
    # MCP
    'MCPClient': ('aiccel.mcp', 'MCPClient'),
    'MCPServer': ('aiccel.mcp', 'MCPServer'),
    'MCPToolAdapter': ('aiccel.mcp', 'MCPToolAdapter'),
    
    # Core
    'AgentConfig': ('aiccel.core', 'AgentConfig'),
    'AgentResponse': ('aiccel.core', 'AgentResponse'),
    'ExecutionContext': ('aiccel.core', 'ExecutionContext'),
    'ExecutionMode': ('aiccel.core', 'ExecutionMode'),
    
    # Reranker
    'NeuralReranker': ('aiccel.rerank', 'NeuralReranker'),
    
    # Request Context (for correlation ID tracking)
    'RequestContext': ('aiccel.request_context', 'RequestContext'),
    'request_scope': ('aiccel.request_context', 'request_scope'),
    'get_request_id': ('aiccel.request_context', 'get_request_id'),
    
    # Constants
    'Timeouts': ('aiccel.constants', 'Timeouts'),
    'Retries': ('aiccel.constants', 'Retries'),
    'SecurityMode': ('aiccel.constants', 'SecurityMode'),
    
    # Exceptions
    'AICCLException': ('aiccel.exceptions', 'AICCLException'),
    'AgentException': ('aiccel.exceptions', 'AgentException'),
    'ProviderException': ('aiccel.exceptions', 'ProviderException'),
    'ToolException': ('aiccel.exceptions', 'ToolException'),
}

# Cache for loaded modules
_LOADED = {}


def __getattr__(name: str):
    """Lazy load modules on first access."""
    # Skip private/special attributes
    if name.startswith('_'):
        raise AttributeError(f"module 'aiccel' has no attribute '{name}'")
    
    # Check cache first
    if name in _LOADED:
        return _LOADED[name]
    
    # Check lazy imports
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        module = _importlib.import_module(module_name)
        obj = getattr(module, attr_name)
        _LOADED[name] = obj
        return obj
    
    # Handle submodule imports
    submodules = {
        'core', 'pipeline', 'di', 'errors', 'mcp', 
        'workflows', 'autonomous', 'integrations',
        'tools', 'tools_v2', 'agent_core'
    }
    if name in submodules:
        module = _importlib.import_module(f'aiccel.{name}')
        _LOADED[name] = module
        return module
    
    raise AttributeError(f"module 'aiccel' has no attribute '{name}'")


def __dir__():
    """List available attributes."""
    return list(_LAZY_IMPORTS.keys()) + ['__version__']


# Only import lightweight stuff at module load
# Everything else is lazy loaded
if TYPE_CHECKING:
    # For IDE support - not executed at runtime
    from .agent import Agent, create_agent
    SlimAgent = Agent
    from .providers import LLMProvider, GeminiProvider, OpenAIProvider, GroqProvider
    from .tools import Tool, SearchTool, WeatherTool, ToolRegistry
    from .manager import AgentManager
    from .conversation_memory import ConversationMemory
    from .privacy import EntityMasker, mask_text, unmask_text
    from .logging_config import configure_logging, get_logger, AgentLogger
    from .workflows import Workflow, WorkflowBuilder, WorkflowExecutor, WorkflowState
    from .autonomous import GoalAgent, Goal, TaskPlanner, SelfReflection
    from .rerank import NeuralReranker


# Encryption is optional - check availability
try:
    from .encryption import ENCRYPTION_AVAILABLE
except ImportError:
    ENCRYPTION_AVAILABLE = False


__all__ = list(_LAZY_IMPORTS.keys()) + [
    '__version__',
    'ENCRYPTION_AVAILABLE',
]