# aiccel/orchestration/router.py
"""
Agent Router
============

Responsible for routing user queries to the most appropriate agent.
"""

from typing import List, Dict, Any, Optional, Protocol, TYPE_CHECKING
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..logger import AILogger
from ..exceptions import AgentException

if TYPE_CHECKING:
    from ..agent import Agent
    from ..providers.base import LLMProvider

class Router:
    """
    Routes queries to appropriate agents using LLM reasoning.
    """
    
    def __init__(
        self, 
        provider: 'LLMProvider',
        agents: Dict[str, Dict[str, Any]],
        logger: AILogger,
        fallback_providers: Optional[List['LLMProvider']] = None,
        instructions: str = None
    ):
        self.provider = provider
        self.agents = agents
        self.logger = logger
        self.fallback_providers = fallback_providers or []
        self.instructions = instructions or (
            "Route queries to the most appropriate agent based on their expertise and available tools. "
            "Consider the query's intent, required knowledge, and tool capabilities."
        )

    def _build_agent_descriptions(self) -> str:
        agent_descriptions = []
        for name, info in self.agents.items():
            tool_info = ""
            agent = info.get("agent")
            if agent:
                if hasattr(agent, "tool_registry") and agent.tool_registry:
                    tools = agent.tool_registry.get_all()
                    if tools:
                        tool_names = [t.name for t in tools]
                        tool_info = f" (Tools: {', '.join(tool_names)})"
            agent_descriptions.append(f"- {name}: {info['description']}{tool_info}")
        return "\n".join(agent_descriptions)

    def _select_default_agent(self) -> Optional[str]:
        """Select a default agent when routing fails."""
        if not self.agents:
            return None
        sorted_agents = sorted(self.agents.keys())
        agent_name = sorted_agents[0]
        self.logger.info(f"Selected default agent: {agent_name}")
        return agent_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def route_async(self, query: str, trace_id: int) -> str:
        """
        Determines the best agent for the query.
        Returns the agent name.
        """
        if not self.agents:
            raise ValueError("No agents available")
            
        if len(self.agents) == 1:
            agent_name = list(self.agents.keys())[0]
            self.logger.info(f"Only one agent available, routing to: {agent_name}")
            return agent_name

        agent_descriptions_text = self._build_agent_descriptions()
        routing_prompt = (
            f"Instructions: {self.instructions}\n\n"
            f"Query: {query}\n\n"
            "Available agents:\n"
            f"{agent_descriptions_text}\n\n"
            "Select the most appropriate agent to handle this query based on their expertise and tools. "
            "You MUST return only the agent name as a plain string (e.g., 'weather_expert'). "
            "Do not include any additional text, explanations, or formatting."
        )
        
        self.logger.trace_step(trace_id, "build_routing_prompt", {"prompt": routing_prompt[:200]})
        
        selected_agent = None
        providers = [self.provider] + self.fallback_providers
        
        for provider in providers:
            try:
                self.logger.info(f"Attempting async routing with provider: {type(provider).__name__}")
                selected_agent = (await provider.generate_async(routing_prompt)).strip()
                self.logger.trace_step(trace_id, "routing_decision", {
                    "provider": type(provider).__name__,
                    "selected_agent": selected_agent
                })
                
                # Validation: Check if returned string matches a key
                # Sometimes LLMs wrap in quotes or add period
                clean_agent = selected_agent.strip('"\'').rstrip('.')
                if clean_agent in self.agents:
                    selected_agent = clean_agent
                    break
                elif selected_agent in self.agents: # Exact match
                    break
                    
                self.logger.warning(f"Invalid agent selected: {selected_agent}, retrying...")
                selected_agent = None
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Async routing with {type(provider).__name__} failed")
                continue

        if not selected_agent:
            self.logger.error("Failed to select a valid agent, utilizing fallback")
            selected_agent = self._select_default_agent()
            self.logger.trace_step(trace_id, "fallback_to_default_agent", {"selected_agent": selected_agent})
            
        return selected_agent
