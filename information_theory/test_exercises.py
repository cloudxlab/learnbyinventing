#!/usr/bin/env python3
"""Test runner for information_theory exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_encode_ab():
    from exercises.ex_1_1_encode_ab import encode_ab
    from exercises.ex_1_1_encode_ab import decode_ab
    assert encode_ab("AABBA") == "00110"
    assert encode_ab("BA") == "10"
    assert decode_ab("00110") == "AABBA"
    assert decode_ab("10") == "BA"

def test_ex_1_2_is_prefix_free():
    from exercises.ex_1_2_is_prefix_free import is_prefix_free
    assert is_prefix_free({"A": "0", "B": "1"})   == True
    assert is_prefix_free({"A": "0", "B": "00"})  == False
    assert is_prefix_free({"A": "0", "B": "10"})  == True

def test_ex_2_1_encode_fixed():
    from exercises.ex_2_1_encode_fixed import encode_fixed
    from exercises.ex_2_1_encode_fixed import decode_fixed
    assert encode_fixed("ABC")    == "000110"
    assert encode_fixed("CAB")    == "100001"
    assert decode_fixed("000110") == "ABC"
    assert decode_fixed("100001") == "CAB"

def test_ex_2_2_encode_var():
    from exercises.ex_2_2_encode_var import encode_var
    from exercises.ex_2_2_encode_var import decode_var
    assert encode_var("ABC")    == "01011"
    assert encode_var("CAB")    == "11010"
    assert decode_var("01011")  == "ABC"
    assert decode_var("11010")  == "CAB"

def test_ex_3_1_avg_bits():
    from exercises.ex_3_1_avg_bits import avg_bits
    frequencies = {"A": 0.50, "B": 0.25, "C": 0.20, "D": 0.05}
    fixed4 = {"A": "00", "B": "01", "C": "10", "D": "11"}
    assert avg_bits(fixed4, frequencies) == 2.0

def test_ex_4_2_build_huffman_tree():
    from exercises.ex_4_2_build_huffman_tree import build_huffman_tree
    tree = build_huffman_tree({"A": 0.50, "B": 0.25, "C": 0.20, "D": 0.05})
    print("Tree:", tree)
    # Should be a nested tuple like ("A", ("B", ("D", "C")))

def test_ex_4_3_assign_codes():
    from exercises.ex_4_3_assign_codes import assign_codes
    codes = assign_codes(("A", ("B", ("D", "C"))))
    print("Codes from tree:", codes)
    assert is_prefix_free(codes), "Huffman codes must be prefix-free"
    frequencies = {"A": 0.50, "B": 0.25, "C": 0.20, "D": 0.05}
    print("Avg bits:", avg_bits(codes, frequencies))

def test_ex_4_4_huffman_scheme():
    from exercises.ex_4_4_huffman_scheme import huffman_scheme
    frequencies = {"A": 0.50, "B": 0.25, "C": 0.20, "D": 0.05}
    scheme = huffman_scheme(frequencies)
    print("Huffman scheme:", scheme)
    assert is_prefix_free(scheme)
    avg = avg_bits(scheme, frequencies)
    print(f"Avg bits/symbol: {avg:.4f}  (fixed would be 2.0)")
    assert avg <= 2.0, "Huffman should beat or match fixed width"

def test_ex_4_5_entropy():
    from exercises.ex_4_5_entropy import entropy
    frequencies = {"A": 0.50, "B": 0.25, "C": 0.20, "D": 0.05}
    h = entropy(frequencies)
    huff_avg = avg_bits(huffman_scheme(frequencies), frequencies)
    print(f"Entropy (lower bound): {h:.4f} bits/symbol")
    print(f"Huffman average:       {huff_avg:.4f} bits/symbol")
    print(f"Gap:                   {huff_avg - h:.4f} bits/symbol")
    assert huff_avg >= h - 1e-9, "Huffman cannot beat entropy"

def test_ex_5_1_encode():
    from exercises.ex_5_1_encode import encode
    frequencies = {"A": 0.50, "B": 0.25, "C": 0.20, "D": 0.05}
    bits, scheme = encode("AABCD", frequencies)
    print("Encoded bits:", bits)
    print("Scheme:      ", scheme)

def test_ex_5_2_decode():
    from exercises.ex_5_2_decode import decode
    frequencies = {"A": 0.50, "B": 0.25, "C": 0.20, "D": 0.05}
    bits, scheme = encode("AABCD", frequencies)
    recovered = decode(bits, scheme)
    assert recovered == "AABCD", f"Got {recovered}"
    print("Recovered:", recovered)


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
