"""
Storage Service for QL Tracker.

This module provides storage backends for persisting function call events to disk.
"""


from abc import ABC, abstractmethod
from typing import Any, Dict, List


class StorageBackend(ABC):
    """Abstract base class for storage backends."""
    
    @abstractmethod
    def store(self, events: List[Dict[str, Any]]) -> None:
        """
        Store a batch of events.
        
        Args:
            events: List of event dictionaries to store
        """
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the storage backend."""
        pass