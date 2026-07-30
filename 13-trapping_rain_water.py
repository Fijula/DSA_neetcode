# Trapping Rain Water
# height[i] is the elevation at position i. Return how much rain water is trapped.
# Key insight: water above index i = min(tallest bar to its LEFT,
#                                       tallest bar to its RIGHT) - height[i]
# Example: height=[0,2,0,3,1,0,1,3,2,1] -> 9
#          height=[4,2,0,3,2,5]         -> 9


# Case 1: Brute force: for each index, rescan both sides for the tallest bar
def trap_brute(height):
    n = len(height)
    total = 0
    for i in range(n):
        left_max = max(height[:i + 1])      # tallest bar from the start up to i
        right_max = max(height[i:])         # tallest bar from i to the end
        total += min(left_max, right_max) - height[i]
    return total
# Time:  O(n^2)   a rescan of both sides for every index
# Space: O(1)     (ignoring the slices Python builds)


# Case 2: Prefix / suffix arrays: precompute the two maxima in one pass each
def trap_prefix(height):
    if not height:
        return 0
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))
# Time:  O(n)   three passes
# Space: O(n)   two helper arrays


# Case 3: Optimal: two pointers, tracking only the running maxima
def trap(height):
    if not height:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total = 0

    while left < right:
        if left_max <= right_max:
            left += 1
            left_max = max(left_max, height[left])
            total += left_max - height[left]     # left_max is the binding wall here
        else:
            right -= 1
            right_max = max(right_max, height[right])
            total += right_max - height[right]
    return total
# Time:  O(n)   single pass
# Space: O(1)   two scalars instead of two arrays
# Why it works: whichever side has the SMALLER max is the side whose water level is
# already decided, so that column can be settled without knowing the other side.


if __name__ == "__main__":
    cases = [
        ([0, 2, 0, 3, 1, 0, 1, 3, 2, 1], 9),
        ([4, 2, 0, 3, 2, 5], 9),
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([], 0),
        ([3, 3, 3], 0),                # flat: nothing is trapped
        ([5, 4, 3, 2, 1], 0),          # monotonic slope: nothing is trapped
    ]
    for height, expected in cases:
        got = trap(height)
        print(height, "->", got, got == expected)

    print(trap_brute([4, 2, 0, 3, 2, 5]))    # 9
    print(trap_prefix([4, 2, 0, 3, 2, 5]))   # 9
