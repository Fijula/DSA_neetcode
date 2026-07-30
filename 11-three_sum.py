# 3Sum
# Given an integer array nums, return all unique triplets [nums[i], nums[j], nums[k]]
# with i != j != k that sum to 0. The triplets themselves must not repeat.
# Example: nums=[-1,0,1,2,-1,-4] -> [[-1,-1,2],[-1,0,1]]
#          nums=[0,1,1]          -> []
#          nums=[0,0,0]          -> [[0,0,0]]


# Case 1: Brute force: every triple, deduplicated with a set of sorted tuples
def three_sum_brute(nums):
    n = len(nums)
    found = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    # sort the triplet so [-1,0,1] and [0,1,-1] collapse into one
                    found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in sorted(found)]
# Time:  O(n^3)
# Space: O(number of triplets)


# Case 2: Optimal: sort, fix one number, then two pointers on the rest
def three_sum(nums):
    nums = sorted(nums)               # sorted() copies, so the caller's list is safe
    n = len(nums)
    result = []

    for i in range(n - 2):
        if nums[i] > 0:
            break                     # sorted, so three positives can never sum to 0
        if i > 0 and nums[i] == nums[i - 1]:
            continue                  # same anchor as last round: skip duplicates

        left, right = i + 1, n - 1    # two-pointer scan over the remaining window
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1             # too small: need a bigger number
            elif total > 0:
                right -= 1            # too big: need a smaller number
            else:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                # skip repeats of the values we just used, or we emit the triplet twice
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

    return result
# Time:  O(n^2)   O(n log n) sort + O(n) anchors x O(n) two-pointer scan
# Space: O(n)     for the sorted copy (output not counted)


if __name__ == "__main__":
    cases = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),          # duplicates must not multiply the answer
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
    ]
    for nums, expected in cases:
        got = three_sum(nums)
        print(nums, "->", got, got == expected)

    print(three_sum_brute([-1, 0, 1, 2, -1, -4]))   # [[-1, -1, 2], [-1, 0, 1]]
