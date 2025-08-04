from typing import List, Dict, Any

from ql_tracker.services.storage.create_backend import create_backend


class StorageService:
    """
    Storage service for persisting events to disk.

    This service provides a pluggable storage interface that can be extended
    with different backends (JSONL, SQLite, etc.).
    """

    def __init__(self, backend_type: str = "jsonl", **backend_kwargs) -> None:
        """
        Initialize the storage service.

        Args:
            backend_type: Type of storage backend to use
            **backend_kwargs: Additional arguments for the backend
        """
        self.backend_type = backend_type
        self.backend = create_backend(backend_type, **backend_kwargs)
        self.backend.initialize()

    def store(self, events: List[Dict[str, Any]]) -> None:
        """
        Store a batch of events.

        Args:
            events: List of event dictionaries to store
        """
        if events:
            self.backend.store(events)

    def get_backend_info(self) -> Dict[str, Any]:
        """
        Get information about the current backend.

        Returns:
            Dictionary with backend information
        """
        return {
            "type": self.backend_type,
            "backend_class": type(self.backend).__name__
        }