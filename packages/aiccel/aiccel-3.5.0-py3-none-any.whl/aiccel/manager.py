# aiccel/manager.py
"""
Agent Manager
=============

Main entry point for multi-agent orchestration.
Delegates complex logic to orchestration components (Router, Collaborator).
"""

import asyncio
import time
import threading
from typing import List, Dict, Any, Optional, Type
from datetime import datetime
import aiohttp

from .agent import Agent
from .logger import AILogger
from .exceptions import AgentException
from .orchestration.router import Router
from .orchestration.collaborator import Collaborator

class AgentManager:
    """Manages multiple specialized agents with thread-safe caching and orchestration."""
    
    def __init__(
        self, 
        llm_provider, 
        agents=None, 
        verbose=False, 
        instructions: str = None, 
        log_file: Optional[str] = None, 
        structured_logging: bool = False, 
        fallback_providers: Optional[List] = None, 
        **kwargs
    ):
        self.provider = llm_provider
        self.agents = {}
        self._history: List[Dict[str, Any]] = []
        self._history_lock = threading.Lock()
        self.verbose = verbose
        
        # Logging
        self.logger = AILogger(
            name="AgentManager",
            verbose=verbose,
            log_file=log_file,
            structured_logging=structured_logging
        )
        
        self.fallback_providers = fallback_providers or []
        self.http_session = None
        
        # Initializing core components
        # Note: Router and Collaborator will be initialized lazily or after agents are added?
        # Ideally they should check self.agents dynamically or share the reference.
        # Since self.agents is a dict passed by reference, updating it here updates it there.
        
        self.router = Router(
            provider=self.provider,
            agents=self.agents,
            logger=self.logger,
            fallback_providers=self.fallback_providers,
            instructions=instructions
        )
        
        self.collaborator = Collaborator(
            provider=self.provider,
            router=self.router,
            agents=self.agents,
            logger=self.logger,
            fallback_providers=self.fallback_providers
        )
        
        # Thread-safe tool cache 
        self._setup_cache()
        
        # Add initial agents
        if agents:
            self._add_initial_agents(agents)

    def _setup_cache(self):
        self._tool_cache_lock = threading.RLock()
        self._tool_cache = {} # OrderedDict not strictly needed for modern dicts but used for LRU
        from collections import OrderedDict
        self._tool_cache = OrderedDict()
        self._tool_cache_max_size = 1000
        self._tool_cache_ttl = 3600
        self._tool_cache_timestamps = {}

    def _add_initial_agents(self, agents):
        if isinstance(agents, list):
            for agent in agents:
                self.add_agent(agent.name, agent, f"Agent specialized in {agent.name} tasks")
        elif isinstance(agents, dict):
            for name, info in agents.items():
                if isinstance(info, dict):
                    self.add_agent(name, info.get("agent"), info.get("description", ""))
                else:
                    self.add_agent(name, info, f"Agent specialized in {name} tasks")

    async def __aenter__(self):
        self.http_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    # =========================================================================
    # Cache Management (Thread-Safe)
    # =========================================================================
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        with self._tool_cache_lock:
            if key not in self._tool_cache:
                return None
            timestamp = self._tool_cache_timestamps.get(key, 0)
            if time.time() - timestamp > self._tool_cache_ttl:
                del self._tool_cache[key]
                del self._tool_cache_timestamps[key]
                return None
            self._tool_cache.move_to_end(key)
            return self._tool_cache[key]
    
    def _set_in_cache(self, key: str, value: Any):
        with self._tool_cache_lock:
            if len(self._tool_cache) >= self._tool_cache_max_size:
                oldest_key = next(iter(self._tool_cache))
                del self._tool_cache[oldest_key]
                del self._tool_cache_timestamps[oldest_key]
            self._tool_cache[key] = value
            self._tool_cache_timestamps[key] = time.time()
    
    def _clear_cache(self):
        with self._tool_cache_lock:
            self._tool_cache.clear()
            self._tool_cache_timestamps.clear()

    # =========================================================================
    # History Management
    # =========================================================================

    @property
    def history(self) -> List[Dict[str, Any]]:
        with self._history_lock:
            return list(self._history)
    
    def _append_history(self, entry: Dict[str, Any]) -> None:
        with self._history_lock:
            self._history.append(entry)
            if len(self._history) > 1000:
                self._history = self._history[-1000:]

    # =========================================================================
    # Agent Management
    # =========================================================================

    @classmethod
    def from_agents(cls, agents: List[Agent], llm_provider=None, verbose=False, **kwargs) -> 'AgentManager':
        if not llm_provider and agents:
            llm_provider = agents[0].provider
        manager = cls(llm_provider=llm_provider, verbose=verbose, **kwargs)
        for agent in agents:
            manager.add_agent(agent.name, agent, f"Agent specialized in {agent.name} tasks")
        return manager

    def add_agent(self, name: str, agent: Agent, description: str) -> 'AgentManager':
        if name in self.agents:
            self.logger.warning(f"Overwriting existing agent: {name}")
            
        self.agents[name] = {
            "agent": agent,
            "description": description
        }
        agent.name = name
        agent.set_verbose(self.verbose)
        
        # Inject shared cache access
        agent._get_from_shared_cache = self._get_from_cache
        agent._set_in_shared_cache = self._set_in_cache
        
        self.logger.info(f"Added agent: {name}")
        return self

    def set_verbose(self, verbose: bool = True) -> 'AgentManager':
        self.verbose = verbose
        self.logger.verbose = verbose
        for info in self.agents.values():
            info["agent"].set_verbose(verbose)
        return self

    def set_instructions(self, instructions: str) -> 'AgentManager':
        self.router.instructions = instructions
        return self

    # =========================================================================
    # Execution
    # =========================================================================

    def run(self, query: str) -> Dict[str, Any]:
        """Sync wrapper for route_async"""
        return asyncio.run(self.route_async(query))
    
    async def run_async(self, query: str) -> Dict[str, Any]:
        """Alias for route_async"""
        return await self.route_async(query)

    async def route_async(self, query: str) -> Dict[str, Any]:
        """Routes query to the best agent and executes."""
        trace_id = self.logger.trace_start("route_query", {"query": query[:50]})
        
        try:
            # 1. Route
            agent_name = await self.router.route_async(query, trace_id)
            agent = self.agents[agent_name]["agent"]
            
            # 2. Execute
            self.logger.info(f"Executing with agent: {agent_name}")
            result = await agent.run_async(query)
            
            # 3. Record
            result["agent_used"] = agent_name
            self._append_history({
                "query": query,
                "agent": agent_name,
                "response": result.get("response"),
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.trace_end(trace_id, result)
            return result
            
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Routing execution failed")
            raise AgentException(f"Routing failed: {e}")

    def collaborate(self, query: str, max_agents: int = 5, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Sync wrapper for collaborate_async"""
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self.collaborate_async(query, max_agents, agent_ids))
        finally:
            loop.close()

    async def collaborate_async(self, query: str, max_agents: int = 5, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Uses Collaborator to handle multi-agent task."""
        trace_id = self.logger.trace_start("collaborate", {"query": query[:50]})
        
        try:
            async with self: # Manage HTTP session if needed
                result = await self.collaborator.collaborate_async(query, max_agents, trace_id, agent_ids)
                
                self._append_history({
                    "query": query,
                    "agents": result["agents_used"],
                    "response": result["response"],
                    "timestamp": datetime.now().isoformat()
                })
                
                self.logger.trace_end(trace_id, result)
                return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Collaboration failed")
            raise AgentException(f"Collaboration failed: {e}")

    # Preserved for backward compatibility / internal use if needed
    def _clean_and_parse_json(self, *args, **kwargs):
        from .utils.json_parser import clean_and_parse_json
        return clean_and_parse_json(*args, **kwargs)