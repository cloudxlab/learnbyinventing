# Assign a Point to the Nearest Centroid
# Write your solution below. Run this file to test: python exercises/05_medium_nearest_centroid.py

dist_to_a = 4.2
dist_to_b = 3.7

# TODO: assign to "A" if dist_to_a is smaller, else "B"
assignment = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    expected = "A" if dist_to_a < dist_to_b else "B"
    assert assignment == expected, f"Expected {expected!r}, got {assignment!r}"
    print("PASS")
