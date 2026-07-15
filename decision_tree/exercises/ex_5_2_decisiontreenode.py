# Exercise 5.2 — Build the `DecisionTreeNode` Class
# Write your solution in this file. Run test_exercises.py to check.

class DecisionTreeNode:

    def __init__(self, decision=None, boundary=None, boundary_value=None, left=None, right=None):
        """
        A node in a decision tree.
        
        If decision is not None: this is a leaf node.
        Otherwise: this is a boundary node with boundary, boundary_value, left, right.
        """
        pass  # replace this


    def check(self, features):
        """
        Traverses the tree and returns the leaf's boolean decision.
        features: dict of {feature_name: value}
        Rule: go LEFT if features[boundary] <= boundary_value, else go RIGHT.
        """
        pass  # replace this



def YES():
    """Returns a leaf node that decides True (accept)."""
    pass



def NO():
    """Returns a leaf node that decides False (reject)."""
    pass
