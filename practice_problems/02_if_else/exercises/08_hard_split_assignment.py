# Assign a Sample to Train, Validation, or Test by Position
# Write your solution below. Run this file to test: python exercises/08_hard_split_assignment.py

n = 10
train_ratio = 0.6
val_ratio = 0.2
i = 7

# TODO: compute train_end and val_end, then classify index i as "train"/"val"/"test"
split = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    train_end = n * train_ratio
    val_end = train_end + n * val_ratio
    expected = "train" if i < train_end else ("val" if i < val_end else "test")
    assert split == expected, f"Expected {expected!r}, got {split!r}"
    print("PASS")
