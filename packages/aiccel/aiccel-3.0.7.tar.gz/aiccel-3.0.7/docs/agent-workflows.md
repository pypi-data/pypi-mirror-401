# Agent Workflows - Complete Guide

Build complex multi-agent systems with DAG-based workflows.

---

## Why Workflows?

Workflows solve common challenges:

| Challenge | Solution |
|-----------|----------|
| Complex multi-step tasks | Chain agents sequentially |
| Parallel processing | Execute agents concurrently |
| Conditional logic | Route based on results |
| Error recovery | Checkpoint and resume |
| Reusability | Define once, run many times |

---

## Architecture Overview

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Input  │────▶│  Node 1 │────▶│  Node 2 │
└─────────┘     └─────────┘     └─────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
              ┌─────────┐                       ┌─────────┐
              │ Node 3a │                       │ Node 3b │
              └─────────┘                       └─────────┘
                    │                                 │
                    └────────────────┬────────────────┘
                                     ▼
                              ┌─────────┐
                              │ Output  │
                              └─────────┘
```

---

## Building Blocks

### 1. WorkflowBuilder

Fluent API for creating workflows:

```python
from aiccel import WorkflowBuilder

workflow = (
    WorkflowBuilder("my_workflow", "Description of what it does")
    .add_agent(...)      # Add agent node
    .add_tool(...)       # Add tool node
    .add_router(...)     # Add routing node
    .add_parallel(...)   # Add parallel execution
    .add_function(...)   # Add custom function
    .connect(...)        # Connect nodes
    .chain(...)          # Chain nodes sequentially
    .build()             # Build workflow
)
```

### 2. Workflow Nodes

Different node types for different purposes:

#### AgentNode - Execute an AI agent

```python
from aiccel.workflows import AgentNode

node = AgentNode(
    id="researcher",                    # Unique identifier
    name="Research Agent",              # Display name
    agent=research_agent,               # Agent instance
    input_key="topic",                  # Key to read from state
    output_key="research_results",      # Key to write to state
    prompt_template="Research: {topic}" # Optional template
)
```

#### ToolNode - Execute a tool directly

```python
from aiccel.workflows import ToolNode

node = ToolNode(
    id="search",
    tool=search_tool,
    args_mapping={
        "query": "search_query"    # Map state keys to tool args
    },
    output_key="search_results"
)
```

#### RouterNode - Decision making

```python
from aiccel.workflows import RouterNode

node = RouterNode(
    id="classify",
    routes={
        "code": lambda s: "code" in s.get("query", "").lower(),
        "math": lambda s: any(op in s.get("query", "") for op in "+-*/"),
        "search": lambda s: "find" in s.get("query", "").lower(),
        "default": lambda s: True  # Fallback
    },
    output_key="route"
)
```

#### ParallelNode - Concurrent execution

```python
from aiccel.workflows import ParallelNode, AgentNode

node = ParallelNode(
    id="multi_research",
    nodes=[
        AgentNode(id="tech", agent=tech_agent, output_key="tech_data"),
        AgentNode(id="market", agent=market_agent, output_key="market_data"),
        AgentNode(id="legal", agent=legal_agent, output_key="legal_data")
    ],
    combine_strategy="merge",  # merge, list, first
    output_key="all_research"
)
```

#### ConditionalNode - If/else logic

```python
from aiccel.workflows import ConditionalNode

node = ConditionalNode(
    id="quality_check",
    condition=lambda s: len(s.get("content", "")) > 500,
    true_node=publish_node,    # If condition true
    false_node=rewrite_node    # If condition false
)
```

#### TransformNode - Data transformation

```python
from aiccel.workflows import TransformNode

node = TransformNode(
    id="format",
    transform=lambda state: {
        "formatted": state.get("raw", "").strip().upper(),
        "word_count": len(state.get("raw", "").split())
    }
)
```

---

## Workflow Patterns

### Pattern 1: Sequential Pipeline

```python
# Research → Analyze → Write → Review

workflow = (
    WorkflowBuilder("content_pipeline")
    
    .add_agent("research", research_agent,
               input_key="topic", output_key="research")
    
    .add_agent("analyze", analyst_agent,
               input_key="research", output_key="analysis")
    
    .add_agent("write", writer_agent,
               input_key="analysis", output_key="draft")
    
    .add_agent("review", reviewer_agent,
               input_key="draft", output_key="final")
    
    .chain("research", "analyze", "write", "review")
    .build()
)
```

### Pattern 2: Fan-Out / Fan-In

```python
# Parallel research from multiple sources, then combine

