# Write a std_dev() Function (Using variance())
# Write your solution below. Run this file to test: python exercises/03_easy_std_dev_function.py

def mean(data):
    """Provided utility -- already implemented, no need to change."""
    return sum(data) / len(data)


def variance(data):
    """Provided utility -- already implemented, no need to change."""
    avg = mean(data)
    return sum((x - avg) ** 2 for x in data) / len(data)


def std_dev(data):
    """Return the population standard deviation of a list of numbers.

    TODO: implement using variance(data) internally.
    """
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    import random
    import statistics

    random.seed(2)
    for _ in range(5):
        sample = [random.uniform(-50, 50) for _ in range(random.randint(2, 20))]
        assert math.isclose(std_dev(sample), statistics.pstdev(sample)), f"std_dev({sample}) is wrong"
    print("PASS")
