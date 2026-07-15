# Decide Whether a Tree Node Is Pure
# Write your solution below. Run this file to test: python exercises/09_hard_pure_node.py

count_a = 8
count_b = 0

# TODO: classify the node as "pure", "mixed (balanced)", or "mixed"
node_status = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    if count_a == 0 or count_b == 0:
        expected = "pure"
    elif count_a == count_b:
        expected = "mixed (balanced)"
    else:
        expected = "mixed"
    assert node_status == expected, f"Expected {expected!r}, got {node_status!r}"
    print("PASS")
