# K Closest Points to Origin
# Given points on a plane, return the k points closest to the origin (0,0).
# Distance is Euclidean, but comparing x^2 + y^2 is enough - the square root is a
# monotonic function, so it never changes the ordering.
# Example: points=[[0,2],[2,2]], k=1 -> [[0,2]]
#          points=[[1,3],[-2,2]], k=1 -> [[-2,2]]


# Case 1: Sort by distance and take the first k
def k_closest_sort(points, k):
    return sorted(points, key=lambda p: p[0] ** 2 + p[1] ** 2)[:k]
# Time:  O(n log n)
# Space: O(n)


# Case 2: Optimal for small k: a MAX-heap capped at k
import heapq

def k_closest(points, k):
    heap = []                          # holds (-distance, x, y): a max-heap by distance

    for x, y in points:
        distance = x * x + y * y       # no sqrt needed
        heapq.heappush(heap, (-distance, x, y))
        if len(heap) > k:
            heapq.heappop(heap)        # evict the FARTHEST point seen so far

    return [[x, y] for _, x, y in heap]
# Time:  O(n log k)   better than sorting when k is much smaller than n
# Space: O(k)
# Mirror of problem 64: to keep the k SMALLEST distances you evict from a max-heap.


# Case 3: Min-heap of everything, popping k times
def k_closest_min_heap(points, k):
    heap = [(x * x + y * y, x, y) for x, y in points]
    heapq.heapify(heap)                # O(n)
    return [[x, y] for _, x, y in (heapq.heappop(heap) for _ in range(k))]
# Time:  O(n + k log n)
# Space: O(n)


if __name__ == "__main__":
    def normalise(points):
        """Sort so results can be compared regardless of internal heap order."""
        return sorted(tuple(p) for p in points)

    cases = [
        ([[0, 2], [2, 2]], 1, [[0, 2]]),
        ([[1, 3], [-2, 2]], 1, [[-2, 2]]),
        ([[3, 3], [5, -1], [-2, 4]], 2, [[3, 3], [-2, 4]]),
        ([[1, 1]], 1, [[1, 1]]),
        ([[0, 0], [1, 1], [2, 2]], 3, [[0, 0], [1, 1], [2, 2]]),   # k = n
        ([[1, 0], [-1, 0]], 1, None),   # a tie: either answer is acceptable
    ]
    for points, k, expected in cases:
        got = k_closest(points, k)
        ok = len(got) == k if expected is None else normalise(got) == normalise(expected)
        print(points, k, "->", got, ok)

    print(k_closest_sort([[3, 3], [5, -1], [-2, 4]], 2))        # [[3,3],[-2,4]]
    print(k_closest_min_heap([[3, 3], [5, -1], [-2, 4]], 2))    # [[3,3],[-2,4]]
