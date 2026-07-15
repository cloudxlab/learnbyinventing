# Build a Confusion Matrix Over a Dataset
# Write your solution below. Run this file to test: python exercises/07_hard_confusion_matrix_loop.py

actual    = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
predicted = [1, 0, 0, 1, 0, 1, 1, 0, 1, 1]

# TODO: loop through actual & predicted together (zip) and count each case
tp = fp = tn = fn = 0


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    expected_tp = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 1)
    expected_fp = sum(1 for a, p in zip(actual, predicted) if a == 0 and p == 1)
    expected_tn = sum(1 for a, p in zip(actual, predicted) if a == 0 and p == 0)
    expected_fn = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 0)

    assert (tp, fp, tn, fn) == (expected_tp, expected_fp, expected_tn, expected_fn), \
        f"Expected (tp,fp,tn,fn)={(expected_tp, expected_fp, expected_tn, expected_fn)}, got {(tp, fp, tn, fn)}"
    print("PASS")
