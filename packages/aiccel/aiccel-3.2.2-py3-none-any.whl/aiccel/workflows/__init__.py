# aiccel/workflows/__init__.py
"""
Agent Workflows
================

DAG-based workflow orchestration for complex multi-agent tasks.
Inspired by Prefect, Airflow, and LangGraph.

Features:
- DAG-based task execution
- Conditional branching
- Parallel execution
- State management
- Checkpointing
"""

from .graph import Workflow, WorkflowNode, WorkflowEdge, WorkflowState
from .nodes import AgentNode, ToolNode, RouterNode, ParallelNode, ConditionalNode
from .builder import WorkflowBuilder
from .executor import WorkflowExecutor

__all__ = [
    # Core
    'Workflow',
    'WorkflowNode',
    'WorkflowEdge',
    'WorkflowState',
    
    # Nodes
    'AgentNode',
    'ToolNode',
    'RouterNode',
    'ParallelNode',
    'ConditionalNode',
    
    # Building
    'WorkflowBuilder',
    
    # Execution
    'WorkflowExecutor',
]
