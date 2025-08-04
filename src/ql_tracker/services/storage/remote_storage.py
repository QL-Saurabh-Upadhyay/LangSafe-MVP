from typing import Dict, List, Any

import requests
from ql_tracker.services.storage.storage import StorageBackend


class RemoteStorageBackend(StorageBackend):
    """HTTP-based storage backend."""

    def __init__(self, network_request: 'NetworkRequestService',endpoint: str = "logs/batch"):
        """
        Initialize HTTP storage backend.

        Args:
            endpoint: HTTP endpoint URL to send events to
        """
        self.network_request = network_request
        self.endpoint = endpoint
        self._initialized = False

    def initialize(self) -> None:
        """Prepare the backend (no-op for HTTP)."""
        self._initialized = True

    def store(self, events: List[Dict[str, Any]]) -> None:
        """Send events to HTTP endpoint as a POST request."""
        if not self._initialized:
            self.initialize()

        self.network_request.batch_post(
            endpoint=self.endpoint,
            data=events
        )
