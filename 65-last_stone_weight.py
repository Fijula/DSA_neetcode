# Last Stone Weight
# Repeatedly smash the two HEAVIEST stones together. If they are equal both shatter; if
# not, the heavier one is left with the weight difference. Return the weight of the last
# remaining stone, or 0 if none remain.
# Example: stones=[2,3,6,2,4] -> 1
#          stones=[1,2]       -> 1


# Case 1: Naive: sort the list again after every smash
def last_stone_weight_sort(stones):
    stones = sorted(stones)
    while len(stones) > 1:
        heaviest = stones.pop()        # the two biggest are at the end
        second = stones.pop()
        if heaviest != second:
            stones.append(heaviest - second)
            stones.sort()              # re-sort so the invariant holds again
    return stones[0] if stones else 0
# Time:  O(n^2 log n)   a sort per smash
# Space: O(n)


# Case 2: Optimal: a MAX-heap, faked with negated values
import heapq

def last_stone_weight(stones):
    # Python only has a min-heap, so store negatives: the "smallest" negative is the
    # largest real weight
    heap = [-stone for stone in stones]
    heapq.heapify(heap)                # O(n)

    while len(heap) > 1:
        heaviest = -heapq.heappop(heap)
        second = -heapq.heappop(heap)

        if heaviest > second:
            heapq.heappush(heap, -(heaviest - second))   # the remainder goes back in
        # equal weights: both are destroyed, nothing is pushed

    return -heap[0] if heap else 0
# Time:  O(n log n)   each stone is pushed/popped a constant number of times
# Space: O(n)
# Negating on the way in and out is the standard Python max-heap idiom - worth
# recognising instantly, since heapq has no reverse option.


if __name__ == "__main__":
    cases = [
        ([2, 3, 6, 2, 4], 1),
        ([1, 2], 1),
        ([2, 7, 4, 1, 8, 1], 1),
        ([1], 1),                      # a single stone survives untouched
        ([2, 2], 0),                   # equal stones annihilate
        ([], 0),
        ([10, 4, 2, 10], 2),
        ([3, 3, 3], 3),
    ]
    for stones, expected in cases:
        got = last_stone_weight(list(stones))
        print(stones, "->", got, got == expected)

    print(last_stone_weight_sort([2, 7, 4, 1, 8, 1]))   # 1
    print(last_stone_weight_sort([2, 2]))               # 0
