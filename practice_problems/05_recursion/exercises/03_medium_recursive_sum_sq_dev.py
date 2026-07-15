# Recursive Sum of Squared Deviations (for Variance)
# Write your solution below. Run this file to test: python exercises/03_medium_recursive_sum_sq_dev.py

def recursive_sum_sq_dev(data, mean_value):
    """Recursively compute sum((x - mean_value) ** 2 for x in data)."""
    # TODO: base case
    # TODO: recursive case
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    import random

    random.seed(6)
    for _ in range(5):
        sample = [random.uniform(-20, 20) for _ in range(random.randint(0, 8))]
        m = random.uniform(-5, 5)
        expected = sum((x - m) ** 2 for x in sample)
        assert math.isclose(recursive_sum_sq_dev(sample, m), expected), \
            f"recursive_sum_sq_dev({sample}, {m}) is wrong"
    print("PASS")
