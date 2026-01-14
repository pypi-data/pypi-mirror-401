# Integrations

AICCEL integrates with popular frameworks and services.

---

## FastAPI Integration

Create REST API endpoints for your agents:

```python
from fastapi import FastAPI
from aiccel import SlimAgent, GeminiProvider
from aiccel.integrations import create_agent_routes

# Create agent
provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
agent = SlimAgent(provider=provider, name="APIAgent")

# Create FastAPI app
app = FastAPI(title="AI Agent API")

# Add agent routes
router = create_agent_routes(agent=agent, prefix="/api/agent")
app.include_router(router)

# Run: uvicorn main:app --reload
```

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/agent/run` | POST | Run agent with query |
| `/api/agent/stream` | POST | Stream response |
| `/api/agent/health` | GET | Health check |
| `/api/agent/info` | GET | Agent information |
| `/api/agent/memory` | DELETE | Clear memory |

### Request/Response

```python
# POST /api/agent/run
# Request:
{
    "query": "What is AI?",
    "context": {"user_id": "123"}  # Optional
}

# Response:
{
    "response": "AI is...",
    "thinking": null,
    "tools_used": [],
    "execution_time": 1.234
}
```

### Workflow Routes

```python
from aiccel.integrations import create_workflow_routes

workflow_router = create_workflow_routes(
    workflow=my_workflow,
    prefix="/api/workflow"
)
app.include_router(workflow_router)

# POST /api/workflow/run
# GET /api/workflow/info
```

---

## LangChain Integration

### Use AICCEL Agent as LangChain Tool

```python
from aiccel import SlimAgent, GeminiProvider
from aiccel.integrations import LangChainAdapter

# Create AICCEL agent
agent = SlimAgent(
    provider=GeminiProvider(api_key="..."),
    name="ExpertAgent"
)

# Convert to LangChain tool
lc_tool = LangChainAdapter.as_tool(
    agent,
    name="expert_agent",
    description="Consult with AI expert"
)

# Use in LangChain chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

chain = ChatPromptTemplate.from_template("{input}") | lc_tool
result = chain.invoke({"input": "Explain transformers"})
```

### Use AICCEL Agent as LangChain Runnable

```python
runnable = LangChainAdapter.as_runnable(agent)

# Use in LCEL chains
from langchain_core.output_parsers import StrOutputParser

chain = runnable | StrOutputParser()
result = await chain.ainvoke("Question")
```

### Use LangChain LLM in AICCEL

```python
from langchain_openai import ChatOpenAI
from aiccel.integrations import LangChainAdapter
from aiccel import SlimAgent

# Create LangChain LLM
lc_llm = ChatOpenAI(model="gpt-4")

# Convert to AICCEL provider
provider = LangChainAdapter.from_langchain_llm(lc_llm)

# Use in AICCEL
agent = SlimAgent(provider=provider, name="LangChainPowered")
result = await agent.run_async("Hello!")
```

---

## OpenAI Function Calling

Convert AICCEL tools to OpenAI function format:

```python
from aiccel import SearchTool, WeatherTool
from aiccel.integrations import OpenAIFunctionsAdapter
from openai import OpenAI

# Create adapter
adapter = OpenAIFunctionsAdapter(tools=[
    SearchTool(api_key="..."),
    WeatherTool(api_key="...")
])

# Get functions in OpenAI format
functions = adapter.get_functions()

# Use with OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in NYC?"}],
    functions=functions,
    function_call="auto"
)

# Execute tool calls
if response.choices[0].message.function_call:
    result = adapter.execute_call(
        response.choices[0].message.function_call
    )
    print(result)
```

### New Tools Format

```python
# Get tools in new format
tools = adapter.get_tools_format()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    tools=tools,
    tool_choice="auto"
)

# Execute multiple tool calls
results = adapter.execute_tool_calls(response.choices[0].message.tool_calls)
```

---

## Webhook Integration

Trigger agents from external services:

```python
from aiccel import SlimAgent, GeminiProvider
from aiccel.integrations import WebhookTrigger
from fastapi import FastAPI, Request

agent = SlimAgent(provider=GeminiProvider(api_key="..."))

# Create webhook trigger
trigger = WebhookTrigger(
    agent=agent,
    secret="webhook_secret_key",  # For signature verification
    input_extractor=lambda data: data.get("text", "")
)

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.body()
    headers = dict(request.headers)
    
    result = await trigger.handle(payload, headers)
    return result
```

### Supported Webhook Formats

Auto-extracts query from:
- **GitHub** - Repository events
- **Slack** - Messages
- **Discord** - Messages
- **Generic JSON** - `query`, `message`, or `text` fields

### Custom Input Extraction

```python
def extract_github_issue(data: dict) -> str:
    if data.get("action") == "opened":
        issue = data.get("issue", {})
        return f"New issue: {issue.get('title')} - {issue.get('body')}"
    return ""

trigger = WebhookTrigger(
    agent=agent,
    input_extractor=extract_github_issue
)
```

---

## MCP (Model Context Protocol)

Use MCP for standardized tool interfaces:

```python
from aiccel.mcp import MCPClient, MCPServer, MCPToolAdapter

# Connect to MCP server
client = MCPClient("http://localhost:8080")

# Get tools from MCP
mcp_tools = client.get_tools()

# Adapt MCP tools for AICCEL
adapted_tools = [MCPToolAdapter(tool) for tool in mcp_tools]

# Use in agent
agent = Agent(provider=provider, tools=adapted_tools)
```

---

## Environment Variables

Store credentials securely:

```python
import os
from aiccel import GeminiProvider, SearchTool

provider = GeminiProvider(
    api_key=os.environ.get("GOOGLE_API_KEY"),
    model="gemini-2.5-flash"
)

search = SearchTool(api_key=os.environ.get("SERPER_API_KEY"))
```

### Example `.env` file

```bash
GOOGLE_API_KEY=your-google-api-key
OPENAI_API_KEY=your-openai-key
SERPER_API_KEY=your-serper-key
OPENWEATHER_API_KEY=your-weather-key
```

---

## Next Steps

- [Middleware](./middleware.md) - Rate limiting and caching
- [Security](./security.md) - Encryption and privacy
