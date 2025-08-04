#!/usr/bin/env python3
"""
Example demonstrating the new initialization API with API key and host configuration.

This example shows how to use the singleton initializer to configure and start
QL Tracker services with API key and host settings.
"""

import asyncio
import time
from typing import List

from trackdecorator import track, initialize, shutdown, get_stats, get_initializer


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
    raise ValueError("This is a test error for initialization example")


def main() -> None:
    """Main function demonstrating the initialization API."""
    print("=== QL Tracker Initialization Example ===\n")
    
    # Method 1: Using the initialize function
    print("1. Initializing with API key and host...")
    initializer = initialize(
        api_key="your-api-key-here",
        host="https://api.example.com",
        config_path="trackconfig.toml"
    )
    
    print(f"   API Key configured: {initializer.get_api_key() is not None}")
    print(f"   Host configured: {initializer.get_host()}")
    print(f"   Services initialized: {initializer.is_initialized()}")
    print(f"   Services running: {initializer.is_running()}")
    
    # Method 2: Using the singleton directly
    print("\n2. Using singleton initializer...")
    singleton = get_initializer()
    print(f"   Same instance: {initializer is singleton}")
    print(f"   API Key: {singleton.get_api_key()}")
    print(f"   Host: {singleton.get_host()}")
    
    # Test function calls
    print("\n3. Testing function calls...")
    result = process_data([1, 2, 3, 4, 5])
    print(f"   Process data result: {result}")
    
    fib_result = calculate_fibonacci(5)
    print(f"   Fibonacci(5) = {fib_result}")
    
    print("\n4. Testing async function...")
    async def run_async():
        return await async_process_data(["hello", "world", "python"])
    
    async_result = asyncio.run(run_async())
    print(f"   Async result: {async_result}")
    
    print("\n5. Testing error handling...")
    try:
        function_with_error()
    except ValueError as e:
        print(f"   Caught error: {e}")
    
    # Show statistics
    print("\n6. Service Statistics:")
    stats = get_stats()
    print(f"   Initialized: {stats['initialized']}")
    print(f"   Running: {stats['running']}")
    print(f"   API Key configured: {stats['api_key_configured']}")
    print(f"   Host configured: {stats['host_configured']}")
    print(f"   Service count: {stats['service_count']}")
    
    for service in stats['services']:
        print(f"   - {service['type']}: running={service['running']}")
        if 'batch_count' in service:
            print(f"     Batches processed: {service['batch_count']}")
        if 'total_events_processed' in service:
            print(f"     Total events: {service['total_events_processed']}")
        if 'queue_size' in service:
            print(f"     Queue size: {service['queue_size']}")
    
    # Wait for background processing
    print("\n7. Waiting for background processing...")
    time.sleep(3)
    
    # Show updated statistics
    print("\n8. Updated Statistics:")
    updated_stats = get_stats()
    for service in updated_stats['services']:
        print(f"   - {service['type']}: running={service['running']}")
        if 'batch_count' in service:
            print(f"     Batches processed: {service['batch_count']}")
        if 'total_events_processed' in service:
            print(f"     Total events: {service['total_events_processed']}")
        if 'queue_size' in service:
            print(f"     Queue size: {service['queue_size']}")
    
    print("\n=== Example completed ===")
    print("Check the logs/ql-tracker.jsonl file for stored events!")
    
    # Shutdown services
    print("\nShutting down services...")
    shutdown()


if __name__ == "__main__":
    main() 