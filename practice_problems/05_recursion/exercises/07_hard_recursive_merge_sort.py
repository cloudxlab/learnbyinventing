# Recursive Merge Sort (to Find the Median)
# Write your solution below. Run this file to test: python exercises/07_hard_recursive_merge_sort.py

def merge(left, right):
    """Provided utility -- merge two already-sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(data):
    """Recursively sort `data` using merge sort.

    TODO:
      base case: a list of 0 or 1 elements is already sorted
      recursive case: split data in half, recursively sort each half,
      then combine them with merge(left_sorted, right_sorted)
    """
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import random

    random.seed(8)
    for _ in range(6):
        sample = [random.randint(-50, 50) for _ in range(random.randint(0, 12))]
        assert merge_sort(sample) == sorted(sample), f"merge_sort({sample}) is wrong"
    print("PASS")
