"""
Main tracker module for QL Tracker.

This module provides the `@track` decorator that logs function calls using event queue.
"""

import asyncio
import functools
import time
from typing import Any, Callable, Dict, Optional, TypeVar

from .config import get_config
from .services.queue.event_queue import create_event
from .initialize import get_initializer

# Type variables for generic function types
F = TypeVar('F', bound=Callable[..., Any])





def _ensure_services_initialized() -> None:
    """Ensure background services are initialized."""
    initializer = get_initializer()
    
    # Initialize services if not already done
    if not initializer.is_initialized():
        initializer.initialize_services()


def _log_function_call(
    func_name: str,
    args: tuple,
    kwargs: Dict[str, Any],
    return_value: Any = None,
    exception: Optional[Exception] = None,
    execution_time: Optional[float] = None,
    is_async: bool = False,
) -> None:
    """Log function call details using event queue only."""
    config = get_config()
    
    if not config.enable_logging:
        return
    
    # Ensure services are initialized
    _ensure_services_initialized()
    
    # Get user context from initializer
    initializer = get_initializer()
    user_api_key = initializer.get_api_key()
    session_id = getattr(initializer, '_session_id', None)
    
    # Get function context information
    import inspect
    frame = inspect.currentframe()
    if frame:
        # Go up the call stack to find the calling function
        caller_frame = frame.f_back
        if caller_frame:
            module_name = caller_frame.f_globals.get('__name__', None)
            file_path = caller_frame.f_code.co_filename
            line_number = caller_frame.f_lineno
            
            # Try to get class name if it's a method
            class_name = None
            if 'self' in caller_frame.f_locals:
                self_obj = caller_frame.f_locals['self']
                class_name = type(self_obj).__name__
        else:
            module_name = None
            file_path = None
            line_number = None
            class_name = None
    else:
        module_name = None
        file_path = None
        line_number = None
        class_name = None
    
    # Create event for background processing
    event = create_event(
        func_name=func_name,
        args=args,
        kwargs=kwargs,
        return_value=return_value,
        exception=exception,
        execution_time=execution_time,
        is_async=is_async,
        user_api_key=user_api_key,
        session_id=session_id,
        module_name=module_name,
        class_name=class_name,
        file_path=file_path,
        line_number=line_number,
    )
    
    # Add event to queue for background processing
    event_queue = initializer.get_event_queue()
    if event_queue:
        event_queue.put(event)


def track(func: F) -> F:
    """
    Decorator to track function calls using event queue.
    
    This decorator works with both synchronous and asynchronous functions.
    It logs function name, arguments, return values, exceptions, and execution time
    by adding events to the background processing queue.
    
    Args:
        func: The function to track
        
    Returns:
        The wrapped function with tracking capabilities
        
    Example:
        >>> @track
        ... def add(a, b):
        ...     return a + b
        >>> add(1, 2)
        # Will log the function call via event queue
    """
    # Check if function is async
    is_async = asyncio.iscoroutinefunction(func)
    
    if is_async:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                _log_function_call(
                    func.__name__,
                    args,
                    kwargs,
                    return_value=result,
                    execution_time=execution_time,
                    is_async=True,
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                _log_function_call(
                    func.__name__,
                    args,
                    kwargs,
                    exception=e,
                    execution_time=execution_time,
                    is_async=True,
                )
                raise
        
        return async_wrapper  # type: ignore
    else:
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                _log_function_call(
                    func.__name__,
                    args,
                    kwargs,
                    return_value=result,
                    execution_time=execution_time,
                    is_async=False,
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                _log_function_call(
                    func.__name__,
                    args,
                    kwargs,
                    exception=e,
                    execution_time=execution_time,
                    is_async=False,
                )
                raise
        
        return sync_wrapper  # type: ignore 