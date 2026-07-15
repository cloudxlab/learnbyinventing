#!/usr/bin/env python3
"""Test runner for backtracking exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_handshakes():
    from exercises.ex_1_1_handshakes import handshakes
    assert handshakes(["A", "B", "C"]) == [("A", "B"), ("A", "C"), ("B", "C")]
    assert handshakes(["A", "B", "C", "D"]) == [
        ("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")]
    assert handshakes(["solo"]) == []
    n = 30
    assert len(handshakes(list(range(n)))) == n * (n - 1) // 2

def test_ex_2_1_next_numb():
    from exercises.ex_2_1_next_numb import next_numb
    a = [0, 0]
    assert next_numb(a, 2) == True and a == [0, 1]
    assert next_numb(a, 2) == True and a == [1, 0]
    assert next_numb(a, 2) == True and a == [1, 1]
    assert next_numb(a, 2) == False

    a = [2, 9]
    assert next_numb(a, 10) == True and a == [3, 0]

def test_ex_2_2_generate():
    from exercises.ex_2_2_generate import generate
    assert generate(1, 3) == ["0", "1", "2"]
    assert generate(2, 2) == ["00", "01", "10", "11"]
    out = generate(3, 3)
    assert len(out) == 27
    assert out[0] == "000" and out[-1] == "222"

def test_ex_2_3_generate_rec():
    from exercises.ex_2_3_generate_rec import generate_rec
    assert generate_rec(1, 3) == ["0", "1", "2"]
    assert generate_rec(2, 2) == ["00", "01", "10", "11"]
    assert generate_rec(3, 3) == generate(3, 3)

def test_ex_3_1_perms():
    from exercises.ex_3_1_perms import perms
    assert perms("x") == ["x"]
    assert sorted(perms("ab")) == ["ab", "ba"]
    assert sorted(perms("abc")) == ["abc", "acb", "bac", "bca", "cab", "cba"]
    assert len(perms("abcde")) == 120

def test_ex_4_1_are_valid():
    from exercises.ex_4_1_are_valid import are_valid
    assert are_valid("[]") == True
    assert are_valid("}{") == False
    assert are_valid("([{}])") == True
    assert are_valid("(]") == False
    assert are_valid("(()") == False
    assert are_valid("") == True
    assert are_valid("()[]{}") == True

def test_ex_5_1_find_first_empty_space():
    from exercises.ex_5_1_find_first_empty_space import find_first_empty_space
    assert find_first_empty_space(puzzle) == (0, 2)
    full = [[1] * 9 for _ in range(9)]
    assert find_first_empty_space(full) == (None, None)

def test_ex_5_2_can_place():
    from exercises.ex_5_2_can_place import can_place
    # Cell (0, 2) of the puzzle: its row holds {5, 3, 7}, its column holds {8},
    # and its 3x3 block holds {5, 3, 6, 9, 8}.
    assert can_place(5, 0, 2, puzzle) == False   # 5 is already in the row
    assert can_place(7, 0, 2, puzzle) == False   # 7 is already in the row
    assert can_place(8, 0, 2, puzzle) == False   # 8 is already in the column
    assert can_place(9, 0, 2, puzzle) == False   # 9 is already in the block
    assert can_place(1, 0, 2, puzzle) == True
    assert can_place(2, 0, 2, puzzle) == True

def test_ex_5_3_solve_sudoku():
    from exercises.ex_5_3_solve_sudoku import solve_sudoku
    from exercises.ex_5_3_solve_sudoku import is_solved
    board = copy.deepcopy(puzzle)
    assert solve_sudoku(board) == True
    assert is_solved(board)
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != 0:
                assert board[r][c] == puzzle[r][c], "a clue was overwritten!"
    print_board(board)


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
