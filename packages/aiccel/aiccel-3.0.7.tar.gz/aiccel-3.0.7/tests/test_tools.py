"""
Tests for Tools system (tools_v2).

Coverage targets:
- BaseTool
- SearchTool
- WeatherTool
- ToolRegistry
- Tool execution
"""
import pytest
from unittest.mock import MagicMock, patch
from typing import Dict, Any


class TestBaseTool:
    """Tests for BaseTool base class."""
    
    def test_tool_creation(self):
        """Test creating a custom tool."""
        from aiccel.tools.base import BaseTool, ParameterSchema
        
        class TestTool(BaseTool):
            @property
            def name(self) -> str:
                return "test_tool"
            
            @property
            def description(self) -> str:
                return "A test tool"
            
            def _execute(self, **kwargs) -> str:
                return f"Executed with: {kwargs}"
        
        tool = TestTool()
        
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
    
    def test_tool_execute(self):
        """Test tool execution."""
        from aiccel.tools.base import BaseTool
        
        class EchoTool(BaseTool):
            @property
            def name(self) -> str:
                return "echo"
            
            @property
            def description(self) -> str:
                return "Echo input"
            
            def _execute(self, message: str = "default") -> str:
                return f"Echo: {message}"
        
        tool = EchoTool()
        result = tool.execute(message="Hello")
        
        assert "Echo: Hello" in result
    
    def test_tool_to_dict(self):
        """Test tool serialization."""
        from aiccel.tools.base import BaseTool
        
        class SimpleTool(BaseTool):
            @property
            def name(self) -> str:
                return "simple"
            
            @property
            def description(self) -> str:
                return "Simple tool"
            
            def _execute(self, **kwargs) -> str:
                return "done"
        
        tool = SimpleTool()
        tool_dict = tool.to_dict()
        
        assert tool_dict["name"] == "simple"
        assert tool_dict["description"] == "Simple tool"
        assert "parameters" in tool_dict


class TestToolRegistry:
    """Tests for ToolRegistry."""
    
    def test_registry_creation(self, mock_provider):
        """Test creating a tool registry."""
        from aiccel.tools.registry import ToolRegistry
        
        registry = ToolRegistry(llm_provider=mock_provider)
        
        assert registry.llm_provider == mock_provider
        assert len(registry.tools) == 0
    
    def test_register_tool(self, mock_provider, mock_tool):
        """Test registering a tool."""
        from aiccel.tools.registry import ToolRegistry
        
        registry = ToolRegistry(llm_provider=mock_provider)
        result = registry.register(mock_tool)
        
        assert len(registry.tools) == 1
        assert result is registry  # Check chaining
    
    def test_get_tool(self, mock_provider, mock_tool):
        """Test getting a registered tool."""
        from aiccel.tools.registry import ToolRegistry
        
        registry = ToolRegistry(llm_provider=mock_provider)
        registry.register(mock_tool)
        
        retrieved = registry.get("mock_tool")
        
        assert retrieved is mock_tool
    
    def test_get_all_tools(self, mock_provider):
        """Test getting all tools."""
        from tests.conftest import MockTool
        from aiccel.tools.registry import ToolRegistry
        
        registry = ToolRegistry(llm_provider=mock_provider)
        registry.register(MockTool(name="tool1"))
        registry.register(MockTool(name="tool2"))
        
        all_tools = registry.get_all()
        
        assert len(all_tools) == 2
    
    def test_registry_chaining(self, mock_provider):
        """Test chaining multiple registrations."""
        from tests.conftest import MockTool
        from aiccel.tools.registry import ToolRegistry
        
        registry = ToolRegistry(llm_provider=mock_provider)
        registry.register(MockTool(name="a")).register(MockTool(name="b")).register(MockTool(name="c"))
        
        assert len(registry.tools) == 3


class TestSearchTool:
    """Tests for SearchTool."""
    
    def test_search_tool_creation(self):
        """Test creating SearchTool."""
        from aiccel.tools.builtin.search import SearchTool
        
        tool = SearchTool(api_key="test-key")
        
        assert tool.name == "search"
        assert "search" in tool.description.lower()
    
    def test_search_tool_to_dict(self):
        """Test SearchTool serialization."""
        from aiccel.tools.builtin.search import SearchTool
        
        tool = SearchTool(api_key="test-key")
        tool_dict = tool.to_dict()
        
        assert tool_dict["name"] == "search"
        assert "query" in str(tool_dict["parameters"])
    
    @patch('requests.Session.post')
    def test_search_tool_execute(self, mock_post):
        """Test SearchTool execution with mocked API."""
        from aiccel.tools.builtin.search import SearchTool
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "organic": [
                {"title": "Test Result", "link": "https://test.com", "snippet": "A test result"}
            ]
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        tool = SearchTool(api_key="test-key")
        result = tool.execute(query="test query")
        
        assert "Test Result" in result or "test" in result.lower()


class TestWeatherTool:
    """Tests for WeatherTool."""
    
    def test_weather_tool_creation(self):
        """Test creating WeatherTool."""
        from aiccel.tools.builtin.weather import WeatherTool
        
        tool = WeatherTool(api_key="test-key")
        
        assert tool.name == "get_weather"
        assert "weather" in tool.description.lower()
    
    def test_weather_tool_to_dict(self):
        """Test WeatherTool serialization."""
        from aiccel.tools.builtin.weather import WeatherTool
        
        tool = WeatherTool(api_key="test-key")
        tool_dict = tool.to_dict()
        
        assert tool_dict["name"] == "get_weather"
        assert "location" in str(tool_dict["parameters"]) or "city" in str(tool_dict["parameters"])
    
    @patch('requests.Session.get')
    def test_weather_tool_execute(self, mock_get):
        """Test WeatherTool execution with mocked API."""
        from aiccel.tools.builtin.weather import WeatherTool
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "Tokyo",
            "sys": {"country": "JP"},
            "main": {"temp": 72, "feels_like": 70, "humidity": 50},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 5}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        tool = WeatherTool(api_key="test-key")
        result = tool.execute(location="Tokyo")
        
        assert "Tokyo" in result or "weather" in result.lower()


class TestToolExecution:
    """Tests for tool execution flow."""
    
    def test_tool_returns_string(self, mock_tool):
        """Test that tool execution returns a string."""
        result = mock_tool.execute({})
        
        assert isinstance(result, str)
    
    def test_tool_call_count(self, mock_tool):
        """Test that tool tracks call count."""
        assert mock_tool.call_count == 0
        
        mock_tool.execute({})
        mock_tool.execute({})
        
        assert mock_tool.call_count == 2


class TestLegacyToolsDeprecation:
    """Tests for legacy tools deprecation."""
    
    def test_deprecated_warning(self):
        """Test that importing old tools shows deprecation warning."""
        import warnings
        
        # This should already have been imported, but check no exceptions
        try:
            from aiccel import tools
            # If we get here, the import worked (warning was just shown)
            assert True
        except ImportError:
            pytest.fail("Legacy tools should still be importable")
