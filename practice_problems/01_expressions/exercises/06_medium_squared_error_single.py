# Squared Error for One Prediction
# Write your solution below. Run this file to test: python exercises/06_medium_squared_error_single.py

y_true = 50
y_pred = 42

# TODO: compute the squared error of this one prediction
squared_error = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = (y_true - y_pred) ** 2
    assert squared_error is not None, "squared_error is still None -- fill in the expression above."
    assert math.isclose(squared_error, expected), f"Expected {expected}, got {squared_error}"
    print("PASS")
