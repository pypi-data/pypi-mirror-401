# aiccel/errors/__init__.py
"""
Unified Error Handling
=======================

Consistent exception hierarchy with proper context and debugging support.
"""

from typing import Optional, Dict, Any, Type
from dataclasses import dataclass, field
from datetime import datetime
import traceback
import sys


# ============================================================================
# BASE EXCEPTION
# ============================================================================

@dataclass
class ErrorContext:
    """Rich context for errors."""
    component: str = ""
    operation: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    trace_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "operation": self.operation,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "trace_id": self.trace_id,
        }


class AiccelError(Exception):
    """
    Base exception for all AICCEL errors.
    
    Features:
    - Rich context
    - Error codes
    - Structured logging support
    - Debug helpers
    """
    
    error_code: str = "AICCEL_ERROR"
    http_status: int = 500
    
    def __init__(
        self,
        message: str,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
        **kwargs
    ):
        self.message = message
        self.context = context or ErrorContext(**kwargs)
        self.cause = cause
        self._traceback = traceback.format_exc() if cause else None
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging/API responses."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "context": self.context.to_dict() if self.context else None,
            "cause": str(self.cause) if self.cause else None,
        }
    
    def with_context(self, **kwargs) -> 'AiccelError':
        """Add context and return self for chaining."""
        for key, value in kwargs.items():
            if hasattr(self.context, key):
                setattr(self.context, key, value)
            else:
                self.context.details[key] = value
        return self
    
    def __str__(self) -> str:
        msg = f"[{self.error_code}] {self.message}"
        if self.context.component:
            msg = f"{self.context.component}: {msg}"
        return msg


# ============================================================================
# PROVIDER ERRORS
# ============================================================================

class ProviderError(AiccelError):
    """Base for LLM provider errors."""
    error_code = "PROVIDER_ERROR"


class APIError(ProviderError):
    """API call failed."""
    error_code = "API_ERROR"
    http_status = 502


class RateLimitError(ProviderError):
    """Rate limit exceeded."""
    error_code = "RATE_LIMIT"
    http_status = 429


class AuthenticationError(ProviderError):
    """Authentication failed."""
    error_code = "AUTH_ERROR"
    http_status = 401


class ModelNotFoundError(ProviderError):
    """Model not found or unavailable."""
    error_code = "MODEL_NOT_FOUND"
    http_status = 404


class ContextLengthError(ProviderError):
    """Context length exceeded."""
    error_code = "CONTEXT_LENGTH"
    http_status = 400


# ============================================================================
# TOOL ERRORS
# ============================================================================

class ToolError(AiccelError):
    """Base for tool errors."""
    error_code = "TOOL_ERROR"


class ToolNotFoundError(ToolError):
    """Tool not found in registry."""
    error_code = "TOOL_NOT_FOUND"
    http_status = 404


class ToolExecutionError(ToolError):
    """Tool execution failed."""
    error_code = "TOOL_EXECUTION"
    http_status = 500


class ToolValidationError(ToolError):
    """Tool input/output validation failed."""
    error_code = "TOOL_VALIDATION"
    http_status = 400


class ToolTimeoutError(ToolError):
    """Tool execution timed out."""
    error_code = "TOOL_TIMEOUT"
    http_status = 504


# ============================================================================
# AGENT ERRORS
# ============================================================================

class AgentError(AiccelError):
    """Base for agent errors."""
    error_code = "AGENT_ERROR"


class ConfigurationError(AgentError):
    """Agent configuration invalid."""
    error_code = "CONFIG_ERROR"
    http_status = 400


class ExecutionError(AgentError):
    """Agent execution failed."""
    error_code = "EXECUTION_ERROR"
    http_status = 500


class ParseError(AgentError):
    """Failed to parse LLM response."""
    error_code = "PARSE_ERROR"
    http_status = 500


class MemoryError(AgentError):
    """Memory operation failed."""
    error_code = "MEMORY_ERROR"
    http_status = 500


# ============================================================================
# SECURITY ERRORS
# ============================================================================

class SecurityError(AiccelError):
    """Base for security errors."""
    error_code = "SECURITY_ERROR"
    http_status = 403


class EncryptionError(SecurityError):
    """Encryption/decryption failed."""
    error_code = "ENCRYPTION_ERROR"


class DecryptionError(SecurityError):
    """Decryption failed."""
    error_code = "DECRYPTION_ERROR"


class ValidationError(SecurityError):
    """Security validation failed."""
    error_code = "VALIDATION_ERROR"
    http_status = 400


class GuardrailError(SecurityError):
    """Guardrail check failed."""
    error_code = "GUARDRAIL_ERROR"


# ============================================================================
# PIPELINE ERRORS
# ============================================================================

class PipelineError(AiccelError):
    """Base for pipeline errors."""
    error_code = "PIPELINE_ERROR"


class MiddlewareError(PipelineError):
    """Middleware execution failed."""
    error_code = "MIDDLEWARE_ERROR"


# ============================================================================
# ERROR HANDLER
# ============================================================================

class ErrorHandler:
    """
    Centralized error handling.
    
    Usage:
        handler = ErrorHandler()
        handler.register(RateLimitError, lambda e: retry_with_backoff())
        
        try:
            result = await agent.run(query)
        except Exception as e:
            handler.handle(e)
    """
    
    def __init__(self):
        self._handlers: Dict[Type[Exception], callable] = {}
        self._default_handler: Optional[callable] = None
    
    def register(
        self,
        error_type: Type[Exception],
        handler: callable
    ) -> 'ErrorHandler':
        """Register handler for error type."""
        self._handlers[error_type] = handler
        return self
    
    def set_default(self, handler: callable) -> 'ErrorHandler':
        """Set default handler for unregistered errors."""
        self._default_handler = handler
        return self
    
    def handle(self, error: Exception) -> Any:
        """Handle an error."""
        for error_type, handler in self._handlers.items():
            if isinstance(error, error_type):
                return handler(error)
        
        if self._default_handler:
            return self._default_handler(error)
        
        raise error
    
    def wrap(self, func: callable) -> callable:
        """Decorator to wrap function with error handling."""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return self.handle(e)
        return wrapper


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def wrap_error(
    error: Exception,
    error_class: Type[AiccelError] = AiccelError,
    **context
) -> AiccelError:
    """Wrap a generic exception in an AiccelError."""
    if isinstance(error, AiccelError):
        return error.with_context(**context)
    
    return error_class(
        message=str(error),
        cause=error,
        **context
    )


def is_retryable(error: Exception) -> bool:
    """Check if error is retryable."""
    retryable_codes = ["RATE_LIMIT", "API_ERROR", "TOOL_TIMEOUT"]
    if isinstance(error, AiccelError):
        return error.error_code in retryable_codes
    return False


# Export all
__all__ = [
    # Base
    'AiccelError',
    'ErrorContext',
    
    # Provider
    'ProviderError',
    'APIError',
    'RateLimitError',
    'AuthenticationError',
    'ModelNotFoundError',
    'ContextLengthError',
    
    # Tool
    'ToolError',
    'ToolNotFoundError',
    'ToolExecutionError',
    'ToolValidationError',
    'ToolTimeoutError',
    
    # Agent
    'AgentError',
    'ConfigurationError',
    'ExecutionError',
    'ParseError',
    'MemoryError',
    
    # Security
    'SecurityError',
    'EncryptionError',
    'DecryptionError',
    'ValidationError',
    'GuardrailError',
    
    # Pipeline
    'PipelineError',
    'MiddlewareError',
    
    # Handler
    'ErrorHandler',
    
    # Utilities
    'wrap_error',
    'is_retryable',
]
