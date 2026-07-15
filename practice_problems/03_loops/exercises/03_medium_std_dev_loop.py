# Compute the Standard Deviation
# Write your solution below. Run this file to test: python exercises/03_medium_std_dev_loop.py

data = [12, 15, 14, 10, 100, 13, 11, 16, 9, 14]

# TODO: compute the mean with a loop
mean_value = None

# TODO: compute the variance (average squared deviation) with a loop
variance = None

# TODO: compute the standard deviation
std_dev = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    import statistics

    expected_mean = statistics.mean(data)
    expected_var = statistics.pvariance(data)
    expected_std = statistics.pstdev(data)

    assert math.isclose(mean_value, expected_mean), f"mean_value: expected {expected_mean}, got {mean_value}"
    assert math.isclose(variance, expected_var), f"variance: expected {expected_var}, got {variance}"
    assert math.isclose(std_dev, expected_std), f"std_dev: expected {expected_std}, got {std_dev}"
    print("PASS")
