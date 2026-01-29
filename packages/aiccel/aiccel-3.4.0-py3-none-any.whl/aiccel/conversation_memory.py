# aiccel/conversation_memory.py
"""
Conversation memory management with compression, summarization, and efficient storage.
"""

import zlib
import logging
import threading
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from .constants import Limits
from .exceptions import MemoryException, MemoryFullError, ValidationException

logger = logging.getLogger(__name__)


@dataclass
class MemoryTurn:
    """Represents a single turn in conversation memory"""
    query: str
    response: str
    tool_used: Optional[str] = None
    tool_output: Optional[str] = None
    timestamp: str = ""
    token_count: int = 0
    compressed: bool = False
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {k: v for k, v in asdict(self).items() if v is not None}


class MemoryCompressor:
    """Handles compression and decompression of memory data"""
    
    @staticmethod
    def compress(text: str, level: int = Limits.COMPRESSION_LEVEL) -> tuple[Optional[str], bool]:
        """
        Compress text with fallback to truncation.
        
        Returns:
            tuple: (compressed_data, is_compressed)
        """
        if not text:
            return None, False
        
        try:
            # Truncate before compression
            truncated = text[:Limits.MAX_COMPRESSED_LENGTH]
            compressed = zlib.compress(truncated.encode('utf-8'), level=level).hex()
            return compressed, True
        except Exception as e:
            logger.warning(f"Compression failed: {e}, using truncated text")
            return text[:Limits.MAX_UNCOMPRESSED_LENGTH], False
    
    @staticmethod
    def decompress(data: str, is_compressed: bool) -> str:
        """
        Decompress data with error handling.
        
        Returns:
            str: Decompressed text or error message
        """
        if not data:
            return ""
        
        if not is_compressed:
            return data
        
        try:
            return zlib.decompress(bytes.fromhex(data)).decode('utf-8')
        except Exception as e:
            logger.error(f"Decompression failed: {e}")
            return "[Error: Could not retrieve data]"


