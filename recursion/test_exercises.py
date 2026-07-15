#!/usr/bin/env python3
"""Test runner for recursion exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_2_factorial_recursive():
    from exercises.ex_1_2_factorial_recursive import factorial_recursive
    assert factorial_recursive(5) == 120
    assert factorial_recursive(3) == 6
    assert factorial_recursive(0) == 1
    assert factorial_recursive(1) == 1

def test_ex_2_2_multiply_recursive():
    from exercises.ex_2_2_multiply_recursive import multiply_recursive
    assert multiply_recursive(4, 3) == 12
    assert multiply_recursive(5, 0) == 0

def test_ex_2_4_multiply_recursive():
    from exercises.ex_2_4_multiply_recursive import multiply_recursive
    assert multiply_recursive(4, 3) == 12
    assert multiply_recursive(5, 0) == 0
    assert multiply_recursive(7, -2) == -14
    assert multiply_recursive(-3, -3) == 9

def test_ex_3_2_power():
    from exercises.ex_3_2_power import power
    assert power(2, 3) == 8
    assert power(5, 2) == 25

def test_ex_4_2_compute_power():
    from exercises.ex_4_2_compute_power import compute_power
    assert compute_power(2, 3) == 8
    assert compute_power(2, -3) == 0.125
    assert compute_power(5, 0) == 1
    assert compute_power(-2, 3) == -8

def test_ex_5_2_recursive_divide():
    from exercises.ex_5_2_recursive_divide import recursive_divide
    assert recursive_divide(17, 5) == (3, 2)
    assert recursive_divide(20, 4) == (5, 0)
    assert recursive_divide(7, 3) == (2, 1)
    assert recursive_divide(0, 1) == (0, 0)

def test_ex_6_2_compute_hcf():
    from exercises.ex_6_2_compute_hcf import compute_hcf
    assert compute_hcf(12, 18) == 6
    assert compute_hcf(100, 25) == 25
    assert compute_hcf(17, 13) == 1
    assert compute_hcf(0, 5) == 5

def test_ex_7_2_solve_hanoi():
    from exercises.ex_7_2_solve_hanoi import solve_hanoi
    total = solve_hanoi(1)
    print("Returns:", total)

def test_ex_7_3_fib():
    from exercises.ex_7_3_fib import fib
    # import time
    # start = time.time()
    # print(fib(30))
    # print("took", time.time() - start, "seconds")


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
