# Exercise 5.2 — Implement Three Upsampling Methods
# Write your solution in this file. Run test_exercises.py to check.

def upsample_nearest(img, scale=2):
    """
    Upsamples a (H, W) image to (H*scale, W*scale) by pixel replication.
    Each output pixel (r, c) copies from input (r//scale, c//scale).
    """
    h, w = img.shape
    out_h, out_w = h * scale, w * scale
    result = np.zeros((out_h, out_w), dtype=np.uint8)
    for r in range(out_h):
        for c in range(out_w):
            pass  # result[r, c] = ???
    return result


# METHOD B: Bilinear Interpolation

def lerp(a, b, t):
    """Linear interpolation between a and b. t=0 gives a, t=1 gives b."""
    pass  # return ???


def upsample_bilinear(img, scale=2):
    """
    Upsamples using bilinear interpolation.
    For each output pixel (r, c):
      - Map to input coordinates: in_r = r / scale, in_c = c / scale
      - Find the four surrounding input pixels
      - Interpolate
    """
    h, w = img.shape
    out_h, out_w = h * scale, w * scale
    result = np.zeros((out_h, out_w), dtype=np.uint8)
    for r in range(out_h):
        for c in range(out_w):
            # Map output coordinates to input space
            in_r = r / scale
            in_c = c / scale

            # Find surrounding pixel indices
            r0 = int(in_r)          # floor
            c0 = int(in_c)          # floor
            r1 = min(r0 + 1, h - 1) # ceiling, clamped to image
            c1 = min(c0 + 1, w - 1)

            # Fractional parts (where between r0 and r1 are we?)
            dr = in_r - r0
            dc = in_c - c0

            # Bilinear interpolation: interpolate in r direction, then c
            # Step 1: interpolate the top row and bottom row
            # top    = lerp(img[r0, c0], img[r0, c1], dc)
            # bottom = lerp(img[r1, c0], img[r1, c1], dc)
            # Step 2: interpolate between top and bottom
            # value = lerp(top, bottom, dr)

            # YOUR CODE HERE
            pass

    return result


# METHOD C: YOUR OWN

def upsample_mymethod(img, scale=2):
    """Your own upsampling method!"""
    pass
