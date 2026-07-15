# Compute the Mean With a Loop
# Write your solution below. Run this file to test: python exercises/01_easy_mean_via_loop.py

data = [12, 15, 14, 10, 100, 13, 11, 16, 9, 14]

# TODO: use a loop to accumulate the total, then divide by len(data)
total = 0
# your loop here

mean_value = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    import statistics

    expected = statistics.mean(data)
    assert mean_value is not None, "mean_value is still None."
    assert math.isclose(mean_value, expected), f"Expected {expected}, got {mean_value}"
    print("PASS")
