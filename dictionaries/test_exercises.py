#!/usr/bin/env python3
"""Test runner for dictionaries exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_0_3_safe_lookup():
    from exercises.ex_0_3_safe_lookup import safe_lookup
    assert safe_lookup({"a": 1}, "a") == 1
    assert safe_lookup({"a": 1}, "b") == "not found"

def test_ex_0_4_count_items():
    from exercises.ex_0_4_count_items import count_items
    assert count_items(["a", "b", "a", "c", "b", "a"]) == {"a": 3, "b": 2, "c": 1}
    assert count_items([1, 2, 1, 1, 3]) == {1: 3, 2: 1, 3: 1}
    assert count_items([]) == {}

def test_ex_1_1_word_count():
    from exercises.ex_1_1_word_count import word_count
    assert word_count("hello world hello") == {"hello": 2, "world": 1}
    assert word_count("apple orange apple banana orange") == {"apple": 2, "orange": 2, "banana": 1}
    assert word_count("") == {}

def test_ex_1_2_most_frequent_word():
    from exercises.ex_1_2_most_frequent_word import most_frequent_word
    assert most_frequent_word("the cat sat on the mat the") == "the"
    assert most_frequent_word("a b a b c a") == "a"

def test_ex_1_3_top_n_words():
    from exercises.ex_1_3_top_n_words import top_n_words
    result = top_n_words("the cat sat on the mat the cat", 2)
    assert result[0] == ("the", 3)
    assert result[1] == ("cat", 2)

    # Try on a longer passage:
    passage = "to be or not to be that is the question to be is to do"
    print(top_n_words(passage, 5))

def test_ex_2_1_anagram_key():
    from exercises.ex_2_1_anagram_key import anagram_key
    assert anagram_key("listen") == "eilnst"
    assert anagram_key("silent") == "eilnst"
    assert anagram_key("evil")   == "eilv"
    assert anagram_key("vile")   == "eilv"
    assert anagram_key("a")      == "a"

def test_ex_2_2_find_anagrams():
    from exercises.ex_2_2_find_anagrams import find_anagrams
    r1 = find_anagrams("listen silent enlist inlets hello world")
    assert sorted(r1["eilnst"]) == sorted(["listen", "silent", "enlist", "inlets"])
    assert r1["ehllo"] == ["hello"]
    assert r1["dlorw"] == ["world"]

    r2 = find_anagrams("evil vile live veil")
    assert sorted(r2["eilv"]) == sorted(["evil", "vile", "live", "veil"])

def test_ex_2_3_find_true_anagram_groups():
    from exercises.ex_2_3_find_true_anagram_groups import find_true_anagram_groups
    r = find_true_anagram_groups("listen silent hello world live evil")
    assert "eilnst" in r and len(r["eilnst"]) == 2
    assert "eilv"   in r and len(r["eilv"])   == 2
    assert "ehllo"  not in r
    assert "dlorw"  not in r

def test_ex_3_1_update_expenses():
    from exercises.ex_3_1_update_expenses import update_expenses
    expenses = {}
    update_expenses([("food", 200), ("rent", 1000)], expenses)
    update_expenses([("food", 300), ("travel", 150)], expenses)
    assert expenses == {"food": 500, "rent": 1000, "travel": 150}
    print(expenses)

def test_ex_3_2_print_expenses():
    from exercises.ex_3_2_print_expenses import print_expenses
    expenses = {"food": 500, "rent": 1000, "travel": 150}
    print_expenses(expenses)

def test_ex_3_3_top_expense():
    from exercises.ex_3_3_top_expense import top_expense
    assert top_expense({"food": 500, "rent": 1000, "travel": 150}) == ("rent", 1000)
    assert top_expense({"a": 10}) == ("a", 10)

def test_ex_3_4_over_budget():
    from exercises.ex_3_4_over_budget import over_budget
    expenses = {"food": 500, "rent": 1000, "travel": 300}
    limits   = {"food": 400, "rent": 1200, "travel": 200}
    result = over_budget(expenses, limits)
    assert result == {"food": (500, 400), "travel": (300, 200)}
    print(result)


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
