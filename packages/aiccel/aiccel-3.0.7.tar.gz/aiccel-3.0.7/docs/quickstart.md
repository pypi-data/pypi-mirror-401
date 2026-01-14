# AICCEL Quick Reference

## Installation

```bash
pip install aiccel
```

---

## Basic Agent

```python
from aiccel import Agent, GeminiProvider

provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
agent = Agent(provider=provider, name="MyAgent")
result = agent.run("Hello!")
```

---

## Agent with Tools

```python
from aiccel import Agent, SearchTool, WeatherTool

agent = Agent(
    provider=provider,
    tools=[SearchTool(api_key="..."), WeatherTool(api_key="...")]
)
```

---

## Async Agent

```python
result = await agent.run_async("Question")

async for chunk in agent.stream("Tell me a story"):
    print(chunk)
```

---

## Multi-Agent Manager

```python
from aiccel import AgentManager

manager = AgentManager(routing_provider=provider)
manager.add_agent(agent1, "expert1", "Description")
manager.add_agent(agent2, "expert2", "Description")

result = manager.route("Complex query")
```

---

## Workflows

```python
from aiccel import WorkflowBuilder, WorkflowExecutor

workflow = (
    WorkflowBuilder("pipeline")
    .add_agent("step1", agent1)
    .add_agent("step2", agent2)
    .chain("step1", "step2")
    .build()
)

result = await WorkflowExecutor().run(workflow, {"query": "..."})
```

---

## Autonomous Goals

```python
from aiccel import GoalAgent, Goal

agent = GoalAgent(provider=provider, tools=[...])
agent.add_goal(Goal(
    id="task1",
    description="Do something",
    success_criteria="Verify it worked"
))

results = await agent.run_until_complete()
```

---

## Middleware

```python
from aiccel import create_default_pipeline, RateLimitMiddleware

pipeline = create_default_pipeline()
pipeline.use(RateLimitMiddleware(requests_per_minute=30))
```

---

## FastAPI

```python
from aiccel.integrations import create_agent_routes
router = create_agent_routes(agent=agent)
app.include_router(router)
```

---

## Privacy

```python
from aiccel import mask_text, unmask_text

masked = mask_text("Email: john@test.com")  # "Email: [EMAIL_1]"
original = unmask_text(masked)
```

---

## Encryption

```python
from aiccel import encrypt, decrypt, generate_key

key = generate_key()
encrypted = encrypt("secret", key)
decrypted = decrypt(encrypted, key)
```

---

## Logging

```python
from aiccel import configure_logging
import logging

configure_logging(level=logging.INFO, quiet_internal=True)
```

---

## Environment Variables

```bash
GOOGLE_API_KEY=your-key
OPENAI_API_KEY=your-key
SERPER_API_KEY=your-key
```

---

## Providers

| Provider | Import | Model Examples |
|----------|--------|----------------|
| Gemini | `GeminiProvider` | gemini-2.5-flash, gemini-pro |
| OpenAI | `OpenAIProvider` | gpt-4o, gpt-4, gpt-3.5-turbo |
| Groq | `GroqProvider` | llama3-70b-8192, mixtral |

---

## Links

- [Full Documentation](./README.md)
- [Agents](./agents.md)
- [Tools](./tools.md)
- [Workflows](./workflows.md)
- [Autonomous](./autonomous.md)
- [Integrations](./integrations.md)
- [Middleware](./middleware.md)
- [Security](./security.md)
