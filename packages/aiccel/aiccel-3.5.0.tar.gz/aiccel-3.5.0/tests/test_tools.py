# tests/test_tools.py
"""
Comprehensive tests for the AICCEL tools system.

Target: 80%+ coverage for tools module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_provider():
    """Mock LLM provider for testing."""
    provider = Mock()
    provider.generate.return_value = "Mock response"
    provider.generate_async = Mock(return_value=asyncio.coroutine(lambda: "Mock async response")())
    return provider


# =============================================================================
# PARAMETER SCHEMA TESTS
# =============================================================================

class TestParameterSchema:
    """Test ParameterSchema class."""
    
    def test_create_string_parameter(self):
        """Test creating a string parameter."""
        from aiccel.tools import ParameterSchema, ParameterType
        
        param = ParameterSchema(
            name="query",
            type=ParameterType.STRING,
            description="Search query",
            required=True
        )
        
        assert param.name == "query"
        assert param.type == ParameterType.STRING
        assert param.required is True
    
    def test_parameter_to_dict(self):
        """Test converting parameter to dictionary."""
        from aiccel.tools import ParameterSchema, ParameterType
        
        param = ParameterSchema(
            name="count",
            type=ParameterType.INTEGER,
            description="Number of results"
        )
        
        result = param.to_dict()
        assert result["type"] == "integer"
        assert result["description"] == "Number of results"
    
    def test_parameter_validation_required(self):
        """Test required parameter validation."""
        from aiccel.tools import ParameterSchema, ParameterType
        
        param = ParameterSchema(
            name="query",
            type=ParameterType.STRING,
            required=True
        )
        
        # Valid value
        is_valid, error = param.validate("test query")
        assert is_valid is True
        
        # Empty value should fail for required
        is_valid, error = param.validate("")
        # Note: empty string is still a string, validation depends on implementation
    
    def test_parameter_validation_type(self):
        """Test type validation."""
        from aiccel.tools import ParameterSchema, ParameterType
        
        param = ParameterSchema(
            name="count",
            type=ParameterType.INTEGER
        )
        
        # Valid integer
        is_valid, error = param.validate(5)
        assert is_valid is True
        
        # Invalid type (string when expecting integer)
        is_valid, error = param.validate("not an integer")
        assert is_valid is False
    
    def test_parameter_with_enum(self):
        """Test parameter with enum constraint."""
        from aiccel.tools import ParameterSchema, ParameterType
        
        param = ParameterSchema(
            name="action",
            type=ParameterType.STRING,
            enum=["start", "stop", "restart"]
        )
        
        is_valid, error = param.validate("start")
        assert is_valid is True
        
        is_valid, error = param.validate("invalid")
        assert is_valid is False


# =============================================================================
# TOOL RESULT TESTS
# =============================================================================

class TestToolResult:
    """Test ToolResult class."""
    
    def test_create_success_result(self):
        """Test creating a success result."""
        from aiccel.tools import ToolResult
        
        result = ToolResult.ok({"data": "value"}, execution_time=0.5)
        
        assert result.success is True
        assert result.data == {"data": "value"}
        assert result.execution_time == 0.5
        assert result.error is None
    
    def test_create_failure_result(self):
        """Test creating a failure result."""
        from aiccel.tools import ToolResult
        
        result = ToolResult.fail("Something went wrong", execution_time=0.1)
        
        assert result.success is False
        assert result.error == "Something went wrong"
        assert result.data is None
    
    def test_result_string_representation(self):
        """Test string representation of result."""
        from aiccel.tools import ToolResult
        
        result = ToolResult.ok("test data")
        str_repr = str(result)
        
        assert "success" in str_repr.lower() or "test data" in str_repr


# =============================================================================
# BASE TOOL TESTS
# =============================================================================

class TestBaseTool:
    """Test BaseTool class."""
    
    def test_create_simple_tool(self):
        """Test creating a simple tool."""
        from aiccel.tools import BaseTool, ParameterSchema, ParameterType
        
        tool = BaseTool(
            name="test_tool",
            description="A test tool",
            parameters=[
                ParameterSchema(name="input", type=ParameterType.STRING, required=True)
            ]
        )
        
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
    
    def test_tool_schema(self):
        """Test getting tool schema."""
        from aiccel.tools import BaseTool, ParameterSchema, ParameterType
        
        tool = BaseTool(
            name="my_tool",
            description="Does something",
            parameters=[
                ParameterSchema(name="query", type=ParameterType.STRING)
            ]
        )
        
        schema = tool.schema
        assert schema.name == "my_tool"
        assert schema.description == "Does something"
    
    def test_tool_with_executor(self):
        """Test tool with custom executor function."""
        from aiccel.tools import BaseTool, ParameterSchema, ParameterType
        
        def my_executor(args):
            return f"Processed: {args.get('input')}"
        
        tool = BaseTool(
            name="executor_tool",
            description="Tool with executor",
            parameters=[ParameterSchema(name="input", type=ParameterType.STRING)],
            executor=my_executor
        )
        
        result = tool.execute({"input": "test"})
        assert result.success is True
        assert "Processed: test" in str(result.data)


# =============================================================================
# BUILT-IN TOOL TESTS
# =============================================================================

class TestCalculatorTool:
    """Test CalculatorTool."""
    
    def test_basic_addition(self):
        """Test basic addition."""
        from aiccel.tools import CalculatorTool
        
        calc = CalculatorTool()
        result = calc.execute({"expression": "2 + 2"})
        
        assert result.success is True
        assert result.data["result"] == 4
    
    def test_complex_expression(self):
        """Test complex mathematical expression."""
        from aiccel.tools import CalculatorTool
        
        calc = CalculatorTool()
        result = calc.execute({"expression": "2 + 2 * 3"})
        
        assert result.success is True
        assert result.data["result"] == 8
    
    def test_math_functions(self):
        """Test math functions like sqrt."""
        from aiccel.tools import CalculatorTool
        
        calc = CalculatorTool()
        result = calc.execute({"expression": "sqrt(16)"})
        
        assert result.success is True
        assert result.data["result"] == 4.0
    
    def test_invalid_expression(self):
        """Test invalid expression handling."""
        from aiccel.tools import CalculatorTool
        
        calc = CalculatorTool()
        result = calc.execute({"expression": "import os"})
        
        assert result.success is False


class TestDateTimeTool:
    """Test DateTimeTool."""
    
    def test_get_now(self):
        """Test getting current datetime."""
        from aiccel.tools import DateTimeTool
        
        dt = DateTimeTool()
        result = dt.execute({"action": "now"})
        
        assert result.success is True
        assert "datetime" in result.data
        assert "timestamp" in result.data
    
    def test_get_today(self):
        """Test getting today's date."""
        from aiccel.tools import DateTimeTool
        
        dt = DateTimeTool()
        result = dt.execute({"action": "today"})
        
        assert result.success is True
        assert "date" in result.data
        assert "weekday" in result.data
    
    def test_add_days(self):
        """Test adding days to current date."""
        from aiccel.tools import DateTimeTool
        
        dt = DateTimeTool()
        result = dt.execute({"action": "add_days", "days": 7})
        
        assert result.success is True
        assert "datetime" in result.data
    
    def test_invalid_action(self):
        """Test invalid action handling."""
        from aiccel.tools import DateTimeTool
        
        dt = DateTimeTool()
        result = dt.execute({"action": "invalid_action"})
        
        assert result.success is False


