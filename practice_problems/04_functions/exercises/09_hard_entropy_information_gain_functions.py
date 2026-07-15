# Compose entropy() and information_gain()
# Write your solution below. Run this file to test: python exercises/09_hard_entropy_information_gain_functions.py

import math
from collections import Counter


def entropy(labels):
    """Provided utility -- already implemented, no need to change."""
    if not labels:
        return 0.0
    n = len(labels)
    counts = Counter(labels)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def information_gain(parent_labels, left_labels, right_labels):
    """Return the information gain from splitting parent_labels into
    left_labels and right_labels.

    TODO: implement using entropy(parent_labels), entropy(left_labels),
    and entropy(right_labels), weighting left/right by their sizes.
    """
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    from collections import Counter


    def ref_entropy(labels):
        if not labels:
            return 0.0
        n = len(labels)
        counts = Counter(labels)
        return -sum((c / n) * math.log2(c / n) for c in counts.values())


    parent = ["yes", "yes", "no", "no", "yes", "no"]
    left = ["yes", "yes", "yes"]
    right = ["no", "no", "no"]
    n = len(parent)
    expected = ref_entropy(parent) - (len(left) / n * ref_entropy(left) + len(right) / n * ref_entropy(right))

    assert math.isclose(information_gain(parent, left, right), expected), \
        f"Expected {expected}, got {information_gain(parent, left, right)}"
    assert information_gain(parent, left, right) > 0.9, "a perfect split should have high information gain"
    print("PASS")