workflow = (
    WorkflowBuilder("multi_source_research")
    
    # Fan out: parallel research
    .add_parallel("gather", [
        AgentNode(id="web", agent=web_agent, output_key="web_results"),
        AgentNode(id="academic", agent=academic_agent, output_key="academic_results"),
        AgentNode(id="news", agent=news_agent, output_key="news_results")
    ], combine_strategy="merge")
    
    # Fan in: synthesize
    .add_agent("synthesize", synthesizer_agent,
               prompt_template="Combine these findings: {web_results} {academic_results} {news_results}",
               output_key="final_report")
    
    .connect("gather", "synthesize")
    .build()
)
```

### Pattern 3: Router with Specialists

```python
workflow = (
    WorkflowBuilder("smart_router")
    
    # Classify the query
    .add_router("classify", routes={
        "code": lambda s: any(kw in s.get("query", "").lower() 
                             for kw in ["code", "program", "function", "python"]),
        "math": lambda s: any(c in s.get("query", "") for c in "+-*/="),
        "creative": lambda s: any(kw in s.get("query", "").lower()
                                 for kw in ["write", "story", "poem"]),
        "general": lambda s: True
    })
    
    # Specialist agents
    .add_agent("code_expert", code_agent, input_key="query", output_key="response")
    .add_agent("math_expert", math_agent, input_key="query", output_key="response")
    .add_agent("creative_expert", creative_agent, input_key="query", output_key="response")
    .add_agent("general_expert", general_agent, input_key="query", output_key="response")
    
    # Route to appropriate expert
    .connect("classify", "code_expert", 
             condition=lambda s: s.get("route") == "code")
    .connect("classify", "math_expert",
             condition=lambda s: s.get("route") == "math")
    .connect("classify", "creative_expert",
             condition=lambda s: s.get("route") == "creative")
    .connect("classify", "general_expert",
             condition=lambda s: s.get("route") == "general")
    
    .build()
)
```

### Pattern 4: Iterative Refinement

```python
from aiccel.workflows import WorkflowNode

class RefinementNode(WorkflowNode):
    """Iteratively refine until quality threshold met."""
    
    def __init__(self, agent, evaluator, max_iterations=3):
        super().__init__(id="refine", name="Refinement", type="refinement")
        self.agent = agent
        self.evaluator = evaluator
        self.max_iterations = max_iterations
    
    async def execute(self, state):
        content = state.get("draft", "")
        
        for i in range(self.max_iterations):
            # Evaluate
            score = await self.evaluator.run_async(
                f"Rate this content 1-10: {content}"
            )
            
            if "8" in score["response"] or "9" in score["response"] or "10" in score["response"]:
                break
            
            # Refine
            result = await self.agent.run_async(
                f"Improve this content: {content}"
            )
            content = result["response"]
        
        state.set("refined_content", content)
        return content


workflow = (
    WorkflowBuilder("iterative_writing")
    .add_agent("draft", writer_agent, input_key="topic", output_key="draft")
    .add_node(RefinementNode(refiner_agent, evaluator_agent))
    .connect("draft", "refine")
    .build()
)
```

### Pattern 5: Human-in-the-Loop

```python
class HumanApprovalNode(WorkflowNode):
    """Wait for human approval before proceeding."""
    
    def __init__(self, approval_callback):
        super().__init__(id="approve", name="Human Approval", type="human")
        self.approval_callback = approval_callback
    
    async def execute(self, state):
        content = state.get("draft", "")
        
        # Request human approval (could be via webhook, UI, etc.)
        approved = await self.approval_callback(content)
        
        state.set("approved", approved)
        return approved


workflow = (
    WorkflowBuilder("human_review")
    .add_agent("generate", writer_agent, output_key="draft")
    .add_node(HumanApprovalNode(request_approval_func))
    .add_agent("publish", publisher_agent, input_key="draft")
    .add_agent("revise", reviser_agent, input_key="draft")
    
    .connect("generate", "approve")
    .connect("approve", "publish", condition=lambda s: s.get("approved"))
    .connect("approve", "revise", condition=lambda s: not s.get("approved"))
    .connect("revise", "approve")  # Loop back for re-approval
    
    .build()
)
```

---

## Workflow State

### Understanding State

State flows through the workflow carrying data:

```python
from aiccel.workflows import WorkflowState

state = WorkflowState(
    inputs={"topic": "AI trends"},    # Initial inputs
    outputs={},                        # Node outputs accumulate here
    context={},                        # Shared context
    history=[]                         # Execution history
)

# Access state
topic = state.get("topic")       # Checks outputs, then inputs, then context
state.set("research", "...")     # Sets in outputs

# In node execution
async def my_node(state):
    input_val = state.get("input_key")
    # Process...
    state.set("output_key", result)
    return result
```

### State Flow Example

```
Input: {"topic": "AI"}
    │
    ▼
[Research Node]
    │ state.set("research", "AI is...")
    ▼
