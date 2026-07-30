# Serialize and Deserialize Binary Tree
# Turn a binary tree into a string and rebuild the identical tree from that string.
# Example: [1,2,3,None,None,4,5] -> "1,2,N,N,3,4,N,N,5,N,N" -> the same tree back
#          []                    -> "N"                     -> empty tree


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


# Case 1: Optimal: preorder DFS with an explicit null marker
class Codec:
    def serialize(self, root):
        parts = []

        def dfs(node):
            if not node:
                parts.append("N")      # the marker is what preserves the SHAPE
                return
            parts.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(parts)

    def deserialize(self, data):
        values = data.split(",")
        self.index = 0                 # a shared cursor into the token list

        def dfs():
            if values[self.index] == "N":
                self.index += 1
                return None

            node = TreeNode(int(values[self.index]))
            self.index += 1
            # rebuild in the SAME preorder the serializer used
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()
# serialize: O(n) time, O(n) space
# deserialize: O(n) time, O(n) space
# Preorder plus null markers is uniquely decodable on its own - unlike preorder alone,
# which needs a second traversal (see problem 58) because it cannot express shape.


# Case 2: BFS level-order encoding, closer to how LeetCode prints trees
from collections import deque

class CodecBFS:
    def serialize(self, root):
        if not root:
            return "N"
        parts, queue = [], deque([root])
        while queue:
            node = queue.popleft()
            if not node:
                parts.append("N")
                continue
            parts.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        return ",".join(parts)

    def deserialize(self, data):
        values = data.split(",")
        if values[0] == "N":
            return None

        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1
        while queue and i < len(values):
            node = queue.popleft()
            if values[i] != "N":       # attach the left child
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
            if i < len(values) and values[i] != "N":   # then the right child
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
        return root
# Time: O(n), Space: O(n)


if __name__ == "__main__":
    codec = Codec()
    cases = [
        [1, 2, 3, None, None, 4, 5],
        [],
        [1],
        [1, 2],
        [-1, 0, 1],                    # negative values must survive the round trip
        [1, 2, 3, 4, 5, 6, 7],
        [10, 5, 15, None, None, 6, 20],
    ]
    for values in cases:
        encoded = codec.serialize(build(values))
        got = to_level_order(codec.deserialize(encoded))
        print(values, "->", encoded, "->", got, got == values)

    bfs = CodecBFS()
    encoded = bfs.serialize(build([1, 2, 3, None, None, 4, 5]))
    print(encoded, to_level_order(bfs.deserialize(encoded)))
