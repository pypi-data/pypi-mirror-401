# aiccel/agent_core/__init__.py
"""
Agent Core Module
==================

Split components from the monolithic agent.py for maintainability.

Components:
- PromptBuilder: Centralized prompt construction
- ToolExecutor: Tool selection and execution
- ExecutionOrchestrator: Execution flow orchestration
"""

from .prompt_builder import PromptBuilder, PromptConfig
from .tool_executor import ToolExecutor, ToolExecutionResult
from .orchestrator import (
    ExecutionOrchestrator,
    ExecutionContext,
    ExecutionResult,
)

__all__ = [
    # Prompt building
    'PromptBuilder',
    'PromptConfig',
    
    # Tool execution
    'ToolExecutor',
    'ToolExecutionResult',
    
    # Orchestration
    'ExecutionOrchestrator',
    'ExecutionContext',
    'ExecutionResult',
]
