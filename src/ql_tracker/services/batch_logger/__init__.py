"""
Batch Logger Service for QL Tracker.

This module provides a background service that monitors the event queue
and flushes events to storage based on batch size and time intervals.
"""

from .batch_logger import BatchLoggerService

__all__ = ["BatchLoggerService"] 