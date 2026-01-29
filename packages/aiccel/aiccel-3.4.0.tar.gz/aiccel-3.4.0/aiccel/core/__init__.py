# aiccel/core/__init__.py
"""
AIccel Core Module
==================

Core abstractions, protocols, and data structures.
Following SOLID principles with clean interfaces.
"""

from .config import AgentConfig, ExecutionMode, ExecutionContext
from .response import AgentResponse
from .plugin import AgentPlugin, PluginManager, PluginHook
from .interfaces import AgentInterface

# New protocols - industry-standard abstractions
from .protocols import (
    LLMProtocol,
    ToolProtocol,
    MemoryProtocol,
    Middleware,
    Context,
    PluginProtocol,
    BaseLLMProvider,
    BaseTool,
    BaseMemory,
    Message,
    ToolCall,
    ToolResult,
    ToolResultStatus,
)

__all__ = [
    # Config
    "AgentConfig",
    "ExecutionMode", 
    "ExecutionContext",
    "AgentResponse",
    
    # Plugins
    "AgentPlugin",
    "PluginManager",
    "PluginHook",
    "AgentInterface",
    
    # Protocols (new)
    "LLMProtocol",
    "ToolProtocol",
    "MemoryProtocol",
    "Middleware",
    "Context",
    "PluginProtocol",
    
    # Base classes (new)
    "BaseLLMProvider",
    "BaseTool",
    "BaseMemory",
    
    # Data structures (new)
    "Message",
    "ToolCall",
    "ToolResult",
    "ToolResultStatus",
]
