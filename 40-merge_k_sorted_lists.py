# Merge k Sorted Linked Lists
# Given an array of k sorted linked lists, merge them all into one sorted list.
# Example: [[1,2,4],[1,3,5],[3,6]] -> [1,1,2,3,3,4,5,6]
#          []                      -> []


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


def _merge_two(list1, list2):
    """The two-list merge from problem 32, reused as a building block."""
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 if list1 else list2
    return dummy.next


# Case 1: Brute force: merge them one at a time into an accumulator
def merge_k_lists_sequential(lists):
    result = None
    for head in lists:
        result = _merge_two(result, head)
    return result
# Time:  O(k * n)   the accumulator is re-walked on every merge
# Space: O(1)
# With k lists of n nodes each this is O(k^2 * n) in total node visits - the early
# merges get traversed again and again.


# Case 2: Optimal: divide and conquer, merging lists in PAIRS
def merge_k_lists(lists):
    if not lists:
        return None

    while len(lists) > 1:
        merged = []
        # pair up neighbours: k lists become k/2, then k/4, ...
        for i in range(0, len(lists), 2):
            list1 = lists[i]
            list2 = lists[i + 1] if (i + 1) < len(lists) else None
            merged.append(_merge_two(list1, list2))
        lists = merged

    return lists[0]
# Time:  O(n log k)   log k rounds, each touching all n nodes once
# Space: O(k)         for the intermediate list array
# Pairing is what removes the repeated re-walking: every node is copied through
# exactly log k merges instead of up to k of them.


# Case 3: Min-heap: always pull the smallest head among the k lists
import heapq

def merge_k_lists_heap(lists):
    heap = []
    # seed the heap with each list's head; the index breaks ties so ListNode is
    # never compared directly (it has no __lt__)
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))

    dummy = ListNode()
    tail = dummy
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
# Time:  O(n log k)   each node is pushed and popped once, heap size is k
# Space: O(k)


if __name__ == "__main__":
    cases = [
        ([[1, 2, 4], [1, 3, 5], [3, 6]], [1, 1, 2, 3, 3, 4, 5, 6]),
        ([], []),
        ([[]], []),
        ([[1]], [1]),
        ([[], [1], []], [1]),                    # some lists empty
        ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
        ([[1], [2], [3], [4], [5]], [1, 2, 3, 4, 5]),   # odd k, tests the pairing
    ]
    for lists, expected in cases:
        got = to_list(merge_k_lists([build(v) for v in lists]))
        print(lists, "->", got, got == expected)

    print(to_list(merge_k_lists_sequential([build(v) for v in [[1, 2, 4], [1, 3, 5]]])))
    print(to_list(merge_k_lists_heap([build(v) for v in [[1, 4, 5], [1, 3, 4], [2, 6]]])))
