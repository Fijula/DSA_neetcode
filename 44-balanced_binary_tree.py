# Balanced Binary Tree
# A tree is height-balanced if, for EVERY node, the heights of its two subtrees differ
# by at most 1. Return True if the tree is balanced.
# Example:     1        -> True
#             / \
#            2   3
#
#          1            -> False   left subtree height 2, right height 0
#         /
#        2
#       /
#      3


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


# Case 1: Brute force: check the balance rule at each node, recomputing heights
def is_balanced_brute(root):
    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if not root:
        return True

    if abs(height(root.left) - height(root.right)) > 1:
        return False
    # the rule must hold for EVERY node, not just the root
    return is_balanced_brute(root.left) and is_balanced_brute(root.right)
# Time:  O(n^2)   height() re-walks the same subtrees over and over
# Space: O(h)


# Case 2: Optimal: one bottom-up pass returning (is_balanced, height)
def is_balanced(root):
    def check(node):
        if not node:
            return True, 0             # empty subtree: balanced, height 0

        left_ok, left_height = check(node.left)
        right_ok, right_height = check(node.right)

        # this node is balanced only if both children are AND their heights are close
        balanced = (left_ok and right_ok
                    and abs(left_height - right_height) <= 1)

        return balanced, 1 + max(left_height, right_height)

    return check(root)[0]
# Time:  O(n)   each node is visited exactly once
# Space: O(h)   recursion depth
# Returning the height ALONGSIDE the verdict is what kills the quadratic blow-up:
# the parent never has to re-measure a subtree the child already measured.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3], True),
        ([1, 2, None, 3], False),      # a left chain of 3 nodes
        ([], True),
        ([1], True),
        ([3, 9, 20, None, None, 15, 7], True),
        ([1, 2, 2, 3, 3, None, None, 4, 4], False),
        ([1, 2, 3, 4, None, None, None, 5], False),   # imbalance deep in the tree
    ]
    for values, expected in cases:
        got = is_balanced(build(values))
        print(values, "->", got, got == expected)

    print(is_balanced_brute(build([1, 2, None, 3])))                 # False
    print(is_balanced_brute(build([3, 9, 20, None, None, 15, 7])))   # True
