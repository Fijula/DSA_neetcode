# Kth Largest Element in an Array
# Return the kth largest value in an unsorted array. Duplicates count separately, so
# this is the kth largest by POSITION in sorted order, not the kth distinct value.
# Example: nums=[2,3,1,5,4], k=2 -> 4
#          nums=[2,2,3,1],   k=3 -> 2


# Case 1: Sort and index from the end
def find_kth_largest_sorted(nums, k):
    return sorted(nums)[-k]
# Time:  O(n log n)
# Space: O(n)


# Case 2: Min-heap of size k
import heapq

def find_kth_largest_heap(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)        # drop the smallest, keep the k largest
    return heap[0]
# Time:  O(n log k)
# Space: O(k)
# Shortcut: heapq.nlargest(k, nums)[-1] does the same thing in one call.


# Case 3: Optimal average case: Quickselect (partial quicksort)
import random

def find_kth_largest(nums, k):
    nums = list(nums)                  # copy: quickselect reorders in place
    target = len(nums) - k             # the kth largest sits at this SORTED index

    left, right = 0, len(nums) - 1
    while True:
        # a random pivot avoids the O(n^2) worst case on sorted input
        pivot_index = random.randint(left, right)
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        pivot = nums[right]

        # Lomuto partition: everything < pivot is moved to the front
        store = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]

        # the pivot is now at its final sorted position
        if store == target:
            return nums[store]
        if store < target:
            left = store + 1           # recurse into the upper part only
        else:
            right = store - 1
# Time:  O(n) average, O(n^2) worst case
# Space: O(1)
# Why it beats sorting: each partition throws away the side that cannot contain the
# answer, so the work halves rather than sorting everything you do not need.


if __name__ == "__main__":
    cases = [
        ([2, 3, 1, 5, 4], 2, 4),
        ([2, 2, 3, 1], 3, 2),
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        ([1], 1, 1),
        ([7, 7, 7], 2, 7),             # duplicates count separately
        ([-1, -5, -3], 1, -1),
    ]
    for nums, k, expected in cases:
        got = find_kth_largest(nums, k)
        print(nums, k, "->", got, got == expected)

    print(find_kth_largest_sorted([3, 2, 1, 5, 6, 4], 2))   # 5
    print(find_kth_largest_heap([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))   # 4
