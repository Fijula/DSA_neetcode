# Validate Binary Search Tree
# A valid BST requires: every value in a node's LEFT subtree is strictly smaller, every
# value in its RIGHT subtree is strictly larger, and both subtrees are valid BSTs.
# Example: root=[2,1,3]      -> True
#          root=[1,2,3]      -> False   2 sits left of 1 but is larger
#          root=[5,4,6,None,None,3,7] -> False   3 is right of 5 but smaller


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


# Case 1: WRONG approach, kept as a warning: only comparing against direct children
def is_valid_bst_broken(root):
    if not root:
        return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return is_valid_bst_broken(root.left) and is_valid_bst_broken(root.right)
# Fails on [5,4,6,None,None,3,7]: the 3 is a valid child of 6, but it is in 5's RIGHT
# subtree while being smaller than 5. A local check cannot see that.


# Case 2: Optimal: DFS carrying the allowed (low, high) range down the tree
def is_valid_bst(root):
    def valid(node, low, high):
        if not node:
            return True                # an empty subtree is a valid BST

        if not (low < node.val < high):
            return False               # this value violates a constraint from an ancestor

        # going left tightens the upper bound, going right tightens the lower bound
        return (valid(node.left, low, node.val)
                and valid(node.right, node.val, high))

    return valid(root, float("-inf"), float("inf"))
# Time:  O(n)   one visit per node
# Space: O(h)   recursion depth
# The bounds are what fix the broken version: each node inherits limits from EVERY
# ancestor, not just its parent, so a far-away violation is still caught.


# Case 3: In-order traversal: a valid BST yields a strictly increasing sequence
def is_valid_bst_inorder(root):
    prev = None                        # the previously visited value

    def inorder(node):
        nonlocal prev
        if not node:
            return True
        if not inorder(node.left):     # visit left subtree first
            return False
        if prev is not None and node.val <= prev:
            return False               # not strictly increasing
        prev = node.val
        return inorder(node.right)

    return inorder(root)
# Time:  O(n)
# Space: O(h)


if __name__ == "__main__":
    cases = [
        ([2, 1, 3], True),
        ([1, 2, 3], False),
        ([5, 4, 6, None, None, 3, 7], False),
        ([], True),
        ([1], True),
        ([2, 2], False),               # duplicates are not allowed
        ([5, 1, 7, None, None, 6, 8], True),
        ([10, 5, 15, None, None, 6, 20], False),   # 6 violates the root's bound
    ]
    for values, expected in cases:
        got = is_valid_bst(build(values))
        print(values, "->", got, got == expected)

    print(is_valid_bst_inorder(build([5, 4, 6, None, None, 3, 7])))   # False
    # the broken version wrongly says True on that same tree:
    print(is_valid_bst_broken(build([5, 4, 6, None, None, 3, 7])))    # True <- wrong
