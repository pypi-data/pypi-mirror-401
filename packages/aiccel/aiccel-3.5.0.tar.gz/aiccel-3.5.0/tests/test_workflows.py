# tests/test_workflows.py
"""
Workflow Tests
===============

Tests for workflow orchestration.
"""

import pytest
import asyncio


class TestWorkflowCreation:
    """Test workflow creation."""
    
    def test_create_workflow(self):
        """Create a basic workflow."""
        from aiccel.workflows import Workflow
        
        workflow = Workflow(
            name="test_workflow",
            description="Test workflow"
        )
        
        assert workflow.name == "test_workflow"
        assert len(workflow.nodes) == 0
    
    def test_add_node(self):
        """Add node to workflow."""
        from aiccel.workflows import Workflow, WorkflowNode
        
        workflow = Workflow(name="test")
        node = WorkflowNode(id="node1", name="Node 1", type="generic")
        
        workflow.add_node(node)
        
        assert len(workflow.nodes) == 1
        assert workflow.get_node("node1") is not None
    
    def test_add_edge(self):
        """Add edge between nodes."""
        from aiccel.workflows import Workflow, WorkflowNode
        
        workflow = Workflow(name="test")
        workflow.add_node(WorkflowNode(id="n1", name="N1"))
        workflow.add_node(WorkflowNode(id="n2", name="N2"))
        workflow.add_edge("n1", "n2")
        
        assert len(workflow.edges) == 1


class TestWorkflowBuilder:
    """Test fluent workflow builder."""
    
    def test_builder_chain(self, mock_provider):
        """Build workflow with chain."""
        from aiccel import WorkflowBuilder, SlimAgent
        
        agent1 = SlimAgent(provider=mock_provider, name="Agent1")
        agent2 = SlimAgent(provider=mock_provider, name="Agent2")
        
        workflow = (
            WorkflowBuilder("test_pipeline")
            .add_agent("step1", agent1)
            .add_agent("step2", agent2)
            .chain("step1", "step2")
            .build()
        )
        
        assert len(workflow.nodes) == 2
        assert len(workflow.edges) == 1
    
    def test_builder_with_function(self):
        """Build workflow with function node."""
        from aiccel import WorkflowBuilder
        
        def transform(state):
            state.set("transformed", True)
            return state
        
        workflow = (
            WorkflowBuilder("func_workflow")
            .add_function("transform", transform)
            .build()
        )
        
        assert len(workflow.nodes) == 1
    
    def test_builder_validation(self):
        """Builder should validate workflow."""
        from aiccel import WorkflowBuilder
        
        with pytest.raises(ValueError):
            # Empty workflow should fail
            WorkflowBuilder("empty").build()


class TestWorkflowNodes:
    """Test workflow node types."""
    
    def test_agent_node(self, mock_provider):
        """Test AgentNode."""
        from aiccel.workflows import AgentNode
        from aiccel import SlimAgent
        
        agent = SlimAgent(provider=mock_provider, name="Test")
        node = AgentNode(id="test", agent=agent)
        
        assert node.type == "agent"
        assert node.agent is agent
    
    def test_router_node(self):
        """Test RouterNode."""
        from aiccel.workflows import RouterNode
        
        node = RouterNode(
            id="router",
            routes={
                "code": lambda s: "code" in s.get("query", ""),
                "default": lambda s: True
            }
        )
        
        assert node.type == "router"
    
    def test_parallel_node(self, mock_provider):
        """Test ParallelNode."""
        from aiccel.workflows import ParallelNode, AgentNode
        from aiccel import SlimAgent
        
        agents = [SlimAgent(provider=mock_provider, name=f"A{i}") for i in range(3)]
        sub_nodes = [AgentNode(id=f"n{i}", agent=a) for i, a in enumerate(agents)]
        
        node = ParallelNode(id="parallel", nodes=sub_nodes)
        
        assert node.type == "parallel"
        assert len(node.sub_nodes) == 3


class TestWorkflowState:
    """Test workflow state management."""
    
    def test_state_get_set(self):
        """Test state get/set."""
        from aiccel.workflows import WorkflowState
        
        state = WorkflowState(inputs={"query": "test"})
        
        # Get from inputs
        assert state.get("query") == "test"
        
        # Set output
        state.set("result", "done")
        assert state.get("result") == "done"
    
    def test_state_history(self):
        """Test state history tracking."""
        from aiccel.workflows import WorkflowState, NodeStatus
        
        state = WorkflowState()
        state.add_to_history("node1", "result1", NodeStatus.SUCCESS)
        state.add_to_history("node2", "result2", NodeStatus.SUCCESS)
        
        assert len(state.history) == 2


class TestWorkflowExecution:
    """Test workflow execution."""
    
    @pytest.mark.asyncio
    async def test_simple_execution(self, mock_provider):
        """Execute simple workflow."""
        from aiccel import WorkflowBuilder, WorkflowExecutor, SlimAgent
        
        mock_provider.default_response = "Step completed"
        agent = SlimAgent(provider=mock_provider, name="Worker")
        
        workflow = (
            WorkflowBuilder("simple")
            .add_agent("step", agent, output_key="result")
            .set_end("step")
            .build()
        )
        
        executor = WorkflowExecutor(timeout=30.0)
        result = await executor.run(workflow, {"query": "test"})
        
        assert result is not None
        # The workflow should complete without errors
        assert result.error is None
    
    @pytest.mark.asyncio
    async def test_execution_timeout(self, mock_provider):
        """Workflow should timeout if too slow."""
        from aiccel import WorkflowBuilder, WorkflowExecutor
        from aiccel.workflows import WorkflowNode
        import asyncio
        
        # Create slow node
        class SlowNode(WorkflowNode):
            async def execute(self, state):
                await asyncio.sleep(10)
                return "done"
        
        workflow = (
            WorkflowBuilder("slow")
            .add_node(SlowNode(id="slow", name="Slow"))
            .build()
        )
        
        executor = WorkflowExecutor(timeout=0.1)  # Very short timeout
        result = await executor.run(workflow, {})
        
        assert result.error is not None or "timeout" in str(result.error).lower()
