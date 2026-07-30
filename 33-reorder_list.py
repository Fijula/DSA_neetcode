# Reorder List
# Reorder a linked list in place so it alternates first node, last node, second node,
# second-to-last node, ... Return nothing; mutate the list.
# Example: [2,4,6,8]   -> [2,8,4,6]
#          [2,4,6,8,10] -> [2,10,4,8,6]


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for val in reversed(values):
        head = ListNode(val, head)
    return head


def to_list(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


# Case 1: Brute force: copy every node into an array, then rewire by index
def reorder_list_array(head):
    if not head:
        return

    nodes = []
    current = head
    while current:
        nodes.append(current)
        current = current.next

    left, right = 0, len(nodes) - 1
    while left < right:
        nodes[left].next = nodes[right]     # front node points at the back node
        left += 1
        if left == right:
            break                            # odd length: middle node is now the tail
        nodes[right].next = nodes[left]      # back node points at the next front node
        right -= 1

    nodes[left].next = None                  # terminate the list
# Time:  O(n)
# Space: O(n)   the array of node references


# Case 2: Optimal: split in half, reverse the second half, then interleave
def reorder_list(head):
    if not head or not head.next:
        return

    # step 1: find the middle with slow / fast pointers
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # step 2: cut the list in two and reverse the second half
    second = slow.next
    slow.next = None                   # first half now ends at slow
    prev = None
    while second:
        next_node = second.next
        second.next = prev
        prev = second
        second = next_node
    second = prev                      # head of the reversed second half

    # step 3: weave the two halves together, alternating one node from each
    first = head
    while second:
        first_next, second_next = first.next, second.next
        first.next = second
        second.next = first_next
        first, second = first_next, second_next
# Time:  O(n)   three linear passes
# Space: O(1)   no array of nodes
# fast starts at head.next so that for even lengths `slow` lands on the END of the
# first half, which is exactly where the cut belongs.


if __name__ == "__main__":
    cases = [
        ([2, 4, 6, 8], [2, 8, 4, 6]),
        ([2, 4, 6, 8, 10], [2, 10, 4, 8, 6]),
        ([1], [1]),
        ([1, 2], [1, 2]),
        ([1, 2, 3], [1, 3, 2]),
        ([], []),
    ]
    for values, expected in cases:
        head = build(values)
        reorder_list(head)
        got = to_list(head)
        print(values, "->", got, got == expected)

    head = build([2, 4, 6, 8, 10])
    reorder_list_array(head)
    print(to_list(head))               # [2, 10, 4, 8, 6]
