"""
Analytics Demo for QL Tracker.

This example demonstrates how to use the analytics functions
to create dashboard data from the comprehensive log schema.
"""

import json
import time
from trackdecorator import track, initialize, get_stats
from trackdecorator.schema.log_schema import create_dashboard_analytics, LogEvent


@track
def generate_sample_data() -> list:
    """Generate sample data for analytics demo."""
    return [{"id": i, "value": i * 2} for i in range(10)]


@track
def process_analytics(data: list) -> dict:
    """Process analytics on sample data."""
    if not data:
        raise ValueError("Data cannot be empty")
    
    return {
        "count": len(data),
        "sum": sum(item.get("value", 0) for item in data),
        "average": sum(item.get("value", 0) for item in data) / len(data),
        "max": max(item.get("value", 0) for item in data),
        "min": min(item.get("value", 0) for item in data)
    }


@track
def simulate_api_call(endpoint: str, timeout: float = 1.0) -> dict:
    """Simulate an API call with configurable timeout."""
    time.sleep(timeout)
    
    if "error" in endpoint.lower():
        raise ConnectionError(f"API call failed for {endpoint}")
    
    return {
        "endpoint": endpoint,
        "status": "success",
        "response_time": timeout,
        "data": {"result": "api_response"}
    }


@track
def database_operation(operation: str, table: str, data: dict = None) -> dict:
    """Simulate database operations."""
    time.sleep(0.1)  # Simulate database latency
    
    if operation not in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
        raise ValueError(f"Invalid operation: {operation}")
    
    return {
        "operation": operation,
        "table": table,
        "affected_rows": len(data) if data else 0,
        "status": "success"
    }


def analyze_logs_from_file(log_file_path: str) -> dict:
    """Analyze logs from a JSONL file."""
    log_events = []
    
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                if line.strip():
                    event_data = json.loads(line)
                    # Convert back to LogEvent for analysis
                    # Note: This is a simplified conversion for demo purposes
                    log_events.append(event_data)
        
        # Create analytics
        analytics = create_dashboard_analytics_from_dicts(log_events)
        return analytics
        
    except Exception as e:
        print(f"Error analyzing logs: {e}")
        return {}


