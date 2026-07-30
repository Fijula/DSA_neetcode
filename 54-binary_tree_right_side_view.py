# Binary Tree Right Side View
# Standing to the right of the tree, return the values you can see - the RIGHTMOST node
# of every level, top to bottom.
# Example: root=[1,2,3,None,5,None,4] -> [1,3,4]
#          root=[1,None,3]            -> [1,3]


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


# Case 1: BFS: take the LAST node of every level
from collections import deque

def right_side_view(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        rightmost = None
        for _ in range(len(queue)):    # drain exactly one level
            node = queue.popleft()
            rightmost = node           # overwritten each time; ends as the last node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(rightmost.val)

    return result
# Time:  O(n)
# Space: O(width)


# Case 2: DFS visiting RIGHT before left, taking the first node seen per depth
def right_side_view_dfs(root):
    result = []

    def dfs(node, depth):
        if not node:
            return
        # going right-first means the first node reached at any depth is the rightmost
        if depth == len(result):
            result.append(node.val)
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return result
# Time:  O(n)
# Space: O(h)
# Note the visit order: swapping to left-first would give the LEFT side view instead,
# which is the same algorithm for a different question.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, None, 5, None, 4], [1, 3, 4]),
        ([1, None, 3], [1, 3]),
        ([], []),
        ([1], [1]),
        ([1, 2, 3, 4], [1, 3, 4]),
        ([1, 2, None, 3], [1, 2, 3]),   # only left children: they ARE the rightmost
    ]
    for values, expected in cases:
        got = right_side_view(build(values))
        print(values, "->", got, got == expected)

    print(right_side_view_dfs(build([1, 2, 3, None, 5, None, 4])))   # [1, 3, 4]
    print(right_side_view_dfs(build([1, 2, None, 3])))               # [1, 2, 3]
