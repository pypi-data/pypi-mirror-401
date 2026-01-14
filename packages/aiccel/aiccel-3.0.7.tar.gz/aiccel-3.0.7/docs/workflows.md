# Workflows

Workflows enable complex multi-step agent orchestration using a DAG (Directed Acyclic Graph) pattern.

## Overview

Workflows let you:
- Chain multiple agents together
- Execute tasks in parallel
- Branch based on conditions
- Checkpointing and recovery

---

## Quick Start

```python
from aiccel import WorkflowBuilder, WorkflowExecutor, SlimAgent, GeminiProvider

provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")

# Create agents
researcher = SlimAgent(provider=provider, name="Researcher")
writer = SlimAgent(provider=provider, name="Writer")

# Build workflow
workflow = (
    WorkflowBuilder("content_pipeline")
    .add_agent("research", researcher, input_key="topic", output_key="research")
    .add_agent("write", writer, input_key="research", output_key="article")
    .connect("research", "write")
    .build()
)

# Execute
executor = WorkflowExecutor()
result = await executor.run(workflow, {"topic": "AI trends in 2024"})

print(result.outputs["article"])
```

---

## Workflow Builder

The `WorkflowBuilder` provides a fluent API for creating workflows.

### Adding Nodes

```python
from aiccel import WorkflowBuilder

builder = WorkflowBuilder("my_workflow")

# Add agent node
builder.add_agent(
    id="agent1",
    agent=my_agent,
    name="Research Agent",
    input_key="query",
    output_key="results"
)

# Add tool node
builder.add_tool(
    id="search",
    tool=search_tool,
    args_mapping={"query": "search_query"}
)

# Add function node
builder.add_function(
    id="process",
    func=lambda state: {"processed": state.get("data")}
)

# Add router node
builder.add_router(
    id="router",
    routes={
        "weather": lambda s: "weather" in s.get("query", "").lower(),
        "search": lambda s: True  # default
    }
)
```

### Connecting Nodes

```python
# Simple connection
builder.connect("node1", "node2")

# Chain multiple nodes
builder.chain("node1", "node2", "node3", "node4")

# Conditional connection
builder.connect(
    "router",
    "weather_agent",
    condition=lambda s: s.get("route") == "weather"
)

# Connect with conditions
builder.connect_conditional(
    source="router",
    routes={
        "weather": "weather_agent",
        "search": "search_agent",
        "default": "general_agent"
    }
)
```

### Entry and End Nodes

```python
builder.set_entry("start_node")  # First node
builder.set_end("final_node")    # Terminal node
```

---

## Node Types

### AgentNode

Executes an AI agent:

```python
from aiccel.workflows import AgentNode

node = AgentNode(
    id="researcher",
    name="Research Agent",
    agent=research_agent,
    input_key="query",
    output_key="research_results",
    prompt_template="Research this topic: {topic}"  # Optional template
)
```

### ToolNode

Executes a tool directly:

```python
from aiccel.workflows import ToolNode

node = ToolNode(
    id="search",
    tool=search_tool,
    args_mapping={"query": "search_query"},  # Map state keys to tool args
    output_key="search_results"
)
```

### RouterNode

Routes to different paths:

```python
from aiccel.workflows import RouterNode

node = RouterNode(
    id="router",
    routes={
        "weather": lambda state: "weather" in state.get("query", "").lower(),
        "math": lambda state: any(op in state.get("query", "") for op in ["+", "-", "*", "/"]),
        "default": lambda state: True
    },
    output_key="route"
)
```

### ParallelNode

Executes multiple nodes concurrently:

```python
from aiccel.workflows import ParallelNode, AgentNode

node = ParallelNode(
    id="parallel_research",
    nodes=[
        AgentNode(id="tech", agent=tech_agent),
        AgentNode(id="business", agent=business_agent),
        AgentNode(id="science", agent=science_agent)
    ],
    combine_strategy="merge",  # merge, list, first
    output_key="all_research"
)
```

### ConditionalNode

Branches based on condition:

