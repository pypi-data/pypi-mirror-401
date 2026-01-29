# aiccel/exceptions.py
"""
Exception hierarchy for the AICCL framework.
Provides clear, actionable error messages with context.
"""

from typing import Optional, Dict, Any


class AICCLException(Exception):
    """Base exception for all AICCL errors"""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}
    
    def __str__(self) -> str:
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} (Context: {context_str})"
        return self.message


class AgentException(AICCLException):
    """Raised when agent operations fail"""
    pass


class ToolException(AICCLException):
    """Base exception for tool-related errors"""
    pass


class ToolExecutionError(ToolException):
    """Raised when tool execution fails"""
    
    def __init__(self, tool_name: str, message: str, original_error: Optional[Exception] = None):
        context = {
            "tool_name": tool_name,
            "original_error": str(original_error) if original_error else None
        }
        super().__init__(message, context)
        self.tool_name = tool_name
        self.original_error = original_error


class ToolValidationError(ToolException):
    """Raised when tool input validation fails"""
    
    def __init__(self, tool_name: str, parameter: str, message: str):
        context = {"tool_name": tool_name, "parameter": parameter}
        super().__init__(message, context)
        self.tool_name = tool_name
        self.parameter = parameter


class ToolNotFoundError(ToolException):
    """Raised when a tool is not found in the registry"""
    
    def __init__(self, tool_name: str, available_tools: list):
        message = f"Tool '{tool_name}' not found"
        context = {"tool_name": tool_name, "available_tools": available_tools}
        super().__init__(message, context)
        self.tool_name = tool_name
        self.available_tools = available_tools


class ProviderException(AICCLException):
    """Base exception for LLM provider errors"""
    pass


class ProviderAuthError(ProviderException):
    """Raised when provider authentication fails"""
    
    def __init__(self, provider: str, message: str = "Authentication failed"):
        context = {"provider": provider}
        super().__init__(message, context)
        self.provider = provider


class ProviderRateLimitError(ProviderException):
    """Raised when provider rate limit is exceeded"""
    
    def __init__(self, provider: str, retry_after: Optional[int] = None):
        message = "Rate limit exceeded"
        context = {"provider": provider, "retry_after": retry_after}
        super().__init__(message, context)
        self.provider = provider
        self.retry_after = retry_after


class ProviderTimeoutError(ProviderException):
    """Raised when provider request times out"""
    
    def __init__(self, provider: str, timeout: float):
        message = f"Request timed out after {timeout}s"
        context = {"provider": provider, "timeout": timeout}
        super().__init__(message, context)
        self.provider = provider
        self.timeout = timeout


class TracingException(AICCLException):
    """Raised when tracing operations fail"""
    pass


class ValidationException(AICCLException):
    """Raised when input validation fails"""
    
    def __init__(self, field: str, message: str, value: Any = None):
        context = {"field": field, "value": value}
        super().__init__(message, context)
        self.field = field
        self.value = value


class MemoryException(AICCLException):
    """Raised when memory operations fail"""
    pass


class MemoryFullError(MemoryException):
    """Raised when memory limit is exceeded"""
    
    def __init__(self, current_size: int, max_size: int):
        message = f"Memory limit exceeded: {current_size}/{max_size}"
        context = {"current_size": current_size, "max_size": max_size}
        super().__init__(message, context)
        self.current_size = current_size
        self.max_size = max_size


class ConfigurationError(AICCLException):
    """Raised when configuration is invalid"""
    
    def __init__(self, parameter: str, message: str, expected: Any = None, actual: Any = None):
        context = {"parameter": parameter, "expected": expected, "actual": actual}
        super().__init__(message, context)
        self.parameter = parameter