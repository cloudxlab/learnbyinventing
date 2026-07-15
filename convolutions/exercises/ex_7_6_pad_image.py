# Exercise 7.6 — Add Padding
# Write your solution in this file. Run test_exercises.py to check.

def pad_image(img, pad_size):
    """
    Pads a (H, W) image with `pad_size` zeros on all sides.
    Returns a (H + 2*pad_size, W + 2*pad_size) array.
    
    Implement using loops — no np.pad!
    """
    H, W = img.shape
    new_H = H + 2 * pad_size
    new_W = W + 2 * pad_size
    result = np.zeros((new_H, new_W), dtype=img.dtype)
    # Copy img into the center of result
    # YOUR CODE HERE
    for r in range(H):
        for c in range(W):
            pass  # result[r + pad_size, c + pad_size] = ???
    return result



def conv_same(image, weights):
    """
    Convolution with 'same' padding: output is the same size as input.
    Uses pad_image internally.
    """
    K = weights.shape[0]
    pad_size = (K - 1) // 2
    # YOUR CODE: pad the image, then call conv on the padded version
    pass
