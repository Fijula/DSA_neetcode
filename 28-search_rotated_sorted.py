# Search in Rotated Sorted Array
# A sorted array of unique integers was rotated. Return the index of target,
# or -1 if it is absent. Must run in O(log n).
# Example: nums=[3,4,5,6,1,2], target=1 -> 4
#          nums=[3,5,6,0,1,2], target=4 -> -1


# Case 1: Brute force: linear scan
def search_brute(nums, target):
    for i, num in enumerate(nums):
        if num == target:
            return i
    return -1
# Time:  O(n)
# Space: O(1)


# Case 2: Optimal: binary search, deciding which half is sorted each step
def search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            # the LEFT half is sorted normally
            if nums[left] <= target < nums[mid]:
                right = mid - 1        # target lies inside that sorted half
            else:
                left = mid + 1         # it must be in the messy right half
        else:
            # the RIGHT half is sorted normally
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
# Time:  O(log n)
# Space: O(1)
# Key idea: after a rotation, at least ONE half of any split is still fully sorted.
# Identify that half, and a simple range check tells you whether target is in it -
# if not, the answer must be in the other half.


# Case 3: Two-phase: find the rotation point, then do a plain binary search
def search_two_phase(nums, target):
    if not nums:
        return -1

    # phase 1: locate the index of the smallest element (the rotation point)
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    pivot = left

    # phase 2: ordinary binary search over the rotated index space
    n = len(nums)
    left, right = 0, n - 1
    while left <= right:
        mid = (left + right) // 2
        real = (mid + pivot) % n       # map the virtual index onto the real array
        if nums[real] == target:
            return real
        if nums[real] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
# Time: O(log n), Space: O(1)


if __name__ == "__main__":
    cases = [
        ([3, 4, 5, 6, 1, 2], 1, 4),
        ([3, 5, 6, 0, 1, 2], 4, -1),
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([1], 1, 0),
        ([1], 2, -1),
        ([1, 2, 3, 4, 5], 5, 4),       # not rotated
        ([5, 1, 2, 3, 4], 5, 0),
    ]
    for nums, target, expected in cases:
        got = search(nums, target)
        print(nums, target, "->", got, got == expected)

    print(search_brute([3, 4, 5, 6, 1, 2], 1))        # 4
    print(search_two_phase([4, 5, 6, 7, 0, 1, 2], 0))  # 4
