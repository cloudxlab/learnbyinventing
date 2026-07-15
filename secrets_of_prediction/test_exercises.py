#!/usr/bin/env python3
"""Test runner for secrets_of_prediction exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_dot_product():
    from exercises.ex_1_1_dot_product import dot_product
    assert dot_product([1, 2], [3, 4]) == 11
    assert dot_product([1, 0, 2], [5, 5, 5]) == 15
    assert dot_product([2], [7]) == 14

def test_ex_1_2_vector_length():
    from exercises.ex_1_2_vector_length import vector_length
    from exercises.ex_1_2_vector_length import convert_to_unit
    assert vector_length([3, 4]) == 5.0
    assert convert_to_unit([3, 4]) == [0.6, 0.8]
    assert abs(vector_length(convert_to_unit([2, 3, 6])) - 1.0) < 1e-9

def test_ex_1_3_cosine_similarity():
    from exercises.ex_1_3_cosine_similarity import cosine_similarity
    assert abs(cosine_similarity([1, 2], [2, 4]) - 1.0) < 1e-9    # same direction
    assert abs(cosine_similarity([1, 0], [0, 1])) < 1e-9           # perpendicular
    assert abs(cosine_similarity([1, 2], [-1, -2]) + 1.0) < 1e-9   # opposite

def test_ex_1_4_matrix_mul():
    from exercises.ex_1_4_matrix_mul import matrix_mul
    A = [[1, 2],
         [3, 4]]
    B = [[5, 6],
         [7, 8]]
    assert matrix_mul(A, B) == [[19, 22], [43, 50]]

    M = [[1, 2, 3],
         [4, 5, 6]]
    v = [[1], [0], [2]]                      # a column vector
    assert matrix_mul(M, v) == [[7], [16]]   # (2x3) @ (3x1) -> (2x1)

def test_ex_3_3_solve_poly():
    from exercises.ex_3_3_solve_poly import solve_poly
    assert abs(solve_poly([1, 2, 3], [6, 12, 20], 4) - 30.0) < 1e-6
    # a line is just a degree-1 polynomial — the apple trips again:
    assert abs(solve_poly([3, 5], [6, 8], 10) - 13.0) < 1e-6
    # and it must reproduce the points it was built from:
    assert abs(solve_poly([1, 2, 3], [6, 12, 20], 2) - 12.0) < 1e-6

def test_ex_4_1_total_error():
    from exercises.ex_4_1_total_error import total_error
    assert total_error(3, 5, factory_data) == 4.0   # hits two points, misses the third by 2
    assert total_error(0, 0, factory_data) == 8*8 + 11*11 + 16*16

def test_ex_4_3_best_line():
    from exercises.ex_4_3_best_line import best_line
    m, c = best_line([(0, 3), (1, 5), (2, 7)])        # perfectly linear: y = 2x + 3
    assert abs(m - 2.0) < 1e-9 and abs(c - 3.0) < 1e-9

    m, c = best_line(factory_data)
    assert abs(m - 4.0) < 1e-9 and abs(c - 11/3) < 1e-9
    print("factory prediction for input 4:", round(m * 4 + c, 3))


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
