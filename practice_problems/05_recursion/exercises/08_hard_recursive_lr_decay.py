# Recursive Learning-Rate Decay Schedule
# Write your solution below. Run this file to test: python exercises/08_hard_recursive_lr_decay.py

def decayed_lr(initial_lr, decay, n):
    """Return the learning rate after n decay steps, using recursion."""
    # TODO: base case -- n == 0
    # TODO: recursive case
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    initial_lr, decay = 0.1, 0.9
    for n in range(0, 10):
        expected = initial_lr * decay ** n
        assert math.isclose(decayed_lr(initial_lr, decay, n), expected), f"decayed_lr(.., {n}) is wrong"
    print("PASS")
