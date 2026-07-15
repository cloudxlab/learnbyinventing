# Compute Covariance Between Two Lists
# Write your solution below. Run this file to test: python exercises/08_hard_covariance_loop.py

x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]

# TODO: compute x_mean and y_mean
x_mean = None
y_mean = None

# TODO: loop through x and y together to accumulate covariance
covariance = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    import statistics

    expected_x_mean, expected_y_mean = statistics.mean(x), statistics.mean(y)
    expected_cov = sum((xi - expected_x_mean) * (yi - expected_y_mean) for xi, yi in zip(x, y)) / len(x)

    assert math.isclose(x_mean, expected_x_mean) and math.isclose(y_mean, expected_y_mean), \
        "x_mean/y_mean are wrong"
    assert math.isclose(covariance, expected_cov), f"Expected {expected_cov}, got {covariance}"
    print("PASS")
