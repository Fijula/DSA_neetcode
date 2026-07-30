# Word Search II
# Given an m x n board of characters and a list of words, return every word that can be
# formed by walking adjacent cells (up/down/left/right). A cell may not be reused
# within a single word.
# Example: board=[["a","b"],["c","d"]], words=["ab","cb","ad","bd","ac"]
#          -> ["ab","ac","bd"]  (order may vary)


# Case 1: Brute force: run a separate DFS for every word
def find_words_brute(board, words):
    if not board or not board[0]:
        return []
    rows, cols = len(board), len(board[0])

    def exists(word):
        def dfs(r, c, index, visited):
            if index == len(word):
                return True
            if not (0 <= r < rows and 0 <= c < cols):
                return False
            if (r, c) in visited or board[r][c] != word[index]:
                return False

            visited.add((r, c))
            found = (dfs(r + 1, c, index + 1, visited)
                     or dfs(r - 1, c, index + 1, visited)
                     or dfs(r, c + 1, index + 1, visited)
                     or dfs(r, c - 1, index + 1, visited))
            visited.remove((r, c))     # backtrack: free the cell for other paths
            return found

        return any(dfs(r, c, 0, set()) for r in range(rows) for c in range(cols))

    return [word for word in words if exists(word)]
# Time:  O(words * m * n * 4^L)   every word rescans the whole board
# Space: O(L)


# Case 2: Optimal: build a trie of ALL words, then walk the board ONCE
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None               # the complete word ending here, if any


def find_words(board, words):
    if not board or not board[0]:
        return []

    # build the trie: shared prefixes are now explored only once
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.word = word

    rows, cols = len(board), len(board[0])
    result = []
    visited = set()

    def dfs(r, c, node):
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in visited:
            return

        char = board[r][c]
        if char not in node.children:
            return                     # no word in the trie continues this way: prune

        next_node = node.children[char]
        if next_node.word:
            result.append(next_node.word)
            next_node.word = None      # clear it so the same word is not added twice

        visited.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc, next_node)
        visited.remove((r, c))         # backtrack

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return result
# Time:  O(m * n * 4^L)   one board walk, shared across all words
# Space: O(total characters in words)
# The trie turns "does any word continue like this?" into a single dict lookup, so a
# dead-end prefix prunes ALL words at once instead of once per word.


if __name__ == "__main__":
    cases = [
        ([["a", "b"], ["c", "d"]], ["ab", "cb", "ad", "bd", "ac"], ["ab", "ac", "bd"]),
        ([["a"]], ["a"], ["a"]),
        ([["a"]], ["b"], []),
        ([["o", "a", "a", "n"],
          ["e", "t", "a", "e"],
          ["i", "h", "k", "r"],
          ["i", "f", "l", "v"]], ["oath", "pea", "eat", "rain"], ["oath", "eat"]),
        ([["a", "b"], ["c", "d"]], ["abcd"], []),   # not a connected walk
        ([], ["a"], []),
    ]
    for board, words, expected in cases:
        got = find_words(board, words)
        print(words, "->", got, sorted(got) == sorted(expected))

    print(find_words_brute([["a", "b"], ["c", "d"]], ["ab", "cb", "ad", "bd", "ac"]))
