# Permutation in String
# Given strings s1 and s2, return True if s2 contains a permutation of s1 as a
# substring - i.e. some window of s2 uses exactly the same letters as s1.
# Example: s1="abc", s2="lecabee" -> True   the window "cab"
#          s1="abc", s2="lecaabee" -> False


# Case 1: Brute force: sort s1, then sort every window of the same length
def check_inclusion_brute(s1, s2):
    n, m = len(s1), len(s2)
    target = sorted(s1)
    for i in range(m - n + 1):
        if sorted(s2[i:i + n]) == target:
            return True
    return False
# Time:  O(m * n log n)   a sort per window
# Space: O(n)


# Case 2: Counter per window: compare letter counts instead of sorting
from collections import Counter

def check_inclusion_counter(s1, s2):
    n, m = len(s1), len(s2)
    if n > m:
        return False

    need = Counter(s1)
    for i in range(m - n + 1):
        if Counter(s2[i:i + n]) == need:
            return True
    return False
# Time:  O(m * n)   rebuilds the whole count for every window
# Space: O(alphabet)


# Case 3: Optimal: fixed-size sliding window, counts updated in O(1) per step
def check_inclusion(s1, s2):
    n, m = len(s1), len(s2)
    if n > m:
        return False

    need = Counter(s1)
    window = Counter(s2[:n])           # the first window, built once
    if window == need:
        return True

    for right in range(n, m):
        window[s2[right]] += 1         # slide in the new character
        left_char = s2[right - n]
        window[left_char] -= 1         # slide out the one that fell off the left
        if window[left_char] == 0:
            del window[left_char]      # drop zeros so == compares cleanly

        if window == need:
            return True
    return False
# Time:  O(m)   the window slides once, each step is constant work
# Space: O(alphabet)
# The window size never changes - it is always len(s1) - which is what makes the
# add-one / remove-one update valid.


if __name__ == "__main__":
    cases = [
        ("abc", "lecabee", True),
        ("abc", "lecaabee", False),
        ("ab", "eidbaooo", True),
        ("ab", "eidboaoo", False),
        ("adc", "dcda", True),
        ("abc", "ab", False),          # s1 longer than s2
        ("a", "a", True),
    ]
    for s1, s2, expected in cases:
        got = check_inclusion(s1, s2)
        print(repr(s1), repr(s2), "->", got, got == expected)

    print(check_inclusion_brute("abc", "lecabee"))     # True
    print(check_inclusion_counter("ab", "eidboaoo"))   # False
