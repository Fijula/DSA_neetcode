# Two Sum
# Given an array nums and a target, return the INDICES of the two numbers that add up
# to target. Exactly one answer exists and one element may not be used twice.
# Example: nums=[3,4,5,6], target=7 -> [0,1]
#          nums=[4,5,6],   target=10 -> [0,2]


# Case 1: Brute force: try every pair
def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):      # j starts after i, so no element is reused
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
# Time:  O(n^2)
# Space: O(1)


# Case 2: Two passes with a hash map: build the index first, then look up
def two_sum_two_pass(nums, target):
    index_of = {num: i for i, num in enumerate(nums)}

    for i, num in enumerate(nums):
        need = target - num
        # the complement must exist AND be a DIFFERENT element
        if need in index_of and index_of[need] != i:
            return [i, index_of[need]]
    return []
# Time:  O(n)
# Space: O(n)
# Note: with duplicates the dict keeps only the LAST index of a value, which is why
# the `!= i` guard is needed - and why the one-pass version below is safer.


# Case 3: Optimal: one pass, storing values only AFTER checking for the complement
def two_sum(nums, target):
    seen = {}                          # value -> the index it was found at

    for i, num in enumerate(nums):
        need = target - num
        if need in seen:
            return [seen[need], i]     # earlier index first
        seen[num] = i                  # store AFTER the check, so i is never matched
                                       # against itself
    return []
# Time:  O(n)   one pass, O(1) lookups
# Space: O(n)   worst case every value is stored
# Storing after checking is the whole safety property: the map only ever holds
# elements strictly before i, so a hit is guaranteed to be a different element.


if __name__ == "__main__":
    cases = [
        ([3, 4, 5, 6], 7, [0, 1]),
        ([4, 5, 6], 10, [0, 2]),
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 3], 6, [0, 1]),           # duplicates: must return two distinct indices
        ([3, 2, 4], 6, [1, 2]),        # the naive "first match" answer [0,0] is wrong
        ([0, 0], 0, [0, 1]),
        ([-1, -2, -3], -5, [1, 2]),
    ]
    for nums, target, expected in cases:
        got = two_sum(nums, target)
        print(nums, target, "->", got, got == expected)

    print(two_sum_brute([3, 2, 4], 6))      # [1, 2]
    print(two_sum_two_pass([2, 7, 11, 15], 9))   # [0, 1]
