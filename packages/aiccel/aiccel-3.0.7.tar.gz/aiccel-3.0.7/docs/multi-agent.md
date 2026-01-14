# Multi-Agent Systems

Build sophisticated multi-agent systems with AICCEL.

---

## Overview

Multi-agent systems allow you to:
- Distribute tasks among specialized agents
- Route queries to the right expert
- Collaborate on complex problems
- Scale AI capabilities

---

## AgentManager

The simplest way to create multi-agent systems.

### Basic Setup

```python
from aiccel import Agent, AgentManager, GeminiProvider

provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")

# Create specialized agents
code_agent = Agent(
    provider=provider,
    name="CodeExpert",
    instructions="You are an expert programmer. Write clean, documented code."
)

research_agent = Agent(
    provider=provider,
    name="Researcher",
    tools=[SearchTool(api_key="...")],
    instructions="Research topics thoroughly using web search."
)

writer_agent = Agent(
    provider=provider,
    name="Writer",
    instructions="Write clear, engaging content."
)

# Create manager
manager = AgentManager(routing_provider=provider)

# Register agents
manager.add_agent(code_agent, "code_expert", "Handles programming and code questions")
manager.add_agent(research_agent, "researcher", "Handles research and fact-finding")
manager.add_agent(writer_agent, "writer", "Handles writing and content creation")
```

### Automatic Routing

```python
# Manager automatically routes to the best agent
result = manager.route("Write a Python function to sort a list")
# Routes to: code_expert

result = manager.route("What are the latest AI trends?")
# Routes to: researcher

result = manager.route("Write a blog post about productivity")
# Routes to: writer
```

### Manual Routing

```python
# Force a specific agent
result = manager.route("Question", agent_id="code_expert")
```

### Async Routing

```python
result = await manager.route_async("Complex question")
```

---

## Specialized Agent Teams

### Research Team

```python
# Literature researcher
lit_agent = Agent(
    provider=provider,
    name="LiteratureReviewer",
    tools=[SearchTool(...)],
    instructions="""Search for academic papers and research.
    Focus on peer-reviewed sources."""
)

# Data analyst
data_agent = Agent(
    provider=provider,
    name="DataAnalyst",
    instructions="""Analyze data and statistics.
    Provide clear insights and visualizations in text."""
)

# Report writer
report_agent = Agent(
    provider=provider,
    name="ReportWriter",
    instructions="""Write professional research reports.
    Include citations and methodology."""
)

# Create team
research_team = AgentManager(routing_provider=provider)
research_team.add_agent(lit_agent, "literature", "Finds research papers")
research_team.add_agent(data_agent, "analyst", "Analyzes data")
research_team.add_agent(report_agent, "reporter", "Writes reports")
```

### Development Team

```python
architect = Agent(
    provider=provider,
    name="Architect",
    instructions="Design software architecture and system design."
)

developer = Agent(
    provider=provider,
    name="Developer",
    instructions="Write clean, tested code. Follow best practices."
)

reviewer = Agent(
    provider=provider,
    name="Reviewer",
    instructions="Review code for bugs, security issues, and improvements."
)

dev_team = AgentManager(routing_provider=provider)
dev_team.add_agent(architect, "architect", "System design")
dev_team.add_agent(developer, "developer", "Code implementation")
dev_team.add_agent(reviewer, "reviewer", "Code review")
```

---

## Agent Collaboration Patterns

### Pattern 1: Sequential Handoff

Agents pass work to each other:

```python
async def sequential_handoff(query: str):
    # Step 1: Research
    research_result = await research_agent.run_async(
        f"Research this topic: {query}"
    )
    
    # Step 2: Analyze (uses research output)
    analysis_result = await analyst_agent.run_async(
        f"Analyze this research: {research_result['response']}"
    )
    
    # Step 3: Write (uses analysis)
    final_result = await writer_agent.run_async(
        f"Write a report based on: {analysis_result['response']}"
    )
    
    return final_result
```

### Pattern 2: Parallel Execution

Multiple agents work simultaneously:

