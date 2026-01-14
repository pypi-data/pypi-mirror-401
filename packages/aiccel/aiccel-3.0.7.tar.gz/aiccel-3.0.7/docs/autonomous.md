# Autonomous Agents

Autonomous agents can pursue goals independently, learn from mistakes, and self-correct.

## Overview

AICCEL provides:
- **GoalAgent** - Pursues goals with automatic retry and reflection
- **TaskPlanner** - AI-powered task decomposition
- **SelfReflection** - Learn from errors

---

## GoalAgent

An agent that autonomously works toward goals.

```python
from aiccel import GoalAgent, Goal, GeminiProvider

provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")

# Create autonomous agent
agent = GoalAgent(
    provider=provider,
    tools=[search_tool, code_tool],
    max_iterations=50,
    reflection_enabled=True,
    verbose=True
)

# Add goals
agent.add_goal(Goal(
    id="research",
    description="Research the latest AI developments",
    success_criteria="Found at least 5 recent AI breakthroughs",
    priority=1,
    max_attempts=3
))

agent.add_goal(Goal(
    id="summarize",
    description="Create a summary report",
    success_criteria="Written a 500+ word summary",
    priority=2,
    dependencies=["research"]  # Depends on research completing first
))

# Run until complete
results = await agent.run_until_complete(timeout=300.0)

print(f"Completed: {results['completed']}")
print(f"Failed: {results['failed']}")
print(f"Results: {results['results']}")
```

---

## Goal Configuration

```python
from aiccel.autonomous import Goal, GoalStatus

goal = Goal(
    id="unique_id",
    description="What to accomplish",
    success_criteria="How to verify success",
    priority=1,              # Lower = higher priority
    deadline=None,           # Optional datetime
    dependencies=["goal1"],  # Must complete first
    max_attempts=3,          # Retry limit
    subtasks=[]              # Auto-generated subtasks
)

# Goal statuses
# GoalStatus.PENDING - Not started
# GoalStatus.IN_PROGRESS - Currently executing
# GoalStatus.COMPLETED - Successfully done
# GoalStatus.FAILED - Failed after all attempts
# GoalStatus.BLOCKED - Dependencies not met
```

---

## Goal Decomposition

Complex goals are automatically broken down:

```python
agent = GoalAgent(provider=provider)

goal = Goal(
    id="build_app",
    description="Build a web scraper application",
    success_criteria="Working scraper that extracts product data"
)

# Agent will decompose into subtasks like:
# - Set up project structure
# - Write scraping logic
# - Add error handling
# - Test with sample sites
# - Document the code

agent.add_goal(goal)
await agent.run_until_complete()
```

---

## TaskPlanner

AI-powered task planning:

```python
from aiccel.autonomous import TaskPlanner

planner = TaskPlanner(
    provider=provider,
    max_tasks=10,
    include_estimates=True
)

# Create a plan
plan = await planner.create_plan(
    goal="Build a REST API for user management",
    context="Using Python and FastAPI",
    constraints=["Must include authentication", "Use PostgreSQL"]
)

# View tasks
for task in plan.tasks:
    print(f"- {task.title} (Est: {task.estimated_time}min)")
    print(f"  Deps: {task.dependencies}")

# Get progress
progress = plan.get_progress()
print(f"Progress: {progress['progress_pct']}%")
```

### Plan Management

```python
# Get next task
next_task = plan.get_next_task(completed={"task1", "task2"})

# Mark task complete
next_task.status = TaskStatus.DONE
next_task.result = "Completed successfully"

# Refine a task
refined = await planner.refine_task(
    task=some_task,
    feedback="Need more detail on the implementation"
)
```

---

## Self-Reflection

Enable agents to learn from mistakes:

```python
from aiccel.autonomous import SelfReflection, ReflectionMixin

# Add reflection to any agent
class LearningAgent(SlimAgent, ReflectionMixin):
    pass

agent = LearningAgent(provider=provider)
agent.enable_reflection(max_memories=50)

# After each action, reflect
result = agent.run("Do something")

if success:
    agent.reflect(
        action="search query",
        outcome=result,
        success=True,
        learnings=["This approach worked well"]
    )
else:
    agent.reflect(
        action="search query",
        outcome=str(error),
        success=False,
        learnings=["Should try different keywords", "API was rate limited"]
    )

# Get relevant learnings for new context
learnings = agent.get_learnings("similar query")
# Returns: ["Should try different keywords", "API was rate limited"]
```

---

## Complete Autonomous Example

```python
import asyncio
from aiccel import GeminiProvider, SearchTool
from aiccel.autonomous import GoalAgent, Goal

async def main():
    provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
    search = SearchTool(api_key="...")
    
    # Create autonomous agent
    agent = GoalAgent(
        provider=provider,
        tools=[search],
        max_iterations=30,
        reflection_enabled=True
    )
    
    # Define multi-step goal
    agent.add_goals([
        Goal(
            id="research_competitors",
            description="Research top 5 AI agent frameworks",
            success_criteria="Found info on LangChain, AutoGPT, CrewAI, Semantic Kernel, and others",
            priority=1
        ),
        Goal(
            id="analyze_features",
            description="Analyze key features of each framework",
            success_criteria="Documented features for each framework",
            priority=2,
            dependencies=["research_competitors"]
        ),
        Goal(
            id="generate_report",
            description="Create comparison report",
            success_criteria="Written structured comparison document",
            priority=3,
            dependencies=["analyze_features"]
        )
    ])
    
    # Run autonomously
    print("Starting autonomous execution...")
    results = await agent.run_until_complete(timeout=180.0)
    
    print("\n=== Results ===")
    print(f"Completed goals: {results['completed']}")
    print(f"Failed goals: {results['failed']}")
    print(f"Total iterations: {results['iterations']}")
    print(f"Duration: {results['duration_s']:.1f}s")
    
    # Print final report
    if "generate_report" in results['results']:
        print("\n=== Comparison Report ===")
        print(results['results']['generate_report'])

asyncio.run(main())
```

---

## Best Practices

1. **Clear success criteria** - Make verification unambiguous
2. **Set max_attempts** - Prevent infinite retries
3. **Use dependencies** - Order goals logically
4. **Enable reflection** - Improves over time
5. **Set timeouts** - For production safety
6. **Monitor progress** - Use `get_status()` for visibility

---

## Next Steps

- [Workflows](./workflows.md) - Structured orchestration
- [Middleware](./middleware.md) - Add rate limiting
