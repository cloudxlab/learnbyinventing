# Compose find_outliers() From Your Stats Functions
# Write your solution below. Run this file to test: python exercises/04_medium_find_outliers_function.py

def mean(data):
    """Provided utility -- already implemented, no need to change."""
    return sum(data) / len(data)


def variance(data):
    """Provided utility -- already implemented, no need to change."""
    avg = mean(data)
    return sum((x - avg) ** 2 for x in data) / len(data)


def std_dev(data):
    """Provided utility -- already implemented, no need to change."""
    return variance(data) ** 0.5


def find_outliers(data, k=2):
    """Return the values in `data` whose distance from the mean exceeds k * std_dev(data).

    TODO: implement using mean(data) and std_dev(data).
    """
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import random
    import statistics

    random.seed(3)
    for _ in range(5):
        base = [random.uniform(0, 20) for _ in range(8)]
        data = base + [500]  # inject an obvious outlier
        m, s = statistics.mean(data), statistics.pstdev(data)
        expected = [x for x in data if abs(x - m) > 2 * s]
        assert find_outliers(data, k=2) == expected, f"find_outliers({data}) is wrong"
    print("PASS")
