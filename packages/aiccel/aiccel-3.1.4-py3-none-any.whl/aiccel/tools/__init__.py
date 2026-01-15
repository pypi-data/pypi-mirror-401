# aiccel/tools/__init__.py
"""
AIccel Tools - Unified Tool System
====================================

This module provides a complete tool system for AI agents with:
- BaseTool: Abstract base class for creating custom tools
- ToolRegistry: Central registry for managing tools
- SearchTool: Web search tool with multiple providers
- WeatherTool: Weather data tool
- Schema-based validation
- Plugin architecture

Usage:
    from aiccel.tools import (
        BaseTool,
        ToolRegistry,
        SearchTool,
        WeatherTool,
        ParameterSchema,
        ToolResult
    )
    
    # Create agents with tools
    from aiccel import Agent, GeminiProvider
    
    agent = Agent(
        provider=GeminiProvider(),
        tools=[SearchTool(api_key="..."), WeatherTool(api_key="...")]
    )
    
    # Create custom tools
    class MyTool(BaseTool):
        @property
        def name(self) -> str:
            return "my_tool"
        
        @property
        def description(self) -> str:
            return "My custom tool"
        
        def _execute(self, **kwargs) -> str:
            return "Result"

Example:
    >>> from aiccel.tools import SearchTool, ToolRegistry
    >>> 
    >>> search = SearchTool(api_key="your-serper-key")
    >>> registry = ToolRegistry()
    >>> registry.register(search)
    >>> 
    >>> # Find relevant tools for a query
    >>> tools = registry.find_relevant_tools("What is the weather?")
"""

# Import from local modules
from .base import (
    ToolProtocol,
    BaseTool,
    ToolSchema,
    ParameterSchema,
    ParameterType,
    ToolResult,
    ToolValidator,
    ToolError,
    ToolExecutionError,
    ToolValidationError,
    ToolConfigurationError,
)

from .registry import ToolRegistry

from .builtin.search import SearchTool, SearchProvider
from .builtin.weather import WeatherTool, WeatherProvider

# Legacy imports for backward compatibility - imported from the old tools.py module
# These are re-exported for users who may have imported them directly
try:
    from .legacy import (
        Tool,
        ToolResult as LegacyToolResult,
    )
except ImportError:
    # Legacy module not available
    Tool = BaseTool  # Alias


__all__ = [
    # Core classes
    "BaseTool",
    "Tool",  # Alias for BaseTool (backward compatibility)
    "ToolProtocol",
    "ToolRegistry",
    
    # Schema & Validation
    "ToolSchema",
    "ParameterSchema",
    "ParameterType",
    "ToolResult",
    "ToolValidator",
    
    # Exceptions
    "ToolError",
    "ToolExecutionError", 
    "ToolValidationError",
    "ToolConfigurationError",
    
    # Builtin tools
    "SearchTool",
    "SearchProvider",
    "WeatherTool",
    "WeatherProvider",
]
