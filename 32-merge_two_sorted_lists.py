# Merge Two Sorted Linked Lists
# Given the heads of two sorted linked lists, splice them into one sorted list and
# return its head. Reuse the existing nodes, do not allocate new ones.
# Example: [1,2,4] + [1,3,5] -> [1,1,2,3,4,5]
#          []      + [1]     -> [1]


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


# Case 1: Iterative with a dummy head node
def merge_two_lists(list1, list2):
    dummy = ListNode()                 # a fake node so we never special-case the head
    tail = dummy                       # always the last node of the merged list

    while list1 and list2:
        if list1.val <= list2.val:     # <= keeps the merge stable
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    # one list is exhausted; the other is already sorted, so attach it wholesale
    tail.next = list1 if list1 else list2

    return dummy.next                  # skip the dummy: the real head is behind it
# Time:  O(n + m)   each node is visited once
# Space: O(1)       only pointers, no new nodes beyond the dummy
# The dummy head is the trick worth remembering: without it you need an awkward
# "is this the first node?" branch inside the loop.


# Case 2: Recursive: pick the smaller head, then merge the rest
def merge_two_lists_recursive(list1, list2):
    if not list1:
        return list2                   # nothing left to merge in
    if not list2:
        return list1

    if list1.val <= list2.val:
        list1.next = merge_two_lists_recursive(list1.next, list2)
        return list1
    list2.next = merge_two_lists_recursive(list1, list2.next)
    return list2
# Time:  O(n + m)
# Space: O(n + m)   recursion depth


if __name__ == "__main__":
    cases = [
        ([1, 2, 4], [1, 3, 5], [1, 1, 2, 3, 4, 5]),
        ([], [1], [1]),
        ([1], [], [1]),
        ([], [], []),
        ([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6]),   # no interleaving needed
        ([5], [1, 2, 3], [1, 2, 3, 5]),
    ]
    for a, b, expected in cases:
        got = to_list(merge_two_lists(build(a), build(b)))
        print(a, b, "->", got, got == expected)

    print(to_list(merge_two_lists_recursive(build([1, 2, 4]), build([1, 3, 5]))))
