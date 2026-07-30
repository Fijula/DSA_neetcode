# Design Add and Search Words Data Structure
# Like a trie, but search(word) may contain "." which matches ANY single character.
# Example: addWord("day") ; addWord("bay") ; addWord("may")
#          search("say")  -> False
#          search(".ay")  -> True
#          search("b..")  -> True


# Case 1: Optimal: trie plus DFS branching on every "."
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_word = True

    def search(self, word):
        def dfs(index, node):
            """Can word[index:] be matched starting from `node`?"""
            for i in range(index, len(word)):
                char = word[i]

                if char == ".":
                    # a wildcard: try EVERY child, succeed if any branch works
                    for child in node.children.values():
                        if dfs(i + 1, child):
                            return True
                    return False       # no child could complete the match
                else:
                    if char not in node.children:
                        return False   # a literal character that is simply absent
                    node = node.children[char]

            return node.is_word        # consumed the pattern: is this a real word end?

        return dfs(0, self.root)
# addWord: O(L)
# search:  O(L) with no dots, up to O(26^d * L) when d dots force branching
# Space:   O(total characters)
# The loop handles the deterministic characters iteratively and only RECURSES at a
# dot - that keeps the branching factor confined to the wildcards.


# Case 2: Naive: keep the words in a list and pattern-match each one
class WordDictionaryList:
    def __init__(self):
        self.words = []

    def addWord(self, word):
        self.words.append(word)

    def search(self, word):
        for candidate in self.words:
            if len(candidate) != len(word):
                continue               # length must match, dots included
            if all(p == "." or p == c for p, c in zip(word, candidate)):
                return True
        return False
# addWord: O(1), search: O(n * L)
# Fine for a handful of words, but every search rescans the entire dictionary.


if __name__ == "__main__":
    wd = WordDictionary()
    for word in ["day", "bay", "may"]:
        wd.addWord(word)

    checks = [
        ("say", False),
        (".ay", True),
        ("b..", True),
        ("day", True),
        ("da", False),                 # a prefix is not a word
        ("....", False),               # wrong length
        ("...", True),
        ("d.y", True),
        ("d.z", False),
    ]
    for pattern, expected in checks:
        got = wd.search(pattern)
        print(repr(pattern), "->", got, got == expected)

    wd2 = WordDictionary()
    wd2.addWord("bad")
    wd2.addWord("dad")
    wd2.addWord("mad")
    print(wd2.search("pad"), wd2.search("bad"), wd2.search(".ad"), wd2.search("b.."))
    # False True True True

    naive = WordDictionaryList()
    for word in ["day", "bay", "may"]:
        naive.addWord(word)
    print(naive.search(".ay"), naive.search("say"))   # True False
