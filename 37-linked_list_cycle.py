# Linked List Cycle
# Return True if the linked list contains a cycle, i.e. some node's next pointer
# leads back to an earlier node.
# Example: 1 -> 2 -> 3 -> 4 -> back to 2   -> True
#          1 -> 2 -> 3 -> None            -> False


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_with_cycle(values, cycle_index=None):
    """Build a list; if cycle_index is given, the tail points back to that index."""
    if not values:
        return None
    nodes = [ListNode(val) for val in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if cycle_index is not None:
        nodes[-1].next = nodes[cycle_index]
    return nodes[0]


# Case 1: Hash set: remember every node visited
def has_cycle_set(head):
    seen = set()
    current = head
    while current:
        if current in seen:            # been here before: a cycle
            return True
        seen.add(current)
        current = current.next
    return False                       # reached None: no cycle
# Time:  O(n)
# Space: O(n)   one entry per node


# Case 2: Optimal: Floyd's tortoise and hare - two pointers at different speeds
def has_cycle(head):
    slow, fast = head, head

    while fast and fast.next:
        slow = slow.next               # one step
        fast = fast.next.next          # two steps
        if slow is fast:               # they met: there must be a loop
            return True

    return False                       # fast ran off the end: no loop
# Time:  O(n)
# Space: O(1)   just two pointers
# Why they must meet: inside a cycle the gap between them shrinks by exactly one
# every iteration, so it eventually hits zero. Compare with `is`, not ==, since we
# care about node identity rather than value.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4], 1, True),       # tail points back at index 1
        ([1, 2, 3], None, False),
        ([], None, False),
        ([1], None, False),
        ([1], 0, True),                # a node pointing at itself
        ([1, 2], 0, True),
    ]
    for values, cycle_index, expected in cases:
        head = build_with_cycle(values, cycle_index)
        got = has_cycle(head)
        print(values, "cycle at", cycle_index, "->", got, got == expected)

    print(has_cycle_set(build_with_cycle([1, 2, 3, 4], 1)))   # True
    print(has_cycle_set(build_with_cycle([1, 2, 3], None)))   # False
