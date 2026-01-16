# aiccel/tools_unified/__init__.py
"""
Unified Tools Module
=====================

Merges tools.py and tools_v2 into a single, clean tool system.
Provides backward compatibility while offering modern features.

Features:
- Protocol-based tool interface
- Built-in tools (search, weather)
- Tool registry with smart selection
- Validation and schema support
"""

from .protocol import ToolProtocol, ToolSchema, ToolResult, ToolParameter
from .base import BaseTool, AsyncTool
from .registry import ToolRegistry
from .validators import ToolValidator, validate_args
from .builtin import SearchTool, WeatherTool

__all__ = [
    # Protocols
    'ToolProtocol',
    'ToolSchema',
    'ToolResult',
    'ToolParameter',
    
    # Base classes
    'BaseTool',
    'AsyncTool',
    
    # Registry
    'ToolRegistry',
    
    # Validation
    'ToolValidator',
    'validate_args',
    
    # Built-in tools
    'SearchTool',
    'WeatherTool',
]
