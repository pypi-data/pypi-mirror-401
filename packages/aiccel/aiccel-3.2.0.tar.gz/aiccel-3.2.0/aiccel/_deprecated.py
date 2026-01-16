# aiccel/_deprecated.py
"""
Deprecation Utilities
======================

Provides warnings and compatibility shims for deprecated features.
"""

import warnings
import functools
from typing import Callable, TypeVar, Type

T = TypeVar('T')


def deprecated(
    reason: str,
    version: str = "2.3.0",
    alternative: str = None,
    remove_in: str = None
):
    """
    Decorator to mark functions/classes as deprecated.
    
    Args:
        reason: Why this is deprecated
        version: Version when deprecated
        alternative: What to use instead
        remove_in: Version when it will be removed
    
    Usage:
        @deprecated("Use new_function instead", alternative="new_function")
        def old_function():
            pass
    """
    def decorator(func_or_class: T) -> T:
        msg = f"{func_or_class.__name__} is deprecated since v{version}. {reason}"
        
        if alternative:
            msg += f" Use {alternative} instead."
        
        if remove_in:
            msg += f" Will be removed in v{remove_in}."
        
        if isinstance(func_or_class, type):
            # It's a class
            original_init = func_or_class.__init__
            
            @functools.wraps(original_init)
            def new_init(self, *args, **kwargs):
                warnings.warn(msg, DeprecationWarning, stacklevel=2)
                original_init(self, *args, **kwargs)
            
            func_or_class.__init__ = new_init
            return func_or_class
        else:
            # It's a function
            @functools.wraps(func_or_class)
            def wrapper(*args, **kwargs):
                warnings.warn(msg, DeprecationWarning, stacklevel=2)
                return func_or_class(*args, **kwargs)
            return wrapper
    
    return decorator


def deprecated_module(
    module_name: str,
    alternative: str,
    version: str = "2.3.0"
):
    """
    Emit deprecation warning for entire module.
    
    Call at module level:
        deprecated_module(__name__, "aiccel.new_module")
    """
    warnings.warn(
        f"Module '{module_name}' is deprecated since v{version}. "
        f"Use '{alternative}' instead.",
        DeprecationWarning,
        stacklevel=3
    )


def deprecated_alias(
    old_name: str,
    new_obj: T,
    version: str = "2.3.0"
) -> T:
    """
    Create a deprecated alias for an object.
    
    Usage:
        OldName = deprecated_alias("OldName", NewName)
    """
    class DeprecatedAlias:
        def __new__(cls, *args, **kwargs):
            warnings.warn(
                f"'{old_name}' is deprecated since v{version}. "
                f"Use '{new_obj.__name__}' instead.",
                DeprecationWarning,
                stacklevel=2
            )
            return new_obj(*args, **kwargs)
        
        # Forward class attributes
        def __getattr__(self, name):
            return getattr(new_obj, name)
    
    # Copy metadata
    DeprecatedAlias.__name__ = old_name
    DeprecatedAlias.__doc__ = f"Deprecated alias for {new_obj.__name__}"
    
    return DeprecatedAlias


# Track deprecation warnings
_DEPRECATION_WARNINGS_SHOWN = set()


def warn_once(message: str, category=DeprecationWarning):
    """Show a deprecation warning only once."""
    if message not in _DEPRECATION_WARNINGS_SHOWN:
        _DEPRECATION_WARNINGS_SHOWN.add(message)
        warnings.warn(message, category, stacklevel=3)
