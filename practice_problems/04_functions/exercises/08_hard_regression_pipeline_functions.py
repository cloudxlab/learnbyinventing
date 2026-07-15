# Build a Linear Regression Pipeline From Smaller Functions
# Write your solution below. Run this file to test: python exercises/08_hard_regression_pipeline_functions.py

def predict(x, slope, intercept):
    """Return the predicted y for a given x, slope, and intercept."""
    # TODO: implement
    pass


def mse(y_true_list, y_pred_list):
    """Return the mean squared error between two equal-length lists."""
    # TODO: implement
    pass


def gradient_descent_fit(x_list, y_list, learning_rate, epochs):
    """Fit y = slope * x + intercept to the data using gradient descent.

    Start slope = intercept = 0.0, run `epochs` update steps (see the
    formulas in the markdown cell above), and return (slope, intercept).
    Call predict() inside your loop.
    """
    slope, intercept = 0.0, 0.0
    # TODO: implement the training loop
    return slope, intercept


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    assert math.isclose(predict(2, 3, 1), 7)

    y_pred_sample = [predict(xi, 3, 1) for xi in [0, 1, 2, 3, 4, 5]]
    assert math.isclose(mse([1, 4, 7, 10, 13, 16], y_pred_sample), 0.0, abs_tol=1e-9)

    x_list = [0, 1, 2, 3, 4, 5]
    y_list = [1, 4, 7, 10, 13, 16]  # y = 3x + 1
    slope, intercept = gradient_descent_fit(x_list, y_list, learning_rate=0.01, epochs=2000)
    assert abs(slope - 3) < 0.3, f"slope {slope} did not converge close to 3"
    assert abs(intercept - 1) < 0.3, f"intercept {intercept} did not converge close to 1"
    print("PASS")
