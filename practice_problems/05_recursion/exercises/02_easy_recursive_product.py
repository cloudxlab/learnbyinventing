# Recursive Product of a List (for Geometric Mean)
# Write your solution below. Run this file to test: python exercises/02_easy_recursive_product.py

def recursive_product(data):
    """Return the product of a list of numbers, using recursion."""
    # TODO: base case -- what should an empty list's product be?
    # TODO: recursive case -- combine data[0] with recursive_product(data[1:])
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    import random

    random.seed(5)
    for _ in range(5):
        sample = [random.randint(1, 5) for _ in range(random.randint(0, 6))]
        assert math.isclose(recursive_product(sample), math.prod(sample)), f"recursive_product({sample}) is wrong"
    print("PASS")
