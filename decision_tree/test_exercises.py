#!/usr/bin/env python3
"""Test runner for decision_tree exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_3_impurity():
    from exercises.ex_1_3_impurity import impurity
    # Verify the spec:
    print(impurity(0.5, 0.5))  # should be 1
    print(impurity(0, 1))      # should be 0
    print(impurity(1, 0))      # should be 0
    print(impurity(0.8, 0.2))  # should be between 0 and 1

    # Verify ordering:
    print(impurity(0.8, 0.2) < impurity(0.7, 0.3))  # should be True
    print(impurity(0.7, 0.3) < impurity(0.6, 0.4))  # should be True

def test_ex_2_1_list_impurity():
    from exercises.ex_2_1_list_impurity import list_impurity
    # Test cases
    test_cases = [
        ["R", "B", "B", "R", "R"],
        ["R", "R", "R", "R"],
        ["B", "B", "B", "B"],
        ["R", "B"],
        [],
    ]

    for lst in test_cases:
        print(f"{str(lst):<40}  impurity = {list_impurity(lst):.4f}")

def test_ex_2_2_total_impurity():
    from exercises.ex_2_2_total_impurity import total_impurity
    # Test cases
    print(total_impurity(["R", "R", "R"], ["B", "B", "B"]))  # perfectly separated → expect high certainty
    print(total_impurity(["R", "B", "R"], ["B", "R", "B"]))  # both mixed
    print(total_impurity(["R"]*9 + ["B"], ["B"]))            # unequal sizes

def test_ex_3_2_find_best_split_position():
    from exercises.ex_3_2_find_best_split_position import find_best_split_position
    # Test
    test_lists = [
        ["R", "B", "B", "R", "R"],
        ["R", "R", "R", "B", "B", "B"],
        ["B", "R", "B", "R", "B", "R"],
        ["R", "R", "R", "R", "B"],
    ]

    for lst in test_lists:
        best_k, min_imp = find_best_split_position(lst)
        print(f"List: {lst}")
        print(f"  Best k={best_k}: left={lst[:best_k]}, right={lst[best_k:]}")
        print(f"  Min impurity: {min_imp:.4f}")
        print()

def test_ex_4_3_split_by_threshold():
    from exercises.ex_4_3_split_by_threshold import split_by_threshold
    # Test manually
    left, right = split_by_threshold(heights, genders, 172)
    print("Left (height <= 172):", left)
    print("Right (height > 172):", right)
    print("Total impurity:", total_impurity(left, right))

def test_ex_4_4_find_best_threshold():
    from exercises.ex_4_4_find_best_threshold import find_best_threshold
    best_t, best_imp = find_best_threshold(heights, genders)
    print(f"Best threshold: height <= {best_t}")
    print(f"Minimum total impurity: {best_imp:.4f}")

    left, right = split_by_threshold(heights, genders, best_t)
    print(f"Left group:  {left}")
    print(f"Right group: {right}")

    plot_height_gender(heights, genders, split_height=best_t)

def test_ex_5_2_decisiontreenode():
    from exercises.ex_5_2_decisiontreenode import DecisionTreeNode
    from exercises.ex_5_2_decisiontreenode import __init__
    from exercises.ex_5_2_decisiontreenode import check
    from exercises.ex_5_2_decisiontreenode import YES
    from exercises.ex_5_2_decisiontreenode import NO
    assert DecisionTreeNode is not None

def test_ex_6_2_find_decision_boundary():
    from exercises.ex_6_2_find_decision_boundary import find_decision_boundary
    best_feat, best_thresh, best_imp = find_decision_boundary(data, ["height", "weight"], "gender")
    print(f"Best split: {best_feat} <= {best_thresh}")
    print(f"Minimum total impurity: {best_imp:.4f}")

    # What are the two groups?
    left_group = [row["gender"] for row in data if row[best_feat] <= best_thresh]
    right_group = [row["gender"] for row in data if row[best_feat] > best_thresh]
    print(f"Left  ({best_feat} <= {best_thresh}): {left_group}")
    print(f"Right ({best_feat} >  {best_thresh}): {right_group}")

def test_ex_7_2_majority_label():
    from exercises.ex_7_2_majority_label import majority_label
    from exercises.ex_7_2_majority_label import is_pure
    # Tests
    assert majority_label(["M", "M", "F", "M"]) == M
    print(majority_label(["F", "M"]))            # tie — what do you return?
    assert is_pure(["M", "M", "M"]) == True
    assert is_pure(["M", "M", "F"]) == False
    print(is_pure([]))                          # edge case — what do you return?

def test_ex_7_3_build_tree():
    from exercises.ex_7_3_build_tree import build_tree
    assert build_tree is not None

def test_ex_8_2_simpledecisiontree():
    from exercises.ex_8_2_simpledecisiontree import SimpleDecisionTree
    from exercises.ex_8_2_simpledecisiontree import __init__
    from exercises.ex_8_2_simpledecisiontree import fit
    from exercises.ex_8_2_simpledecisiontree import predict
    assert SimpleDecisionTree is not None

def test_ex_8_3_gini_impurity():
    from exercises.ex_8_3_gini_impurity import gini_impurity
    from exercises.ex_8_3_gini_impurity import entropy_impurity
    # Plot all three impurity measures on the same graph
    ps = [i/100 for i in range(101)]
    plt.figure(figsize=(8, 4))
    plt.plot(ps, [impurity(p, 1-p) for p in ps], label='Your formula')
    plt.plot(ps, [gini_impurity(p, 1-p) for p in ps], label='Gini', linestyle='--')
    plt.plot(ps, [entropy_impurity(p, 1-p) for p in ps], label='Entropy', linestyle=':')
    plt.xlabel('p'); plt.ylabel('impurity'); plt.title('Comparing impurity measures')
    plt.legend(); plt.grid(True)
    plt.show()


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
