"""
Tests for the Agent class.

Coverage targets:
- Agent initialization
- Agent.run() execution
- Agent.run_async() execution  
- Tool integration
- Memory management
- Error handling
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio


class TestAgentConfig:
    """Tests for AgentConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        from aiccel.agent import AgentConfig
        
        config = AgentConfig()
        
        assert config.name == "Agent"
        assert config.memory_type == "buffer"
        assert config.max_memory_turns == 10
        assert config.max_memory_tokens == 4000
        assert config.strict_tool_usage is False
        assert config.verbose is False
        assert config.timeout == 60.0
    
    def test_custom_config(self):
        """Test custom configuration."""
        from aiccel.agent import AgentConfig
        
        config = AgentConfig(
            name="CustomBot",
            instructions="Be helpful.",
            memory_type="summary",
            max_memory_turns=20,
            strict_tool_usage=True,
            verbose=True
        )
        
        assert config.name == "CustomBot"
        assert config.instructions == "Be helpful."
        assert config.memory_type == "summary"
        assert config.max_memory_turns == 20
        assert config.strict_tool_usage is True
        assert config.verbose is True


class TestAgentInitialization:
    """Tests for Agent initialization."""
    
    def test_basic_initialization(self, mock_provider):
        """Test basic agent creation."""
        from aiccel.agent import Agent
        
        agent = Agent(provider=mock_provider)
        
        assert agent.provider == mock_provider
        assert agent.tools == []
        assert agent.config.name == "Agent"
        assert agent._initialized is False
    
    def test_initialization_with_name(self, mock_provider):
        """Test agent with custom name."""
        from aiccel.agent import Agent
        
        agent = Agent(
            provider=mock_provider,
            name="TestAgent",
            instructions="You are a test agent."
        )
        
        assert agent.config.name == "TestAgent"
        assert agent.config.instructions == "You are a test agent."
    
    def test_initialization_with_tools(self, mock_provider, mock_tool):
        """Test agent with tools."""
        from aiccel.agent import Agent
        
        agent = Agent(
            provider=mock_provider,
            tools=[mock_tool]
        )
        
        assert len(agent.tools) == 1
        assert agent.tools[0].name == "mock_tool"
    
    def test_initialization_with_config(self, mock_provider):
        """Test agent with AgentConfig."""
        from aiccel.agent import Agent, AgentConfig
        
        config = AgentConfig(
            name="ConfigAgent",
            memory_type="window",
            max_memory_turns=5
        )
        
        agent = Agent(provider=mock_provider, config=config)
        
        assert agent.config.name == "ConfigAgent"
        assert agent.config.memory_type == "window"
        assert agent.config.max_memory_turns == 5


class TestAgentRun:
    """Tests for Agent.run() method."""
    
    def test_simple_run(self, mock_provider):
        """Test basic run execution."""
        from aiccel.agent import Agent
        
        agent = Agent(
            provider=mock_provider,
            name="SimpleAgent"
        )
        
        result = agent.run("Hello, world!")
        
        assert "response" in result
        assert isinstance(result["response"], str)
    
    def test_run_with_tools(self, mock_provider, mock_tool):
        """Test run with tool execution."""
        from aiccel.agent import Agent
        
        # Configure mock to suggest tool usage
        mock_provider.responses[""] = "I'll use the mock_tool to help you."
        
        agent = Agent(
            provider=mock_provider,
            tools=[mock_tool],
            verbose=False
        )
        
        result = agent.run("Use the tool please")
        
        assert "response" in result
        assert "tools_used" in result
    
    def test_run_returns_error_on_exception(self, mock_provider):
        """Test that run returns error response instead of raising."""
        from aiccel.agent import Agent
        
        # Make provider raise an exception
        mock_provider.generate = MagicMock(side_effect=Exception("API Error"))
        
        agent = Agent(provider=mock_provider)
        result = agent.run("Test query")
        
        assert "error" in result
        assert "API Error" in result.get("error", "") or "API Error" in result.get("response", "")


