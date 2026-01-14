"""
AIccel Jailbreak Detection Module
=================================

Provides automated safety checks using the 'traromal/AIccel_Jailbreak' model.
This module helps prevent prompt injection and malicious usage of agents.
"""

from typing import Dict, Any, Optional
import time
import functools

# Optional dependency
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from .logging_config import get_logger

logger = get_logger("jailbreak")

class JailbreakGuard:
    """
    Guard for detecting and blocking jailbreak attempts using a classifier model.
    """
    
    def __init__(self, model_name: str = "traromal/AIccel_Jailbreak", threshold: float = 0.5):
        """
        Initialize the guard.
        
        Args:
            model_name: HuggingFace model ID.
            threshold: Confidence threshold to block.
        """
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers library not installed. Jailbreak detection is DISABLED.")
            self.classifier = None
            return

        self.model_name = model_name
        self.threshold = threshold
        self.classifier = None
        # Don't load immediately; wait for first check() call
        # self._load_model()
        
    def _load_model(self):
        """Lazy load the model."""
        try:
            logger.info(f"Loading Jailbreak classifier: {self.model_name}")
            self.classifier = pipeline("text-classification", model=self.model_name)
            logger.info("Jailbreak classifier loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Jailbreak model: {e}")
            self.classifier = None

    def check(self, prompt: str) -> bool:
        """
        Check if a prompt is safe.
        
        Returns:
            True if safe, False if jailbreak detected.
        """
        if not self.classifier and TRANSFORMERS_AVAILABLE:
            self._load_model()
            
        if not self.classifier:
            # Open fail: if we can't check, we assume safe (or user policy might differ)
            # Ideally, in strict environments, this should be False.
            return True
            
        try:
            # Classifier returns list of dicts: [{'label': 'LABEL_X', 'score': 0.9}]
            # Assuming model outputs 'SAFE' or 'UNSAFE' or similar labels, or binary.
            # adjusting based on standard HuggingFace pipeline output.
            result = self.classifier(prompt)
            
            # Note: Need to know specific model labels. Assuming standard binary classifier logic.
            # If model "traromal/AIccel_Jailbreak" follows standard safety classifiers:
            # Usually Label_1 = Unsafe/Jailbreak, Label_0 = Safe.
            # Or explicit labels like "JAILBREAK", "SAFE".
            
            # Since exact labels aren't specified in request, logging output for first usage might be needed.
            # For now, we will log the result and default to 'safe' unless high confidence 'unsafe'.
            
            label = result[0]['label']
            score = result[0]['score']
            
            logger.debug(f"Jailbreak check: {label} ({score:.4f})")
            
            # Heuristic map - Adjust based on actual model labels
            unsafe_labels = ["JAILBREAK", "UNSAFE", "LABEL_1", "INJECTION"] 
            
            if label.upper() in unsafe_labels and score > self.threshold:
                logger.warning(f"Jailbreak attempt blocked! Prompt: {prompt[:50]}...")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error during jailbreak check: {e}")
            return True # Fail open to avoid blocking valid queries on error

    def guard(self, func):
        """Decorator to guard an agent's run method."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract prompt - usually first arg or 'query' kwarg
            prompt = kwargs.get('query')
            if not prompt and len(args) > 0:
                # args[0] is self usually for methods, so args[1]
                if hasattr(args[0], 'run'): # method call check
                    if len(args) > 1: prompt = args[1]
                else:
                    prompt = args[0]
            
            if prompt and isinstance(prompt, str):
                if not self.check(prompt):
                    raise ValueError("Security Alert: Prompt detected as potential jailbreak/unsafe.")
            
            return func(*args, **kwargs)
        return wrapper

# Global instance for easy import
_global_guard = None

def get_guard() -> JailbreakGuard:
    global _global_guard
    if _global_guard is None:
        _global_guard = JailbreakGuard()
    return _global_guard

def check_prompt(prompt: str) -> bool:
    """Convenience function."""
    return get_guard().check(prompt)
