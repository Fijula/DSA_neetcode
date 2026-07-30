# Lowest Common Ancestor of a Binary Search Tree
# Given a BST and two nodes p and q, return their lowest common ancestor - the deepest
# node that has both of them as descendants. A node may be a descendant of itself.
# Example: root=[5,3,8,1,4,7,9], p=3, q=8 -> 5
#          root=[5,3,8,1,4,7,9], p=3, q=4 -> 3   (3 is its own descendant)


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


def find(root, val):
    """Locate the node holding val, so the tests can pass real node objects."""
    if not root:
        return None
    if root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)


# Case 1: Optimal: walk down, following the BST ordering
def lowest_common_ancestor(root, p, q):
    current = root

    while current:
        if p.val > current.val and q.val > current.val:
            current = current.right    # both are larger: the LCA is to the right
        elif p.val < current.val and q.val < current.val:
            current = current.left     # both are smaller: the LCA is to the left
        else:
            # the values SPLIT here (or one of them equals current), so this is the
            # deepest node that still has both below it
            return current
    return None
# Time:  O(h)   one root-to-node walk, O(log n) on a balanced BST
# Space: O(1)
# The BST property does all the work: no searching or backtracking is needed, because
# the first node where p and q fall on opposite sides must be their LCA.


# Case 2: General recursion that works on ANY binary tree, not just a BST
def lowest_common_ancestor_general(root, p, q):
    if not root or root is p or root is q:
        return root

    left = lowest_common_ancestor_general(root.left, p, q)
    right = lowest_common_ancestor_general(root.right, p, q)

    if left and right:
        return root                    # found one on each side: this is the split point
    return left or right               # both below on one side, or neither found
# Time:  O(n)   must potentially inspect every node
# Space: O(h)


if __name__ == "__main__":
    tree = [5, 3, 8, 1, 4, 7, 9]
    cases = [
        (tree, 3, 8, 5),
        (tree, 3, 4, 3),               # ancestor is one of the nodes itself
        (tree, 1, 4, 3),
        (tree, 7, 9, 8),
        (tree, 1, 9, 5),               # opposite corners: the root
        ([2, 1], 1, 2, 2),
    ]
    for values, p_val, q_val, expected in cases:
        root = build(values)
        got = lowest_common_ancestor(root, find(root, p_val), find(root, q_val))
        print(values, p_val, q_val, "->", got.val, got.val == expected)

    root = build(tree)
    general = lowest_common_ancestor_general(root, find(root, 1), find(root, 4))
    print(general.val)                 # 3