State: {"topic": "AI", "research": "AI is..."}
    │
    ▼
[Write Node]
    │ state.set("article", "...")
    ▼
State: {"topic": "AI", "research": "AI is...", "article": "..."}
```

---

## Workflow Execution

### Basic Execution

```python
from aiccel import WorkflowExecutor

executor = WorkflowExecutor(
    max_iterations=100,     # Prevent infinite loops
    timeout=300.0,          # 5 minute timeout
    checkpoint_enabled=True # Enable checkpoints
)

# Async execution (recommended)
result = await executor.run(workflow, {"topic": "Quantum Computing"})

# Sync execution
result = executor.run_sync(workflow, {"topic": "Quantum Computing"})
```

### Accessing Results

```python
# All outputs
print(result.outputs)

# Specific output
print(result.get("final_article"))

# Execution history
for step in result.history:
    print(f"{step['node_id']}: {step['status']} at {step['timestamp']}")

# Check for errors
if result.error:
    print(f"Workflow failed: {result.error}")
```

### Checkpointing & Recovery

```python
executor = WorkflowExecutor(checkpoint_enabled=True)

try:
    result = await executor.run(workflow, inputs)
except Exception as e:
    print(f"Failed at: {e}")
    
    # Resume from last checkpoint
    result = await executor.run(workflow, inputs, resume_from="last_node_id")
```

---

## Complete Examples

### Example 1: Blog Content Generator

```python
import asyncio
from aiccel import SlimAgent, GeminiProvider, SearchTool
from aiccel import WorkflowBuilder, WorkflowExecutor

async def main():
    provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
    search = SearchTool(api_key="...")
    
    # Create agents
    researcher = SlimAgent(provider=provider, name="Researcher", tools=[search])
    outliner = SlimAgent(provider=provider, name="Outliner",
                         instructions="Create detailed outlines for articles.")
    writer = SlimAgent(provider=provider, name="Writer",
                       instructions="Write engaging blog posts.")
    editor = SlimAgent(provider=provider, name="Editor",
                       instructions="Edit for clarity and grammar.")
    
    # Build workflow
    workflow = (
        WorkflowBuilder("blog_generator")
        
        .add_agent("research", researcher,
                   input_key="topic",
                   output_key="research_notes",
                   prompt_template="Research this topic thoroughly: {topic}")
        
        .add_agent("outline", outliner,
                   input_key="research_notes",
                   output_key="outline",
                   prompt_template="Create an outline based on: {research_notes}")
        
        .add_agent("write", writer,
                   output_key="draft",
                   prompt_template="Write a blog post following this outline: {outline}")
        
        .add_agent("edit", editor,
                   input_key="draft",
                   output_key="final_post",
                   prompt_template="Edit this draft: {draft}")
        
        .chain("research", "outline", "write", "edit")
        .set_end("edit")
        .build()
    )
    
    # Execute
    executor = WorkflowExecutor(timeout=180.0)
    result = await executor.run(workflow, {
        "topic": "The Future of Remote Work in 2025"
    })
    
    print("=== Final Blog Post ===")
    print(result.outputs["final_post"])

asyncio.run(main())
```

### Example 2: Code Review Pipeline

```python
workflow = (
    WorkflowBuilder("code_review")
    
    # Analyze code
    .add_agent("analyze", analyzer_agent,
               input_key="code",
               output_key="analysis",
               prompt_template="Analyze this code for issues: {code}")
    
    # Parallel checks
    .add_parallel("checks", [
        AgentNode(id="security", agent=security_agent,
                  prompt_template="Check for security issues: {code}",
                  output_key="security_report"),
        AgentNode(id="performance", agent=performance_agent,
                  prompt_template="Check for performance issues: {code}",
                  output_key="perf_report"),
        AgentNode(id="style", agent=style_agent,
                  prompt_template="Check code style: {code}",
                  output_key="style_report")
    ])
    
    # Combine reports
    .add_agent("summarize", summarizer_agent,
               output_key="final_review",
               prompt_template="""
               Create a code review summary:
               Analysis: {analysis}
               Security: {security_report}
               Performance: {perf_report}
               Style: {style_report}
               """)
    
    .connect("analyze", "checks")
    .connect("checks", "summarize")
    .build()
)
```

---

## Best Practices

1. **Keep nodes focused** - One responsibility per node
2. **Use descriptive IDs** - `research_phase` not `node1`
3. **Set timeouts** - Prevent runaway workflows
4. **Enable checkpoints** - For recovery
5. **Test individual nodes** - Before composing
6. **Log state changes** - For debugging
7. **Handle all routing cases** - Include default routes

---

## Next Steps

- [MCP Integration](./mcp.md) - Connect to external tools
- [Autonomous Workflows](./autonomous.md) - Self-directing agents
