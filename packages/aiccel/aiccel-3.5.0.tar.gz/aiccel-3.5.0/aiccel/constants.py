# aiccel/constants.py
"""
AICCEL Framework Constants
==========================

Centralized configuration constants following Google's engineering standards.
All magic numbers should be defined here with clear documentation.

This module is the single source of truth for:
- Timeouts
- Limits
- Performance tuning
- Security parameters
"""

from enum import Enum, auto
from typing import Final


# =============================================================================
# FRAMEWORK METADATA
# =============================================================================

FRAMEWORK_NAME: Final[str] = "aiccel"
FRAMEWORK_VERSION: Final[str] = "3.1.4"


# =============================================================================
# SECURITY CONSTANTS
# =============================================================================

class SecurityMode(str, Enum):
    """Security mode for fail-open vs fail-closed behavior."""
    FAIL_OPEN = "fail_open"      # Allow on error (development)
    FAIL_CLOSED = "fail_closed"  # Block on error (production)
    

class JailbreakConfig:
    """Jailbreak detection configuration."""
    DEFAULT_MODEL: Final[str] = "traromal/AIccel_Jailbreak"
    DEFAULT_THRESHOLD: Final[float] = 0.5
    DEFAULT_SECURITY_MODE: Final[SecurityMode] = SecurityMode.FAIL_CLOSED
    UNSAFE_LABELS: Final[tuple] = ("JAILBREAK", "UNSAFE", "LABEL_1", "INJECTION")


# =============================================================================
# PERFORMANCE CONSTANTS
# =============================================================================

class Timeouts:
    """Timeout values in seconds."""
    DEFAULT_REQUEST: Final[float] = 60.0
    DEFAULT_TOOL: Final[float] = 30.0
    DEFAULT_COLLABORATION: Final[float] = 45.0
    DEFAULT_STREAMING: Final[float] = 120.0
    MIN_BACKOFF: Final[float] = 1.0
    MAX_BACKOFF: Final[float] = 60.0


class Retries:
    """Retry configuration."""
    DEFAULT_MAX_ATTEMPTS: Final[int] = 3
    DEFAULT_MULTIPLIER: Final[float] = 1.0
    MIN_WAIT: Final[float] = 1.0
    MAX_WAIT: Final[float] = 10.0


class Concurrency:
    """Concurrency limits."""
    DEFAULT_SEMAPHORE_SIZE: Final[int] = 5
    MAX_PARALLEL_AGENTS: Final[int] = 10
    CONNECTION_POOL_SIZE: Final[int] = 10


# =============================================================================
# MEMORY & CACHE CONSTANTS
# =============================================================================

class Cache:
    """Cache configuration."""
    DEFAULT_TTL: Final[int] = 3600  # 1 hour
    DEFAULT_MAX_SIZE: Final[int] = 1000
    TOOL_CACHE_TTL: Final[int] = 300  # 5 minutes
    TOOL_CACHE_SIZE: Final[int] = 100


class Memory:
    """Memory limits."""
    MAX_HISTORY_SIZE: Final[int] = 1000
    MAX_QUERY_LENGTH: Final[int] = 100_000  # 100KB
    MAX_RESPONSE_LENGTH: Final[int] = 500_000  # 500KB
    COMPRESSION_THRESHOLD: Final[int] = 1024  # Only compress > 1KB


# =============================================================================
# TOKEN ESTIMATION (Provider-aware)
# =============================================================================

class TokenEstimation:
    """Token estimation parameters by provider."""
    # Average characters per token (empirically measured)
    OPENAI_CHARS_PER_TOKEN: Final[float] = 3.5
    GEMINI_CHARS_PER_TOKEN: Final[float] = 4.0
    GROQ_CHARS_PER_TOKEN: Final[float] = 3.5
    DEFAULT_CHARS_PER_TOKEN: Final[float] = 4.0
    
    # Token limits
    DEFAULT_MAX_TOKENS: Final[int] = 4096
    DEFAULT_CONTEXT_WINDOW: Final[int] = 128000


# =============================================================================
# LIMITS (Existing, enhanced)
# =============================================================================

class Limits:
    """Legacy limits class - maintained for backward compatibility."""
    MAX_MEMORY_TURNS: Final[int] = 50
    MAX_MEMORY_TOKENS: Final[int] = 32000
    MAX_PROMPT_LENGTH: Final[int] = 100000
    MAX_COMPRESSED_LENGTH: Final[int] = 50000
    MAX_UNCOMPRESSED_LENGTH: Final[int] = 10000
    COMPRESSION_LEVEL: Final[int] = 6
    MAX_TOOL_OUTPUT_LENGTH: Final[int] = 50000
    MAX_TOOL_RETRIES: Final[int] = 3
    MAX_TOOL_FAILURES: Final[int] = 3


# =============================================================================
# LOGGING CONSTANTS
# =============================================================================

class LogConfig:
    """Logging configuration."""
    MAX_LOG_MESSAGE_LENGTH: Final[int] = 10000
    TRUNCATION_SUFFIX: Final[str] = "...[truncated]"
    SENSITIVE_PATTERNS: Final[tuple] = (
        r"api[_-]?key",
        r"password",
        r"secret",
        r"token",
        r"auth",
        r"credential",
    )


# =============================================================================
# HTTP CONSTANTS
# =============================================================================

class HTTP:
    """HTTP configuration."""
    USER_AGENT: Final[str] = f"{FRAMEWORK_NAME}/{FRAMEWORK_VERSION}"
    CONNECT_TIMEOUT: Final[float] = 10.0
    READ_TIMEOUT: Final[float] = 60.0
    POOL_CONNECTIONS: Final[int] = 10
    POOL_MAXSIZE: Final[int] = 10
    MAX_RETRIES_ADAPTER: Final[int] = 3


# =============================================================================
# ERROR CODES (For structured error handling)
# =============================================================================

class ErrorCode(Enum):
    """Standardized error codes for programmatic handling."""
    # Agent errors (1xxx)
    AGENT_INIT_FAILED = 1001
    AGENT_RUN_FAILED = 1002
    AGENT_TIMEOUT = 1003
    
    # Provider errors (2xxx)
    PROVIDER_AUTH_FAILED = 2001
    PROVIDER_RATE_LIMITED = 2002
    PROVIDER_TIMEOUT = 2003
    PROVIDER_INVALID_RESPONSE = 2004
    
    # Tool errors (3xxx)
    TOOL_NOT_FOUND = 3001
    TOOL_VALIDATION_FAILED = 3002
    TOOL_EXECUTION_FAILED = 3003
    TOOL_TIMEOUT = 3004
    
    # Security errors (4xxx)
    SECURITY_JAILBREAK_DETECTED = 4001
    SECURITY_PII_DETECTED = 4002
    SECURITY_ENCRYPTION_FAILED = 4003
    
    # Memory errors (5xxx)
    MEMORY_FULL = 5001
    MEMORY_COMPRESSION_FAILED = 5002


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Metadata
    "FRAMEWORK_NAME",
    "FRAMEWORK_VERSION",
    
    # Security
    "SecurityMode",
    "JailbreakConfig",
    
    # Performance
    "Timeouts",
    "Retries", 
    "Concurrency",
    
    # Memory & Cache
    "Cache",
    "Memory",
    "TokenEstimation",
    "Limits",
    
    # Logging
    "LogConfig",
    
    # HTTP
    "HTTP",
    
    # Errors
    "ErrorCode",
]