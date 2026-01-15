# Advanced Agent Patterns

Deep dive into creating powerful AI agents with AICCEL.

---

## Agent Types

### 1. Simple Agent

For basic Q&A:

```python
from aiccel import Agent, GeminiProvider

agent = Agent(
    provider=GeminiProvider(api_key="...", model="gemini-2.5-flash"),
    name="SimpleAgent",
    instructions="Answer questions accurately and concisely."
)

result = agent.run("What is Python?")
```

### 2. Tool-Using Agent

For tasks requiring external data:

```python
from aiccel import Agent, GeminiProvider, SearchTool, WeatherTool

agent = Agent(
    provider=GeminiProvider(api_key="...", model="gemini-2.5-flash"),
    tools=[
        SearchTool(api_key="serper-key"),
        WeatherTool(api_key="weather-key")
    ],
    name="AssistantAgent",
    instructions="""You are a helpful assistant that can:
- Search the web for current information
- Get weather forecasts
Use tools when needed. Provide accurate, sourced information."""
)

# Agent automatically decides when to use tools
result = agent.run("What's the weather in Tokyo and what events are happening there?")
```

### 3. Thinking Agent

For complex reasoning:

```python
agent = Agent(
    provider=provider,
    name="ReasoningAgent",
    instructions="Think step by step. Analyze complex problems carefully."
)

# Enable thinking mode
agent.enable_thinking(True)

result = agent.run("If a train leaves Chicago at 9am going 60mph...")

print("Thinking:", result["thinking"])
print("Answer:", result["response"])
```

### 4. Specialist Agent

Focused on one domain:

```python
code_agent = Agent(
    provider=provider,
    name="CodeExpert",
    instructions="""You are an expert Python programmer.
- Write clean, documented code
- Follow PEP 8 guidelines
- Include error handling
- Explain your code clearly"""
)

legal_agent = Agent(
    provider=provider,
    name="LegalExpert",
    instructions="""You are a legal expert.
- Provide accurate legal information
- Cite relevant laws when applicable
- Always recommend consulting a lawyer for specific cases
- Be clear about jurisdiction limitations"""
)
```

### 5. Conversational Agent

For multi-turn conversations:

```python
agent = Agent(
    provider=provider,
    name="ChatBot",
    instructions="""You are a friendly conversational assistant.
- Remember context from the conversation
- Ask clarifying questions when needed
- Be personable but professional""",
    memory_type="buffer",
    max_memory_turns=20,
    max_memory_tokens=8000
)

# Multi-turn conversation
agent.run("Hi, I'm Alex")
agent.run("What's a good programming language to learn?")
agent.run("Why did you recommend that one?")  # Remembers context
```

---

## Custom Agent Classes

### Extending Agent

```python
from aiccel import Agent

class ResearchAgent(Agent):
    """Agent specialized for research tasks."""

    def __init__(self, provider, **kwargs):
        super().__init__(
            provider=provider,
            name="ResearchAgent",
            instructions="""You are a research specialist.
- Search for accurate, recent information
- Cite sources when possible
- Synthesize findings clearly""",
            **kwargs
        )
        self.research_history = []

    def research(self, topic: str) -> dict:
        """Conduct research on a topic."""
        result = self.run(f"Research this topic thoroughly: {topic}")
        self.research_history.append({
            "topic": topic,
            "findings": result["response"]
        })
        return result

    def get_history(self) -> list:
        return self.research_history

# Usage
researcher = ResearchAgent(provider, tools=[SearchTool(api_key="...")])
result = researcher.research("Quantum computing advances in 2024")
```

### Extending SlimAgent

```python
from aiccel import SlimAgent
from aiccel.autonomous import ReflectionMixin

class LearningAgent(SlimAgent, ReflectionMixin):
    """Agent that learns from its mistakes."""

    def __init__(self, provider, **kwargs):
        super().__init__(provider=provider, **kwargs)
        self.enable_reflection(max_memories=100)

    async def run_and_learn(self, query: str) -> dict:
        try:
            result = await self.run_async(query)

            # Learn from success
            self.reflect(
                action=query,
                outcome=result["response"],
                success=True,
                learnings=["This approach worked"]
            )

            return result

        except Exception as e:
            # Learn from failure
            self.reflect(
                action=query,
                outcome=str(e),
                success=False,
                learnings=[f"Failed due to: {e}"]
            )
            raise
```

