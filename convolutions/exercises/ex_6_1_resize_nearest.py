# Exercise 6.1 — A New Challenge
# Write your solution in this file. Run test_exercises.py to check.

def resize_nearest(img, target_h, target_w):
    """
    Resizes img to (target_h, target_w) using nearest neighbor.
    For output pixel (r, c), map to input (round(r * h / target_h), round(c * w / target_w))
    or equivalently: input_r = int(r * h / target_h), clamped to [0, h-1].
    """
    h, w = img.shape
    result = np.zeros((target_h, target_w), dtype=np.uint8)
    for r in range(target_h):
        for c in range(target_w):
            # Map to input coordinates
            # in_r = ???  (use int(...) to round down)
            # in_c = ???
            # Clamp to valid range: in_r must be < h, in_c must be < w
            pass
    return result


# METHOD B: Bilinear Resize (arbitrary target size)

def resize_bilinear(img, target_h, target_w):
    """
    Resizes img to (target_h, target_w) using bilinear interpolation.
    For output pixel (r, c), the input coordinates are:
      in_r = r * (h - 1) / (target_h - 1)
      in_c = c * (w - 1) / (target_w - 1)
    Then bilinearly interpolate.
    """
    h, w = img.shape
    result = np.zeros((target_h, target_w), dtype=np.uint8)
    for r in range(target_h):
        for c in range(target_w):
            # Input coordinates (note: use (h-1)/(target_h-1) to map edges correctly)
            in_r = r * (h - 1) / max(1, target_h - 1)
            in_c = c * (w - 1) / max(1, target_w - 1)

            r0 = int(in_r)
            c0 = int(in_c)
            r1 = min(r0 + 1, h - 1)
            c1 = min(c0 + 1, w - 1)

            dr = in_r - r0
            dc = in_c - c0

            # YOUR BILINEAR INTERPOLATION HERE
            pass
    return result
