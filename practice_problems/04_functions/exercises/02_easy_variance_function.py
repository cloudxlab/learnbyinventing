# Write a variance() Function (Using mean())
# Write your solution below. Run this file to test: python exercises/02_easy_variance_function.py

def mean(data):
    """Provided utility -- already implemented, no need to change."""
    return sum(data) / len(data)


def variance(data):
    """Return the population variance of a list of numbers.

    TODO: implement using mean(data) internally (call your mean()
    function -- don't recompute the mean with raw sum()/len() again).
    """
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    import random
    import statistics

    random.seed(1)
    for _ in range(5):
        sample = [random.uniform(-50, 50) for _ in range(random.randint(2, 20))]
        assert math.isclose(variance(sample), statistics.pvariance(sample)), f"variance({sample}) is wrong"
    print("PASS")
