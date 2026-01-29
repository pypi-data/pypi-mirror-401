"""
Tests for CLI module.

Coverage targets:
- Version command
- Run command
- Chat command  
- Tools command
- Encrypt/Decrypt commands
"""
import pytest
from unittest.mock import MagicMock, patch
import sys


class TestCLIVersion:
    """Tests for version command."""
    
    def test_get_version(self):
        """Test getting version."""
        from aiccel.cli import get_version
        
        version = get_version()
        
        assert isinstance(version, str)
        assert version != "unknown"
    
    def test_cmd_version(self, capsys):
        """Test version command output."""
        from aiccel.cli import cmd_version
        
        args = MagicMock()
        cmd_version(args)
        
        captured = capsys.readouterr()
        assert "aiccel" in captured.out.lower()


class TestCLITools:
    """Tests for tools command."""
    
    def test_tools_list(self, capsys):
        """Test tools list command."""
        from aiccel.cli import cmd_tools
        
        args = MagicMock()
        args.action = "list"
        
        cmd_tools(args)
        
        captured = capsys.readouterr()
        assert "SearchTool" in captured.out
        assert "WeatherTool" in captured.out


class TestCLIMain:
    """Tests for main entry point."""
    
    def test_main_no_args(self):
        """Test main with no arguments shows help."""
        from aiccel.cli import main
        
        with patch('sys.argv', ['aiccel']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 0
    
    def test_main_version(self, capsys):
        """Test main with version command."""
        from aiccel.cli import main
        
        with patch('sys.argv', ['aiccel', 'version']):
            main()
        
        captured = capsys.readouterr()
        assert "aiccel" in captured.out.lower()


class TestCLIArgumentParsing:
    """Tests for argument parsing."""
    
    def test_run_args(self):
        """Test run command argument parsing."""
        import argparse
        from aiccel.cli import main
        
        # This tests that the parser is correctly configured
        with patch('sys.argv', ['aiccel', 'run', 'test query', '-p', 'gemini', '-v']):
            with patch('aiccel.cli.cmd_run') as mock_run:
                main()
                
                # Check that cmd_run was called with correct args
                args = mock_run.call_args[0][0]
                assert args.query == 'test query'
                assert args.provider == 'gemini'
                assert args.verbose is True
    
    def test_chat_args(self):
        """Test chat command argument parsing."""
        from aiccel.cli import main
        
        with patch('sys.argv', ['aiccel', 'chat', '-p', 'openai']):
            with patch('aiccel.cli.cmd_chat') as mock_chat:
                main()
                
                args = mock_chat.call_args[0][0]
                assert args.provider == 'openai'
    
    def test_tools_args(self):
        """Test tools command argument parsing."""
        from aiccel.cli import main
        
        with patch('sys.argv', ['aiccel', 'tools', 'list']):
            with patch('aiccel.cli.cmd_tools') as mock_tools:
                main()
                
                args = mock_tools.call_args[0][0]
                assert args.action == 'list'


class TestCLIRunCommand:
    """Tests for run command."""
    
    def test_run_without_api_key(self, capsys, monkeypatch):
        """Test run fails without API key."""
        from aiccel.cli import cmd_run
        
        # Clear any API keys
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        args = MagicMock()
        args.query = "test"
        args.provider = "gemini"
        args.model = None
        args.verbose = False
        
        with pytest.raises(SystemExit):
            cmd_run(args)
        
        captured = capsys.readouterr()
        assert "API key" in captured.out or "Error" in captured.out


class TestCLIMaskCommand:
    """Tests for mask command."""
    
    def test_mask_command(self, capsys):
        """Test mask command."""
        from aiccel.cli import cmd_mask
        
        args = MagicMock()
        args.text = "Contact user@example.com"
        args.show_mapping = False
        
        cmd_mask(args)
        
        captured = capsys.readouterr()
        assert "Masked text" in captured.out
    
    def test_mask_with_mapping(self, capsys):
        """Test mask command with mapping output."""
        from aiccel.cli import cmd_mask
        
        args = MagicMock()
        args.text = "Email: test@test.com"
        args.show_mapping = True
        
        cmd_mask(args)
        
        captured = capsys.readouterr()
        assert "Mapping" in captured.out
