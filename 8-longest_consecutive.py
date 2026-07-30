# Longest Consecutive Sequence
# Given an unsorted array of integers nums, return the LENGTH of the longest
# sequence of consecutive integers that can be formed. The elements do not have
# to be next to each other in the array. Must run in O(n) time.
# Example: nums=[2,20,4,10,3,4,5]   -> 4   the sequence [2,3,4,5]
#          nums=[0,3,2,5,4,6,1,1]   -> 7   the sequence [0,1,2,3,4,5,6]


# Case 1: Brute force: for every number, walk upward while the next one exists
def longest_consecutive_brute(nums):
    longest = 0
    for num in nums:
        current = num
        streak = 1
        while current + 1 in nums:     # `in` on a LIST scans it every time
            current += 1
            streak += 1
        longest = max(longest, streak)
    return longest
# Time:  O(n^3) worst case   O(n) numbers x O(n) walk x O(n) list lookup
# Space: O(1)


# Case 2: Sort, then scan for runs that step by exactly 1
def longest_consecutive_sort(nums):
    if not nums:
        return 0

    ordered = sorted(set(nums))        # set() drops duplicates, they break the count
    longest = 1
    streak = 1
    for i in range(1, len(ordered)):
        if ordered[i] == ordered[i - 1] + 1:
            streak += 1                # still climbing the same run
        else:
            streak = 1                 # gap: start a fresh run
        longest = max(longest, streak)
    return longest
# Time:  O(n log n)   dominated by the sort
# Space: O(n)         for the sorted set
# Note: correct, but sorting means it misses the O(n) requirement.


# Case 3: Optimal: hash set, and only start counting from the START of a sequence
def longest_consecutive(nums):
    num_set = set(nums)                # O(1) membership checks
    longest = 0

    for num in num_set:
        if num - 1 in num_set:
            continue                   # not a start: someone else will count this run

        length = 1                     # num starts a sequence, walk it upward
        while num + length in num_set:
            length += 1

        longest = max(longest, length)
    return longest
# Time:  O(n)   each number is visited once as a start and once inside one walk
# Space: O(n)   for the set
# Why it is O(n) despite the inner while loop: the walk only runs for numbers with
# no left neighbour, so every element is stepped over by exactly one walk total.


if __name__ == "__main__":
    cases = [
        ([2, 20, 4, 10, 3, 4, 5], 4),
        ([0, 3, 2, 5, 4, 6, 1, 1], 7),
        ([], 0),
        ([5], 1),
        ([1, 1, 1], 1),                # all duplicates: sequence length is still 1
        ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6], 7),   # [3,4,5,6,7,8,9]
    ]

    for nums, expected in cases:
        got = longest_consecutive(nums)
        print(nums, "->", got, got == expected)

    print(longest_consecutive_brute([2, 20, 4, 10, 3, 4, 5]))   # 4
    print(longest_consecutive_sort([0, 3, 2, 5, 4, 6, 1, 1]))   # 7
