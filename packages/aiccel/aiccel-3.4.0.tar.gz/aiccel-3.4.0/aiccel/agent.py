# aiccel/agent_slim.py
"""
Slim Agent Implementation
==========================

Lightweight, fast agent using modular architecture.

Features:
- Fast startup with lazy imports
- Uses agent_core modules
- Memory efficient
- Async-first design
"""

from __future__ import annotations
import asyncio
import time
from typing import Dict, Any, List, Optional, Union, TYPE_CHECKING
from dataclasses import dataclass, field

# Lazy imports for fast startup
if TYPE_CHECKING:
    from .providers import LLMProvider
    from .tools import Tool, ToolRegistry
    from .conversation_memory import ConversationMemory

from .logging_config import get_logger, AgentLogger


from .core import AgentConfig

# Re-export AgentConfig for backward compatibility
# AgentConfig is now imported from .core to avoid duplication

class Agent:
    """
    Lightweight, high-performance AI agent with tool execution and memory.
    
    The Agent class is the core component of the aiccel framework. It provides:
    - Multi-provider LLM support (OpenAI, Gemini, Groq)
    - Tool execution with automatic argument parsing
    - Conversation memory with multiple strategies
    - Async-first design with sync wrappers
    - Lazy initialization for fast startup (~50ms)
    
    Attributes:
        provider: The LLM provider instance (GeminiProvider, OpenAIProvider, etc.)
        tools: List of Tool instances available to the agent
        config: AgentConfig instance with all settings
        memory: ConversationMemory instance (lazily initialized)
        logger: AgentLogger instance for tracing and debugging
    
    Example:
        Basic usage with tools:
        
        >>> from aiccel import Agent, GeminiProvider, SearchTool
        >>> 
        >>> provider = GeminiProvider(api_key="your-key")
        >>> search = SearchTool(api_key="serper-key")
        >>> 
        >>> agent = Agent(
        ...     provider=provider,
        ...     tools=[search],
        ...     name="ResearchAgent",
        ...     instructions="Help users find information.",
        ...     verbose=True
        ... )
        >>> 
        >>> result = agent.run("What is the latest news about AI?")
        >>> print(result["response"])
        
        Async usage:
        
        >>> import asyncio
        >>> result = asyncio.run(agent.run_async("Search for Python tutorials"))
        
        Chaining:
        
        >>> agent = Agent(provider=provider).add_tool(search).enable_thinking()
    
    See Also:
        - AgentManager: For multi-agent orchestration
        - AgentConfig: For configuration options
        - Tool: Base class for creating custom tools
    """
    
    # __slots__ removed to allow dynamic attribute injection by AgentManager

    def __init__(
        self,
        provider: 'LLMProvider',
        tools: Optional[List['Tool']] = None,
        config: Optional[AgentConfig] = None,
        name: str = "Agent",
        instructions: str = "",
        description: str = "",
        memory_type: str = "buffer",
        max_memory_turns: int = 10,
        max_memory_tokens: int = 4000,
        strict_tool_usage: bool = False,
        verbose: bool = False,
        **kwargs
    ):
        """
        Initialize an AI Agent.
        
        Args:
            provider: LLM provider instance (required). Must implement the LLMProvider interface.
            tools: List of Tool instances. Default: None (no tools).
            config: Pre-built AgentConfig. If provided, overrides individual params.
            name: Agent name for logging and identification.
            instructions: System prompt defining agent behavior.
            description: Brief description for AgentManager routing.
            memory_type: Memory strategy. Options: 'buffer', 'summary', 'window', 'none'.
            max_memory_turns: Max conversation turns to keep.
            max_memory_tokens: Max tokens for memory context.
            strict_tool_usage: Force tool usage for all responses.
            verbose: Enable detailed console logging.
            **kwargs: Additional arguments for extensibility.
        
        Raises:
            ValueError: If provider is None.
            TypeError: If tools is not a list.
        
        Example:
            >>> agent = Agent(
            ...     provider=GeminiProvider(),
            ...     tools=[SearchTool(), WeatherTool()],
            ...     name="MyAgent",
            ...     verbose=True
            ... )
        """
        self.provider = provider
        self.tools = tools or []
        
        # Build config from params or use provided
        if config:
            self.config = config
        else:
            self.config = AgentConfig(
                name=name,
                instructions=instructions or "You are a helpful AI assistant.",
                description=description,
                memory_type=memory_type,
                max_memory_turns=max_memory_turns,
                max_memory_tokens=max_memory_tokens,
                strict_tool_usage=strict_tool_usage,
                verbose=verbose
            )
            
            # Store any extra kwargs in config if needed, or just attached to agent
            # For flexibility, we can attach arbitrary kwargs to config instance
            for k, v in kwargs.items():
                if not hasattr(self.config, k):
                     setattr(self.config, k, v)
        
        self.logger = AgentLogger(self.config.name, verbose=self.config.verbose)
        self.memory = None
        self._tool_executor = None
        self._tool_registry = None  # Store registry reference
        self._prompt_builder = None
        self._orchestrator = None
        self._initialized = False
        
        # Log initialization
        self.logger.info(
            f"Agent '{self.config.name}' initialized with {len(self.tools)} tools. "
            f"Strict mode: {self.config.strict_tool_usage}"
        )
    
    def _lazy_init(self):
        """Lazy initialization of heavy components."""
        if self._initialized:
            return
        
        # Import only when needed
        from .conversation_memory import ConversationMemory
        from .agent_core import PromptBuilder, ToolExecutor, ExecutionOrchestrator, PromptConfig
        from .tools.registry import ToolRegistry
        
        # Initialize memory
        self.memory = ConversationMemory(
            memory_type=self.config.memory_type,
            max_turns=self.config.max_memory_turns,
            max_tokens=self.config.max_memory_tokens
        )
        
        # Validate tools list vs registry
        self._tool_registry = ToolRegistry(llm_provider=self.provider)
        for tool in self.tools:
            self._tool_registry.register(tool)
        
        # Initialize components
        prompt_config = PromptConfig(
            name=self.config.name,
            instructions=self.config.instructions,
            strict_tool_usage=self.config.strict_tool_usage
        )
        
        self._prompt_builder = PromptBuilder(prompt_config, self.tools)
        self._tool_executor = ToolExecutor(
            tool_registry=self._tool_registry,
            llm_provider=self.provider,
            logger_instance=self.logger,
            strict_mode=self.config.strict_tool_usage
        )
        self._orchestrator = ExecutionOrchestrator(
            llm_provider=self.provider,
            tool_executor=self._tool_executor,
            prompt_builder=self._prompt_builder,
            memory=self.memory,
            agent_logger=self.logger
        )
        
        self._initialized = True
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Run agent synchronously.
        
        Args:
            query: User query
            
        Returns:
            Response dict with 'response', 'thinking', 'tools_used', etc.
            
        Raises:
            ValueError: If query is None, empty, or exceeds max length.
        """
        # Input validation
        if query is None:
            raise ValueError("Query cannot be None")
        if not isinstance(query, str):
            query = str(query)
        query = query.strip()
        if not query:
            raise ValueError("Query cannot be empty")
        
        # Limit query length to prevent memory issues (100KB max)
        max_query_length = 100_000
        if len(query) > max_query_length:
            self.logger.warning(f"Query truncated from {len(query)} to {max_query_length} chars")
            query = query[:max_query_length]
        
        # Security: Check for jailbreak attempts if enabled
        if self.config.safety_enabled and not self.config.lightweight:
            from .jailbreak import check_prompt
            if not check_prompt(query):
                 return {
                    "response": "I cannot fulfill this request due to security policies.",
                    "thinking": None,
                    "tools_used": [],
                    "tool_outputs": [],
                    "error": "Jailbreak attempt detected"
                }
            
        self._lazy_init()
        
        trace_id = self.logger.trace_start("agent_run", {"query": query})
        start = time.perf_counter()
        
        try:
            from .agent_core import ExecutionContext
            
            context = ExecutionContext(
                query=query,
                trace_id=trace_id,
                has_tools=bool(self.tools),
                relevant_tools=self._tool_executor.find_relevant_tools(query) if self.tools else [],
                thinking_enabled=self.config.thinking_enabled
            )
            
            result = self._orchestrator.execute(query, context)
            
            execution_time = (time.perf_counter() - start) * 1000
            self.logger.trace_end(trace_id, {"execution_time_ms": execution_time})
            
            return result.to_dict()
            
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Agent execution failed")
            # Return error response instead of crashing
            return {
                "response": f"I encountered an error while processing your request: {str(e)}",
                "thinking": None,
                "tools_used": [],
                "tool_outputs": [],
                "error": str(e)
            }
    
    async def run_async(self, query: str) -> Dict[str, Any]:
        """Run agent asynchronously."""
        if self.config.safety_enabled and not self.config.lightweight:
            from .jailbreak import check_prompt
            loop = asyncio.get_running_loop()
            is_safe = await loop.run_in_executor(None, check_prompt, query)
            if not is_safe:
                 return {
                    "response": "I cannot fulfill this request due to security policies.",
                    "thinking": None,
                    "tools_used": [],
                    "tool_outputs": [],
                    "error": "Jailbreak attempt detected"
                }
            
        self._lazy_init()
        
        trace_id = self.logger.trace_start("agent_run_async", {"query": query})
        start = time.perf_counter()
        
        try:
            from .agent_core import ExecutionContext
            
            context = ExecutionContext(
                query=query,
                trace_id=trace_id,
                has_tools=bool(self.tools),
                relevant_tools=self._tool_executor.find_relevant_tools(query) if self.tools else [],
                thinking_enabled=self.config.thinking_enabled
            )
            
            result = await self._orchestrator.execute_async(query, context)
            
            execution_time = (time.perf_counter() - start) * 1000
            self.logger.trace_end(trace_id, {"execution_time_ms": execution_time})
            
            return result.to_dict()
            
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Async execution failed")
            # Return error response instead of crashing
            return {
                "response": f"I encountered an error while processing your request: {str(e)}",
                "thinking": None,
                "tools_used": [],
                "tool_outputs": [],
                "error": str(e)
            }
    
    async def stream(self, query: str):
        """
        Stream agent response.
        
        Usage:
            async for chunk in agent.stream("Tell me a story"):
                print(chunk, end='', flush=True)
        """
        self._lazy_init()
        
        # Check if provider supports streaming
        if hasattr(self.provider, 'generate_stream'):
            prompt = self._prompt_builder.build_main_prompt(
                query, 
                self._tool_executor.find_relevant_tools(query) if self.tools else [],
                self.memory.get_formatted_history() if self.memory else ""
            )
            
            async for chunk in self.provider.generate_stream(prompt):
                yield chunk
        else:
            # Fallback to non-streaming
            result = await self.run_async(query)
            yield result['response']
    
    def enable_thinking(self, enabled: bool = True) -> 'Agent':
        """Enable/disable thinking mode. Returns self for chaining."""
        self.config.thinking_enabled = enabled
        return self
    
    def add_tool(self, tool: 'Tool') -> 'Agent':
        """Add a tool. Returns self for chaining."""
        self.tools.append(tool)
        self._initialized = False  # Force reinit
        return self
    
    def clear_memory(self):
        """Clear conversation memory."""
        if self.memory:
            self.memory.clear()
    
    def get_memory(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        if self.memory:
            return self.memory.get_history()
        return []
    
    def set_verbose(self, verbose: bool):
        """Set verbose mode."""
        self.config.verbose = verbose
        self.logger.verbose = verbose
        
    def with_tool(self, tool: 'Tool') -> 'Agent':
        """Alias for add_tool for backward compatibility."""
        return self.add_tool(tool)
        
    def sync_tools_to_registry(self):
        """Force registry update. Backward compatibility."""
        self._initialized = False
        self._lazy_init()
        
    @property
    def tool_registry(self):
        """Access tool registry. Initializes if needed."""
        self._lazy_init()
        return self._tool_registry

    def __repr__(self) -> str:
        return f"<Agent(name='{self.config.name}', tools={len(self.tools)})>"


# Convenience function
def create_agent(
    provider: 'LLMProvider',
    tools: Optional[List['Tool']] = None,
    **kwargs
) -> Agent:
    """Create a slim agent with sensible defaults."""
    return Agent(provider=provider, tools=tools, **kwargs)
