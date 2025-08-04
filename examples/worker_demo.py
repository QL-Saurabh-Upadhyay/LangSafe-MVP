"""
Comprehensive demo of the log worker functionality.

This example demonstrates how the log worker picks up logs every 3 seconds
and processes them through the batch logger in the background.
"""

import time
import random
from trackdecorator import track, initialize, get_stats


@track
def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


@track
def process_data(data: list) -> dict:
    """Process a list of data and return statistics."""
    if not data:
        raise ValueError("Data list cannot be empty")
    
    return {
        "count": len(data),
        "sum": sum(data),
        "average": sum(data) / len(data),
        "min": min(data),
        "max": max(data)
    }


@track
def simulate_work(duration: float) -> str:
    """Simulate some work for a given duration."""
    time.sleep(duration)
    return f"Work completed in {duration:.2f} seconds"


def main():
    """Main function to demonstrate log worker functionality."""
    print("🚀 Starting QL Tracker Log Worker Demo")
    print("=" * 50)
    
    # Initialize services with log worker
    initializer = initialize(
        config_path="trackconfig.toml",
        auto_start=True
    )
    
    print("✅ QL Tracker initialized successfully!")
    print("🔄 Log worker will process logs every 3 seconds...")
    print("=" * 50)
    
    # Phase 1: Initial operations
    print("📝 Phase 1: Performing initial operations...")
    
    try:
        result1 = calculate_fibonacci(5)
        print(f"  calculate_fibonacci(5) = {result1}")
    except Exception as e:
        print(f"  calculate_fibonacci(5) raised: {e}")
    
    try:
        result2 = process_data([1, 2, 3, 4, 5])
        print(f"  process_data([1,2,3,4,5]) = {result2}")
    except Exception as e:
        print(f"  process_data([1,2,3,4,5]) raised: {e}")
    
    try:
        result3 = process_data([])
        print(f"  process_data([]) = {result3}")
    except Exception as e:
        print(f"  process_data([]) raised: {e}")
    
    print("\n⏳ Waiting for first processing cycle...")
    time.sleep(4)  # Wait for first 3-second cycle
    
    # Phase 2: More operations
    print("\n📝 Phase 2: Performing more operations...")
    
    for i in range(3):
        try:
            data = [random.randint(1, 100) for _ in range(random.randint(3, 8))]
            result = process_data(data)
            print(f"  process_data({data}) = {result}")
        except Exception as e:
            print(f"  process_data raised: {e}")
    
    print("\n⏳ Waiting for second processing cycle...")
    time.sleep(4)  # Wait for second 3-second cycle
    
    # Phase 3: Simulate work
    print("\n📝 Phase 3: Simulating work...")
    
    for i in range(2):
        try:
            duration = random.uniform(0.1, 0.3)
            result = simulate_work(duration)
            print(f"  {result}")
        except Exception as e:
            print(f"  simulate_work raised: {e}")
    
    print("\n⏳ Waiting for final processing cycle...")
    time.sleep(4)  # Wait for final 3-second cycle
    
    # Show final statistics
    print("\n" + "=" * 50)
    print("📊 Final Statistics:")
    final_stats = get_stats()
    
    print(f"  Initialized: {final_stats.get('initialized', 'N/A')}")
    print(f"  Running: {final_stats.get('running', 'N/A')}")
    print(f"  Service Count: {final_stats.get('service_count', 'N/A')}")
    
    services = final_stats.get('services', [])
    for i, service in enumerate(services):
        print(f"\n  Service {i+1} ({service.get('type', 'Unknown')}):")
        for key, value in service.items():
            if key != 'type':
                print(f"    {key}: {value}")
    
    print("\n🛑 Shutting down...")
    initializer.stop()
    print("✅ Demo completed!")


if __name__ == "__main__":
    main() 