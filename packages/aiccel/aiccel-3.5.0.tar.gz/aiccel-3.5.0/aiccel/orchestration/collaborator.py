# aiccel/orchestration/collaborator.py
"""
Agent Collaborator
==================

Manages complex multi-agent collaboration workflows.
"""

import asyncio
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..core.schemas import CollaborationPlan, SubTask
from ..logger import AILogger
from ..utils.json_parser import clean_and_parse_json

if TYPE_CHECKING:
    from ..agent import Agent
    from ..providers.base import LLMProvider
    from .router import Router

class Collaborator:
    """
    Orchestrates collaboration between multiple agents.
    """
    
    def __init__(
        self,
        provider: 'LLMProvider',
        router: 'Router',
        agents: Dict[str, Dict[str, Any]],
        logger: AILogger,
        fallback_providers: Optional[List['LLMProvider']] = None,
        semaphore: Optional[asyncio.Semaphore] = None
    ):
        self.provider = provider
        self.router = router
        self.agents = agents
        self.logger = logger
        self.fallback_providers = fallback_providers or []
        self.semaphore = semaphore or asyncio.Semaphore(5)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def collaborate_async(self, query: str, max_agents: int, trace_id: int, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Executing collaboration workflow."""
        
        # 1. Planning Phase
        plan = await self._plan_collaboration(query, max_agents, agent_ids, trace_id)
        
        # 2. Execution Phase
        agent_results = await self._execute_collaboration(plan, trace_id)
        
        # 3. Synthesis Phase
        final_response = await self._synthesize_collaboration(query, agent_results, trace_id)

        return {
            "response": final_response,
            "agent_results": agent_results,
            "agents_used": list(set(r["agent"] for r in agent_results)),
            "plan": plan.model_dump()
        }

    async def _plan_collaboration(self, query: str, max_agents: int, agent_ids: List[str], trace_id: int) -> CollaborationPlan:
        """Splits query into sub-tasks."""
        
        if agent_ids:
            # Explicit agent selection implies skipping LLM planning for agent selection, 
            # but we still might want task splitting. 
            # For simplicity, we assume explicit IDs means "run this query on these agents" or "simple split"
            # But the logic in original manager.py was: just run the same query on all selected agents?
            # Re-reading manager.py:
            # "return CollaborationPlan(tasks=[SubTask(sub_query=query, agent=aid) for aid in selected_agents])"
            # Yes, parallel execution of same query.
            
            valid_agent_ids = [aid for aid in agent_ids if aid in self.agents]
            if valid_agent_ids:
                selected_agents = valid_agent_ids[:max_agents]
                return CollaborationPlan(tasks=[SubTask(sub_query=query, agent=aid) for aid in selected_agents])

        agent_descriptions = self.router._build_agent_descriptions()
        query_split_prompt = (
            f"Instructions: {self.router.instructions}\n\n"
            f"Query: {query}\n\n"
            f"Available agents:\n{agent_descriptions}\n\n"
            "Split the query into distinct sub-tasks for collaboration. Return valid JSON matching the schema.\n"
            "Example: {\"tasks\": [{\"sub_query\": \"...\", \"agent\": \"...\"}]}"
        )

        providers = [self.provider] + self.fallback_providers
        for provider in providers:
            try:
                response = await provider.generate_async(query_split_prompt)
                
                # We need a custom validate helper because CollaborationPlan expects 'tasks' list
                # clean_and_parse_json can return dict or list
                # We will handle it manually via clean_and_parse_json with schema
                
                return clean_and_parse_json(
                    response, 
                    "planning", 
                    schema_class=CollaborationPlan, 
                    logger=self.logger
                )
            except Exception as e:
                self.logger.warning(f"Planning failed with {type(provider).__name__}: {e}")

        # Fallback to single agent
        default_agent = self.router._select_default_agent()
        if not default_agent:
             raise ValueError("No agents available for fallback")
             
        return CollaborationPlan(tasks=[SubTask(sub_query=query, agent=default_agent)])

    async def _execute_collaboration(self, plan: CollaborationPlan, trace_id: int) -> List[Dict[str, Any]]:
        """Executes all sub-tasks in parallel."""
        tasks = []
        for task in plan.tasks:
            if task.agent not in self.agents:
                self.logger.warning(f"Agent {task.agent} not found, skipping task")
                continue
                
            agent = self.agents[task.agent]["agent"]
            tasks.append(self._run_single_task(task, agent, trace_id))
        
        if not tasks:
            return []
            
        return await asyncio.gather(*tasks)

    async def _run_single_task(self, task: SubTask, agent: 'Agent', trace_id: int) -> Dict[str, Any]:
        async with self.semaphore:
            try:
                # We assume 45s timeout per task
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
        """Combines multiple agent responses."""
        if not agent_results:
             return "No results to synthesize."
             
        responses_text = "\n".join([f"Agent {r['agent']} (on '{r['sub_query']}'): {r['response']}" for r in agent_results])
        synthesis_prompt = f"Original Query: {query}\n\nAgent Responses:\n{responses_text}\n\nSynthesize these into a single coherent answer."

        for provider in [self.provider] + self.fallback_providers:
            try:
                return await provider.generate_async(synthesis_prompt)
            except Exception as e:
                self.logger.warning(f"Synthesis failed with {type(provider).__name__}: {e}")

        return "Failed to synthesize a response from agents."
