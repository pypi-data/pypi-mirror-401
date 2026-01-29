"""
AIccel Jailbreak Detection Module
==================================

Production-grade jailbreak detection with configurable security modes.

Security Modes:
- FAIL_CLOSED: Block on any error (production default - security first)
- FAIL_OPEN: Allow on error (development/testing only)

This module is designed following Google's security-first principles.
"""

from typing import Dict, Any, Optional, Callable
import time
import functools
import os
from enum import Enum

from .constants import SecurityMode, JailbreakConfig
from .exceptions import AICCLException

# Optional dependency
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from .logging_config import get_logger

logger = get_logger("jailbreak")


class JailbreakDetectedError(AICCLException):
    """Raised when a jailbreak attempt is detected."""
    
    def __init__(self, prompt_preview: str, confidence: float):
        message = "Jailbreak attempt detected"
        context = {
            "prompt_preview": prompt_preview[:50] + "..." if len(prompt_preview) > 50 else prompt_preview,
            "confidence": confidence
        }
        super().__init__(message, context)
        self.confidence = confidence


class JailbreakModelError(AICCLException):
    """Raised when the jailbreak model fails to load or execute."""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        context = {"original_error": str(original_error) if original_error else None}
        super().__init__(message, context)
        self.original_error = original_error


class JailbreakGuard:
    """
    Production-grade jailbreak detection guard.
    
    Features:
    - Configurable security mode (fail-open vs fail-closed)
    - Lazy model loading
    - Thread-safe singleton pattern
    - Proper exception hierarchy
    - Comprehensive logging
    
    Security Note:
        Default mode is FAIL_CLOSED for production safety.
        Only use FAIL_OPEN in development/testing environments.
    
    Example:
        # Production (fail-closed)
        guard = JailbreakGuard(security_mode=SecurityMode.FAIL_CLOSED)
        
        # Development (fail-open)
        guard = JailbreakGuard(security_mode=SecurityMode.FAIL_OPEN)
    """
    
    def __init__(
        self,
        model_name: str = None,
        threshold: float = None,
        security_mode: SecurityMode = None
    ):
        """
        Initialize the jailbreak guard.
        
        Args:
            model_name: HuggingFace model ID (default: from JailbreakConfig)
            threshold: Confidence threshold to block (default: 0.5)
            security_mode: FAIL_OPEN or FAIL_CLOSED (default: FAIL_CLOSED)
        """
        # Use config defaults
        self.model_name = model_name or JailbreakConfig.DEFAULT_MODEL
        self.threshold = threshold if threshold is not None else JailbreakConfig.DEFAULT_THRESHOLD
        
        # Security mode from env or parameter (env takes precedence for deployment)
        env_mode = os.environ.get("AICCEL_SECURITY_MODE", "").upper()
        if env_mode == "FAIL_OPEN":
            self.security_mode = SecurityMode.FAIL_OPEN
        elif env_mode == "FAIL_CLOSED":
            self.security_mode = SecurityMode.FAIL_CLOSED
        else:
            self.security_mode = security_mode or JailbreakConfig.DEFAULT_SECURITY_MODE
        
        self.classifier = None
        self._model_load_attempted = False
        self._model_load_error: Optional[Exception] = None
        
        # Log security mode - IMPORTANT for audit
        logger.info(
            f"JailbreakGuard initialized: model={self.model_name}, "
            f"threshold={self.threshold}, security_mode={self.security_mode.value}"
        )
        
        if not TRANSFORMERS_AVAILABLE:
            logger.warning(
                "Transformers library not installed. "
                f"Mode={self.security_mode.value} will apply on model unavailability."
            )

    def _load_model(self) -> bool:
        """
        Lazy load the model.
        
        Returns:
            True if model loaded successfully, False otherwise.
        """
        if self._model_load_attempted:
            return self.classifier is not None
        
        self._model_load_attempted = True
        
        if not TRANSFORMERS_AVAILABLE:
            self._model_load_error = ImportError("transformers library not installed")
            logger.error("Cannot load jailbreak model: transformers not installed")
            return False
        
        try:
            logger.info(f"Loading Jailbreak classifier: {self.model_name}")
            start = time.perf_counter()
            self.classifier = pipeline("text-classification", model=self.model_name)
            duration = time.perf_counter() - start
            logger.info(f"Jailbreak classifier loaded successfully in {duration:.2f}s")
            return True
        except Exception as e:
            self._model_load_error = e
            logger.error(f"Failed to load Jailbreak model: {e}")
            return False

    def _handle_model_unavailable(self) -> bool:
        """
        Handle case when model is unavailable based on security mode.
        
        Returns:
            True (safe) for FAIL_OPEN, raises exception for FAIL_CLOSED.
        
        Raises:
            JailbreakModelError: In FAIL_CLOSED mode when model unavailable.
        """
        if self.security_mode == SecurityMode.FAIL_OPEN:
            logger.warning(
                "Jailbreak model unavailable, FAIL_OPEN mode: allowing prompt. "
                "WARNING: This is insecure for production!"
            )
            return True
        else:
            # FAIL_CLOSED: Security first
            error_msg = (
                "Jailbreak detection model unavailable and security_mode=FAIL_CLOSED. "
                "Blocking request for security."
            )
            logger.error(error_msg)
            raise JailbreakModelError(error_msg, self._model_load_error)

    def _handle_check_error(self, error: Exception, prompt: str) -> bool:
        """
        Handle errors during check based on security mode.
        
        Args:
            error: The exception that occurred
            prompt: The prompt being checked (for logging)
        
        Returns:
            True (safe) for FAIL_OPEN.
        
        Raises:
            JailbreakModelError: In FAIL_CLOSED mode.
        """
        prompt_preview = prompt[:50] + "..." if len(prompt) > 50 else prompt
        
        if self.security_mode == SecurityMode.FAIL_OPEN:
            logger.warning(
                f"Jailbreak check failed with error, FAIL_OPEN mode: allowing. "
                f"Error: {error}, Prompt: {prompt_preview}"
            )
            return True
        else:
            error_msg = f"Jailbreak check failed: {error}"
            logger.error(f"{error_msg}, Prompt: {prompt_preview}")
            raise JailbreakModelError(error_msg, error)

    def check(self, prompt: str) -> bool:
        """
        Check if a prompt is safe.
        
        Args:
            prompt: The prompt to check
        
        Returns:
            True if prompt is safe, False if jailbreak detected.
        
        Raises:
            JailbreakModelError: If model unavailable and mode is FAIL_CLOSED.
            JailbreakDetectedError: If jailbreak detected (optional, use is_safe for bool).
        """
        if not prompt or not prompt.strip():
            return True  # Empty prompts are safe
        
        # Ensure model is loaded
        if self.classifier is None:
            if not self._load_model():
                return self._handle_model_unavailable()
        
        try:
            # Run classification
            result = self.classifier(prompt[:512])  # Truncate for model safety
            
            label = result[0]['label']
            score = result[0]['score']
            
            logger.debug(f"Jailbreak check: label={label}, score={score:.4f}")
            
            # Check against unsafe labels
            is_unsafe = (
                label.upper() in JailbreakConfig.UNSAFE_LABELS 
                and score > self.threshold
            )
            
            if is_unsafe:
                prompt_preview = prompt[:50] + "..." if len(prompt) > 50 else prompt
                logger.warning(
                    f"Jailbreak attempt blocked! "
                    f"Label={label}, Score={score:.4f}, Prompt: {prompt_preview}"
                )
                return False
            
            return True
            
        except Exception as e:
            return self._handle_check_error(e, prompt)

    def check_or_raise(self, prompt: str) -> None:
        """
        Check prompt and raise exception if jailbreak detected.
        
        Use this for strict enforcement where you want exception-based flow.
        
        Raises:
            JailbreakDetectedError: If jailbreak detected.
            JailbreakModelError: If model fails in FAIL_CLOSED mode.
        """
        if not self.check(prompt):
            # Get more info for the exception
            if self.classifier:
                result = self.classifier(prompt[:512])
                confidence = result[0]['score']
            else:
                confidence = 0.0
            raise JailbreakDetectedError(prompt, confidence)

    def guard(self, func: Callable) -> Callable:
        """
        Decorator to guard a function with jailbreak detection.
        
        Usage:
            guard = JailbreakGuard()
            
            @guard.guard
            def process_prompt(query: str):
                ...
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract prompt from various positions
            prompt = kwargs.get('query') or kwargs.get('prompt')
            
            if not prompt and args:
                # Check if method (first arg is self)
                if hasattr(args[0], 'run'):
                    prompt = args[1] if len(args) > 1 else None
                else:
                    prompt = args[0] if isinstance(args[0], str) else None
            
            if prompt and isinstance(prompt, str):
                self.check_or_raise(prompt)
            
            return func(*args, **kwargs)
        return wrapper

    @property
    def is_available(self) -> bool:
        """Check if the guard's model is available."""
        if not self._model_load_attempted:
            self._load_model()
        return self.classifier is not None


