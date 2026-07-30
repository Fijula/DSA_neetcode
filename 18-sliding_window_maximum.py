# Sliding Window Maximum
# Given an array nums and a window size k, return a list holding the maximum of every
# window of size k as it slides from left to right.
# Example: nums=[1,2,1,0,4,2,6], k=3 -> [2,2,4,4,6]
#          nums=[1],             k=1 -> [1]


# Case 1: Brute force: take max() of every window
def max_sliding_window_brute(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
# Time:  O(n * k)   max() rescans the whole window each time
# Space: O(n - k + 1)   for the output


# Case 2: Optimal: monotonic decreasing deque holding INDICES
from collections import deque

def max_sliding_window(nums, k):
    if not nums or k <= 0:
        return []

    dq = deque()                       # indices, values at them strictly decreasing
    result = []

    for i, num in enumerate(nums):
        # any smaller value still in the deque can never be a future maximum,
        # because `num` is both bigger AND stays in the window longer
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)

        if dq[0] <= i - k:             # the front has slid out of the window
            dq.popleft()

        if i >= k - 1:                 # the first full window has formed
            result.append(nums[dq[0]])   # front is always the window maximum
    return result
# Time:  O(n)   each index is pushed once and popped at most once
# Space: O(k)   the deque never holds more than one window's worth
# The deque stays sorted descending by value, so its front is the answer for free -
# no scanning of the window is ever needed.


if __name__ == "__main__":
    cases = [
        ([1, 2, 1, 0, 4, 2, 6], 3, [2, 2, 4, 4, 6]),
        ([1], 1, [1]),
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([9, 8, 7, 6], 2, [9, 8, 7]),           # decreasing input
        ([1, 2, 3, 4], 4, [4]),                 # window covers the whole array
        ([7, 7, 7], 2, [7, 7]),                 # ties must not drop entries wrongly
    ]
    for nums, k, expected in cases:
        got = max_sliding_window(nums, k)
        print(nums, k, "->", got, got == expected)

    print(max_sliding_window_brute([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [3,3,5,5,6,7]
