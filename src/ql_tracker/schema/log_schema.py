"""
Log Schema for QL Tracker.

This module defines the comprehensive schema for log events including
user API key mapping, success status, and analytical fields for dashboard visualization.
"""

import hashlib
import json
import platform
import socket
import sys
import threading
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class LogLevel(Enum):
    """Log levels for function calls."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"


class FunctionType(Enum):
    """Types of functions being tracked."""
    SYNC = "sync"
    ASYNC = "async"
    GENERATOR = "generator"
    COROUTINE = "coroutine"


@dataclass
class SystemInfo:
    """System information for analytics."""
    platform: str
    python_version: str
    hostname: str
    process_id: int
    thread_id: int
    memory_usage_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None


@dataclass
class PerformanceMetrics:
    """Performance metrics for function calls."""
    execution_time_ms: float
    memory_delta_mb: Optional[float] = None
    cpu_time_ms: Optional[float] = None
    io_operations: Optional[int] = None
    network_calls: Optional[int] = None


@dataclass
class ErrorInfo:
    """Detailed error information."""
    error_type: str
    error_message: str
    error_code: Optional[str] = None
    stack_trace: Optional[str] = None
    severity: str = "error"
    recoverable: bool = True


@dataclass
class LogEvent:
    """
    Comprehensive log event schema for QL Tracker.
    
    This schema includes all necessary fields for dashboard analytics,
    user tracking, and performance monitoring.
    """
    # Core identification
    event_id: str
    timestamp: str
    function_name: str
    function_type: FunctionType
    args: tuple
    kwargs: Dict[str, Any]
    is_success: bool
    log_level: LogLevel
    performance: PerformanceMetrics
    system_info: SystemInfo
    
    # Optional fields with defaults
    user_api_key: Optional[str] = None
    session_id: Optional[str] = None
    module_name: Optional[str] = None
    class_name: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    return_value: Optional[Any] = None
    exception: Optional[ErrorInfo] = None
    tags: Optional[Dict[str, Any]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None
    parent_event_id: Optional[str] = None
    batch_id: Optional[str] = None
    batch_size: Optional[int] = None
    batch_position: Optional[int] = None
    execution_category: Optional[str] = None  # e.g., "database", "api", "computation"
    business_value: Optional[str] = None  # e.g., "critical", "important", "routine"
    user_impact: Optional[str] = None  # e.g., "high", "medium", "low"
    cost_estimate: Optional[float] = None  # Estimated cost in currency units
    data_sensitivity: Optional[str] = None  # e.g., "public", "internal", "confidential"
    compliance_tags: Optional[list[str]] = None  # e.g., ["GDPR", "HIPAA"]
    alert_level: Optional[str] = None  # e.g., "none", "warning", "critical"
    alert_message: Optional[str] = None
    alert_sent: bool = False
    schema_version: str = "1.0.0"
    tracker_version: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the log event to a dictionary."""
        data = asdict(self)
        
        # Convert enums to strings
        data["function_type"] = self.function_type.value
        data["log_level"] = self.log_level.value
        
        # Handle nested objects
        if self.exception:
            data["exception"] = asdict(self.exception)
        if self.performance:
            data["performance"] = asdict(self.performance)
        if self.system_info:
            data["system_info"] = asdict(self.system_info)
        
        return data
    
    def to_json(self) -> str:
        """Convert the log event to JSON string."""
        return json.dumps(self.to_dict(), default=str)
    
    def get_hash(self) -> str:
        """Get a hash of the event for deduplication."""
        content = f"{self.function_name}{self.args}{self.kwargs}{self.timestamp}"
        return hashlib.md5(content.encode()).hexdigest()


def get_system_info() -> SystemInfo:
    """Get current system information."""
    return SystemInfo(
        platform=platform.platform(),
        python_version=sys.version,
        hostname=socket.gethostname(),
        process_id=threading.get_ident(),
        thread_id=threading.current_thread().ident or 0,
    )


def get_performance_metrics(execution_time: float) -> PerformanceMetrics:
    """Get performance metrics for the function call."""
    return PerformanceMetrics(
        execution_time_ms=execution_time * 1000,  # Convert to milliseconds
    )


def determine_log_level(exception: Optional[Exception] = None, execution_time: float = 0) -> LogLevel:
    """Determine the appropriate log level based on execution context."""
    if exception is not None:
        return LogLevel.ERROR
    elif execution_time > 1.0:  # More than 1 second
        return LogLevel.WARNING
    else:
        return LogLevel.INFO


def determine_function_type(is_async: bool = False) -> FunctionType:
    """Determine the function type."""
    if is_async:
        return FunctionType.ASYNC
    else:
        return FunctionType.SYNC


def determine_execution_category(function_name: str, module_name: Optional[str] = None) -> Optional[str]:
    """Determine the execution category for analytics."""
    name_lower = function_name.lower()
    module_lower = (module_name or "").lower()
    
    # Database operations
    if any(keyword in name_lower for keyword in ["db_", "database", "query", "sql", "select", "insert", "update", "delete"]):
        return "database"
    
    # API operations
    if any(keyword in name_lower for keyword in ["api_", "http", "request", "post", "get", "put", "delete", "fetch"]):
        return "api"
    
    # File operations
    if any(keyword in name_lower for keyword in ["file_", "read", "write", "save", "load", "upload", "download"]):
        return "file_io"
    
    # Computation
    if any(keyword in name_lower for keyword in ["calculate", "compute", "process", "analyze", "transform"]):
        return "computation"
    
    # Network operations
    if any(keyword in name_lower for keyword in ["network", "socket", "connect", "send", "receive"]):
        return "network"
    
    # Default
    return "general"


