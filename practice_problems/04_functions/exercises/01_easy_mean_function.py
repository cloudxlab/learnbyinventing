# Write a mean() Function
# Write your solution below. Run this file to test: python exercises/01_easy_mean_function.py

def mean(data):
    """Return the arithmetic mean of a list of numbers."""
    # TODO: implement
    pass


# quick manual check while developing -- feel free to change this
sample = [4, 8, 6, 5, 3]
print(mean(sample))


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    import random
    import statistics

    random.seed(0)
    for _ in range(5):
        sample = [random.uniform(-100, 100) for _ in range(random.randint(1, 20))]
        assert math.isclose(mean(sample), statistics.mean(sample)), f"mean({sample}) is wrong"
    print("PASS")
