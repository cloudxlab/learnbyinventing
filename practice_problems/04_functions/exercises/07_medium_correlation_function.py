# Write a correlation() Function (Using Covariance & Std Dev)
# Write your solution below. Run this file to test: python exercises/07_medium_correlation_function.py

def mean(data):
    """Provided utility -- already implemented, no need to change."""
    return sum(data) / len(data)


def covariance(x, y):
    """Provided utility -- already implemented, no need to change."""
    mx, my = mean(x), mean(y)
    return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / len(x)


def std_dev(data):
    """Provided utility -- already implemented, no need to change."""
    avg = mean(data)
    return (sum((v - avg) ** 2 for v in data) / len(data)) ** 0.5


def correlation(x, y):
    """Return the Pearson correlation coefficient between x and y.

    TODO: implement using covariance(x, y) and std_dev(x), std_dev(y).
    """
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / len(x)
    sx = (sum((v - mx) ** 2 for v in x) / len(x)) ** 0.5
    sy = (sum((v - my) ** 2 for v in y) / len(y)) ** 0.5
    expected = cov / (sx * sy)

    assert math.isclose(correlation(x, y), expected), f"Expected {expected}, got {correlation(x, y)}"

    x2, y2 = [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]
    assert correlation(x2, y2) < 0, "correlation of perfectly inverse data should be negative"
    print("PASS")
