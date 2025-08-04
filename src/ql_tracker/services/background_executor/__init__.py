"""
Background Executor Service for QL Tracker.

This module provides a service manager that handles background threads
and ensures graceful shutdown of long-running services.
"""

from .background_executor import BackgroundExecutorService, get_background_executor, initialize_services

__all__ = ["BackgroundExecutorService", "get_background_executor", "initialize_services"] 