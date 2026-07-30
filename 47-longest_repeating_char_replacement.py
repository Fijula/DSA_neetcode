# Longest Repeating Character Replacement
# You may replace up to k characters of s with any uppercase letter. Return the length
# of the longest substring that can be made of ONE repeated character.
# Example: s="XYYX",   k=2 -> 4   replace both X, or both Y
#          s="AAABABB", k=1 -> 5   "AAABA" -> "AAAAA"


# Case 1: Brute force: check every substring
def character_replacement_brute(s, k):
    from collections import Counter

    n = len(s)
    best = 0
    for i in range(n):
        for j in range(i, n):
            window = s[i:j + 1]
            counts = Counter(window)
            # keep the most common letter, replace all the others
            replacements = len(window) - max(counts.values())
            if replacements <= k:
                best = max(best, len(window))
    return best
# Time:  O(n^3)
# Space: O(alphabet)


# Case 2: Sliding window, recomputing the majority count each step
def character_replacement_recount(s, k):
    counts = {}
    left = 0
    best = 0

    for right in range(len(s)):
        counts[s[right]] = counts.get(s[right], 0) + 1

        # shrink while the window needs more replacements than we are allowed
        while (right - left + 1) - max(counts.values()) > k:
            counts[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)
    return best
# Time:  O(n * alphabet)   max() rescans the counts on every step
# Space: O(alphabet)


# Case 3: Optimal: track the best count seen so far, never decrease it
def character_replacement(s, k):
    counts = {}
    left = 0
    max_count = 0                      # highest single-letter count seen in ANY window
    best = 0

    for right in range(len(s)):
        counts[s[right]] = counts.get(s[right], 0) + 1
        max_count = max(max_count, counts[s[right]])

        # window is invalid: too many characters would need replacing
        if (right - left + 1) - max_count > k:
            counts[s[left]] -= 1
            left += 1                  # slide, keeping the window size the same

        best = max(best, right - left + 1)
    return best
# Time:  O(n)   no inner loop, no rescan of the counts
# Space: O(alphabet)
# The surprising part: max_count is never decreased even when the window shrinks, so
# it can go "stale". That is harmless - a stale max_count only ever understates how
# many replacements are needed, and the answer can only grow when a genuinely better
# max_count appears, so `best` is never overstated.


if __name__ == "__main__":
    cases = [
        ("XYYX", 2, 4),
        ("AAABABB", 1, 5),
        ("ABAB", 2, 4),
        ("AABABBA", 1, 4),
        ("A", 0, 1),
        ("", 2, 0),
        ("ABCDE", 0, 1),               # no replacements allowed
        ("AAAA", 0, 4),
    ]
    for s, k, expected in cases:
        got = character_replacement(s, k)
        print(repr(s), k, "->", got, got == expected)

    print(character_replacement_brute("AABABBA", 1))     # 4
    print(character_replacement_recount("AAABABB", 1))   # 5
