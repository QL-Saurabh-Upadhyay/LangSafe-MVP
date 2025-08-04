"""
QL Tracker - A modern Python decorator for tracking function calls.

This package provides a `@track` decorator that logs function calls with rich formatting,
supporting both synchronous and asynchronous functions, along with background event processing.
"""

from .tracker import track
from .config import load_config, get_config
from .services.queue.event_queue import EventQueue, create_event
from .services.storage.storage_service import StorageService
from .services.background_executor.background_executor import BackgroundExecutorService, get_background_executor
from .initialize import initialize, shutdown, get_stats, get_initializer, QLTrackerInitializer

__version__ = "0.2.0"
__all__ = [
    "track", 
    "load_config", 
    "get_config",
    "EventQueue",
    "create_event", 
    "StorageService",
    "BackgroundExecutorService",
    "get_background_executor",
    "initialize",
    "shutdown",
    "get_stats",
    "get_initializer",
    "QLTrackerInitializer"
] 