# Min-Max Scale a Single Value
# Write your solution below. Run this file to test: python exercises/03_easy_minmax_single.py

x = 150
min_val = 100
max_val = 200

# TODO: min-max scale x into the [0, 1] range as a single expression
scaled = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = (x - min_val) / (max_val - min_val)
    assert scaled is not None, "scaled is still None -- fill in the expression above."
    assert math.isclose(scaled, expected), f"Expected {expected}, got {scaled}"
    print("PASS")
