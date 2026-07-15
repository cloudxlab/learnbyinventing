# Apply the Sigmoid Activation Function
# Write your solution below. Run this file to test: python exercises/07_medium_sigmoid_single.py

import math

x = 2.5

# TODO: compute sigmoid(x) as a single expression, using math.exp
activation = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = 1 / (1 + math.exp(-x))
    assert activation is not None, "activation is still None -- fill in the expression above."
    assert math.isclose(activation, expected), f"Expected {expected}, got {activation}"
    print("PASS")
