#!/usr/bin/env python3
"""Test runner for if_else exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_2_roll_die():
    from exercises.ex_1_2_roll_die import roll_die
    for _ in range(20):
        print(roll_die(), end=" ")

def test_ex_1_3_coin_toss():
    from exercises.ex_1_3_coin_toss import coin_toss
    print([coin_toss() for _ in range(20)])

    heads_count = 0
    for _ in range(10000):
        if coin_toss() == "Heads":
            heads_count = heads_count  # fill in: count heads
    print(f"Heads: {heads_count} / 10000")

def test_ex_1_4_classify_roll():
    from exercises.ex_1_4_classify_roll import classify_roll
    for _ in range(20):
        n = roll_die()
        print(f"{n} -> {classify_roll(n)}")

def test_ex_2_2_closer_point():
    from exercises.ex_2_2_closer_point import closer_point
    assert closer_point((1, 2), (0, 0), (5, 5)) == A
    assert closer_point((4, 4), (0, 0), (8, 8)) == Equal
    assert closer_point((7, 3), (2, 3), (10, 3)) == B

def test_ex_3_2_is_point_on_line_1d():
    from exercises.ex_3_2_is_point_on_line_1d import is_point_on_line_1d
    assert is_point_on_line_1d(2, 5, 3) == True
    assert is_point_on_line_1d(5, 2, 3) == True
    assert is_point_on_line_1d(2, 5, 6) == False
    assert is_point_on_line_1d(4, 4, 4) == True
    assert is_point_on_line_1d(4, 4, 5) == False

def test_ex_4_2_are_lines_touching_or_overlapping():
    from exercises.ex_4_2_are_lines_touching_or_overlapping import are_lines_touching_or_overlapping
    assert are_lines_touching_or_overlapping(1, 4, 3, 6) == True
    assert are_lines_touching_or_overlapping(1, 3, 3, 5) == True
    assert are_lines_touching_or_overlapping(1, 2, 3, 4) == False

def test_ex_5_2_is_point_inside_rectangle():
    from exercises.ex_5_2_is_point_inside_rectangle import is_point_inside_rectangle
    assert is_point_inside_rectangle(0, 0, 10, 5, 3, 2) == True
    assert is_point_inside_rectangle(0, 0, 10, 5, 10, 5) == True
    assert is_point_inside_rectangle(0, 0, 10, 5, 11, 5) == False
    assert is_point_inside_rectangle(-5, -5, 5, 5, 0, 0) == True

def test_ex_6_2_are_rectangles_intersecting():
    from exercises.ex_6_2_are_rectangles_intersecting import are_rectangles_intersecting
    assert are_rectangles_intersecting(((0, 0), (3, 3)), ((2, 2), (5, 5))) == True
    assert are_rectangles_intersecting(((0, 0), (1, 1)), ((2, 2), (3, 3))) == False
    assert are_rectangles_intersecting(((0, 0), (2, 2)), ((2, 2), (4, 4))) == True
    assert are_rectangles_intersecting(((0, 0), (5, 5)), ((1, 1), (2, 2))) == True

def test_ex_6_3_my_impurity():
    from exercises.ex_6_3_my_impurity import my_impurity
    for c1, c2 in [(0, 5), (5, 5), (7, 3), (9, 1)]:
        print(f"my_impurity({c1}, {c2}) = {my_impurity(c1, c2)}")


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
