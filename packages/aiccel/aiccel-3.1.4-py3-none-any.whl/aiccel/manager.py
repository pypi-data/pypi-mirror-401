import json
import asyncio
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import aiohttp
import orjson
import re
import time

from .agent import Agent
from .tools import ToolRegistry
from .logger import AILogger
from .core.schemas import CollaborationPlan, SubTask, RoutingDecision

import threading
from collections import OrderedDict

class AgentManager:
    """Manages multiple specialized agents with thread-safe caching"""
    
    def __init__(self, llm_provider, agents=None, verbose=False, instructions: str = None, 
                 log_file: Optional[str] = None, structured_logging: bool = False, 
                 fallback_providers: Optional[List] = None, **kwargs):
        self.provider = llm_provider
        self.agents = {}
        self.history = []
        self.verbose = verbose
        self.instructions = instructions or (
            "Route queries to the most appropriate agent based on their expertise and available tools. "
            "Consider the query's intent, required knowledge, and tool capabilities."
        )
        self.logger = AILogger(
            name="AgentManager",
            verbose=verbose,
            log_file=log_file,
            structured_logging=structured_logging
        )
        self.fallback_providers = fallback_providers or []
        self.http_session = None
        self.semaphore = asyncio.Semaphore(2)
        self.config = kwargs # Store extra config
        
        # Thread-safe tool cache with LRU eviction
        self._tool_cache_lock = threading.RLock()
        self._tool_cache = OrderedDict()
        self._tool_cache_max_size = 1000
        self._tool_cache_ttl = 3600  # 1 hour
        self._tool_cache_timestamps = {}

        if agents:
            if isinstance(agents, list):
                for agent in agents:
                    self.add_agent(
                        name=agent.name,
                        agent=agent,
                        description=f"Agent specialized in {agent.name} tasks"
                    )
            elif isinstance(agents, dict):
                for name, agent_info in agents.items():
                    if isinstance(agent_info, dict):
                        self.add_agent(
                            name=name,
                            agent=agent_info.get("agent"),
                            description=agent_info.get("description", f"Agent specialized in {name} tasks")
                        )
                    else:
                        self.add_agent(
                            name=name,
                            agent=agent_info,
                            description=f"Agent specialized in {name} tasks"
                        )
    async def __aenter__(self):
        self.http_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()


    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Thread-safe cache retrieval with TTL check"""
        with self._tool_cache_lock:
            if key not in self._tool_cache:
                return None
            
            # Check TTL
            timestamp = self._tool_cache_timestamps.get(key, 0)
            if time.time() - timestamp > self._tool_cache_ttl:
                # Expired
                del self._tool_cache[key]
                del self._tool_cache_timestamps[key]
                return None
            
            # Move to end (LRU)
            self._tool_cache.move_to_end(key)
            return self._tool_cache[key]
    
    def _set_in_cache(self, key: str, value: Any):
        """Thread-safe cache storage with LRU eviction"""
        with self._tool_cache_lock:
            # Remove oldest if at capacity
            if len(self._tool_cache) >= self._tool_cache_max_size:
                oldest_key = next(iter(self._tool_cache))
                del self._tool_cache[oldest_key]
                del self._tool_cache_timestamps[oldest_key]
            
            # Add new entry
            self._tool_cache[key] = value
            self._tool_cache_timestamps[key] = time.time()
    
    def _clear_cache(self):
        """Clear the entire cache"""
        with self._tool_cache_lock:
            self._tool_cache.clear()
            self._tool_cache_timestamps.clear()

    @classmethod
    def from_agents(cls, agents: List[Agent], llm_provider=None, verbose=False, 
                    instructions: str = None, log_file: Optional[str] = None, 
                    structured_logging: bool = False, 
                    fallback_providers: Optional[List] = None) -> 'AgentManager':
        if not llm_provider and agents:
            llm_provider = agents[0].provider
        manager = cls(
            llm_provider=llm_provider,
            verbose=verbose,
            instructions=instructions,
            log_file=log_file,
            structured_logging=structured_logging,
            fallback_providers=fallback_providers
        )
        for agent in agents:
            manager.add_agent(
                name=agent.name,
                agent=agent,
                description=f"Agent specialized in {agent.name} tasks"
            )
        return manager

    def set_verbose(self, verbose: bool = True) -> 'AgentManager':
        self.verbose = verbose
        self.logger.verbose = verbose
        for name, info in self.agents.items():
            info["agent"].set_verbose(verbose)
        self.logger.info(f"Verbose mode set to: {verbose}")
        return self

    def set_instructions(self, instructions: str) -> 'AgentManager':
        self.instructions = instructions
        self.logger.info(f"Updated routing instructions: {instructions[:50]}...")
        return self

    def add_agent(self, name: str, agent: Agent, description: str) -> 'AgentManager':
        """Add agent with shared thread-safe cache access"""
        self.agents[name] = {
            "agent": agent,
            "description": description
        }
        agent.name = name
        agent.set_verbose(self.verbose)
        
        # Give agent access to thread-safe cache methods
        agent._get_from_shared_cache = self._get_from_cache
        agent._set_in_shared_cache = self._set_in_cache
        
        self.logger.info(f"Added agent: {name} - {description}")
        return self

    def _build_agent_descriptions(self) -> str:
        agent_descriptions = []
        for name, info in self.agents.items():
            tool_info = ""
            if agent := info["agent"]:
                if hasattr(agent, "tool_registry") and agent.tool_registry:
                    tools = agent.tool_registry.get_all()
                    if tools:
                        tool_names = [t.name for t in tools]
                        tool_info = f" (Tools: {', '.join(tool_names)})"
            agent_descriptions.append(f"- {name}: {info['description']}{tool_info}")
        return "\n".join(agent_descriptions)

    def _select_default_agent(self) -> str:
        """Select a default agent when routing fails. Uses the first available agent."""
        if not self.agents:
            return None
        
        # Sort agents by name for consistent selection and return the first one
        sorted_agents = sorted(self.agents.keys())
        selected_agent = sorted_agents[0]
        
        self.logger.info(f"Selected default agent: {selected_agent}")
        return selected_agent

    def _clean_and_parse_json(self, response: str, trace_id: int, context: str, schema_class=None) -> Any:
        """Robust JSON parsing with Pydantic validation if provided"""
        
        # Remove markdown
        cleaned = re.sub(r'^```(?:json)?\n?|\n?```$', '', response.strip(), flags=re.MULTILINE).strip()
        
        # Attempt 1: Direct parsing
        parsed = None
        try:
            parsed = orjson.loads(cleaned)
        except orjson.JSONDecodeError:
            # Attempt 2: Extract JSON (array or object)
            json_match = re.search(r'(\[.*?\]|\{.*?\})', cleaned, re.DOTALL)
            if json_match:
                try:
                    parsed = orjson.loads(json_match.group(0))
                except orjson.JSONDecodeError:
                    pass
        
        if parsed is not None:
            if schema_class:
                try:
                    # If it's a list but we expect an object (CollaborationPlan), wrap it
                    if isinstance(parsed, list) and schema_class == CollaborationPlan:
                        return CollaborationPlan(tasks=parsed)
                    return schema_class.model_validate(parsed)
                except Exception as e:
                    self.logger.warning(f"Schema validation failed for {context}: {e}")
            
            # Simple validation fallback if no schema provided
            if self._validate_sub_queries(parsed):
                return parsed

        # Fallback: Return single query with default agent
        self.logger.warning(f"JSON parsing/validation failed for {context}, using fallback")
        default_agent = self._select_default_agent()
        fallback_data = [{"sub_query": response[:500], "agent": default_agent}]
        return CollaborationPlan(tasks=fallback_data) if schema_class == CollaborationPlan else fallback_data

    def _validate_sub_queries(self, parsed: Any) -> bool:
        """Validate sub-query structure"""
        if not isinstance(parsed, list):
            return False
        
        for item in parsed:
            if not isinstance(item, dict):
                return False
            if "sub_query" not in item or "agent" not in item:
                return False
            if item["agent"] not in self.agents:
                return False
        
        return True

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def route(self, query: str) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("route_query", {"query": query[:100] + "..." if len(query) > 100 else query})
        if not self.agents:
            self.logger.error("No agents available to handle query")
            self.logger.trace_end(trace_id, {"error": "No agents available"})
            raise ValueError("No agents available")
        if len(self.agents) == 1:
            agent_name = list(self.agents.keys())[0]
            agent = self.agents[agent_name]["agent"]
            self.logger.info(f"Only one agent available, using: {agent_name}")
            try:
                result = agent.run(query)
                result["agent_used"] = agent_name
                self.history.append({
                    "query": query,
                    "agent": agent_name,
                    "response": result["response"],
                    "timestamp": datetime.now().isoformat()
                })
                self.logger.trace_step(trace_id, "agent_execution", {
                    "agent": agent_name,
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
                })
                self.logger.trace_end(trace_id, result)
                return result
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
                raise Exception(f"Single agent {agent_name} failed: {str(e)}")
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
        self.logger.trace_step(trace_id, "build_routing_prompt", {"prompt": routing_prompt[:200] + "..." if len(routing_prompt) > 200 else routing_prompt})
        selected_agent = None
        providers = [self.provider] + self.fallback_providers
        for provider in providers:
            try:
                self.logger.info(f"Attempting routing with provider: {type(provider).__name__}")
                selected_agent = provider.generate(routing_prompt).strip()
                self.logger.trace_step(trace_id, "routing_decision", {
                    "provider": type(provider).__name__,
                    "selected_agent": selected_agent
                })
                if selected_agent in self.agents:
                    break
                self.logger.warning(f"Invalid agent selected: {selected_agent}, retrying with next provider")
                selected_agent = None
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Routing with provider {type(provider).__name__} failed")
                continue
        if not selected_agent:
            self.logger.error("Failed to select a valid agent, falling back to default agent")
            selected_agent = self._select_default_agent()
            self.logger.trace_step(trace_id, "fallback_to_default_agent", {"selected_agent": selected_agent})
        agent = self.agents[selected_agent]["agent"]
        self.logger.info(f"Routing query to agent: {selected_agent}")
        try:
            result = agent.run(query)
            result["agent_used"] = selected_agent
            self.history.append({
                "query": query,
                "agent": selected_agent,
                "response": result["response"],
                "timestamp": datetime.now().isoformat()
            })
            self.logger.trace_step(trace_id, "agent_execution", {
                "agent": selected_agent,
                "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
            })
            self.logger.trace_end(trace_id, result)
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {selected_agent} execution failed")
            raise Exception(f"Agent {selected_agent} failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def route_async(self, query: str) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("route_query_async", {"query": query[:100] + "..." if len(query) > 100 else query})
        if not self.agents:
            self.logger.error("No agents available to handle query")
            self.logger.trace_end(trace_id, {"error": "No agents available"})
            raise ValueError("No agents available")
        if len(self.agents) == 1:
            agent_name = list(self.agents.keys())[0]
            agent = self.agents[agent_name]["agent"]
            self.logger.info(f"Only one agent available, using: {agent_name}")
            try:
                result = await agent.run_async(query)
                result["agent_used"] = agent_name
                self.history.append({
                    "query": query,
                    "agent": agent_name,
                    "response": result["response"],
                    "timestamp": datetime.now().isoformat()
                })
                self.logger.trace_step(trace_id, "agent_execution", {
                    "agent": agent_name,
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
                })
                self.logger.trace_end(trace_id, result)
                return result
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
                raise Exception(f"Single agent {agent_name} failed: {str(e)}")
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
        self.logger.trace_step(trace_id, "build_routing_prompt", {"prompt": routing_prompt[:200] + "..." if len(routing_prompt) > 200 else routing_prompt})
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
                if selected_agent in self.agents:
                    break
                self.logger.warning(f"Invalid agent selected: {selected_agent}, retrying with next provider")
                selected_agent = None
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Async routing with provider {type(provider).__name__} failed")
                continue
        if not selected_agent:
            self.logger.error("Failed to select a valid agent, falling back to default agent")
            selected_agent = self._select_default_agent()
            self.logger.trace_step(trace_id, "fallback_to_default_agent", {"selected_agent": selected_agent})
        agent = self.agents[selected_agent]["agent"]
        self.logger.info(f"Routing query to agent: {selected_agent}")
        try:
            result = await agent.run_async(query)
            result["agent_used"] = selected_agent
            self.history.append({
                "query": query,
                "agent": selected_agent,
                "response": result["response"],
                "timestamp": datetime.now().isoformat()
            })
            self.logger.trace_step(trace_id, "agent_execution", {
                "agent": selected_agent,
                "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
            })
            self.logger.trace_end(trace_id, result)
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {selected_agent} execution failed")
            raise Exception(f"Agent {selected_agent} failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def collaborate(self, query: str, max_agents: int = 5, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("collaborate", {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "max_agents": max_agents
        })
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.collaborate_async(query, max_agents, agent_ids)
                )
                self.logger.trace_end(trace_id, {
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"],
                    "agents_used": result["agents_used"]
                })
                return result
            finally:
                loop.close()
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Synchronous collaboration failed")
            raise Exception(f"Collaboration failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def collaborate_async(self, query: str, max_agents: int = 5, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("collaborate_async", {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "max_agents": max_agents
        })

        async with self:  # Manage HTTP session
            if not self.agents:
                self.logger.error("No agents available for collaboration")
                self.logger.trace_end(trace_id, {"error": "No agents available"})
                raise ValueError("No agents available")

            # 1. Planning Phase
            plan = await self._plan_collaboration(query, max_agents, agent_ids, trace_id)
            
            # 2. Execution Phase
            agent_results = await self._execute_collaboration(query, plan, trace_id)
            
            # 3. Synthesis Phase
            final_response = await self._synthesize_collaboration(query, agent_results, trace_id)

            final_result = {
                "response": final_response,
                "agent_results": agent_results,
                "agents_used": list(set(r["agent"] for r in agent_results)),
                "plan": plan.model_dump() if isinstance(plan, CollaborationPlan) else plan
            }

            self.history.append({
                "query": query,
                "agents": final_result["agents_used"],
                "response": final_response,
                "timestamp": datetime.now().isoformat()
            })

            self.logger.trace_end(trace_id, final_result)
            return final_result

    async def _plan_collaboration(self, query: str, max_agents: int, agent_ids: List[str], trace_id: int) -> CollaborationPlan:
        """Splits query into sub-tasks and assigns agents using LLM or explicit IDs."""
        
        # Generate dynamic instructions for the manager
        dynamic_instructions = self.generate_dynamic_instructions(query)
        self.instructions = dynamic_instructions if dynamic_instructions else self.instructions

        if agent_ids:
            valid_agent_ids = [aid for aid in agent_ids if aid in self.agents]
            if valid_agent_ids:
                selected_agents = valid_agent_ids[:max_agents]
                return CollaborationPlan(tasks=[SubTask(sub_query=query, agent=aid) for aid in selected_agents])

        agent_descriptions = self._build_agent_descriptions()
        query_split_prompt = (
            f"Instructions: {self.instructions}\n\n"
            f"Query: {query}\n\n"
            f"Available agents:\n{agent_descriptions}\n\n"
            "Split the query into distinct sub-tasks for collaboration. Return valid JSON matching the schema.\n"
            "Example: {\"tasks\": [{\"sub_query\": \"...\", \"agent\": \"...\"}]}"
        )

        for provider in [self.provider] + self.fallback_providers:
            try:
                response = await provider.generate_async(query_split_prompt)
                return self._clean_and_parse_json(response, trace_id, "planning", schema_class=CollaborationPlan)
            except Exception as e:
                self.logger.warning(f"Planning failed with {type(provider).__name__}: {e}")

        # Fallback
        return CollaborationPlan(tasks=[SubTask(sub_query=query, agent=self._select_default_agent())])

    async def _execute_collaboration(self, query: str, plan: CollaborationPlan, trace_id: int) -> List[Dict[str, Any]]:
        """Executes all sub-tasks in parallel with concurrency control."""
        tasks = []
        for task in plan.tasks:
            agent = self.agents[task.agent]["agent"]
            tasks.append(self._run_single_collaboration_task(task, agent, trace_id))
        
        return await asyncio.gather(*tasks)

    async def _run_single_collaboration_task(self, task: SubTask, agent: Agent, trace_id: int) -> Dict[str, Any]:
        async with self.semaphore:
            try:
                result = await asyncio.wait_for(
                    agent.run_async(task.sub_query),
                    timeout=45.0
                )
                return {
                    "agent": task.agent,
                    "sub_query": task.sub_query,
                    "response": result.get("response", "No response"),
                    "success": True
                }
            except Exception as e:
                return {
                    "agent": task.agent,
                    "sub_query": task.sub_query,
                    "response": f"Error: {str(e)}",
                    "success": False
                }

    async def _synthesize_collaboration(self, query: str, agent_results: List[Dict[str, Any]], trace_id: int) -> str:
        """Combines multiple agent responses into a final answer."""
        responses_text = "\n".join([f"Agent {r['agent']} (on '{r['sub_query']}'): {r['response']}" for r in agent_results])
        synthesis_prompt = f"Original Query: {query}\n\nAgent Responses:\n{responses_text}\n\nSynthesize these into a single coherent answer."

        for provider in [self.provider] + self.fallback_providers:
            try:
                return await provider.generate_async(synthesis_prompt)
            except Exception as e:
                self.logger.warning(f"Synthesis failed with {type(provider).__name__}: {e}")

        return "Failed to synthesize a response from agents."

            self.history.append({
                "query": query,
                "agents": selected_agents,
                "response": final_response,
                "timestamp": datetime.now().isoformat()
            })

            self.logger.trace_end(trace_id, {
                "response": final_response[:100] + "..." if len(final_response) > 100 else final_response,
                "agents_used": selected_agents,
                "sub_queries": sub_queries
            })
            return final_result

    async def _run_agent_async_with_error_handling(self, agent: Agent, agent_name: str, query: str, trace_id: int) -> Dict[str, Any]:
        try:
            result = await agent.run_async(query)
            normalized_result = {
                "agent": agent_name,
                "agent_used": agent_name,
                "response": result.get("response", "No response"),
                "tool_used": result.get("tool_used"),
                "tool_output": result.get("tool_output")
            }
            self.logger.trace_step(trace_id, f"agent_{agent_name}_execution", {
                "agent": agent_name,
                "response": normalized_result["response"][:100] + "..." if len(normalized_result["response"]) > 100 else normalized_result["response"]
            })
            return normalized_result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
            return {
                "agent": agent_name,
                "agent_used": agent_name,
                "response": f"Error: Agent {agent_name} failed: {str(e)}",
                "tool_used": None,
                "tool_output": None
            }

    def generate_dynamic_instructions(self, query: str) -> str:
        """Generate dynamic instructions for the manager based on the query and available agents."""
        agent_descriptions = self._build_agent_descriptions()
        prompt = (
            f"Query: {query}\n\n"
            f"Available agents:\n{agent_descriptions}\n\n"
            "Based on the query, determine the best way to split it into sub-queries and assign them to agents. "
            "Provide instructions on how to handle the query effectively, considering the agents' expertise and tools."
        )
        return self.provider.generate(prompt)