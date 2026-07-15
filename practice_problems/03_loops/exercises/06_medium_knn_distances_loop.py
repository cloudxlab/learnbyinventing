# Distances From a Query Point to a Training Set
# Write your solution below. Run this file to test: python exercises/06_medium_knn_distances_loop.py

query = (5, 5)
training_points = [(1, 2), (4, 4), (8, 9), (0, 0), (6, 5)]

# TODO: loop through training_points and compute the Euclidean distance
# from `query` to each one; store results in `distances`
distances = []


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math

    expected = [((query[0] - px) ** 2 + (query[1] - py) ** 2) ** 0.5 for px, py in training_points]
    assert len(distances) == len(training_points), "distances has the wrong length"
    assert all(math.isclose(a, b) for a, b in zip(distances, expected)), \
        f"Expected {expected}, got {distances}"
    print("PASS")
