# Find Minimum in Rotated Sorted Array
# A sorted array was rotated some number of times. Return its minimum element in
# O(log n) time. All values are unique.
# Example: nums=[3,4,5,6,1,2] -> 1
#          nums=[4,5,0,1,2,3] -> 0
#          nums=[1,2,3]       -> 1   (not rotated at all)


# Case 1: Brute force: just scan for the smallest value
def find_min_brute(nums):
    smallest = nums[0]
    for num in nums:
        smallest = min(smallest, num)
    return smallest
# Time:  O(n)
# Space: O(1)
# Note: correct, but ignores the sorted structure and misses the O(log n) target.


# Case 2: Optimal: binary search on which HALF is properly sorted
def find_min(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[right]:
            # mid is in the "high" segment before the rotation point,
            # so the minimum must be strictly to the right of mid
            left = mid + 1
        else:
            # nums[mid] <= nums[right]: this half is sorted, so mid could BE the
            # minimum - never discard it
            right = mid

    return nums[left]                  # left == right: the single surviving candidate
# Time:  O(log n)
# Space: O(1)
# Comparing against nums[right] rather than nums[left] is what keeps this short:
# it distinguishes "still in the rotated part" from "already in the sorted part"
# with a single test, and the loop condition left < right avoids an infinite loop.


if __name__ == "__main__":
    cases = [
        ([3, 4, 5, 6, 1, 2], 1),
        ([4, 5, 0, 1, 2, 3], 0),
        ([1, 2, 3], 1),                # no rotation
        ([2, 1], 1),
        ([1], 1),
        ([5, 1, 2, 3, 4], 1),          # rotated by one
        ([2, 3, 4, 5, 1], 1),
        ([11, 13, 15, 17], 11),
    ]
    for nums, expected in cases:
        got = find_min(nums)
        print(nums, "->", got, got == expected)

    print(find_min_brute([4, 5, 0, 1, 2, 3]))   # 0
