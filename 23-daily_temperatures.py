# Daily Temperatures
# For each day, return how many days you must wait for a WARMER temperature.
# If no warmer day ever comes, the answer for that day is 0.
# Example: temps=[30,38,30,36,35,40,28] -> [1,4,1,2,1,0,0]
#          temps=[22,21,20]             -> [0,0,0]


# Case 1: Brute force: for each day, scan forward for the first warmer day
def daily_temperatures_brute(temperatures):
    n = len(temperatures)
    result = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                result[i] = j - i      # distance to the first warmer day
                break
    return result
# Time:  O(n^2)
# Space: O(n)   for the output


# Case 2: Optimal: monotonic decreasing stack of days still waiting for an answer
def daily_temperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []                         # indices whose warmer day is not known yet

    for i, temp in enumerate(temperatures):
        # today is warmer than the days parked on the stack, so it answers them
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day
        stack.append(i)                # today now waits for ITS warmer day

    return result                      # days left on the stack keep their 0
# Time:  O(n)   each index is pushed once and popped at most once
# Space: O(n)   the stack
# The stack holds temperatures in decreasing order: anything warmer than a parked day
# would already have popped it, which is why one pass answers every day.


if __name__ == "__main__":
    cases = [
        ([30, 38, 30, 36, 35, 40, 28], [1, 4, 1, 2, 1, 0, 0]),
        ([22, 21, 20], [0, 0, 0]),
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([30], [0]),
        ([30, 30, 30], [0, 0, 0]),     # equal is NOT warmer
    ]
    for temps, expected in cases:
        got = daily_temperatures(temps)
        print(temps, "->", got, got == expected)

    print(daily_temperatures_brute([73, 74, 75, 71, 69, 72, 76, 73]))
