# Reverse Linked List
# Given the head of a singly linked list, reverse it and return the new head.
# Example: 0 -> 1 -> 2 -> 3   becomes   3 -> 2 -> 1 -> 0
#          empty list         stays     empty


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# --- helpers used by every linked-list file in this repo ---
def build(values):
    """Turn [1,2,3] into a linked list and return its head."""
    head = None
    for val in reversed(values):
        head = ListNode(val, head)
    return head


def to_list(head):
    """Turn a linked list back into a plain Python list."""
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


# Case 1: Iterative: walk forward, flipping each next pointer as you go
def reverse_list(head):
    prev = None                        # the reversed part built so far
    current = head

    while current:
        next_node = current.next       # save it: we are about to overwrite current.next
        current.next = prev            # flip this link backwards
        prev = current                 # the reversed part grows by one node
        current = next_node            # advance into the untouched part

    return prev                        # current is None, prev is the last node = new head
# Time:  O(n)   one pass
# Space: O(1)   only three pointers, no new nodes


# Case 2: Recursive: reverse the rest, then attach the current node at the end
def reverse_list_recursive(head):
    if not head or not head.next:
        return head                    # empty list or single node: already reversed

    new_head = reverse_list_recursive(head.next)   # reverse everything after head
    head.next.next = head              # make the next node point back at head
    head.next = None                   # head becomes the new tail
    return new_head
# Time:  O(n)
# Space: O(n)   one stack frame per node


if __name__ == "__main__":
    cases = [
        ([0, 1, 2, 3], [3, 2, 1, 0]),
        ([], []),
        ([1], [1]),
        ([1, 2], [2, 1]),
    ]
    for values, expected in cases:
        got = to_list(reverse_list(build(values)))
        print(values, "->", got, got == expected)

    print(to_list(reverse_list_recursive(build([0, 1, 2, 3]))))   # [3, 2, 1, 0]
    print(to_list(reverse_list_recursive(build([]))))             # []
