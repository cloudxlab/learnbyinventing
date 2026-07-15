# Sum of Squared Deviations
# Write your solution below. Run this file to test: python exercises/02_easy_sum_sq_dev_loop.py

data = [12, 15, 14, 10, 100, 13, 11, 16, 9, 14]
mean_value = 21.4  # precomputed mean of `data`

# TODO: use a loop to compute the sum of squared deviations from the mean
sum_sq_dev = 0
# your loop here


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = sum((x - mean_value) ** 2 for x in data)
    assert math.isclose(sum_sq_dev, expected), f"Expected {expected}, got {sum_sq_dev}"
    print("PASS")
