# Model Context Protocol (MCP)

MCP is an open standard for connecting AI agents to external tools and data sources.

---

## What is MCP?

**Model Context Protocol** allows AI agents to:
- Connect to external tool servers
- Discover available tools dynamically
- Call tools across process/network boundaries
- Share resources and context

AICCEL fully supports MCP as both client and server.

---

## Quick Start

### Connect to MCP Server

```python
from aiccel import Agent, GeminiProvider
from aiccel.mcp import MCPClient, MCPToolAdapter

# Connect to MCP server
client = MCPClient("http://localhost:3000/mcp")
await client.connect()

# Get tools from MCP server
adapter = MCPToolAdapter(client)
mcp_tools = adapter.get_tools()

# Use with AICCEL agent
provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
agent = Agent(provider=provider, tools=mcp_tools)

result = await agent.run_async("Use the external tools")
```

### Expose AICCEL Tools via MCP

```python
from aiccel import SearchTool, WeatherTool
from aiccel.mcp import MCPServer

# Create MCP server with AICCEL tools
server = MCPServer(
    name="my-tool-server",
    tools=[
        SearchTool(api_key="..."),
        WeatherTool(api_key="...")
    ]
)

# Start server
await server.start(host="localhost", port=3000)
```

---

## MCPClient

Connect to MCP-compliant tool servers.

### Connecting

```python
from aiccel.mcp import MCPClient

# HTTP transport
client = MCPClient("http://localhost:3000/mcp")

# WebSocket transport
client = MCPClient("ws://localhost:3000/mcp")

# Stdio transport (for local processes)
client = MCPClient("stdio://path/to/executable")

# Connect
await client.connect()

# Connection info
print(f"Connected: {client.is_connected}")
print(f"Server name: {client.server_info.name}")
print(f"Protocol version: {client.protocol_version}")
```

### Listing Tools

```python
# Get all available tools
tools = await client.list_tools()

for tool in tools:
    print(f"Tool: {tool.name}")
    print(f"  Description: {tool.description}")
    print(f"  Parameters: {tool.parameters}")
```

### Calling Tools

```python
# Call a tool directly
result = await client.call_tool(
    name="search",
    arguments={"query": "Python tutorials"}
)

print(f"Result: {result.content}")
print(f"Success: {result.is_error}")
```

### Listing Resources

```python
# Get available resources
resources = await client.list_resources()

for resource in resources:
    print(f"Resource: {resource.uri}")
    print(f"  Name: {resource.name}")
    print(f"  Type: {resource.mime_type}")
```

### Reading Resources

```python
# Read a resource
content = await client.read_resource("file:///path/to/document.txt")
print(content.text)

# Or binary content
image = await client.read_resource("file:///path/to/image.png")
print(f"Binary size: {len(image.blob)} bytes")
```

### Disconnect

```python
await client.disconnect()
```

---

## MCPToolAdapter

Convert MCP tools to AICCEL tools.

```python
from aiccel.mcp import MCPClient, MCPToolAdapter

# Connect to server
client = MCPClient("http://localhost:3000/mcp")
await client.connect()

# Create adapter
adapter = MCPToolAdapter(client)

# Get all tools as AICCEL tools
aiccel_tools = adapter.get_tools()

# Get specific tool
search_tool = adapter.get_tool("search")

# Use with agent
agent = Agent(provider=provider, tools=aiccel_tools)
```

### Sync vs Async

```python
# Async (recommended)
result = await tool.execute_async(query="test")

# Sync (uses event loop)
result = tool.execute(query="test")
```

---

## MCPServer

Expose your AICCEL tools via MCP.

### Creating Server

```python
from aiccel.mcp import MCPServer
from aiccel import SearchTool, WeatherTool

# Create tools
search = SearchTool(api_key="...")
weather = WeatherTool(api_key="...")

# Create custom tool
from aiccel.tools_unified import BaseTool

class CalculatorTool(BaseTool):
    _name = "calculator"
    _description = "Perform calculations"
    
    def execute(self, expression: str) -> str:
        return str(eval(expression))

# Create server
server = MCPServer(
    name="my-tools-server",
    version="1.0.0",
    tools=[search, weather, CalculatorTool()]
)
```

### Starting Server

```python
# HTTP server
await server.start(
    host="0.0.0.0",
    port=3000,
    transport="http"
)

# WebSocket server
await server.start(
    host="0.0.0.0",
    port=3001,
    transport="websocket"
)

# Stdio (for integration with other tools)
await server.start(transport="stdio")
```

### Adding Resources

```python
# Add a file resource
server.add_resource(
    uri="file:///config.json",
    name="Configuration",
    description="Server configuration file",
    mime_type="application/json"
)

# Add dynamic resource
@server.resource("data://users/{user_id}")
async def get_user(user_id: str) -> str:
    # Fetch user data
    return json.dumps({"id": user_id, "name": "..."}
```

### Server Lifecycle

```python
# Start
await server.start(port=3000)

# Check status
print(f"Running: {server.is_running}")
print(f"Tools: {len(server.tools)}")

# Stop
await server.stop()
```

---

## MCP Protocol Details

### Messages

```python
from aiccel.mcp import MCPRequest, MCPResponse, MCPNotification

# Request (expects response)
request = MCPRequest(
    method="tools/call",
    params={"name": "search", "arguments": {"query": "test"}}
)

# Response
response = MCPResponse(
    result={"content": "Search results..."},
    id=request.id
)

# Notification (no response expected)
notification = MCPNotification(
    method="progress",
    params={"percent": 50}
)
```

### Tool Definition

