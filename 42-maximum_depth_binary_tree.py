# Maximum Depth of Binary Tree
# Return the number of nodes along the longest path from the root down to a leaf.
# An empty tree has depth 0.
# Example:     1          -> 3
#             / \
#            2   3
#               /
#              4


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# --- helper used by every tree file in this repo ---
def build(values):
    """Build a tree from a level-order list, using None for missing nodes.
    [1,2,3,None,None,4] gives the tree drawn above."""
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


# Case 1: Recursive DFS: depth = 1 + the deeper of the two subtrees
def max_depth(root):
    if not root:
        return 0                       # base case: an empty subtree adds nothing
    return 1 + max(max_depth(root.left), max_depth(root.right))
# Time:  O(n)   every node visited once
# Space: O(h)   recursion depth, h = height (O(n) if the tree is a chain)


# Case 2: Iterative BFS: count the levels as you peel them off
from collections import deque

def max_depth_bfs(root):
    if not root:
        return 0

    queue = deque([root])
    levels = 0
    while queue:
        # drain exactly one level per outer iteration
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels += 1
    return levels
# Time:  O(n)
# Space: O(width of the widest level)


# Case 3: Iterative DFS with an explicit stack of (node, depth)
def max_depth_iterative(root):
    stack = [(root, 1)] if root else []
    best = 0
    while stack:
        node, depth = stack.pop()
        best = max(best, depth)
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))
    return best
# Time: O(n), Space: O(h)


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, None, None, 4], 3),
        ([], 0),
        ([1], 1),
        ([1, 2, None, 3, None, 4], 4),           # a left-leaning chain
        ([3, 9, 20, None, None, 15, 7], 3),
        ([1, None, 2, None, 3], 3),              # a right-leaning chain
    ]
    for values, expected in cases:
        got = max_depth(build(values))
        print(values, "->", got, got == expected)

    print(max_depth_bfs(build([3, 9, 20, None, None, 15, 7])))         # 3
    print(max_depth_iterative(build([1, 2, None, 3, None, 4])))        # 4
