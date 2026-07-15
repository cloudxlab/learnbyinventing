# Compose a Simple k-Nearest-Neighbors Classifier
# Write your solution below. Run this file to test: python exercises/05_medium_knn_predict_function.py

def euclidean_distance(p1, p2):
    """Provided utility -- already implemented, no need to change."""
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5


def knn_classify(point, training_points, training_labels, k=3):
    """Classify `point` using k-Nearest Neighbors.

    TODO:
      1. Compute the distance from `point` to every point in training_points
         (use euclidean_distance).
      2. Find the k closest training points.
      3. Return whichever label is most common among those k neighbors.
    """
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    training_points = [(1, 1), (1, 2), (2, 1), (8, 8), (8, 9), (9, 8)]
    training_labels = ["A", "A", "A", "B", "B", "B"]

    assert knn_classify((1.5, 1.5), training_points, training_labels, k=3) == "A"
    assert knn_classify((8.5, 8.5), training_points, training_labels, k=3) == "B"
    print("PASS")
