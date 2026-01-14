# Tools

Tools extend agent capabilities to interact with external services and APIs.

## Built-in Tools

### SearchTool

Web search using Serper API:

```python
from aiccel import SearchTool

search = SearchTool(
    api_key="your-serper-api-key",
    timeout=15
)

# Direct usage
result = search.execute(query="Latest AI news", num_results=5)
print(result)

# With agent
agent = Agent(provider=provider, tools=[search])
result = agent.run("Search for Python tutorials")
```

**Get Serper API Key**: [serper.dev](https://serper.dev)

---

### WeatherTool

Weather information using OpenWeatherMap:

```python
from aiccel import WeatherTool

weather = WeatherTool(
    api_key="your-openweathermap-key",
    timeout=15
)

# Direct usage
result = weather.execute(location="London", units="metric")
print(result)

# With agent
agent = Agent(provider=provider, tools=[weather])
result = agent.run("What's the weather in Tokyo?")
```

**Get API Key**: [openweathermap.org](https://openweathermap.org/api)

---

## Creating Custom Tools

### Method 1: Using BaseTool

```python
from aiccel.tools_unified import BaseTool, ToolParameter

class CalculatorTool(BaseTool):
    _name = "calculator"
    _description = "Perform mathematical calculations"
    _parameters = [
        ToolParameter(
            name="expression",
            type="string",
            description="Math expression to evaluate",
            required=True
        )
    ]
    _tags = ["math", "calculator"]
    
    def execute(self, expression: str) -> str:
        try:
            result = eval(expression)  # Use safer eval in production
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

# Use it
calc = CalculatorTool()
agent = Agent(provider=provider, tools=[calc])
```

---

### Method 2: Using Decorator

```python
from aiccel.tools_unified import tool, ToolParameter

@tool(
    name="translator",
    description="Translate text between languages",
    parameters=[
        ToolParameter(name="text", type="string", required=True),
        ToolParameter(name="target_lang", type="string", required=True)
    ]
)
def translate(text: str, target_lang: str) -> str:
    # Your translation logic
    return f"Translated to {target_lang}: {text}"

agent = Agent(provider=provider, tools=[translate])
```

---

### Method 3: Using BaseCustomTool

```python
from aiccel import BaseCustomTool

class EmailTool(BaseCustomTool):
    name = "send_email"
    description = "Send an email to a recipient"
    parameters = {
        "to": {"type": "string", "description": "Recipient email", "required": True},
        "subject": {"type": "string", "description": "Email subject", "required": True},
        "body": {"type": "string", "description": "Email body", "required": True}
    }
    
    def execute(self, to: str, subject: str, body: str) -> str:
        # Send email logic
        return f"Email sent to {to}"
```

---

## Async Tools

For I/O-bound operations:

```python
from aiccel.tools_unified import AsyncTool

class APITool(AsyncTool):
    _name = "api_call"
    _description = "Call an external API"
    
    async def execute_async(self, url: str) -> str:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
```

---

## Tool Registry

Manage multiple tools:

```python
from aiccel import ToolRegistry

registry = ToolRegistry(llm_provider=provider)

# Register tools
registry.register(search_tool)
registry.register(weather_tool)
registry.register(calculator_tool)

# Find relevant tools for a query
relevant = registry.find_relevant_tools("What's the weather?")
# Returns: [weather_tool]

# Get all tools
all_tools = registry.get_tools()

# Get tool by name
tool = registry.get_tool("search")
```

---

## Tool Validation

Validate tool inputs:

```python
from aiccel.tools_unified import ToolValidator, ToolParameter

validator = ToolValidator([
    ToolParameter(name="query", type="string", required=True),
    ToolParameter(name="limit", type="integer", default=10)
])

args = {"query": "test"}
errors = validator.validate(args)

if errors:
    print(f"Validation errors: {errors}")
else:
    print("Valid!")

# Auto-fix args
fixed_args = validator.validate_and_fix(args)
```

---

## Tool Statistics

Track tool performance:

```python
tool = SearchTool(api_key="...")

# After some usage
stats = tool.get_stats()
print(stats)
# {
#     "name": "search",
#     "execution_count": 15,
#     "total_time_ms": 2500.5,
#     "avg_time_ms": 166.7
# }
```

---

## OpenAI Function Calling Format

Convert tools for OpenAI:

```python
from aiccel.integrations import OpenAIFunctionsAdapter

adapter = OpenAIFunctionsAdapter(tools=[search_tool, weather_tool])

# Get OpenAI functions format
functions = adapter.get_functions()

# Use with OpenAI client
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[...],
    functions=functions
)

# Execute tool calls from response
results = adapter.execute_tool_calls(response.tool_calls)
```

---

## Best Practices

1. **Clear descriptions** - LLM uses descriptions to decide when to use tools
2. **Specific parameters** - Define all required parameters clearly
3. **Error handling** - Always return meaningful error messages
4. **Timeout handling** - Set appropriate timeouts for external APIs
5. **Caching** - Cache results for repeated queries

```python
class CachedSearchTool(SearchTool):
    _cache = {}
    
    def execute(self, query: str, **kwargs) -> str:
        if query in self._cache:
            return self._cache[query]
        
        result = super().execute(query, **kwargs)
        self._cache[query] = result
        return result
```

---

## Next Steps

- [Agents](./agents.md) - Use tools with agents
- [Workflows](./workflows.md) - Tools in workflows
