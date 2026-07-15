# Compute the Entropy of a List of Labels
# Write your solution below. Run this file to test: python exercises/10_hard_entropy_loop.py

import math

labels = ["yes", "yes", "no", "yes", "no", "no", "yes", "yes"]

# TODO: count how many times each label occurs (loop + dict)
counts = {}

# TODO: use counts to compute entropy: -sum(p * log2(p)) for each class
entropy = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math
    from collections import Counter

    ref_counts = Counter(labels)
    n = len(labels)
    ref_entropy = -sum((c / n) * math.log2(c / n) for c in ref_counts.values())

    assert dict(counts) == dict(ref_counts), f"Expected counts {dict(ref_counts)}, got {dict(counts)}"
    assert math.isclose(entropy, ref_entropy), f"Expected {ref_entropy}, got {entropy}"
    print("PASS")