class ConversationMemory:
    """
    Enhanced conversation memory with compression, summarization, and token management.
    
    Features:
    - Automatic compression of old turns
    - Token-aware memory management
    - Summarization for long histories
    - Thread-safe operations
    """
    
    VALID_MEMORY_TYPES = {"buffer", "window", "summary"}
    
    def __init__(
        self,
        memory_type: str = "buffer",
        max_turns: int = Limits.MAX_MEMORY_TURNS,
        max_tokens: int = Limits.MAX_MEMORY_TOKENS,
        llm_provider = None
    ):
        """
        Initialize conversation memory.
        
        Args:
            memory_type: Type of memory ('buffer', 'window', 'summary')
            max_turns: Maximum number of turns to keep
            max_tokens: Maximum total tokens to keep
            llm_provider: LLM provider for summarization (required for 'summary' type)
        
        Raises:
            ValidationException: If configuration is invalid
        """
        self._validate_config(memory_type, llm_provider)
        
        self.memory_type = memory_type
        self.max_turns = max_turns
        self.max_tokens = max_tokens
        self.llm_provider = llm_provider
        self._history: List[Dict[str, Any]] = []
        self._history_lock = threading.RLock()
        self.compressor = MemoryCompressor()
        
        logger.debug(f"Initialized ConversationMemory: type={memory_type}, max_turns={max_turns}, max_tokens={max_tokens}")
    
    def _validate_config(self, memory_type: str, llm_provider) -> None:
        """Validate memory configuration"""
        if memory_type not in self.VALID_MEMORY_TYPES:
            raise ValidationException(
                "memory_type",
                f"Invalid memory type. Must be one of: {self.VALID_MEMORY_TYPES}",
                expected=self.VALID_MEMORY_TYPES,
                actual=memory_type
            )
        
        if memory_type == "summary" and not llm_provider:
            raise ValidationException(
                "llm_provider",
                "Summary memory type requires an llm_provider",
                expected="LLMProvider instance",
                actual=None
            )

    @property
    def history(self) -> List[Dict[str, Any]]:
        """Thread-safe access to history (returns copy)."""
        with self._history_lock:
            return list(self._history)
    
    def _calculate_token_count(self, text: str, chars_per_token: float = 4.0) -> int:
        """
        Estimate token count.
        
        Args:
            text: Text to estimate
            chars_per_token: Average characters per token (default: 4.0)
        
        Returns:
            Estimated token count
        """
        if not text:
            return 0
        return max(1, int(len(text) / chars_per_token))
    
    def add_turn(
        self,
        query: str,
        response: str,
        tool_used: Optional[str] = None,
        tool_output: Optional[str] = None
    ) -> None:
        """
        Add a conversation turn to memory.
        
        Args:
            query: User query
            response: Agent response
            tool_used: Name of tool used (if any)
            tool_output: Tool output (if any)
        
        Raises:
            MemoryException: If memory operation fails
        """
        try:
            # Sanitize inputs
            query = str(query) if query else ""
            response = str(response) if response else ""
            tool_output = str(tool_output) if tool_output else None
            
            # Compress data
            query_compressed, query_is_compressed = self.compressor.compress(query)
            response_compressed, response_is_compressed = self.compressor.compress(response)
            tool_output_compressed, tool_output_is_compressed = (
                self.compressor.compress(tool_output) if tool_output else (None, False)
            )
            
            # Calculate token counts from ORIGINAL data
            query_tokens = self._calculate_token_count(query)
            response_tokens = self._calculate_token_count(response)
            tool_tokens = self._calculate_token_count(tool_output) if tool_output else 0
            total_tokens = query_tokens + response_tokens + tool_tokens
            
            # Create turn
            turn = {
                "query": query_compressed,
                "response": response_compressed,
                "tool_used": tool_used,
                "tool_output": tool_output_compressed,
                "timestamp": datetime.now().isoformat(),
                "query_compressed": query_is_compressed,
                "response_compressed": response_is_compressed,
                "tool_output_compressed": tool_output_is_compressed,
                "token_count": total_tokens
            }
            
            # Add turn thread-safely
            with self._history_lock:
                self._history.append(turn)
            self._manage_memory()
            
            logger.debug(f"Added turn to memory: {total_tokens} tokens")
            
        except Exception as e:
            logger.error(f"Failed to add turn to memory: {e}")
            raise MemoryException(f"Failed to add turn: {e}")
    
    def _manage_memory(self) -> None:
        """Manage memory size and apply retention policies (thread-safe)"""
        try:
            with self._history_lock:
                # Calculate current total tokens
                current_tokens = sum(turn.get("token_count", 0) for turn in self._history)
                
                # Remove oldest turns until within limits
                while (len(self._history) > self.max_turns or current_tokens > self.max_tokens) and self._history:
                    removed = self._history.pop(0)
                    current_tokens -= removed.get("token_count", 0)
                    logger.debug(f"Removed old turn: {removed.get('token_count', 0)} tokens")
                
                # Trigger summarization if configured
                if self.memory_type == "summary" and len(self._history) > self.max_turns // 2:
                    self._summarize_history()
            
        except Exception as e:
            logger.error(f"Memory management error: {e}")
            raise MemoryException(f"Memory management failed: {e}")
    
    def _summarize_history(self) -> None:
        """Summarize conversation history to save space"""
        if len(self.history) <= 1 or not self.llm_provider:
            return
        
        try:
            # Get turns to summarize (leave most recent)
            to_summarize = self.history[:-1]
            summary_parts = ["Summarize the following conversation history (max 200 words):\n\n"]
            
            for turn in to_summarize:
                try:
                    query = self.compressor.decompress(
                        turn["query"],
                        turn.get("query_compressed", True)
                    )
                    response = self.compressor.decompress(
                        turn["response"],
                        turn.get("response_compressed", True)
                    )
                    
                    summary_parts.append(f"User: {query}\nAssistant: {response}\n")
                    
                    if turn.get("tool_output"):
                        tool_output = self.compressor.decompress(
                            turn["tool_output"],
                            turn.get("tool_output_compressed", True)
                        )
                        summary_parts.append(f"Tool Output: {tool_output}\n")
                
                except Exception as e:
                    logger.warning(f"Failed to decompress turn for summary: {e}")
                    continue
            
            summary_prompt = "".join(summary_parts)
            summary = self.llm_provider.generate(summary_prompt)
            
            # Store summary as new first entry
            summary_compressed, summary_is_compressed = self.compressor.compress(summary)
            summary_tokens = self._calculate_token_count(summary)
            
            summary_turn = {
                "query": self.compressor.compress("Conversation summary")[0],
                "response": summary_compressed,
                "tool_used": None,
                "tool_output": None,
                "timestamp": datetime.now().isoformat(),
                "query_compressed": True,
                "response_compressed": summary_is_compressed,
                "tool_output_compressed": False,
                "token_count": summary_tokens + self._calculate_token_count("Conversation summary")
            }
            
            # Replace old turns with summary + keep most recent
            self.history = [summary_turn] + self.history[-1:]
            logger.info("Summarized conversation history")
            
        except Exception as e:
            logger.error(f"History summarization failed: {e}")
            raise MemoryException(f"Summarization failed: {e}")
    
    def get_context(self, max_context_turns: Optional[int] = None) -> str:
        """
        Get conversation context as formatted string.
        
        Args:
            max_context_turns: Maximum turns to include (None for all)
        
        Returns:
            str: Formatted conversation context
        """
        if not self.history:
            return ""
        
        try:
            context_parts = ["Conversation History:\n"]
            turns = self.history[-max_context_turns:] if max_context_turns else self.history
            
            for turn in turns:
                try:
                    query = self.compressor.decompress(
                        turn["query"],
                        turn.get("query_compressed", True)
                    )
                    response = self.compressor.decompress(
                        turn["response"],
                        turn.get("response_compressed", True)
                    )
                    
                    context_parts.append(f"User: {query}\nAssistant: {response}\n")
                    
                    if turn.get("tool_used") and turn.get("tool_output"):
                        tool_output = self.compressor.decompress(
                            turn["tool_output"],
                            turn.get("tool_output_compressed", True)
                        )
                        context_parts.append(f"Tool Used: {turn['tool_used']}\nTool Output: {tool_output}\n")
                    
                    context_parts.append("\n")
                
                except Exception as e:
                    logger.warning(f"Failed to decompress turn in get_context: {e}")
                    continue
            
            context = "".join(context_parts).strip()
            
            # Safety truncation
            if len(context) > Limits.MAX_PROMPT_LENGTH:
                context = context[-Limits.MAX_PROMPT_LENGTH:]
                logger.warning(f"Context truncated to {Limits.MAX_PROMPT_LENGTH} chars")
            
            return context
        
        except Exception as e:
            logger.error(f"Error getting context: {e}")
            return ""
    
    def get_formatted_history(self) -> str:
        """Alias for get_context for backward compatibility."""
        return self.get_context()

    def clear(self) -> None:
        """Clear all conversation history (thread-safe)."""
        with self._history_lock:
            self._history = []
        logger.info("Conversation memory cleared")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get decompressed conversation history.
        
        Returns:
            List[Dict]: List of conversation turns
        """
        decompressed_history = []
        
        for turn in self.history:
            try:
                decompressed_turn = {
                    "query": self.compressor.decompress(
                        turn["query"],
                        turn.get("query_compressed", True)
                    ),
                    "response": self.compressor.decompress(
                        turn["response"],
                        turn.get("response_compressed", True)
                    ),
                    "tool_used": turn.get("tool_used"),
                    "tool_output": self.compressor.decompress(
                        turn["tool_output"],
                        turn.get("tool_output_compressed", True)
                    ) if turn.get("tool_output") else None,
                    "timestamp": turn.get("timestamp", "Unknown"),
                    "token_count": turn.get("token_count", 0)
                }
                decompressed_history.append(decompressed_turn)
            
            except Exception as e:
                logger.warning(f"Failed to decompress history turn: {e}")
                decompressed_history.append({
                    "query": "[Error: Could not retrieve]",
                    "response": "[Error: Could not retrieve]",
                    "tool_used": turn.get("tool_used"),
                    "tool_output": None,
                    "timestamp": turn.get("timestamp", "Unknown"),
                    "token_count": 0
                })
        
        return decompressed_history
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_turns": len(self.history),
            "total_tokens": sum(turn.get("token_count", 0) for turn in self.history),
            "max_turns": self.max_turns,
            "max_tokens": self.max_tokens,
            "memory_type": self.memory_type,
            "compression_enabled": any(
                turn.get("query_compressed", False) or turn.get("response_compressed", False)
                for turn in self.history
            )
        }