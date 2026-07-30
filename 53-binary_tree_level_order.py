# Binary Tree Level Order Traversal
# Return the node values level by level, top to bottom, left to right - one inner list
# per level.
# Example: root=[1,2,3,4,5,6,7] -> [[1],[2,3],[4,5,6,7]]
#          root=[]              -> []


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


# Case 1: Optimal: BFS, draining exactly one level per outer iteration
from collections import deque

def level_order(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)        # snapshot: how many nodes are on THIS level
        level = []

        for _ in range(level_size):    # pop exactly that many, no more
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)
    return result
# Time:  O(n)   each node enters and leaves the queue once
# Space: O(width)   the queue holds at most one level plus its children
# Capturing len(queue) BEFORE the inner loop is the whole trick - it separates the
# current level from the children being appended during the same iteration.


# Case 2: DFS carrying the depth, appending into the right bucket
def level_order_dfs(root):
    result = []

    def dfs(node, depth):
        if not node:
            return
        if depth == len(result):
            result.append([])          # first time we reach this depth: open a bucket
        result[depth].append(node.val)
        dfs(node.left, depth + 1)      # left first, so each level stays left-to-right
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return result
# Time:  O(n)
# Space: O(h) recursion + O(n) output


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4, 5, 6, 7], [[1], [2, 3], [4, 5, 6, 7]]),
        ([], []),
        ([1], [[1]]),
        ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
        ([1, 2, None, 3], [[1], [2], [3]]),      # a left-leaning chain
        ([1, None, 2, None, 3], [[1], [2], [3]]),
    ]
    for values, expected in cases:
        got = level_order(build(values))
        print(values, "->", got, got == expected)

    print(level_order_dfs(build([3, 9, 20, None, None, 15, 7])))   # [[3],[9,20],[15,7]]
