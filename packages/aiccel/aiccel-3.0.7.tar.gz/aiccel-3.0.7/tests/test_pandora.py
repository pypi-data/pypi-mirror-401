"""
Tests for Pandora ETL module.

Coverage targets:
- DataFrame loading
- Code generation
- Code execution
- Error handling and retries
- Security restrictions
"""
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd


class TestPandoraInitialization:
    """Tests for Pandora initialization."""
    
    def test_basic_initialization(self, mock_provider):
        """Test basic Pandora creation."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider)
        
        assert pandora.llm == mock_provider
        assert pandora.max_retries == 4
        assert pandora.verbose is True
    
    def test_custom_retries(self, mock_provider):
        """Test custom retry configuration."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider, max_retries=2)
        
        assert pandora.max_retries == 2


class TestPandoraProfile:
    """Tests for data profiling."""
    
    def test_profile_data(self, mock_provider, sample_dataframe):
        """Test DataFrame profiling."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider, verbose=False)
        profile = pandora._profile_data(sample_dataframe)
        
        assert "shape" in profile
        assert profile["shape"] == (3, 5)
        assert "columns" in profile
        assert "name" in profile["columns"]
        assert "email" in profile["columns"]
    
    def test_profile_numeric_columns(self, mock_provider, sample_dataframe):
        """Test profiling of numeric columns."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider, verbose=False)
        profile = pandora._profile_data(sample_dataframe)
        
        salary_info = profile["columns"]["salary"]
        assert "min" in salary_info
        assert "max" in salary_info
        assert salary_info["min"] == 50000
        assert salary_info["max"] == 60000
    
    def test_profile_string_columns(self, mock_provider, sample_dataframe):
        """Test profiling of string columns."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider, verbose=False)
        profile = pandora._profile_data(sample_dataframe)
        
        name_info = profile["columns"]["name"]
        assert "unique_count" in name_info
        assert name_info["unique_count"] == 3


class TestPandoraCodeExtraction:
    """Tests for code extraction from LLM responses."""
    
    def test_extract_code_plain(self, mock_provider):
        """Test extracting plain code."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider, verbose=False)
        
        text = "df['new_col'] = df['salary'] * 2"
        code = pandora._extract_code(text)
        
        assert code == text
    
    def test_extract_code_from_markdown(self, mock_provider):
        """Test extracting code from markdown blocks."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider, verbose=False)
        
        text = """Here's the code:
```python
df['new_col'] = df['salary'] * 2
```
That should work!"""
        
        code = pandora._extract_code(text)
        
        assert "df['new_col']" in code
        assert "```" not in code


class TestPandoraDo:
    """Tests for Pandora.do() method."""
    
    def test_do_simple_transformation(self, mock_provider, sample_dataframe):
        """Test simple DataFrame transformation."""
        from aiccel.pandora import Pandora
        
        # Mock LLM to return valid transformation code
        mock_provider.responses[""] = "df['salary_doubled'] = df['salary'] * 2"
        
        pandora = Pandora(llm=mock_provider, verbose=False, max_retries=1)
        
        result = pandora.do(sample_dataframe, "Double the salary column")
        
        assert isinstance(result, pd.DataFrame)
        assert "salary_doubled" in result.columns
    
    def test_do_preserves_original(self, mock_provider, sample_dataframe):
        """Test that original DataFrame is not modified."""
        from aiccel.pandora import Pandora
        
        original_columns = list(sample_dataframe.columns)
        
        mock_provider.responses[""] = "df['new_col'] = 1"
        
        pandora = Pandora(llm=mock_provider, verbose=False, max_retries=1)
        pandora.do(sample_dataframe, "Add a column")
        
        # Original should be unchanged
        assert list(sample_dataframe.columns) == original_columns
    
    def test_do_safe_mode_returns_original_on_failure(self, mock_provider, sample_dataframe):
        """Test safe_mode returns original on failure."""
        from aiccel.pandora import Pandora
        
        # Make LLM return invalid code
        mock_provider.responses[""] = "raise Exception('Fail')"
        
        pandora = Pandora(llm=mock_provider, verbose=False, max_retries=0)
        
        result = pandora.do(sample_dataframe, "Do something", safe_mode=True)
        
        # Should return original DataFrame
        assert result.shape == sample_dataframe.shape


class TestPandoraBuiltins:
    """Tests for safe builtins restriction."""
    
    def test_safe_builtins_allow_basic_ops(self, mock_provider, sample_dataframe):
        """Test that basic operations are allowed."""
        from aiccel.pandora import Pandora
        
        # Code using allowed builtins
        mock_provider.responses[""] = """
total = sum([1, 2, 3])
df['total'] = total
"""
        
        pandora = Pandora(llm=mock_provider, verbose=False, max_retries=1)
        result = pandora.do(sample_dataframe, "Add total")
        
        assert "total" in result.columns


class TestPandoraRetries:
    """Tests for retry mechanism."""
    
    def test_retries_on_error(self, mock_provider, sample_dataframe):
        """Test that Pandora retries on error."""
        from aiccel.pandora import Pandora
        
        call_count = [0]
        
        original_generate = mock_provider.generate
        def counting_generate(prompt, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return "invalid_syntax("  # Will cause SyntaxError
            return "df['new'] = 1"  # Valid code on retry
        
        mock_provider.generate = counting_generate
        
        pandora = Pandora(llm=mock_provider, verbose=False, max_retries=2)
        result = pandora.do(sample_dataframe, "Test retries")
        
        assert call_count[0] >= 2  # At least 2 attempts
        assert "new" in result.columns


class TestPandoraPromptBuilding:
    """Tests for prompt construction."""
    
    def test_initial_prompt_contains_profile(self, mock_provider, sample_dataframe):
        """Test that initial prompt contains data profile."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider, verbose=False)
        profile = pandora._profile_data(sample_dataframe)
        prompt = pandora._build_initial_prompt(profile, "Test instruction")
        
        assert "PANDORA" in prompt
        assert "Test instruction" in prompt
        assert "columns" in prompt.lower() or "profile" in prompt.lower()
    
    def test_repair_prompt_contains_error(self, mock_provider):
        """Test that repair prompt contains error info."""
        from aiccel.pandora import Pandora
        
        pandora = Pandora(llm=mock_provider, verbose=False)
        prompt = pandora._build_repair_prompt(
            instruction="Test",
            bad_code="x = y",
            error="NameError: y is not defined",
            output=""
        )
        
        assert "NameError" in prompt
        assert "x = y" in prompt
