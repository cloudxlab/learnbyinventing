#!/usr/bin/env python3
"""Test runner for sorting exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_0_1_is_sorted():
    from exercises.ex_0_1_is_sorted import is_sorted
    assert is_sorted([1, 2, 2, 9]) == True
    assert is_sorted([1, 3, 2])    == False
    assert is_sorted([5])          == True
    assert is_sorted([])           == True

def test_ex_0_2_swap():
    from exercises.ex_0_2_swap import swap
    x = [10, 20, 30]
    swap(x, 0, 2)
    assert x == [30, 20, 10]
    swap(x, 1, 1)
    assert x == [30, 20, 10]

def test_ex_1_1_bubble_pass():
    from exercises.ex_1_1_bubble_pass import bubble_pass
    x = [3, 1, 4, 1, 5, 9, 2, 6]
    bubble_pass(x)
    assert x == [1, 3, 1, 4, 5, 2, 6, 9]
    x = [2, 1]
    bubble_pass(x)
    assert x == [1, 2]

def test_ex_1_2_pass_sort():
    from exercises.ex_1_2_pass_sort import pass_sort
    x = [5, 2, 9, 1, 5, 6]
    pass_sort(x)
    assert x == [1, 2, 5, 5, 6, 9]

    x = [1]
    pass_sort(x)
    assert x == [1]

    x = list(range(100, 0, -1))     # worst case: reversed
    pass_sort(x)
    assert is_sorted(x)

def test_ex_1_3_pass_sort_counting():
    from exercises.ex_1_3_pass_sort_counting import pass_sort_counting
    for n in [10, 100, 1000]:
        data = random.sample(range(10000), n)
        comparisons = pass_sort_counting(data)
        assert is_sorted(data)
        print(f"n={n:5d}  comparisons={comparisons:8d}  ratio to n^2: {comparisons/(n*n):.3f}")

def test_ex_2_1_insert_card():
    from exercises.ex_2_1_insert_card import insert_card
    x = [2, 5, 8, 3]
    insert_card(x, 3)
    assert x == [2, 3, 5, 8]

    x = [1, 2, 3, 0]
    insert_card(x, 3)
    assert x == [0, 1, 2, 3]

    x = [1, 2, 3, 9]      # already in the right place
    insert_card(x, 3)
    assert x == [1, 2, 3, 9]

def test_ex_2_2_card_sort():
    from exercises.ex_2_2_card_sort import card_sort
    x = [5, 2, 9, 1, 5, 6]
    card_sort(x)
    assert x == [1, 2, 5, 5, 6, 9]

    x = list(range(200, 0, -1))
    card_sort(x)
    assert is_sorted(x)

def test_ex_2_3_card_sort_counting():
    from exercises.ex_2_3_card_sort_counting import card_sort_counting
    sorted_data   = list(range(1000))
    reversed_data = list(range(1000, 0, -1))

    c1 = card_sort_counting(sorted_data)
    c2 = card_sort_counting(reversed_data)
    assert is_sorted(sorted_data) and is_sorted(reversed_data)
    print(f"Already sorted (n=1000): {c1} comparisons")
    print(f"Reversed       (n=1000): {c2} comparisons")

def test_ex_3_1_merge():
    from exercises.ex_3_1_merge import merge
    assert merge([1, 5, 9], [2, 3, 7]) == [1, 2, 3, 5, 7, 9]
    assert merge([], [4, 8])           == [4, 8]
    assert merge([4, 8], [])           == [4, 8]
    assert merge([1, 1], [1])          == [1, 1, 1]

def test_ex_3_2_split_sort():
    from exercises.ex_3_2_split_sort import split_sort
    assert split_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]
    assert split_sort([])  == []
    assert split_sort([7]) == [7]

    data = random.sample(range(100000), 10000)
    assert split_sort(data) == sorted(data)

def test_ex_4_1_partition_01():
    from exercises.ex_4_1_partition_01 import partition_01
    from exercises.ex_4_1_partition_01 import check_partition_01
    check_partition_01([(0,"x"), (1, 12), (0, 34), (1, 90), (1, 89), (0, "s"), (1, "7")])
    check_partition_01([(1, "a"), (0, "b")])
    check_partition_01([(0, "a"), (0, "b")])
    check_partition_01([])

def test_ex_4_2_partition():
    from exercises.ex_4_2_partition import partition
    x = [3, 8, 2, 5, 1, 4]
    p = partition(x, 0, 5)
    assert x[p] == 4
    assert all(v < 4 for v in x[:p])
    assert all(v >= 4 for v in x[p:])

def test_ex_4_3_pivot_sort():
    from exercises.ex_4_3_pivot_sort import pivot_sort
    x = [5, 2, 9, 1, 5, 6]
    pivot_sort(x)
    assert x == [1, 2, 5, 5, 6, 9]

    data = random.sample(range(100000), 10000)
    expected = sorted(data)
    pivot_sort(data)
    assert data == expected

def test_ex_5_1_count_values():
    from exercises.ex_5_1_count_values import count_values
    assert count_values([3, 1, 3, 0], 3) == [1, 1, 0, 2]
    assert count_values([], 2)           == [0, 0, 0]

def test_ex_5_2_tally_sort():
    from exercises.ex_5_2_tally_sort import tally_sort
    assert tally_sort([3, 1, 3, 0], 3) == [0, 1, 3, 3]

    ages = [random.randint(0, 200) for _ in range(1000000)]
    t0 = time.perf_counter()
    result = tally_sort(ages, 200)
    t1 = time.perf_counter()
    assert result == sorted(ages)


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
