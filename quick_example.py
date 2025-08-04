#!/usr/bin/env python3
"""
Simple example of using the @track decorator.

Run this script to see the tracking in action.
"""

from ql_tracker import track, initialize, shutdown

# Initialize services
initialize()

@track
def add_numbers(a, b):
    """Add two numbers with tracking."""
    return a + b

@track
def multiply_numbers(a, b):
    """Multiply two numbers with tracking."""
    return a * b

def main():
    print("🧮 Testing @track decorator...")
    
    # Test some functions
    result1 = add_numbers(10, 5)
    print(f"10 + 5 = {result1}")
    
    result2 = multiply_numbers(4, 7)
    print(f"4 * 7 = {result2}")
    
    # Wait for background processing
    import time
    time.sleep(2)
    
    # Shutdown
    shutdown()
    print("✅ Example completed!")

if __name__ == "__main__":
    main()
