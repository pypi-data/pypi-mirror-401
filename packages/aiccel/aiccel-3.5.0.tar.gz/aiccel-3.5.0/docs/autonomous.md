# 🤖 Autonomous Agents

Autonomous agents are "Goal Driven." Unlike workflows, you give them a high-level objective, and they plan and execute tasks until the goal is met.

---

## 1. GoalAgent

The `GoalAgent` is the most powerful entity in AICCEL. It can decompose a goal, execute sub-tasks, and reflect on its own performance.

```python
from aiccel.autonomous import GoalAgent, Goal
from aiccel import GeminiProvider

agent = GoalAgent(
    provider=GeminiProvider(),
    tools=[...],
    max_iterations=20,     # Safety limit to prevent infinite loops
    reflection_enabled=True # Agent will learn from errors as it goes
)

# Assign a multi-step objective
agent.add_goal(Goal(
    id="market_research",
    description="Analyze the top 3 competitors in the AI industry",
    success_criteria="Found names, pricing, and 2 unique features for each"
))

# Run until the criteria is met
results = await agent.run_until_complete()
```

---

## 2. Key Terminology

### `Goal`
A structured object defining what success looks like.
*   `id`: Internal identifier.
*   `description`: What to do.
*   `success_criteria`: **Critical**. The agent uses this to verify if it has actually finished the task.
*   `dependencies`: List of goal IDs that must finish first.

### `TaskPlanner`
Under the hood, `GoalAgent` uses a `TaskPlanner` to break complex goals into smaller sub-tasks. You can also use it standalone:

```python
from aiccel.autonomous import TaskPlanner

planner = TaskPlanner(provider=provider)
plan = await planner.create_plan("Launch a new satellite into orbit")

for task in plan.tasks:
    print(f"Step: {task.title}")
```

---

## 3. Self-Reflection
When `reflection_enabled=True`, the agent keeps a "learning buffer." If it tries to use a tool and fails, it records the failure. The next time it tries that task, it will adapt its strategy.

---

## 4. Best Practices

1.  **Define success precisely**: Instead of saying "Research AI," say "Find 5 recent articles on generative AI published in 2024."
2.  **Set `max_iterations`**: Autonomous agents can become over-ambitious. Always set a limit to manage costs.
3.  **Monitor with `verbose`**: Setting `verbose=True` lets you see the agent's internal reasoning as it plans its next move.
