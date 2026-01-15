# aiccel/tools_unified/registry.py
"""
Tool Registry
==============

Central registry for tool management with smart selection.
"""

import re
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field

from .protocol import ToolProtocol, ToolSchema
from .base import BaseTool
from ..logging_config import get_logger

logger = get_logger("tool_registry")


class ToolRegistry:
    """
    Central registry for managing tools.
    
    Features:
    - Tool registration and lookup
    - Smart tool selection based on query
    - Tag-based filtering
    - LLM-based tool matching
    """
    
    def __init__(self, llm_provider=None):
        self._tools: Dict[str, ToolProtocol] = {}
        self._llm_provider = llm_provider
    
    def register(self, tool: Union[ToolProtocol, BaseTool]) -> 'ToolRegistry':
        """
        Register a tool.
        
        Args:
            tool: Tool instance to register
            
        Returns:
            Self for chaining
        """
        name = tool.name
        
        if name in self._tools:
            logger.warning(f"Overwriting existing tool: {name}")
        
        self._tools[name] = tool
        logger.debug(f"Registered tool: {name}")
        
        return self
    
    def register_many(self, tools: List[ToolProtocol]) -> 'ToolRegistry':
        """Register multiple tools."""
        for tool in tools:
            self.register(tool)
        return self
    
    def unregister(self, name: str) -> bool:
        """Unregister a tool by name."""
        if name in self._tools:
            del self._tools[name]
            return True
        return False
    
    def get(self, name: str) -> Optional[ToolProtocol]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_tool(self, name: str) -> Optional[ToolProtocol]:
        """Alias for get()."""
        return self.get(name)
    
    def get_tools(self) -> List[ToolProtocol]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def get_tool_names(self) -> List[str]:
        """Get all tool names."""
        return list(self._tools.keys())
    
    def has_tool(self, name: str) -> bool:
        """Check if tool exists."""
        return name in self._tools
    
    def count(self) -> int:
        """Get number of registered tools."""
        return len(self._tools)
    
    def find_by_tag(self, tag: str) -> List[ToolProtocol]:
        """Find tools by tag."""
        return [
            tool for tool in self._tools.values()
            if hasattr(tool, 'tags') and tag in tool.tags
        ]
    
    def find_relevant_tools(
        self,
        query: str,
        max_tools: int = 5,
        threshold: float = 0.1  # Lowered threshold to include more tools
    ) -> List[ToolProtocol]:
        """
        Find tools relevant to a query.
        
        Uses keyword matching and optionally LLM for smarter selection.
        
        Args:
            query: User query
            max_tools: Maximum tools to return
            threshold: Relevance threshold (0-1)
            
        Returns:
            List of relevant tools
        """
        if not self._tools:
            return []
        
        # Quick keyword-based matching
        scored_tools = []
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        for tool in self._tools.values():
            score = self._calculate_relevance(tool, query_lower, query_words)
            if score >= threshold:
                scored_tools.append((score, tool))
        
        # Sort by score descending
        scored_tools.sort(key=lambda x: x[0], reverse=True)
        
        # Return top tools
        return [tool for _, tool in scored_tools[:max_tools]]
    
    def _calculate_relevance(
        self,
        tool: ToolProtocol,
        query_lower: str,
        query_words: set
    ) -> float:
        """Calculate relevance score for a tool."""
        score = 0.0
        
        name = tool.name.lower()
        desc = tool.description.lower() if tool.description else ""
        
        # Name match (high weight)
        if name in query_lower:
            score += 0.5
        
        # Word overlap
        tool_words = set(re.findall(r'\w+', f"{name} {desc}"))
        overlap = len(query_words & tool_words)
        if overlap > 0:
            score += min(overlap * 0.15, 0.45)
        
        # Tag matching
        if hasattr(tool, 'tags'):
            for tag in tool.tags:
                if tag.lower() in query_lower:
                    score += 0.2
        
        # Keyword boosting
        keywords = {
            'search': ['search', 'find', 'look', 'query', 'google', 'what', 'who', 'when', 'where', 'how', 'explain', 'tell', 'show'],
            'weather': ['weather', 'temperature', 'forecast', 'climate', 'rain', 'sunny', 'cloudy'],
        }
        
        for tool_type, kws in keywords.items():
            if tool_type in name or tool_type in desc:
                for kw in kws:
                    if kw in query_lower:
                        score += 0.3
                        break
        
        return min(score, 1.0)
    
    def get_schemas(self) -> List[ToolSchema]:
        """Get schemas for all tools."""
        schemas = []
        for tool in self._tools.values():
            if hasattr(tool, 'get_schema'):
                schemas.append(tool.get_schema())
            else:
                schemas.append(ToolSchema(
                    name=tool.name,
                    description=tool.description,
                    parameters=[]
                ))
        return schemas
    
    def to_openai_functions(self) -> List[Dict[str, Any]]:
        """Convert all tools to OpenAI function calling format."""
        return [
            tool.to_openai_function() if hasattr(tool, 'to_openai_function')
            else {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": getattr(tool, 'parameters', {})
                }
            }
            for tool in self._tools.values()
        ]
    
    def clear(self):
        """Remove all tools."""
        self._tools.clear()
    
    def __len__(self) -> int:
        return len(self._tools)
    
    def __contains__(self, name: str) -> bool:
        return name in self._tools
    
    def __iter__(self):
        return iter(self._tools.values())
    
    def __repr__(self) -> str:
        return f"<ToolRegistry(tools={list(self._tools.keys())})>"
