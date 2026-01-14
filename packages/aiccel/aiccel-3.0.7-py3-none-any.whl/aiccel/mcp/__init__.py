# aiccel/mcp/__init__.py
"""
Model Context Protocol (MCP) Support for AIccel
================================================

This module provides MCP client/server capabilities allowing AIccel agents
to connect to external tool servers and expose their tools via MCP.

Features:
- MCPClient: Connect to MCP-compliant tool servers
- MCPServer: Expose aiccel tools as MCP tools  
- MCPToolAdapter: Convert MCP tools to aiccel Tool instances
- Multiple transports: stdio, HTTP/SSE, WebSocket

Usage:
    from aiccel.mcp import MCPClient, MCPToolAdapter
    
    # Connect to an MCP server
    client = MCPClient("http://localhost:3000/mcp")
    await client.connect()
    
    # Get tools from server
    mcp_tools = await client.list_tools()
    
    # Convert to aiccel tools
    adapter = MCPToolAdapter(client)
    aiccel_tools = adapter.get_tools()
    
    # Use with agent
    agent = Agent(provider=provider, tools=aiccel_tools)
"""

from .protocol import (
    MCPProtocol,
    MCPMessage,
    MCPRequest,
    MCPResponse,
    MCPNotification,
    ToolDefinition,
    ResourceDefinition,
    ToolCallResult,
)
from .client import MCPClient
from .server import MCPServer
from .adapter import MCPToolAdapter

__all__ = [
    "MCPProtocol",
    "MCPMessage",
    "MCPRequest",
    "MCPResponse", 
    "MCPNotification",
    "ToolDefinition",
    "ResourceDefinition",
    "ToolCallResult",
    "MCPClient",
    "MCPServer",
    "MCPToolAdapter",
]
