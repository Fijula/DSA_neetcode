# Kth Largest Element in a Stream
# Design a class initialised with k and a starting list. Each add(val) inserts a value
# and returns the kth LARGEST value seen so far.
# Example: k=3, nums=[1,2,3,3] ; add(3) -> 3 ; add(5) -> 3 ; add(6) -> 5 ; add(7) -> 6
#          k=1, nums=[]        ; add(2) -> 2 ; add(1) -> 2


# Case 1: Naive: keep everything sorted and index in
class KthLargestSorted:
    def __init__(self, k, nums):
        self.k = k
        self.nums = sorted(nums)

    def add(self, val):
        # insert into the sorted list, then read the kth from the end
        self.nums.append(val)
        self.nums.sort()
        return self.nums[-self.k]
# add: O(n log n) per call
# Space: O(n)


# Case 2: Optimal: a MIN-heap capped at exactly k elements
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = list(nums)
        heapq.heapify(self.heap)       # O(n), cheaper than k separate pushes

        # discard everything below the top k: they can never be the kth largest
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)   # evict the smallest, keeping the k largest
        return self.heap[0]            # the heap's minimum IS the kth largest
# __init__: O(n), add: O(log k)
# Space: O(k)
# The counterintuitive part: to track the kth LARGEST you keep a MIN-heap. Its root is
# the smallest of the k biggest values, which is exactly the kth largest overall.


if __name__ == "__main__":
    kth = KthLargest(3, [1, 2, 3, 3])
    results = [kth.add(3), kth.add(5), kth.add(6), kth.add(7), kth.add(8)]
    print(results, results == [3, 3, 5, 6, 7])

    k1 = KthLargest(1, [])
    r1 = [k1.add(2), k1.add(1), k1.add(5)]
    print(r1, r1 == [2, 2, 5])         # k=1 tracks the running maximum

    k2 = KthLargest(2, [0])
    r2 = [k2.add(-1), k2.add(1), k2.add(-2), k2.add(-4), k2.add(3)]
    print(r2, r2 == [0, 0, 0, 0, 1])   # negatives handled the same way

    k3 = KthLargest(4, [7, 7, 7, 7, 8, 3])
    print(k3.add(2), k3.add(10))       # 7 7

    sorted_version = KthLargestSorted(3, [1, 2, 3, 3])
    print([sorted_version.add(3), sorted_version.add(5), sorted_version.add(6)])
    # [3, 3, 5]
