# Copy List with Random Pointer
# Each node has a next pointer AND a random pointer that may point at any node in the
# list or at None. Return a DEEP copy: new nodes whose pointers mirror the original.
# Example: [[3,None],[7,3],[4,0],[5,1]]
#          means node values 3,7,4,5 with random pointers -> None, index 3, index 0,
#          index 1. The copy must have the same shape but share no nodes.


class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def build(pairs):
    """pairs = [(val, random_index_or_None), ...] -> head of the built list."""
    nodes = [Node(val) for val, _ in pairs]
    for i, (_, random_index) in enumerate(pairs):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if random_index is not None:
            nodes[i].random = nodes[random_index]
    return nodes[0] if nodes else None


def to_pairs(head):
    """Serialise back to [(val, random_index_or_None), ...] so copies can be compared."""
    nodes, index_of = [], {}
    current = head
    while current:
        index_of[id(current)] = len(nodes)
        nodes.append(current)
        current = current.next
    return [(n.val, index_of[id(n.random)] if n.random else None) for n in nodes]


# Case 1: Two passes with a hash map: old node -> new node
def copy_random_list(head):
    if not head:
        return None

    old_to_new = {}

    # pass 1: create every new node, pointers not wired yet
    current = head
    while current:
        old_to_new[current] = Node(current.val)
        current = current.next

    # pass 2: now that every node exists, wire both pointers by lookup
    current = head
    while current:
        copy = old_to_new[current]
        copy.next = old_to_new.get(current.next)      # .get returns None past the tail
        copy.random = old_to_new.get(current.random)
        current = current.next

    return old_to_new[head]
# Time:  O(n)   two passes
# Space: O(n)   the map
# Two passes are needed because a random pointer can point FORWARD to a node that
# does not exist yet during pass 1.


# Case 2: Optimal space: weave the copies into the original list, then unweave
def copy_random_list_interleave(head):
    if not head:
        return None

    # pass 1: insert each copy directly after its original -> A A' B B' C C'
    current = head
    while current:
        copy = Node(current.val, current.next)
        current.next = copy
        current = copy.next

    # pass 2: a copy's random is the node right after the original's random
    current = head
    while current:
        if current.random:
            current.next.random = current.random.next
        current = current.next.next

    # pass 3: detach the copies, restoring the original list
    new_head = head.next
    current = head
    while current:
        copy = current.next
        current.next = copy.next
        copy.next = copy.next.next if copy.next else None
        current = current.next

    return new_head
# Time:  O(n)   three passes
# Space: O(1)   no hash map, the interleaving itself records the pairing


if __name__ == "__main__":
    cases = [
        [(3, None), (7, 3), (4, 0), (5, 1)],
        [(1, 1), (2, 1)],
        [(1, None)],
        [],
        [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)],
    ]
    for pairs in cases:
        copy = copy_random_list(build(pairs))
        got = to_pairs(copy)
        print(pairs, "->", got, got == pairs)

    # the copy must be made of genuinely new nodes, not shared references
    original = build([(3, None), (7, 3), (4, 0), (5, 1)])
    copy = copy_random_list(original)
    print("distinct nodes:", copy is not original and copy.next is not original.next)

    print(to_pairs(copy_random_list_interleave(build([(3, None), (7, 3), (4, 0), (5, 1)]))))
