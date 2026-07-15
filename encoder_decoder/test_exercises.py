#!/usr/bin/env python3
"""Test runner for encoder_decoder exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_parse_line():
    from exercises.ex_1_1_parse_line import parse_line
    assert parse_line("sandeep, 2, 2.0\n") == ("sandeep", 2, 2.0)
    assert parse_line("nitin,1, 3.5")      == ("nitin", 1, 3.5)
    assert parse_line("a@b.com , 7 , 0.5") == ("a@b.com", 7, 0.5)

def test_ex_1_2_read_data():
    from exercises.ex_1_2_read_data import read_data
    rows = read_data("our_data.csv")
    assert rows == [("sandeep", 1, 1.0), ("nitin", 2, 3.0), ("subodh", 2, 1.0),
                    ("sandeep", 2, 2.0), ("nitin", 1, 2.0)]

def test_ex_2_1_build_mapping():
    from exercises.ex_2_1_build_mapping import build_mapping
    mapping = build_mapping(rows)
    assert mapping == {"sandeep": 1, "nitin": 2, "subodh": 3}

def test_ex_2_2_save_mapping():
    from exercises.ex_2_2_save_mapping import save_mapping
    from exercises.ex_2_2_save_mapping import load_mapping
    save_mapping(mapping, "mapping.csv")
    print(open("mapping.csv").read())
    assert load_mapping("mapping.csv") == mapping

def test_ex_2_3_encode_file():
    from exercises.ex_2_3_encode_file import encode_file
    encode_file("our_data.csv", "encoded.csv", "mapping.csv")
    print(open("encoded.csv").read())

    expected = "1,1,1.0\n2,2,3.0\n3,2,1.0\n1,2,2.0\n2,1,2.0\n"
    assert open("encoded.csv").read() == expected
    assert load_mapping("mapping.csv") == {"sandeep": 1, "nitin": 2, "subodh": 3}

def test_ex_4_1_invert():
    from exercises.ex_4_1_invert import invert
    assert invert({"sandeep": 1, "nitin": 2}) == {1: "sandeep", 2: "nitin"}

def test_ex_4_2_decode_file():
    from exercises.ex_4_2_decode_file import decode_file
    decode_file("recommendations.csv", "mapping.csv", "final.csv")
    result = open("final.csv").read()
    print(result)
    assert result == "subodh,1,1.5\n"

def test_ex_5_1_check_pipeline():
    from exercises.ex_5_1_check_pipeline import check_pipeline
    assert check_pipeline("big_data.csv", "big_final.csv") == True


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
