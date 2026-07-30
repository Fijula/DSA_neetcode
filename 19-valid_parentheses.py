# Valid Parentheses
# Given a string containing only ()[]{}, return True if every bracket is closed by the
# matching type, in the right order, and nothing is left unclosed.
# Example: s="[]"     -> True
#          s="([{}])" -> True
#          s="[(])"   -> False   closed in the wrong order


# Case 1: Brute force: repeatedly delete adjacent matching pairs
def is_valid_brute(s):
    while "()" in s or "[]" in s or "{}" in s:
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""                     # everything cancelled out -> valid
# Time:  O(n^2)   each pass rebuilds the whole string
# Space: O(n)


# Case 2: Optimal: a stack of the openers still waiting to be closed
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}   # closer -> its required opener
    stack = []

    for char in s:
        if char not in pairs:          # an opener: park it until its closer shows up
            stack.append(char)
            continue

        # a closer: the top of the stack must be its exact partner
        if not stack or stack.pop() != pairs[char]:
            return False

    return not stack                   # leftover openers were never closed
# Time:  O(n)   one pass, each character pushed/popped at most once
# Space: O(n)   worst case all openers, e.g. "((((("
# A stack is the right shape here because brackets close in LIFO order: the most
# recently opened bracket is always the one that must close next.


if __name__ == "__main__":
    cases = [
        ("[]", True),
        ("([{}])", True),
        ("[(])", False),
        ("", True),
        ("(", False),                  # unclosed opener
        (")", False),                  # closer with nothing open
        ("()[]{}", True),
        ("((", False),
    ]
    for s, expected in cases:
        got = is_valid(s)
        print(repr(s), "->", got, got == expected)

    print(is_valid_brute("([{}])"))    # True
    print(is_valid_brute("[(])"))      # False
