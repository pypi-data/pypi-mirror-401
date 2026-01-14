# examples/autonomous_example.py
"""
Autonomous Agent Example
=========================

Shows how to use GoalAgent for autonomous task execution.
"""

import asyncio
import os
from aiccel import GeminiProvider, SearchTool, configure_logging
from aiccel.autonomous import GoalAgent, Goal
import logging

configure_logging(level=logging.INFO)


async def main():
    # Setup
    provider = GeminiProvider(
        api_key=os.environ.get("GOOGLE_API_KEY", "AIzaSyBKz_dp5X8zFgnPyJXUGBeQfsoibu8_XEg"),
        model="gemini-2.5-flash"
    )
    
    tools = []
    if os.environ.get("SERPER_API_KEY"):
        tools.append(SearchTool(api_key=os.environ["SERPER_API_KEY"]))
    
    # Create autonomous agent
    agent = GoalAgent(
        provider=provider,
        tools=tools,
        max_iterations=30,
        reflection_enabled=True,
        verbose=True
    )
    
    print("=" * 50)
    print("Autonomous Agent Example")
    print("=" * 50)
    
    # Add goals
    agent.add_goals([
        Goal(
            id="research_ai",
            description="Research the top 3 AI trends in 2025",
            success_criteria="Identified and described 3 distinct AI trends",
            priority=1,
            max_attempts=2
        ),
        Goal(
            id="analyze_trends",
            description="Analyze the business impact of these AI trends",
            success_criteria="Provided business impact analysis for each trend",
            priority=2,
            dependencies=["research_ai"]  # Must complete research first
        ),
        Goal(
            id="create_summary",
            description="Create an executive summary of the analysis",
            success_criteria="Written a concise executive summary (3-5 paragraphs)",
            priority=3,
            dependencies=["analyze_trends"]
        )
    ])
    
    print(f"\nGoals to achieve: {list(agent.goals.keys())}")
    print("Starting autonomous execution...\n")
    
    # Run autonomously
    results = await agent.run_until_complete(timeout=180.0)
    
    # Print results
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    
    print(f"\n✅ Completed goals: {results['completed']}")
    print(f"❌ Failed goals: {results['failed']}")
    print(f"⏳ Pending goals: {results['pending']}")
    print(f"⏱️ Total iterations: {results['iterations']}")
    print(f"⏱️ Duration: {results['duration_s']:.1f}s")
    
    # Print individual results
    for goal_id, result in results['results'].items():
        print(f"\n--- {goal_id} ---")
        print(result[:500] if isinstance(result, str) else str(result)[:500])
        print("...")


if __name__ == "__main__":
    asyncio.run(main())
