#!/usr/bin/env python3
"""
Example demonstrating background processing capabilities of QL Tracker.

This example shows how the @track decorator automatically processes events
in the background using the EventQueue, BatchLoggerService, and StorageService.
"""

import asyncio
import time
from typing import List

from trackdecorator import track, get_background_executor


@track
def process_data(items: List[int]) -> List[int]:
    """Process a list of numbers."""
    time.sleep(0.1)  # Simulate processing
    return [x * 2 for x in items]


@track
def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


@track
async def async_process_data(data: List[str]) -> List[str]:
    """Process data asynchronously."""
    await asyncio.sleep(0.2)  # Simulate async work
    return [item.upper() for item in data]


@track
def function_with_error() -> None:
    """A function that raises an exception."""
    raise ValueError("This is a test error for background processing")


def main() -> None:
    """Main function demonstrating background processing."""
    print("=== QL Tracker Background Processing Example ===\n")
    
    # Get background executor to monitor services
    executor = get_background_executor()
    
    print("Starting background services...")
    print(f"Services running: {executor.is_running()}")
    
    # Test various function calls
    print("\n1. Processing data...")
    result = process_data([1, 2, 3, 4, 5])
    print(f"Result: {result}")
    
    print("\n2. Calculating Fibonacci...")
    fib_result = calculate_fibonacci(5)
    print(f"Fibonacci(5) = {fib_result}")
    
    print("\n3. Async processing...")
    async def run_async():
        return await async_process_data(["hello", "world", "python"])
    
    async_result = asyncio.run(run_async())
    print(f"Async result: {async_result}")
    
    print("\n4. Function with error...")
    try:
        function_with_error()
    except ValueError as e:
        print(f"Caught error: {e}")
    
    # Show service statistics
    print("\n5. Service Statistics:")
    stats = executor.get_service_stats()
    print(f"Background executor running: {stats['running']}")
    print(f"Number of services: {stats['service_count']}")
    
    for service in stats['services']:
        print(f"  - {service['type']}: running={service['running']}")
        if 'batch_count' in service:
            print(f"    Batches processed: {service['batch_count']}")
        if 'total_events_processed' in service:
            print(f"    Total events: {service['total_events_processed']}")
        if 'queue_size' in service:
            print(f"    Queue size: {service['queue_size']}")
    
    print("\n6. Waiting for background processing...")
    time.sleep(3)  # Wait for background processing
    
    # Show updated statistics
    print("\n7. Updated Service Statistics:")
    stats = executor.get_service_stats()
    for service in stats['services']:
        print(f"  - {service['type']}: running={service['running']}")
        if 'batch_count' in service:
            print(f"    Batches processed: {service['batch_count']}")
        if 'total_events_processed' in service:
            print(f"    Total events: {service['total_events_processed']}")
        if 'queue_size' in service:
            print(f"    Queue size: {service['queue_size']}")
    
    print("\n=== Example completed ===")
    print("Check the logs/ql-tracker.jsonl file for stored events!")


if __name__ == "__main__":
    main() 