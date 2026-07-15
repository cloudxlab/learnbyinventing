# Exercise 7.3 — Build the Tree Recursively
# Write your solution in this file. Run test_exercises.py to check.

def build_tree(data, features, label):
    """
    Recursively builds a decision tree.
    
    data     : list of dicts
    features : list of feature names to split on
    label    : the target column name
    
    Returns a DecisionTreeNode (either leaf or boundary).
    """
    labels = [row[label] for row in data]

    # Base case 1: empty data
    if len(data) == 0:
        pass  # return a leaf — but with what label?

    # Base case 2: pure or single element
    if is_pure(labels) or len(data) == 1:
        pass  # return a leaf

    # Recursive case
    best_feat, best_thresh, best_imp = find_decision_boundary(data, features, label)

    left_data  = [row for row in data if row[best_feat] <= best_thresh]
    right_data = [row for row in data if row[best_feat] >  best_thresh]

    # Safety: if the split doesn't separate anything, stop
    if len(left_data) == 0 or len(right_data) == 0:
        pass  # return a leaf

    left_tree  = build_tree(left_data,  features, label)
    right_tree = build_tree(right_data, features, label)

    return DecisionTreeNode(
        boundary=best_feat,
        boundary_value=best_thresh,
        left=left_tree,
        right=right_tree
    )
