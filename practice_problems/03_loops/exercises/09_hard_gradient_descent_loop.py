# Run Several Iterations of Gradient Descent
# Write your solution below. Run this file to test: python exercises/09_hard_gradient_descent_loop.py

target = 10
w = 0.0
learning_rate = 0.1
epochs = 20
loss_history = []

# TODO: loop `epochs` times, updating w and appending to loss_history each time


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    w_ref = 0.0
    expected_history = []
    for _ in range(epochs):
        grad = 2 * (w_ref - target)
        w_ref = w_ref - learning_rate * grad
        expected_history.append((w_ref - target) ** 2)

    assert len(loss_history) == epochs, f"loss_history should have {epochs} entries, has {len(loss_history)}"
    assert all(math.isclose(a, b) for a, b in zip(loss_history, expected_history)), "loss_history values are wrong"
    assert math.isclose(w, w_ref), f"Expected w close to {w_ref}, got {w}"
    assert loss_history[-1] < loss_history[0], "loss should decrease over training"
    print("PASS")
