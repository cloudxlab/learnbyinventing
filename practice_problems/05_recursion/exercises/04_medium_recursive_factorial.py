# Recursive Factorial (for Counting Outcomes)
# Write your solution below. Run this file to test: python exercises/04_medium_recursive_factorial.py

def factorial(n):
    """Return n! using recursion."""
    # TODO: base case
    # TODO: recursive case
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    for n in range(0, 10):
        assert factorial(n) == math.factorial(n), f"factorial({n}) is wrong"
    print("PASS")
