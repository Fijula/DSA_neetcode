# Binary Search
# Given a sorted array of unique integers, return the index of target, or -1 if it is
# absent. Must run in O(log n).
# Example: nums=[-1,0,3,5,9,12], target=9  -> 4
#          nums=[-1,0,3,5,9,12], target=2  -> -1


# Case 1: Brute force: linear scan
def search_brute(nums, target):
    for i, num in enumerate(nums):
        if num == target:
            return i
    return -1
# Time:  O(n)
# Space: O(1)


# Case 2: Optimal: iterative binary search
def search(nums, target):
    left, right = 0, len(nums) - 1      # an INCLUSIVE range: [left, right]

    while left <= right:                # <= because left == right is still one candidate
        # (left + right) // 2 can overflow in Java/C; this form never does
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1              # target is in the upper half
        else:
            right = mid - 1             # target is in the lower half

    return -1                           # the range collapsed: target is absent
# Time:  O(log n)   the search space halves every iteration
# Space: O(1)
# The two easy bugs: using `<` instead of `<=` (misses a one-element range), and
# writing `left = mid` instead of `mid + 1` (mid never leaves the range -> infinite loop).


# Case 3: Recursive
def search_recursive(nums, target):
    def helper(left, right):
        if left > right:
            return -1                   # empty range
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            return helper(mid + 1, right)
        return helper(left, mid - 1)

    return helper(0, len(nums) - 1)
# Time:  O(log n)
# Space: O(log n)   recursion depth


if __name__ == "__main__":
    cases = [
        ([-1, 0, 3, 5, 9, 12], 9, 4),
        ([-1, 0, 3, 5, 9, 12], 2, -1),
        ([5], 5, 0),
        ([5], -5, -1),
        ([], 1, -1),                   # empty array
        ([1, 2, 3, 4, 5], 1, 0),       # first element
        ([1, 2, 3, 4, 5], 5, 4),       # last element
        ([1, 2], 2, 1),
    ]
    for nums, target, expected in cases:
        got = search(nums, target)
        print(nums, target, "->", got, got == expected)

    print(search_brute([-1, 0, 3, 5, 9, 12], 9))       # 4
    print(search_recursive([-1, 0, 3, 5, 9, 12], 2))   # -1
