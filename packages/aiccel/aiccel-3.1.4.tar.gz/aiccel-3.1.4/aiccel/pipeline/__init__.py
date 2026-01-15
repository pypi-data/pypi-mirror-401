# aiccel/pipeline/__init__.py
"""
Pipeline Module
================

Extensible middleware pipeline for agent execution.
"""

from .middleware import (
    MiddlewarePipeline,
    Middleware,
    LoggingMiddleware,
    ValidationMiddleware,
    RateLimitMiddleware,
    RetryMiddleware,
    CachingMiddleware,
    MetricsMiddleware,
    create_default_pipeline,
)

__all__ = [
    'MiddlewarePipeline',
    'Middleware',
    'LoggingMiddleware',
    'ValidationMiddleware',
    'RateLimitMiddleware',
    'RetryMiddleware',
    'CachingMiddleware',
    'MetricsMiddleware',
    'create_default_pipeline',
]
