# Subtree of Another Tree
# Return True if subRoot appears as a SUBTREE of root - i.e. some node of root, taken
# together with all of its descendants, is identical to subRoot.
# Example: root=[1,2,3,4,5], subRoot=[2,4,5] -> True
#          root=[1,2,3],     subRoot=[2,3]   -> False   (2's children are not 3)


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


# Case 1: Optimal enough: at every node, run a full "same tree" comparison
def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)


def is_subtree(root, sub_root):
    if not sub_root:
        return True                    # an empty tree is a subtree of anything
    if not root:
        return False                   # non-empty target cannot fit in an empty tree

    if is_same_tree(root, sub_root):
        return True                    # match rooted right here

    # otherwise look for a match deeper down, on either side
    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)
# Time:  O(n * m)   the comparison may restart at each of n nodes
# Space: O(h)
# A whole-subtree match is required, not just a matching path: that is why
# is_same_tree must reach all the way down to the None children on both sides.


# Case 2: Serialise both trees, then do a substring search
def is_subtree_serialize(root, sub_root):
    def serialize(node):
        if not node:
            return "#"                 # a marker for None, so structure is preserved
        # the leading "^" delimits values, stopping 12 from matching inside 112
        return f"^{node.val},{serialize(node.left)},{serialize(node.right)}"

    return serialize(sub_root) in serialize(root)
# Time:  O(n + m) to build, plus the substring search
# Space: O(n + m)
# The None markers are essential: without them, differently-shaped trees can serialise
# to the same string and produce false positives.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4, 5], [2, 4, 5], True),
        ([1, 2, 3], [2, 3], False),
        ([3, 4, 5, 1, 2], [4, 1, 2], True),
        ([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2], False),
        ([1], [1], True),
        ([1], [], True),               # empty subRoot
        ([], [1], False),
        ([1, 1], [1], True),           # a leaf 1 matches
    ]
    for a, b, expected in cases:
        got = is_subtree(build(a), build(b))
        print(a, b, "->", got, got == expected)

    print(is_subtree_serialize(build([1, 2, 3, 4, 5]), build([2, 4, 5])))   # True
    print(is_subtree_serialize(build([1, 2, 3]), build([2, 3])))            # False
