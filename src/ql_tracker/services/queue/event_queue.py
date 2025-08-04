"""
Event Queue Service for QL Tracker.

This module provides a thread-safe in-memory queue for storing function call events.
"""

import threading
from queue import Queue
from typing import Any, Dict, Optional


class EventQueue:
    """
    Thread-safe in-memory queue for storing function call events.
    
    This class provides a thread-safe queue that stores function call events
    with metadata including function name, arguments, return values, exceptions,
    and timestamps.
    """
    
    def __init__(self, maxsize: int = 1000) -> None:
        """
        Initialize the event queue.
        
        Args:
            maxsize: Maximum number of events in the queue
        """
        self._queue: Queue = Queue(maxsize=maxsize)
        self._lock = threading.Lock()
        self._event_count = 0
        self._new_event_signal = threading.Event()
    
    def put(self, event: Dict[str, Any]) -> None:
        """
        Add an event to the queue.
        
        Args:
            event: Event dictionary containing function call data
        """
        with self._lock:
            self._event_count += 1
            current_size = self._queue.qsize()
        
        self._queue.put(event)
        if current_size >= 10:
            self._new_event_signal.set()
    
    def get(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Get an event from the queue.
        
        Args:
            timeout: Timeout in seconds for getting an event
            
        Returns:
            Event dictionary or None of timeouts
        """
        try:
            return self._queue.get(timeout=timeout)
        except:
            return None
    
    def get_batch(self, max_size: int, timeout: float = 0.1) -> list[Dict[str, Any]]:
        """
        Get a batch of events from the queue.
        
        Args:
            max_size: Maximum number of events to get
            timeout: Timeout in seconds for getting each event
            
        Returns:
            List of event dictionaries
        """
        events = []
        
        # Get the first event with timeout
        first_event = self.get(timeout=timeout)
        if first_event is None:
            return events
        
        events.append(first_event)
        
        # Try to get more events without blocking
        for _ in range(max_size - 1):
            event = self.get(timeout=0)
            if event is None:
                break
            events.append(event)
        
        return events
    
    def size(self) -> int:
        """
        Get the current size of the queue.
        
        Returns:
            Number of events in the queue
        """
        return self._queue.qsize()
    
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Returns:
            True if queue is empty, False otherwise
        """
        return self._queue.empty()
    
    def clear(self) -> None:
        """Clear all events from the queue."""
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except:
                break
    
    def get_event_count(self) -> int:
        """
        Get the total number of events that have been put into the queue.
        
        Returns:
            Total event count
        """
        with self._lock:
            return self._event_count

    @property
    def new_event_signal(self):
        return self._new_event_signal


def create_event(
    func_name: str,
    args: tuple,
    kwargs: Dict[str, Any],
    return_value: Any = None,
    exception: Optional[Exception] = None,
    execution_time: Optional[float] = None,
    is_async: bool = False,
    user_api_key: Optional[str] = None,
    session_id: Optional[str] = None,
    module_name: Optional[str] = None,
    class_name: Optional[str] = None,
    file_path: Optional[str] = None,
    line_number: Optional[int] = None,
    tags: Optional[Dict[str, Any]] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None,
    parent_event_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a standardized event dictionary using the new schema.
    
    Args:
        func_name: Name of the function
        args: Function arguments
        kwargs: Function keyword arguments
        return_value: Function return value
        exception: Exception if function failed
        execution_time: Function execution time in seconds
        is_async: Whether the function is async
        user_api_key: User's API key for tracking
        session_id: Session identifier
        module_name: Module name where function is defined
        class_name: Class name if function is a method
        file_path: File path where function is defined
        line_number: Line number where function is called
        tags: Additional tags for categorization
        custom_fields: Custom fields for specific use cases
        correlation_id: Correlation ID for request tracing
        parent_event_id: Parent event ID for nested calls
        
    Returns:
        Event dictionary with comprehensive schema
    """
    from ...schema.log_schema import create_log_event
    
    # Create comprehensive log event
    log_event = create_log_event(
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
        tags=tags,
        custom_fields=custom_fields,
        correlation_id=correlation_id,
        parent_event_id=parent_event_id,
    )
    
    # Convert to dictionary for queue storage
    return log_event.to_dict() 