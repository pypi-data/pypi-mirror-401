# aiccel/providers.py
"""
DEPRECATED: This module is deprecated and will be removed in v4.0.0.
Please import from `aiccel.providers` package instead.

Migration:
    Old: from aiccel.providers import OpenAIProvider
    New: from aiccel.providers import OpenAIProvider (same import works if you use the package)
"""

import warnings
from .providers.base import LLMProvider
from .providers.openai import OpenAIProvider
from .providers.gemini import GeminiProvider
from .providers.groq import GroqProvider

warnings.warn(
    "aiccel.providers module is deprecated. Use aiccel.providers package instead.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = [
    "LLMProvider",
    "OpenAIProvider",
    "GeminiProvider",
    "GroqProvider",
]