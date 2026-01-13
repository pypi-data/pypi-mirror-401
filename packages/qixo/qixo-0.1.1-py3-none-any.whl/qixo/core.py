"""
qixo - A lightweight Python library for executing JavaScript in a QuickJS sandbox
"""

import json
from typing import Any, Optional
import quickjs


class QixoError(Exception):
    """Base exception for qixo errors"""
    
    def __init__(self, message: str, stack: Optional[str] = None):
        super().__init__(message)
        self.stack = stack


class Qixo:
    """
    A sandboxed JavaScript execution environment using QuickJS.
    
    Args:
        memory_limit_mb: Maximum memory in megabytes (default: 10MB)
        timeout_ms: Maximum execution time in milliseconds (default: 5000ms)
    
    Examples:
        >>> with Qixo() as box:
        ...     result = box.eval("1 + 1")
        ...     print(result)
        2
        
        >>> with Qixo(memory_limit_mb=5, timeout_ms=1000) as box:
        ...     result = box.eval("({name: 'qixo', version: 1})")
        ...     print(result)
        {'name': 'qixo', 'version': 1}
    """
    
    def __init__(
        self,
        memory_limit_mb: int = 10,
        timeout_ms: int = 5000,
    ):
        self.memory_limit_mb = memory_limit_mb
        self.timeout_ms = timeout_ms
        self._context: Optional[quickjs.Context] = None
    
    def __enter__(self) -> "Qixo":
        """Initialize the QuickJS context"""
        # Convert MB to bytes for QuickJS
        memory_limit_bytes = self.memory_limit_mb * 1024 * 1024
        
        # Create context with limits
        self._context = quickjs.Context()
        
        # Set memory limit
        self._context.set_memory_limit(memory_limit_bytes)
        
        # Set time limit (convert ms to seconds)
        self._context.set_time_limit(self.timeout_ms / 1000.0)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the QuickJS context"""
        if self._context:
            self._context = None
        return False
    
    def eval(self, code: str) -> Any:
        """
        Evaluate JavaScript code and return the result.
        
        Args:
            code: JavaScript code to execute
            
        Returns:
            The result of the evaluation, converted to Python types:
            - JavaScript objects become Python dicts
            - JavaScript arrays become Python lists
            - JavaScript primitives (string, number, boolean, null) map directly
            
        Raises:
            QixoError: If the code fails to execute or exceeds limits
            
        Examples:
            >>> box.eval("1 + 1")
            2
            >>> box.eval("'hello' + ' ' + 'world'")
            'hello world'
            >>> box.eval("[1, 2, 3].map(x => x * 2)")
            [2, 4, 6]
            >>> box.eval("({name: 'test', value: 42})")
            {'name': 'test', 'value': 42}
        """
        if not self._context:
            raise QixoError("Qixo context not initialized. Use 'with Qixo() as box:'")
        
        try:
            # Check if this is a function/variable declaration (statement)
            # These don't return values, they define things in the global scope
            is_statement = (
                code.strip().startswith('function ') or
                code.strip().startswith('var ') or
                code.strip().startswith('let ') or
                code.strip().startswith('const ')
            )
            
            if is_statement:
                # Execute as statement (no return value expected)
                result = self._context.eval(code)
                return None
            else:
                # Try to wrap as expression first
                wrapped_code = f"(function() {{ return ({code}); }})()"
                try:
                    result = self._context.eval(wrapped_code)
                except Exception:
                    # If wrapped version fails, try unwrapped
                    result = self._context.eval(code)
            
            # Convert JavaScript result to Python
            return self._js_to_python(result)
            
        except quickjs.JSException as e:
            # Extract error message and stack trace
            error_msg = str(e)
            stack = getattr(e, 'stack', None)
            raise QixoError(error_msg, stack=stack)
        except Exception as e:
            raise QixoError(f"Execution error: {str(e)}")
    
    def _js_to_python(self, value: Any) -> Any:
        """
        Convert JavaScript values to Python types.
        
        For complex objects/arrays, we use the quickjs library's json method
        to ensure proper conversion.
        """
        # Handle None/null
        if value is None:
            return None
        
        # Handle primitives directly
        if isinstance(value, (bool, int, float, str)):
            return value
        
        # For QuickJS objects, convert to JSON
        # The quickjs library provides a .json() method on objects
        if hasattr(value, 'json'):
            try:
                json_str = value.json()
                return json.loads(json_str)
            except Exception:
                pass
        
        # Fallback attempts
        if isinstance(value, (list, tuple)):
            return [self._js_to_python(item) for item in value]
        elif isinstance(value, dict):
            return {key: self._js_to_python(val) for key, val in value.items()}
        else:
            # Last resort: convert to string
            return str(value)
