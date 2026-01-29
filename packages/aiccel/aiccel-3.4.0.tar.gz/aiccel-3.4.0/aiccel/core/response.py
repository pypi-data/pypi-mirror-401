# aiccel/core/response.py
"""
Agent Response
==============

Structured response from agent execution.
Extracted from agent.py for better modularity.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple


@dataclass
class AgentResponse:
    """
    Structured response from agent execution.
    
    Contains:
    - response: The main response text
    - thinking: Optional thinking/reasoning process
    - tools_used: List of (tool_name, args) tuples
    - tool_outputs: List of (tool_name, args, output) tuples
    - metadata: Additional response metadata
    - execution_time: Time taken to execute
    """
    response: str
    thinking: Optional[str] = None
    tools_used: List[Tuple[str, Dict[str, Any]]] = field(default_factory=list)
    tool_outputs: List[Tuple[str, Dict[str, Any], str]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "response": self.response,
            "thinking": self.thinking,
            "tools_used": self.tools_used,
            "tool_outputs": self.tool_outputs,
            "metadata": self.metadata,
            "execution_time": self.execution_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentResponse":
        """Create from dictionary"""
        return cls(
            response=data.get("response", ""),
            thinking=data.get("thinking"),
            tools_used=data.get("tools_used", []),
            tool_outputs=data.get("tool_outputs", []),
            metadata=data.get("metadata", {}),
            execution_time=data.get("execution_time", 0.0)
        )
    
    @classmethod
    def error(cls, message: str, execution_time: float = 0.0) -> "AgentResponse":
        """Create error response"""
        return cls(
            response=f"Error: {message}",
            metadata={"error": True, "error_message": message},
            execution_time=execution_time
        )
    
    @property
    def has_tools(self) -> bool:
        """Check if tools were used"""
        return bool(self.tools_used)
    
    @property
    def has_errors(self) -> bool:
        """Check if any tool returned an error"""
        for _, _, output in self.tool_outputs:
            if isinstance(output, str) and output.startswith("Error"):
                return True
        return False
    
    @property
    def tool_names(self) -> List[str]:
        """Get list of tool names used"""
        return [name for name, _ in self.tools_used]
    
    def get_tool_output(self, tool_name: str) -> Optional[str]:
        """Get output for a specific tool"""
        for name, _, output in self.tool_outputs:
            if name == tool_name:
                return output
        return None
    
    def __str__(self) -> str:
        """Human-readable representation"""
        parts = [f"Response: {self.response[:200]}..."]
        if self.tools_used:
            parts.append(f"Tools used: {', '.join(self.tool_names)}")
        if self.thinking:
            parts.append(f"Thinking: {self.thinking[:100]}...")
        parts.append(f"Execution time: {self.execution_time:.2f}s")
        return "\n".join(parts)
