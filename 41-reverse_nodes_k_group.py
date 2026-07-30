# Reverse Nodes in k-Group
# Reverse the nodes of a linked list k at a time and return the new head. If the
# final group has fewer than k nodes, leave it as it is.
# Example: head=[1,2,3,4,5], k=2 -> [2,1,4,3,5]
#          head=[1,2,3,4,5], k=3 -> [3,2,1,4,5]


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


# Case 1: Brute force: collect the values, reverse them in chunks, rebuild
def reverse_k_group_values(head, k):
    values = to_list(head)
    result = []
    for i in range(0, len(values), k):
        chunk = values[i:i + k]
        # only reverse FULL groups; a short tail is left alone
        result.extend(chunk[::-1] if len(chunk) == k else chunk)
    return build(result)
# Time:  O(n)
# Space: O(n)   and it allocates brand new nodes rather than relinking


# Case 2: Optimal: relink in place, one group at a time
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy                 # the node just before the group being reversed

    while True:
        # look ahead k nodes; if fewer exist, this tail stays as it is
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next

        group_next = kth.next          # the first node AFTER this group

        # reverse the group: point each node at its predecessor
        prev, current = group_next, group_prev.next
        while current is not group_next:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        # group_prev.next was the group's first node, which is now its LAST node.
        # Save it before rewiring, because it becomes the next group_prev.
        new_group_prev = group_prev.next
        group_prev.next = kth          # kth is now the group's first node
        group_prev = new_group_prev
# Time:  O(n)   each node is visited a constant number of times
# Space: O(1)   pure pointer surgery
# Seeding `prev = group_next` instead of None is the neat part: it connects the
# reversed group to the rest of the list without a separate fix-up step.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),
        ([1, 2, 3, 4], 2, [2, 1, 4, 3]),
        ([1, 2, 3], 1, [1, 2, 3]),               # k=1 changes nothing
        ([1, 2], 3, [1, 2]),                     # k larger than the list
        ([], 2, []),
        ([1, 2, 3, 4, 5, 6], 3, [3, 2, 1, 6, 5, 4]),
    ]
    for values, k, expected in cases:
        got = to_list(reverse_k_group(build(values), k))
        print(values, k, "->", got, got == expected)

    print(to_list(reverse_k_group_values(build([1, 2, 3, 4, 5]), 3)))   # [3,2,1,4,5]
