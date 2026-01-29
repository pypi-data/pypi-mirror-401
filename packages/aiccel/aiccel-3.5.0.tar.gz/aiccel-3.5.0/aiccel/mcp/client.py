# aiccel/mcp/client.py
"""
MCP Client Implementation
=========================

Provides a client for connecting to MCP-compliant tool servers.
Supports multiple transports: stdio, HTTP/SSE, WebSocket.

Usage:
    from aiccel.mcp import MCPClient
    
    # HTTP transport
    client = MCPClient("http://localhost:3000/mcp")
    await client.connect()
    
    # List available tools
    tools = await client.list_tools()
    
    # Call a tool
    result = await client.call_tool("search", {"query": "AI news"})
    
    # Cleanup
    await client.close()
"""

import asyncio
import json
import logging
import os
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Callable, Awaitable
from dataclasses import dataclass, field
import uuid

from .protocol import (
    MCPVersion,
    MCPMethod,
    MCPErrorCode,
    MCPError,
    MCPRequest,
    MCPResponse,
    MCPNotification,
    MCPProtocol,
    ToolDefinition,
    ResourceDefinition,
    ResourceContent,
    ToolCallResult,
    InitializeParams,
    InitializeResult,
    ClientCapabilities,
    ServerCapabilities,
)

logger = logging.getLogger(__name__)


class MCPTransport(ABC):
    """Abstract base transport for MCP communication"""
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection"""
        pass
    
    @abstractmethod
    async def send(self, message: str) -> None:
        """Send a message"""
        pass
    
    @abstractmethod
    async def receive(self) -> str:
        """Receive a message"""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close connection"""
        pass
    
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connected"""
        pass


class StdioTransport(MCPTransport):
    """Transport for stdio-based MCP servers (subprocess)"""
    
    def __init__(self, command: List[str], cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None):
        self.command = command
        self.cwd = cwd
        self.env = {**os.environ, **(env or {})}
        self._process: Optional[asyncio.subprocess.Process] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Start the subprocess"""
        logger.info(f"Starting MCP server: {' '.join(self.command)}")
        self._process = await asyncio.create_subprocess_exec(
            *self.command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.cwd,
            env=self.env
        )
        self._connected = True
        logger.info(f"MCP server started with PID: {self._process.pid}")
    
    async def send(self, message: str) -> None:
        """Send message via stdin"""
        if not self._process or not self._process.stdin:
            raise ConnectionError("Not connected")
        
        # MCP uses Content-Length header like LSP
        data = message.encode('utf-8')
        header = f"Content-Length: {len(data)}\r\n\r\n"
        self._process.stdin.write(header.encode('utf-8') + data)
        await self._process.stdin.drain()
        logger.debug(f"Sent: {message[:200]}...")
    
    async def receive(self) -> str:
        """Receive message from stdout"""
        if not self._process or not self._process.stdout:
            raise ConnectionError("Not connected")
        
        # Read Content-Length header
        header_line = await self._process.stdout.readline()
        if not header_line:
            raise ConnectionError("Server closed connection")
        
        header = header_line.decode('utf-8').strip()
        if not header.startswith("Content-Length:"):
            # Skip blank lines
            if header:
                logger.warning(f"Unexpected header: {header}")
            return await self.receive()
        
        content_length = int(header.split(":")[1].strip())
        
        # Read blank line after header
        await self._process.stdout.readline()
        
        # Read content
        data = await self._process.stdout.read(content_length)
        message = data.decode('utf-8')
        logger.debug(f"Received: {message[:200]}...")
        return message
    
    async def close(self) -> None:
        """Terminate subprocess"""
        if self._process:
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self._process.kill()
            self._connected = False
            logger.info("MCP server terminated")
    
    @property
    def is_connected(self) -> bool:
        return self._connected and self._process is not None


