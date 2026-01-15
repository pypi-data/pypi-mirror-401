"""
Tests for AgentManager multi-agent orchestration.

Coverage targets:
- Manager initialization
- Agent routing
- Agent collaboration
- Error handling
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock


class TestAgentManagerInit:
    """Tests for AgentManager initialization."""
    
    def test_basic_initialization(self, mock_provider):
        """Test basic manager creation."""
        from aiccel.manager import AgentManager
        
        manager = AgentManager(llm_provider=mock_provider)
        
        assert manager.llm_provider == mock_provider
        assert len(manager.agents) == 0
    
    def test_initialization_with_agents(self, mock_provider):
        """Test manager with initial agents."""
        from aiccel.manager import AgentManager
        from aiccel.agent import Agent
        
        agent1 = Agent(provider=mock_provider, name="Agent1")
        agent2 = Agent(provider=mock_provider, name="Agent2")
        
        manager = AgentManager(
            llm_provider=mock_provider,
            agents={
                "agent1": {"agent": agent1, "description": "First agent"},
                "agent2": {"agent": agent2, "description": "Second agent"}
            }
        )
        
        assert len(manager.agents) == 2


class TestAddAgent:
    """Tests for adding agents."""
    
    def test_add_agent(self, mock_provider):
        """Test adding an agent."""
        from aiccel.manager import AgentManager
        from aiccel.agent import Agent
        
        manager = AgentManager(llm_provider=mock_provider)
        agent = Agent(provider=mock_provider, name="NewAgent")
        
        manager.add_agent("new_agent", agent, "A new agent")
        
        assert "new_agent" in manager.agents


class TestFromAgents:
    """Tests for from_agents class method."""
    
    def test_from_agents_classmethod(self, mock_provider):
        """Test creating manager from agent list."""
        from aiccel.manager import AgentManager
        from aiccel.agent import Agent
        
        agent1 = Agent(provider=mock_provider, name="Agent1")
        agent1.config.description = "First agent"
        
        agent2 = Agent(provider=mock_provider, name="Agent2")
        agent2.config.description = "Second agent"
        
        manager = AgentManager.from_agents(
            agents=[agent1, agent2],
            llm_provider=mock_provider
        )
        
        assert len(manager.agents) == 2


class TestRoute:
    """Tests for query routing."""
    
    def test_route_simple_query(self, mock_provider):
        """Test routing a simple query."""
        from aiccel.manager import AgentManager
        from aiccel.agent import Agent
        
        # Configure mock to return routing decision
        mock_provider.responses[""] = '{"agent": "search_agent", "sub_queries": [{"agent": "search_agent", "query": "test"}]}'
        
        agent = Agent(provider=mock_provider, name="SearchAgent")
        
        manager = AgentManager(
            llm_provider=mock_provider,
            agents={
                "search_agent": {"agent": agent, "description": "Search agent"}
            }
        )
        
        result = manager.route("Search for something")
        
        assert "response" in result


class TestSetVerbose:
    """Tests for verbose mode."""
    
    def test_set_verbose(self, mock_provider):
        """Test setting verbose mode."""
        from aiccel.manager import AgentManager
        
        manager = AgentManager(llm_provider=mock_provider, verbose=False)
        assert manager.verbose is False
        
        manager.set_verbose(True)
        assert manager.verbose is True


class TestSetInstructions:
    """Tests for custom instructions."""
    
    def test_set_instructions(self, mock_provider):
        """Test setting custom instructions."""
        from aiccel.manager import AgentManager
        
        manager = AgentManager(llm_provider=mock_provider)
        manager.set_instructions("Route all queries to the best agent")
        
        assert manager.instructions == "Route all queries to the best agent"


class TestCache:
    """Tests for caching mechanism."""
    
    def test_cache_set_and_get(self, mock_provider):
        """Test cache operations."""
        from aiccel.manager import AgentManager
        
        manager = AgentManager(llm_provider=mock_provider)
        
        manager._set_in_cache("test_key", "test_value")
        cached = manager._get_from_cache("test_key")
        
        assert cached == "test_value"
    
    def test_cache_clear(self, mock_provider):
        """Test clearing cache."""
        from aiccel.manager import AgentManager
        
        manager = AgentManager(llm_provider=mock_provider)
        
        manager._set_in_cache("key1", "value1")
        manager._set_in_cache("key2", "value2")
        
        manager._clear_cache()
        
        assert manager._get_from_cache("key1") is None
        assert manager._get_from_cache("key2") is None
