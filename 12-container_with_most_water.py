# Container With Most Water
# heights[i] is the height of a vertical bar at position i. Pick two bars so that the
# water held between them is maximised, and return that amount.
# Water = (distance between the bars) * (height of the SHORTER bar).
# Example: heights=[1,7,2,5,4,7,3,6] -> 36
#          heights=[2,2,2]           -> 4


# Case 1: Brute force: try every pair of bars
def max_area_brute(heights):
    n = len(heights)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            width = j - i
            height = min(heights[i], heights[j])   # the shorter bar limits the water
            best = max(best, width * height)
    return best
# Time:  O(n^2)
# Space: O(1)


# Case 2: Optimal: two pointers from both ends, always move the SHORTER bar
def max_area(heights):
    left, right = 0, len(heights) - 1
    best = 0

    while left < right:
        width = right - left
        best = max(best, width * min(heights[left], heights[right]))

        if heights[left] < heights[right]:
            left += 1                  # the short side caps us, so discard it
        else:
            right -= 1
    return best
# Time:  O(n)   one pass, the pointers meet in the middle
# Space: O(1)
# Why discarding the shorter bar is safe: keeping it and moving the taller one only
# shrinks the width while the height stays capped by that same short bar, so every
# pair we skip is worse than the one we just measured.


if __name__ == "__main__":
    cases = [
        ([1, 7, 2, 5, 4, 7, 3, 6], 36),
        ([2, 2, 2], 4),
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),         # the two tall walls at the ends win
    ]
    for heights, expected in cases:
        got = max_area(heights)
        print(heights, "->", got, got == expected)

    print(max_area_brute([1, 7, 2, 5, 4, 7, 3, 6]))   # 36
