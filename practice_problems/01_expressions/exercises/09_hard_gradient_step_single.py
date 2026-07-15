# One Gradient Descent Update Step
# Write your solution below. Run this file to test: python exercises/09_hard_gradient_step_single.py

w = 4.0
learning_rate = 0.1
gradient = 2.5

# TODO: apply one gradient descent update step
new_w = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = w - learning_rate * gradient
    assert new_w is not None, "new_w is still None -- fill in the expression above."
    assert math.isclose(new_w, expected), f"Expected {expected}, got {new_w}"
    print("PASS")