```python
import asyncio

async def parallel_research(topic: str):
    # Run multiple agents in parallel
    results = await asyncio.gather(
        tech_agent.run_async(f"Technical aspects of: {topic}"),
        market_agent.run_async(f"Market analysis of: {topic}"),
        legal_agent.run_async(f"Legal considerations for: {topic}")
    )
    
    # Combine results
    combined = "\n\n".join([r["response"] for r in results])
    
    # Synthesize
    final = await synthesis_agent.run_async(
        f"Create comprehensive report from:\n{combined}"
    )
    
    return final
```

### Pattern 3: Debate / Critique

Agents challenge each other:

```python
async def agent_debate(topic: str):
    # Initial position
    position_a = await agent_a.run_async(f"Argue FOR: {topic}")
    
    # Counter-argument
    position_b = await agent_b.run_async(
        f"Argue AGAINST based on: {position_a['response']}"
    )
    
    # Rebuttal
    rebuttal = await agent_a.run_async(
        f"Respond to criticism: {position_b['response']}"
    )
    
    # Moderator summarizes
    summary = await moderator_agent.run_async(
        f"""Summarize the debate:
        Position A: {position_a['response']}
        Position B: {position_b['response']}
        Rebuttal: {rebuttal['response']}"""
    )
    
    return summary
```

### Pattern 4: Expert Consultation

Main agent consults specialists:

```python
class ConsultingAgent(Agent):
    def __init__(self, provider, experts: dict, **kwargs):
        super().__init__(provider=provider, **kwargs)
        self.experts = experts
    
    async def run_with_experts(self, query: str):
        # Determine which experts to consult
        experts_needed = await self.run_async(
            f"What expertise is needed for: {query}\nAvailable: {list(self.experts.keys())}"
        )
        
        # Consult relevant experts
        consultations = {}
        for expert_name, expert_agent in self.experts.items():
            if expert_name.lower() in experts_needed["response"].lower():
                result = await expert_agent.run_async(
                    f"Expert opinion on: {query}"
                )
                consultations[expert_name] = result["response"]
        
        # Synthesize expert opinions
        final = await self.run_async(
            f"Based on expert consultations: {consultations}\nAnswer: {query}"
        )
        
        return final

# Usage
agent = ConsultingAgent(
    provider=provider,
    experts={
        "legal": legal_agent,
        "financial": finance_agent,
        "technical": tech_agent
    },
    name="Consultant"
)
```

### Pattern 5: Supervisor-Worker

One agent coordinates others:

```python
class SupervisorAgent:
    def __init__(self, provider, workers: dict):
        self.coordinator = Agent(
            provider=provider,
            name="Supervisor",
            instructions="""Coordinate work among workers.
            Assign tasks, review results, ensure quality."""
        )
        self.workers = workers
    
    async def execute_task(self, task: str):
        # Plan work
        plan = await self.coordinator.run_async(
            f"Create work plan for: {task}\nWorkers: {list(self.workers.keys())}"
        )
        
        # Assign to workers
        results = {}
        for worker_name, worker in self.workers.items():
            if worker_name in plan["response"]:
                result = await worker.run_async(f"Your part of: {task}")
                results[worker_name] = result["response"]
        
        # Review and combine
        final = await self.coordinator.run_async(
            f"Review and combine results: {results}"
        )
        
        return final
```

---

## Dynamic Agent Creation

Create agents on-demand:

```python
class AgentFactory:
    def __init__(self, provider):
        self.provider = provider
        self.cache = {}
    
    def get_agent(self, specialty: str) -> Agent:
        if specialty not in self.cache:
            self.cache[specialty] = Agent(
                provider=self.provider,
                name=f"{specialty.title()}Expert",
                instructions=f"You are an expert in {specialty}."
            )
        return self.cache[specialty]

factory = AgentFactory(provider)

# Get or create agents dynamically
python_expert = factory.get_agent("python programming")
ml_expert = factory.get_agent("machine learning")
```

---

## Agent Communication

### Shared Memory

```python
from aiccel import ConversationMemory

# Shared memory for all agents
shared_memory = ConversationMemory(memory_type="buffer", max_turns=50)

# Agents share context
agent_a = Agent(provider=provider, name="AgentA")
agent_a.memory = shared_memory

agent_b = Agent(provider=provider, name="AgentB")
agent_b.memory = shared_memory  # Same memory!

# Agent A's conversation is visible to Agent B
agent_a.run("I'm working on project X")
agent_b.run("What project was mentioned?")  # Sees Agent A's context
```

