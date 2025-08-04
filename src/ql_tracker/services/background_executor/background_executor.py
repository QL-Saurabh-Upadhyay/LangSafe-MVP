"""
Background Executor Service for QL Tracker.

This module provides a service manager that handles background threads
and ensures a graceful shutdown of long-running services.
"""

import atexit
import signal
import threading
from typing import Any, Dict, List


from ..queue.event_queue import EventQueue
from ql_tracker.services.storage.storage_service import StorageService
from ..worker.log_worker import LogWorkerService
from ..network_request.network_request import NetworkRequestService


class BackgroundExecutorService:
    """
    Service manager for background threads and graceful shutdown.
    
    This service manages the lifecycle of background services like
    BatchLoggerService and ensures they are properly started and stopped.
    """
    
    def __init__(self) -> None:
        """Initialize the background executor service."""
        self._services: List[Any] = []
        self._running = False
        self._lock = threading.Lock()
        self._shutdown_hooks: List[callable] = []
        
        # Register shutdown handlers
        atexit.register(self._shutdown)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def add_service(self, service: Any) -> None:
        """
        Add a service to be managed.
        
        Args:
            service: Service object with start() and stop() methods
        """
        with self._lock:
            self._services.append(service)
    
    def start_all_services(self) -> None:
        """Start all registered services."""
        with self._lock:
            if self._running:
                return
            
            self._running = True
            
            for service in self._services:
                try:
                    if hasattr(service, 'start'):
                        service.start()
                except Exception as e:
                    print(f"Error starting service {type(service).__name__}: {e}")
    
    def stop_all_services(self) -> None:
        """Stop all registered services."""
        with self._lock:
            if not self._running:
                return
            
            self._running = False
            
            # Stop services in reverse order
            for service in reversed(self._services):
                try:
                    if hasattr(service, 'stop'):
                        service.stop()
                    elif hasattr(service, 'force_flush'):
                        service.force_flush()
                except Exception as e:
                    print(f"Error stopping service {type(service).__name__}: {e}")
    
    def add_shutdown_hook(self, hook: callable) -> None:
        """
        Add a shutdown hook to be called during shutdown.
        
        Args:
            hook: Function to call during shutdown
        """
        self._shutdown_hooks.append(hook)
    
    def _shutdown(self) -> None:
        """Internal shutdown method called by at exit."""
        if self._running:
            print("Shutting down background services...")
            self.stop_all_services()
            
            # Call shutdown hooks
            for hook in self._shutdown_hooks:
                try:
                    hook()
                except Exception as e:
                    print(f"Error in shutdown hook: {e}")
    
    def _signal_handler(self, signum: int, frame: Any) -> None:
        """Handle shutdown signals."""
        print(f"\nReceived signal {signum}, shutting down...")
        self._shutdown()
        exit(0)
    
    def is_running(self) -> bool:
        """
        Check if the service manager is running.
        
        Returns:
            True if services are running, False otherwise
        """
        with self._lock:
            return self._running
    
    def get_service_stats(self) -> Dict[str, Any]:
        """
        Get statistics about all managed services.
        
        Returns:
            Dictionary with service statistics
        """
        stats = {
            "running": self.is_running(),
            "service_count": len(self._services),
            "services": []
        }
        
        for service in self._services:
            service_stats = {
                "type": type(service).__name__,
                "running": getattr(service, 'is_running', lambda: False)()
            }
            
            # Add service-specific stats if available
            if hasattr(service, 'get_stats'):
                service_stats.update(service.get_stats())
            
            stats["services"].append(service_stats)
        
        return stats


# Global instance for easy access
_background_executor = BackgroundExecutorService()


def get_background_executor() -> BackgroundExecutorService:
    """
    Get the global background executor instance.
    
    Returns:
        BackgroundExecutorService instance
    """
    return _background_executor


def initialize_services(
    host,
    api_key,
    backend_type,
    output_path,
    worker_interval_secs: float = 3.0,
) -> tuple[EventQueue,StorageService,LogWorkerService,NetworkRequestService]:
    """
    Initialize and start all background services.
    
    Args:
        event_queue: Event queue instance
        storage_service: Storage service instance
        max_batch_size: Maximum batch size for logging
        flush_interval_secs: Flush interval in seconds
        worker_interval_secs: Worker processing interval in seconds
        
    Returns:
        Tuple of (BatchLoggerService, LogWorkerService) instances
        :param output_path:
        :param backend_type:
        :param worker_interval_secs:
        :param api_key:
        :param host:
    """

    event_queue = EventQueue()

    # Create Network Request service
    network_request = NetworkRequestService(
        base_url=host,
        api_key=api_key
    )
    storage_service= None

    if backend_type == "jsonl":
        storage_service = StorageService(backend_type=backend_type, output_path=output_path)
    else:
        storage_service = StorageService(
            backend_type=backend_type,
            network_request=network_request,
            endpoint="api/logs"
        )

    # Create log worker service
    log_worker = LogWorkerService(
        event_queue=event_queue,
        processing_interval_secs=worker_interval_secs,
        storage_service=storage_service
    )
    
    # Add to background executor
    executor = get_background_executor()

    executor.add_service(event_queue)
    executor.add_service(network_request)
    executor.add_service(storage_service)
    executor.add_service(log_worker)




    # Start all services
    executor.start_all_services()
    
    return event_queue,storage_service,log_worker,network_request