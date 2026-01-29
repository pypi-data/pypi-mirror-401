# aiccel/providers/__init__.py
"""
AICCEL LLM Providers
====================

Multi-provider LLM support with connection pooling and observability.

Available Providers:
    - OpenAIProvider: OpenAI GPT models
    - GeminiProvider: Google Gemini models
    - GroqProvider: Groq-hosted models (LLaMA, Mixtral)

Usage:
    from aiccel.providers import OpenAIProvider, GeminiProvider, GroqProvider
"""

from .base import LLMProvider
from .openai import OpenAIProvider
from .gemini import GeminiProvider
from .groq import GroqProvider

__all__ = [
    "LLMProvider",
    "OpenAIProvider", 
    "GeminiProvider",
    "GroqProvider",
]
