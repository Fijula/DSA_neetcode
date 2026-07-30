# Remove Nth Node From End of List
# Remove the nth node counting from the END of the list and return the new head.
# Example: head=[1,2,3,4], n=2 -> [1,2,4]
#          head=[1,2],     n=2 -> [2]      (the head itself is removed)
#          head=[1],       n=1 -> []


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


# Case 1: Two passes: count the length, then walk to length - n
def remove_nth_from_end_two_pass(head, n):
    length = 0
    current = head
    while current:
        length += 1
        current = current.next

    if n == length:
        return head.next               # removing the head: just skip it

    # stop at the node just before the target
    current = head
    for _ in range(length - n - 1):
        current = current.next
    current.next = current.next.next
    return head
# Time:  O(n)   two passes
# Space: O(1)


# Case 2: Optimal: one pass, two pointers held n apart
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)          # lets us delete the real head without a branch
    left = dummy
    right = head

    for _ in range(n):                 # open a gap of exactly n nodes
        right = right.next

    # slide both until right falls off the end; left then sits before the target
    while right:
        left = left.next
        right = right.next

    left.next = left.next.next         # unlink the nth-from-end node
    return dummy.next
# Time:  O(n)   a single pass
# Space: O(1)
# The fixed gap is what converts "nth from the end" into "where right runs out":
# when right is None, left is n+1 nodes from the end, i.e. just before the target.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4], 2, [1, 2, 4]),
        ([1, 2], 2, [2]),
        ([1], 1, []),
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4]),   # remove the tail
        ([1, 2, 3, 4, 5], 5, [2, 3, 4, 5]),   # remove the head
    ]
    for values, n, expected in cases:
        got = to_list(remove_nth_from_end(build(values), n))
        print(values, n, "->", got, got == expected)

    print(to_list(remove_nth_from_end_two_pass(build([1, 2, 3, 4]), 2)))   # [1, 2, 4]
    print(to_list(remove_nth_from_end_two_pass(build([1, 2]), 2)))         # [2]