class HTTPTransport(MCPTransport):
    """Transport for HTTP-based MCP servers (SSE)"""
    
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        self.url = url.rstrip('/')
        self.headers = headers or {}
        self._session = None
        self._connected = False
        self._event_queue: asyncio.Queue = asyncio.Queue()
    
    async def connect(self) -> None:
        """Establish HTTP connection"""
        try:
            import aiohttp
            self._session = aiohttp.ClientSession()
            self._connected = True
            logger.info(f"Connected to MCP server at {self.url}")
        except ImportError:
            raise ImportError("aiohttp is required for HTTP transport")
    
    async def send(self, message: str) -> None:
        """Send message via POST"""
        if not self._session:
            raise ConnectionError("Not connected")
        
        import aiohttp
        async with self._session.post(
            self.url,
            json=json.loads(message),
            headers={"Content-Type": "application/json", **self.headers}
        ) as response:
            if response.status != 200:
                text = await response.text()
                raise ConnectionError(f"HTTP error {response.status}: {text}")
            
            # For request/response, read response immediately
            data = await response.json()
            await self._event_queue.put(json.dumps(data))
    
    async def receive(self) -> str:
        """Receive message from queue"""
        return await self._event_queue.get()
    
    async def close(self) -> None:
        """Close HTTP session"""
        if self._session:
            await self._session.close()
            self._connected = False
            logger.info("HTTP connection closed")
    
    @property
    def is_connected(self) -> bool:
        return self._connected


