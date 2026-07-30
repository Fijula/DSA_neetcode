# Count Good Nodes in Binary Tree
# A node is GOOD if no node on the path from the root down to it holds a LARGER value.
# The root is always good. Return how many good nodes the tree has.
# Example: root=[2,1,1,3,None,1,5] -> 3   the root 2, the 3 under 1, and the 5
#          root=[1,2,-1,3,4]       -> 4


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


# Case 1: Optimal: DFS carrying the maximum value seen on the path so far
def good_nodes(root):
    def dfs(node, path_max):
        if not node:
            return 0

        # good means nothing on the path above it was strictly larger
        count = 1 if node.val >= path_max else 0
        path_max = max(path_max, node.val)     # extend the path maximum downward

        count += dfs(node.left, path_max)
        count += dfs(node.right, path_max)
        return count

    return dfs(root, float("-inf")) if root else 0
# Time:  O(n)   one visit per node
# Space: O(h)   recursion depth
# Passing path_max DOWN is what makes this one pass: each node needs only a single
# number summarising its ancestors, not the whole path.


# Case 2: Iterative DFS with an explicit stack of (node, path_max)
def good_nodes_iterative(root):
    if not root:
        return 0

    stack = [(root, float("-inf"))]
    count = 0
    while stack:
        node, path_max = stack.pop()
        if node.val >= path_max:
            count += 1
        new_max = max(path_max, node.val)
        if node.left:
            stack.append((node.left, new_max))
        if node.right:
            stack.append((node.right, new_max))
    return count
# Time: O(n), Space: O(h)


if __name__ == "__main__":
    cases = [
        ([2, 1, 1, 3, None, 1, 5], 3),
        ([1, 2, -1, 3, 4], 4),
        ([], 0),
        ([1], 1),                      # the root alone is good
        ([3, 1, 4, 3, None, 1, 5], 4),
        ([9, 3, 6, None, None, None, None], 1),   # everything below is smaller
        ([1, 1, 1], 3),                # equal values still count as good
    ]
    for values, expected in cases:
        got = good_nodes(build(values))
        print(values, "->", got, got == expected)

    print(good_nodes_iterative(build([3, 1, 4, 3, None, 1, 5])))   # 4
