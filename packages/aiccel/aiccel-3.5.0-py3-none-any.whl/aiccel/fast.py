# aiccel/fast.py
"""
Fast Import Module
===================

Lazy loading for fast startup. Use this instead of main package
when startup time is critical.

Usage:
    from aiccel.fast import Agent, GeminiProvider
    
    # Components loaded on first use, not on import
"""

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .agent import Agent
    from .agent_slim import SlimAgent
    from .providers import GeminiProvider, OpenAIProvider, GroqProvider, LLMProvider
    from .tools import Tool, SearchTool, WeatherTool, ToolRegistry
    from .manager import AgentManager

__all__ = [
    'Agent', 'SlimAgent',
    'GeminiProvider', 'OpenAIProvider', 'GroqProvider', 'LLMProvider',
    'Tool', 'SearchTool', 'WeatherTool', 'ToolRegistry',
    'AgentManager',
    'Workflow', 'WorkflowBuilder',
    'GoalAgent', 'TaskPlanner',
    'configure_logging', 'get_logger',
]


class _LazyLoader:
    """Lazy module/class loader."""
    
    _cache = {}
    
    _mappings = {
        # Core
        'Agent': ('aiccel.agent', 'Agent'),
        'SlimAgent': ('aiccel.agent_slim', 'SlimAgent'),
        'create_agent': ('aiccel.agent_slim', 'create_agent'),
        
        # Providers
        'GeminiProvider': ('aiccel.providers', 'GeminiProvider'),
        'OpenAIProvider': ('aiccel.providers', 'OpenAIProvider'),
        'GroqProvider': ('aiccel.providers', 'GroqProvider'),
        'LLMProvider': ('aiccel.providers', 'LLMProvider'),
        
        # Tools (Unified)
        'Tool': ('aiccel.tools', 'BaseTool'),
        'BaseTool': ('aiccel.tools', 'BaseTool'),
        'SearchTool': ('aiccel.tools', 'SearchTool'),
        'WeatherTool': ('aiccel.tools', 'WeatherTool'),
        'ToolRegistry': ('aiccel.tools', 'ToolRegistry'),
        
        # Manager
        'AgentManager': ('aiccel.manager', 'AgentManager'),
        
        # Memory
        'ConversationMemory': ('aiccel.conversation_memory', 'ConversationMemory'),
        
        # Workflows
        'Workflow': ('aiccel.workflows.graph', 'Workflow'),
        'WorkflowBuilder': ('aiccel.workflows.builder', 'WorkflowBuilder'),
        'WorkflowExecutor': ('aiccel.workflows.executor', 'WorkflowExecutor'),
        
        # Autonomous
        'GoalAgent': ('aiccel.autonomous.goal_agent', 'GoalAgent'),
        'Goal': ('aiccel.autonomous.goal_agent', 'Goal'),
        'TaskPlanner': ('aiccel.autonomous.planner', 'TaskPlanner'),
        
        # Logging
        'configure_logging': ('aiccel.logging_config', 'configure_logging'),
        'get_logger': ('aiccel.logging_config', 'get_logger'),
        'AgentLogger': ('aiccel.logging_config', 'AgentLogger'),
        
        # Privacy
        'EntityMasker': ('aiccel.privacy', 'EntityMasker'),
        'mask_text': ('aiccel.privacy', 'mask_text'),
        
        # Pipeline
        'MiddlewarePipeline': ('aiccel.pipeline.middleware', 'MiddlewarePipeline'),
        'create_default_pipeline': ('aiccel.pipeline.middleware', 'create_default_pipeline'),
        
        # DI
        'Container': ('aiccel.di.container', 'Container'),
        'get_container': ('aiccel.di.container', 'get_container'),
    }
    
    @classmethod
    def get(cls, name: str):
        """Get a lazily-loaded class/function."""
        if name in cls._cache:
            return cls._cache[name]
        
        if name not in cls._mappings:
            raise ImportError(f"Cannot lazily import '{name}'")
        
        module_name, attr_name = cls._mappings[name]
        module = importlib.import_module(module_name)
        obj = getattr(module, attr_name)
        
        cls._cache[name] = obj
        return obj


def __getattr__(name: str):
    """Module-level lazy loading."""
    # Skip special attributes
    if name.startswith('_'):
        raise AttributeError(f"module 'aiccel.fast' has no attribute '{name}'")
    return _LazyLoader.get(name)


# Immediately available (lightweight)
from .logging_config import configure_logging, get_logger

__version__ = "3.1.4"
