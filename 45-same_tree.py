# Same Tree
# Given the roots of two binary trees, return True if they are structurally identical
# AND every corresponding pair of nodes holds the same value.
# Example: [1,2,3] and [1,2,3] -> True
#          [1,2]   and [1,None,2] -> False   same values, different shape


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


# Case 1: Recursive: compare the roots, then recurse on both sides in lockstep
def is_same_tree(p, q):
    if not p and not q:
        return True                    # both empty: identical
    if not p or not q:
        return False                   # exactly one empty: shapes differ
    if p.val != q.val:
        return False                   # same shape here, but different values

    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
# Time:  O(n)   n = size of the smaller tree; it stops at the first difference
# Space: O(h)   recursion depth
# Checking left-with-left and right-with-right is what makes this a STRUCTURE check:
# a mirrored tree correctly comes out as not the same.


# Case 2: Iterative: a stack of node pairs to compare
def is_same_tree_iterative(p, q):
    stack = [(p, q)]
    while stack:
        node1, node2 = stack.pop()
        if not node1 and not node2:
            continue                   # this branch matches, nothing more to do
        if not node1 or not node2 or node1.val != node2.val:
            return False
        stack.append((node1.left, node2.left))
        stack.append((node1.right, node2.right))
    return True
# Time: O(n), Space: O(h)


if __name__ == "__main__":
    cases = [
        ([1, 2, 3], [1, 2, 3], True),
        ([1, 2], [1, None, 2], False),           # same values, mirrored shape
        ([], [], True),
        ([1], [], False),
        ([1, 2, 1], [1, 1, 2], False),           # same multiset, different positions
        ([1, 2, 3, 4], [1, 2, 3, 4], True),
        ([1, 2, 3], [1, 2, 4], False),           # one value differs
    ]
    for a, b, expected in cases:
        got = is_same_tree(build(a), build(b))
        print(a, b, "->", got, got == expected)

    print(is_same_tree_iterative(build([1, 2, 3]), build([1, 2, 3])))     # True
    print(is_same_tree_iterative(build([1, 2]), build([1, None, 2])))     # False
