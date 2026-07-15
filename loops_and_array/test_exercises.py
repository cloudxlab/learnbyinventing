#!/usr/bin/env python3
"""Test runner for loops_and_array exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_find_min_max():
    from exercises.ex_1_1_find_min_max import find_min_max
    assert find_min_max([5, 8, 2, 10, 3]) == (2, 10)
    assert find_min_max([7, 7, 7, 7]) == (7, 7)
    assert find_min_max([-3, 0, 3]) == (-3, 3)

def test_ex_1_2_min_max_normalize():
    from exercises.ex_1_2_min_max_normalize import min_max_normalize
    assert min_max_normalize(20, [10, 20, 30]) == 0.5
    assert min_max_normalize(10, [10, 20, 30]) == 0.0
    assert min_max_normalize(30, [10, 20, 30]) == 1.0

def test_ex_1_3_compute_mean():
    from exercises.ex_1_3_compute_mean import compute_mean
    assert compute_mean([2, 4, 6, 8]) == 5.0
    assert compute_mean([10, 20, 30]) == 20.0
    assert compute_mean([]) == 0

def test_ex_1_4_compute_sd():
    from exercises.ex_1_4_compute_sd import compute_sd
    assert compute_sd([2, 4, 4, 4, 5, 5, 7, 9]) == 2.0
    assert compute_sd([10, 10, 10, 10]) == 0.0
    assert abs(compute_sd([0, 6]) - 3.0) < 1e-9

def test_ex_1_5_find_outliers():
    from exercises.ex_1_5_find_outliers import find_outliers
    assert find_outliers([10, 12, 12, 13, 12, 11, 90], 2) == [90]
    assert find_outliers([5, 6, 7, 8, 9, 10, 100], 2) == [100]
    assert find_outliers([1, 2, 3, 4, 5], 2) == []

def test_ex_1_6_compute_iqr():
    from exercises.ex_1_6_compute_iqr import compute_iqr
    assert compute_iqr([1, 2, 3, 4, 5, 6, 7, 8, 9]) == 4.0
    assert compute_iqr([10, 20, 30, 40, 50, 60]) == 30.0

def test_ex_1_7_standardize():
    from exercises.ex_1_7_standardize import standardize
    assert standardize([10, 10, 10]) == [0.0, 0.0, 0.0]
    result = standardize([1, 2, 3, 4, 5])
    assert abs(compute_mean(result)) < 1e-9
    assert abs(compute_sd(result) - 1.0) < 1e-9

def test_ex_2_1_compute_rmse():
    from exercises.ex_2_1_compute_rmse import compute_rmse
    assert compute_rmse([2, 3, 4], [3, 2, 5]) == 1.0
    assert compute_rmse([1, 2, 3], [1, 2, 3]) == 0.0
    print("Bonus:", compute_rmse([2, 3, 4], [3, 1, 7]))

def test_ex_2_2_compute_mae():
    from exercises.ex_2_2_compute_mae import compute_mae
    assert compute_mae([3, 5, 2], [2, 5, 4]) == 1.0
    assert compute_mae([1, 2, 3], [1, 2, 3]) == 0.0
    assert compute_mae([[0,0],[2,0]], [[1,0],[2,1]]) == 0.5

def test_ex_2_3_compute_huber_loss():
    from exercises.ex_2_3_compute_huber_loss import compute_huber_loss
    assert abs(compute_huber_loss([5, 2, 7], [4.8, 2.5, 10], 1) - 0.881667) < 1e-4
    assert compute_huber_loss([1, 2, 3], [1, 2, 3], 1) == 0.0

def test_ex_3_1_closer_point():
    from exercises.ex_3_1_closer_point import closer_point
    assert closer_point([1, 2], [0, 0], [5, 5]) == "A"
    assert closer_point([3, 3, 3], [0, 0, 0], [6, 6, 6]) == "Equal"
    assert closer_point([15, 15], [2, 2], [20, 20]) == "B"

def test_ex_3_2_find_nearest_1d():
    from exercises.ex_3_2_find_nearest_1d import find_nearest_1d
    assert find_nearest_1d([2, 5, 8, 12], 6) == 5
    assert find_nearest_1d([1, 4, 10, 20], 15) == 10

def test_ex_3_3_find_nearest_2d():
    from exercises.ex_3_3_find_nearest_2d import find_nearest_2d
    assert find_nearest_2d([(1,2),(3,4),(6,1)], (2,3)) == (1, 2)
    assert find_nearest_2d([(0,0),(5,5),(2,1)], (3,3)) == (2, 1)

def test_ex_3_4_find_nearest_nd():
    from exercises.ex_3_4_find_nearest_nd import find_nearest_nd
    assert find_nearest_nd([1,2], [[3,4],[2,1],[0,0]]) == [2, 1]
    assert find_nearest_nd([0,0,0], [[1,1,1],[2,2,2],[-1,-1,-1]]) == [1, 1, 1]

def test_ex_3_5_euclidean_distance():
    from exercises.ex_3_5_euclidean_distance import euclidean_distance
    from exercises.ex_3_5_euclidean_distance import manhattan_distance
    from exercises.ex_3_5_euclidean_distance import find_nearest_neighbour
    assert find_nearest_neighbour([1,2], [[3,4],[2,2],[0,0]], euclidean_distance) == [2, 2]
    assert find_nearest_neighbour([1,2,3], [[5,5,5],[0,0,0],[2,2,2]], manhattan_distance) == [2, 2, 2]

def test_ex_4_1_multiply_polynomial():
    from exercises.ex_4_1_multiply_polynomial import multiply_polynomial
    assert multiply_polynomial([2, 0, 3, 10], 5) == [10, 0, 15, 50]
    assert multiply_polynomial([1, -2, 4], 3) == [3, -6, 12]
    assert multiply_polynomial([1, 0], 0) == [0, 0]

def test_ex_4_2_add_polynomials():
    from exercises.ex_4_2_add_polynomials import add_polynomials
    assert add_polynomials([2, 0, 3, 10], [1, 4, 0, 6]) == [3, 4, 3, 16]
    assert add_polynomials([5, 2], [3]) == [5, 5]
    assert add_polynomials([1], [1]) == [2]

def test_ex_4_3_multiply_polynomials():
    from exercises.ex_4_3_multiply_polynomials import multiply_polynomials
    assert multiply_polynomials([2, 3], [1, 4]) == [2, 11, 12]
    assert multiply_polynomials([2, 0, 3, 10], [1, 2]) == [2, 4, 3, 16, 20]
    assert multiply_polynomials([1], [5]) == [5]

def test_ex_5_1_solve_for_first_variable():
    from exercises.ex_5_1_solve_for_first_variable import solve_for_first_variable
    assert solve_for_first_variable([3, 4, 6, 20], [5, 6]) == -12.0
    assert solve_for_first_variable([2, 5, 7], [4]) == -6.5

def test_ex_5_2_eliminate_variable_pair():
    from exercises.ex_5_2_eliminate_variable_pair import eliminate_variable_pair
    assert eliminate_variable_pair([2, 1, 5], [1, -1, 1], 0) == [3, 3]
    assert eliminate_variable_pair([1, 2, 3], [2, 1, 4], 1) == [-3, -5]

def test_ex_5_3_eliminate_variable():
    from exercises.ex_5_3_eliminate_variable import eliminate_variable
    result = eliminate_variable([[2, 1, 5], [1, -1, 1]], 0)
    print("After eliminating x:", result)
    # Expect [[3, 3]] meaning 3y = 3 → y = 1

def test_ex_5_4_solve_equations():
    from exercises.ex_5_4_solve_equations import solve_equations
    r2 = solve_equations([[2, 1, 5], [1, -1, 1]])
    assert abs(r2[0] - 2.0) < 1e-9 and abs(r2[1] - 1.0) < 1e-9, f"Got {r2}"

    r3 = solve_equations([[1,1,1,6],[0,2,5,-4],[2,5,-1,27]])
    assert all(abs(a - b) < 1e-9 for a, b in zip(r3, [5.0, 3.0, -2.0])), f"Got {r3}"
    print("x, y =", r2)
    print("x, y, z =", r3)

def test_ex_6_1_fair_coin_toss():
    from exercises.ex_6_1_fair_coin_toss import fair_coin_toss
    results = [fair_coin_toss() for _ in range(10)]
    heads = results.count(0)
    print(f"10 tosses: {heads} heads, {10-heads} tails")

def test_ex_6_2_biased_coin_toss():
    from exercises.ex_6_2_biased_coin_toss import biased_coin_toss
    n = 1000
    heads = sum(biased_coin_toss() == 0 for _ in range(n))
    print(f"Heads in {n} tosses: {heads} ({100*heads/n:.1f}%) — expect ~70%")

def test_ex_6_3_biased_coin_toss():
    from exercises.ex_6_3_biased_coin_toss import biased_coin_toss
    n = 2000
    for p_target in [0.3, 0.9]:
        heads = sum(biased_coin_toss(p_target) == 0 for _ in range(n))
        frac = heads / n
        print(f"p={p_target}: {frac:.3f} (expect {p_target})")
        assert abs(frac - p_target) < 0.06, f"Too far from target: {frac}"

def test_ex_6_4_weighted_choice():
    from exercises.ex_6_4_weighted_choice import weighted_choice
    n = 10000
    counts = Counter(weighted_choice([0.5, 0.3, 0.2]) for _ in range(n))
    for idx in range(3):
        print(f"index {idx}: {counts[idx]/n:.3f}")
    print("(expect ~0.50, ~0.30, ~0.20)")

def test_ex_6_5_normalize_to_probabilities():
    from exercises.ex_6_5_normalize_to_probabilities import normalize_to_probabilities
    assert normalize_to_probabilities([1, 2, 2]) == [0.2, 0.4, 0.4]
    assert normalize_to_probabilities([3, 3, 4]) == [0.3, 0.3, 0.4]

def test_ex_6_6_softmax():
    from exercises.ex_6_6_softmax import softmax
    r1 = softmax([1, 2, 3])
    assert abs(sum(r1) - 1.0) < 1e-9
    r2 = softmax([2, 2, 2])
    assert all(abs(x - 1/3) < 1e-9 for x in r2)
    print("softmax([1,2,3]):", [round(x, 4) for x in r1])

def test_ex_6_7_softmax():
    from exercises.ex_6_7_softmax import softmax
    r1 = softmax([1, 2, 3])
    r2 = softmax([1000, 1001, 1002])
    assert abs(sum(r2) - 1.0) < 1e-9
    for a, b in zip(r1, r2):
        assert abs(a - b) < 1e-9, f"{a} vs {b}"
    print("softmax([1000,1001,1002]):", [round(x, 4) for x in r2])

def test_ex_6_8_softmax_with_temperature():
    from exercises.ex_6_8_softmax_with_temperature import softmax_with_temperature
    r1     = softmax_with_temperature([1, 2, 3], 1)
    r_sharp = softmax_with_temperature([1, 2, 3], 0.5)
    r_flat  = softmax_with_temperature([1, 2, 3], 2)
    assert abs(sum(r1) - 1) < 1e-9
    assert r_sharp[2] > r1[2] > r_flat[2], "Temperature effect not working"
    print(f"T=0.5: {[round(x,3) for x in r_sharp]}")
    print(f"T=1.0: {[round(x,3) for x in r1]}")
    print(f"T=2.0: {[round(x,3) for x in r_flat]}")

def test_ex_6_9_weighted_choice_with_temperature():
    from exercises.ex_6_9_weighted_choice_with_temperature import weighted_choice_with_temperature
    n = 5000
    for T in [0.5, 1.0, 2.0]:
        counts = [0, 0, 0]
        for _ in range(n):
            counts[weighted_choice_with_temperature([1, 2, 8], T)] += 1
        fracs = [c/n for c in counts]
        print(f"T={T}: {[round(f,3) for f in fracs]}")
    print("(index 2 should dominate more at lower T)")

def test_ex_7_1_flatten_list():
    from exercises.ex_7_1_flatten_list import flatten_list
    assert flatten_list([1, [1, 2, [3, 4]]]) == [1, 1, 2, 3, 4]
    assert flatten_list([1, [2, [3, [4, 5]]]]) == [1, 2, 3, 4, 5]
    assert flatten_list([1, 2, 3]) == [1, 2, 3]
    assert flatten_list([[[]]]) == []

def test_ex_7_2_solve_expression():
    from exercises.ex_7_2_solve_expression import solve_expression
    assert solve_expression(42) == 42
    assert solve_expression(["+", 20, 40]) == 60
    assert solve_expression(["*", ["+", 20, 40], 90]) == 5400
    assert solve_expression(["-", ["*", ["/", 100, 10], 5], 15]) == 35

def test_ex_7_3_calculate():
    from exercises.ex_7_3_calculate import calculate
    assert calculate(42) == 42
    assert calculate(["+", 1, 2, 3]) == 6
    assert calculate(["*", 2, 3, 4]) == 24
    assert calculate(["-", 10, 4]) == 6
    assert calculate(["/", 8, 2]) == 4
    assert calculate(["sqrt", 16]) == 4
    assert calculate(["log", 100]) == 2
    assert calculate(["+", ["sqrt", 16], ["log", 1000], 2]) == 9

    for bad in (["-", 1, 2, 3], ["sqrt", 4, 9], ["/", 8], ["@", 1, 2]):
        try:
            calculate(bad)
            assert False, f"{bad} should have raised ValueError"
        except ValueError:
            pass

def test_ex_8_1_xors():
    from exercises.ex_8_1_xors import xors
    assert xors([1], [2], [3]) == [0]
    assert xors([1, 2], [2, 3], [3, 4]) == [0, 5]
    assert xors([7, 7], [0, 7], [0, 0]) == [7, 0]

def test_ex_8_2_reverse_in_place():
    from exercises.ex_8_2_reverse_in_place import reverse_in_place
    a = [1, 2, 3, 4, 5]
    assert reverse_in_place(a) is None      # modifies in place, returns nothing
    assert a == [5, 4, 3, 2, 1]

    b = [10, 20]
    reverse_in_place(b)
    assert b == [20, 10]

    c = [7]
    reverse_in_place(c)
    assert c == [7]

def test_ex_8_3_shift_left():
    from exercises.ex_8_3_shift_left import shift_left
    a = [10, 20, 30]
    shift_left(a)
    assert a == [20, 30, 10]
    shift_left(a)
    assert a == [30, 10, 20]

    b = [1]
    shift_left(b)
    assert b == [1]

def test_ex_8_4_shift_left_k():
    from exercises.ex_8_4_shift_left_k import shift_left_k
    a = [1, 2, 3, 4, 5]
    shift_left_k(a, 2)
    assert a == [3, 4, 5, 1, 2]

    b = [1, 2, 3, 4, 5, 6]
    shift_left_k(b, 4)
    assert b == [5, 6, 1, 2, 3, 4]

    c = [1, 2, 3]
    shift_left_k(c, 0)
    assert c == [1, 2, 3]

    d = [1, 2, 3]
    shift_left_k(d, 3)
    assert d == [1, 2, 3]


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
