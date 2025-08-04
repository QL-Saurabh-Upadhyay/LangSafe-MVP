"""
Event Queue Service for QL Tracker.

This module provides a thread-safe in-memory queue for storing function call events.
"""

from .event_queue import EventQueue, create_event

__all__ = ["EventQueue", "create_event"] 