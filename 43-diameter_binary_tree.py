# Diameter of Binary Tree
# The diameter is the number of EDGES on the longest path between any two nodes.
# That path does not have to pass through the root.
# Example:     1        -> 3   the path 4 -> 2 -> 1 -> 3 has 3 edges
#             / \
#            2   3
#           /
#          4


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values):
            if values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


# Case 1: Brute force: at every node, add up the heights of its two subtrees
def diameter_of_binary_tree_brute(root):
    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if not root:
        return 0

    # the longest path THROUGH this node, in edges
    through_here = height(root.left) + height(root.right)
    # ...or the answer lies entirely inside one of the subtrees
    return max(through_here,
               diameter_of_binary_tree_brute(root.left),
               diameter_of_binary_tree_brute(root.right))
# Time:  O(n^2)   height() is recomputed from scratch at every node
# Space: O(h)


# Case 2: Optimal: one DFS that returns height and updates the best diameter
def diameter_of_binary_tree(root):
    best = 0                           # tracked across the whole traversal

    def height(node):
        nonlocal best
        if not node:
            return 0                   # an empty subtree has height 0

        left = height(node.left)
        right = height(node.right)

        # the path bending at this node uses left + right edges
        best = max(best, left + right)

        return 1 + max(left, right)    # height reported up to the parent

    height(root)
    return best
# Time:  O(n)   each node's height is computed exactly once
# Space: O(h)   recursion depth
# The trick is doing two jobs in one traversal: the RETURN value feeds the parent's
# height, while the side effect on `best` records the best bend seen anywhere.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4], 3),
        ([1, 2, 3, None, None, 4], 3),
        ([], 0),
        ([1], 0),                      # a single node has no edges
        ([1, 2], 1),
        ([1, 2, 3, 4, 5], 3),          # 4 -> 2 -> 5 is 2 edges; 4 -> 2 -> 1 -> 3 is 3
        ([1, 2, None, 3, None, 4], 3),  # a chain of 4 nodes
    ]
    for values, expected in cases:
        got = diameter_of_binary_tree(build(values))
        print(values, "->", got, got == expected)

    print(diameter_of_binary_tree_brute(build([1, 2, 3, 4, 5])))   # 3
