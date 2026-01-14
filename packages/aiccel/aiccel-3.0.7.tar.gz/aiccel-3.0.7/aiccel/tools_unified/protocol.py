# aiccel/tools_unified/protocol.py
"""
Tool Protocols & Data Structures
=================================

Defines the interface that all tools must follow.
Uses Python protocols for structural subtyping (duck typing with type safety).
"""

from typing import Dict, Any, List, Optional, Protocol, runtime_checkable
from dataclasses import dataclass, field
from enum import Enum


class ToolResultStatus(Enum):
    """Status of tool execution."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"


@dataclass
class ToolParameter:
    """Definition of a tool parameter."""
    name: str
    type: str  # "string", "number", "boolean", "array", "object"
    description: str = ""
    required: bool = True
    default: Any = None
    enum: Optional[List[Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "required": self.required,
        }
        if self.default is not None:
            result["default"] = self.default
        if self.enum:
            result["enum"] = self.enum
        return result


@dataclass
class ToolSchema:
    """Schema definition for a tool."""
    name: str
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    returns: str = "string"
    examples: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    p.name: {
                        "type": p.type,
                        "description": p.description,
                        **({"enum": p.enum} if p.enum else {}),
                        **({"default": p.default} if p.default is not None else {})
                    }
                    for p in self.parameters
                },
                "required": [p.name for p in self.parameters if p.required]
            },
            "returns": self.returns,
            "tags": self.tags,
        }
    
    def to_openai_function(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        p.name: {
                            "type": p.type,
                            "description": p.description,
                        }
                        for p in self.parameters
                    },
                    "required": [p.name for p in self.parameters if p.required]
                }
            }
        }


@dataclass
class ToolResult:
    """Result from tool execution."""
    status: ToolResultStatus
    output: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def success(self) -> bool:
        return self.status == ToolResultStatus.SUCCESS
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
        }
    
    @classmethod
    def ok(cls, output: Any, **metadata) -> 'ToolResult':
        """Create successful result."""
        return cls(status=ToolResultStatus.SUCCESS, output=output, metadata=metadata)
    
    @classmethod
    def fail(cls, error: str, **metadata) -> 'ToolResult':
        """Create error result."""
        return cls(status=ToolResultStatus.ERROR, error=error, metadata=metadata)


@runtime_checkable
class ToolProtocol(Protocol):
    """
    Protocol for tools.
    
    Any class with these methods/properties can be used as a tool.
    This enables duck typing with type safety.
    """
    
    @property
    def name(self) -> str:
        """Unique tool name."""
        ...
    
    @property
    def description(self) -> str:
        """Tool description for LLM."""
        ...
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool."""
        ...


@runtime_checkable
class AsyncToolProtocol(Protocol):
    """Protocol for async tools."""
    
    @property
    def name(self) -> str:
        ...
    
    @property
    def description(self) -> str:
        ...
    
    async def execute_async(self, **kwargs) -> Any:
        """Execute the tool asynchronously."""
        ...
