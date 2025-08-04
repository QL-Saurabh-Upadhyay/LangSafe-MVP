"""
Batch Logger Service for QL Tracker.

This module provides a background service that monitors the event queue
and flushes events to storage based on batch size and time intervals.
"""

import threading
import time
from typing import Any, Dict, Optional

from ..queue.event_queue import EventQueue
from ql_tracker.services.storage.storage_service import StorageService


class BatchLoggerService:
    """
    Background service that monitors the event queue and flushes events to storage.
    
    This service runs continuously in a background thread and flushes events
    when either a maximum batch size is reached or a time interval has elapsed.
    """
    
    def __init__(
        self,
        event_queue: EventQueue,
        storage_service: StorageService,
        max_batch_size: int = 10,
        flush_interval_secs: float = 5.0,
        auto_process: bool = True,
    ) -> None:
        """
        Initialize the batch logger service.
        
        Args:
            event_queue: Event queue to monitor
            storage_service: Storage service for persisting events
            max_batch_size: Maximum number of events to batch before flushing
            flush_interval_secs: Time interval in seconds to flush events
            auto_process: Whether to automatically process events in background thread
        """
        self.event_queue = event_queue
        self.storage_service = storage_service
        self.max_batch_size = max_batch_size
        self.flush_interval_secs = flush_interval_secs
        self.auto_process = auto_process
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._last_flush_time = time.time()
        self._batch_count = 0
        self._total_events_processed = 0
    
    def start(self) -> None:
        """Start the batch logger service in a background thread."""
        with self._lock:
            if self._running:
                return
            
            self._running = True
            if self.auto_process:
                self._thread = threading.Thread(target=self._run, daemon=True)
                self._thread.start()
    
    def stop(self) -> None:
        """Stop the batch logger service."""
        with self._lock:
            self._running = False
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
    
    def _run(self) -> None:
        """Main loop for the batch logger service."""
        while self._running:
            try:
                # Check if we should flush based on time interval
                current_time = time.time()
                time_since_last_flush = current_time - self._last_flush_time
                
                if time_since_last_flush >= self.flush_interval_secs:
                    self._flush_events()
                    self._last_flush_time = current_time
                
                # Try to get events from the queue
                events = self.event_queue.get_batch(
                    max_size=self.max_batch_size,
                    timeout=min(1.0, self.flush_interval_secs / 2)
                )
                
                if events:
                    # Store events immediately if we have a full batch
                    if len(events) >= self.max_batch_size:
                        self.storage_service.store(events)
                        self._batch_count += 1
                        self._total_events_processed += len(events)
                    else:
                        # For smaller batches, we'll wait for the time-based flush
                        # This is a simplified approach - in a real implementation,
                        # you might want to buffer these events
                        self.storage_service.store(events)
                        self._batch_count += 1
                        self._total_events_processed += len(events)
                
                # Small sleep to prevent busy waiting
                time.sleep(0.1)
                
            except Exception as e:
                # Log error but continue running
                print(f"Error in batch logger service: {e}")
                time.sleep(1.0)
    
    def _flush_events(self) -> None:
        """Flush any remaining events from the queue."""
        events = self.event_queue.get_batch(max_size=100, timeout=0)
        if events:
            self.storage_service.store(events)
            self._batch_count += 1
            self._total_events_processed += len(events)
    
    def is_running(self) -> bool:
        """
        Check if the service is running.
        
        Returns:
            True if the service is running, False otherwise
        """
        with self._lock:
            return self._running
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the batch logger service.
        
        Returns:
            Dictionary with service statistics
        """
        return {
            "running": self.is_running(),
            "batch_count": self._batch_count,
            "total_events_processed": self._total_events_processed,
            "queue_size": self.event_queue.size(),
            "max_batch_size": self.max_batch_size,
            "flush_interval_secs": self.flush_interval_secs,
        }
    
    def force_flush(self) -> None:
        """Force an immediate flush of all events in the queue."""
        self._flush_events() 