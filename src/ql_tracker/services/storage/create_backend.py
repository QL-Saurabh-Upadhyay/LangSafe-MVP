from ql_tracker.services.storage.storage import StorageBackend
from ql_tracker.services.storage.json_storage import JSONLStorageBackend
from ql_tracker.services.storage.remote_storage import RemoteStorageBackend


def create_backend(backend_type: str, **kwargs) -> StorageBackend:
    """
    Create a storage backend based on type.

    Args:
        backend_type: Type of backend to create
        **kwargs: Arguments for the backend

    Returns:
        Storage backend instance

    Raises:
        ValueError: If a backend type is not supported
    """
    if backend_type.lower() == "jsonl":
        return JSONLStorageBackend(**kwargs)
    if backend_type.lower() == "remote":
        return RemoteStorageBackend(
            network_request=kwargs["network_request"],
            endpoint=kwargs.get("endpoint", "logs/batch")
        )
    else:
        raise ValueError(f"Unsupported storage backend: {backend_type}")