---

## Agent Personalities

Create agents with distinct personalities:

```python
# Friendly helper
friendly_agent = Agent(
    provider=provider,
    name="FriendlyHelper",
    instructions="""You are a warm, friendly assistant named Alex.
- Use casual, approachable language
- Add appropriate emojis occasionally 😊
- Be encouraging and supportive
- Remember to ask how the user is doing"""
)

# Professional analyst
analyst_agent = Agent(
    provider=provider,
    name="Analyst",
    instructions="""You are a professional business analyst.
- Use formal, precise language
- Support claims with data
- Structure responses with clear headings
- Avoid speculation; state uncertainties clearly"""
)

# Creative writer
creative_agent = Agent(
    provider=provider,
    name="CreativeWriter",
    instructions="""You are a creative writing assistant.
- Use vivid, descriptive language
- Employ literary devices when appropriate
- Match the tone and style requested
- Offer creative alternatives and suggestions"""
)
```

---

## Agent with Custom Tools

Create domain-specific tools:

```python
from aiccel import Agent, GeminiProvider
from aiccel.tools_unified import BaseTool, ToolParameter

class DatabaseQueryTool(BaseTool):
    _name = "query_database"
    _description = "Query the company database for information"
    _parameters = [
        ToolParameter(name="query", type="string", description="SQL query or natural language question"),
        ToolParameter(name="table", type="string", description="Table name", required=False)
    ]

    def __init__(self, connection_string: str):
        super().__init__()
        self.connection_string = connection_string

    def execute(self, query: str, table: str = None) -> str:
        # Your database logic here
        return f"Results for: {query}"


class EmailSenderTool(BaseTool):
    _name = "send_email"
    _description = "Send an email to a recipient"
    _parameters = [
        ToolParameter(name="to", type="string", description="Recipient email", required=True),
        ToolParameter(name="subject", type="string", description="Email subject", required=True),
        ToolParameter(name="body", type="string", description="Email body", required=True)
    ]

    def execute(self, to: str, subject: str, body: str) -> str:
        # Your email logic here
        return f"Email sent to {to}"


class SlackNotifierTool(BaseTool):
    _name = "notify_slack"
    _description = "Send a notification to a Slack channel"
    _parameters = [
        ToolParameter(name="channel", type="string", description="Slack channel"),
        ToolParameter(name="message", type="string", description="Message to send")
    ]

    def __init__(self, webhook_url: str):
        super().__init__()
        self.webhook_url = webhook_url

    def execute(self, channel: str, message: str) -> str:
        import requests
        requests.post(self.webhook_url, json={"channel": channel, "text": message})
        return f"Sent to #{channel}"


# Create agent with custom tools
business_agent = Agent(
    provider=GeminiProvider(api_key="...", model="gemini-2.5-flash"),
    tools=[
        DatabaseQueryTool(connection_string="..."),
        EmailSenderTool(),
        SlackNotifierTool(webhook_url="...")
    ],
    name="BusinessAgent",
    instructions="""You are a business automation agent.
- Query databases for business data
- Send emails when requested
- Notify Slack for important updates
- Always confirm before taking actions"""
)
```

---

## Multi-Agent Collaboration

### Agent Manager

Route queries to specialist agents:

```python
from aiccel import Agent, AgentManager, GeminiProvider

provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")

# Create specialist agents
code_agent = Agent(provider=provider, name="CodeExpert",
                   instructions="You are an expert programmer.")
writing_agent = Agent(provider=provider, name="Writer",
                      instructions="You are a professional writer.")
research_agent = Agent(provider=provider, name="Researcher",
                       tools=[SearchTool(api_key="...")],
                       instructions="Research topics thoroughly.")

# Create manager
manager = AgentManager(routing_provider=provider)
manager.add_agent(code_agent, "code_expert", "Handles programming questions")
manager.add_agent(writing_agent, "writer", "Handles writing tasks")
manager.add_agent(research_agent, "researcher", "Handles research queries")

# Manager automatically routes to best agent
result = manager.route("Write a Python function to sort a list")  # -> code_expert
result = manager.route("Research AI trends in healthcare")         # -> researcher
result = manager.route("Write a blog post about travel")          # -> writer
```

