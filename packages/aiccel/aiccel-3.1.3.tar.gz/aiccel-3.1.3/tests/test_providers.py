"""
Tests for LLM Providers.

Coverage targets:
- OpenAIProvider
- GeminiProvider  
- GroqProvider
- Provider initialization
- Error handling
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import os


class TestOpenAIProvider:
    """Tests for OpenAIProvider."""
    
    def test_initialization_with_api_key(self):
        """Test initialization with explicit API key."""
        from aiccel.providers import OpenAIProvider
        
        with patch('aiccel.providers.requests.Session'):
            provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")
        
        assert provider.model == "gpt-4o-mini"
        assert provider.api_key == "test-key"
    
    def test_initialization_from_env(self, monkeypatch):
        """Test initialization from environment variable."""
        monkeypatch.setenv("OPENAI_API_KEY", "env-test-key")
        
        from aiccel.providers import OpenAIProvider
        
        with patch('aiccel.providers.requests.Session'):
            provider = OpenAIProvider()
        
        assert provider.api_key == "env-test-key"
    
    def test_default_model(self):
        """Test default model is set."""
        from aiccel.providers import OpenAIProvider
        
        with patch('aiccel.providers.requests.Session'):
            provider = OpenAIProvider(api_key="test-key")
        
        assert provider.model == "gpt-4o"


class TestGeminiProvider:
    """Tests for GeminiProvider."""
    
    def test_initialization_with_api_key(self):
        """Test initialization with explicit API key."""
        from aiccel.providers import GeminiProvider
        
        with patch('aiccel.providers.requests.Session'):
            provider = GeminiProvider(api_key="test-key", model="gemini-2.0-flash")
        
        assert provider.model == "gemini-2.0-flash"
        assert provider.api_key == "test-key"
    
    def test_initialization_from_env(self, monkeypatch):
        """Test initialization from environment variable."""
        monkeypatch.setenv("GOOGLE_API_KEY", "env-google-key")
        
        from aiccel.providers import GeminiProvider
        
        with patch('aiccel.providers.requests.Session'):
            provider = GeminiProvider()
        
        assert provider.api_key == "env-google-key"
    
    def test_default_model(self):
        """Test default model is set."""
        from aiccel.providers import GeminiProvider
        
        with patch('aiccel.providers.requests.Session'):
            provider = GeminiProvider(api_key="test-key")
        
        assert "gemini" in provider.model.lower()


class TestGroqProvider:
    """Tests for GroqProvider."""
    
    def test_initialization_with_api_key(self):
        """Test initialization with explicit API key."""
        from aiccel.providers import GroqProvider
        
        with patch('aiccel.providers.requests.Session'):
            provider = GroqProvider(api_key="test-key", model="llama3-70b-8192")
        
        assert provider.model == "llama3-70b-8192"
        assert provider.api_key == "test-key"
    
    def test_initialization_from_env(self, monkeypatch):
        """Test initialization from environment variable."""
        monkeypatch.setenv("GROQ_API_KEY", "env-groq-key")
        
        from aiccel.providers import GroqProvider
        
        with patch('aiccel.providers.requests.Session'):
            provider = GroqProvider()
        
        assert provider.api_key == "env-groq-key"


class TestProviderGenerate:
    """Tests for provider generate methods."""
    
    def test_generate_returns_string(self, mock_provider):
        """Test that generate returns a string."""
        result = mock_provider.generate("Hello")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_generate_with_pattern_match(self, mock_provider):
        """Test generate with pattern matching."""
        mock_provider.responses["weather"] = "It's sunny!"
        
        result = mock_provider.generate("What's the weather?")
        
        assert result == "It's sunny!"
    
    def test_generate_default_response(self, mock_provider):
        """Test generate falls back to default."""
        result = mock_provider.generate("Something random")
        
        assert result == mock_provider.default_response


class TestProviderChat:
    """Tests for provider chat methods."""
    
    def test_chat_with_messages(self, mock_provider):
        """Test chat with message history."""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"}
        ]
        
        result = mock_provider.chat(messages)
        
        assert isinstance(result, str)


class TestProviderEmbed:
    """Tests for provider embedding methods."""
    
    def test_embed_returns_list(self, mock_provider):
        """Test embed returns a list of floats."""
        result = mock_provider.embed("Test text")
        
        assert isinstance(result, list)
        assert all(isinstance(x, float) for x in result)
    
    def test_embed_deterministic(self, mock_provider):
        """Test embed is deterministic for same input."""
        text = "Same input text"
        
        result1 = mock_provider.embed(text)
        result2 = mock_provider.embed(text)
        
        assert result1 == result2


class TestProviderCallHistory:
    """Tests for provider call history tracking."""
    
    def test_call_history_recorded(self, mock_provider):
        """Test that calls are recorded."""
        assert len(mock_provider.call_history) == 0
        
        mock_provider.generate("First call")
        mock_provider.generate("Second call")
        
        assert len(mock_provider.call_history) == 2
    
    def test_clear_history(self, mock_provider):
        """Test clearing call history."""
        mock_provider.generate("Test")
        assert len(mock_provider.call_history) == 1
        
        mock_provider.clear_history()
        
        assert len(mock_provider.call_history) == 0