# =============================================================================
# SINGLETON MANAGEMENT
# =============================================================================

_global_guard: Optional[JailbreakGuard] = None
_guard_lock = __import__('threading').Lock()


def get_guard(
    security_mode: Optional[SecurityMode] = None,
    reinitialize: bool = False
) -> JailbreakGuard:
    """
    Get or create the global JailbreakGuard singleton.
    
    Args:
        security_mode: Security mode override
        reinitialize: Force reinitialization
    
    Returns:
        JailbreakGuard instance
    """
    global _global_guard
    
    with _guard_lock:
        if _global_guard is None or reinitialize:
            _global_guard = JailbreakGuard(security_mode=security_mode)
        return _global_guard


def check_prompt(prompt: str, security_mode: Optional[SecurityMode] = None) -> bool:
    """
    Convenience function to check a prompt.
    
    Args:
        prompt: Prompt to check
        security_mode: Optional security mode override
    
    Returns:
        True if safe, False if jailbreak detected
    
    Raises:
        JailbreakModelError: In FAIL_CLOSED mode if model unavailable
    """
    return get_guard(security_mode=security_mode).check(prompt)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "JailbreakGuard",
    "JailbreakDetectedError",
    "JailbreakModelError",
    "get_guard",
    "check_prompt",
    "TRANSFORMERS_AVAILABLE",
]
