"""
Example demonstrating the log worker functionality.

This example shows how the log worker picks up logs every 3 seconds
and processes them through the batch logger in the background.
"""

import time
from trackdecorator import track, initialize, get_stats


@track
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@track
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@track
def divide_numbers(a: int, b: int) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def main():
    """Main function to demonstrate log worker functionality."""
    print("Initializing QL Tracker with log worker...")
    
    # Initialize services with log worker
    initializer = initialize(
        host="https://localhost:3000",
        api_key="sfkasdkfmaksdmfkadmf",
        config_path="trackconfig.toml",
        auto_start=True
    )
    
    print("QL Tracker initialized successfully!")
    print("Log worker will process logs every 3 seconds...")
    print("-" * 50)
    
    # Perform some tracked operations
    print("Performing tracked operations...")
    
    # Normal operations
    result1 = add_numbers(5, 3)
    print(f"add_numbers(5, 3) = {result1}")
    
    result2 = multiply_numbers(4, 7)
    print(f"multiply_numbers(4, 7) = {result2}")
    
    # Operation that might raise an exception
    try:
        result3 = divide_numbers(10, 2)
        print(f"divide_numbers(10, 2) = {result3}")
    except Exception as e:
        print(f"divide_numbers(10, 2) raised: {e}")
    
    try:
        result4 = divide_numbers(10, 0)
        print(f"divide_numbers(10, 0) = {result4}")
    except Exception as e:
        print(f"divide_numbers(10, 0) raised: {e}")
    
    print("-" * 50)
    print("Waiting for log worker to process events...")
    
    # Wait for the worker to process events
    for i in range(5):
        time.sleep(1)
        stats = get_stats()
        print(f"After {i+1}s - Queue size: {stats.get('services', [{}])[0].get('queue_size', 'N/A')}")
    
    print("-" * 50)
    print("Final statistics:")
    final_stats = get_stats()
    for key, value in final_stats.items():
        print(f"  {key}: {value}")
    
    print("\nShutting down...")
    initializer.stop()


if __name__ == "__main__":
    main() 