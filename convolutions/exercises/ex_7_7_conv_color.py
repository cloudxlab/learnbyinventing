# Exercise 7.7 — Convolution on a Color Image
# Write your solution in this file. Run test_exercises.py to check.

def conv_color(image_rgb, weights):
    """
    Applies conv_same independently to each color channel.
    image_rgb: (H, W, 3) uint8 array
    weights  : (K, K) kernel
    Returns  : (H, W, 3) float64 array
    """
    H, W = image_rgb.shape[0], image_rgb.shape[1]
    result = np.zeros((H, W, 3), dtype=np.float64)

    for ch in range(3):  # ch = 0 (R), 1 (G), 2 (B)
        channel = image_rgb[:, :, ch].astype(np.float64)
        # Apply conv_same to this channel
        # result[:, :, ch] = ???
        pass

    return result


# Apply blur to color image and display
# color_blurred = conv_color(color_arr, kernel_blur)

# DISPLAY HELPER for color convolution output

def show_color_conv(original, output, title='Color Convolution'):
    lo = output.min()
    hi = output.max()
    if hi > lo:
        display = ((output - lo) / (hi - lo) * 255).astype(np.uint8)
    else:
        display = np.zeros_like(output, dtype=np.uint8)
    show_images([original, display], titles=['Original', title])
