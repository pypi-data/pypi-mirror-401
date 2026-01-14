"""
Pytest configuration and shared fixtures.
"""
import pytest
import os
import sys
from unittest.mock import MagicMock, AsyncMock, patch
from typing import Dict, Any, List


# Add the package to path for testing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MockLLMProvider:
    """
    Mock LLM provider for testing without API calls.
    
    This mock simulates LLM responses for deterministic testing.
    """
    
    def __init__(self, responses: Dict[str, str] = None, default_response: str = "Mock response"):
        """
        Initialize mock provider.
        
        Args:
            responses: Dict mapping query patterns to responses
            default_response: Default response when no pattern matches
        """
        self.responses = responses or {}
        self.default_response = default_response
        self.call_history: List[Dict] = []
        self.model = "mock-model"
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Synchronous generation."""
        self.call_history.append({"prompt": prompt, "kwargs": kwargs})
        
        # Check for pattern matches
        for pattern, response in self.responses.items():
            if pattern.lower() in prompt.lower():
                return response
        
        return self.default_response
    
    async def generate_async(self, prompt: str, **kwargs) -> str:
        """Async generation."""
        return self.generate(prompt, **kwargs)
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """Chat completion."""
        # Extract the last user message
        last_message = messages[-1]["content"] if messages else ""
        return self.generate(last_message, **kwargs)
    
    async def chat_async(self, messages: List[Dict], **kwargs) -> str:
        """Async chat completion."""
        return self.chat(messages, **kwargs)
    
    def embed(self, text: str) -> List[float]:
        """Generate mock embeddings."""
        # Return deterministic embeddings based on text length
        return [0.1 * (i % 10) for i in range(len(text) % 100 + 100)]
    
    async def embed_async(self, text: str) -> List[float]:
        """Async embedding."""
        return self.embed(text)
    
    def clear_history(self):
        """Clear call history."""
        self.call_history = []


class MockTool:
    """Mock tool for testing."""
    
    def __init__(self, name: str = "mock_tool", response: str = "Mock tool executed"):
        self.name = name
        self.description = f"Mock tool: {name}"
        self.response = response
        self.call_count = 0
        self._parameters = []
    
    def execute(self, args: Dict[str, Any]) -> str:
        """Execute mock tool."""
        self.call_count += 1
        return self.response
    
    async def execute_async(self, args: Dict[str, Any]) -> str:
        """Async execute mock tool."""
        return self.execute(args)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }


@pytest.fixture
def mock_provider():
    """Provide a mock LLM provider."""
    return MockLLMProvider(
        responses={
            "weather": "The weather is sunny, 72°F",
            "search": '["search"]',
            "tool": '["mock_tool"]',
            "hello": "Hello! How can I help you today?",
        },
        default_response="I can help you with that."
    )


@pytest.fixture
def mock_tool():
    """Provide a mock tool."""
    return MockTool()


@pytest.fixture
def sample_dataframe():
    """Provide a sample pandas DataFrame for Pandora tests."""
    try:
        import pandas as pd
        return pd.DataFrame({
            "name": ["John Doe", "Jane Smith", "Bob Wilson"],
            "email": ["john@example.com", "jane@test.org", "bob@company.net"],
            "phone": ["555-1234", "555-5678", "555-9012"],
            "salary": [50000, 60000, 55000],
            "department": ["Engineering", "Marketing", "Sales"]
        })
    except ImportError:
        pytest.skip("pandas not available")


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for file operations."""
    return tmp_path


@pytest.fixture
def env_setup(monkeypatch):
    """Setup environment variables for testing."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("GROQ_API_KEY", "test-groq-key")
    monkeypatch.setenv("SERPER_API_KEY", "test-serper-key")
    monkeypatch.setenv("OPENWEATHERMAP_API_KEY", "test-weather-key")


# Async test support
@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
