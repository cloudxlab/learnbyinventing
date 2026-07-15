#!/usr/bin/env python3
"""Test runner for classes_and_objects exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_customer():
    from exercises.ex_1_1_customer import Customer
    c = Customer("Sandeep", "India")
    assert c.name == "Sandeep"
    assert c.place == "India"
    assert c.describe() == "Sandeep from India"
    c2 = Customer("Nitin", "Bharat")
    assert c2.describe() == "Nitin from Bharat"

def test_ex_2_1_twopointline():
    from exercises.ex_2_1_twopointline import TwoPointLine
    model = TwoPointLine()
    model.fit([2, 5], [3, 9])            # the points (2, 3) and (5, 9)
    assert model.predict([3, 0, 5]) == [5.0, -1.0, 9.0]

    thermo = TwoPointLine()
    thermo.fit([1, 2], [30, 35])         # the thermometer calibration
    assert thermo.predict([3]) == [40.0]
    assert thermo.predict([2.1]) == [35.5]

    # two models live side by side without interfering:
    assert model.predict([2]) == [3.0]

def test_ex_2_2_twopointline():
    from exercises.ex_2_2_twopointline import TwoPointLine
    model = TwoPointLine()
    try:
        model.fit([1, 2, 3], [1, 2, 3])
        assert False, "fit should have raised ValueError"
    except ValueError:
        pass

    model.fit([2, 5], [3, 9])
    assert model.predict([2]) == [3.0]

def test_ex_3_1_animal():
    from exercises.ex_3_1_animal import Animal
    from exercises.ex_3_1_animal import Dog
    from exercises.ex_3_1_animal import Cat
    d = Dog()
    assert d.eat() == "eating"          # inherited: Dog never defines eat
    assert d.bark() == "woof!"
    assert Cat().eat() == "eating"
    assert Cat().meow() == "meow"
    assert isinstance(d, Animal)        # a Dog IS an Animal

def test_ex_4_1_node():
    from exercises.ex_4_1_node import Node
    tree = Node(10,
                Node(4, Node(1), Node(11)),
                Node(5, Node(15), Node(16)))
    assert tree.total() == 62
    assert tree.count() == 7
    assert Node(42).total() == 42
    assert Node(42).count() == 1

def test_ex_4_2_node():
    from exercises.ex_4_2_node import Node
    tree = Node(10,
                Node(4, Node(1), Node(11)),
                Node(5, Node(15), Node(16)))
    assert tree.min_val() == 1
    assert tree.max_val() == 16
    assert tree.find(11) == True
    assert tree.find(99) == False
    assert tree.max_depth() == 3
    assert Node(7).max_depth() == 1

    tree.apply(lambda v: v * 2)
    assert tree.total() == 124
    assert tree.min_val() == 2

def test_ex_5_1_decisionnode():
    from exercises.ex_5_1_decisionnode import DecisionNode
    from exercises.ex_5_1_decisionnode import Yes
    from exercises.ex_5_1_decisionnode import No
    # the offer tree: salary -> learningOpp -> dist
    dist = DecisionNode("dist", 1, Yes(), No())            # close enough -> Yes
    learning = DecisionNode("learningOpp", 1, No(), dist)  # no learning -> No
    offer_tree = DecisionNode("salary", 1, No(), learning) # low salary -> No

    assert offer_tree.answer({"salary": 2,   "learningOpp": 3, "dist": 0.5}) == True
    assert offer_tree.answer({"salary": 0.5, "learningOpp": 3, "dist": 0.5}) == False
    assert offer_tree.answer({"salary": 2,   "learningOpp": 0, "dist": 0.5}) == False
    assert offer_tree.answer({"salary": 2,   "learningOpp": 3, "dist": 5})   == False

def test_ex_6_1_to_dict():
    from exercises.ex_6_1_to_dict import to_dict
    from exercises.ex_6_1_to_dict import from_dict
    d = to_dict(offer_tree)
    assert d["criteria"] == "salary"
    assert d["boundary"] == 1
    assert d["left"] == {"leaf": False}

    with open("offer_tree.json", "w") as f:
        json.dump(d, f)
    with open("offer_tree.json") as f:
        loaded = from_dict(json.load(f))

    for case in [{"salary": 2,   "learningOpp": 3, "dist": 0.5},
                 {"salary": 0.5, "learningOpp": 3, "dist": 0.5},
                 {"salary": 2,   "learningOpp": 0, "dist": 0.5},
                 {"salary": 2,   "learningOpp": 3, "dist": 5}]:
        assert loaded.answer(case) == offer_tree.answer(case)


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
