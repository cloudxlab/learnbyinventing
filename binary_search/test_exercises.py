#!/usr/bin/env python3
"""Test runner for binary_search exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_0_1_count_halvings():
    from exercises.ex_0_1_count_halvings import count_halvings
    assert count_halvings(1) == 0
    assert count_halvings(16) == 4
    assert count_halvings(1000) == 9   # floor(log2(1000))
    print(f"To find a number in [1..1000], at most {count_halvings(1000)+1} guesses needed.")

def test_ex_1_1_sqrt_binary_search():
    from exercises.ex_1_1_sqrt_binary_search import sqrt_binary_search
    assert abs(sqrt_binary_search(25,  0.0001) - 5.0)    < 0.001
    assert abs(sqrt_binary_search(2,   0.0001) - 1.4142) < 0.001
    assert abs(sqrt_binary_search(0,   0.0001) - 0.0)    < 0.001
    assert abs(sqrt_binary_search(144, 0.0001) - 12.0)   < 0.001
    print(f"sqrt(2) ≈ {sqrt_binary_search(2, 1e-9):.9f}  (math.sqrt = {math.sqrt(2):.9f})")

def test_ex_2_1_cuberoot_binary_search():
    from exercises.ex_2_1_cuberoot_binary_search import cuberoot_binary_search
    assert abs(cuberoot_binary_search(27,    1e-6) - 3.0)    < 1e-4
    assert abs(cuberoot_binary_search(8,     1e-6) - 2.0)    < 1e-4
    assert abs(cuberoot_binary_search(-64,   1e-6) - (-4.0)) < 1e-4
    assert abs(cuberoot_binary_search(0.001, 1e-6) - 0.1)    < 1e-4
    assert abs(cuberoot_binary_search(0,     1e-6) - 0.0)    < 1e-4
    print(f"cuberoot(-125) ≈ {cuberoot_binary_search(-125, 1e-9):.6f}  (expect -5.0)")

def test_ex_3_1_nth_root_binary_search():
    from exercises.ex_3_1_nth_root_binary_search import nth_root_binary_search
    assert abs(nth_root_binary_search(16,  2) - 4.0)             < 1e-6
    assert abs(nth_root_binary_search(27,  3) - 3.0)             < 1e-6
    assert abs(nth_root_binary_search(81,  4) - 3.0)             < 1e-6
    assert abs(nth_root_binary_search(32,  5) - 2.0)             < 1e-6
    assert abs(nth_root_binary_search(1,   7) - 1.0)             < 1e-6
    assert abs(nth_root_binary_search(0.5, 2) - math.sqrt(0.5))  < 1e-6

def test_ex_4_1_log10_binary_search():
    from exercises.ex_4_1_log10_binary_search import log10_binary_search
    assert abs(log10_binary_search(100)  - 2.0)    < 1e-6
    assert abs(log10_binary_search(1000) - 3.0)    < 1e-6
    assert abs(log10_binary_search(0.01) - (-2.0)) < 1e-6
    assert abs(log10_binary_search(1)    - 0.0)    < 1e-9
    assert abs(log10_binary_search(2)    - math.log10(2)) < 1e-6
    print(f"log10(2) ≈ {log10_binary_search(2):.8f}  (math.log10 = {math.log10(2):.8f})")

def test_ex_5_1_log_base_n():
    from exercises.ex_5_1_log_base_n import log_base_n
    assert abs(log_base_n(8,    2) - 3.0)             < 1e-6
    assert abs(log_base_n(81,   3) - 4.0)             < 1e-6
    assert abs(log_base_n(0.04, 5) - (-2.0))          < 1e-6
    assert abs(log_base_n(10,   2) - math.log(10, 2)) < 1e-6
    assert abs(log_base_n(100, 10) - 2.0)             < 1e-6
    print(f"log2(10) ≈ {log_base_n(10, 2):.8f}  (math.log = {math.log(10, 2):.8f})")

def test_ex_6_1_contains():
    from exercises.ex_6_1_contains import contains
    arr = [1, 3, 5, 7, 9, 11]
    assert contains(arr, 7) == True
    assert contains(arr, 1) == True
    assert contains(arr, 11) == True
    assert contains(arr, 4) == False
    assert contains(arr, 0) == False
    assert contains(arr, 12) == False
    assert contains([], 5) == False

def test_ex_6_2_find_first():
    from exercises.ex_6_2_find_first import find_first
    from exercises.ex_6_2_find_first import find_last
    arr = [1, 2, 2, 2, 3, 5, 5]
    assert find_first(arr, 2) == 1
    assert find_last(arr, 2) == 3
    assert find_first(arr, 5) == 5
    assert find_last(arr, 5) == 6
    assert find_first(arr, 4) == -1
    assert find_last(arr, 4) == -1
    assert find_first(arr, 1) == 0 and find_last(arr, 1) == 0

def test_ex_6_3_count_val():
    from exercises.ex_6_3_count_val import count_val
    readings = [0]*5 + [1]*3 + [2]*4
    assert count_val(readings, 0) == 5
    assert count_val(readings, 1) == 3
    assert count_val(readings, 2) == 4
    assert count_val(readings, 7) == 0

    big = [0]*400000 + [1]*300000 + [2]*300000
    assert count_val(big, 1) == 300000

def test_ex_6_4_commons():
    from exercises.ex_6_4_commons import commons
    big = list(range(0, 2_000_000, 2))   # a million even numbers
    assert commons([5, 10, 999_999, 1_000_000], big) == [10, 1_000_000]
    assert commons([1, 3, 7], big) == []
    assert commons([0, 2, 4], big) == [0, 2, 4]

def test_ex_6_5_find_min_convex():
    from exercises.ex_6_5_find_min_convex import find_min_convex
    assert find_min_convex([10, 9, 8, 6.5, 4.1, 3.2, 2, 4, 4.5, 6]) == 2
    assert find_min_convex([5, 3, 1, 2, 8]) == 1
    assert find_min_convex([3, 2, 1]) == 1      # all downhill
    assert find_min_convex([1, 2, 3]) == 1      # all uphill
    assert find_min_convex([7]) == 7


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