def determine_business_value(function_name: str, execution_time: float, exception: Optional[Exception] = None) -> Optional[str]:
    """Determine the business value of the function call."""
    if exception is not None:
        return "critical"
    elif execution_time > 5.0:  # More than 5 seconds
        return "important"
    elif execution_time > 1.0:  # More than 1 second
        return "routine"
    else:
        return "routine"


def create_log_event(
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
) -> LogEvent:
    """
    Create a comprehensive log event.
    
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
        LogEvent instance
    """
    # Default execution time if not provided
    if execution_time is None:
        execution_time = 0.0
    
    # Determine success status
    is_success = exception is None
    
    # Create error info if exception exists
    error_info = None
    if exception is not None:
        error_info = ErrorInfo(
            error_type=type(exception).__name__,
            error_message=str(exception),
            stack_trace="".join(traceback.format_exception(type(exception), exception, exception.__traceback__)) if exception else None
        )
    
    # Generate event ID
    event_id = str(uuid.uuid4())
    
    # Create log event
    log_event = LogEvent(
        event_id=event_id,
        timestamp=datetime.now().isoformat(),
        user_api_key=user_api_key,
        session_id=session_id,
        function_name=func_name,
        function_type=determine_function_type(is_async),
        module_name=module_name,
        class_name=class_name,
        file_path=file_path,
        line_number=line_number,
        args=args,
        kwargs=kwargs,
        return_value=return_value,
        exception=error_info,
        is_success=is_success,
        log_level=determine_log_level(exception, execution_time),
        performance=get_performance_metrics(execution_time),
        system_info=get_system_info(),
        tags=tags,
        custom_fields=custom_fields,
        correlation_id=correlation_id,
        parent_event_id=parent_event_id,
        execution_category=determine_execution_category(func_name, module_name),
        business_value=determine_business_value(func_name, execution_time, exception),
        user_impact="medium",  # Default, can be customized
        data_sensitivity="internal",  # Default, can be customized
        compliance_tags=[],  # Default, can be customized
        alert_level="none",  # Default, can be customized
        alert_sent=False,
        tracker_version="0.1.0",  # Should be dynamic
    )
    
    return log_event


def validate_log_event(log_event: LogEvent) -> bool:
    """
    Validate a log event.
    
    Args:
        log_event: LogEvent to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Check required fields
        if not log_event.event_id:
            return False
        if not log_event.function_name:
            return False
        if not log_event.timestamp:
            return False
        
        # Check data types
        if not isinstance(log_event.is_success, bool):
            return False
        if not isinstance(log_event.performance, PerformanceMetrics):
            return False
        if not isinstance(log_event.system_info, SystemInfo):
            return False
        
        # Check enum values
        if log_event.function_type not in FunctionType:
            return False
        if log_event.log_level not in LogLevel:
            return False
        
        return True
    except Exception:
        return False


def create_dashboard_analytics(log_events: list[LogEvent]) -> Dict[str, Any]:
    """
    Create dashboard analytics from a list of log events.
    
    Args:
        log_events: List of log events
        
    Returns:
        Dictionary with analytics data
    """
    if not log_events:
        return {}
    
    total_events = len(log_events)
    successful_events = sum(1 for event in log_events if event.is_success)
    failed_events = total_events - successful_events
    
    # Performance metrics
    execution_times = [event.performance.execution_time_ms for event in log_events]
    avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
    max_execution_time = max(execution_times) if execution_times else 0
    min_execution_time = min(execution_times) if execution_times else 0
    
    # Function distribution
    function_counts = {}
    for event in log_events:
        func_name = event.function_name
        function_counts[func_name] = function_counts.get(func_name, 0) + 1
    
    # Error analysis
    error_types = {}
    for event in log_events:
        if event.exception:
            error_type = event.exception.error_type
            error_types[error_type] = error_types.get(error_type, 0) + 1
    
    # Category distribution
    category_counts = {}
    for event in log_events:
        category = event.execution_category or "unknown"
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Business value distribution
    business_value_counts = {}
    for event in log_events:
        value = event.business_value or "unknown"
        business_value_counts[value] = business_value_counts.get(value, 0) + 1
    
    return {
        "summary": {
            "total_events": total_events,
            "successful_events": successful_events,
            "failed_events": failed_events,
            "success_rate": (successful_events / total_events * 100) if total_events > 0 else 0,
        },
        "performance": {
            "average_execution_time_ms": avg_execution_time,
            "max_execution_time_ms": max_execution_time,
            "min_execution_time_ms": min_execution_time,
            "total_execution_time_ms": sum(execution_times),
        },
        "functions": {
            "top_functions": sorted(function_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "function_count": len(function_counts),
        },
        "errors": {
            "error_types": error_types,
            "total_errors": failed_events,
        },
        "categories": {
            "category_distribution": category_counts,
        },
        "business_value": {
            "value_distribution": business_value_counts,
        },
        "time_series": {
            "events_per_minute": {},  # Would need timestamp grouping
            "errors_per_minute": {},  # Would need timestamp grouping
        }
    } 