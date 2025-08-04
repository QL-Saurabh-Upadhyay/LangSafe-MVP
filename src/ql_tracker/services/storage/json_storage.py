import json
from pathlib import Path
from typing import List, Dict, Any

from ql_tracker.services.storage.storage import StorageBackend


class JSONLStorageBackend(StorageBackend):
    """JSON Lines storage backend."""

    def __init__(self, output_path: str) -> None:
        """
        Initialize JSON storage backend.

        Args:
            output_path: Path to the output file
        """
        self.output_path = Path(output_path)
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the storage backend by creating the output directory."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialized = True

    def store(self, events: List[Dict[str, Any]]) -> None:
        """
        Store events to JSON file.

        Args:
            events: List of event dictionaries to store
        """
        if not self._initialized:
            self.initialize()

        # Ensure the directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write events to file
        with open(self.output_path, "a", encoding="utf-8") as f:
            for event in events:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

