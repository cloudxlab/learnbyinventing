# Exercise 3.2 — Implement Your Formulas
# Write your solution in this file. Run test_exercises.py to check.

def rgb_to_gray_average(arr):
    """
    Converts color image to grayscale using simple average: (R+G+B)/3.
    arr: numpy array of shape (H, W, 3), dtype uint8
    Returns: numpy array of shape (H, W), dtype uint8
    """
    h, w = arr.shape[0], arr.shape[1]
    result = np.zeros((h, w), dtype=np.uint8)
    for r in range(h):
        for c in range(w):
            R, G, B = arr[r, c, 0], arr[r, c, 1], arr[r, c, 2]
            gray = int((R + G + B) / 3)
            result[r, c] = max(0, min(255, gray))
    return result

# YOUR CODE: implement the other methods

def rgb_to_gray_lightness(arr):
    pass


def rgb_to_gray_luminosity(arr):
    pass


def rgb_to_gray_mymethod(arr):
    """Your own formula!"""
    pass
