# Exercise 5.3 — `solve_sudoku`
# Write your solution in this file. Run test_exercises.py to check.

import copy

def solve_sudoku(board):
    pass  # replace this


# --- checker (provided): every row, column and block must be exactly {1..9} ---

def is_solved(board):
    want = set(range(1, 10))
    for r in range(9):
        if set(board[r]) != want:
            return False
    for c in range(9):
        if set(board[r][c] for r in range(9)) != want:
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            if set(board[r][c]
                   for r in range(br, br + 3)
                   for c in range(bc, bc + 3)) != want:
                return False
    return True
