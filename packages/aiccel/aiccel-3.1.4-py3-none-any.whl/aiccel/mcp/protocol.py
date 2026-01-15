# aiccel/mcp/protocol.py
"""
Model Context Protocol (MCP) Protocol Definitions
==================================================

Implements the MCP protocol specification for tool/resource communication.
Based on the Anthropic MCP specification and JSON-RPC 2.0.

References:
- https://github.com/anthropics/mcp
- https://www.jsonrpc.org/specification
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Union, Callable, Awaitable
from enum import Enum
import json
import uuid
from datetime import datetime


class MCPVersion:
    """MCP Protocol Version"""
    CURRENT = "2024-11-05"
    SUPPORTED = ["2024-11-05", "2024-10-01"]


class MCPMethod(str, Enum):
    """Standard MCP methods"""
    # Lifecycle
    INITIALIZE = "initialize"
    INITIALIZED = "notifications/initialized"
    SHUTDOWN = "shutdown"
    
    # Tools
    TOOLS_LIST = "tools/list"
    TOOLS_CALL = "tools/call"
    
    # Resources
    RESOURCES_LIST = "resources/list"
    RESOURCES_READ = "resources/read"
    RESOURCES_SUBSCRIBE = "resources/subscribe"
    RESOURCES_UNSUBSCRIBE = "resources/unsubscribe"
    
    # Prompts
    PROMPTS_LIST = "prompts/list"
    PROMPTS_GET = "prompts/get"
    
    # Logging
    LOGGING_SET_LEVEL = "logging/setLevel"
    
    # Notifications
    PROGRESS = "notifications/progress"
    MESSAGE = "notifications/message"
    RESOURCES_UPDATED = "notifications/resources/updated"
    TOOLS_CHANGED = "notifications/tools/list_changed"


class MCPErrorCode(int, Enum):
    """Standard JSON-RPC and MCP error codes"""
    # JSON-RPC standard errors
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    
    # MCP-specific errors
    RESOURCE_NOT_FOUND = -32001
    TOOL_NOT_FOUND = -32002
    TOOL_EXECUTION_ERROR = -32003
    INVALID_TOOL_ARGS = -32004
    TIMEOUT = -32005


@dataclass
class MCPError:
    """MCP Error object"""
    code: int
    message: str
    data: Optional[Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"code": self.code, "message": self.message}
        if self.data is not None:
            result["data"] = self.data
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPError":
        return cls(
            code=data.get("code", MCPErrorCode.INTERNAL_ERROR),
            message=data.get("message", "Unknown error"),
            data=data.get("data")
        )


@dataclass
class JSONSchema:
    """JSON Schema for tool parameters"""
    type: str = "object"
    properties: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"type": self.type}
        if self.properties:
            result["properties"] = self.properties
        if self.required:
            result["required"] = self.required
        if self.description:
            result["description"] = self.description
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JSONSchema":
        return cls(
            type=data.get("type", "object"),
            properties=data.get("properties", {}),
            required=data.get("required", []),
            description=data.get("description")
        )


@dataclass
class ToolDefinition:
    """MCP Tool definition"""
    name: str
    description: str
    inputSchema: JSONSchema = field(default_factory=JSONSchema)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.inputSchema.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolDefinition":
        input_schema = data.get("inputSchema", {})
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            inputSchema=JSONSchema.from_dict(input_schema) if isinstance(input_schema, dict) else JSONSchema()
        )


@dataclass
class ToolCallResult:
    """Result of tool call"""
    content: List[Dict[str, Any]]  # Array of content items (text, image, etc.)
    isError: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "isError": self.isError
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolCallResult":
        return cls(
            content=data.get("content", []),
            isError=data.get("isError", False)
        )
    
    @classmethod
    def text(cls, text: str, is_error: bool = False) -> "ToolCallResult":
        """Create a text result"""
        return cls(
            content=[{"type": "text", "text": text}],
            isError=is_error
        )
    
    @classmethod
    def error(cls, message: str) -> "ToolCallResult":
        """Create an error result"""
        return cls.text(message, is_error=True)


@dataclass
class ResourceDefinition:
    """MCP Resource definition"""
    uri: str
    name: str
    description: Optional[str] = None
    mimeType: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "uri": self.uri,
            "name": self.name,
        }
        if self.description:
            result["description"] = self.description
        if self.mimeType:
            result["mimeType"] = self.mimeType
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResourceDefinition":
        return cls(
            uri=data["uri"],
            name=data["name"],
            description=data.get("description"),
            mimeType=data.get("mimeType")
        )


@dataclass
class ResourceContent:
    """Content of a resource"""
    uri: str
    text: Optional[str] = None
    blob: Optional[str] = None  # base64 encoded
    mimeType: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"uri": self.uri}
        if self.text is not None:
            result["text"] = self.text
        if self.blob is not None:
            result["blob"] = self.blob
        if self.mimeType:
            result["mimeType"] = self.mimeType
        return result


@dataclass
class MCPMessage:
    """Base MCP message (JSON-RPC 2.0)"""
    jsonrpc: str = "2.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return {"jsonrpc": self.jsonrpc}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class MCPRequest(MCPMessage):
    """MCP Request message"""
    id: Union[str, int] = field(default_factory=lambda: str(uuid.uuid4()))
    method: str = ""
    params: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "jsonrpc": self.jsonrpc,
            "id": self.id,
            "method": self.method,
        }
        if self.params is not None:
            result["params"] = self.params
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPRequest":
        return cls(
            jsonrpc=data.get("jsonrpc", "2.0"),
            id=data.get("id", str(uuid.uuid4())),
            method=data.get("method", ""),
            params=data.get("params")
        )


@dataclass
class MCPResponse(MCPMessage):
    """MCP Response message"""
    id: Union[str, int] = ""
    result: Optional[Any] = None
    error: Optional[MCPError] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "jsonrpc": self.jsonrpc,
            "id": self.id,
        }
        if self.error is not None:
            result["error"] = self.error.to_dict()
        else:
            result["result"] = self.result
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPResponse":
        error_data = data.get("error")
        return cls(
            jsonrpc=data.get("jsonrpc", "2.0"),
            id=data.get("id", ""),
            result=data.get("result"),
            error=MCPError.from_dict(error_data) if error_data else None
        )
    
    @classmethod
    def success(cls, id: Union[str, int], result: Any) -> "MCPResponse":
        return cls(id=id, result=result)
    
    @classmethod
    def failure(cls, id: Union[str, int], code: int, message: str, data: Any = None) -> "MCPResponse":
        return cls(id=id, error=MCPError(code=code, message=message, data=data))


@dataclass
class MCPNotification(MCPMessage):
    """MCP Notification message (no response expected)"""
    method: str = ""
    params: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "jsonrpc": self.jsonrpc,
            "method": self.method,
        }
        if self.params is not None:
            result["params"] = self.params
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPNotification":
        return cls(
            jsonrpc=data.get("jsonrpc", "2.0"),
            method=data.get("method", ""),
            params=data.get("params")
        )


@dataclass
class ServerCapabilities:
    """Server capabilities advertised during initialization"""
    tools: Optional[Dict[str, Any]] = None
    resources: Optional[Dict[str, Any]] = None
    prompts: Optional[Dict[str, Any]] = None
    logging: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.tools is not None:
            result["tools"] = self.tools
        if self.resources is not None:
            result["resources"] = self.resources
        if self.prompts is not None:
            result["prompts"] = self.prompts
        if self.logging is not None:
            result["logging"] = self.logging
        return result


@dataclass
class ClientCapabilities:
    """Client capabilities sent during initialization"""
    roots: Optional[Dict[str, Any]] = None
    sampling: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.roots is not None:
            result["roots"] = self.roots
        if self.sampling is not None:
            result["sampling"] = self.sampling
        return result


@dataclass
class InitializeParams:
    """Parameters for initialize request"""
    protocolVersion: str
    capabilities: ClientCapabilities
    clientInfo: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "protocolVersion": self.protocolVersion,
            "capabilities": self.capabilities.to_dict(),
            "clientInfo": self.clientInfo
        }


@dataclass
class InitializeResult:
    """Result of initialize request"""
    protocolVersion: str
    capabilities: ServerCapabilities
    serverInfo: Dict[str, str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InitializeResult":
        caps_data = data.get("capabilities", {})
        return cls(
            protocolVersion=data.get("protocolVersion", MCPVersion.CURRENT),
            capabilities=ServerCapabilities(
                tools=caps_data.get("tools"),
                resources=caps_data.get("resources"),
                prompts=caps_data.get("prompts"),
                logging=caps_data.get("logging")
            ),
            serverInfo=data.get("serverInfo", {})
        )


class MCPProtocol(ABC):
    """Abstract base class for MCP protocol handlers"""
    
    @abstractmethod
    async def send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a request and wait for response"""
        pass
    
    @abstractmethod
    async def send_notification(self, method: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Send a notification (no response expected)"""
        pass
    
    @abstractmethod
    async def receive(self) -> MCPMessage:
        """Receive next message"""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the connection"""
        pass
