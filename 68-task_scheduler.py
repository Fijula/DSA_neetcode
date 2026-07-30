# Task Scheduler
# tasks is a list of task types (characters). Each task takes one CPU interval, and two
# tasks of the SAME type must be separated by at least n intervals. The CPU may idle.
# Return the minimum number of intervals needed to finish everything.
# Example: tasks=["X","X","Y","Y"], n=2 -> 5   X Y idle X Y
#          tasks=["A","A","A","B","C"], n=3 -> 7   A B C idle A idle idle A


# Case 1: Simulation with a max-heap and a cooldown queue
from collections import Counter, deque
import heapq

def least_interval_simulation(tasks, n):
    counts = Counter(tasks)
    heap = [-count for count in counts.values()]   # max-heap: most frequent first
    heapq.heapify(heap)

    time = 0
    cooling = deque()                  # (remaining_count, time it becomes available)

    while heap or cooling:
        time += 1

        if heap:
            remaining = heapq.heappop(heap) + 1    # run it once (values are negative)
            if remaining:
                cooling.append((remaining, time + n))   # still has copies left
        # else: nothing runnable, so this interval is an idle one

        # anything whose cooldown has expired returns to the heap
        if cooling and cooling[0][1] == time:
            heapq.heappush(heap, cooling.popleft()[0])

    return time
# Time:  O(total intervals * log 26) -> effectively O(total intervals)
# Space: O(26)
# Greedy choice: always run the task with the most copies left, which keeps the
# frequent tasks spread out and minimises forced idling.


# Case 2: Optimal: compute the answer directly from the frequency counts
def least_interval(tasks, n):
    if not tasks:
        return 0

    counts = Counter(tasks)
    max_count = max(counts.values())
    # how many task types share that peak frequency
    max_count_tasks = sum(1 for c in counts.values() if c == max_count)

    # Lay the most frequent task out as (max_count - 1) blocks of size (n + 1),
    # then append one final row holding every task tied at the peak.
    slots = (max_count - 1) * (n + 1) + max_count_tasks

    # If there are enough OTHER tasks, they fill every idle slot and nothing is wasted,
    # in which case the answer is simply the number of tasks.
    return max(slots, len(tasks))
# Time:  O(n)   one counting pass
# Space: O(26)
# The formula is a counting argument, not a simulation: the schedule's length is
# dictated entirely by the most frequent task, unless there is so much other work
# that the idle gaps get filled anyway.


if __name__ == "__main__":
    cases = [
        (["X", "X", "Y", "Y"], 2, 5),
        (["A", "A", "A", "B", "C"], 3, 7),
        (["A", "A", "A", "B", "B", "B"], 2, 8),
        (["A", "A", "A", "B", "B", "B"], 0, 6),      # no cooldown: no idling
        (["A"], 5, 1),
        ([], 2, 0),
        (["A", "B", "C", "D", "E", "A", "B", "C", "D", "E"], 4, 10),
        (["A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2, 10),
    ]
    for tasks, n, expected in cases:
        got = least_interval(tasks, n)
        print(tasks, n, "->", got, got == expected)

    print(least_interval_simulation(["A", "A", "A", "B", "C"], 3))          # 7
    print(least_interval_simulation(["A", "A", "A", "B", "B", "B"], 2))     # 8