### Agent Handoff

Pass context between agents:

```python
# Agent 1 does research
research_result = research_agent.run("Research sustainable energy trends")

# Agent 2 writes based on research
writing_result = writing_agent.run(
    f"Write an article based on this research: {research_result['response']}"
)

# Agent 3 reviews
review_result = review_agent.run(
    f"Review this article for accuracy: {writing_result['response']}"
)
```

---

## Agent Configuration Patterns

### Environment-Based Config

```python
import os

class AgentFactory:
    @staticmethod
    def create_agent(agent_type: str) -> Agent:
        provider = GeminiProvider(
            api_key=os.environ["GOOGLE_API_KEY"],
            model=os.environ.get("MODEL", "gemini-2.5-flash")
        )

        configs = {
            "research": {
                "name": "Researcher",
                "instructions": "Research topics thoroughly.",
                "tools": [SearchTool(api_key=os.environ.get("SERPER_KEY", ""))]
            },
            "coder": {
                "name": "Coder",
                "instructions": "Write clean, documented code.",
                "tools": []
            },
            "assistant": {
                "name": "Assistant",
                "instructions": "Be helpful and friendly.",
                "tools": []
            }
        }

        config = configs.get(agent_type, configs["assistant"])
        return Agent(provider=provider, **config)

# Usage
agent = AgentFactory.create_agent("research")
```

### Config File

```python
import yaml

# config.yaml:
# agents:
#   research:
#     name: Researcher
#     instructions: Research topics thoroughly.
#     tools: [search]
#   coder:
#     name: Coder
#     instructions: Write clean code.

def load_agent_from_config(config_path: str, agent_name: str) -> Agent:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    agent_config = config["agents"][agent_name]

    # Build tools
    tools = []
    for tool_name in agent_config.get("tools", []):
        if tool_name == "search":
            tools.append(SearchTool(api_key=os.environ["SERPER_KEY"]))

    return Agent(
        provider=provider,
        name=agent_config["name"],
        instructions=agent_config["instructions"],
        tools=tools
    )
```

---

## Best Practices

### 1. Clear Instructions

```python
# ❌ Vague
agent = Agent(provider=provider, instructions="Be helpful")

# ✅ Specific
agent = Agent(provider=provider, instructions="""You are a customer support agent for TechCorp.
- Answer questions about our products
- Offer solutions to common problems
- Escalate complex issues to human support
- Always be polite and professional
- Never make up information about products""")
```

### 2. Tool Selection

```python
# ❌ Too many tools
agent = Agent(provider=provider, tools=[tool1, tool2, tool3, tool4, tool5, tool6, tool7, tool8])

# ✅ Focused tools (3-5 is optimal)
agent = Agent(provider=provider, tools=[search_tool, weather_tool, calculator_tool])
```

### 3. Error Handling

```python
from aiccel.errors import AgentError, ProviderError, ToolError

async def safe_agent_call(agent: Agent, query: str) -> dict:
    try:
        return await agent.run_async(query)
    except ProviderError as e:
        return {"error": f"LLM unavailable: {e}", "fallback": True}
    except ToolError as e:
        return {"error": f"Tool failed: {e}", "partial": True}
    except AgentError as e:
        return {"error": f"Agent error: {e}"}
```

### 4. Memory Management

```python
# Clear memory for new conversations
agent.clear_memory()

# Export memory before clearing
conversation = agent.get_memory()
save_to_database(conversation)
agent.clear_memory()
```

---

## Next Steps

- [Agent Workflows](./agent-workflows.md) - Chain agents together
- [Multi-Agent Systems](./multi-agent.md) - Complex agent orchestration
- [MCP Integration](./mcp.md) - Model Context Protocol
