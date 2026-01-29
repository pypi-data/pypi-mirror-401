# aiccel/mcp/server.py
"""
MCP Server Implementation
=========================

Exposes aiccel tools as an MCP-compliant server.
Allows external applications to use aiccel tools via MCP protocol.

Usage:
    from aiccel.mcp import MCPServer
    from aiccel.tools import SearchTool, WeatherTool
    
    # Create server with tools
    server = MCPServer(
        name="aiccel-tools",
        version="1.0.0",
        tools=[search_tool, weather_tool]
    )
    
    # Run as stdio server
    await server.run_stdio()
    
    # Or run as HTTP server
    await server.run_http(port=3000)
"""

import asyncio
import json
import logging
import sys
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field

from .protocol import (
    MCPVersion,
    MCPMethod,
    MCPErrorCode,
    MCPError,
    MCPRequest,
    MCPResponse,
    MCPNotification,
    ToolDefinition,
    ResourceDefinition,
    ResourceContent,
    ToolCallResult,
    JSONSchema,
    ServerCapabilities,
    InitializeResult,
)

logger = logging.getLogger(__name__)


@dataclass
class ServerInfo:
    """Server information"""
    name: str
    version: str


class MCPServer:
    """
    MCP Server that exposes aiccel tools.
    
    This server implements the MCP protocol and allows external
    applications to discover and call aiccel tools.
    
    Features:
    - Tool registration and execution
    - Resource serving
    - Multiple transports (stdio, HTTP)
    - Notification support
    
    Example:
        # Create server
        server = MCPServer(
            name="my-tools",
            version="1.0.0"
        )
        
        # Register tools
        server.add_tool(search_tool)
        server.add_tool(weather_tool)
        
        # Run
        await server.run_stdio()
    """
    
    def __init__(
        self,
        name: str = "aiccel-mcp-server",
        version: str = "1.0.0",
        tools: Optional[List[Any]] = None,
        resources: Optional[List[ResourceDefinition]] = None
    ):
        self.info = ServerInfo(name=name, version=version)
        self._tools: Dict[str, Any] = {}
        self._tool_definitions: Dict[str, ToolDefinition] = {}
        self._resources: Dict[str, ResourceDefinition] = {}
        self._resource_handlers: Dict[str, Callable] = {}
        self._initialized = False
        self._client_info: Optional[Dict[str, str]] = None
        
        # Register provided tools
        if tools:
            for tool in tools:
                self.add_tool(tool)
        
        # Register provided resources
        if resources:
            for resource in resources:
                self._resources[resource.uri] = resource
        
        # Method handlers
        self._handlers: Dict[str, Callable] = {
            MCPMethod.INITIALIZE.value: self._handle_initialize,
            MCPMethod.SHUTDOWN.value: self._handle_shutdown,
            MCPMethod.TOOLS_LIST.value: self._handle_tools_list,
            MCPMethod.TOOLS_CALL.value: self._handle_tools_call,
            MCPMethod.RESOURCES_LIST.value: self._handle_resources_list,
            MCPMethod.RESOURCES_READ.value: self._handle_resources_read,
        }
    
    def add_tool(self, tool: Any) -> "MCPServer":
        """
        Add an aiccel tool to the server.
        
        Args:
            tool: An aiccel Tool instance
            
        Returns:
            Self for chaining
        """
        self._tools[tool.name] = tool
        
        # Create MCP tool definition
        tool_dict = tool.to_dict()
        params = tool_dict.get("parameters", {})
        
        self._tool_definitions[tool.name] = ToolDefinition(
            name=tool.name,
            description=tool.description,
            inputSchema=JSONSchema(
                type=params.get("type", "object"),
                properties=params.get("properties", {}),
                required=params.get("required", [])
            )
        )
        
        logger.info(f"Registered tool: {tool.name}")
        return self
    
    def add_resource(
        self,
        uri: str,
        name: str,
        handler: Callable[[str], str],
        description: Optional[str] = None,
        mime_type: Optional[str] = None
    ) -> "MCPServer":
        """
        Add a resource to the server.
        
        Args:
            uri: Resource URI
            name: Resource name
            handler: Function that returns resource content
            description: Optional description
            mime_type: Optional MIME type
            
        Returns:
            Self for chaining
        """
        self._resources[uri] = ResourceDefinition(
            uri=uri,
            name=name,
            description=description,
            mimeType=mime_type
        )
        self._resource_handlers[uri] = handler
        
        logger.info(f"Registered resource: {uri}")
        return self
    
    @property
    def capabilities(self) -> ServerCapabilities:
        """Get server capabilities"""
        caps = ServerCapabilities()
        
        if self._tools:
            caps.tools = {"listChanged": True}
        
        if self._resources:
            caps.resources = {"subscribe": False, "listChanged": True}
        
        return caps
    
    async def handle_message(self, message: str) -> Optional[str]:
        """
        Handle an incoming MCP message.
        
        Args:
            message: JSON-RPC message string
            
        Returns:
            Response string or None for notifications
        """
        try:
            data = json.loads(message)
        except json.JSONDecodeError as e:
            response = MCPResponse.failure(
                None,
                MCPErrorCode.PARSE_ERROR,
                f"Invalid JSON: {e}"
            )
            return response.to_json()
        
        # Check if it's a notification (no id)
        if "id" not in data:
            await self._handle_notification(MCPNotification.from_dict(data))
            return None
        
        # It's a request
        request = MCPRequest.from_dict(data)
        response = await self._handle_request(request)
        return response.to_json()
    
    async def _handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle a request"""
        handler = self._handlers.get(request.method)
        
        if not handler:
            return MCPResponse.failure(
                request.id,
                MCPErrorCode.METHOD_NOT_FOUND,
                f"Method not found: {request.method}"
            )
        
        try:
            result = await handler(request.params or {})
            return MCPResponse.success(request.id, result)
        except Exception as e:
            logger.error(f"Error handling {request.method}: {e}")
            return MCPResponse.failure(
                request.id,
                MCPErrorCode.INTERNAL_ERROR,
                str(e)
            )
    
    async def _handle_notification(self, notification: MCPNotification) -> None:
        """Handle a notification"""
        if notification.method == MCPMethod.INITIALIZED.value:
            self._initialized = True
            logger.info("Client initialized")
    
    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        self._client_info = params.get("clientInfo", {})
        
        logger.info(f"Initialize from {self._client_info.get('name', 'unknown')}")
        
        return {
            "protocolVersion": MCPVersion.CURRENT,
            "capabilities": self.capabilities.to_dict(),
            "serverInfo": {
                "name": self.info.name,
                "version": self.info.version
            }
        }
    
    async def _handle_shutdown(self, params: Dict[str, Any]) -> None:
        """Handle shutdown request"""
        logger.info("Shutdown requested")
        return None
    
    async def _handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request"""
        return {
            "tools": [d.to_dict() for d in self._tool_definitions.values()]
        }
    
    async def _handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not name:
            raise ValueError("Tool name required")
        
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")
        
        logger.info(f"Calling tool: {name}")
        
        try:
            # Execute tool
            if hasattr(tool, "execute_async"):
                try:
                    result = await tool.execute_async(arguments)
                except Exception:
                    result = tool.execute(arguments)
            else:
                result = tool.execute(arguments)
            
            # Format result
            return ToolCallResult.text(str(result)).to_dict()
            
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return ToolCallResult.error(str(e)).to_dict()
    
    async def _handle_resources_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resources/list request"""
        return {
            "resources": [r.to_dict() for r in self._resources.values()]
        }
    
    async def _handle_resources_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resources/read request"""
        uri = params.get("uri")
        
        if not uri:
            raise ValueError("Resource URI required")
        
        handler = self._resource_handlers.get(uri)
        if not handler:
            raise ValueError(f"Resource not found: {uri}")
        
        try:
            content = handler(uri)
            return {
                "contents": [
                    {
                        "uri": uri,
                        "text": content,
                        "mimeType": self._resources[uri].mimeType
                    }
                ]
            }
        except Exception as e:
            raise ValueError(f"Error reading resource: {e}")
    
    async def run_stdio(self) -> None:
        """
        Run server using stdio transport.
        
        Reads from stdin and writes to stdout using Content-Length framing.
        """
        logger.info(f"Starting MCP server {self.info.name} v{self.info.version} on stdio")
        
        loop = asyncio.get_running_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        
        await loop.connect_read_pipe(
            lambda: protocol, sys.stdin.buffer
        )
        
        writer_transport, writer_protocol = await loop.connect_write_pipe(
            asyncio.streams.FlowControlMixin, sys.stdout.buffer
        )
        writer = asyncio.StreamWriter(writer_transport, writer_protocol, None, loop)
        
        try:
            while True:
                # Read Content-Length header
                header_line = await reader.readline()
                if not header_line:
                    break
                
                header = header_line.decode('utf-8').strip()
                if not header.startswith("Content-Length:"):
                    continue
                
                content_length = int(header.split(":")[1].strip())
                
                # Read blank line
                await reader.readline()
                
                # Read content
                data = await reader.read(content_length)
                message = data.decode('utf-8')
                
                # Handle message
                response = await self.handle_message(message)
                
                if response:
                    # Write response with Content-Length
                    response_bytes = response.encode('utf-8')
                    header = f"Content-Length: {len(response_bytes)}\r\n\r\n"
                    writer.write(header.encode('utf-8') + response_bytes)
                    await writer.drain()
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Server error: {e}")
    
    async def run_http(
        self,
        host: str = "0.0.0.0",
        port: int = 3000,
        path: str = "/mcp"
    ) -> None:
        """
        Run server using HTTP transport.
        
        Args:
            host: Host to bind to
            port: Port to listen on
            path: URL path for MCP endpoint
        """
        try:
            from aiohttp import web
        except ImportError:
            raise ImportError("aiohttp is required for HTTP server")
        
        async def handle_request(request: web.Request) -> web.Response:
            try:
                data = await request.json()
                message = json.dumps(data)
                
                response = await self.handle_message(message)
                
                if response:
                    return web.json_response(
                        json.loads(response),
                        content_type="application/json"
                    )
                else:
                    return web.Response(status=204)
                    
            except Exception as e:
                return web.json_response(
                    {"error": str(e)},
                    status=500
                )
        
        app = web.Application()
        app.router.add_post(path, handle_request)
        
        logger.info(f"Starting MCP server {self.info.name} v{self.info.version} on http://{host}:{port}{path}")
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            pass
        finally:
            await runner.cleanup()


def run_mcp_server(
    tools: List[Any],
    name: str = "aiccel-mcp-server",
    version: str = "1.0.0",
    transport: str = "stdio"
) -> None:
    """
    Convenience function to run an MCP server.
    
    Args:
        tools: List of aiccel tools to expose
        name: Server name
        version: Server version
        transport: "stdio" or "http"
    """
    server = MCPServer(name=name, version=version, tools=tools)
    
    if transport == "stdio":
        asyncio.run(server.run_stdio())
    elif transport == "http":
        asyncio.run(server.run_http())
    else:
        raise ValueError(f"Unknown transport: {transport}")
