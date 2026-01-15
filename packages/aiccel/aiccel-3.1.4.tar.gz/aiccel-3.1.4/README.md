# ⚡ AICCEL Framework 3.1: The Production-Grade Agentic Library

**AICCEL (AI-Accelerated Agentic Library)** is a high-performance, security-first framework for building orchestrated AI systems.

[![PyPI version](https://badge.fury.io/py/aiccel.svg)](https://badge.fury.io/py/aiccel)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---


## 📦 Installation

AICCEL is modular. Install only what you need.

```bash
pip install aiccel             # Core (OpenAI, Gemini, Groq support)
pip install aiccel[safety]     # Jailbreak Guard (Transformers)
pip install aiccel[privacy]    # PII Masking (GLiNER)
pip install aiccel[all]        # Full Suite (Security, Data, RAG)
```

**Verify your environment:**

```bash
aiccel check
```

---

## 🏗️ 1. Building High-Performance Agents

The `Agent` is the core building block. It uses an internal **ExecutionPlanner** to determine strategies before acting.

```python
from aiccel import Agent, GeminiProvider, SearchTool

# 1. Setup Provider & Tools
provider = GeminiProvider(api_key="...", model="gemini-2.0-flash")
search = SearchTool(api_key="...")

# 2. Build the Agent
agent = Agent(
    provider=provider,
    tools=[search],
    name="ResearchAgent",
    instructions="You are a precise technical researcher."
)

# 3. Execution
result = agent.run("What are the latest breakthroughs in battery tech?")

print(f"Thought: {result['thinking']}")
print(f"Answer: {result['response']}")
```

### ⚙️ Feature: Thinking & Planning
AICCEL Agents have a "Think-before-you-act" mode. When `thinking_enabled=True`, the agent uses a separate planning pass to structure its tool usage, resulting in much higher accuracy for complex tasks.

---

## 🛡️ 2. Enterprise Security Suite

### 🕵️ PII Masking (`aiccel.privacy`)
Automatically detects and masks sensitive data (Emails, Phones, Names) using GLiNER before it hits the LLM.

```python
from aiccel.privacy import mask_text

# Mask data
result = mask_text("Contact John at john.doe@example.com")
# Output: "Contact [PERSON_1] at [EMAIL_1]"

# Mapping is kept locally to unmask the response later.
```

### 🛑 Jailbreak Guard
Protect your system from malicious prompt injections.
```python
from aiccel import AgentConfig
config = AgentConfig(safety_enabled=True) # Blocks attacks automatically
```

### 🔐 Secure Vault & Encryption
Military-grade AES-256-GCM encryption for managing API keys and secrets.
```python
from aiccel.encryption import encrypt, decrypt
encrypted = encrypt("my-secret-key", "strong-password")
```

---

## 🎼 3. Multi-Agent Orchestration

### 🤝 AgentManager
Coordinate specialist agents to solve problems that are too big for one LLM.

```python
from aiccel.manager import AgentManager

# Create a expert team
manager = AgentManager(
    llm_provider=provider,
    agents=[research_agent, math_agent, writer_agent]
)

# Collaborative reasoning
response = await manager.collaborate_async("Analyze this fiscal report and summarize findings.")
```

### ⛓️ Workflow DAGs
Build deterministic pipelines with loops and conditional routing.

```python
from aiccel import WorkflowBuilder

workflow = (WorkflowBuilder("pipeline")
    .add_agent("research", researcher)
    .add_agent("write", writer)
    .chain("research", "write")
    .build())
```

---

## 🔬 4. Advanced Utilities

*   **Neural Reranking**: Advanced semantic sorting for RAG applications.
*   **MCP Support**: Native **Model Context Protocol** client to connect to thousands of external tools.
*   **Autonomous Goal Agents**: Agents that can break down a high-level goal into a dynamic task list.

---

## 📖 Full Documentation
Visit our [Documentation Directory](./docs/README.md) for specialized guides:
* [🚀 Quickstart Guide](./docs/quickstart.md)
* [🤖 Deep Dive: Agents](./docs/agents.md)
* [🛡️ Security & Privacy Full Guide](./docs/security.md)
* [⛓️ Building Complex Workflows](./docs/agent-workflows.md)


