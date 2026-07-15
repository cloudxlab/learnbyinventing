# Recursive Binomial Coefficient via Pascal's Rule
# Write your solution below. Run this file to test: python exercises/05_medium_recursive_n_choose_k.py

def n_choose_k(n, k):
    """Return the binomial coefficient C(n, k), using Pascal's rule recursively."""
    # TODO: base cases -- k == 0 or k == n
    # TODO: recursive case -- Pascal's rule
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    for n in range(0, 8):
        for k in range(0, n + 1):
            assert n_choose_k(n, k) == math.comb(n, k), f"n_choose_k({n}, {k}) is wrong"
    print("PASS")
