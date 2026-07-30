# Min Stack
# Design a stack supporting push, pop, top and getMin - all in O(1) time.
# Example: push(1), push(2), push(0)
#          getMin() -> 0 ; pop() ; getMin() -> 1 ; top() -> 2


# Case 1: Naive: scan the whole stack for the minimum
class MinStackNaive:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return min(self.stack)         # O(n): rescans everything on every call
# push/pop/top: O(1), getMin: O(n)
# Space: O(n)


# Case 2: Optimal: a parallel stack holding the minimum "as of" each depth
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []            # min_stack[i] = min of stack[0 .. i]

    def push(self, val):
        self.stack.append(val)
        # the new minimum is either val itself or the previous minimum
        smallest = val if not self.min_stack else min(val, self.min_stack[-1])
        self.min_stack.append(smallest)

    def pop(self):
        self.min_stack.pop()           # keep the two stacks the same height
        return self.stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]      # O(1): already computed at push time
# All four operations: O(1)
# Space: O(n)   one extra entry per element
# Why the duplicate minima are worth storing: popping must restore the minimum that
# was valid BEFORE the pushed element, and only a per-depth record can do that.


if __name__ == "__main__":
    st = MinStack()
    st.push(1)
    st.push(2)
    st.push(0)
    print(st.getMin(), st.getMin() == 0)   # 0
    st.pop()
    print(st.getMin(), st.getMin() == 1)   # 1
    print(st.top(), st.top() == 2)         # 2

    # a descending push order, so every push lowers the minimum
    st2 = MinStack()
    for val in [5, 4, 3, 2, 1]:
        st2.push(val)
    print(st2.getMin(), st2.getMin() == 1)     # 1
    for _ in range(4):
        st2.pop()
    print(st2.getMin(), st2.getMin() == 5)     # 5, restored correctly

    naive = MinStackNaive()
    for val in [3, 1, 2]:
        naive.push(val)
    print(naive.getMin(), naive.top())         # 1 2
