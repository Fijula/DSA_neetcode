# Largest Rectangle in Histogram
# heights[i] is the height of bar i, every bar has width 1. Return the area of the
# largest rectangle that fits entirely inside the histogram.
# Example: heights=[7,1,7,2,2,4] -> 8    the last 4 bars at height 2 give 4x2=8
#          heights=[1,3,7]       -> 7
#          heights=[2,1,5,6,2,3] -> 10   the 5 and 6 bars: 2 wide x 5 tall


# Case 1: Brute force: expand left and right from each bar while it stays tall enough
def largest_rectangle_area_brute(heights):
    n = len(heights)
    best = 0
    for i in range(n):
        height = heights[i]
        left = i
        while left > 0 and heights[left - 1] >= height:
            left -= 1                  # extend while the neighbours are at least as tall
        right = i
        while right < n - 1 and heights[right + 1] >= height:
            right += 1
        best = max(best, height * (right - left + 1))
    return best
# Time:  O(n^2)
# Space: O(1)


# Case 2: Optimal: monotonic increasing stack of (start_index, height)
def largest_rectangle_area(heights):
    stack = []                         # (index the bar can extend back to, height)
    best = 0

    for i, height in enumerate(heights):
        start = i
        # every taller bar on the stack is blocked by this shorter one: settle it now
        while stack and stack[-1][1] > height:
            prev_index, prev_height = stack.pop()
            best = max(best, prev_height * (i - prev_index))
            start = prev_index         # this bar inherits the popped bar's reach left
        stack.append((start, height))

    # whatever survives can extend all the way to the right edge
    for index, height in stack:
        best = max(best, height * (len(heights) - index))
    return best
# Time:  O(n)   each bar is pushed once and popped at most once
# Space: O(n)   the stack
# The `start = prev_index` line is the subtle part: after popping a taller bar, the
# current shorter bar could have started back where that bar did, since everything
# between them was at least as tall as it.


if __name__ == "__main__":
    cases = [
        ([7, 1, 7, 2, 2, 4], 8),
        ([1, 3, 7], 7),
        ([2, 1, 5, 6, 2, 3], 10),
        ([2, 4], 4),
        ([5], 5),
        ([3, 3, 3], 9),                # a flat block: full width x height
        ([], 0),
    ]
    for heights, expected in cases:
        got = largest_rectangle_area(heights)
        print(heights, "->", got, got == expected)

    print(largest_rectangle_area_brute([2, 1, 5, 6, 2, 3]))   # 10
