"""
Log Worker Service for QL Tracker.

This module provides a background worker that picks up logs every 3 seconds
and processes them through the batch logger.
"""

import threading
import time
from typing import Any, Dict, Optional

from ..queue.event_queue import EventQueue
from ql_tracker.services.storage.storage_service import StorageService


class LogWorkerService:
    """
    Background worker that picks up logs every 3 seconds and processes them.
    
    This service runs continuously in a background thread and processes events
    from the queue at regular intervals, ensuring logs are processed efficiently
    in the background.
    """
    
    def __init__(
        self,
        event_queue: EventQueue,
        storage_service: StorageService,
        processing_interval_secs: float = 3.0,

    ) -> None:
        """
        Initialize the log worker service.
        
        Args:
            event_queue: Event queue to monitor
            processing_interval_secs: Time interval in seconds between processing cycles
        """
        self.event_queue = event_queue
        self.storage_service =storage_service
        self.processing_interval_secs = processing_interval_secs
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._total_events_processed = 0
        self._processing_cycles = 0
        self._last_processing_time = 0.0
        self._wake_signal = self.event_queue.new_event_signal

    def start(self) -> None:
        """Start the log worker service in a background thread."""
        with self._lock:
            if self._running:
                return
            
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            print(f"Log worker started - processing logs every {self.processing_interval_secs} seconds")
    
    def stop(self) -> None:
        """Stop the log worker service."""
        with self._lock:
            self._running = False
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=10.0)
            print("Log worker stopped")
    
    def _run(self) -> None:
        """Main loop for the log worker service."""

        while self._running:
            # Wait until a new event arrives or timeout for the interval
            self._wake_signal.wait(timeout=self.processing_interval_secs)
            # Immediately clear the signal before processing
            self._wake_signal.clear()
                # Process events if enough time has passed
            try:
               self._process_events()
               self._processing_cycles += 1
               self._last_processing_time = time.time()
            except Exception as e:
               print(f"Error in log worker service: {e}")
               time.sleep(1.0)

    
    def _process_events(self) -> None:
        """Process events from the queue."""
        try:
            # Get all available events from the queue
            events = self.event_queue.get_batch(max_size=100, timeout=0)
            
            if events:
                # Process events through batch logger
                self.storage_service.store(events)
                self._total_events_processed += len(events)
                
                # Log processing info with more details
                print(f"Log worker processed {len(events)} events (total: {self._total_events_processed})")
                for event in events:
                    func_name = event.get('function_name', 'unknown')
                    print(f"  - Processed: {func_name}")
            else:
                print("Log worker: No events to process")
            
        except Exception as e:
            print(f"Error processing events in log worker: {e}")
    
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
        Get statistics about the log worker service.
        
        Returns:
            Dictionary with service statistics
        """
        return {
            "running": self.is_running(),
            "processing_cycles": self._processing_cycles,
            "total_events_processed": self._total_events_processed,
            "queue_size": self.event_queue.size(),
            "processing_interval_secs": self.processing_interval_secs,
            "last_processing_time": self._last_processing_time,
        }
    
    def force_process(self) -> None:
        """Force an immediate professing of all events in the queue."""
        self._process_events() 