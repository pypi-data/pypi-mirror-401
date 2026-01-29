# 🤝 Multi-Agent Systems

The `AgentManager` allows you to orchestrate multiple specialized agents to solve complex, multi-step problems.

---

## 1. The `AgentManager`

The manager acts as a router and a synthesizer. It analyzes the user query, breaks it into sub-tasks, assigns them to the right agents, and merges the results into a final answer.

```python
from aiccel.manager import AgentManager
from aiccel.agent import Agent

# 1. Define specialized agents
researcher = Agent(name="Researcher", instructions="Find facts about technology.")
writer = Agent(name="Writer", instructions="Write professional articles.")

# 2. Initialize Manager
manager = AgentManager(
    llm_provider=provider,
    agents=[researcher, writer],
    verbose=True
)

# 3. Collaborate
result = await manager.collaborate_async("Research the impact of AI on medicine and write a summary.")
```

---

## 2. Collaboration Workflow

When `collaborate_async` is called, the manager follows three distinct phases:

1.  **Planning**: Analyzes the query and creates a `CollaborationPlan` (list of sub-tasks).
2.  **Execution**: Runs sub-tasks in parallel or sequence, depending on dependencies.
3.  **Synthesis**: Merges all tool outputs and agent responses into a final, coherent answer.

---

## 3. Schemas & Data Integrity

AgentManager v3.0 uses Pydantic schemas for internal communication. This eliminates parsing errors and ensures high reliability.

*   `CollaborationPlan`: The overall execution strategy.
*   `SubTask`: A granular task assigned to a specific agent.
*   `RoutingDecision`: Instructions for redirecting a query.

---

## 4. Why use a Manager?

*   **Task Specialization**: One "mega-agent" is often less accurate than two specialized agents.
*   **Parallel Execution**: Run multiple searches or calculations at once to save time.
*   **Reduced Context Bloat**: Each agent only sees what it needs to see for its specific task.

---

## 5. Tips for Success

1.  **Agent Descriptions**: The manager relies on the `description` field of an agent to decide who to hire. Make sure it accurately reflects the agent's expertise.
2.  **Instructions**: You can provide the manager with its own `instructions` (e.g., "Always prioritize the Research agent for technical queries").
3.  **Fallback**: The manager can handle fallback providers if the primary LLM is rate-limited.
