# Valid Palindrome
# Given a string s, return True if it is a palindrome, ignoring every
# non-alphanumeric character and treating uppercase and lowercase as the same.
# Example: s="Was it a car or a cat I saw?" -> True
#          s="tab a cat"                    -> False


# Case 1: Clean the string, then compare it with its own reverse
def is_palindrome_clean(s):
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
# Time:  O(n)
# Space: O(n)   the cleaned copy plus its reverse


# Case 2: Optimal: two pointers walking inward, no extra string
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1                  # skip junk from the left
        while left < right and not s[right].isalnum():
            right -= 1                 # skip junk from the right

        if s[left].lower() != s[right].lower():
            return False               # a real mismatch: not a palindrome
        left += 1
        right -= 1
    return True
# Time:  O(n)   each pointer moves at most n steps in total
# Space: O(1)   nothing allocated


# Case 3: Short: same clean-and-reverse idea on a list of characters
def is_palindrome_short(s):
    cleaned = [c for c in s.lower() if c.isalnum()]
    return cleaned == cleaned[::-1]
# Time: O(n), Space: O(n)


if __name__ == "__main__":
    cases = [
        ("Was it a car or a cat I saw?", True),
        ("tab a cat", False),
        ("", True),                    # empty string counts as a palindrome
        (".,", True),                  # nothing left after cleaning
        ("0P", False),                 # digit vs letter: lower() must not equate them
        ("A man, a plan, a canal: Panama", True),
    ]
    for s, expected in cases:
        got = is_palindrome(s)
        print(repr(s), "->", got, got == expected)

    print(is_palindrome_clean("Was it a car or a cat I saw?"))   # True
    print(is_palindrome_short("tab a cat"))                      # False
