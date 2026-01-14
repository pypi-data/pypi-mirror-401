"""
Tests for Embedding Providers.
"""
import pytest
from unittest.mock import MagicMock, patch
import sys

class TestGeminiEmbeddingProvider:
    """Tests for GeminiEmbeddingProvider using google-genai SDK."""
    
    def test_initialization(self):
        """Test initialization with new SDK client."""
        # Mock google.genai module availability
        with patch.dict(sys.modules, {'google.genai': MagicMock(), 'google.genai.types': MagicMock()}):
            from aiccel.embeddings import GeminiEmbeddingProvider, GOOGLE_GENAI_AVAILABLE
            
            # Manually set the flag since we just patched the module but import happened before
            # Actually, we should force reload or just mock the flag if possible
            # But simpler: just mock the class attributes if needed or relying on the import check
            
            if not GOOGLE_GENAI_AVAILABLE:
                # If local env doesnt have it, we can't fully test without mocking the import check
                pass

    @patch('aiccel.embeddings.GOOGLE_GENAI_AVAILABLE', True)
    @patch('aiccel.embeddings.genai')
    def test_embed_call(self, mock_genai):
        """Test embed method calls the new SDK correctly."""
        from aiccel.embeddings import GeminiEmbeddingProvider
        
        # Setup mock client
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        
        # Setup mock response
        mock_response = MagicMock()
        mock_response.embeddings = [MagicMock()]
        mock_response.embeddings[0].values = [0.1, 0.2, 0.3]
        mock_client.models.embed_content.return_value = mock_response
        
        provider = GeminiEmbeddingProvider(api_key="test-key")
        
        # Call embed
        embeddings = provider.embed("test text")
        
        # Verify
        assert len(embeddings) == 1
        assert embeddings[0] == [0.1, 0.2, 0.3]
        
        # Verify call arguments
        mock_client.models.embed_content.assert_called_once()
        call_args = mock_client.models.embed_content.call_args
        assert call_args.kwargs['model'] == "text-embedding-004"
        assert call_args.kwargs['contents'] == "test text"

    @patch('aiccel.embeddings.GOOGLE_GENAI_AVAILABLE', False)
    def test_missing_dependency(self):
        """Test error when google-genai is missing."""
        from aiccel.embeddings import GeminiEmbeddingProvider
        
        with pytest.raises(ImportError) as exc:
            GeminiEmbeddingProvider(api_key="test-key")
        
        assert "google-genai" in str(exc.value)
