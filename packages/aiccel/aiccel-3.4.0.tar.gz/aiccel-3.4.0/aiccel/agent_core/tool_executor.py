# aiccel/agent_core/tool_executor.py
"""
Tool Executor Module
=====================

Handles tool selection, validation, and execution.
Split from agent.py for maintainability.
"""

import re
import json
import asyncio
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from cachetools import TTLCache

from ..logging_config import get_logger
from ..errors import ToolError, ToolNotFoundError, ToolExecutionError, ToolValidationError

logger = get_logger("tool_executor")


@dataclass
class ToolExecutionResult:
    """Result of tool execution."""
    tool_name: str
    args: Dict[str, Any]
    output: Any
    success: bool
    error: Optional[str] = None
    duration_ms: float = 0.0
    cached: bool = False


class ToolExecutor:
    """
    Handles tool selection, validation, and execution.
    
    Features:
    - Result caching
    - Retry logic
    - Failure tracking
    - Validation
    """
    
    def __init__(
        self,
        tool_registry=None,
        llm_provider=None,
        logger_instance=None,
        strict_mode: bool = False,
        cache_ttl: int = 300,
        max_retries: int = 2
    ):
        self.tool_registry = tool_registry
        self.llm_provider = llm_provider
        self.agent_logger = logger_instance
        self.strict_mode = strict_mode
        self.max_retries = max_retries
        
        # Caches
        self._result_cache = TTLCache(maxsize=100, ttl=cache_ttl)
        self._tool_failures: Dict[str, int] = {}
        self._max_failures = 3
    
    def get_tools(self) -> List[Any]:
        """Get all available tools."""
        if self.tool_registry:
            return self.tool_registry.get_tools()
        return []
    
    def get_tool(self, name: str) -> Optional[Any]:
        """Get a specific tool by name."""
        if self.tool_registry:
            if hasattr(self.tool_registry, 'get_tool'):
                return self.tool_registry.get_tool(name)
            return self.tool_registry.get(name)
        return None
    
    def find_relevant_tools(self, query: str) -> List[Any]:
        """Find tools relevant to the query."""
        if self.tool_registry and hasattr(self.tool_registry, 'find_relevant_tools'):
            return self.tool_registry.find_relevant_tools(query)
        return self.get_tools()
    
    def should_skip_tool(self, tool_name: str) -> bool:
        """Check if tool should be skipped due to repeated failures."""
        return self._tool_failures.get(tool_name, 0) >= self._max_failures
    
    def record_failure(self, tool_name: str):
        """Record a tool failure."""
        self._tool_failures[tool_name] = self._tool_failures.get(tool_name, 0) + 1
        logger.warning(f"Tool failure recorded: {tool_name} ({self._tool_failures[tool_name]}/{self._max_failures})")
    
    def record_success(self, tool_name: str):
        """Reset failure count on success."""
        if tool_name in self._tool_failures:
            del self._tool_failures[tool_name]
    
    def generate_cache_key(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Generate consistent cache key for tool execution."""
        args_str = json.dumps(args, sort_keys=True, default=str)
        return hashlib.md5(f"{tool_name}:{args_str}".encode()).hexdigest()
    
    def execute(
        self,
        tool_name: str,
        args: Dict[str, Any],
        use_cache: bool = True,
        trace_id: Optional[int] = None
    ) -> ToolExecutionResult:
        """
        Execute a tool with caching support.
        
        Args:
            tool_name: Name of the tool
            args: Tool arguments
            use_cache: Whether to use caching
            trace_id: Trace ID for logging
            
        Returns:
            ToolExecutionResult
        """
        import time
        start = time.perf_counter()
        
        # Check cache
        cache_key = self.generate_cache_key(tool_name, args)
        if use_cache and cache_key in self._result_cache:
            cached = self._result_cache[cache_key]
            logger.debug(f"Cache hit for {tool_name}")
            return ToolExecutionResult(
                tool_name=tool_name,
                args=args,
                output=cached,
                success=True,
                cached=True,
                duration_ms=(time.perf_counter() - start) * 1000
            )
        
        # Check if should skip
        if self.should_skip_tool(tool_name):
            return ToolExecutionResult(
                tool_name=tool_name,
                args=args,
                output=None,
                success=False,
                error=f"Tool {tool_name} skipped due to repeated failures"
            )
        
        # Get tool
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolExecutionResult(
                tool_name=tool_name,
                args=args,
                output=None,
                success=False,
                error=f"Tool not found: {tool_name}"
            )
        
        # Validate args
        validated_args = self._validate_and_fix_args(tool, args)
        
        # Execute with retry
        last_error = None
        import inspect
        
        for attempt in range(self.max_retries + 1):
            try:
                if hasattr(tool, 'execute'):
                    # Check for legacy signature execute(args)
                    sig = inspect.signature(tool.execute)
                    params = list(sig.parameters.values())
                    if len(params) == 1 and params[0].name == 'args':
                         result = tool.execute(validated_args)
                    else:
                         result = tool.execute(**validated_args)
                elif callable(tool):
                    result = tool(**validated_args)
                else:
                    raise ToolExecutionError(f"Tool {tool_name} is not executable")
                
                # Success
                duration_ms = (time.perf_counter() - start) * 1000
                self.record_success(tool_name)
                
                # Cache result
                if use_cache:
                    self._result_cache[cache_key] = result
                
                if self.agent_logger and trace_id is not None:
                    self.agent_logger.trace_step(trace_id, f"Tool {tool_name} executed", {
                        "duration_ms": duration_ms,
                        "cached": False
                    })
                
                return ToolExecutionResult(
                    tool_name=tool_name,
                    args=validated_args,
                    output=result,
                    success=True,
                    duration_ms=duration_ms
                )
                
            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    logger.warning(f"Tool {tool_name} failed (attempt {attempt + 1}): {e}")
                    continue
        
        # All retries failed
        self.record_failure(tool_name)
        duration_ms = (time.perf_counter() - start) * 1000
        
        return ToolExecutionResult(
            tool_name=tool_name,
            args=args,
            output=None,
            success=False,
            error=last_error,
            duration_ms=duration_ms
        )
    
    async def execute_async(
        self,
        tool_name: str,
        args: Dict[str, Any],
        use_cache: bool = True,
        trace_id: Optional[int] = None
    ) -> ToolExecutionResult:
        """Execute tool asynchronously."""
        tool = self.get_tool(tool_name)
        
        if tool and hasattr(tool, 'execute_async'):
            # True async execution
            import time
            start = time.perf_counter()
            
            try:
                result = await tool.execute_async(**args)
                
                return ToolExecutionResult(
                    tool_name=tool_name,
                    args=args,
                    output=result,
                    success=True,
                    duration_ms=(time.perf_counter() - start) * 1000
                )
            except Exception as e:
                return ToolExecutionResult(
                    tool_name=tool_name,
                    args=args,
                    output=None,
                    success=False,
                    error=str(e)
                )
        
        # Fallback to sync in executor
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, lambda: self.execute(tool_name, args, use_cache, trace_id)
        )
    
    def parse_tool_calls(self, response: str, query: str = "") -> List[Tuple[str, Dict[str, Any]]]:
        """
        Parse tool usage from LLM response.
        
        Args:
            response: LLM response text
            query: Original query for context
            
        Returns:
            List of (tool_name, tool_args) tuples
        """
        tool_calls = []
        
        # Helper to process extracted data
        def process_data(data):
            found = []
            if isinstance(data, dict):
                if self._is_valid_tool_call(data):
                    tool_name = data.get('tool') or data.get('name') or data.get('function')
                    args = data.get('args') or data.get('arguments') or data.get('parameters') or {}
                    found.append((tool_name, args))
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and self._is_valid_tool_call(item):
                        tool_name = item.get('tool') or item.get('name') or item.get('function')
                        args = item.get('args') or item.get('arguments') or item.get('parameters') or {}
                        found.append((tool_name, args))
            return found

        # 1. Try parsing extracted code blocks
        json_pattern = r'```(?:json)?\s*([\[\{].*?[\]\}])\s*```'
        matches = re.findall(json_pattern, response, re.DOTALL)
        for match in matches:
            try:
                data = json.loads(match)
                tool_calls.extend(process_data(data))
            except json.JSONDecodeError:
                continue
        
        if tool_calls:
            return tool_calls

        # 2. Try parsing the whole response (cleaning markdown)
        clean_response = response.strip()
        if clean_response.startswith("```"):
             # Remove first line if it starts with ```
             clean_response = re.sub(r'^```\w*\s*', '', clean_response)
        if clean_response.endswith("```"):
             clean_response = re.sub(r'\s*```$', '', clean_response)
        
        try:
            data = json.loads(clean_response)
            tool_calls.extend(process_data(data))
        except json.JSONDecodeError:
             pass

        if tool_calls:
            return tool_calls

        # 3. Aggressive search for [...] or {...}
        try:
            # Find outermost brackets
            start_list = response.find('[')
            end_list = response.rfind(']')
            if start_list != -1 and end_list != -1 and end_list > start_list:
                try:
                    data = json.loads(response[start_list:end_list+1])
                    tool_calls.extend(process_data(data))
                except Exception:
                    pass
            
            if not tool_calls:
                start_dict = response.find('{')
                end_dict = response.rfind('}')
                if start_dict != -1 and end_dict != -1 and end_dict > start_dict:
                    try:
                        data = json.loads(response[start_dict:end_dict+1])
                        tool_calls.extend(process_data(data))
                    except Exception:
                        pass
        except Exception:
            pass

        return tool_calls
    
    def _is_valid_tool_call(self, data: Any) -> bool:
        """Validate tool call structure."""
        if not isinstance(data, dict):
            return False
        
        tool_name = data.get('tool') or data.get('name') or data.get('function')
        if not tool_name:
            return False
        
        # Check if tool exists
        if self.strict_mode and not self.get_tool(tool_name):
            return False
        
        return True
    
    def _validate_and_fix_args(self, tool: Any, args: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix tool arguments."""
        if not args:
            return {}
        
        # Get expected parameters
        params = {}
        
        # 1. Try standard protocol (to_dict)
        if hasattr(tool, 'to_dict'):
            try:
                tool_def = tool.to_dict()
                properties = tool_def.get('parameters', {}).get('properties', {})
                # Normalize to simple dict
                for name, schema in properties.items():
                    params[name] = schema
            except Exception:
                pass
        
        # 2. Try list of ParameterSchema (BaseTool)
        if not params and hasattr(tool, '_parameters') and isinstance(tool._parameters, list):
             for param in tool._parameters:
                 params[param.name] = param.to_dict()

        # 3. Fallback to attribute
        if not params:
            raw_params = getattr(tool, 'parameters', {})
            if isinstance(raw_params, dict):
                params = raw_params
            elif isinstance(raw_params, list):
                # Handle list of dicts or objects
                for p in raw_params:
                    if hasattr(p, 'name'):
                        params[p.name] = {'required': getattr(p, 'required', False)}
                    elif isinstance(p, dict) and 'name' in p:
                        params[p['name']] = p
        
        if not params:
            return args
        
        fixed_args = dict(args)
        
        # Add missing required params with defaults
        for param_name, param_info in params.items():
            if param_name not in fixed_args:
                is_required = False
                if isinstance(param_info, dict):
                    is_required = param_info.get('required', False)
                
                if is_required:
                    # Try to infer from common aliases in args
                    # e.g. if tool expects 'location' but valid args had 'city'
                    if param_name in ('location', 'city', 'place'):
                        val = args.get('city') or args.get('place') or args.get('location')
                        if val: fixed_args[param_name] = val
                    elif param_name in ('query', 'q', 'search', 'topic'):
                         val = args.get('query') or args.get('q') or args.get('search') or args.get('topic')
                         if val: fixed_args[param_name] = val

        return fixed_args