```python
from aiccel.mcp import ToolDefinition

tool = ToolDefinition(
    name="search",
    description="Search the web",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query"
            }
        },
        "required": ["query"]
    }
)
```

### Resource Definition

```python
from aiccel.mcp import ResourceDefinition

resource = ResourceDefinition(
    uri="file:///documents/report.pdf",
    name="Annual Report",
    description="Company annual report 2024",
    mimeType="application/pdf"
)
```

---

## Transports

### HTTP/SSE Transport

```python
# Client
client = MCPClient("http://localhost:3000/mcp")

# Server-Sent Events for streaming
await client.connect()

# Receives streamed responses
async for chunk in client.stream_call("long_running_tool", args):
    print(chunk)
```

### WebSocket Transport

```python
# Client
client = MCPClient("ws://localhost:3000/mcp")
await client.connect()

# Full duplex communication
await client.call_tool("search", {"query": "test"})
```

### Stdio Transport

For local process communication:

```python
# Client connecting to local process
client = MCPClient("stdio://./mcp-server")
await client.connect()

# Server running on stdio
server = MCPServer(name="local-server", tools=[...])
await server.start(transport="stdio")
```

---

## Complete Example: MCP Tool Server

```python
# mcp_server.py
import asyncio
from aiccel import SearchTool, WeatherTool
from aiccel.mcp import MCPServer
from aiccel.tools_unified import BaseTool, ToolParameter


class DatabaseTool(BaseTool):
    """Query a database."""
    _name = "query_database"
    _description = "Execute SQL queries"
    _parameters = [
        ToolParameter(name="query", type="string", required=True),
        ToolParameter(name="limit", type="integer", default=10)
    ]
    
    def execute(self, query: str, limit: int = 10) -> str:
        # Your DB logic
        return f"Query results for: {query} (limit {limit})"


class FileTool(BaseTool):
    """Read and write files."""
    _name = "file_operations"
    _description = "Read, write, and list files"
    _parameters = [
        ToolParameter(name="operation", type="string", enum=["read", "write", "list"]),
        ToolParameter(name="path", type="string"),
        ToolParameter(name="content", type="string", required=False)
    ]
    
    def execute(self, operation: str, path: str, content: str = None) -> str:
        if operation == "read":
            with open(path) as f:
                return f.read()
        elif operation == "write":
            with open(path, "w") as f:
                f.write(content)
            return f"Written to {path}"
        elif operation == "list":
            import os
            return str(os.listdir(path))


async def main():
    # Create server
    server = MCPServer(
        name="my-tool-server",
        version="1.0.0",
        tools=[
            SearchTool(api_key="..."),
            WeatherTool(api_key="..."),
            DatabaseTool(),
            FileTool()
        ]
    )
    
    # Add resources
    server.add_resource(
        uri="file:///config.json",
        name="Server Config",
        mime_type="application/json"
    )
    
    print("Starting MCP server on http://localhost:3000")
    await server.start(host="0.0.0.0", port=3000)
    
    # Keep running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Complete Example: MCP Client

```python
# mcp_client.py
import asyncio
from aiccel import Agent, GeminiProvider
from aiccel.mcp import MCPClient, MCPToolAdapter


async def main():
    # Connect to MCP server
    client = MCPClient("http://localhost:3000")
    await client.connect()
    
    print(f"Connected to: {client.server_info.name}")
    
    # List available tools
    tools = await client.list_tools()
    print(f"\nAvailable tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Create adapter
    adapter = MCPToolAdapter(client)
    aiccel_tools = adapter.get_tools()
    
    # Create agent with MCP tools
    provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
    agent = Agent(
        provider=provider,
        tools=aiccel_tools,
        name="MCPAgent",
        instructions="Use the available tools to help users."
    )
    
    # Use agent
    result = await agent.run_async("Search for Python tutorials")
    print(f"\nAgent response: {result['response']}")
    
    # Cleanup
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Integration with Workflows

```python
from aiccel import WorkflowBuilder
from aiccel.mcp import MCPClient, MCPToolAdapter
from aiccel.workflows import ToolNode

# Connect to MCP
client = MCPClient("http://tools-server:3000")
await client.connect()
adapter = MCPToolAdapter(client)

# Get specific MCP tool
search_tool = adapter.get_tool("search")
db_tool = adapter.get_tool("query_database")

# Use in workflow
workflow = (
    WorkflowBuilder("mcp_workflow")
    
    .add_tool("search", search_tool, 
              args_mapping={"query": "search_query"},
              output_key="search_results")
    
    .add_tool("db_query", db_tool,
              args_mapping={"query": "sql_query"},
              output_key="db_results")
    
    .add_agent("analyze", analyzer_agent,
               prompt_template="Analyze: {search_results} {db_results}")
    
    .chain("search", "db_query", "analyze")
    .build()
)
```

---

## Best Practices

1. **Handle disconnections** - MCP connections can drop
   ```python
   try:
       result = await client.call_tool(...)
   except ConnectionError:
       await client.reconnect()
       result = await client.call_tool(...)
   ```

2. **Cache tool definitions** - Don't list tools repeatedly
   ```python
   if not hasattr(self, '_tools_cache'):
       self._tools_cache = await client.list_tools()
   ```

3. **Set timeouts** - External calls can hang
   ```python
   result = await asyncio.wait_for(
       client.call_tool("slow_tool", args),
       timeout=30.0
   )
   ```

4. **Validate inputs** - Before sending to MCP
5. **Log MCP calls** - For debugging

---

## Next Steps

- [Agent Workflows](./agent-workflows.md) - Build complex pipelines
- [Integrations](./integrations.md) - Connect with other systems
