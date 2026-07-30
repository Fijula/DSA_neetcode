# Two Sum II - Input Array Is Sorted
# Given a 1-indexed array of integers sorted in NON-DECREASING order, find the two
# numbers that add up to target and return their 1-based indices [i, j] with i < j.
# Exactly one solution exists and one element may not be used twice.
# Example: numbers=[1,2,3,4], target=3 -> [1,2]
#          numbers=[2,3,4],   target=6 -> [1,3]


# Case 1: Brute force: try every pair
def two_sum_brute(numbers, target):
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]  # +1 because the answer is 1-indexed
    return []
# Time:  O(n^2)
# Space: O(1)


# Case 2: Hash map: remember what we have seen and look for the complement
def two_sum_hash(numbers, target):
    seen = {}                          # value -> its 1-based index
    for i, num in enumerate(numbers):
        need = target - num
        if need in seen:
            return [seen[need], i + 1]
        seen[num] = i + 1
    return []
# Time:  O(n)
# Space: O(n)
# Note: works on unsorted input too, but wastes the fact that this array IS sorted.


# Case 3: Optimal: two pointers from both ends - O(1) space, thanks to the sorting
def two_sum(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1                  # need a bigger sum: raise the smaller value
        else:
            right -= 1                 # need a smaller sum: lower the bigger value
    return []
# Time:  O(n)   the pointers only ever move toward each other
# Space: O(1)
# Why moving one pointer never skips the answer: if the sum is too small, no pair
# using the current left value can work, so left can be discarded safely.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4], 3, [1, 2]),
        ([2, 3, 4], 6, [1, 3]),
        ([-1, 0], -1, [1, 2]),
        ([1, 3, 4, 5, 7, 10, 11], 9, [3, 4]),   # 4 + 5
    ]
    for numbers, target, expected in cases:
        got = two_sum(numbers, target)
        print(numbers, target, "->", got, got == expected)

    print(two_sum_brute([2, 3, 4], 6))     # [1, 3]
    print(two_sum_hash([1, 2, 3, 4], 3))   # [1, 2]
