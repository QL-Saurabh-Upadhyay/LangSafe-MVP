"""
Example demonstrating the log worker functionality.

This example shows how the log worker picks up logs every 3 seconds
and processes them through the batch logger in the background.
"""
import time

from ql_tracker import track, initialize, get_stats


@track
def subtract(a, b): return a - b

@track
def power(a, b): return a ** b

@track
def modulus(a, b): return a % b

@track
def floor_divide(a, b): return a // b

@track
def concatenate_strings(a, b): return a + b

@track
def reverse_string(s): return s[::-1]

@track
def divide_with_check(a: float, b: float) -> float:
    """Divide two numbers and raise ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b

@track
def parse_int(value: str) -> int:
    """Parse a string to an integer and raise ValueError if invalid."""
    return int(value)


@track
def is_even(n): return n % 2 == 0

@track
def factorial(n): return 1 if n == 0 else n * factorial(n - 1)

@track
def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)

@track
def max_of_list(lst): return max(lst)

@track
def min_of_list(lst): return min(lst)

@track
def sum_of_list(lst): return sum(lst)

@track
def average_of_list(lst): return sum(lst) / len(lst)

@track
def sort_list(lst): return sorted(lst)

@track
def unique_elements(lst): return list(set(lst))

@track
def to_uppercase(s): return s.upper()

@track
def to_lowercase(s): return s.lower()

@track
def capitalize_string(s): return s.capitalize()

@track
def is_palindrome(s): return s == s[::-1]

@track
def count_vowels(s): return sum(c in 'aeiouAEIOU' for c in s)

@track
def square_list(lst): return [x**2 for x in lst]

@track
def cube_list(lst): return [x**3 for x in lst]

@track
def filter_even(lst): return [x for x in lst if x % 2 == 0]

@track
def filter_odd(lst): return [x for x in lst if x % 2 != 0]

@track
def map_increment(lst): return [x+1 for x in lst]

@track
def map_decrement(lst): return [x-1 for x in lst]

@track
def combine_dicts(d1, d2): return {**d1, **d2}

@track
def get_keys(d): return list(d.keys())

@track
def get_values(d): return list(d.values())

@track
def get_items(d): return list(d.items())

@track
def dict_from_lists(keys, values): return dict(zip(keys, values))

@track
def check_key(d, key): return key in d

@track
def square(n): return n * n

@track
def cube(n): return n ** 3

@track
def double(n): return n * 2

@track
def triple(n): return n * 3

@track
def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

@track
def gcd(a, b):
    while b: a, b = b, a % b
    return a

@track
def lcm(a, b):
    def gcd(x, y):
        while y: x, y = y, x % y
        return x
    return abs(a * b) // gcd(a, b)

@track
def repeat_string(s, times): return s * times

@track
def flatten_list(lst): return [item for sublist in lst for item in sublist]

@track
def list_intersection(a, b): return list(set(a) & set(b))

@track
def list_union(a, b): return list(set(a) | set(b))

@track
def list_difference(a, b): return list(set(a) - set(b))

@track
def list_symmetric_difference(a, b): return list(set(a) ^ set(b))

@track
def count_occurrences(lst, item): return lst.count(item)

@track
def zip_lists(a, b): return list(zip(a, b))

@track
def unzip_list(z): return list(map(list, zip(*z)))

@track
def index_of(lst, value): return lst.index(value) if value in lst else -1

@track
def replace_in_string(s, old, new): return s.replace(old, new)

@track
def split_string(s, delimiter=" "): return s.split(delimiter)


def main():
    # Initialize QL Tracker
    initializer = initialize(
        host="https://689065c01d3e57320941af16--idyllic-empanada-76b277.netlify.app",
        api_key="sfkasdkfmaksdmfkadmf",
        config_path="trackconfig.toml",
        auto_start=True
    )

    try:
        # Perform operations with all the tracked functions
        subtract(10, 4)
        power(2, 10)
        modulus(10, 3)
        floor_divide(20, 6)
        concatenate_strings("hello", "world")
        reverse_string("tracker")
        is_even(42)
        try:
            divide_with_check(10, 0)
        except Exception as e:
            print(f"Handled exception from divide_with_check: {e}")

        try:
            parse_int("not-a-number")
        except Exception as e:
            print(f"Handled exception from parse_int: {e}")

        factorial(6)
        fibonacci(7)
        max_of_list([1, 5, 9])
        min_of_list([4, 0, -1])
        sum_of_list([2, 4, 6])
        average_of_list([1, 2, 3, 4, 5])
        sort_list([5, 2, 8])
        unique_elements([1, 2, 2, 3])
        to_uppercase("hello")
        to_lowercase("WORLD")
        capitalize_string("tracker")
        is_palindrome("madam")
        count_vowels("Hello World")
        square_list([1, 2, 3])
        cube_list([1, 2, 3])
        filter_even([1, 2, 3, 4])
        filter_odd([1, 2, 3, 4])
        map_increment([10, 20])
        map_decrement([10, 20])
        combine_dicts({"a": 1}, {"b": 2})
        get_keys({"x": 10, "y": 20})
        get_values({"x": 10, "y": 20})
        get_items({"x": 10, "y": 20})
        dict_from_lists(["a", "b"], [1, 2])
        check_key({"k": 5}, "k")
        square(9)
        cube(3)
        double(8)
        triple(4)
        is_prime(29)
        gcd(48, 18)
        lcm(5, 3)
        repeat_string("hi", 3)
        flatten_list([[1, 2], [3, 4]])
        list_intersection([1, 2], [2, 3])
        list_union([1, 2], [2, 3])
        list_difference([1, 2], [2])
        list_symmetric_difference([1, 2], [2, 3])
        count_occurrences([1, 2, 2, 3], 2)
        zipped = zip_lists([1, 2], ["a", "b"])
        unzip_list(zipped)
        index_of([10, 20, 30], 20)
        replace_in_string("hello world", "world", "tracker")
        split_string("a,b,c", delimiter=",")

        # Let log worker flush logs in background
        for i in range(5):
            time.sleep(1)
            stats = get_stats()
            print(f"[{i+1}s] Queue size: {stats.get('services', [{}])[0].get('queue_size', 'N/A')}")

    finally:
        print("Final tracker stats:")
        print(get_stats())
        initializer.stop()


if __name__ == "__main__":
    main()