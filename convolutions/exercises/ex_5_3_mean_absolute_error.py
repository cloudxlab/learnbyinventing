# Exercise 5.3 — Compare and Analyze
# Write your solution in this file. Run test_exercises.py to check.

def mean_absolute_error(img_a, img_b):
    """
    Computes pixel-wise mean absolute error between two same-size images.
    Use only Python loops — no np.mean, no array subtraction.
    """
    h, w = img_a.shape
    total = 0
    for r in range(h):
        for c in range(w):
            pass  # total += ???
    return total / (h * w)
