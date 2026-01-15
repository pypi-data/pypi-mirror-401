# ⛓️ Workflows

Workflows allow you to build deterministic pipelines of agents and tools using a Directed Acyclic Graph (DAG) pattern.

---

## 1. Why use Workflows?
While standard agents are dynamic, workflows are **reliable**. They ensure steps happen in a specific order, with defined data passing between them.

---

## 2. A Simple Content Pipeline

```python
from aiccel import WorkflowBuilder, WorkflowExecutor, Agent, GeminiProvider

provider = GeminiProvider()

# 1. Define nodes
researcher = Agent(provider=provider, name="Researcher")
writer = Agent(provider=provider, name="Writer")

# 2. Build the graph
workflow = (
    WorkflowBuilder("blog_post_gen")
    .add_agent("research", researcher, input_key="topic", output_key="raw_info")
    .add_agent("write", writer, input_key="raw_info", output_key="blog_post")
    .connect("research", "write")
    .build()
)

# 3. Execute
executor = WorkflowExecutor()
result = await executor.run(workflow, {"topic": "The future of AI"})
print(result.outputs['blog_post'])
```

---

## 3. Node Types

### `add_agent`
Executes an agent. You can map global state to agent input and save agent output back to state.
*   `input_key`: Where to find the query in the state.
*   `output_key`: Where to save the answer.

### `add_parallel`
Executes multiple agents or tasks **at the same time**. Great for comparing different search results or generating multiple drafts.

### `add_router`
Branch the workflow based on data.
```python
builder.add_router("decision_node", routes={
    "is_code": lambda state: "code" in state['query'],
    "is_text": lambda state: True
})
```

---

## 4. Execution & Checkpoints

Workflows can be long-running. AICCEL includes built-in state management.

```python
executor = WorkflowExecutor(
    checkpoint_enabled=True,
    timeout=300.0  # Time out after 5 minutes
)

# Execute async
result = await executor.run(workflow, inputs)

# result.history contains a full trace of what happened and when.
```

---

## 5. Tips
1.  **Keep it focused**: Use Workflows for structured processes (like writing an email based on a report).
2.  **Naming handles**: Use clear IDs for nodes (e.g., `"search_node"`, `"format_response"`) to make debugging easier.
3.  **Parallelize**: Use `add_parallel` whenever steps don't depend on each other to drastically reduce total runtime.
