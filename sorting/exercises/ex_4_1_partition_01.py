# Exercise 4.1 — Partition 0s and 1s
# Write your solution in this file. Run test_exercises.py to check.

def partition_01(lst):
    pass  # replace this: one pass, swaps only, no second list



def check_partition_01(original):
    lst = list(original)
    partition_01(lst)
    assert sorted(map(str, lst)) == sorted(map(str, original)), "elements changed!"
    keys = [k for k, v in lst]
    boundary = keys.count(0)
    assert all(k == 0 for k in keys[:boundary]), f"zeros not in front: {lst}"
    assert all(k == 1 for k in keys[boundary:]), f"ones not at back: {lst}"
