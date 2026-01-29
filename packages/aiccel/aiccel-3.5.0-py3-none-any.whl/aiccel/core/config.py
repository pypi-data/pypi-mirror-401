# aiccel/core/config.py
"""
Agent Configuration
===================

Contains configuration dataclasses and enums for agent behavior.
Extracted from agent.py for better modularity.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class ExecutionMode(Enum):
    """Agent execution modes"""
    NORMAL = "normal"
    THINKING = "thinking"
    STRICT_TOOLS = "strict_tools"
    NO_TOOLS = "no_tools"


# Default limits - centralized here to avoid duplication
class Limits:
    """Default limits for agent configuration"""
    MAX_MEMORY_TURNS = 20
    MAX_MEMORY_TOKENS = 4000
    DEFAULT_TIMEOUT = 30.0
    MAX_PROMPT_LENGTH = 8000
    MAX_TOOL_RETRIES = 3
    CACHE_MAX_SIZE = 100
    CACHE_TTL = 300


@dataclass
class AgentConfig:
    """
    Configuration for agent behavior.
    
    Extracted from agent.py for better separation of concerns.
    """
    name: str = "Agent"
    description: str = "AI Agent"
    instructions: str = "You are a helpful AI assistant. Provide accurate and concise answers."
    memory_type: str = "buffer"
    max_memory_turns: int = Limits.MAX_MEMORY_TURNS
    max_memory_tokens: int = Limits.MAX_MEMORY_TOKENS
    strict_tool_usage: bool = False
    thinking_enabled: bool = False
    verbose: bool = False
    log_file: Optional[str] = None
    timeout: float = Limits.DEFAULT_TIMEOUT
    lightweight: bool = False
    safety_enabled: bool = False
    
    def validate(self) -> None:
        """Validate configuration parameters"""
        if self.max_memory_turns < 1:
            raise ValueError("max_memory_turns must be at least 1")
        if self.max_memory_tokens < 100:
            raise ValueError("max_memory_tokens must be at least 100")
        if self.timeout < 0:
            raise ValueError("timeout must be positive")
        if self.memory_type not in ("buffer", "window", "summary"):
            raise ValueError(f"Invalid memory_type: {self.memory_type}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "memory_type": self.memory_type,
            "max_memory_turns": self.max_memory_turns,
            "max_memory_tokens": self.max_memory_tokens,
            "strict_tool_usage": self.strict_tool_usage,
            "thinking_enabled": self.thinking_enabled,
            "verbose": self.verbose,
            "timeout": self.timeout,
            "lightweight": self.lightweight,
            "safety_enabled": self.safety_enabled,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AgentConfig":
        """Create from dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class ExecutionContext:
    """
    Context for agent execution.
    
    Holds all information needed for a single query execution.
    """
    query: str
    trace_id: int
    has_tools: bool
    relevant_tools: list = field(default_factory=list)
    execution_mode: ExecutionMode = ExecutionMode.NORMAL
    start_time: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)
    
    def get_duration(self) -> float:
        """Get execution duration in seconds"""
        return time.time() - self.start_time
    
    def add_metadata(self, key: str, value) -> "ExecutionContext":
        """Add metadata to context"""
        self.metadata[key] = value
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "query": self.query,
            "trace_id": self.trace_id,
            "has_tools": self.has_tools,
            "relevant_tools": [t.name for t in self.relevant_tools],
            "execution_mode": self.execution_mode.value,
            "duration": self.get_duration(),
            "metadata": self.metadata,
        }
