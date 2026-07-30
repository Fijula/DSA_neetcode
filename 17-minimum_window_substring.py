# Minimum Window Substring
# Given strings s and t, return the SHORTEST substring of s that contains every
# character of t including duplicates. Return "" if no such window exists.
# Example: s="OUZODYXAZV", t="XYZ" -> "YXAZ"
#          s="xyz",        t="xyz" -> "xyz"
#          s="x",          t="xy"  -> ""


# Case 1: Brute force: test every substring, keep the shortest valid one
from collections import Counter

def min_window_brute(s, t):
    if not t or not s:
        return ""

    need = Counter(t)
    best = ""
    n = len(s)
    for i in range(n):
        for j in range(i + len(t), n + 1):
            window = Counter(s[i:j])
            # every needed character present in at least the needed quantity?
            if all(window[c] >= need[c] for c in need):
                if not best or (j - i) < len(best):
                    best = s[i:j]
                break                  # growing this start index further only lengthens
    return best
# Time:  O(n^2 * alphabet)
# Space: O(n)


# Case 2: Optimal: sliding window that grows right, then shrinks left while valid
def min_window(s, t):
    if not t or not s:
        return ""

    need = Counter(t)
    window = {}
    have, required = 0, len(need)       # `required` = how many DISTINCT chars to satisfy
    best_len = float("inf")
    best_range = [-1, -1]
    left = 0

    for right, char in enumerate(s):
        window[char] = window.get(char, 0) + 1
        # this character just brought its count up to exactly what t needs
        if char in need and window[char] == need[char]:
            have += 1

        while have == required:          # valid window: try to shrink it
            if (right - left + 1) < best_len:
                best_len = right - left + 1
                best_range = [left, right]

            left_char = s[left]
            window[left_char] -= 1
            if left_char in need and window[left_char] < need[left_char]:
                have -= 1                # dropping it broke validity, stop shrinking
            left += 1

    left, right = best_range
    return s[left:right + 1] if best_len != float("inf") else ""
# Time:  O(n + m)   each pointer sweeps s at most once
# Space: O(alphabet)
# The `have` counter is the trick: it avoids re-comparing two whole dictionaries on
# every step, turning the validity check into a single integer comparison.


if __name__ == "__main__":
    cases = [
        ("OUZODYXAZV", "XYZ", "YXAZ"),
        ("xyz", "xyz", "xyz"),
        ("x", "xy", ""),
        ("ADOBECODEBANC", "ABC", "BANC"),
        ("a", "aa", ""),               # duplicates in t must be respected
        ("aa", "aa", "aa"),
        ("", "a", ""),
    ]
    for s, t, expected in cases:
        got = min_window(s, t)
        print(repr(s), repr(t), "->", repr(got), got == expected)

    print(min_window_brute("ADOBECODEBANC", "ABC"))   # BANC
