# 🛠️ Unified Tool System

Tools allow agents to interact with the real world—searching the web, checking weather, or performing calculations.

---

## 1. Built-in Tools

AICCEL comes with high-quality built-in tools that are ready to go.

### `SearchTool`
Universal web search supporting multiple providers (Serper, Tavily, Brave).

```python
from aiccel.tools import SearchTool

# Uses Serper.dev by default
search = SearchTool(api_key="your-serper-key")
# Or Tavily
search = SearchTool(provider="tavily", api_key="...")
```

### `WeatherTool`
Current weather and forecasts.

```python
from aiccel.tools import WeatherTool
weather = WeatherTool(api_key="your-owm-key")
```

---

## 2. Custom Tools

Creating your own tool is as simple as inheriting from `BaseTool`.

```python
from aiccel.tools import BaseTool

class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Perform basic math (add, multiply)."

    def _execute(self, a: float, b: float, op: str) -> str:
        if op == "add": return str(a + b)
        if op == "mul": return str(a * b)
        return "Unknown operator"

# Use it in an agent
agent = Agent(provider=p, tools=[CalculatorTool()])
```

---

## 3. Tool Registry

The `ToolRegistry` is used by Agents to dynamically find and validate tools.

*   **Validation**: It automatically checks inputs against expected schemas.
*   **Discovery**: It can "find relevant tools" for a query, optimizing the context window for large toolsets.

---

## 4. MCP (Model Context Protocol)

AICCEL has experimental support for the **Model Context Protocol**. You can import MCP-compliant tools and use them directly.

```python
from aiccel.tools import MCPTool

mcp_tool = MCPTool(endpoint="https://mcp.example.com")
agent = Agent(provider=p, tools=[mcp_tool])
```

---

## 5. Security Note

For tools that involve code execution (like Pandora) or file system access, it is **strongly recommended** to use `subprocess` or `service` isolation modes (see [Security](./security.md)).
