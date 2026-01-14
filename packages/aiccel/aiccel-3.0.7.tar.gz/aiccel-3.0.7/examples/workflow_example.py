# examples/workflow_example.py
"""
Workflow Example
=================

Shows how to create and execute a multi-step workflow.
"""

import asyncio
import os
from aiccel import (
    SlimAgent, GeminiProvider,
    WorkflowBuilder, WorkflowExecutor,
    configure_logging
)
import logging

configure_logging(level=logging.INFO, quiet_internal=True)


async def main():
    # Setup provider
    provider = GeminiProvider(
        api_key=os.environ.get("GOOGLE_API_KEY", "your-api-key"),
        model="gemini-2.5-flash"
    )
    
    # Create specialized agents
    researcher = SlimAgent(
        provider=provider,
        name="Researcher",
        instructions="Research topics thoroughly and provide detailed information."
    )
    
    summarizer = SlimAgent(
        provider=provider,
        name="Summarizer",
        instructions="Summarize content into clear, concise bullet points."
    )
    
    writer = SlimAgent(
        provider=provider,
        name="Writer",
        instructions="Write engaging content based on the provided information."
    )
    
    # Build workflow
    workflow = (
        WorkflowBuilder("content_pipeline", "Generate blog content from a topic")
        
        # Step 1: Research
        .add_agent(
            id="research",
            agent=researcher,
            input_key="topic",
            output_key="research_data",
            prompt_template="Research this topic in detail: {topic}"
        )
        
        # Step 2: Summarize
        .add_agent(
            id="summarize",
            agent=summarizer,
            input_key="research_data",
            output_key="key_points",
            prompt_template="Extract key points from this research: {research_data}"
        )
        
        # Step 3: Write
        .add_agent(
            id="write",
            agent=writer,
            input_key="key_points",
            output_key="blog_post",
            prompt_template="Write a blog post using these key points: {key_points}"
        )
        
        # Connect in sequence
        .chain("research", "summarize", "write")
        .set_end("write")
        
        .build()
    )
    
    print("=" * 50)
    print("Workflow Example: Content Generation Pipeline")
    print("=" * 50)
    print(f"Workflow: {workflow.name}")
    print(f"Nodes: {list(workflow.nodes.keys())}")
    print()
    
    # Execute workflow
    executor = WorkflowExecutor(timeout=120.0)
    
    result = await executor.run(
        workflow,
        {"topic": "The Future of Artificial Intelligence"}
    )
    
    # Print results
    print("\n=== Research Data ===")
    print(result.outputs.get("research_data", "")[:500] + "...")
    
    print("\n=== Key Points ===")
    print(result.outputs.get("key_points", ""))
    
    print("\n=== Final Blog Post ===")
    print(result.outputs.get("blog_post", ""))
    
    print("\n=== Execution Stats ===")
    print(f"Total steps: {len(result.history)}")
    for step in result.history:
        print(f"  - {step['node_id']}: {step['status']}")


if __name__ == "__main__":
    asyncio.run(main())
