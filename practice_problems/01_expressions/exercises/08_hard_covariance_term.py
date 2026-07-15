# One Term of a Covariance Sum
# Write your solution below. Run this file to test: python exercises/08_hard_covariance_term.py

x, x_mean = 5, 4
y, y_mean = 12, 9

# TODO: compute (x - x_mean) * (y - y_mean)
term = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = (x - x_mean) * (y - y_mean)
    assert term is not None, "term is still None -- fill in the expression above."
    assert math.isclose(term, expected), f"Expected {expected}, got {term}"
    print("PASS")
