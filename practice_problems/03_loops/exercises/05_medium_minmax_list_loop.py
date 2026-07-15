# Min-Max Normalize an Entire List
# Write your solution below. Run this file to test: python exercises/05_medium_minmax_list_loop.py

data = [12, 15, 14, 10, 100, 13, 11, 16, 9, 14]

# TODO: find the minimum and maximum of data
min_val = None
max_val = None

# TODO: loop through data and build a list of min-max scaled values
scaled_data = []


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected_min, expected_max = min(data), max(data)
    expected_scaled = [(x - expected_min) / (expected_max - expected_min) for x in data]

    assert min_val == expected_min and max_val == expected_max, "min_val/max_val are wrong"
    assert len(scaled_data) == len(data), "scaled_data has the wrong length"
    assert all(math.isclose(a, b) for a, b in zip(scaled_data, expected_scaled)), \
        f"Expected {expected_scaled}, got {scaled_data}"
    print("PASS")
