#!/usr/bin/env python3
"""Test runner for pattern_matching exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_match_exact():
    from exercises.ex_1_1_match_exact import match_exact
    assert match_exact("abc", "abc")   == True
    assert match_exact("abc", "abd")   == False
    assert match_exact("abc", "abcd")  == False
    assert match_exact("abcd", "abc")  == False
    assert match_exact("", "")         == True
    assert match_exact("", "a")        == False

def test_ex_2_1_match_q():
    from exercises.ex_2_1_match_q import match_q
    assert match_q("a?c", "abc")  == True
    assert match_q("a?c", "axc")  == True
    assert match_q("a?c", "ac")   == False
    assert match_q("a?c", "abcd") == False
    assert match_q("???", "xyz")  == True
    assert match_q("a?", "a1")    == True
    assert match_q("a?", "a")     == False
    assert match_q("abc", "abc")  == True

def test_ex_3_1_match():
    from exercises.ex_3_1_match import match
    # literals and ? still work
    assert match("abc", "abc")  == True
    assert match("a?c", "axc")  == True

    # star
    assert match("a*", "a")     == True
    assert match("a*", "ab")    == True
    assert match("a*", "abc")   == True
    assert match("a*b", "ab")       == True
    assert match("a*b", "axyzb")    == True
    assert match("a*b", "a123b")    == True
    assert match("a*b", "axyz")     == False
    assert match("a*b*c", "abc")    == True
    assert match("a*b*c", "abbbc")  == True
    assert match("a*b*c", "a1b1c")  == True
    assert match("a*b*c", "a1c1b")  == False

    # combined
    assert match("aa?b*", "aa1b")                 == True
    assert match("aa?b*", "aaxby")                == True
    assert match("aa?b*", "aa1bcdeffgshshshsh")   == True
    assert match("aa?b*", "aab")                  == False
    assert match("aa?b*", "ab")                   == False

    # edge cases
    assert match("*", "")           == True
    assert match("*", "anything")   == True
    assert match("", "")            == True
    assert match("", "x")           == False

def test_ex_3_3_find_matching():
    from exercises.ex_3_3_find_matching import find_matching
    files = ["report.txt", "report.pdf", "data1.csv", "data2.csv", "notes.txt", "img.png"]
    assert find_matching("*.txt", files)     == ["report.txt", "notes.txt"]
    assert find_matching("data?.csv", files) == ["data1.csv", "data2.csv"]
    assert find_matching("report.*", files)  == ["report.txt", "report.pdf"]
    assert find_matching("*", files)         == files

def test_ex_4_2_is_valid_date():
    from exercises.ex_4_2_is_valid_date import is_valid_date
    assert is_valid_date("05/07/1980") == True
    assert is_valid_date("31/08/1980") == True
    assert is_valid_date("05-11-1980") == True
    assert is_valid_date("30/08/1980") == True
    assert is_valid_date("99/07/1980") == False
    assert is_valid_date("05/19/1980") == False
    assert is_valid_date("00/04/1980") == False
    assert is_valid_date("01/00/1980") == False
    assert is_valid_date("05/88/1980") == False

def test_ex_4_3_find_card_numbers():
    from exercises.ex_4_3_find_card_numbers import find_card_numbers
    result = find_card_numbers("cc: 1234-4567-8909-1111 and 1234 4567 8909 1111 and 1234456789091111")
    assert result == ["1234-4567-8909-1111", "1234 4567 8909 1111", "1234456789091111"], result
    assert find_card_numbers("call me at 12345") == []

def test_ex_4_4_find_emails():
    from exercises.ex_4_4_find_emails import find_emails
    result = find_emails("Contact sandeep@example.com or admin.team@my-site.org today")
    assert result == ["sandeep@example.com", "admin.team@my-site.org"], result
    assert find_emails("no emails here @ nothing") == []

def test_ex_4_5_find_urls():
    from exercises.ex_4_5_find_urls import find_urls
    urls = find_urls(LOG_LINES)
    print(f"Found {len(urls)} URLs:")
    for u in urls:
        print("  ", u)

    assert len(urls) == 6
    assert "http://yandex.com/bots" in urls
    assert "http://www.knowbigdata.com/page/course-page-big-data-and-hadoop" in urls
    assert all(u.startswith("http") for u in urls)


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
