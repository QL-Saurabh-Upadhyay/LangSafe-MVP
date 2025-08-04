#!/usr/bin/env python3
"""
Collaboration Example - How to use the @track decorator when cloning from GitHub.

This example demonstrates the complete setup process for using the @track decorator
in a collaborative environment after cloning the repository from GitHub.
"""

import asyncio
import time
from typing import List, Dict, Any

# Import the track decorator and initialization functions
from ql_tracker import track, initialize, shutdown, get_stats, get_initializer


def setup_tracker():
    """Initialize the QL Tracker services."""
    print("🔧 Setting up QL Tracker...")
    
    # Initialize with optional API key and host (using None for local-only mode)
    initializer = initialize(
        api_key=None,  # Optional: Replace with your actual API key
        host=None,  # Optional: Replace with your actual host (None for local-only)
        config_path="trackconfig.toml"  # Optional: Path to your config file
    )
    
    print(f"✅ Services initialized: {initializer.is_initialized()}")
    print(f"✅ Services running: {initializer.is_running()}")
    print(f"✅ API Key configured: {initializer.get_api_key() is not None}")
    print(f"✅ Host configured: {initializer.get_host()}")
    
    return initializer


@track
def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number with tracking."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


@track
def process_data(items: List[int]) -> List[int]:
    """Process a list of numbers with tracking."""
    time.sleep(0.1)  # Simulate processing time
    return [x * 2 for x in items]


@track
async def fetch_data_async(url: str) -> Dict[str, Any]:
    """Fetch data asynchronously with tracking."""
    await asyncio.sleep(0.2)  # Simulate async work
    return {"url": url, "data": "sample data", "timestamp": time.time()}


@track
def function_with_error() -> None:
    """A function that raises an exception to demonstrate error tracking."""
    raise ValueError("This is a test error for demonstration purposes")


class DataProcessor:
    """Example class with tracked methods."""
    
    def __init__(self, name: str):
        self.name = name
    
    @track
    def process_batch(self, data: List[str]) -> List[str]:
        """Process a batch of data with tracking."""
        time.sleep(0.1)
        return [f"{self.name}: {item.upper()}" for item in data]
    
    @track
    async def async_process_batch(self, data: List[str]) -> List[str]:
        """Process a batch of data asynchronously with tracking."""
        await asyncio.sleep(0.2)
        return [f"{self.name}: {item.lower()}" for item in data]


def demonstrate_basic_tracking():
    """Demonstrate basic function tracking."""
    print("\n📊 Basic Function Tracking Examples:")
    print("-" * 50)
    
    # Simple function tracking
    result = calculate_fibonacci(5)
    print(f"Fibonacci(5) = {result}")
    
    # List processing
    data = [1, 2, 3, 4, 5]
    processed = process_data(data)
    print(f"Processed data: {processed}")


async def demonstrate_async_tracking():
    """Demonstrate async function tracking."""
    print("\n🔄 Async Function Tracking Examples:")
    print("-" * 50)
    
    # Async function tracking
    result = await fetch_data_async("https://api.example.com/data")
    print(f"Fetched data: {result}")


async def demonstrate_class_tracking():
    """Demonstrate class method tracking."""
    print("\n🏗️ Class Method Tracking Examples:")
    print("-" * 50)
    
    processor = DataProcessor("TestProcessor")
    
    # Sync method tracking
    result = processor.process_batch(["hello", "world", "python"])
    print(f"Processed batch: {result}")
    
    # Async method tracking
    async_result = await processor.async_process_batch(["HELLO", "WORLD", "PYTHON"])
    print(f"Async processed batch: {async_result}")


def demonstrate_error_tracking():
    """Demonstrate error tracking."""
    print("\n❌ Error Tracking Examples:")
    print("-" * 50)
    
    try:
        function_with_error()
    except ValueError as e:
        print(f"Caught expected error: {e}")


def show_service_statistics():
    """Show current service statistics."""
    print("\n📈 Service Statistics:")
    print("-" * 50)
    
    stats = get_stats()
    print(f"Services initialized: {stats['initialized']}")
    print(f"Services running: {stats['running']}")
    print(f"API Key configured: {stats['api_key_configured']}")
    print(f"Host configured: {stats['host_configured']}")
    print(f"Service count: {stats['service_count']}")
    
    for service in stats['services']:
        print(f"\nService: {service['type']}")
        print(f"  Running: {service['running']}")
        if 'batch_count' in service:
            print(f"  Batches processed: {service['batch_count']}")
        if 'total_events_processed' in service:
            print(f"  Total events: {service['total_events_processed']}")
        if 'queue_size' in service:
            print(f"  Queue size: {service['queue_size']}")


def demonstrate_configuration():
    """Demonstrate configuration options."""
    print("\n⚙️ Configuration Examples:")
    print("-" * 50)
    
    from ql_tracker import get_config, load_config
    
    # Get current configuration
    config = get_config()
    print(f"Logging enabled: {config.enable_logging}")
    print(f"Pretty print: {config.pretty_print}")
    print(f"Log to file: {config.log_to_file}")
    print(f"Log level: {config.log_level}")
    
    # Load custom configuration (if available)
    try:
        load_config("trackconfig.toml")
        print("✅ Custom configuration loaded successfully")
    except FileNotFoundError:
        print("ℹ️ No custom configuration file found, using defaults")


async def main():
    """Main function demonstrating the complete setup and usage."""
    print("🚀 QL Tracker - Collaboration Setup Example")
    print("=" * 60)
    
    # Step 1: Setup the tracker
    initializer = setup_tracker()
    
    # Step 2: Demonstrate various tracking scenarios
    demonstrate_basic_tracking()
    await demonstrate_async_tracking()
    await demonstrate_class_tracking()
    demonstrate_error_tracking()
    
    # Step 3: Show configuration options
    demonstrate_configuration()
    
    # Step 4: Wait for background processing
    print("\n⏳ Waiting for background processing...")
    time.sleep(3)
    
    # Step 5: Show final statistics
    show_service_statistics()
    
    # Step 6: Graceful shutdown
    print("\n🛑 Shutting down services...")
    shutdown()
    
    print("\n✅ Example completed successfully!")
    print("📁 Check the logs/ql-tracker.jsonl file for stored events!")
    print("\n💡 Tips for collaboration:")
    print("   - Always initialize services before using @track")
    print("   - Use virtual environments to avoid conflicts")
    print("   - Configure logging appropriately for your environment")
    print("   - Monitor service statistics in production")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 