```python
from aiccel.workflows import ConditionalNode

node = ConditionalNode(
    id="quality_check",
    condition=lambda state: len(state.get("content", "")) > 500,
    true_node=publish_node,
    false_node=rewrite_node
)
```

### TransformNode

Transforms state data:

```python
from aiccel.workflows import TransformNode

node = TransformNode(
    id="format",
    transform=lambda state: {
        "formatted_output": state.get("raw_output", "").strip().upper()
    }
)
```

---

## Execution

### Basic Execution

```python
from aiccel import WorkflowExecutor

executor = WorkflowExecutor(
    max_iterations=100,
    timeout=300.0,
    checkpoint_enabled=True
)

# Async execution (recommended)
result = await executor.run(workflow, {"input": "value"})

# Sync execution
result = executor.run_sync(workflow, {"input": "value"})
```

### Accessing Results

```python
# Get outputs
print(result.outputs)  # All node outputs

# Get specific output
print(result.get("final_answer"))

# Get execution history
for step in result.history:
    print(f"{step['node_id']}: {step['status']}")
```

### Checkpointing

Resume from failures:

```python
executor = WorkflowExecutor(checkpoint_enabled=True)

try:
    result = await executor.run(workflow, inputs)
except Exception:
    # Resume from last checkpoint
    result = await executor.run(workflow, inputs, resume_from="last_node_id")
```

---

## Complete Example

```python
from aiccel import (
    WorkflowBuilder, WorkflowExecutor,
    SlimAgent, GeminiProvider, SearchTool
)

# Setup
provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
search = SearchTool(api_key="...")

# Create specialized agents
researcher = SlimAgent(provider=provider, name="Researcher", tools=[search])
analyzer = SlimAgent(provider=provider, name="Analyzer")
writer = SlimAgent(provider=provider, name="Writer")

# Build workflow
workflow = (
    WorkflowBuilder("blog_generator", "Generate blog posts from topics")
    
    # Step 1: Research the topic
    .add_agent("research", researcher,
               input_key="topic",
               output_key="research_data",
               prompt_template="Research thoroughly: {topic}")
    
    # Step 2: Analyze the research
    .add_agent("analyze", analyzer,
               input_key="research_data",
               output_key="key_points",
               prompt_template="Extract key points from: {research_data}")
    
    # Step 3: Write the blog post
    .add_agent("write", writer,
               input_key="key_points",
               output_key="blog_post",
               prompt_template="Write a blog post using these points: {key_points}")
    
    # Connect in sequence
    .chain("research", "analyze", "write")
    .set_end("write")
    
    .build()
)

# Execute
async def main():
    executor = WorkflowExecutor(timeout=120.0)
    result = await executor.run(workflow, {"topic": "The Future of AI"})
    
    print("=== Blog Post ===")
    print(result.outputs["blog_post"])
    
    print("\n=== Execution Stats ===")
    print(f"Steps: {len(result.history)}")
    print(f"Duration: {result.elapsed_ms:.0f}ms")

import asyncio
asyncio.run(main())
```

---

## Parallel Execution Example

```python
workflow = (
    WorkflowBuilder("parallel_research")
    
    # Parallel research from multiple angles
    .add_parallel("research_all", [
        AgentNode(id="tech", agent=tech_researcher, output_key="tech_research"),
        AgentNode(id="market", agent=market_researcher, output_key="market_research"),
        AgentNode(id="user", agent=user_researcher, output_key="user_research"),
    ], combine_strategy="merge")
    
    # Synthesize all research
    .add_agent("synthesize", synthesis_agent,
               prompt_template="Combine these research findings: {tech_research} {market_research} {user_research}")
    
    .connect("research_all", "synthesize")
    .build()
)
```

---

## Best Practices

1. **Name nodes clearly** - Use descriptive IDs
2. **Keep workflows focused** - One workflow per task type
3. **Use checkpointing** - For long-running workflows
4. **Set timeouts** - Prevent infinite loops
5. **Handle errors** - Add error handling nodes

---

## Next Steps

- [Autonomous](./autonomous.md) - Goal-driven workflows
- [FastAPI](./fastapi.md) - Expose workflows as APIs
