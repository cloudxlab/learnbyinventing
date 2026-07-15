#!/usr/bin/env python3
"""Test runner for trees_and_heaps exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_evaluate():
    from exercises.ex_1_1_evaluate import evaluate
    assert evaluate(expr) == 10
    assert evaluate(Node(42)) == 42
    assert evaluate(Node("-", Node(10), Node(4))) == 6

def test_ex_2_1_insert():
    from exercises.ex_2_1_insert import insert
    root = None
    for v in [10, 12, 1, 11, 13, 3]:
        root = insert(root, v)

    print_tree(root)
    assert root.val == 10
    assert root.left.val == 1
    assert root.right.val == 12
    assert root.left.right.val == 3
    assert root.right.left.val == 11
    assert root.right.right.val == 13

def test_ex_2_2_contains():
    from exercises.ex_2_2_contains import contains
    assert contains(root, 11) == True
    assert contains(root, 10) == True
    assert contains(root, 13) == True
    assert contains(root, 7)  == False
    assert contains(None, 5)  == False

def test_ex_2_3_in_order():
    from exercises.ex_2_3_in_order import in_order
    result = in_order(root)
    print(result)
    assert result == [1, 3, 10, 11, 12, 13]

    # tree sort on random data:
    values = random.sample(range(1000), 50)
    r = None
    for v in values:
        r = insert(r, v)
    assert in_order(r) == sorted(values)

def test_ex_2_4_find_min():
    from exercises.ex_2_4_find_min import find_min
    assert find_min(root) == 1
    assert find_min(root.right) == 11
    assert find_min(Node(42)) == 42

def test_ex_2_5_delete():
    from exercises.ex_2_5_delete import delete
    # rebuild a fresh tree
    root = None
    for v in [10, 12, 1, 11, 13, 3]:
        root = insert(root, v)

    root = delete(root, 1)              # case: node with one child (1 has right child 3)
    assert in_order(root) == [3, 10, 11, 12, 13]

    root = delete(root, 13)             # case: leaf
    assert in_order(root) == [3, 10, 11, 12]

    root = delete(root, 10)             # case: two children (the root itself!)
    assert in_order(root) == [3, 11, 12]

    root = delete(root, 99)             # deleting a missing value changes nothing
    assert in_order(root) == [3, 11, 12]

    # stress test: delete everything in random order
    values = random.sample(range(500), 100)
    r = None
    for v in values:
        r = insert(r, v)
    random.shuffle(values)
    remaining = sorted(values)
    for v in values:
        r = delete(r, v)
        remaining.remove(v)
        assert in_order(r) == remaining, f"tree broken after deleting {v}"

def test_ex_3_1_parent():
    from exercises.ex_3_1_parent import parent
    from exercises.ex_3_1_parent import left_child
    from exercises.ex_3_1_parent import right_child
    assert parent(3) == 1 and parent(4) == 1 and parent(1) == 0 and parent(2) == 0
    assert left_child(0) == 1 and right_child(0) == 2
    assert left_child(1) == 3 and right_child(1) == 4

def test_ex_3_2_heap_push():
    from exercises.ex_3_2_heap_push import heap_push
    h = [1, 3, 2, 8, 5]
    heap_push(h, 0)
    assert h == [0, 3, 1, 8, 5, 2]

    h = []
    for v in [5, 3, 8, 1]:
        heap_push(h, v)
    assert h[0] == 1, "minimum must be at the root"

def test_ex_3_3_heap_pop():
    from exercises.ex_3_3_heap_pop import heap_pop
    h = [1, 3, 2, 8, 5]
    assert heap_pop(h) == 1
    assert heap_pop(h) == 2
    assert heap_pop(h) == 3
    assert heap_pop(h) == 5
    assert heap_pop(h) == 8
    assert h == []

    # stress: pushes and pops always yield values in sorted order
    values = [random.randint(0, 1000) for _ in range(500)]
    h = []
    for v in values:
        heap_push(h, v)
    popped = [heap_pop(h) for _ in range(len(values))]
    assert popped == sorted(values)

def test_ex_3_4_run_scheduler():
    from exercises.ex_3_4_run_scheduler import run_scheduler
    order = run_scheduler([(1300, "task1"), (1230, "task2"), (1400, "task3"), (1100, "task4")])
    assert order == ["task4", "task2", "task1", "task3"]

def test_ex_3_5_heap_sort():
    from exercises.ex_3_5_heap_sort import heap_sort
    assert heap_sort([5, 2, 9, 1]) == [1, 2, 5, 9]
    assert heap_sort([]) == []

    # agree with the standard library on random data
    data = [random.randint(0, 100) for _ in range(200)]
    mine = list(data)
    h = []
    for v in mine:
        heap_push(h, v)

    theirs = list(data)
    heapq.heapify(theirs)

    assert heap_pop(h) == heapq.heappop(theirs)
    assert heap_pop(h) == heapq.heappop(theirs)
    assert heap_pop(h) == heapq.heappop(theirs)

def test_ex_4_1_in_order_iter():
    from exercises.ex_4_1_in_order_iter import in_order_iter
    assert in_order_iter(root) == in_order(root)
    assert in_order_iter(None) == []

    values = random.sample(range(1000), 100)
    r = None
    for v in values:
        r = insert(r, v)
    assert in_order_iter(r) == sorted(values)

def test_ex_4_2_parse():
    from exercises.ex_4_2_parse import parse
    assert evaluate(parse("((3+4)*(9-10))")) == -7
    assert evaluate(parse("(((3*4)+7)-12)")) == 7
    assert evaluate(parse("(2+3)")) == 5

    leaf = parse("42")
    assert leaf.val == 42
    assert leaf.left is None and leaf.right is None

    print_tree(parse("((3+4)*(9-10))"))


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
