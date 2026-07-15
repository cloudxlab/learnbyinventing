# Recursive Binary Search Over Sorted Distances
# Write your solution below. Run this file to test: python exercises/06_medium_recursive_binary_search.py

def find_insert_index(sorted_list, value):
    """Return the index at which `value` should be inserted into
    sorted_list (ascending) to keep it sorted. Implement using
    recursive binary search (no loops, don't use the bisect module).
    """
    # TODO: implement recursive binary search
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import bisect
    import random

    random.seed(7)
    for _ in range(8):
        sorted_list = sorted(random.sample(range(-50, 50), 10))
        value = random.randint(-60, 60)
        assert find_insert_index(sorted_list, value) == bisect.bisect_left(sorted_list, value), \
            f"find_insert_index({sorted_list}, {value}) is wrong"
    print("PASS")
