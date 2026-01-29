# aiccel/logger.py
"""
Agent Logger - Clean Minimal Implementation
============================================

LangChain-inspired logging with:
- No emojis
- No duplicates
- Clean, parsable output
- Optimized performance
"""

import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

from .logging_config import get_logger, configure_logging, AgentLogger


class ColorFormatter(logging.Formatter):
    """Clean formatter with optional colors."""
    
    COLORS = {
        'DEBUG': '\033[90m',
        'INFO': '\033[0m',
        'WARNING': '\033[33m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[1;31m',
        'RESET': '\033[0m'
    }
    
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None, style: str = '%'):
        super().__init__(fmt, datefmt, style)
        self.is_tty = sys.stdout.isatty()
    
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if self.is_tty:
            color = self.COLORS.get(record.levelname, '')
            return f"{color}{msg}{self.COLORS['RESET']}"
        return msg


class JSONFormatter(logging.Formatter):
    """Structured JSON logging for production."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            'ts': datetime.fromtimestamp(record.created).isoformat(),
            'lvl': record.levelname,
            'mod': record.name,
            'msg': record.getMessage()
        }
        
        if record.exc_info:
            log_entry['error'] = {
                'type': record.exc_info[0].__name__ if record.exc_info[0] else "Unknown",
                'message': str(record.exc_info[1]) if record.exc_info[1] else "",
                'trace': self.formatException(record.exc_info)
            }
        
        if hasattr(record, 'extra_data') and record.extra_data:
            log_entry['data'] = record.extra_data
        
        return json.dumps(log_entry, default=str, separators=(',', ':'))


class TraceLogger(AgentLogger):
    """
    Extended logger with enhanced trace visualization.
    
    Backward compatible with existing AILogger usage.
    """
    
    def __init__(
        self,
        name: str,
        level: Union[int, str] = logging.INFO,
        verbose: bool = False,
        log_file: Optional[str] = None,
        structured_logging: bool = False,
        use_colors: bool = True
    ):
        super().__init__(name, verbose)
        
        # Configure underlying logger if log_file specified
        if log_file:
            self._setup_file_handler(log_file, structured_logging)
    
    def _setup_file_handler(self, log_file: str, structured: bool):
        """Add file handler to the logger."""
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            handler = logging.FileHandler(log_path, encoding='utf-8')
            if structured:
                handler.setFormatter(JSONFormatter())
            else:
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                ))
            self._logger.addHandler(handler)
        except IOError as e:
            self.error(f"Failed to setup file logger: {e}")
    
    def visualize_trace(self, trace_id: int) -> str:
        """Generate clean trace visualization."""
        trace = self.get_trace(trace_id)
        if not trace:
            return f"Invalid trace ID: {trace_id}"
        
        lines = [
            f"Trace #{trace_id}: {trace.get('action', 'N/A')}",
            f"Duration: {trace.get('duration_ms', 0):.0f}ms",
            f"Steps: {len(trace.get('steps', []))}",
            f"Errors: {len(trace.get('errors', []))}"
        ]
        
        if trace.get('inputs'):
            lines.append(f"Input: {self._format_data(trace['inputs'])}")
        
        if trace.get('steps'):
            lines.append("\nSteps:")
            for i, step in enumerate(trace['steps'], 1):
                lines.append(f"  {i}. {step.get('name', 'N/A')}")
                if step.get('details'):
                    lines.append(f"     {self._format_data(step['details'])}")
        
        if trace.get('errors'):
            lines.append("\nErrors:")
            for err in trace['errors']:
                lines.append(f"  - {err.get('context', 'N/A')}: {err.get('message', 'N/A')}")
        
        if trace.get('outputs'):
            lines.append(f"\nOutput: {self._format_data(trace['outputs'])}")
        
        return "\n".join(lines)
    
    def _format_data(self, data: Dict[str, Any], max_len: int = 100) -> str:
        """Format data dict to compact string."""
        if not data:
            return "{}"
        try:
            s = json.dumps(data, default=str, separators=(',', ':'))
            if len(s) > max_len:
                return s[:max_len] + "..."
            return s
        except Exception:
            return str(data)[:max_len]
    
    # Backward compatibility methods
    def log(self, message: str, exc_info=None, extra_data: Optional[Dict[str, Any]] = None):
        """Compatibility: alias for info()."""
        self.info(message)
    
    def _archive_oldest_trace(self):
        """Archive oldest trace when max is reached."""
        max_traces = 100
        if len(self.traces) > max_traces:
            oldest_id = min(self.traces.keys())
            del self.traces[oldest_id]


# Factory function for creating loggers
def create_logger(
    name: str,
    verbose: bool = False,
    log_file: Optional[str] = None,
    structured: bool = False
) -> TraceLogger:
    """
    Create a configured trace logger.
    
    Args:
        name: Logger name
        verbose: Enable verbose output
        log_file: Optional file path for logging
        structured: Use JSON structured logging
        
    Returns:
        Configured TraceLogger instance
    """
    return TraceLogger(
        name=name,
        verbose=verbose,
        log_file=log_file,
        structured_logging=structured
    )


# Backward compatibility alias - AILogger is now TraceLogger
AILogger = TraceLogger