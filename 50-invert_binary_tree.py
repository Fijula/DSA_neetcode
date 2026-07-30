# Invert Binary Tree
# Swap every node's left and right child, producing the mirror image of the tree.
# Example:     1          becomes      1
#             / \                     / \
#            2   3                   3   2
#           /                             \
#          4                               4


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    """Level-order list -> tree. None marks a missing node."""
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


def to_level_order(root):
    """Tree -> level-order list, with trailing Nones trimmed."""
    if not root:
        return []
    result, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result and result[-1] is None:
        result.pop()
    return result


# Case 1: Recursive DFS: swap the children, then invert each subtree
def invert_tree(root):
    if not root:
        return None

    root.left, root.right = root.right, root.left   # swap at this node
    invert_tree(root.left)                          # then fix everything below
    invert_tree(root.right)
    return root
# Time:  O(n)   every node is swapped once
# Space: O(h)   recursion depth
# The swap can go before OR after the recursive calls - both work, because each node's
# swap is independent of its descendants'.


# Case 2: Iterative BFS with a queue
from collections import deque

def invert_tree_bfs(root):
    if not root:
        return None

    queue = deque([root])
    while queue:
        node = queue.popleft()
        node.left, node.right = node.right, node.left
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return root
# Time:  O(n)
# Space: O(width of the widest level)


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4], [1, 3, 2, None, None, None, 4]),
        ([], []),
        ([1], [1]),
        ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1]),
        ([1, 2], [1, None, 2]),
    ]
    for values, expected in cases:
        got = to_level_order(invert_tree(build(values)))
        print(values, "->", got, got == expected)

    print(to_level_order(invert_tree_bfs(build([4, 2, 7, 1, 3, 6, 9]))))
