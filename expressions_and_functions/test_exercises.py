#!/usr/bin/env python3
"""Test runner for expressions_and_functions exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_2_last_digit():
    from exercises.ex_1_2_last_digit import last_digit
    assert last_digit(2784) == 4
    assert last_digit(7) == 7
    assert last_digit(100) == 0
    assert last_digit(0) == 0

def test_ex_1_3_remove_last_digit():
    from exercises.ex_1_3_remove_last_digit import remove_last_digit
    assert remove_last_digit(2784) == 278
    assert remove_last_digit(7) == 0
    assert remove_last_digit(100) == 10
    print(remove_last_digit(0))     # your prediction?

def test_ex_1_4_check_roundtrip():
    from exercises.ex_1_4_check_roundtrip import check_roundtrip
    for n in [2784, 7, 100, 0, 999999]:
        print(n, "->", check_roundtrip(n))

def test_ex_2_2_calculate_interest():
    from exercises.ex_2_2_calculate_interest import calculate_interest
    assert calculate_interest(1000, 5, 2) == 100.0
    assert calculate_interest(1500, 4.3, 3) == 193.5
    assert calculate_interest(500, 10, 0) == 0.0

def test_ex_3_2_calculate_hypotenuse():
    from exercises.ex_3_2_calculate_hypotenuse import calculate_hypotenuse
    assert calculate_hypotenuse(3, 4) == 5.0
    assert calculate_hypotenuse(5, 12) == 13.0
    assert calculate_hypotenuse(0, 0) == 0.0

def test_ex_3_4_find_distance_2d():
    from exercises.ex_3_4_find_distance_2d import find_distance_2d
    assert find_distance_2d(0, 0, 3, 4) == 5.0
    assert find_distance_2d(1, 2, 4, 6) == 5.0

def test_ex_3_6_calculate_distance_3d():
    from exercises.ex_3_6_calculate_distance_3d import calculate_distance_3d
    assert calculate_distance_3d(0, 0, 0, 1, 1, 1) == 1.7320508075688772
    assert calculate_distance_3d(2, 3, 5, 2, 3, 5) == 0.0
    assert calculate_distance_3d(1, 2, 3, 4, 6, 9) == 7.810249675906654

def test_ex_3_8_manhattan_distance():
    from exercises.ex_3_8_manhattan_distance import manhattan_distance
    assert manhattan_distance(2, 3, 5, 1) == 5
    assert manhattan_distance(0, 0, 0, 0) == 0
    assert manhattan_distance(-1, -1, 1, 1) == 4

def test_ex_4_2_predict():
    from exercises.ex_4_2_predict import predict
    assert predict(2, 3, 4) == 11
    assert predict(-1, 5, 2) == 3

def test_ex_4_5_fit():
    from exercises.ex_4_5_fit import fit
    assert fit(1, 2, 3, 6) == (2.0, 0.0)
    assert fit(0, 5, 2, 9) == (2.0, 5.0)

def test_ex_5_2_approx_derivative():
    from exercises.ex_5_2_approx_derivative import approx_derivative
    from exercises.ex_5_2_approx_derivative import square
    print(approx_derivative(square, 3, 0.0001))   # approx 6

def test_ex_5_3_cube():
    from exercises.ex_5_3_cube import cube
    print("cube'(2) approx:", approx_derivative(cube, 2, 0.0001), " (true: 12)")
    print("sin'(0) approx: ", approx_derivative(math.sin, 0, 0.0001), " (true: 1)")

    print("\nEffect of h on cube'(2):")
    for h in [0.1, 0.01, 0.0001, 0.0000001, 1e-15]:
        print(f"  h={h:<12} derivative={approx_derivative(cube, 2, h)}")

def test_ex_5_4_tangent_line_intercept():
    from exercises.ex_5_4_tangent_line_intercept import tangent_line_intercept
    print(tangent_line_intercept(square, 3, 0.0001))

def test_ex_5_5_all_digits():
    from exercises.ex_5_5_all_digits import all_digits
    assert all_digits is not None


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
