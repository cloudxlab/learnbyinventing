# Recursive Sum of a List
# Write your solution below. Run this file to test: python exercises/01_easy_recursive_sum.py

def recursive_sum(data):
    """Return the sum of a list of numbers, using recursion (no loops, no sum())."""
    # TODO: base case -- what should an empty list sum to?
    # TODO: recursive case -- combine data[0] with recursive_sum(data[1:])
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import random

    random.seed(4)
    for _ in range(5):
        sample = [random.randint(-50, 50) for _ in range(random.randint(0, 10))]
        assert recursive_sum(sample) == sum(sample), f"recursive_sum({sample}) is wrong"
    print("PASS")
