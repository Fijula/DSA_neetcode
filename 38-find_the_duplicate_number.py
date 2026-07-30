# Find the Duplicate Number
# nums has n+1 integers, each in the range [1, n], and exactly one value repeats.
# Return that value WITHOUT modifying the array and in O(1) extra space.
# Example: nums=[1,2,3,2,2] -> 2
#          nums=[1,3,4,2,2] -> 2


# Case 1: Hash set: remember what has been seen
def find_duplicate_set(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
    return -1
# Time:  O(n)
# Space: O(n)   breaks the O(1) space requirement


# Case 2: Sort, then look for two neighbours that are equal
def find_duplicate_sort(nums):
    ordered = sorted(nums)             # sorted() copies, so the input stays untouched
    for i in range(1, len(ordered)):
        if ordered[i] == ordered[i - 1]:
            return ordered[i]
    return -1
# Time:  O(n log n)
# Space: O(n)   for the copy


# Case 3: Optimal: Floyd's cycle detection, treating values as next pointers
def find_duplicate(nums):
    # Think of i -> nums[i] as a linked list. Because values are in [1, n] and there
    # are n+1 of them, two indices point at the same value, creating a cycle whose
    # ENTRANCE is the duplicate.
    slow, fast = 0, 0
    while True:
        slow = nums[slow]              # one step
        fast = nums[nums[fast]]        # two steps
        if slow == fast:
            break                      # they met somewhere inside the cycle

    # phase 2: walk one pointer from the start; they meet at the cycle entrance
    slow2 = 0
    while slow != slow2:
        slow = nums[slow]
        slow2 = nums[slow2]
    return slow
# Time:  O(n)
# Space: O(1)   and the array is never modified
# The phase-2 restart works because the distance from the start to the entrance equals
# the distance from the meeting point to the entrance, going around the loop.


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 2, 2], 2),
        ([1, 3, 4, 2, 2], 2),
        ([3, 1, 3, 4, 2], 3),
        ([1, 1], 1),
        ([2, 2, 2, 2, 2], 2),          # the duplicate appears many times
        ([1, 4, 4, 2, 3], 4),
    ]
    for nums, expected in cases:
        before = list(nums)
        got = find_duplicate(nums)
        # confirm the input was not mutated, as the problem requires
        print(nums, "->", got, got == expected, "unchanged:", nums == before)

    print(find_duplicate_set([1, 3, 4, 2, 2]))    # 2
    print(find_duplicate_sort([3, 1, 3, 4, 2]))   # 3
