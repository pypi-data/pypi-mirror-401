# aiccel/agent_core/prompt_builder.py
"""
Prompt Builder Module
=====================

Centralized prompt construction with caching.
Split from agent.py for maintainability.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from cachetools import TTLCache

from ..logging_config import get_logger

logger = get_logger("prompt_builder")


@dataclass
class PromptConfig:
    """Configuration for prompt building."""
    instructions: str = "You are a helpful AI assistant."
    name: str = "Agent"
    strict_tool_usage: bool = False
    thinking_enabled: bool = False


class PromptBuilder:
    """
    Centralized prompt building with caching.
    Separates prompt logic from execution logic.
    """
    
    _prompt_cache = TTLCache(maxsize=100, ttl=3600)
    
    def __init__(self, config: PromptConfig, tools: List[Any] = None):
        self.config = config
        self.tools = tools or []
        self._tool_registry = None
    
    def set_tool_registry(self, registry):
        """Set tool registry for dynamic tool access."""
        self._tool_registry = registry
    
    def build_main_prompt(
        self,
        query: str,
        relevant_tools: List[Any],
        memory_context: str = ""
    ) -> str:
        """
        Build main execution prompt with tools and context.
        
        Args:
            query: User query
            relevant_tools: List of relevant tools
            memory_context: Conversation history
            
        Returns:
            Complete prompt string
        """
        # Build static parts with caching
        cache_key = self._get_cache_key(relevant_tools)
        
        if cache_key in self._prompt_cache:
            static_parts = self._prompt_cache[cache_key]
        else:
            static_parts = self._build_static_parts(relevant_tools)
            self._prompt_cache[cache_key] = static_parts
        
        return self._assemble_prompt(query, static_parts, memory_context, relevant_tools)
    
    def build_thinking_prompt(self, query: str, has_tools: bool = False) -> str:
        """Build prompt for thinking phase."""
        tool_mention = ""
        if has_tools:
            tool_names = [t.name for t in self.tools[:5]] if self.tools else []
            if tool_names:
                tool_mention = f"\nAvailable tools: {', '.join(tool_names)}"
        
        return f"""Analyze this query and plan your approach:
Query: {query}
{tool_mention}

Think step by step:
1. What is being asked?
2. What tools or knowledge are needed?
3. What's the best approach?

Provide your analysis concisely."""

    def build_synthesis_prompt(
        self,
        query: str,
        tool_outputs: List[Tuple[str, Dict[str, Any], str]]
    ) -> str:
        """Build prompt for synthesizing tool outputs."""
        outputs_text = "\n\n".join([
            f"**{name}** (args: {args}):\n{output}"
            for name, args, output in tool_outputs
        ])
        
        return f"""Based on the following tool outputs, provide a comprehensive response to the user's query.

Original Query: {query}

Tool Outputs:
{outputs_text}

Instructions:
- Synthesize all relevant information
- Be concise but complete
- Use natural language
- Cite sources if available"""

    def build_tool_selection_prompt(self, query: str, tools: List[Any]) -> str:
        """Build prompt for direct tool selection."""
        tool_desc = self._format_tool_descriptions(tools)
        
        return f"""Select and use the appropriate tool(s) to answer this query.

Query: {query}

Available Tools:
{tool_desc}

Respond with a JSON tool call:
```json
{{"tool": "tool_name", "args": {{"param": "value"}}}}
```"""

    def _build_static_parts(self, relevant_tools: List[Any]) -> Dict[str, str]:
        """Build static parts of prompt (cached)."""
        return {
            "instructions": self.config.instructions,
            "tool_usage": self._build_tool_usage_instructions(relevant_tools),
            "tool_descriptions": self._format_tool_descriptions(relevant_tools),
        }
    
    def _build_tool_usage_instructions(self, tools: List[Any]) -> str:
        """Build instructions for tool usage."""
        if not tools:
            return ""
        
        return """
To use tools, respond with a JSON list of tool calls. You can call multiple tools or the same tool multiple times in parallel to answer different parts of the query.
Format:
```json
[
  {"tool": "tool_name", "args": {"param": "value"}},
  {"tool": "another_tool", "args": {"param": "value"}}
]
```
Use tools whenever you need to fetch outside information. If you use a search tool, ALWAYS include the URLs from the search results in your final answer.
If no tool is needed, provide a direct and helpful answer.

Only use tools when necessary. Provide direct answers when possible."""

    def _assemble_prompt(
        self,
        query: str,
        static_parts: Dict[str, str],
        memory_context: str,
        relevant_tools: List[Any]
    ) -> str:
        """Assemble final prompt from parts."""
        parts = [f"# Instructions\n{static_parts['instructions']}"]
        
        if relevant_tools:
            parts.append(f"\n# Available Tools\n{static_parts['tool_descriptions']}")
            parts.append(static_parts['tool_usage'])
        
        if memory_context:
            parts.append(f"\n# Conversation History\n{memory_context}")
        
        parts.append(f"\n# Current Query\n{query}")
        
        return "\n".join(parts)
    
    def _format_tool_descriptions(self, tools: List[Any]) -> str:
        """Format tool descriptions."""
        if not tools:
            return "No tools available."
        
        import json
        descriptions = []
        for tool in tools:
            # Prefer standard to_dict() protocol
            if hasattr(tool, 'to_dict'):
                try:
                    tool_def = tool.to_dict()
                    name = tool_def.get('name', 'Unknown')
                    desc = tool_def.get('description', '')
                    params = tool_def.get('parameters', {})
                except Exception:
                    # Fallback if to_dict fails
                    name = getattr(tool, 'name', str(tool))
                    desc = getattr(tool, 'description', 'No description')
                    params = getattr(tool, 'parameters', {})
            else:
                name = getattr(tool, 'name', str(tool))
                desc = getattr(tool, 'description', 'No description')
                params = getattr(tool, 'parameters', {})
            
            param_text = ""
            if params:
                # Pretty print parameters for the LLM to understand structure
                if isinstance(params, dict) or isinstance(params, list):
                    param_text = f"\n  Parameters: {json.dumps(params)}"
                else:
                    param_text = f"\n  Parameters: {params}"
            
            descriptions.append(f"- **{name}**: {desc}{param_text}")
        
        return "\n".join(descriptions)
    
    def _get_cache_key(self, tools: List[Any]) -> str:
        """Generate cache key for prompt."""
        tool_names = tuple(getattr(t, 'name', str(t)) for t in tools)
        return f"{self.config.name}:{self.config.instructions[:50]}:{tool_names}"