class TestAgentAsync:
    """Tests for Agent async methods."""
    
    @pytest.mark.asyncio
    async def test_run_async(self, mock_provider):
        """Test async run execution."""
        from aiccel.agent import Agent
        
        agent = Agent(provider=mock_provider)
        
        result = await agent.run_async("Hello async!")
        
        assert "response" in result
        assert isinstance(result["response"], str)


class TestAgentMemory:
    """Tests for Agent memory management."""
    
    def test_get_memory_empty(self, mock_provider):
        """Test getting empty memory."""
        from aiccel.agent import Agent
        
        agent = Agent(provider=mock_provider)
        agent._lazy_init()
        
        memory = agent.get_memory()
        
        assert isinstance(memory, list)
        assert len(memory) == 0
    
    def test_clear_memory(self, mock_provider):
        """Test clearing memory."""
        from aiccel.agent import Agent
        
        agent = Agent(provider=mock_provider)
        agent._lazy_init()
        
        # Add some history
        agent.memory.add_user_message("Test message")
        agent.memory.add_assistant_message("Test response")
        
        assert len(agent.get_memory()) > 0
        
        agent.clear_memory()
        
        assert len(agent.get_memory()) == 0


class TestAgentToolManagement:
    """Tests for Agent tool management."""
    
    def test_add_tool(self, mock_provider, mock_tool):
        """Test adding a tool after initialization."""
        from aiccel.agent import Agent
        
        agent = Agent(provider=mock_provider)
        assert len(agent.tools) == 0
        
        result = agent.add_tool(mock_tool)
        
        assert len(agent.tools) == 1
        assert result is agent  # Check chaining works
    
    def test_with_tool_alias(self, mock_provider, mock_tool):
        """Test with_tool alias."""
        from aiccel.agent import Agent
        
        agent = Agent(provider=mock_provider)
        result = agent.with_tool(mock_tool)
        
        assert len(agent.tools) == 1
        assert result is agent
    
    def test_tool_chaining(self, mock_provider):
        """Test chaining multiple tools."""
        from aiccel.agent import Agent
        from tests.conftest import MockTool
        
        tool1 = MockTool(name="tool1")
        tool2 = MockTool(name="tool2")
        tool3 = MockTool(name="tool3")
        
        agent = Agent(provider=mock_provider)
        agent.add_tool(tool1).add_tool(tool2).add_tool(tool3)
        
        assert len(agent.tools) == 3


class TestAgentConfiguration:
    """Tests for Agent configuration methods."""
    
    def test_enable_thinking(self, mock_provider):
        """Test enabling thinking mode."""
        from aiccel.agent import Agent
        
        agent = Agent(provider=mock_provider)
        
        assert agent.config.thinking_enabled is False
        
        result = agent.enable_thinking(True)
        
        assert agent.config.thinking_enabled is True
        assert result is agent  # Check chaining
    
    def test_set_verbose(self, mock_provider):
        """Test setting verbose mode."""
        from aiccel.agent import Agent
        
        agent = Agent(provider=mock_provider)
        
        assert agent.config.verbose is False
        
        agent.set_verbose(True)
        
        assert agent.config.verbose is True


class TestAgentRepr:
    """Tests for Agent string representation."""
    
    def test_repr(self, mock_provider, mock_tool):
        """Test __repr__ method."""
        from aiccel.agent import Agent
        
        agent = Agent(
            provider=mock_provider,
            tools=[mock_tool],
            name="TestAgent"
        )
        
        repr_str = repr(agent)
        
        assert "TestAgent" in repr_str
        assert "tools=1" in repr_str


class TestCreateAgent:
    """Tests for create_agent convenience function."""
    
    def test_create_agent_function(self, mock_provider):
        """Test create_agent helper."""
        from aiccel.agent import create_agent
        
        agent = create_agent(
            provider=mock_provider,
            name="HelperAgent"
        )
        
        assert agent.config.name == "HelperAgent"
