# Kth Smallest Element in a BST
# Return the kth smallest value in a BST (1-indexed).
# Example: root=[2,1,3], k=1 -> 1
#          root=[4,3,5,2,None], k=4 -> 5


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


# Case 1: Brute force: collect every value in order, then index into it
def kth_smallest_brute(root, k):
    values = []

    def inorder(node):
        if not node:
            return
        inorder(node.left)
        values.append(node.val)
        inorder(node.right)

    inorder(root)
    return values[k - 1]               # in-order on a BST is already sorted
# Time:  O(n)   always visits the whole tree
# Space: O(n)   stores every value


# Case 2: Recursive in-order with a counter, stopping as soon as k is reached
def kth_smallest_counter(root, k):
    count = 0
    answer = None

    def inorder(node):
        nonlocal count, answer
        if not node or answer is not None:
            return                     # already found: unwind without more work
        inorder(node.left)
        count += 1
        if count == k:
            answer = node.val
            return
        inorder(node.right)

    inorder(root)
    return answer
# Time:  O(h + k)   only walks as far as the kth node
# Space: O(h)


# Case 3: Optimal: iterative in-order with an explicit stack
def kth_smallest(root, k):
    stack = []
    current = root

    while stack or current:
        # dive as far left as possible, stacking the nodes on the way down
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()          # the smallest unvisited node
        k -= 1
        if k == 0:
            return current.val         # early exit: the rest of the tree is untouched

        current = current.right        # then process its right subtree
    return -1
# Time:  O(h + k)
# Space: O(h)   the stack holds one root-to-node path
# In-order traversal of a BST emits values in ascending order, so "kth smallest" is
# just "stop after k emissions" - no sorting and no full traversal needed.


if __name__ == "__main__":
    cases = [
        ([2, 1, 3], 1, 1),
        ([4, 3, 5, 2], 4, 5),
        ([3, 1, 4, None, 2], 1, 1),
        ([5, 3, 6, 2, 4, None, None, 1], 3, 3),
        ([1], 1, 1),
        ([2, 1, 3], 3, 3),             # the largest value
        ([5, 3, 8, 1, 4, 7, 9], 5, 7),
    ]
    for values, k, expected in cases:
        got = kth_smallest(build(values), k)
        print(values, k, "->", got, got == expected)

    print(kth_smallest_brute(build([4, 3, 5, 2]), 4))     # 5
    print(kth_smallest_counter(build([3, 1, 4, None, 2]), 1))   # 1
