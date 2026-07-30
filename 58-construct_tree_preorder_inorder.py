# Construct Binary Tree from Preorder and Inorder Traversal
# Rebuild the tree from its preorder and inorder traversals. All values are unique.
# preorder = root, LEFT subtree, RIGHT subtree
# inorder  = LEFT subtree, root, RIGHT subtree
# Example: preorder=[1,2,3,4], inorder=[2,1,3,4] -> [1,2,3,None,None,None,4]
#          preorder=[1],       inorder=[1]       -> [1]


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def to_level_order(root):
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


# Case 1: Recursive with slicing - clear, but wasteful
def build_tree_slicing(preorder, inorder):
    if not preorder or not inorder:
        return None

    root = TreeNode(preorder[0])       # preorder[0] is always the root
    mid = inorder.index(preorder[0])   # everything left of it in inorder is the left subtree

    # mid values belong to the left subtree, so preorder[1 : mid+1] covers exactly them
    root.left = build_tree_slicing(preorder[1:mid + 1], inorder[:mid])
    root.right = build_tree_slicing(preorder[mid + 1:], inorder[mid + 1:])
    return root
# Time:  O(n^2)   index() is a linear scan and the slices copy
# Space: O(n^2)   from the slice copies


# Case 2: Optimal: an index map plus a moving preorder pointer, no slicing
def build_tree(preorder, inorder):
    index_of = {val: i for i, val in enumerate(inorder)}   # O(1) root lookup
    pre_index = 0

    def helper(left, right):
        """Build from inorder[left .. right] inclusive."""
        nonlocal pre_index
        if left > right:
            return None                # empty range

        root_val = preorder[pre_index]
        pre_index += 1                 # consume the root, in preorder sequence
        root = TreeNode(root_val)

        mid = index_of[root_val]
        # build LEFT first: preorder demands the whole left subtree before the right
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root

    return helper(0, len(inorder) - 1)
# Time:  O(n)   each value handled once, lookups are O(1)
# Space: O(n)   the map plus recursion depth
# The order of the two recursive calls is load-bearing: pre_index advances through
# preorder as a shared cursor, so the left subtree must be consumed first.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4], [2, 1, 3, 4], [1, 2, 3, None, None, None, 4]),
        ([1], [1], [1]),
        ([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7]),
        ([], [], []),
        ([1, 2], [2, 1], [1, 2]),      # left child only
        ([1, 2], [1, 2], [1, None, 2]),  # right child only
    ]
    for preorder, inorder, expected in cases:
        got = to_level_order(build_tree(preorder, inorder))
        print(preorder, inorder, "->", got, got == expected)

    print(to_level_order(build_tree_slicing([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])))
