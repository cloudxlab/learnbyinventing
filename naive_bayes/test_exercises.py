#!/usr/bin/env python3
"""Test runner for naive_bayes exercises. Run: python test_exercises.py"""
import sys
import os
import math

sys.path.insert(0, os.path.dirname(__file__))

data = [
    {"Outlook": "Sunny",    "Temperature": "Hot",  "Humidity": "High",   "Wind": "Weak",   "Play": "No"},
    {"Outlook": "Sunny",    "Temperature": "Hot",  "Humidity": "High",   "Wind": "Strong", "Play": "No"},
    {"Outlook": "Overcast", "Temperature": "Hot",  "Humidity": "High",   "Wind": "Weak",   "Play": "Yes"},
    {"Outlook": "Rainy",    "Temperature": "Mild", "Humidity": "High",   "Wind": "Weak",   "Play": "Yes"},
    {"Outlook": "Rainy",    "Temperature": "Cool", "Humidity": "Normal", "Wind": "Weak",   "Play": "Yes"},
    {"Outlook": "Rainy",    "Temperature": "Cool", "Humidity": "Normal", "Wind": "Strong", "Play": "No"},
    {"Outlook": "Overcast", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Strong", "Play": "Yes"},
    {"Outlook": "Sunny",    "Temperature": "Mild", "Humidity": "High",   "Wind": "Weak",   "Play": "No"},
    {"Outlook": "Sunny",    "Temperature": "Cool", "Humidity": "Normal", "Wind": "Weak",   "Play": "Yes"},
    {"Outlook": "Rainy",    "Temperature": "Mild", "Humidity": "Normal", "Wind": "Weak",   "Play": "Yes"},
    {"Outlook": "Sunny",    "Temperature": "Mild", "Humidity": "Normal", "Wind": "Strong", "Play": "Yes"},
    {"Outlook": "Overcast", "Temperature": "Mild", "Humidity": "High",   "Wind": "Strong", "Play": "Yes"},
    {"Outlook": "Overcast", "Temperature": "Hot",  "Humidity": "Normal", "Wind": "Weak",   "Play": "Yes"},
    {"Outlook": "Rainy",    "Temperature": "Mild", "Humidity": "High",   "Wind": "Strong", "Play": "No"},
]


def test_ex_2_4_count_where():
    from exercises.ex_2_4_count_where import count_where
    assert count_where(data, {"Play": "Yes"}) == 9
    assert count_where(data, {"Play": "No"}) == 5
    assert count_where(data, {"Outlook": "Sunny", "Play": "Yes"}) == 2
    assert count_where(data, {"Outlook": "Sunny", "Play": "No"}) == 3
    assert count_where(data, {"Outlook": "Overcast"}) == 4
    assert count_where(data, {"Outlook": "Overcast", "Play": "No"}) == 0

def test_ex_2_5_probability():
    from exercises.ex_2_5_probability import probability
    assert abs(probability(data, {"Outlook": "Sunny"}, {"Play": "Yes"}) - 2/9) < 0.001
    assert abs(probability(data, {"Outlook": "Sunny"}, {"Play": "No"}) - 3/5) < 0.001
    assert abs(probability(data, {"Wind": "Strong"}, {"Play": "Yes"}) - 3/9) < 0.001
    assert abs(probability(data, {"Wind": "Strong"}, {"Play": "No"}) - 3/5) < 0.001

def test_ex_2_6_predict_one_feature():
    from exercises.ex_2_6_predict_one_feature import predict_one_feature
    assert predict_one_feature(data, "Outlook", "Sunny", "Play", ["Yes", "No"]) == "No"
    assert predict_one_feature(data, "Outlook", "Overcast", "Play", ["Yes", "No"]) == "Yes"
    assert predict_one_feature(data, "Outlook", "Rainy", "Play", ["Yes", "No"]) == "Yes"
    assert predict_one_feature(data, "Wind", "Strong", "Play", ["Yes", "No"]) == "No"
    assert predict_one_feature(data, "Wind", "Weak", "Play", ["Yes", "No"]) == "Yes"

def test_ex_3_3_predict_two_features():
    from exercises.ex_3_3_predict_two_features import predict_two_features
    assert predict_two_features(data, "Outlook", "Sunny", "Temperature", "Hot",
                                "Play", ["Yes", "No"]) == "No"
    assert predict_two_features(data, "Outlook", "Rainy", "Temperature", "Cool",
                                "Play", ["Yes", "No"]) == "Yes"
    assert predict_two_features(data, "Outlook", "Overcast", "Temperature", "Mild",
                                "Play", ["Yes", "No"]) == "Yes"
    assert predict_two_features(data, "Outlook", "Sunny", "Wind", "Strong",
                                "Play", ["Yes", "No"]) == "No"

def test_ex_4_2_predict():
    from exercises.ex_4_2_predict import predict
    assert predict(data, {"Outlook": "Sunny", "Temperature": "Hot", "Humidity": "High"},
                   "Play", ["Yes", "No"]) == "No"
    assert predict(data, {"Outlook": "Overcast", "Temperature": "Mild", "Humidity": "Normal"},
                   "Play", ["Yes", "No"]) == "Yes"
    assert predict(data, {"Outlook": "Rainy", "Temperature": "Cool",
                          "Humidity": "Normal", "Wind": "Weak"},
                   "Play", ["Yes", "No"]) == "Yes"
    assert predict(data, {"Outlook": "Sunny", "Temperature": "Hot",
                          "Humidity": "High", "Wind": "Strong"},
                   "Play", ["Yes", "No"]) == "No"

def test_ex_5_2_probability_smooth():
    from exercises.ex_5_2_probability_smooth import probability_smooth
    assert abs(probability_smooth(data, {"Outlook": "Overcast"}, {"Play": "No"}, 3) - 1/8) < 0.001
    assert abs(probability_smooth(data, {"Outlook": "Sunny"}, {"Play": "No"}, 3) - 0.5) < 0.001
    assert abs(probability_smooth(data, {"Outlook": "Sunny"}, {"Play": "Yes"}, 3) - 0.25) < 0.001

def test_ex_5_3_predict_smooth():
    from exercises.ex_5_3_predict_smooth import predict_smooth
    assert predict_smooth(data, {"Outlook": "Sunny", "Temperature": "Hot",
                                 "Humidity": "High", "Wind": "Strong"},
                          "Play", ["Yes", "No"]) == "No"
    assert predict_smooth(data, {"Outlook": "Overcast", "Temperature": "Mild",
                                 "Humidity": "Normal", "Wind": "Weak"},
                          "Play", ["Yes", "No"]) == "Yes"
    assert predict_smooth(data, {"Outlook": "Overcast", "Temperature": "Hot",
                                 "Humidity": "High", "Wind": "Strong"},
                          "Play", ["Yes", "No"]) == "Yes"

def test_ex_6_2_naive_bayes():
    from exercises.ex_6_2_naive_bayes import NaiveBayes
    X = [{"Outlook": row["Outlook"], "Temperature": row["Temperature"],
          "Humidity": row["Humidity"], "Wind": row["Wind"]} for row in data]
    y = [row["Play"] for row in data]
    nb = NaiveBayes()
    nb.fit(X, y)
    preds = nb.predict([
        {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": "High", "Wind": "Strong"},
        {"Outlook": "Overcast", "Temperature": "Hot", "Humidity": "Normal", "Wind": "Weak"},
        {"Outlook": "Rainy", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Weak"},
    ])
    assert preds == ["No", "Yes", "Yes"]


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
