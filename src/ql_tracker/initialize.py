"""
Initialization module for QL Tracker.

This module provides a singleton pattern for initializing all services
with API key and host configuration.
"""

import threading
from typing import Optional

from .config import get_config, load_config
from .services.queue.event_queue import EventQueue
from .services.storage.storage_service import StorageService
from .services.background_executor.background_executor import initialize_services, get_background_executor


class QLTrackerInitializer:
    """
    Singleton class for initializing QL Tracker services.
    
    This class ensures that services are initialized only once and provides
    a centralized way to configure and start all background services.
    """
    
    _instance: Optional['QLTrackerInitializer'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'QLTrackerInitializer':
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    # Initialize the instance
                    cls._instance._event_queue = None
                    cls._instance._storage_service = None
                    cls._instance._network_request = None
                    cls._instance._log_worker = None
                    cls._instance._background_executor = get_background_executor()
                    cls._instance._api_key = None
                    cls._instance._host = None
                    cls._instance._session_id = None
                    cls._instance._services_started = False
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize the QL Tracker initializer (no-op for singleton)."""
        pass
    
    def configure(
        self,
        api_key: Optional[str] = None,
        host: Optional[str] = None,
        config_path: Optional[str] = "trackconfig.toml"
    ) -> 'QLTrackerInitializer':
        """
        Configure the QL Tracker initializer.
        
        Args:
            api_key: API key for external services
            host: Host URL for external services
            config_path: Path to a configuration file
            
        Returns:
            Self for method chaining
        """
         # Load configuration
        if config_path:
            load_config(config_path)
            config = get_config()
            if config.api_key:
                self._api_key = config.api_key
            if config.host:
                self._host = config.host
        
        # Set API key and host
        if api_key:
            self._api_key = api_key
        if host:
            self._host = host
        
        return self
    
    def initialize_services(self) -> 'QLTrackerInitializer':
        """
        Initialize all background services.
        
        Returns:
            Self for method chaining
        """
        if self._services_started:
            return self
        
        # Load configuration
        config = get_config()
        

        

        
        # Initialize background services
        event_queue,storage_service,log_worker, network_request = initialize_services(
            host=self._host,
            api_key=self._api_key,
            backend_type=config.storage_backend,
            output_path=config.storage_output_path,
            worker_interval_secs=3.0,  # Process logs every 3 seconds
        )
        # Create event queue
        self._event_queue = event_queue
        # Create storage service
        self._storage_service = storage_service
        # Store references to services

        self._log_worker = log_worker
        self._network_request = network_request
        
        self._services_started = True
        return self
    
    def start(self) -> 'QLTrackerInitializer':
        """
        Start all background services.
        
        Returns:
            Self for method chaining
        """
        if not self._services_started:
            self.initialize_services()
        
        # Start background executor
        self._background_executor.start_all_services()
        return self
    
    def stop(self) -> 'QLTrackerInitializer':
        """
        Stop all background services.
        
        Returns:
            Self for method chaining
        """
        self._background_executor.stop_all_services()
        return self
    
    def get_event_queue(self) -> Optional[EventQueue]:
        """
        Get the event queue instance.
        
        Returns:
            EventQueue instance or None if not initialized
        """
        return self._event_queue
    
    def get_storage_service(self) -> Optional[StorageService]:
        """
        Get the storage service instance.
        
        Returns:
            StorageService instance or None if not initialized
        """
        return self._storage_service

    
    def get_log_worker(self):
        """
        Get the log worker service instance.
        
        Returns:
            LogWorkerService instance or None if not initialized
        """
        return self._log_worker
    
    def get_background_executor(self):
        """
        Get the background executor instance.
        
        Returns:
            BackgroundExecutorService instance
        """
        return self._background_executor
    
    def get_api_key(self) -> Optional[str]:
        """
        Get the configured API key.
        
        Returns:
            API key or None if not configured
        """
        return self._api_key
    
    def get_host(self) -> Optional[str]:
        """
        Get the configured host URL.
        
        Returns:
            Host URL or None if not configured
        """
        return self._host
    
    def get_session_id(self) -> Optional[str]:
        """
        Get the current session ID.
        
        Returns:
            Session ID or None if not set
        """
        return self._session_id
    
    def set_session_id(self, session_id: str) -> None:
        """
        Set the session ID for tracking.
        
        Args:
            session_id: Session identifier
        """
        self._session_id = session_id
    
    def is_initialized(self) -> bool:
        """
        Check if services are initialized.
        
        Returns:
            True if services are initialized, False otherwise
        """
        return self._services_started
    
    def is_running(self) -> bool:
        """
        Check if services are running.
        
        Returns:
            True if services are running, False otherwise
        """
        return self._background_executor.is_running()
    
    def get_stats(self) -> dict:
        """
        Get statistics about all services.
        
        Returns:
            Dictionary with service statistics
        """
        stats = {
            "initialized": self.is_initialized(),
            "running": self.is_running(),
            "api_key_configured": self._api_key is not None,
            "host_configured": self._host is not None,
        }
        
        if self._background_executor:
            stats.update(self._background_executor.get_service_stats())
        
        return stats


# Global singleton instance
_initializer: Optional[QLTrackerInitializer] = None


def get_initializer() -> QLTrackerInitializer:
    """
    Get the global QL Tracker initializer instance.
    
    Returns:
        QLTrackerInitializer singleton instance
    """
    global _initializer
    if _initializer is None:
        _initializer = QLTrackerInitializer()
    return _initializer


def initialize(
    api_key: Optional[str] = None,
    host: Optional[str] = None,
    config_path: Optional[str] = None,
    auto_start: bool = True
) -> QLTrackerInitializer:
    """
    Initialize QL Tracker services.
    
    Args:
        api_key: API key for external services
        host: Host URL for external services
        config_path: Path to a configuration file
        auto_start: Whether to automatically start services
        
    Returns:
        QLTrackerInitializer instance
    """
    initializer = get_initializer()
    
    # Configure and initialize
    initializer.configure(api_key=api_key, host=host, config_path=config_path)
    initializer.initialize_services()
    
    # Start services if requested
    if auto_start:
        initializer.start()
    
    return initializer


def shutdown() -> None:
    """Shutdown all QL Tracker services."""
    initializer = get_initializer()
    initializer.stop()


def get_stats() -> dict:
    """
    Get statistics about QL Tracker services.
    
    Returns:
        Dictionary with service statistics
    """
    initializer = get_initializer()
    return initializer.get_stats() 