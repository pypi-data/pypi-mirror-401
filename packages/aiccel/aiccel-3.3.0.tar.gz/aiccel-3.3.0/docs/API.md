# AICCEL API Reference
## Version 3.2

This document provides comprehensive API documentation for the AICCEL framework.

---

## Table of Contents

1. [Agent](#agent)
2. [Providers](#providers)
3. [Tools](#tools)
4. [Security](#security)
5. [Memory](#memory)
6. [Multi-Agent](#multi-agent)
7. [Workflows](#workflows)
8. [Utilities](#utilities)

---

## Agent

### `Agent`

The core AI agent class that handles queries, tools, and conversation.

```python
from aiccel import Agent, GeminiProvider

agent = Agent(
    provider=GeminiProvider(),
    name="MyAgent",
    instructions="You are a helpful assistant.",
    tools=[],
    config=None,
    memory=None,
    fallback_providers=[]
)
```

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `LLMProvider` | Required | The LLM provider to use |
| `name` | `str` | `"Agent"` | Agent name for logging |
| `instructions` | `str` | `""` | System instructions for the agent |
| `tools` | `List[BaseTool]` | `[]` | List of tools available to the agent |
| `config` | `AgentConfig` | `None` | Configuration options |
| `memory` | `ConversationMemory` | `None` | Conversation memory instance |
| `fallback_providers` | `List[LLMProvider]` | `[]` | Fallback providers if primary fails |

#### Methods

##### `run(query: str) -> Dict`

Execute a query synchronously.

```python
result = agent.run("What is the weather in Tokyo?")
print(result["response"])  # The agent's response
print(result["thinking"])  # Chain-of-thought (if enabled)
print(result["tools_used"])  # List of (tool_name, args) tuples
```

**Returns:**
```python
{
    "response": str,      # The agent's response
    "thinking": str,      # Thinking/reasoning (if enabled)
    "tools_used": List,   # Tools that were called
    "tool_outputs": List, # Raw tool outputs
    "execution_time": float,
    "metadata": Dict
}
```

##### `run_async(query: str) -> Dict`

Execute a query asynchronously.

```python
result = await agent.run_async("Analyze this data...")
```

##### `enable_thinking() -> Agent`

Enable chain-of-thought reasoning.

```python
agent.enable_thinking()
```

##### `add_tool(tool: BaseTool) -> Agent`

Add a tool to the agent.

```python
from aiccel.tools import SearchTool
agent.add_tool(SearchTool(api_key="..."))
```

##### `with_tool(tool: BaseTool) -> Agent`

Fluent API for adding tools (returns self).

```python
agent = Agent(provider=provider).with_tool(search).with_tool(calculator)
```

##### `get_memory() -> ConversationMemory`

Get the agent's conversation memory.

```python
memory = agent.get_memory()
messages = memory.get_messages()
```

##### `clear_memory() -> None`

Clear the conversation history.

```python
agent.clear_memory()
```

---

### `AgentConfig`

Configuration options for agents.

```python
from aiccel import AgentConfig

config = AgentConfig(
    thinking_enabled=True,
    thinking_budget=500,
    strict_tool_usage=False,
    max_tool_retries=3,
    tool_timeout=30.0,
    safety_enabled=True,
    pii_masking=False,
    memory_type="buffer",
    max_memory_turns=50,
    max_memory_tokens=32000
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `thinking_enabled` | `bool` | `False` | Enable chain-of-thought |
| `thinking_budget` | `int` | `500` | Max tokens for thinking |
| `strict_tool_usage` | `bool` | `False` | Require tools for all queries |
| `max_tool_retries` | `int` | `3` | Retry failed tools N times |
| `tool_timeout` | `float` | `30.0` | Tool execution timeout (seconds) |
| `safety_enabled` | `bool` | `False` | Enable jailbreak detection |
| `pii_masking` | `bool` | `False` | Auto-mask PII |
| `memory_type` | `str` | `"buffer"` | Memory type: buffer/window/summary |
| `max_memory_turns` | `int` | `50` | Max conversation turns |
| `max_memory_tokens` | `int` | `32000` | Max tokens in memory |

---

## Providers

### `GeminiProvider`

Google Gemini LLM provider.

```python
from aiccel import GeminiProvider

provider = GeminiProvider(
    api_key="...",  # Or uses GOOGLE_API_KEY env var
    model="gemini-2.0-flash",
    verbose=False
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `generate(prompt)` | Generate text completion |
| `generate_async(prompt)` | Async text completion |
| `chat(messages)` | Multi-turn chat completion |
| `chat_async(messages)` | Async chat completion |

### `OpenAIProvider`

OpenAI GPT provider.

```python
from aiccel import OpenAIProvider

provider = OpenAIProvider(
    api_key="...",  # Or uses OPENAI_API_KEY env var
    model="gpt-4o-mini",
    embedding_model="text-embedding-3-small"
)
```

#### Additional Methods

| Method | Description |
|--------|-------------|
| `embed(text)` | Generate text embeddings |
| `embed_async(text)` | Async embeddings |

### `GroqProvider`

Groq ultra-fast inference provider.

```python
from aiccel import GroqProvider

provider = GroqProvider(
    api_key="...",  # Or uses GROQ_API_KEY env var
    model="llama3-70b-8192"
)
```

---

## Tools

### `BaseTool`

Base class for creating custom tools.

```python
from aiccel.tools import BaseTool, ParameterSchema, ParameterType

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Does something useful",
            parameters=[
                ParameterSchema(
                    name="query",
                    type=ParameterType.STRING,
                    description="The query to process",
                    required=True
                )
            ]
        )
    
    def _execute(self, args):
        query = args.get("query")
        return {"result": f"Processed: {query}"}
```

### `ParameterSchema`

Define tool parameters.

```python
from aiccel.tools import ParameterSchema, ParameterType

param = ParameterSchema(
    name="query",
    type=ParameterType.STRING,  # STRING, NUMBER, INTEGER, BOOLEAN, ARRAY, OBJECT
    description="Search query",
    required=True,
    default=None,
    enum=None,  # List of allowed values
    min_length=1,
    max_length=1000
)
```

### `ToolResult`

Result from tool execution.

```python
from aiccel.tools import ToolResult

# Success
result = ToolResult.ok({"data": "value"}, execution_time=0.5)

# Failure
result = ToolResult.fail("Error message", execution_time=0.1)
```

### Built-in Tools

#### `SearchTool`

Web search via SerpAPI or Tavily.

```python
from aiccel.tools import SearchTool

search = SearchTool(
    api_key="...",  # SerpAPI key
    max_results=5
)

result = search.execute({"query": "Python tutorials"})
```

#### `WeatherTool`

Weather lookup via OpenWeatherMap.

```python
from aiccel.tools import WeatherTool

weather = WeatherTool(api_key="...")
result = weather.execute({"location": "Tokyo"})
```

#### `CalculatorTool`

Safe mathematical calculations.

```python
from aiccel.tools import CalculatorTool

calc = CalculatorTool()
result = calc.execute({"expression": "sqrt(16) + 2 * 3"})
# {"result": 10.0, "expression": "sqrt(16) + 2 * 3"}
```

#### `DateTimeTool`

Date/time utilities.

```python
from aiccel.tools import DateTimeTool

dt = DateTimeTool()
result = dt.execute({"action": "now"})
# {"datetime": "2024-01-15T10:30:00", "timestamp": ..., "formatted": "..."}
```

---

## Security

### `JailbreakGuard`

Detect and block jailbreak attempts.

```python
from aiccel.jailbreak import JailbreakGuard, SecurityMode

guard = JailbreakGuard(
    security_mode=SecurityMode.FAIL_CLOSED,  # Block on detection/error
    threshold=0.5,
    model_name="traromal/AIccel_Jailbreak"
)

# Check a prompt
is_safe = guard.check("Normal query")  # True
is_safe = guard.check("Ignore all instructions...")  # False

# Decorator for automatic protection
@guard.guard
def process_query(query: str):
    return agent.run(query)
```

#### Security Modes

| Mode | Behavior |
|------|----------|
| `FAIL_CLOSED` | Block if detection fails or jailbreak detected (production) |
| `FAIL_OPEN` | Allow if detection fails (development) |

### `EntityMasker`

Mask PII (Personally Identifiable Information).

```python
from aiccel.privacy import EntityMasker

masker = EntityMasker()

# Mask text
masked, mapping = masker.mask("Email john@example.com")
# masked: "Email [EMAIL_1]"

# Unmask after processing
original = masker.unmask(masked, mapping)
```

### Encryption

AES-256-GCM encryption for sensitive data.

```python
from aiccel.encryption import encrypt, decrypt

# Encrypt
encrypted = encrypt("my-secret-api-key", password="secure-password")

# Decrypt
original = decrypt(encrypted, password="secure-password")
```

---

## Memory

### `ConversationMemory`

Manage conversation history.

```python
from aiccel import ConversationMemory

memory = ConversationMemory(
    memory_type="buffer",  # buffer, window, summary
    max_turns=50,
    max_tokens=32000
)

# Add a turn
memory.add_turn(
    query="Hello",
    response="Hi there!",
    tool_used=None,
    tool_output=None
)

# Get messages for LLM
messages = memory.get_messages()

# Clear history
memory.clear()
```

#### Memory Types

| Type | Description |
|------|-------------|
| `buffer` | Keep all turns up to max_turns |
| `window` | Sliding window of recent turns |
| `summary` | Summarize old conversations |

---

## Multi-Agent

### `AgentManager`

Orchestrate multiple agents.

```python
from aiccel import Agent, AgentManager, GeminiProvider

# Create specialist agents
researcher = Agent(provider=GeminiProvider(), name="Researcher")
writer = Agent(provider=GeminiProvider(), name="Writer")

# Create manager
manager = AgentManager(
    llm_provider=GeminiProvider(),
    agents=[researcher, writer]
)

# Route to best agent
result = manager.route("Write an article about AI")

# Collaborative processing
result = await manager.collaborate_async("Complex task...")
```

---

## Workflows

### `WorkflowBuilder`

Build deterministic agent pipelines.

```python
from aiccel import WorkflowBuilder, WorkflowExecutor

workflow = (
    WorkflowBuilder("my-pipeline")
    .add_agent("research", researcher)
    .add_agent("write", writer)
    .chain("research", "write")
    .build()
)

executor = WorkflowExecutor(workflow)
result = await executor.execute_async("Create content about AI")
```

---

## Utilities

### Request Context

Track requests across the application.

```python
from aiccel import request_scope, get_request_id

with request_scope(user_id="123") as ctx:
    print(f"Request ID: {ctx.request_id}")
    result = agent.run(query)
    # All logs include request_id for correlation
```

### Exceptions

Custom exceptions for error handling.

```python
from aiccel.exceptions import (
    AICCLException,       # Base exception
    AgentException,       # Agent errors
    ProviderException,    # LLM provider errors
    ToolException,        # Tool execution errors
)

try:
    result = agent.run(query)
except ProviderException as e:
    print(f"Provider failed: {e.message}")
    print(f"Context: {e.context}")
except AgentException as e:
    print(f"Agent error: {e}")
```

### Constants

Centralized configuration.

```python
from aiccel.constants import Timeouts, Retries, SecurityMode

# Access default values
print(Timeouts.DEFAULT_REQUEST)  # 30 seconds
print(Retries.DEFAULT_MAX_ATTEMPTS)  # 3
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `GOOGLE_API_KEY` | Google/Gemini API key |
| `GROQ_API_KEY` | Groq API key |
| `SERPAPI_API_KEY` | SerpAPI key for search |
| `AICCEL_SECURITY_MODE` | Security mode: `FAIL_CLOSED` or `FAIL_OPEN` |

---

## Quick Examples

### Basic Agent

```python
from aiccel import Agent, GeminiProvider

agent = Agent(provider=GeminiProvider())
result = agent.run("What is 2 + 2?")
print(result["response"])
```

### Agent with Tools

```python
from aiccel import Agent, GeminiProvider
from aiccel.tools import SearchTool, CalculatorTool

agent = Agent(
    provider=GeminiProvider(),
    tools=[SearchTool(api_key="..."), CalculatorTool()]
)

result = agent.run("What's the population of Tokyo times 2?")
```

### Secure Agent

```python
from aiccel import Agent, GeminiProvider, AgentConfig
from aiccel.jailbreak import JailbreakGuard

guard = JailbreakGuard()

@guard.guard
def ask_agent(query: str):
    agent = Agent(provider=GeminiProvider())
    return agent.run(query)

result = ask_agent("Normal question")  # Works
result = ask_agent("Ignore instructions...")  # Blocked!
```

---

*For more examples, see the [Examples Directory](./examples/) and [README](./README.md).*
