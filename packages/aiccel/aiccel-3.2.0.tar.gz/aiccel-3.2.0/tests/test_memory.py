"""
Tests for ConversationMemory module.

Coverage targets:
- Memory initialization
- Adding messages
- Memory retrieval
- Memory clearing
- Token limiting
"""
import pytest


class TestConversationMemoryInit:
    """Tests for ConversationMemory initialization."""
    
    def test_default_initialization(self):
        """Test default memory creation."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory()
        
        assert memory.memory_type == "buffer"
        assert memory.max_turns == 20
        assert len(memory.get_history()) == 0
    
    def test_custom_initialization(self):
        """Test custom memory configuration."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory(
            memory_type="window",
            max_turns=5,
            max_tokens=1000
        )
        
        assert memory.memory_type == "window"
        assert memory.max_turns == 5


class TestAddingMessages:
    """Tests for adding messages to memory."""
    
    def test_add_user_message(self):
        """Test adding a user message."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory()
        memory.add_user_message("Hello, AI!")
        
        history = memory.get_history()
        assert len(history) == 1
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hello, AI!"
    
    def test_add_assistant_message(self):
        """Test adding an assistant message."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory()
        memory.add_assistant_message("Hello, human!")
        
        history = memory.get_history()
        assert len(history) == 1
        assert history[0]["role"] == "assistant"
    
    def test_add_multiple_messages(self):
        """Test adding multiple messages."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory()
        memory.add_user_message("Hi")
        memory.add_assistant_message("Hello!")
        memory.add_user_message("How are you?")
        memory.add_assistant_message("I'm great!")
        
        history = memory.get_history()
        assert len(history) == 4


class TestMemoryClear:
    """Tests for clearing memory."""
    
    def test_clear_memory(self):
        """Test clearing all messages."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory()
        memory.add_user_message("Test 1")
        memory.add_user_message("Test 2")
        memory.add_user_message("Test 3")
        
        assert len(memory.get_history()) == 3
        
        memory.clear()
        
        assert len(memory.get_history()) == 0


class TestMaxTurns:
    """Tests for max turns limiting."""
    
    def test_max_turns_limit(self):
        """Test that memory respects max turns."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory(max_turns=3)
        
        for i in range(10):
            memory.add_user_message(f"Message {i}")
        
        # Should only keep the most recent messages
        history = memory.get_history()
        assert len(history) <= 6  # 3 turns = up to 6 messages (user + assistant each)


class TestFormattedHistory:
    """Tests for formatted history output."""
    
    def test_get_formatted_history(self):
        """Test getting formatted history string."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory()
        memory.add_user_message("Hello")
        memory.add_assistant_message("Hi there!")
        
        formatted = memory.get_formatted_history()
        
        assert isinstance(formatted, str)
        assert "Hello" in formatted
        assert "Hi there!" in formatted
    
    def test_formatted_empty_history(self):
        """Test formatted history when empty."""
        from aiccel.conversation_memory import ConversationMemory
        
        memory = ConversationMemory()
        formatted = memory.get_formatted_history()
        
        assert formatted == "" or formatted is None or "no" in formatted.lower()
