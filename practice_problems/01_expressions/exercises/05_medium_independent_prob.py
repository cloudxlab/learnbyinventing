# Probability of Two Independent Events
# Write your solution below. Run this file to test: python exercises/05_medium_independent_prob.py

p_rain = 0.3
p_traffic = 0.6

# TODO: probability that BOTH independent events happen
p_both = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = p_rain * p_traffic
    assert p_both is not None, "p_both is still None -- fill in the expression above."
    assert math.isclose(p_both, expected), f"Expected {expected}, got {p_both}"
    print("PASS")
