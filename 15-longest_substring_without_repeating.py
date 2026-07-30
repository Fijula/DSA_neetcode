# Longest Substring Without Repeating Characters
# Given a string s, return the LENGTH of the longest substring with no repeated
# characters. A substring must be contiguous.
# Example: s="zxyzxyz" -> 3   "xyz"
#          s="xxxx"    -> 1   "x"


# Case 1: Brute force: test every substring for duplicates
def length_of_longest_substring_brute(s):
    n = len(s)
    best = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            if s[j] in seen:
                break                  # duplicate: this start index cannot grow further
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best
# Time:  O(n^2)
# Space: O(min(n, alphabet))


# Case 2: Optimal: sliding window, shrink from the left on a duplicate
def length_of_longest_substring(s):
    window = set()                     # characters currently inside the window
    left = 0
    best = 0

    for right in range(len(s)):
        while s[right] in window:
            window.remove(s[left])     # shrink from the left until the clash is gone
            left += 1
        window.add(s[right])
        best = max(best, right - left + 1)
    return best
# Time:  O(n)   each character is added once and removed at most once
# Space: O(min(n, alphabet))


# Case 3: Optimal with a jump: store last index of each char and skip ahead
def length_of_longest_substring_jump(s):
    last_seen = {}                     # character -> the last index it appeared at
    left = 0
    best = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1     # jump past the previous copy in one step
        last_seen[char] = right
        best = max(best, right - left + 1)
    return best
# Time:  O(n)   no inner while loop at all
# Space: O(min(n, alphabet))


if __name__ == "__main__":
    cases = [
        ("zxyzxyz", 3),
        ("xxxx", 1),
        ("", 0),
        ("abcabcbb", 3),
        ("pwwkew", 3),                 # "wke", not the non-contiguous "pwke"
        ("dvdf", 3),                   # "vdf": the naive left++ reset gets this wrong
    ]
    for s, expected in cases:
        got = length_of_longest_substring(s)
        print(repr(s), "->", got, got == expected)

    print(length_of_longest_substring_brute("pwwkew"))   # 3
    print(length_of_longest_substring_jump("dvdf"))      # 3
