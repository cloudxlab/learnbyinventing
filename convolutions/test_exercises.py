#!/usr/bin/env python3
"""Test runner for convolutions exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_3_2_rgb_to_gray_average():
    from exercises.ex_3_2_rgb_to_gray_average import rgb_to_gray_average
    from exercises.ex_3_2_rgb_to_gray_average import rgb_to_gray_lightness
    from exercises.ex_3_2_rgb_to_gray_average import rgb_to_gray_luminosity
    from exercises.ex_3_2_rgb_to_gray_average import rgb_to_gray_mymethod
    # Test — run average on the color image
    gray_average = rgb_to_gray_average(color_arr)
    print("Shape:", gray_average.shape)
    print("Dtype:", gray_average.dtype)

def test_ex_4_3_downsample_nearest():
    from exercises.ex_4_3_downsample_nearest import downsample_nearest
    from exercises.ex_4_3_downsample_nearest import downsample_average
    from exercises.ex_4_3_downsample_nearest import downsample_max
    from exercises.ex_4_3_downsample_nearest import downsample_mymethod
    # Test one of them
    small = downsample_nearest(img_100)
    print("Output shape:", small.shape)  # Should be (50, 50)

def test_ex_5_2_upsample_nearest():
    from exercises.ex_5_2_upsample_nearest import upsample_nearest
    from exercises.ex_5_2_upsample_nearest import lerp
    from exercises.ex_5_2_upsample_nearest import upsample_bilinear
    from exercises.ex_5_2_upsample_nearest import upsample_mymethod
    # Test Method A
    big_nearest = upsample_nearest(img_50)
    print("Output shape:", big_nearest.shape)  # Should be (100, 100)

def test_ex_5_3_mean_absolute_error():
    from exercises.ex_5_3_mean_absolute_error import mean_absolute_error
    # Compute and print MAE for each method
    mae_nearest = mean_absolute_error(big_nearest, img_100)
    print(f"MAE (Nearest):  {mae_nearest:.4f}")

    # Add bilinear and mymethod when ready
    # mae_bilinear = mean_absolute_error(big_bilinear, img_100)
    # print(f"MAE (Bilinear): {mae_bilinear:.4f}")

def test_ex_6_1_resize_nearest():
    from exercises.ex_6_1_resize_nearest import resize_nearest
    from exercises.ex_6_1_resize_nearest import resize_bilinear
    # Test: resize 50x50 to 150x150
    # img_150_nearest  = resize_nearest(img_50, 150, 150)
    # img_150_bilinear = resize_bilinear(img_50, 150, 150)
    # print("150x150 shapes:", img_150_nearest.shape, img_150_bilinear.shape)

def test_ex_7_2_conv():
    from exercises.ex_7_2_conv import conv
    # SANITY CHECK: Identity filter — should return the original image (minus edges)
    identity_kernel = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ], dtype=np.float64)

    result = conv(img_100.astype(np.float64), identity_kernel)
    print("Output shape:", result.shape)            # Should be (98, 98)

    # Check: result[0,0] should equal img_100[1,1]
    print(f"result[0,0] = {result[0,0]:.1f}")
    print(f"img_100[1,1] = {img_100[1,1]}")
    print("Match:", abs(result[0,0] - float(img_100[1,1])) < 1e-9)

def test_ex_7_6_pad_image():
    from exercises.ex_7_6_pad_image import pad_image
    from exercises.ex_7_6_pad_image import conv_same
    # Test
    padded = pad_image(img_100, pad_size=1)
    print("Padded shape:", padded.shape)  # Should be (102, 102)

    # result_same = conv_same(img_100.astype(np.float64), kernel_blur)
    # print("conv_same output shape:", result_same.shape)  # Should be (100, 100)

def test_ex_7_7_conv_color():
    from exercises.ex_7_7_conv_color import conv_color
    from exercises.ex_7_7_conv_color import show_color_conv
    # show_color_conv(color_arr, color_blurred, title='Color Blur')


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = errors = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}: {e}")
        except Exception as e:
            errors += 1
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")
    total = passed + failed + errors
    print(f"\n{passed}/{total} passed, {failed} failed, {errors} errors")
    sys.exit(0 if failed + errors == 0 else 1)