### Message Passing

```python
class MessageBroker:
    def __init__(self):
        self.messages = []
    
    def send(self, sender: str, recipient: str, content: str):
        self.messages.append({
            "from": sender,
            "to": recipient,
            "content": content
        })
    
    def receive(self, recipient: str) -> list:
        msgs = [m for m in self.messages if m["to"] == recipient]
        self.messages = [m for m in self.messages if m["to"] != recipient]
        return msgs

# Usage
broker = MessageBroker()

# Agent A sends message
broker.send("agent_a", "agent_b", "Please review this code")

# Agent B receives
messages = broker.receive("agent_b")
```

---

## Scaling Agents

### Concurrent Execution

```python
import asyncio

async def scale_agents(queries: list, agent: Agent, max_concurrent: int = 5):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def limited_run(query):
        async with semaphore:
            return await agent.run_async(query)
    
    results = await asyncio.gather(*[limited_run(q) for q in queries])
    return results

# Process many queries
queries = ["Query 1", "Query 2", "Query 3", ...]
results = await scale_agents(queries, agent, max_concurrent=10)
```

### Load Balancing

```python
import random

class LoadBalancer:
    def __init__(self, agents: list):
        self.agents = agents
        self.usage = {id(a): 0 for a in agents}
    
    def get_agent(self) -> Agent:
        # Get least used agent
        agent = min(self.agents, key=lambda a: self.usage[id(a)])
        self.usage[id(agent)] += 1
        return agent

# Create multiple instances
agents = [Agent(provider=provider, name=f"Worker{i}") for i in range(5)]
balancer = LoadBalancer(agents)

# Distribute work
for query in queries:
    agent = balancer.get_agent()
    result = await agent.run_async(query)
```

---

## Complete Example

```python
import asyncio
from aiccel import Agent, AgentManager, GeminiProvider, SearchTool

async def main():
    provider = GeminiProvider(api_key="...", model="gemini-2.5-flash")
    
    # Create team
    researcher = Agent(
        provider=provider,
        name="Researcher",
        tools=[SearchTool(api_key="...")],
        instructions="Research topics thoroughly."
    )
    
    analyst = Agent(
        provider=provider,
        name="Analyst",
        instructions="Analyze data and provide insights."
    )
    
    writer = Agent(
        provider=provider,
        name="Writer",
        instructions="Write clear, professional content."
    )
    
    # Create manager
    manager = AgentManager(routing_provider=provider)
    manager.add_agent(researcher, "research", "Research and fact-finding")
    manager.add_agent(analyst, "analysis", "Data analysis")
    manager.add_agent(writer, "writing", "Content creation")
    
    # Collaborative task
    print("=== Multi-Agent Research Project ===\n")
    
    # Step 1: Research
    print("Step 1: Researching...")
    research = await researcher.run_async(
        "Research the impact of AI on employment"
    )
    print(f"Research complete: {len(research['response'])} chars\n")
    
    # Step 2: Analyze
    print("Step 2: Analyzing...")
    analysis = await analyst.run_async(
        f"Analyze this research:\n{research['response']}"
    )
    print(f"Analysis complete\n")
    
    # Step 3: Write report
    print("Step 3: Writing report...")
    report = await writer.run_async(
        f"Write an executive summary:\n{analysis['response']}"
    )
    print(f"Report complete\n")
    
    print("=== Final Report ===")
    print(report["response"])

asyncio.run(main())
```

---

## Best Practices

1. **Specialized agents** - Each agent should excel at one thing
2. **Clear routing** - Make agent purposes obvious
3. **Context sharing** - Pass relevant context between agents
4. **Error isolation** - One agent's failure shouldn't crash others
5. **Monitoring** - Log which agents handle which queries
6. **Fallbacks** - Have default agents for unroutable queries

---

## Next Steps

- [Workflows](./agent-workflows.md) - DAG-based orchestration
- [Autonomous](./autonomous.md) - Goal-driven agents
