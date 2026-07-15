# Compose precision(), recall(), and f1_score()
# Write your solution below. Run this file to test: python exercises/06_medium_classification_metrics_functions.py

def precision(tp, fp):
    """Return tp / (tp + fp), or 0.0 if the denominator is 0."""
    # TODO: implement
    pass


def recall(tp, fn):
    """Return tp / (tp + fn), or 0.0 if the denominator is 0."""
    # TODO: implement
    pass


def f1_score(precision_value, recall_value):
    """Return the harmonic mean of precision and recall, or 0.0 if both are 0."""
    # TODO: implement
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    assert math.isclose(precision(8, 2), 0.8)
    assert math.isclose(precision(0, 0), 0.0)
    assert math.isclose(recall(8, 2), 0.8)
    assert math.isclose(recall(0, 0), 0.0)
    assert math.isclose(f1_score(0.8, 0.8), 0.8)
    assert math.isclose(f1_score(0.0, 0.0), 0.0)
    assert math.isclose(f1_score(1.0, 0.5), 2 * 1.0 * 0.5 / (1.0 + 0.5))
    print("PASS")
