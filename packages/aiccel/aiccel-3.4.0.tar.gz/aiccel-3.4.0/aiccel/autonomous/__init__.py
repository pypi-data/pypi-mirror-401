# aiccel/autonomous/__init__.py
"""
Autonomous Agent Capabilities
==============================

Self-improving, goal-driven autonomous agents.

Features:
- Goal decomposition
- Self-reflection
- Memory and learning
- Plan execution
- Error recovery
"""

from .goal_agent import GoalAgent, Goal, GoalStatus
from .self_reflection import ReflectionMixin, SelfReflection
from .planner import TaskPlanner, Task, Plan

__all__ = [
    'GoalAgent',
    'Goal',
    'GoalStatus',
    'ReflectionMixin',
    'SelfReflection',
    'TaskPlanner',
    'Task',
    'Plan',
]
