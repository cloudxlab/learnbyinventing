# Classify Correlation Strength and Direction
# Write your solution below. Run this file to test: python exercises/06_medium_correlation_strength.py

r = -0.82

# TODO: set strength to "weak", "moderate", or "strong" based on abs(r)
strength = None

# TODO: set direction to "positive", "negative", or "none" based on the sign of r
direction = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    def ref_strength(r):
        a = abs(r)
        if a < 0.3:
            return "weak"
        elif a < 0.7:
            return "moderate"
        else:
            return "strong"


    def ref_direction(r):
        if r > 0:
            return "positive"
        elif r < 0:
            return "negative"
        else:
            return "none"


    assert strength == ref_strength(r), f"strength: expected {ref_strength(r)!r}, got {strength!r}"
    assert direction == ref_direction(r), f"direction: expected {ref_direction(r)!r}, got {direction!r}"
    print("PASS")
