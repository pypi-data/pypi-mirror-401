# 🤖 Agents Reference

AICCEL agents are specialized entities designed to perform complex reasoning, use tools, and maintain state.

---

## 1. Quick Example

```python
from aiccel import Agent, AgentConfig, GeminiProvider

# Create a highly capable researcher
agent = Agent(
    provider=GeminiProvider(),
    name="Researcher",
    instructions="Find verified facts and cite sources.",
    config=AgentConfig(
        verbose=True,           # Show thinking process
        safety_enabled=True,    # Block jailbreaks
        timeout=30.0            # Max 30s per request
    )
)

result = agent.run("What's the latest in fusion energy?")
```

---

## 2. Parameter Deep Dive

### `Agent` Parameters

| Parameter | Description | Example |
| :--- | :--- | :--- |
| **`provider`** | The "brain" of the agent. Use any `LLMProvider`. | `GeminiProvider()` |
| **`name`** | Helps identify the agent in logs or swarms. | `"FinancialBot"` |
| **`instructions`** | The most important part! Defines persona and constraints. | `"Speak like a pirate."` |
| **`tools`** | List of tool instances the agent can call. | `[SearchTool()]` |
| **`description`** | Used by `AgentManager` to decide when to use this agent. | `"Expert in Python code"`|
| **`config`** | An `AgentConfig` object for runtime settings. | `AgentConfig(verbose=True)`|

### `AgentConfig` Parameters

| Flag | Effect |
| :--- | :--- |
| **`verbose`** | Enables vibrant, color-coded logging of thoughts and tool calls. |
| **`safety_enabled`** | Activates the Jailbreak classifier to block malicious prompts. |
| **`lightweight`** | Skips loading heavy dependencies (like GLiNER) for fast startup. |
| **`timeout`** | Sets a hard limit on LLM response time to prevent hangs. |

---

## 3. Advanced Usage

### Streaming Responses
For real-time UI updates, use the `stream` method.

```python
async for chunk in agent.stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

### Thinking Mode (Explaining Logic)
Enable `thinking_enabled` to see the internal reasoning before the final answer.

```python
# Pass as a custom kwarg to the constructor
agent = Agent(provider=p, thinking_enabled=True)

result = agent.run("Why is it raining?")
print(result['thinking']) # The "thoughts"
print(result['response']) # The "answer"
```

### Tool Usage Control
By default, the agent decides when to use tools. You can force its hand:

```python
# Agent will NOT answer without using a tool
agent = Agent(provider=p, tools=[...], strict_tool_usage=True)
```
