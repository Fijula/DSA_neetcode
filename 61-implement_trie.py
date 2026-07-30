# Implement Trie (Prefix Tree)
# A trie stores strings character by character along shared paths, making prefix
# queries fast. Implement insert(word), search(word) and startsWith(prefix).
# Example: insert("apple") ; search("apple") -> True ; search("app") -> False
#          startsWith("app") -> True


# Case 1: Optimal: a tree of nodes, one child per character
class TrieNode:
    def __init__(self):
        self.children = {}             # character -> the TrieNode below it
        self.is_word = False           # does a complete word END at this node?


class Trie:
    def __init__(self):
        self.root = TrieNode()         # the root holds no character itself

    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()   # extend the path
            current = current.children[char]
        current.is_word = True         # mark the end, so "app" != "apple"

    def _walk(self, prefix):
        """Follow prefix from the root; return the node reached, or None."""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return None
            current = current.children[char]
        return current

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word   # must be a marked word END

    def startsWith(self, prefix):
        return self._walk(prefix) is not None      # existing path is enough
# insert / search / startsWith: O(L)   L = length of the word
# Space: O(total characters inserted)
# The is_word flag is what separates the two queries: search demands a marked
# terminal node, startsWith only demands that the path exists.


# Case 2: Naive: a set of words  (kept to show what a trie buys you)
class TrieSet:
    def __init__(self):
        self.words = set()

    def insert(self, word):
        self.words.add(word)

    def search(self, word):
        return word in self.words

    def startsWith(self, prefix):
        return any(w.startswith(prefix) for w in self.words)   # O(n * L) scan
# insert / search: O(L), startsWith: O(n * L)
# The prefix query is where the set loses: it must test every stored word, while the
# trie just follows one path.


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    print(trie.search("apple"), trie.search("apple") is True)          # True
    print(trie.search("app"), trie.search("app") is False)             # False, prefix only
    print(trie.startsWith("app"), trie.startsWith("app") is True)      # True
    trie.insert("app")
    print(trie.search("app"), trie.search("app") is True)              # now True

    t2 = Trie()
    for word in ["car", "card", "care", "dog"]:
        t2.insert(word)
    print(t2.search("car"), t2.search("care"), t2.search("ca"))        # True True False
    print(t2.startsWith("ca"), t2.startsWith("do"), t2.startsWith("z"))  # True True False
    print(t2.search(""), t2.startsWith(""))                            # False True

    t3 = Trie()
    t3.insert("")                       # inserting the empty word marks the root
    print(t3.search(""))                # True

    naive = TrieSet()
    naive.insert("apple")
    print(naive.search("app"), naive.startsWith("app"))                # False True
