# Exercise 7.1 — Minimize MSE with `find_minima`
# Write your solution in this file. Run test_exercises.py to check.

def mse_for_optimizer(params):
    m, c = params
    return mse(X_data, y_data, m, c)
