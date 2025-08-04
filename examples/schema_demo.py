"""
Demo of the comprehensive log schema with API key mapping and analytics.

This example demonstrates the new schema that includes user API key mapping,
success status, and analytical fields for dashboard visualization.
"""

import time
import uuid
from trackdecorator import track, initialize, get_stats, get_initializer


@track
def calculate_complex_math(a: float, b: float, operation: str = "add") -> float:
    """Calculate complex mathematical operations."""
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")


@track
def process_user_data(user_id: str, data: dict) -> dict:
    """Process user data with business logic."""
    if not user_id:
        raise ValueError("User ID is required")
    
    # Simulate some processing
    time.sleep(0.1)
    
    return {
        "user_id": user_id,
        "processed": True,
        "data_count": len(data),
        "timestamp": time.time()
    }


@track
def fetch_api_data(endpoint: str, params: dict = None) -> dict:
    """Simulate API call with potential failure."""
    if not endpoint:
        raise ValueError("Endpoint is required")
    
    # Simulate API call
    time.sleep(0.2)
    
    # Simulate occasional failure
    if "error" in endpoint.lower():
        raise ConnectionError(f"Failed to connect to {endpoint}")
    
    return {
        "endpoint": endpoint,
        "status": "success",
        "data": {"result": "api_data"},
        "params": params or {}
    }


@track
def database_query(query: str, limit: int = 100) -> list:
    """Simulate database query."""
    if not query:
        raise ValueError("Query is required")
    
    # Simulate database operation
    time.sleep(0.15)
    
    return [{"id": i, "data": f"record_{i}"} for i in range(min(limit, 10))]


def main():
    """Main function to demonstrate the new schema."""
    print("🚀 QL Tracker Schema Demo")
    print("=" * 50)
    
    # Initialize with API key and session
    initializer = initialize(
        api_key="demo_api_key_12345",
        host="https://api.example.com",
        config_path="trackconfig.toml",
        auto_start=True
    )
    
    # Set session ID for tracking
    session_id = str(uuid.uuid4())
    initializer.set_session_id(session_id)
    
    print(f"✅ Initialized with API Key: {initializer.get_api_key()}")
    print(f"🆔 Session ID: {session_id}")
    print("=" * 50)
    
    # Demo 1: Successful operations
    print("📝 Demo 1: Successful Operations")
    print("-" * 30)
    
    try:
        result1 = calculate_complex_math(10, 5, "add")
        print(f"  calculate_complex_math(10, 5, 'add') = {result1}")
    except Exception as e:
        print(f"  calculate_complex_math raised: {e}")
    
    try:
        result2 = process_user_data("user123", {"name": "John", "age": 30})
        print(f"  process_user_data('user123', {{'name': 'John', 'age': 30}}) = {result2}")
    except Exception as e:
        print(f"  process_user_data raised: {e}")
    
    try:
        result3 = fetch_api_data("/api/users", {"limit": 10})
        print(f"  fetch_api_data('/api/users', {{'limit': 10}}) = {result3}")
    except Exception as e:
        print(f"  fetch_api_data raised: {e}")
    
    # Demo 2: Operations with errors
    print("\n📝 Demo 2: Operations with Errors")
    print("-" * 30)
    
    try:
        result4 = calculate_complex_math(10, 0, "divide")
        print(f"  calculate_complex_math(10, 0, 'divide') = {result4}")
    except Exception as e:
        print(f"  calculate_complex_math raised: {e}")
    
    try:
        result5 = process_user_data("", {"name": "John"})
        print(f"  process_user_data('', {{'name': 'John'}}) = {result5}")
    except Exception as e:
        print(f"  process_user_data raised: {e}")
    
    try:
        result6 = fetch_api_data("error_endpoint")
        print(f"  fetch_api_data('error_endpoint') = {result6}")
    except Exception as e:
        print(f"  fetch_api_data raised: {e}")
    
    # Demo 3: Database operations
    print("\n📝 Demo 3: Database Operations")
    print("-" * 30)
    
    try:
        result7 = database_query("SELECT * FROM users", 5)
        print(f"  database_query('SELECT * FROM users', 5) = {len(result7)} records")
    except Exception as e:
        print(f"  database_query raised: {e}")
    
    try:
        result8 = database_query("", 10)
        print(f"  database_query('', 10) = {result8}")
    except Exception as e:
        print(f"  database_query raised: {e}")
    
    # Wait for processing
    print("\n⏳ Waiting for log worker to process events...")
    time.sleep(4)
    
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
    print("✅ Schema demo completed!")


if __name__ == "__main__":
    main() 