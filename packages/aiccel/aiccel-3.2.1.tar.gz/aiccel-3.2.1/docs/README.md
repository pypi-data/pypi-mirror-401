# AICCEL Framework Documentation

<p align="center">
  <strong>🚀 The Best-in-Class AI Agent Framework for Python</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#examples">Examples</a> •
  <a href="#api-reference">API Reference</a>
</p>

---

## Overview

**AICCEL** is a production-ready AI agent framework that makes building intelligent agents simple, fast, and secure.

### Why AICCEL?

| Feature | AICCEL | LangChain | AutoGPT |
|---------|--------|-----------|---------|
| **Simple API** | ✅ 3 lines to start | ❌ Complex chains | ❌ Heavy setup |
| **Multi-Provider** | ✅ OpenAI, Gemini, Groq | ✅ | ❌ OpenAI only |
| **Workflows** | ✅ DAG-based | ⚠️ LCEL only | ❌ |
| **Security** | ✅ Built-in encryption | ❌ | ❌ |
| **Autonomous** | ✅ Goal-driven agents | ⚠️ | ✅ |
| **Fast Startup** | ✅ Lazy loading | ❌ Heavy | ❌ Heavy |

---

## Installation

```bash
pip install aiccel
```

### Optional Dependencies

```bash
# For encryption features
pip install cryptography

# For PDF RAG
pip install PyPDF2 chromadb

# For FastAPI integration
pip install fastapi uvicorn
```

---

## Quick Start

### 1. Basic Agent

```python
from aiccel import Agent, GeminiProvider

# Create provider
provider = GeminiProvider(
    api_key="your-api-key",
    model="gemini-2.5-flash"
)

# Create agent
agent = Agent(
    provider=provider,
    name="MyAgent",
    instructions="You are a helpful assistant."
)

# Run
result = agent.run("What is the capital of France?")
print(result["response"])
```

### 2. Agent with Tools

```python
from aiccel import Agent, GeminiProvider, SearchTool, WeatherTool

provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
search = SearchTool(api_key="serper-api-key")
weather = WeatherTool(api_key="openweather-api-key")

agent = Agent(
    provider=provider,
    tools=[search, weather],
    name="AssistantAgent"
)

result = agent.run("What's the weather in Tokyo?")
```

### 3. Multi-Agent System

```python
from aiccel import Agent, AgentManager, GeminiProvider

provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")

# Create specialized agents
search_agent = Agent(provider=provider, name="Searcher", tools=[SearchTool(...)])
writer_agent = Agent(provider=provider, name="Writer", instructions="Write clearly.")

# Create manager
manager = AgentManager(routing_provider=provider)
manager.add_agent(search_agent, "search_expert", "Handles web searches")
manager.add_agent(writer_agent, "writer_expert", "Writes content")

# Route automatically
result = manager.route("Find info about AI and write a summary")
```

---

## Features

### 📦 Core Components
- [Agents (Implementation Guide)](./agents.md) - **Detailed Parameter Reference** & Configuration
- [Advanced Agents](./advanced-agents.md) - Custom agents, personalities, patterns
- [Providers](./providers.md) - LLM providers (OpenAI, Gemini, Groq)
- [Tools](./tools.md) - Built-in and custom tools

### 🔒 Security (New v3.0)
- [Security Guide](./security.md) - **Jailbreak Detection**, PII Masking, & Encryption
- [Privacy](./security.md#pii-masking-data-privacy) - GLiNER-based redaction

### 🤝 Multi-Agent
- [Multi-Agent Systems](./multi-agent.md) - Agent teams and collaboration
- [Agent Workflows](./agent-workflows.md) - DAG-based orchestration
- [Workflow Patterns](./workflows.md) - Common workflow patterns

### 🤖 Autonomous
- [Autonomous Agents](./autonomous.md) - Goal-driven execution
- [Task Planner](./autonomous.md#taskplanner) - AI task decomposition
- [Self-Reflection](./autonomous.md#self-reflection) - Learning from mistakes

### 🔌 Integrations
- [MCP (Model Context Protocol)](./mcp.md) - Connect to external tools
- [FastAPI](./integrations.md#fastapi-integration) - REST API endpoints
- [LangChain](./integrations.md#langchain-integration) - Bi-directional compatibility
- [Webhooks](./integrations.md#webhook-integration) - External triggers

### 🔒 Security
- [Encryption](./security.md#encryption) - AES-256 encryption
- [Privacy](./security.md#privacy---pii-masking) - PII masking

### ⚡ Performance
- [Middleware](./middleware.md) - Extensible pipeline
- [Quick Reference](./quickstart.md) - Cheat sheet

---

## Examples

See the [examples/](../examples/) directory for complete examples:

- `basic_agent.py` - Simple agent usage
- `multi_agent.py` - Multi-agent orchestration
- `workflow_example.py` - Workflow builder
- `autonomous_example.py` - Goal-driven agent
- `fastapi_server.py` - REST API server

---

## Support

- 📖 [Full Documentation](./docs/)
- 🐛 [Report Issues](https://github.com/your-repo/aiccel/issues)
- 💬 [Discussions](https://github.com/your-repo/aiccel/discussions)

---

## License

MIT License - see [LICENSE](../LICENSE) for details.
