# Exercise 7.2 — Your First Convolution
# Write your solution in this file. Run test_exercises.py to check.

def conv(image, weights):
    """
    Applies a convolution filter to a grayscale image.

    Parameters:
        image   : 2D numpy array of shape (H, W)
        weights : 2D numpy array of shape (K, K) — the filter kernel

    Returns:
        output  : 2D numpy array of shape (H-K+1, W-K+1)
                  Contains the raw convolution output (may not be in [0,255])
    """
    H, W = image.shape
    K    = weights.shape[0]  # Kernel size (assume square)

    out_H = H - K + 1
    out_W = W - K + 1

    output = np.zeros((out_H, out_W), dtype=np.float64)

    for r in range(out_H):
        for c in range(out_W):
            total = 0.0
            for i in range(K):
                for j in range(K):
                    pass  # total += ???
            output[r, c] = total

    return output
