# Min-Max Normalize Without Dividing by Zero
# Write your solution below. Run this file to test: python exercises/07_medium_safe_normalize.py

x = 5
min_val = 5
max_val = 5

# TODO: handle the max_val == min_val edge case, else use the normal formula
scaled = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = 0.0 if max_val == min_val else (x - min_val) / (max_val - min_val)
    assert scaled is not None, "scaled is still None -- fill in the if/else above."
    assert math.isclose(scaled, expected), f"Expected {expected}, got {scaled}"
    print("PASS")
