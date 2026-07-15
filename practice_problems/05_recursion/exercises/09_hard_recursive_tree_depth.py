# Recursive Depth of a Decision Tree
# Write your solution below. Run this file to test: python exercises/09_hard_recursive_tree_depth.py

def tree_depth(node):
    """`node` is either {"leaf": <label>} or {"left": <node>, "right": <node>}.
    Return the maximum depth of the tree rooted at `node` (a lone leaf has depth 1).
    """
    # TODO: base case -- node is a leaf
    # TODO: recursive case -- 1 + max depth of the two children
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    def ref_depth(node):
        if "leaf" in node:
            return 1
        return 1 + max(ref_depth(node["left"]), ref_depth(node["right"]))


    tree = {
        "left": {"left": {"leaf": "A"}, "right": {"leaf": "B"}},
        "right": {"leaf": "C"},
    }
    assert tree_depth(tree) == ref_depth(tree) == 3, f"Expected 3, got {tree_depth(tree)}"
    assert tree_depth({"leaf": "X"}) == 1
    print("PASS")