class MCPClient:
    """
    MCP Client for connecting to tool servers.
    
    Supports:
    - Stdio transport (subprocess)
    - HTTP transport (REST/SSE)
    - WebSocket transport (bidirectional)
    
    Example:
        # Connect to stdio server
        client = MCPClient.from_command(["npx", "@modelcontextprotocol/server-search"])
        await client.connect()
        
        # Connect to HTTP server
        client = MCPClient.from_url("http://localhost:3000/mcp")
        await client.connect()
        
        # Use tools
        tools = await client.list_tools()
        result = await client.call_tool("search", {"query": "hello"})
    """
    
    def __init__(self, transport: MCPTransport):
        self.transport = transport
        self._initialized = False
        self._request_id = 0
        self._pending_requests: Dict[Union[str, int], asyncio.Future] = {}
        self._server_info: Optional[InitializeResult] = None
        self._tools: Dict[str, ToolDefinition] = {}
        self._resources: Dict[str, ResourceDefinition] = {}
        self._notification_handlers: Dict[str, List[Callable]] = {}
        self._receive_task: Optional[asyncio.Task] = None
    
    @classmethod
    def from_command(
        cls, 
        command: List[str], 
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
    ) -> "MCPClient":
        """Create client from subprocess command"""
        return cls(StdioTransport(command, cwd, env))
    
    @classmethod
    def from_url(
        cls, 
        url: str, 
        headers: Optional[Dict[str, str]] = None
    ) -> "MCPClient":
        """Create client from HTTP URL"""
        return cls(HTTPTransport(url, headers))
    
    async def connect(self) -> InitializeResult:
        """Connect and initialize the MCP session"""
        await self.transport.connect()
        
        # Start message receiver for stdio
        if isinstance(self.transport, StdioTransport):
            self._receive_task = asyncio.create_task(self._receive_loop())
        
        # Initialize session
        result = await self._initialize()
        self._initialized = True
        
        # Cache tools and resources
        if result.capabilities.tools:
            await self._refresh_tools()
        if result.capabilities.resources:
            await self._refresh_resources()
        
        return result
    
    async def close(self) -> None:
        """Close the connection"""
        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
        
        await self.transport.close()
        self._initialized = False
    
    async def list_tools(self) -> List[ToolDefinition]:
        """List available tools"""
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call connect() first.")
        
        result = await self._send_request(MCPMethod.TOOLS_LIST)
        tools = [ToolDefinition.from_dict(t) for t in result.get("tools", [])]
        self._tools = {t.name: t for t in tools}
        return tools
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> ToolCallResult:
        """Call a tool by name"""
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call connect() first.")
        
        result = await self._send_request(
            MCPMethod.TOOLS_CALL,
            {"name": name, "arguments": arguments}
        )
        return ToolCallResult.from_dict(result)
    
    async def list_resources(self) -> List[ResourceDefinition]:
        """List available resources"""
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call connect() first.")
        
        result = await self._send_request(MCPMethod.RESOURCES_LIST)
        resources = [ResourceDefinition.from_dict(r) for r in result.get("resources", [])]
        self._resources = {r.uri: r for r in resources}
        return resources
    
    async def read_resource(self, uri: str) -> ResourceContent:
        """Read a resource by URI"""
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call connect() first.")
        
        result = await self._send_request(
            MCPMethod.RESOURCES_READ,
            {"uri": uri}
        )
        contents = result.get("contents", [])
        if not contents:
            raise ValueError(f"No content returned for resource: {uri}")
        
        content = contents[0]
        return ResourceContent(
            uri=content.get("uri", uri),
            text=content.get("text"),
            blob=content.get("blob"),
            mimeType=content.get("mimeType")
        )
    
    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get cached tool by name"""
        return self._tools.get(name)
    
    def get_resource(self, uri: str) -> Optional[ResourceDefinition]:
        """Get cached resource by URI"""
        return self._resources.get(uri)
    
    def on_notification(self, method: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register notification handler"""
        if method not in self._notification_handlers:
            self._notification_handlers[method] = []
        self._notification_handlers[method].append(handler)
    
    @property
    def server_info(self) -> Optional[Dict[str, str]]:
        """Get server info from initialization"""
        return self._server_info.serverInfo if self._server_info else None
    
    @property
    def capabilities(self) -> Optional[ServerCapabilities]:
        """Get server capabilities"""
        return self._server_info.capabilities if self._server_info else None
    
    async def _initialize(self) -> InitializeResult:
        """Send initialize request"""
        params = InitializeParams(
            protocolVersion=MCPVersion.CURRENT,
            capabilities=ClientCapabilities(),
            clientInfo={"name": "aiccel", "version": "2.0.0"}
        )
        
        result = await self._send_request(MCPMethod.INITIALIZE, params.to_dict())
        self._server_info = InitializeResult.from_dict(result)
        
        # Send initialized notification
        await self._send_notification(MCPMethod.INITIALIZED)
        
        logger.info(f"Initialized MCP session with {self._server_info.serverInfo.get('name', 'unknown')}")
        return self._server_info
    
    async def _refresh_tools(self) -> None:
        """Refresh tool cache"""
        await self.list_tools()
    
    async def _refresh_resources(self) -> None:
        """Refresh resource cache"""
        await self.list_resources()
    
    async def _send_request(
        self, 
        method: Union[str, MCPMethod], 
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Send request and wait for response"""
        self._request_id += 1
        request_id = self._request_id
        
        request = MCPRequest(
            id=request_id,
            method=method.value if isinstance(method, MCPMethod) else method,
            params=params
        )
        
        # Create future for response
        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()
        self._pending_requests[request_id] = future
        
        try:
            await self.transport.send(request.to_json())
            
            # For HTTP transport, response comes immediately
            if isinstance(self.transport, HTTPTransport):
                response_str = await self.transport.receive()
                response = MCPResponse.from_dict(json.loads(response_str))
                
                if response.error:
                    raise MCPClientError(
                        response.error.code,
                        response.error.message,
                        response.error.data
                    )
                
                return response.result
            
            # For stdio, wait for response via receive loop
            result = await asyncio.wait_for(future, timeout=30.0)
            return result
            
        except asyncio.TimeoutError:
            self._pending_requests.pop(request_id, None)
            raise MCPClientError(MCPErrorCode.TIMEOUT, "Request timed out")
        finally:
            self._pending_requests.pop(request_id, None)
    
    async def _send_notification(
        self, 
        method: Union[str, MCPMethod],
        params: Optional[Dict[str, Any]] = None
    ) -> None:
        """Send notification (no response expected)"""
        notification = MCPNotification(
            method=method.value if isinstance(method, MCPMethod) else method,
            params=params
        )
        await self.transport.send(notification.to_json())
    
    async def _receive_loop(self) -> None:
        """Background loop to receive messages"""
        try:
            while True:
                message_str = await self.transport.receive()
                message = json.loads(message_str)
                
                if "id" in message:
                    # Response
                    response = MCPResponse.from_dict(message)
                    future = self._pending_requests.get(response.id)
                    if future and not future.done():
                        if response.error:
                            future.set_exception(MCPClientError(
                                response.error.code,
                                response.error.message,
                                response.error.data
                            ))
                        else:
                            future.set_result(response.result)
                else:
                    # Notification
                    notification = MCPNotification.from_dict(message)
                    await self._handle_notification(notification)
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in receive loop: {e}")
    
    async def _handle_notification(self, notification: MCPNotification) -> None:
        """Handle incoming notification"""
        handlers = self._notification_handlers.get(notification.method, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(notification.params or {})
                else:
                    handler(notification.params or {})
            except Exception as e:
                logger.error(f"Error in notification handler: {e}")
        
        # Handle tool/resource change notifications
        if notification.method == MCPMethod.TOOLS_CHANGED.value:
            await self._refresh_tools()
        elif notification.method == MCPMethod.RESOURCES_UPDATED.value:
            await self._refresh_resources()


class MCPClientError(Exception):
    """Exception raised by MCP client"""
    
    def __init__(self, code: int, message: str, data: Any = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"
