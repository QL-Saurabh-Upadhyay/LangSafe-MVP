#!/usr/bin/env python3
"""
Example usage of the @track decorator.

This example demonstrates how to use the @track decorator on both
synchronous and asynchronous functions.
"""

import asyncio
from typing import List

from trackdecorator import track



@track
def calculate_sum(numbers: List[int]) -> int:
    """Calculate the sum of a list of numbers."""
    return sum(numbers)


@track
async def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers (may raise an exception)."""
    await asyncio.sleep(10)
    return a / b





def main() -> None:
    """Main function demonstrating the @track decorator."""
    print("=== QL Tracker Example ===\n")
    
    # Test synchronous functions
    print("Testing synchronous functions:")
    print("-" * 40)
    
    # Function with list argument
    numbers = [1, 2, 3, 4, 5]
    sum_result = calculate_sum(numbers)
    print(f"Sum of {numbers} = {sum_result}\n")
    
    # Function that raises an exception
    try:
        result = asyncio.run(divide_numbers(10, 5))
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Caught expected Exception: {e}\n")
    
    print("=== Example completed ===")


if __name__ == "__main__":
    main() 