# Euclidean Distance Between Two Points
# Write your solution below. Run this file to test: python exercises/04_medium_euclidean_2d.py

x1, y1 = 2, 3
x2, y2 = 7, 11

# TODO: compute the Euclidean distance between (x1, y1) and (x2, y2)
distance = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    assert distance is not None, "distance is still None -- fill in the expression above."
    assert math.isclose(distance, expected), f"Expected {expected}, got {distance}"
    print("PASS")
