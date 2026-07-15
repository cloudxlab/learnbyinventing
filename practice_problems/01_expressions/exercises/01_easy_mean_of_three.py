# Find the Mean of Three Numbers
# Write your solution below. Run this file to test: python exercises/01_easy_mean_of_three.py

a = 21
b = 19
c = 26

# TODO: compute the mean of a, b, c as a single expression
mean_value = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = (a + b + c) / 3
    assert mean_value is not None, "mean_value is still None -- fill in the expression above."
    assert math.isclose(mean_value, expected), f"Expected {expected}, got {mean_value}"
    print("PASS")
