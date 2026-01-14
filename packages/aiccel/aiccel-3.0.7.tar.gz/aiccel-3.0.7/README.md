# AICCEL Framework 3.0: The Complete Implementation Guide

**AICCEL (AI-Accelerated Agentic Library)** is a production-grade Python framework designed for building secure, high-performance, and orchestrated AI systems. Unlike other frameworks that suffer from bloat and complexity, AICCEL focuses on **modularity**, **speed (~50ms startup)**, and **security-first** architecture.

This guide provides a comprehensive review of the framework's capabilities and serves as the definitive manual for implementing autonomous agents using AICCEL.

---

## 📦 Installation

AICCEL is modular. Install only what you need to keep your deployment lightweight.

```bash
# 🚀 Core Framework (Lightweight)
pip install aiccel

# 🛡️ Production Security (Jailbreak Detection & Transformers)
pip install aiccel[safety]

# 🕵️‍♀️ Privacy Suite (PII Masking with GLiNER)
pip install aiccel[privacy]

# 📦 The Full Suite (Recommended for Dev)
pip install aiccel[all]
```

---

## 🏗️ Building Agents: The Core

The `Agent` class is the fundamental unit of AICCEL. It encapsulates the LLM, memory, tools, and execution logic.

### Minimal Implementation
```python
from aiccel import Agent, GeminiProvider

# 1. Initialize Provider
provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")

# 2. Create Agent
agent = Agent(provider=provider, instructions="You are a helpful assistant.")

# 3. Run
print(agent.run("Hello world!")["response"])
```

### 🔧 Comprehensive Configuration

AICCEL `Agent`s are highly configurable. You can pass parameters to control behavior, memory, and security.

```python
agent = Agent(
    # --- Core Components ---
    provider=provider,                  # The LLM backend (Gemini/OpenAI/Groq)
    tools=[search_tool, weather_tool],  # List of capabilities
    
    # --- Identity & Behavior ---
    name="AnalystBot",                  # ID for logging & orchestration
    description="Analyzes market data", # Used by Manager for routing decisions
    instructions="Be precise and concise.", # System Prompt / Persona
    
    # --- Memory Management ---
    memory_type="summary",              # Strategies: 'buffer', 'summary', 'window', 'none'
    max_memory_turns=20,                # How many exchanges to keep
    max_memory_tokens=4000,             # Hard limit on context window
    
    # --- Execution Constraints ---
    strict_tool_usage=False,            # If True, MUST use a tool for every reply
    timeout=60.0,                       # Execution timeout in seconds
    verbose=True,                       # Enable rich console logging
    
    # --- Advanced / Custom (Automatic **kwargs support) ---
    thinking_enabled=True,              # Enable Chain-of-Thought (if supported)
    custom_tag="finance-dept",          # Custom metadata attached to config
    knowledge_base_id="kb-123"          # Any custom param you need for extensions
)
```

#### Parameter Reference Table

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `provider` | `LLMProvider` | **Required** | The intelligence backend. |
| `name` | `str` | `"Agent"` | The agent's identifier. Critical for multi-agent routing. |
| `instructions`| `str` | `""` | The "Soul" of the agent. Defines persona and constraints. |
| `tools` | `List[Tool]` | `[]` | Tools the agent can invoke (Search, Calculator, API, etc.). |
| `memory_type` | `str` | `"buffer"` | `'buffer'` (full history), `'summary'` (LLM summarized), `'window'` (last N), `'none'` (stateless). |
| `verbose` | `bool` | `False` | Prints thinking process, tool calls, and debug info. |
| `**kwargs` | `Any` | - | **New in 3.0.3**: Any extra arguments are automatically stored in `agent.config`. |

---

## 🎼 Orchestration: The Agent Manager

For complex tasks, use `AgentManager` to route queries to specialized agents or have them collaborate.

```python
from aiccel import AgentManager

# Define specialized agents
researcher = Agent(name="Researcher", instructions="Search for facts.", tools=[search])
writer = Agent(name="Writer", instructions="Write engaging posts.")

# Initialize Manager
manager = AgentManager(
    llm_provider=provider,
    agents=[researcher, writer],
    verbose=True,
    instructions="You are a project manager. Route tasks efficiently."
)

# 1. Routing (Selects ONE best agent)
# "Route queries to the most appropriate agent based on expertise."
response = manager.route("Find the latest stock price of AAPL") 

# 2. Collaboration (Splits task across multiple agents)
# "Analyze query, split into sub-tasks, execute in parallel, and synthesize."
response = manager.collaborate("Research quantum computing and write a short poem about it.")
```

---

## 🛡️ Security & Production Readiness (New in v3.0)

AICCEL 3.0 introduces an industry-leading security suite.

### 1. Jailbreak Detection (`aiccel[safety]`)
Automatically blocks malicious prompts designed to bypass instructions (e.g., "Ignore previous instructions").

*   **How to enable**: Install with `[safety]` or `[all]`.
*   **Behavior**: The `Agent.run()` method automatically checks input against a Transformer-based guardrail model (`traromal/AIccel_Jailbreak`).
*   **Manual Check**:
    ```python
    from aiccel.jailbreak import check_prompt
    if not check_prompt(user_input):
        raise SecurityError("Unsafe input detected!")
    ```

### 2. PII Masking (`aiccel[privacy]`)
Prevents sensitive data (Email, Phone, Names) from ever reaching the LLM provider. Uses GLiNER for high-accuracy Named Entity Recognition.

```python
from aiccel.privacy import mask_text, unmask_text

# 1. Mask Input
sensitive_input = "Contact John Doe at 555-0199."
result = mask_text(sensitive_input, remove_person=True, remove_phone=True)

print(result['masked_text']) 
# Output: "Contact PERSON_8a2f at PHONE_9b1c."

# 2. Send to Agent (Agent sees only masked text)
agent_response = agent.run(result['masked_text'])

# 3. Unmask Response (Restore real names)
final_output = unmask_text(agent_response['response'], result['mask_mapping'])
```

### 3. Pandora Sandbox
`Pandora` is AICCEL's data engineering agent. It writes and executes code to transform Pandas DataFrames.

*   **Security Update**: Pandora now includes input validation to prevent arbitrary code injection instructions.
*   **Usage**:
    ```python
    from aiccel.pandora import Pandora
    
    pandora = Pandora(llm=provider)
    # Safe execution loop with retry & self-correction
    clean_df = pandora.do(dirty_df, "Clean the 'price' column and convert to float")
    ```

---

## 🔌 API Reference & Extensibility

### Supported LLM Providers
*   `GeminiProvider(api_key, model)`
*   `OpenAIProvider(api_key, model)`
*   `GroqProvider(api_key, model)`

### Defining Custom Tools
Subclass `Tool` to give agents new capabilities.

```python
from aiccel import Tool

class MyTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_monitor",
            description="Checks system status. Returns 'OK' or 'ERROR'.",
            parameters={"target": "str"} # JSON Schema definition
        )

    def execute(self, target: str):
        return f"Status of {target}: OK"
```

---

*Built with ❤️ by the AICCEL Team.*