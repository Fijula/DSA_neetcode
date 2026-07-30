# Koko Eating Bananas
# piles[i] bananas sit in pile i. Koko eats at a fixed speed of k bananas per hour:
# each hour she picks one pile and eats k from it (or the whole pile if it has fewer,
# spending the rest of that hour idle). Return the SMALLEST k that finishes every pile
# within h hours.
# Example: piles=[1,4,3,2], h=9 -> 2
#          piles=[25,10,23,4],h=4 -> 25


# Case 1: Brute force: try every speed from 1 upward
import math

def min_eating_speed_brute(piles, h):
    def hours_needed(speed):
        # each pile takes ceil(pile / speed) hours - she never mixes piles in an hour
        return sum(math.ceil(pile / speed) for pile in piles)

    speed = 1
    while hours_needed(speed) > h:
        speed += 1
    return speed
# Time:  O(max(piles) * n)   worst case tries every speed
# Space: O(1)


# Case 2: Optimal: binary search over the SPEED, not over the array
def min_eating_speed(piles, h):
    # any speed in [1, max(piles)] is worth considering; going faster than the biggest
    # pile cannot save time, since only one pile is eaten per hour
    left, right = 1, max(piles)
    best = right

    while left <= right:
        speed = left + (right - left) // 2

        hours = 0
        for pile in piles:
            hours += math.ceil(pile / speed)

        if hours <= h:
            best = speed               # this speed works, try to go slower
            right = speed - 1
        else:
            left = speed + 1           # too slow, must speed up

    return best
# Time:  O(n log(max(piles)))
# Space: O(1)
# The idea worth taking away: binary search does not need a sorted array - it needs a
# MONOTONIC predicate. Here "can she finish in h hours at speed k?" is False for small
# k and True for all larger k, so the boundary between them can be bisected.


if __name__ == "__main__":
    cases = [
        ([1, 4, 3, 2], 9, 2),
        ([25, 10, 23, 4], 4, 25),
        ([3, 6, 7, 11], 8, 4),
        ([30, 11, 23, 4, 20], 5, 30),
        ([30, 11, 23, 4, 20], 6, 23),
        ([1], 1, 1),
        ([312884470], 968709470, 1),   # far more hours than needed: speed 1 suffices
    ]
    for piles, h, expected in cases:
        got = min_eating_speed(piles, h)
        print(piles, h, "->", got, got == expected)

    print(min_eating_speed_brute([1, 4, 3, 2], 9))    # 2
    print(min_eating_speed_brute([3, 6, 7, 11], 8))   # 4
