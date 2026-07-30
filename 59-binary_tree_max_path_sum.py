# Binary Tree Maximum Path Sum
# A path is any sequence of nodes connected by edges; it needs not pass through the
# root, and each node appears at most once. Return the largest possible sum of values
# along such a path. Values may be negative.
# Example: root=[1,2,3]        -> 6   2 -> 1 -> 3
#          root=[-15,10,20,None,None,15,5,-5] -> 40   15 -> 20 -> 5
#          root=[-3]           -> -3  a single node is still a valid path


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


# Case 1: Optimal: one DFS returning the best DOWNWARD path, tracking the best BEND
def max_path_sum(root):
    best = float("-inf")               # the answer may be negative, so not 0

    def gain(node):
        """Largest sum of a path that starts at `node` and only goes DOWN."""
        nonlocal best
        if not node:
            return 0

        # a subtree contributing a negative sum is better skipped entirely,
        # which is what max(..., 0) expresses
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)

        # the path that BENDS at this node uses both sides; it cannot be extended
        # upward, so it is only ever an answer candidate
        best = max(best, node.val + left + right)

        # what the parent can actually use: this node plus its better single side
        return node.val + max(left, right)

    gain(root)
    return best
# Time:  O(n)   one visit per node
# Space: O(h)   recursion depth
# The two-values-per-node idea is the crux: what you RETURN (a straight downward path,
# usable by the parent) differs from what you RECORD (a bent path, which is a complete
# answer but useless to the parent).


# Case 2: Same algorithm, returning both numbers explicitly instead of using nonlocal
def max_path_sum_explicit(root):
    def helper(node):
        """Returns (best downward path from node, best complete path in this subtree)."""
        if not node:
            return 0, float("-inf")

        left_down, left_best = helper(node.left)
        right_down, right_best = helper(node.right)

        left_down = max(left_down, 0)
        right_down = max(right_down, 0)

        bend = node.val + left_down + right_down
        down = node.val + max(left_down, right_down)
        return down, max(bend, left_best, right_best)

    return helper(root)[1]
# Time: O(n), Space: O(h)


if __name__ == "__main__":
    cases = [
        ([1, 2, 3], 6),
        ([-15, 10, 20, None, None, 15, 5, -5], 40),
        ([-3], -3),                    # all negative: the least-bad single node
        ([-10, 9, 20, None, None, 15, 7], 42),
        ([2, -1], 2),                  # skipping the negative child is better
        ([1], 1),
        ([-2, -1], -1),
    ]
    for values, expected in cases:
        got = max_path_sum(build(values))
        print(values, "->", got, got == expected)

    print(max_path_sum_explicit(build([-10, 9, 20, None, None, 15, 7])))   # 42
    print(max_path_sum_explicit(build([-3])))                              # -3
