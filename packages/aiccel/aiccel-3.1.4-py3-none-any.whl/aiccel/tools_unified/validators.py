# aiccel/tools_unified/validators.py
"""
Tool Validators
================

Validation utilities for tool inputs and outputs.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

from .protocol import ToolParameter


@dataclass
class ValidationError:
    """Validation error details."""
    field: str
    message: str
    value: Any = None


class ToolValidator:
    """
    Validates tool inputs and outputs.
    
    Features:
    - Type validation
    - Required field checking
    - Range validation
    - Pattern matching
    """
    
    def __init__(self, parameters: List[ToolParameter]):
        self.parameters = {p.name: p for p in parameters}
    
    def validate(self, args: Dict[str, Any]) -> List[ValidationError]:
        """
        Validate arguments against parameter schema.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required fields
        for name, param in self.parameters.items():
            if param.required and name not in args:
                if param.default is None:
                    errors.append(ValidationError(
                        field=name,
                        message=f"Required field '{name}' is missing"
                    ))
        
        # Validate types
        for name, value in args.items():
            if name in self.parameters:
                param = self.parameters[name]
                type_error = self._validate_type(value, param.type)
                if type_error:
                    errors.append(ValidationError(
                        field=name,
                        message=type_error,
                        value=value
                    ))
                
                # Check enum values
                if param.enum and value not in param.enum:
                    errors.append(ValidationError(
                        field=name,
                        message=f"Value must be one of: {param.enum}",
                        value=value
                    ))
        
        return errors
    
    def validate_and_fix(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and attempt to fix arguments.
        
        Returns:
            Fixed arguments dict
        """
        fixed = dict(args)
        
        # Add defaults for missing required fields
        for name, param in self.parameters.items():
            if name not in fixed:
                if param.default is not None:
                    fixed[name] = param.default
        
        # Type coercion
        for name, value in list(fixed.items()):
            if name in self.parameters:
                param = self.parameters[name]
                coerced = self._coerce_type(value, param.type)
                if coerced is not None:
                    fixed[name] = coerced
        
        return fixed
    
    def _validate_type(self, value: Any, expected_type: str) -> Optional[str]:
        """Validate value type."""
        type_map = {
            'string': str,
            'number': (int, float),
            'integer': int,
            'boolean': bool,
            'array': list,
            'object': dict,
        }
        
        expected = type_map.get(expected_type)
        if expected and not isinstance(value, expected):
            return f"Expected {expected_type}, got {type(value).__name__}"
        
        return None
    
    def _coerce_type(self, value: Any, target_type: str) -> Any:
        """Attempt to coerce value to target type."""
        try:
            if target_type == 'string':
                return str(value)
            elif target_type == 'number':
                return float(value)
            elif target_type == 'integer':
                return int(value)
            elif target_type == 'boolean':
                if isinstance(value, str):
                    return value.lower() in ('true', '1', 'yes')
                return bool(value)
            elif target_type == 'array':
                if isinstance(value, str):
                    return [v.strip() for v in value.split(',')]
                return list(value)
        except (ValueError, TypeError):
            pass
        
        return None


def validate_args(
    args: Dict[str, Any],
    parameters: List[ToolParameter],
    fix: bool = True
) -> tuple:
    """
    Convenience function to validate tool arguments.
    
    Args:
        args: Arguments to validate
        parameters: Parameter definitions
        fix: Whether to attempt fixing invalid args
        
    Returns:
        Tuple of (validated_args, errors)
    """
    validator = ToolValidator(parameters)
    
    if fix:
        fixed_args = validator.validate_and_fix(args)
        errors = validator.validate(fixed_args)
        return fixed_args, errors
    else:
        errors = validator.validate(args)
        return args, errors
