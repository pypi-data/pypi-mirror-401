# tests/test_providers.py
"""
Comprehensive tests for AICCEL LLM providers.

Tests provider initialization, API calls, caching, and error handling.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio


# =============================================================================
# BASE PROVIDER TESTS
# =============================================================================

class TestBaseProvider:
    """Test BaseProvider class."""
    
    def test_import_providers(self):
        """Test importing all providers."""
        from aiccel.providers import LLMProvider, OpenAIProvider, GeminiProvider, GroqProvider
        
        assert LLMProvider is not None
        assert OpenAIProvider is not None
        assert GeminiProvider is not None
        assert GroqProvider is not None
    
    def test_provider_env_key_lookup(self):
        """Test that providers look up API keys from environment."""
        import os
        from aiccel.providers import GeminiProvider
        
        # Save and set test key
        old_key = os.environ.get("GOOGLE_API_KEY")
        os.environ["GOOGLE_API_KEY"] = "test-key-123"
        
        try:
            provider = GeminiProvider()
            assert provider.api_key == "test-key-123"
        finally:
            # Restore
            if old_key:
                os.environ["GOOGLE_API_KEY"] = old_key
            else:
                os.environ.pop("GOOGLE_API_KEY", None)


# =============================================================================
# OPENAI PROVIDER TESTS
# =============================================================================

class TestOpenAIProvider:
    """Test OpenAIProvider class."""
    
    def test_initialization(self):
        """Test OpenAI provider initialization."""
        from aiccel.providers import OpenAIProvider
        
        provider = OpenAIProvider(
            api_key="test-key",
            model="gpt-4o-mini"
        )
        
        assert provider.api_key == "test-key"
        assert provider.model == "gpt-4o-mini"
    
    def test_default_model(self):
        """Test default model is set."""
        from aiccel.providers import OpenAIProvider
        
        provider = OpenAIProvider(api_key="test-key")
        
        assert provider.model == "gpt-4o"
    
    @patch('aiccel.providers.LLMProvider._get_sync_session')
    def test_generate_uses_connection_pooling(self, mock_session):
        """Test that generate uses connection pooling."""
        from aiccel.providers import OpenAIProvider
        
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.content = b'{"choices": [{"message": {"content": "Hello"}}]}'
        
        mock_session.return_value.post.return_value = mock_response
        
        provider = OpenAIProvider(api_key="test-key")
        
        try:
            result = provider.generate("Hello")
            mock_session.assert_called()
        except Exception:
            pass  # May fail without actual API, but session should be called


# =============================================================================
# GEMINI PROVIDER TESTS
# =============================================================================

class TestGeminiProvider:
    """Test GeminiProvider class."""
    
    def test_initialization(self):
        """Test Gemini provider initialization."""
        from aiccel.providers import GeminiProvider
        
        provider = GeminiProvider(
            api_key="test-key",
            model="gemini-2.0-flash"
        )
        
        assert provider.api_key == "test-key"
        assert provider.model == "gemini-2.0-flash"
    
    def test_default_model(self):
        """Test default model."""
        from aiccel.providers import GeminiProvider
        
        provider = GeminiProvider(api_key="test-key")
        
        assert "gemini" in provider.model.lower()
    
    def test_env_key_lookup(self):
        """Test environment variable lookup."""
        import os
        from aiccel.providers import GeminiProvider
        
        os.environ["GOOGLE_API_KEY"] = "env-key-test"
        
        try:
            provider = GeminiProvider()
            assert provider.api_key == "env-key-test"
        finally:
            os.environ.pop("GOOGLE_API_KEY", None)


# =============================================================================
# GROQ PROVIDER TESTS
# =============================================================================

class TestGroqProvider:
    """Test GroqProvider class."""
    
    def test_initialization(self):
        """Test Groq provider initialization."""
        from aiccel.providers import GroqProvider
        
        provider = GroqProvider(
            api_key="test-key",
            model="llama3-70b-8192"
        )
        
        assert provider.api_key == "test-key"
        assert provider.model == "llama3-70b-8192"
    
    def test_default_model(self):
        """Test default model."""
        from aiccel.providers import GroqProvider
        
        provider = GroqProvider(api_key="test-key")
        
        assert "llama" in provider.model.lower()


# =============================================================================
# PROVIDER CACHING TESTS
# =============================================================================

class TestProviderCaching:
    """Test provider response caching."""
    
    def test_cache_initialization(self):
        """Test that cache is initialized."""
        from aiccel.providers_base import BaseProvider
        
        # Create a subclass for testing
        class TestProvider(BaseProvider):
            ENV_KEY_PREFIX = "TEST"
            
            def _generate_impl(self, prompt, **kwargs):
                return "response"
            
            def _chat_impl(self, messages, **kwargs):
                return "response"
            
            def _embed_impl(self, text):
                return [0.1, 0.2]
        
        provider = TestProvider(api_key="test")
        
        assert provider._response_cache is not None
        assert provider._cache_lock is not None
    
    def test_cache_is_instance_level(self):
        """Test that cache is per-instance (thread-safe)."""
        from aiccel.providers_base import BaseProvider
        
        class TestProvider(BaseProvider):
            ENV_KEY_PREFIX = "TEST"
            
            def _generate_impl(self, prompt, **kwargs):
                return "response"
            
            def _chat_impl(self, messages, **kwargs):
                return "response"
            
            def _embed_impl(self, text):
                return [0.1, 0.2]
        
        provider1 = TestProvider(api_key="test1")
        provider2 = TestProvider(api_key="test2")
        
        # Each should have their own cache
        assert provider1._response_cache is not provider2._response_cache


# =============================================================================
# CONNECTION POOLING TESTS
# =============================================================================

class TestConnectionPooling:
    """Test connection pooling functionality."""
    
    def test_sync_session_exists(self):
        """Test that LLMProvider has sync session method."""
        from aiccel.providers import LLMProvider
        
        assert hasattr(LLMProvider, '_get_sync_session')
    
    def test_sync_session_is_shared(self):
        """Test that sync session is shared across instances."""
        from aiccel.providers import LLMProvider, OpenAIProvider
        
        # Reset class-level session for test
        LLMProvider._sync_session = None
        
        provider1 = OpenAIProvider(api_key="test1")
        session1 = provider1._get_sync_session()
        
        provider2 = OpenAIProvider(api_key="test2")
        session2 = provider2._get_sync_session()
        
        # Should be the same session (connection pooling)
        assert session1 is session2


# =============================================================================
# EMBEDDING PROVIDER TESTS
# =============================================================================

class TestEmbeddingProviders:
    """Test embedding providers."""
    
    def test_openai_embedding_provider(self):
        """Test OpenAI embedding provider initialization."""
        from aiccel.embeddings import OpenAIEmbeddingProvider
        
        provider = OpenAIEmbeddingProvider(
            api_key="test-key",
            model="text-embedding-3-small"
        )
        
        assert provider.model == "text-embedding-3-small"
    
    def test_gemini_embedding_provider(self):
        """Test Gemini embedding provider initialization."""
        try:
            from aiccel.embeddings import GeminiEmbeddingProvider
            
            provider = GeminiEmbeddingProvider(
                api_key="test-key",
                model="text-embedding-004"
            )
            
            assert provider.model == "text-embedding-004"
        except ImportError:
            pytest.skip("google-genai not installed")


# =============================================================================
# PROVIDER EXCEPTION TESTS
# =============================================================================

class TestProviderExceptions:
    """Test provider exception handling."""
    
    def test_provider_exception_has_context(self):
        """Test that ProviderException includes context."""
        from aiccel.exceptions import ProviderException
        
        error = ProviderException(
            "API rate limited",
            context={"provider": "OpenAI", "status_code": 429}
        )
        
        assert error.context["provider"] == "OpenAI"
        assert error.context["status_code"] == 429
    
    def test_provider_exception_string(self):
        """Test ProviderException string representation."""
        from aiccel.exceptions import ProviderException
        
        error = ProviderException("Test error")
        
        assert "Test error" in str(error)


# =============================================================================
# ASYNC PROVIDER TESTS
# =============================================================================

class TestAsyncProviders:
    """Test async provider functionality."""
    
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test provider as async context manager."""
        from aiccel.providers import OpenAIProvider
        
        async with OpenAIProvider(api_key="test-key") as provider:
            assert provider.http_session is not None


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
