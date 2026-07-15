#!/usr/bin/env python3
"""Test runner for gradient_descent exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_f():
    from exercises.ex_1_1_f import f
    # Step 2: Plot it
    # plot_function(...)

    # Step 3: Write your visual estimate of the minimum below
    # My guess: x ≈ ???

def test_ex_2_1_numerical_derivative():
    from exercises.ex_2_1_numerical_derivative import numerical_derivative
    # Test it
    test_points = [0, 1, 1.5, 2]
    for x in test_points:
        slope = numerical_derivative(f, x)
        # print x, slope, and direction

def test_ex_2_3_find_minima_1d():
    from exercises.ex_2_3_find_minima_1d import find_minima_1d
    # Test it
    x_min, f_min, history = find_minima_1d(f, x_start=2.0)
    print(f"Minimum found at x = {x_min:.6f}")
    print(f"f(x_min) = {f_min:.6f}")
    print(f"Steps taken: {len(history)}")

def test_ex_3_1_fa():
    from exercises.ex_3_1_fa import fA
    plot_function(fA, x_range=(-2, 2), title="fA: x^6 - 4x^2 + 10")

    # YOUR CODE: run find_minima_1d and plot_descent
    # What do you notice? Are there multiple minima?

def test_ex_4_1_g():
    from exercises.ex_4_1_g import g
    plot_function_2d(g, title="g(x,y) = x^2 + y^2")

    # Now define and plot h1, h2, h3
    # ...

def test_ex_4_2_partial_x():
    from exercises.ex_4_2_partial_x import partial_x
    from exercises.ex_4_2_partial_x import partial_y
    from exercises.ex_4_2_partial_x import gradient_2d
    # Test on g(x,y) = x^2 + y^2
    test_points = [(1, 1), (3, 0), (0, 0)]
    for (x, y) in test_points:
        grad = gradient_2d(g, x, y)
        print(f"Gradient at ({x}, {y}) = {grad}")

def test_ex_4_3_find_minima_2d():
    from exercises.ex_4_3_find_minima_2d import find_minima_2d
    # Test on g
    x_min, y_min, f_min, history = find_minima_2d(g, x_start=2.0, y_start=3.0)
    print(f"g: minimum at ({x_min:.4f}, {y_min:.4f}), f={f_min:.6f}, steps={len(history)}")
    plot_function_2d(g, mark_xy=(x_min, y_min), title="g: descent result")

def test_ex_5_1_compute_gradient():
    from exercises.ex_5_1_compute_gradient import compute_gradient
    from exercises.ex_5_1_compute_gradient import find_minima
    # Test 1D
    min_vars, f_min, history = find_minima(lambda v: v[0]**4 - 4*v[0] + 10, [2.0])
    print(f"1D minimum: x = {min_vars[0]:.6f}, f = {f_min:.6f}")

    # Test 2D
    min_vars, f_min, history = find_minima(lambda v: v[0]**2 + v[1]**2, [2.0, 3.0])
    print(f"2D minimum: x = {min_vars[0]:.6f}, y = {min_vars[1]:.6f}, f = {f_min:.6f}")

def test_ex_5_2_p():
    from exercises.ex_5_2_p import p
    from exercises.ex_5_2_p import q
    # Run find_minima on p
    min_vars, f_min, history = find_minima(p, [0.0, 0.0, 0.0])
    print(f"p minimum: {min_vars}, f = {f_min:.6f}")

    # Run find_minima on q
    # YOUR CODE

    # What is the analytical answer for q?

def test_ex_6_2_mse():
    from exercises.ex_6_2_mse import mse
    # Sanity check
    X_tiny = np.array([1.0, 2.0, 3.0])
    y_tiny = np.array([3.0, 5.0, 7.0])
    print(f"MSE for perfect line (should be 0): {mse(X_tiny, y_tiny, 2.0, 1.0):.6f}")

    # Compare on main dataset
    lines_to_test = [
        (2.5, 4.0, "true line"),
        (1.0, 5.0, "guess 1"),
        (5.0, 0.0, "guess 2"),
    ]
    for m, c, label in lines_to_test:
        error = mse(X_data, y_data, m, c)
        print(f"{label:15s}: m={m}, c={c}  →  MSE={error:.4f}")

def test_ex_6_3_mse_landscape():
    from exercises.ex_6_3_mse_landscape import mse_landscape
    plot_function_2d(mse_landscape, x_range=(0, 5), y_range=(-5, 15),
                     title="MSE Landscape",
                     mark_xy=(2.5, 4.0))

def test_ex_7_1_mse_for_optimizer():
    from exercises.ex_7_1_mse_for_optimizer import mse_for_optimizer
    # Run the optimizer — tune alpha if needed
    min_params, f_min, history = find_minima(mse_for_optimizer, [0.0, 0.0], alpha=0.001)

    m_found, c_found = min_params
    print(f"Found:  m = {m_found:.4f},  c = {c_found:.4f}")
    print(f"True:   m = 2.5000,  c = 4.0000")
    print(f"MSE at found values: {mse(X_data, y_data, m_found, c_found):.4f}")

    # Plot the result
    plot_data_and_line(X_data, y_data, m=m_found, c=c_found, title=f"Best fit: m={m_found:.2f}, c={c_found:.2f}")

def test_ex_7_3_mse_d1():
    from exercises.ex_7_3_mse_d1 import mse_d1
    # find_minima and plot result

def test_ex_8_1_predict():
    from exercises.ex_8_1_predict import predict
    assert predict([1, 2], [2, 3], 1) == 9      # 2*1 + 3*2 + 1
    assert predict([0, 0], [2, 3], 1) == 1      # only the intercept survives
    assert predict([10], [0.5], 2) == 7         # works for a single feature too

def test_ex_8_2_total_err_sqr():
    from exercises.ex_8_2_total_err_sqr import total_err_sqr
    assert total_err_sqr(X, y, [2, 3], 1) == 0.0      # perfect weights, zero error
    assert abs(total_err_sqr(X, y, [0, 0], 0) - 207.5) < 1e-9

def test_ex_8_3_gradients():
    from exercises.ex_8_3_gradients import gradients
    gm, gc = gradients(X, y, [2, 3], 1)
    assert all(abs(g) < 1e-3 for g in gm) and abs(gc) < 1e-3   # flat at the optimum

    gm, gc = gradients(X, y, [0, 0], 0)
    assert gm[0] < 0 and gm[1] < 0 and gc < 0   # all slopes point downhill-negative
    print("gradients at zero weights:", [round(g, 1) for g in gm], round(gc, 1))

def test_ex_8_4_fit():
    from exercises.ex_8_4_fit import fit
    m, c = fit(X, y)
    print("found m =", [round(v, 3) for v in m], " c =", round(c, 3))
    assert abs(m[0] - 2) < 0.05
    assert abs(m[1] - 3) < 0.05
    assert abs(c - 1) < 0.15
    assert total_err_sqr(X, y, m, c) < 0.01

def test_ex_8_5_add_feature():
    from exercises.ex_8_5_add_feature import add_feature
    assert add_feature([[1, 2], [3, 4]], lambda row: row[0] * row[1]) == [[1, 2, 2], [3, 4, 12]]

    Xc = [[1], [2], [3], [4], [5]]
    yc = [1, 4, 9, 16, 25]                      # y = x^2

    m1, c1 = fit(Xc, yc, learning_rate=0.005, epochs=8000)
    line_mse = total_err_sqr(Xc, yc, m1, c1)

    Xc2 = add_feature(Xc, lambda row: row[0] ** 2)
    m2, c2 = fit(Xc2, yc, learning_rate=0.001, epochs=20000)
    curve_mse = total_err_sqr(Xc2, yc, m2, c2)

    print(f"straight line MSE: {line_mse:.3f}   with x^2 feature: {curve_mse:.6f}")
    assert line_mse > 1
    assert curve_mse < 0.1

def test_ex_8_6_analytic_gradients():
    from exercises.ex_8_6_analytic_gradients import analytic_gradients
    gm_a, gc_a = analytic_gradients(X, y, [0.5, -1.0], 2.0)
    gm_n, gc_n = gradients(X, y, [0.5, -1.0], 2.0)
    print("analytic:", [round(g, 3) for g in gm_a], round(gc_a, 3))
    print("numeric: ", [round(g, 3) for g in gm_n], round(gc_n, 3))
    assert all(abs(a - b) < 1e-2 for a, b in zip(gm_a, gm_n))
    assert abs(gc_a - gc_n) < 1e-2
    print("chain rule verified — calculus agrees with nudging")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = errors = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}: {e}")
        except Exception as e:
            errors += 1
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")
    total = passed + failed + errors
    print(f"\n{passed}/{total} passed, {failed} failed, {errors} errors")
    sys.exit(0 if failed + errors == 0 else 1)
