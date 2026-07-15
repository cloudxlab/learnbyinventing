# Classify One Prediction (TP / FP / TN / FN)
# Write your solution below. Run this file to test: python exercises/04_medium_confusion_single.py

actual = 1
predicted = 0

# TODO: set category to "TP", "FP", "TN", or "FN" based on the table above
category = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    table = {(1, 1): "TP", (0, 1): "FP", (0, 0): "TN", (1, 0): "FN"}
    expected = table[(actual, predicted)]
    assert category == expected, f"Expected {expected!r}, got {category!r}"
    print("PASS")