def create_dashboard_analytics_from_dicts(log_events: list) -> dict:
    """Create dashboard analytics from a list of log event dictionaries."""
    if not log_events:
        return {}
    
    total_events = len(log_events)
    successful_events = sum(1 for event in log_events if event.get('is_success', False))
    failed_events = total_events - successful_events
    
    # Performance metrics
    execution_times = []
    for event in log_events:
        performance = event.get('performance', {})
        if performance and 'execution_time_ms' in performance:
            execution_times.append(performance['execution_time_ms'])
    
    avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
    max_execution_time = max(execution_times) if execution_times else 0
    min_execution_time = min(execution_times) if execution_times else 0
    
    # Function distribution
    function_counts = {}
    for event in log_events:
        func_name = event.get('function_name', 'unknown')
        function_counts[func_name] = function_counts.get(func_name, 0) + 1
    
    # Error analysis
    error_types = {}
    for event in log_events:
        exception = event.get('exception')
        if exception:
            error_type = exception.get('error_type', 'unknown')
            error_types[error_type] = error_types.get(error_type, 0) + 1
    
    # Category distribution
    category_counts = {}
    for event in log_events:
        category = event.get('execution_category', 'unknown')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Business value distribution
    business_value_counts = {}
    for event in log_events:
        value = event.get('business_value', 'unknown')
        business_value_counts[value] = business_value_counts.get(value, 0) + 1
    
    # User API key analysis
    api_key_counts = {}
    for event in log_events:
        api_key = event.get('user_api_key', 'anonymous')
        api_key_counts[api_key] = api_key_counts.get(api_key, 0) + 1
    
    # Session analysis
    session_counts = {}
    for event in log_events:
        session_id = event.get('session_id', 'no_session')
        session_counts[session_id] = session_counts.get(session_id, 0) + 1
    
    return {
        "summary": {
            "total_events": total_events,
            "successful_events": successful_events,
            "failed_events": failed_events,
            "success_rate": (successful_events / total_events * 100) if total_events > 0 else 0,
        },
        "performance": {
            "average_execution_time_ms": avg_execution_time,
            "max_execution_time_ms": max_execution_time,
            "min_execution_time_ms": min_execution_time,
            "total_execution_time_ms": sum(execution_times),
        },
        "functions": {
            "top_functions": sorted(function_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "function_count": len(function_counts),
        },
        "errors": {
            "error_types": error_types,
            "total_errors": failed_events,
        },
        "categories": {
            "category_distribution": category_counts,
        },
        "business_value": {
            "value_distribution": business_value_counts,
        },
        "users": {
            "api_key_distribution": api_key_counts,
            "unique_users": len(api_key_counts),
        },
        "sessions": {
            "session_distribution": session_counts,
            "unique_sessions": len(session_counts),
        }
    }


def main():
    """Main function to demonstrate analytics capabilities."""
    print("🚀 QL Tracker Analytics Demo")
    print("=" * 50)
    
    # Initialize tracker
    initializer = initialize(
        api_key="analytics_demo_key",
        config_path="trackconfig.toml",
        auto_start=True
    )
    
    print("✅ Tracker initialized for analytics demo")
    print("=" * 50)
    
    # Perform various operations to generate logs
    print("📝 Generating sample data and operations...")
    
    # Successful operations
    try:
        data = generate_sample_data()
        print(f"  Generated {len(data)} sample records")
        
        analytics = process_analytics(data)
        print(f"  Analytics result: {analytics}")
        
        api_result = simulate_api_call("/api/data", 0.5)
        print(f"  API call result: {api_result}")
        
        db_result = database_operation("SELECT", "users", {"id": 1, "name": "John"})
        print(f"  Database operation: {db_result}")
        
    except Exception as e:
        print(f"  Error in operations: {e}")
    
    # Operations with errors
    try:
        simulate_api_call("error_endpoint")
    except Exception as e:
        print(f"  Expected API error: {e}")
    
    try:
        database_operation("INVALID", "users")
    except Exception as e:
        print(f"  Expected DB error: {e}")
    
    # Wait for processing
    print("\n⏳ Waiting for log worker to process events...")
    time.sleep(4)
    
    # Analyze the logs
    print("\n📊 Analyzing logs...")
    analytics = analyze_logs_from_file("logs/ql-tracker.jsonl")
    
    if analytics:
        print("\n" + "=" * 50)
        print("📈 Dashboard Analytics Results:")
        print("=" * 50)
        
        # Summary
        summary = analytics.get("summary", {})
        print(f"\n📋 Summary:")
        print(f"  Total Events: {summary.get('total_events', 0)}")
        print(f"  Successful: {summary.get('successful_events', 0)}")
        print(f"  Failed: {summary.get('failed_events', 0)}")
        print(f"  Success Rate: {summary.get('success_rate', 0):.1f}%")
        
        # Performance
        performance = analytics.get("performance", {})
        print(f"\n⚡ Performance:")
        print(f"  Avg Execution Time: {performance.get('average_execution_time_ms', 0):.2f}ms")
        print(f"  Max Execution Time: {performance.get('max_execution_time_ms', 0):.2f}ms")
        print(f"  Min Execution Time: {performance.get('min_execution_time_ms', 0):.2f}ms")
        
        # Functions
        functions = analytics.get("functions", {})
        print(f"\n🔧 Functions:")
        print(f"  Unique Functions: {functions.get('function_count', 0)}")
        print(f"  Top Functions:")
        for func_name, count in functions.get("top_functions", [])[:5]:
            print(f"    {func_name}: {count} calls")
        
        # Errors
        errors = analytics.get("errors", {})
        print(f"\n❌ Errors:")
        print(f"  Total Errors: {errors.get('total_errors', 0)}")
        for error_type, count in errors.get("error_types", {}).items():
            print(f"    {error_type}: {count}")
        
        # Categories
        categories = analytics.get("categories", {})
        print(f"\n📂 Categories:")
        for category, count in categories.get("category_distribution", {}).items():
            print(f"    {category}: {count}")
        
        # Business Value
        business_value = analytics.get("business_value", {})
        print(f"\n💼 Business Value:")
        for value, count in business_value.get("value_distribution", {}).items():
            print(f"    {value}: {count}")
        
        # Users
        users = analytics.get("users", {})
        print(f"\n👥 Users:")
        print(f"  Unique Users: {users.get('unique_users', 0)}")
        for api_key, count in users.get("api_key_distribution", {}).items():
            print(f"    {api_key}: {count} events")
        
        # Sessions
        sessions = analytics.get("sessions", {})
        print(f"\n🆔 Sessions:")
        print(f"  Unique Sessions: {sessions.get('unique_sessions', 0)}")
        for session_id, count in sessions.get("session_distribution", {}).items():
            if session_id and session_id != "no_session":
                print(f"    {session_id[:8]}...: {count} events")
            else:
                print(f"    {session_id}: {count} events")
    
    print("\n🛑 Shutting down...")
    initializer.stop()
    print("✅ Analytics demo completed!")


if __name__ == "__main__":
    main() 