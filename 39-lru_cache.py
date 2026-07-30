# LRU Cache
# Design a cache with a fixed capacity where get and put both run in O(1).
# When it is full, inserting evicts the LEAST RECENTLY USED key. Both get and put
# count as "using" a key.
# Example: capacity=2 ; put(1,10) ; put(2,20) ; get(1) -> 10 ;
#          put(3,30) evicts key 2 ; get(2) -> -1


# Case 1: Optimal: hash map + doubly linked list
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}                # key -> its Node, for O(1) lookup

        # two sentinels so insert/remove never need a None check
        self.left = Node()             # left.next is the LEAST recently used
        self.right = Node()            # right.prev is the MOST recently used
        self.left.next = self.right
        self.right.prev = self.left

    def _remove(self, node):
        """Unlink a node from the list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert(self, node):
        """Link a node in just before `right`, marking it most recently used."""
        prev, nxt = self.right.prev, self.right
        prev.next = node
        node.prev = prev
        node.next = nxt
        nxt.prev = node

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)             # touching a key refreshes its position
        self._insert(node)
        return node.val

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])      # overwrite: drop the old node

        node = Node(key, value)
        self.cache[key] = node
        self._insert(node)

        if len(self.cache) > self.capacity:
            lru = self.left.next               # the node next to the left sentinel
            self._remove(lru)
            del self.cache[lru.key]            # keep map and list in sync
# get / put: O(1)
# Space: O(capacity)
# The pairing is the whole design: the hash map gives O(1) lookup, and the linked list
# gives O(1) reordering. Neither structure can do both alone.


# Case 2: Short: OrderedDict already is a hash map plus a linked list
from collections import OrderedDict

class LRUCacheOrdered:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)    # mark as most recently used
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)     # pop the oldest entry
# get / put: O(1)


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    print(cache.get(1), cache.get(1) == 10)      # 10, and key 1 is now most recent
    cache.put(3, 30)                             # evicts key 2, not key 1
    print(cache.get(2), cache.get(2) == -1)      # -1
    print(cache.get(3), cache.get(3) == 30)      # 30

    # overwriting an existing key must not evict anything
    c2 = LRUCache(2)
    c2.put(1, 1)
    c2.put(1, 100)
    c2.put(2, 2)
    print(c2.get(1), c2.get(1) == 100)
    print(c2.get(2), c2.get(2) == 2)

    # capacity 1: every put evicts the previous key
    c3 = LRUCache(1)
    c3.put(1, 1)
    c3.put(2, 2)
    print(c3.get(1), c3.get(1) == -1)

    ordered = LRUCacheOrdered(2)
    ordered.put(1, 10)
    ordered.put(2, 20)
    ordered.get(1)
    ordered.put(3, 30)
    print(ordered.get(2), ordered.get(1))        # -1 10
