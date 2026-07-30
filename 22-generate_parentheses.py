# Generate Parentheses
# Given n, return every combination of n pairs of parentheses that is well formed.
# Example: n=1 -> ["()"]
#          n=3 -> ["((()))","(()())","(())()","()(())","()()()"]


# Case 1: Brute force: build every string of length 2n, keep the valid ones
def generate_parenthesis_brute(n):
    def is_valid(s):
        depth = 0
        for char in s:
            depth += 1 if char == "(" else -1
            if depth < 0:              # a ")" arrived with nothing open
                return False
        return depth == 0

    result = []

    def build(current):
        if len(current) == 2 * n:
            if is_valid(current):
                result.append(current)
            return
        build(current + "(")
        build(current + ")")

    build("")
    return result
# Time:  O(2^(2n) * n)   every string generated, then validated
# Space: O(n) recursion depth


# Case 2: Optimal: backtracking that only ever builds VALID prefixes
def generate_parenthesis(n):
    result = []
    stack = []                         # the string being built, as a list of chars

    def backtrack(open_count, close_count):
        if len(stack) == 2 * n:        # used all n pairs
            result.append("".join(stack))
            return

        if open_count < n:             # room left to open another pair
            stack.append("(")
            backtrack(open_count + 1, close_count)
            stack.pop()                # undo: this is the "backtrack" step

        if close_count < open_count:   # only close what is actually open
            stack.append(")")
            backtrack(open_count, close_count + 1)
            stack.pop()

    backtrack(0, 0)
    return result
# Time:  O(4^n / sqrt(n))   the nth Catalan number of results, each built in O(n)
# Space: O(n)   recursion depth plus the working stack
# The two conditions are the whole algorithm: `open < n` bounds the size, and
# `close < open` guarantees we never produce an invalid string in the first place,
# so no validity check is needed at the end.


if __name__ == "__main__":
    cases = [
        (1, ["()"]),
        (2, ["(())", "()()"]),
        (3, ["((()))", "(()())", "(())()", "()(())", "()()()"]),
    ]
    for n, expected in cases:
        got = generate_parenthesis(n)
        print(n, "->", got, got == expected)

    # count only: n=4 should give the 4th Catalan number, 14
    print(len(generate_parenthesis(4)), len(generate_parenthesis(4)) == 14)
    print(generate_parenthesis_brute(2))   # ['(())', '()()']
