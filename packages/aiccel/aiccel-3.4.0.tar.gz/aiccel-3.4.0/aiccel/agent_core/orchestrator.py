# aiccel/agent_core/orchestrator.py
"""
Execution Orchestrator Module
==============================

Orchestrates the execution flow of the agent.
Handles thinking, tool execution, and response synthesis.
Split from agent.py for maintainability.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from ..logging_config import get_logger, Colors
from ..errors import ExecutionError, ProviderError

logger = get_logger("orchestrator")


@dataclass
class ExecutionContext:
    """Context for agent execution."""
    query: str
    trace_id: int
    has_tools: bool = False
    relevant_tools: List[Any] = field(default_factory=list)
    thinking_enabled: bool = False
    start_time: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_ms(self) -> float:
        return (time.time() - self.start_time) * 1000


@dataclass
class ExecutionResult:
    """Result of orchestrated execution."""
    response: str
    thinking: Optional[str] = None
    tool_calls: List[Tuple[str, Dict[str, Any]]] = field(default_factory=list)
    tool_outputs: List[Tuple[str, Dict[str, Any], str]] = field(default_factory=list)
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "response": self.response,
            "thinking": self.thinking,
            "tools_used": self.tool_calls,
            "tool_outputs": self.tool_outputs,
            "execution_time": self.execution_time_ms,
            "metadata": self.metadata
        }


class ExecutionOrchestrator:
    """
    Orchestrates the execution flow of the agent.
    
    Flow:
    1. Thinking phase (optional)
    2. Tool selection and execution
    3. Response synthesis
    """
    
    def __init__(
        self,
        llm_provider,
        tool_executor,
        prompt_builder,
        memory=None,
        agent_logger=None,
        config=None,
        fallback_providers: List = None
    ):
        self.llm_provider = llm_provider
        self.tool_executor = tool_executor
        self.prompt_builder = prompt_builder
        self.memory = memory
        self.agent_logger = agent_logger
        self.config = config
        self.fallback_providers = fallback_providers or []
    
    def execute(self, query: str, context: ExecutionContext) -> ExecutionResult:
        """
        Execute query with full orchestration.
        
        Args:
            query: User query
            context: Execution context
            
        Returns:
            ExecutionResult with response and metadata
        """
        start_time = time.perf_counter()
        thinking = None
        tool_calls = []
        tool_outputs = []
        
        try:
            # Phase 1: Thinking (optional)
            if context.thinking_enabled:
                thinking = self._execute_thinking_phase(query, context)
                if self.agent_logger and self.agent_logger.verbose and thinking:
                     print(f"{Colors.BLUE}›{Colors.RESET} Thinking process:\n{Colors.DIM}{thinking}{Colors.RESET}")

            # Phase 2: Generate initial response
            response = self._generate_response(query, context, thinking)
            
            # Phase 3: Parse and execute tool calls
            parsed_tools = self.tool_executor.parse_tool_calls(response, query)
            
            if parsed_tools:
                # Visual feedback
                if self.agent_logger and self.agent_logger.verbose:
                    tool_names = ', '.join([t[0] for t in parsed_tools])
                    print(f"{Colors.BLUE}›{Colors.RESET} Agent selected tools: {Colors.BOLD}{tool_names}{Colors.RESET}")
                
                for tool_name, tool_args in parsed_tools:
                    if self.agent_logger and self.agent_logger.verbose:
                        print(f"  {Colors.DIM}└─{Colors.RESET} Executing {Colors.CYAN}{tool_name}{Colors.RESET}...")
                    
                    result = self.tool_executor.execute(
                        tool_name, tool_args, 
                        trace_id=context.trace_id
                    )
                    
                    tool_calls.append((tool_name, tool_args))
                    tool_outputs.append((
                        tool_name, 
                        tool_args, 
                        str(result.output) if result.success else result.error
                    ))
                
                # Phase 4: Synthesize final response
                if tool_outputs:
                    if self.agent_logger and self.agent_logger.verbose:
                        print(f"{Colors.BLUE}›{Colors.RESET} Synthesizing response...")
                    response = self._synthesize_response(query, tool_outputs)
            
            execution_time = (time.perf_counter() - start_time) * 1000
            
            # Update memory
            if self.memory:
                self.memory.add_turn(query, response)
            
            return ExecutionResult(
                response=response,
                thinking=thinking,
                tool_calls=tool_calls,
                tool_outputs=tool_outputs,
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            if self.agent_logger:
                self.agent_logger.trace_error(context.trace_id, e, "Execution failed")
            raise ExecutionError(str(e), cause=e)
    
    async def execute_async(self, query: str, context: ExecutionContext) -> ExecutionResult:
        """Execute query asynchronously."""
        start_time = time.perf_counter()
        thinking = None
        tool_calls = []
        tool_outputs = []
        
        try:
            # Phase 1: Thinking (optional)
            if context.thinking_enabled:
                thinking = await self._execute_thinking_phase_async(query, context)
                if self.agent_logger and self.agent_logger.verbose and thinking:
                     print(f"{Colors.BLUE}›{Colors.RESET} Thinking process:\n{Colors.DIM}{thinking}{Colors.RESET}")
            
            # Phase 2: Generate initial response
            response = await self._generate_response_async(query, context, thinking)
            
            # Phase 3: Parse and execute tool calls
            parsed_tools = self.tool_executor.parse_tool_calls(response, query)
            
            if parsed_tools:
                # Visual feedback
                if self.agent_logger and self.agent_logger.verbose:
                    tool_names = ', '.join([t[0] for t in parsed_tools])
                    print(f"{Colors.BLUE}›{Colors.RESET} Agent selected tools: {Colors.BOLD}{tool_names}{Colors.RESET}")
                
                # Execute tools concurrently
                tasks = [
                    self.tool_executor.execute_async(
                        tool_name, tool_args,
                        trace_id=context.trace_id
                    )
                    for tool_name, tool_args in parsed_tools
                ]
                
                if self.agent_logger and self.agent_logger.verbose:
                    print(f"  {Colors.DIM}└─{Colors.RESET} Executing tools in parallel...")
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for (tool_name, tool_args), result in zip(parsed_tools, results):
                    tool_calls.append((tool_name, tool_args))
                    
                    if isinstance(result, Exception):
                        tool_outputs.append((tool_name, tool_args, str(result)))
                        if self.agent_logger and self.agent_logger.verbose:
                            print(f"  {Colors.RED}✗{Colors.RESET} {str(tool_name)} failed")
                    else:
                        tool_outputs.append((
                            tool_name, tool_args,
                            str(result.output) if result.success else result.error
                        ))
                
                # Phase 4: Synthesize final response
                if tool_outputs:
                    if self.agent_logger and self.agent_logger.verbose:
                        print(f"{Colors.BLUE}›{Colors.RESET} Synthesizing response...")
                    response = await self._synthesize_response_async(query, tool_outputs)
            
            execution_time = (time.perf_counter() - start_time) * 1000
            
            # Update memory
            if self.memory:
                self.memory.add_turn(query, response)
            
            return ExecutionResult(
                response=response,
                thinking=thinking,
                tool_calls=tool_calls,
                tool_outputs=tool_outputs,
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            if self.agent_logger:
                self.agent_logger.trace_error(context.trace_id, e, "Async execution failed")
            raise ExecutionError(str(e), cause=e)
    
    def _execute_thinking_phase(self, query: str, context: ExecutionContext) -> Optional[str]:
        """Execute thinking phase."""
        try:
            prompt = self.prompt_builder.build_thinking_prompt(query, context.has_tools)
            thinking = self._call_llm(prompt)
            
            if self.agent_logger:
                self.agent_logger.trace_step(context.trace_id, "Thinking phase complete")
            
            return thinking
        except Exception as e:
            logger.warning(f"Thinking phase failed: {e}")
            return None
    
    async def _execute_thinking_phase_async(self, query: str, context: ExecutionContext) -> Optional[str]:
        """Execute thinking phase asynchronously."""
        try:
            prompt = self.prompt_builder.build_thinking_prompt(query, context.has_tools)
            thinking = await self._call_llm_async(prompt)
            return thinking
        except Exception:
            return None
    
    def _generate_response(
        self,
        query: str,
        context: ExecutionContext,
        thinking: Optional[str] = None
    ) -> str:
        """Generate initial LLM response."""
        memory_context = ""
        if self.memory:
            memory_context = self.memory.get_formatted_history()
        
        prompt = self.prompt_builder.build_main_prompt(
            query, context.relevant_tools, memory_context
        )
        
        return self._call_llm(prompt)
    
    async def _generate_response_async(
        self,
        query: str,
        context: ExecutionContext,
        thinking: Optional[str] = None
    ) -> str:
        """Generate initial LLM response asynchronously."""
        memory_context = ""
        if self.memory:
            memory_context = self.memory.get_formatted_history()
        
        prompt = self.prompt_builder.build_main_prompt(
            query, context.relevant_tools, memory_context
        )
        
        return await self._call_llm_async(prompt)
    
    def _synthesize_response(
        self,
        query: str,
        tool_outputs: List[Tuple[str, Dict[str, Any], str]]
    ) -> str:
        """Synthesize final response from tool outputs."""
        prompt = self.prompt_builder.build_synthesis_prompt(query, tool_outputs)
        return self._call_llm(prompt)
    
    async def _synthesize_response_async(
        self,
        query: str,
        tool_outputs: List[Tuple[str, Dict[str, Any], str]]
    ) -> str:
        """Synthesize final response asynchronously."""
        prompt = self.prompt_builder.build_synthesis_prompt(query, tool_outputs)
        return await self._call_llm_async(prompt)
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM with fallback support."""
        providers = [self.llm_provider] + self.fallback_providers
        
        for provider in providers:
            try:
                return provider.generate(prompt)
            except Exception as e:
                logger.warning(f"Provider {type(provider).__name__} failed: {e}")
                continue
        
        raise ProviderError("All providers failed")
    
    async def _call_llm_async(self, prompt: str) -> str:
        """Call LLM asynchronously with fallback support."""
        providers = [self.llm_provider] + self.fallback_providers
        
        for provider in providers:
            try:
                if hasattr(provider, 'generate_async'):
                    return await provider.generate_async(prompt)
                else:
                    # Fallback to sync in executor
                    loop = asyncio.get_running_loop()
                    return await loop.run_in_executor(
                        None, provider.generate, prompt
                    )
            except Exception as e:
                logger.warning(f"Async provider {type(provider).__name__} failed: {e}")
                continue
        
        raise ProviderError("All providers failed")
