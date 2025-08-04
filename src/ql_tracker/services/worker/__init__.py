"""
Worker Service for QL Tracker.

This module provides a background worker that picks up logs every 3 seconds
and processes them through the batch logger.
"""

from .log_worker import LogWorkerService

__all__ = ["LogWorkerService"] 