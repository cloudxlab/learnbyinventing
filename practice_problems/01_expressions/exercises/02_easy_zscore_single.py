# Compute a Single Z-Score
# Write your solution below. Run this file to test: python exercises/02_easy_zscore_single.py

x = 82
mu = 70
sigma = 8

# TODO: compute the z-score of x as a single expression
z_score = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = (x - mu) / sigma
    assert z_score is not None, "z_score is still None -- fill in the expression above."
    assert math.isclose(z_score, expected), f"Expected {expected}, got {z_score}"
    print("PASS")
