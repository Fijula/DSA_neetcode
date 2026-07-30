# Median of Two Sorted Arrays
# Given two sorted arrays nums1 and nums2, return the median of their combined
# contents. Must run in O(log(m + n)).
# Example: nums1=[1,2], nums2=[3]     -> 2.0
#          nums1=[1,3], nums2=[2,4]   -> 2.5


# Case 1: Brute force: merge everything and read the middle
def find_median_brute(nums1, nums2):
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n % 2:
        return float(merged[n // 2])   # odd length: the exact middle element
    mid = n // 2
    return (merged[mid - 1] + merged[mid]) / 2   # even: average the two middles
# Time:  O((m+n) log(m+n))   the sort
# Space: O(m+n)


# Case 2: Merge with two pointers, stopping at the halfway mark
def find_median_merge(nums1, nums2):
    total = len(nums1) + len(nums2)
    half = total // 2

    i = j = 0
    prev = current = 0
    # walk the merge only as far as the median position
    for _ in range(half + 1):
        prev = current
        if i < len(nums1) and (j >= len(nums2) or nums1[i] <= nums2[j]):
            current = nums1[i]
            i += 1
        else:
            current = nums2[j]
            j += 1

    if total % 2:
        return float(current)
    return (prev + current) / 2
# Time:  O(m + n)
# Space: O(1)


# Case 3: Optimal: binary search for the correct PARTITION of the smaller array
def find_median(nums1, nums2):
    # always binary search the shorter array so the index maths stays in range
    a, b = (nums1, nums2) if len(nums1) <= len(nums2) else (nums2, nums1)
    total = len(a) + len(b)
    half = total // 2

    left, right = 0, len(a) - 1
    while True:
        i = (left + right) // 2            # take a[0 .. i], that is i+1 elements
        j = half - (i + 1) - 1             # take b[0 .. j] to fill the left side

        # values at the partition edges; infinities cover the empty-side cases
        a_left = a[i] if i >= 0 else float("-inf")
        a_right = a[i + 1] if (i + 1) < len(a) else float("inf")
        b_left = b[j] if j >= 0 else float("-inf")
        b_right = b[j + 1] if (j + 1) < len(b) else float("inf")

        if a_left <= b_right and b_left <= a_right:
            # correct partition: every left value is <= every right value
            if total % 2:
                return float(min(a_right, b_right))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2

        if a_left > b_right:
            right = i - 1                  # took too much from a
        else:
            left = i + 1                   # took too little from a
# Time:  O(log(min(m, n)))
# Space: O(1)
# The insight: the median only depends on WHERE you cut the two arrays, not on
# merging them. A cut is correct when both left maxima are <= both right minima.


if __name__ == "__main__":
    cases = [
        ([1, 2], [3], 2.0),
        ([1, 3], [2, 4], 2.5),
        ([1, 2, 3, 4], [5, 6, 7, 8], 4.5),
        ([], [1], 1.0),                # one array empty
        ([2], [], 2.0),
        ([1, 1], [1, 1], 1.0),         # all equal
        ([1, 2, 3], [4, 5, 6, 7, 8], 4.5),
    ]
    for nums1, nums2, expected in cases:
        got = find_median(nums1, nums2)
        print(nums1, nums2, "->", got, got == expected)

    print(find_median_brute([1, 3], [2, 4]))   # 2.5
    print(find_median_merge([1, 2], [3]))      # 2.0
