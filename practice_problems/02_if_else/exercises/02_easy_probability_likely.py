# Classify a Probability as Likely or Unlikely
# Write your solution below. Run this file to test: python exercises/02_easy_probability_likely.py

p = 0.72

# TODO: set label to "likely" if p >= 0.5, else "unlikely"
label = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    expected = "likely" if p >= 0.5 else "unlikely"
    assert label == expected, f"Expected {expected!r}, got {label!r}"
    print("PASS")
