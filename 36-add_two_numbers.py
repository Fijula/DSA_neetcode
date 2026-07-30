# Add Two Numbers
# Two non-negative integers are stored as linked lists with the digits in REVERSE
# order (least significant digit first). Add them and return the sum the same way.
# Example: [1,2,3] + [4,5,6] -> [5,7,9]      321 + 654 = 975
#          [9]     + [9]     -> [8,1]        9 + 9 = 18


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


# Case 1: Optimal: one pass, adding digit by digit with a carry
def add_two_numbers(l1, l2):
    dummy = ListNode()
    tail = dummy
    carry = 0

    # keep going while either list has digits left OR a carry is still pending
    while l1 or l2 or carry:
        digit1 = l1.val if l1 else 0   # a missing digit counts as 0
        digit2 = l2.val if l2 else 0

        total = digit1 + digit2 + carry
        carry = total // 10            # 0 or 1
        tail.next = ListNode(total % 10)
        tail = tail.next

        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy.next
# Time:  O(max(n, m))
# Space: O(max(n, m))   for the result list
# Reverse order is a gift here: the least significant digits line up at the heads, so
# addition proceeds in exactly the direction the lists are traversed.


# Case 2: Convert to integers, add, convert back  (fine in Python, not in Java)
def add_two_numbers_int(l1, l2):
    def to_int(node):
        value, place = 0, 1
        while node:
            value += node.val * place
            place *= 10
            node = node.next
        return value

    total = to_int(l1) + to_int(l2)
    # digits back out in reverse order, which is the format we need
    digits = [int(c) for c in str(total)][::-1]
    return build(digits)
# Time:  O(n + m)
# Space: O(n + m)
# Note: relies on unbounded integers. In a language with 32/64-bit ints this
# overflows, which is exactly why the digit-by-digit version is the real answer.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3], [4, 5, 6], [5, 7, 9]),
        ([9], [9], [8, 1]),
        ([0], [0], [0]),
        ([9, 9, 9], [1], [0, 0, 0, 1]),          # carry ripples through and extends
        ([2, 4, 3], [5, 6, 4], [7, 0, 8]),
        ([1], [9, 9, 9], [0, 0, 0, 1]),          # different lengths
    ]
    for a, b, expected in cases:
        got = to_list(add_two_numbers(build(a), build(b)))
        print(a, b, "->", got, got == expected)

    print(to_list(add_two_numbers_int(build([9, 9, 9]), build([1]))))   # [0, 0, 0, 1]
