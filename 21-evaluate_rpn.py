# Evaluate Reverse Polish Notation
# Evaluate an arithmetic expression in postfix form: operators come AFTER their two
# operands. Valid operators are + - * /, and division truncates toward zero.
# Example: tokens=["1","2","+","3","*"]  -> 9    (1+2)*3
#          tokens=["4","13","5","/","+"] -> 6    4 + (13/5) = 4 + 2


# Case 1: Optimal (and the only sensible way): a stack of operands
def eval_rpn(tokens):
    stack = []

    for token in tokens:
        if token not in ("+", "-", "*", "/"):
            stack.append(int(token))   # a number: park it
            continue

        # an operator: its operands are the two most recent numbers.
        # order matters - the SECOND pop is the left-hand side
        right = stack.pop()
        left = stack.pop()

        if token == "+":
            stack.append(left + right)
        elif token == "-":
            stack.append(left - right)
        elif token == "*":
            stack.append(left * right)
        else:
            # Python's // floors (-7//2 == -4), the problem wants truncation (-3)
            stack.append(int(left / right))

    return stack[0]                    # exactly one value is left: the answer
# Time:  O(n)   one pass over the tokens
# Space: O(n)   the stack of pending operands


# Case 2: Same idea, operators looked up in a dict of lambdas
import operator

def eval_rpn_dict(tokens):
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": lambda a, b: int(a / b),  # truncate toward zero, not floor
    }
    stack = []
    for token in tokens:
        if token in ops:
            right, left = stack.pop(), stack.pop()
            stack.append(ops[token](left, right))
        else:
            stack.append(int(token))
    return stack[0]
# Time: O(n), Space: O(n)


if __name__ == "__main__":
    cases = [
        (["1", "2", "+", "3", "*"], 9),
        (["4", "13", "5", "/", "+"], 6),
        (["2", "1", "+", "3", "*"], 9),
        (["-7", "2", "/"], -3),        # truncation, NOT floor division (-4)
        (["5"], 5),
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
    ]
    for tokens, expected in cases:
        got = eval_rpn(tokens)
        print(tokens, "->", got, got == expected)

    print(eval_rpn_dict(["-7", "2", "/"]))   # -3
