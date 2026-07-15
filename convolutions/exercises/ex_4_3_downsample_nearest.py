# Exercise 4.3 — Implement Three Downsampling Methods
# Write your solution in this file. Run test_exercises.py to check.

def downsample_nearest(img):
    """
    Downsamples a (H, W) image to (H//2, W//2) by taking every other pixel.
    """
    h, w = img.shape
    out_h, out_w = h // 2, w // 2
    result = np.zeros((out_h, out_w), dtype=np.uint8)
    for r in range(out_h):
        for c in range(out_w):
            pass  # result[r, c] = ???
    return result


# METHOD B: Average Pooling

def downsample_average(img):
    """
    Downsamples by averaging each 2x2 block.
    """
    h, w = img.shape
    out_h, out_w = h // 2, w // 2
    result = np.zeros((out_h, out_w), dtype=np.uint8)
    for r in range(out_h):
        for c in range(out_w):
            pass  # result[r, c] = average of 2x2 block
    return result


# METHOD C: Max Pooling

def downsample_max(img):
    """
    Downsamples by taking the maximum of each 2x2 block.
    """
    h, w = img.shape
    out_h, out_w = h // 2, w // 2
    result = np.zeros((out_h, out_w), dtype=np.uint8)
    for r in range(out_h):
        for c in range(out_w):
            pass  # result[r, c] = max of 2x2 block
    return result


# METHOD D: YOUR OWN

def downsample_mymethod(img):
    """Your own downsampling method — describe it in the docstring!"""
    pass