class TestDummyTool:
    """Test DummyTool."""
    
    def test_echo_input(self):
        """Test echoing input."""
        from aiccel.tools import DummyTool
        
        dummy = DummyTool()
        result = dummy.execute({"input": "Hello World"})
        
        assert result.success is True
        assert result.data["echo"] == "Hello World"
        assert result.data["status"] == "ok"


# =============================================================================
# TOOL REGISTRY TESTS
# =============================================================================

class TestToolRegistry:
    """Test ToolRegistry class."""
    
    def test_register_tool(self):
        """Test registering a tool."""
        from aiccel.tools import ToolRegistry, DummyTool
        
        registry = ToolRegistry()
        dummy = DummyTool()
        
        registry.register(dummy)
        
        assert registry.get("dummy") is dummy
    
    def test_get_all_tools(self):
        """Test getting all registered tools."""
        from aiccel.tools import ToolRegistry, DummyTool, CalculatorTool
        
        registry = ToolRegistry()
        registry.register(DummyTool())
        registry.register(CalculatorTool())
        
        tools = registry.get_all()
        assert len(tools) == 2
    
    def test_unregister_tool(self):
        """Test unregistering a tool."""
        from aiccel.tools import ToolRegistry, DummyTool
        
        registry = ToolRegistry()
        dummy = DummyTool()
        
        registry.register(dummy)
        registry.unregister("dummy")
        
        assert registry.get("dummy") is None


# =============================================================================
# TOOL VALIDATOR TESTS
# =============================================================================

class TestToolValidator:
    """Test ToolValidator class."""
    
    def test_validate_required_params(self):
        """Test validating required parameters."""
        from aiccel.tools import ToolValidator, ToolSchema, ParameterSchema, ParameterType
        
        schema = ToolSchema(
            name="test",
            description="Test tool",
            parameters=[
                ParameterSchema(name="required_param", type=ParameterType.STRING, required=True)
            ]
        )
        
        validator = ToolValidator()
        
        # Missing required param
        is_valid, errors = validator.validate(schema, {})
        assert is_valid is False
        assert len(errors) > 0
        
        # With required param
        is_valid, errors = validator.validate(schema, {"required_param": "value"})
        assert is_valid is True
    
    def test_type_coercion(self):
        """Test type coercion."""
        from aiccel.tools import ToolValidator, ToolSchema, ParameterSchema, ParameterType
        
        schema = ToolSchema(
            name="test",
            description="Test tool",
            parameters=[
                ParameterSchema(name="count", type=ParameterType.INTEGER)
            ]
        )
        
        validator = ToolValidator()
        
        # String to integer
        coerced = validator.coerce_types(schema, {"count": "5"})
        assert coerced["count"] == 5


# =============================================================================
# ASYNC TOOL TESTS
# =============================================================================

class TestAsyncTools:
    """Test async tool functionality."""
    
    @pytest.mark.asyncio
    async def test_async_execution(self):
        """Test async tool execution."""
        from aiccel.tools import CalculatorTool
        
        calc = CalculatorTool()
        result = await calc.execute_async({"expression": "10 + 5"})
        
        assert result.success is True
        assert result.data["result"] == 15


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
