# aiccel/tools_unified/base.py
"""
Base Tool Classes
==================

Abstract base classes for creating tools.
Provides common functionality and enforces interface.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from .protocol import ToolSchema, ToolParameter, ToolResult, ToolResultStatus


class BaseTool(ABC):
    """
    Abstract base class for tools.
    
    Subclass this to create custom tools with:
    - Automatic schema generation
    - Validation
    - Error handling
    - Logging
    """
    
    # Override in subclass
    _name: str = ""
    _description: str = ""
    _parameters: List[ToolParameter] = []
    _tags: List[str] = []
    
    def __init__(self):
        self._execution_count = 0
        self._total_time_ms = 0.0
    
    @property
    def name(self) -> str:
        return self._name or self.__class__.__name__
    
    @property
    def description(self) -> str:
        return self._description or self.__doc__ or "No description"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """Get parameters in legacy format."""
        return {
            p.name: {
                "type": p.type,
                "description": p.description,
                "required": p.required
            }
            for p in self._parameters
        }
    
    @property
    def tags(self) -> List[str]:
        return self._tags
    
    def get_schema(self) -> ToolSchema:
        """Get full tool schema."""
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters=self._parameters,
            tags=self._tags
        )
    
    def to_openai_function(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling format."""
        return self.get_schema().to_openai_function()
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        Execute the tool.
        
        Override this in subclass to implement tool logic.
        
        Returns:
            Tool output (any type)
        """
        pass
    
    async def execute_async(self, **kwargs) -> Any:
        """
        Execute the tool asynchronously.
        
        Override for true async implementation.
        Default falls back to sync execution.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.execute(**kwargs))
    
    def run(self, **kwargs) -> ToolResult:
        """
        Execute tool with timing and error handling.
        
        Returns:
            ToolResult with output or error
        """
        start = time.perf_counter()
        
        try:
            output = self.execute(**kwargs)
            duration = (time.perf_counter() - start) * 1000
            
            self._execution_count += 1
            self._total_time_ms += duration
            
            return ToolResult.ok(output, duration_ms=duration)
            
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            return ToolResult.fail(str(e), duration_ms=duration)
    
    async def run_async(self, **kwargs) -> ToolResult:
        """Execute tool asynchronously with timing and error handling."""
        start = time.perf_counter()
        
        try:
            output = await self.execute_async(**kwargs)
            duration = (time.perf_counter() - start) * 1000
            
            return ToolResult.ok(output, duration_ms=duration)
            
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            return ToolResult.fail(str(e), duration_ms=duration)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tool execution statistics."""
        return {
            "name": self.name,
            "execution_count": self._execution_count,
            "total_time_ms": self._total_time_ms,
            "avg_time_ms": (
                self._total_time_ms / self._execution_count 
                if self._execution_count > 0 else 0
            )
        }
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}')>"


class AsyncTool(BaseTool):
    """
    Base class for async-first tools.
    
    Implement execute_async() instead of execute().
    Sync execution will run async in event loop.
    """
    
    def execute(self, **kwargs) -> Any:
        """Sync wrapper for async execution."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.execute_async(**kwargs))
    
    @abstractmethod
    async def execute_async(self, **kwargs) -> Any:
        """Execute the tool asynchronously."""
        pass


class FunctionTool(BaseTool):
    """
    Wrap a plain function as a tool.
    
    Usage:
        def my_func(query: str) -> str:
            return f"Result for {query}"
        
        tool = FunctionTool(
            func=my_func,
            name="my_tool",
            description="Does something"
        )
    """
    
    def __init__(
        self,
        func,
        name: str,
        description: str,
        parameters: Optional[List[ToolParameter]] = None,
        tags: Optional[List[str]] = None
    ):
        super().__init__()
        self._func = func
        self._name = name
        self._description = description
        self._parameters = parameters or []
        self._tags = tags or []
    
    def execute(self, **kwargs) -> Any:
        return self._func(**kwargs)


def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Optional[List[ToolParameter]] = None,
    tags: Optional[List[str]] = None
):
    """
    Decorator to create a tool from a function.
    
    Usage:
        @tool(name="search", description="Search the web")
        def search(query: str) -> str:
            return f"Results for {query}"
    """
    def decorator(func):
        return FunctionTool(
            func=func,
            name=name or func.__name__,
            description=description or func.__doc__ or "No description",
            parameters=parameters,
            tags=tags
        )
    return decorator
