# aiccel/tools/__init__.py
"""
AICCEL Tools System
===================

This is the **unified** tool system for AICCEL v3.2+.

Quick Start:
    from aiccel.tools import BaseTool, ToolResult, ParameterSchema

    class MyTool(BaseTool):
        def __init__(self):
            super().__init__(
                name="my_tool",
                description="Does something useful",
                parameters=[
                    ParameterSchema(name="query", type=ParameterType.STRING, required=True)
                ]
            )
        
        def _execute(self, args):
            return f"Result for {args['query']}"

Available Classes:
    - BaseTool: Base class for creating tools
    - ToolResult: Result of tool execution
    - ToolSchema: Complete tool schema
    - ParameterSchema: Parameter definition
    - ToolRegistry: Register and manage tools

Built-in Tools:
    - SearchTool: Web search via SerpAPI
    - WeatherTool: Weather lookup via OpenWeatherMap
    - CalculatorTool: Mathematical calculations
    - DateTimeTool: Date/time utilities
"""

# =============================================================================
# CORE EXPORTS - Primary Tool System
# =============================================================================

from .base import (
    # Exceptions
    ToolError,
    ToolExecutionError,
    ToolValidationError,
    ToolConfigurationError,
    
    # Data Structures
    ParameterType,
    ParameterSchema,
    ToolSchema,
    ToolResult,
    
    # Validator
    ToolValidator,
    
    # Protocol and Base
    ToolProtocol,
    BaseTool,
)

# Registry
from .registry import ToolRegistry

# Built-in tools
try:
    from .builtin import (
        SearchTool,
        WeatherTool,
        CalculatorTool,
        DateTimeTool,
        DummyTool,
    )
except ImportError:
    # Builtin tools may depend on optional packages
    SearchTool = None
    WeatherTool = None
    CalculatorTool = None
    DateTimeTool = None
    DummyTool = None

# Legacy module for backward compatibility
try:
    from .legacy import (
        LegacyToolWrapper,
        convert_legacy_tool,
    )
except ImportError:
    LegacyToolWrapper = None
    convert_legacy_tool = None


# =============================================================================
# CONVENIENCE CLASSES FROM tools_unified (backwards compat)
# =============================================================================

try:
    from ..tools_unified.base import (
        AsyncTool,
        FunctionTool,
        tool,
    )
    from ..tools_unified.protocol import (
        ToolParameter,
    )
except ImportError:
    # Define simple versions if tools_unified not available
    AsyncTool = None
    FunctionTool = None
    tool = None
    ToolParameter = None


# =============================================================================
# BACKWARDS COMPATIBILITY ALIASES
# =============================================================================

Tool = BaseTool  # Alias for common name


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Exceptions
    "ToolError",
    "ToolExecutionError",
    "ToolValidationError", 
    "ToolConfigurationError",
    
    # Data Structures
    "ParameterType",
    "ParameterSchema",
    "ToolSchema",
    "ToolResult",
    "ToolParameter",
    
    # Validator
    "ToolValidator",
    
    # Base Classes
    "ToolProtocol",
    "BaseTool",
    "AsyncTool",
    "FunctionTool",
    "Tool",  # Alias
    
    # Decorator
    "tool",
    
    # Registry
    "ToolRegistry",
    
    # Built-in Tools
    "SearchTool",
    "WeatherTool",
    "CalculatorTool",
    "DateTimeTool",
    "DummyTool",
    
    # Legacy
    "LegacyToolWrapper",
    "convert_legacy_tool",
]
