#!/usr/bin/env python3
"""Test runner for random_forest exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_variance():
    from exercises.ex_1_1_variance import variance
    assert variance([10, 10, 10, 10, 10]) == 0
    assert variance([1, 50, 3, 80]) == 1105.25
    assert variance([1, 3]) == 1.0
    assert variance([4]) == 0

def test_ex_1_2_total_variance():
    from exercises.ex_1_2_total_variance import total_variance
    assert total_variance([10, 10, 10], [0, 0, 0]) == 0.0
    assert abs(total_variance([10, 9, 11, 8, 10], [1]) - 0.8667) < 1e-3
    assert total_variance([5], [5]) == 0.0

def test_ex_1_3_variance_reduction():
    from exercises.ex_1_3_variance_reduction import variance_reduction
    values = [10, 9, 11, 8, 10, 1]
    assert abs(variance(values) - 11.1389) < 1e-3

    good = variance_reduction(values, [10, 9, 11, 8, 10], [1])
    bad = variance_reduction(values, [10, 9, 11], [8, 10, 1])
    print("good split:", round(good, 4), " bad split:", round(bad, 4))
    assert abs(good - 10.2722) < 1e-3
    assert good > bad

def test_ex_2_2_find_best_split():
    from exercises.ex_2_2_find_best_split import find_best_split
    f, t, red = find_best_split(X, y)
    print("best split: feature", f, "threshold", t, "reduction", round(red, 2))
    assert f == 0
    assert abs(t - 1200) < 1e-9
    assert abs(red - 2669.44) < 0.1
    assert find_best_split([[1, 1]], [10]) == (None, None, 0.0)

def test_ex_3_1_decisiontreeregressor():
    from exercises.ex_3_1_decisiontreeregressor import DecisionTreeRegressor
    # A deep tree memorizes this tiny dataset perfectly...
    deep = DecisionTreeRegressor(max_depth=5, min_samples_split=2)
    deep.fit(X, y)
    assert root_mean_squared_error(y, deep.predict(X)) < 1e-9

    # ...a depth-1 "stump" can only ask one question, so it must generalize:
    stump = DecisionTreeRegressor(max_depth=1, min_samples_split=2)
    stump.fit(X, y)
    assert root_mean_squared_error(y, stump.predict(X)) > 5

    p = deep.predict([[550, 1], [2000, 5]])
    print("predictions for a 550 sqft and a 2000 sqft house:", p)
    assert 50 <= p[0] <= 65
    assert 150 <= p[1] <= 170

def test_ex_4_1_bootstrap_sample():
    from exercises.ex_4_1_bootstrap_sample import bootstrap_sample
    X16 = [[500, 1], [550, 1], [600, 1], [650, 2], [700, 2], [800, 2], [900, 2],
           [1200, 3], [1300, 3], [1400, 3], [1500, 3], [1600, 3],
           [1700, 4], [1800, 4], [1900, 4], [2000, 4]]
    y16 = [48, 54, 57, 64, 66, 95, 81, 120, 127, 136, 149, 157, 171, 205, 189, 197]

    random.seed(7)
    Xs, ys = bootstrap_sample(X16, y16)
    assert len(Xs) == len(X16) and len(ys) == len(y16)
    assert all(row in X16 for row in Xs)
    assert all(ys[i] == y16[X16.index(Xs[i])] for i in range(len(Xs)))
    assert Xs != X16    # drawing the original order back is astronomically unlikely

def test_ex_4_2_choose_features():
    from exercises.ex_4_2_choose_features import choose_features
    feats = choose_features(4, 2)
    print("this tree may only ask about features:", feats)
    assert len(feats) == 2
    assert len(set(feats)) == 2
    assert set(feats) <= {0, 1, 2, 3}

def test_ex_5_1_randomforestregressor():
    from exercises.ex_5_1_randomforestregressor import RandomForestRegressor
    X_test = [[575, 1], [750, 2], [1350, 3], [1650, 3], [1950, 4]]
    y_test = [55, 70, 132, 165, 192]

    random.seed(42)
    rf = RandomForestRegressor(n_estimators=20, max_depth=3,
                               min_samples_split=2, max_features=1)
    rf.fit(X16, y16)
    assert len(rf.trees) == 20

    rf_train = root_mean_squared_error(y16, rf.predict(X16))
    rf_test = root_mean_squared_error(y_test, rf.predict(X_test))

    single = DecisionTreeRegressor(max_depth=10, min_samples_split=2)
    single.fit(X16, y16)
    single_train = root_mean_squared_error(y16, single.predict(X16))
    single_test = root_mean_squared_error(y_test, single.predict(X_test))

    print(f"single tree — train RMSE {single_train:6.2f}   test RMSE {single_test:6.2f}")
    print(f"forest (20) — train RMSE {rf_train:6.2f}   test RMSE {rf_test:6.2f}")
    assert rf_train < 30 and rf_test < 30


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
