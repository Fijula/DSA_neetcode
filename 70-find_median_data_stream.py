# Find Median from Data Stream
# Design a class where addNum(num) inserts a value and findMedian() returns the median
# of everything added so far. With an even count, the median is the average of the two
# middle values.
# Example: addNum(1) ; addNum(3) ; findMedian() -> 2.0 ; addNum(2) ; findMedian() -> 2.0


# Case 1: Naive: keep a sorted list
import bisect

class MedianFinderSorted:
    def __init__(self):
        self.nums = []

    def addNum(self, num):
        bisect.insort(self.nums, num)  # O(n): the insert shifts elements

    def findMedian(self):
        n = len(self.nums)
        mid = n // 2
        if n % 2:
            return float(self.nums[mid])
        return (self.nums[mid - 1] + self.nums[mid]) / 2
# addNum: O(n), findMedian: O(1)
# Space: O(n)


# Case 2: Optimal: two heaps splitting the data at the median
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []                # MAX-heap (negated) holding the LOWER half
        self.large = []                # MIN-heap holding the UPPER half

    def addNum(self, num):
        # always push to `small` first, then move its largest across
        heapq.heappush(self.small, -num)

        # keep the invariant: every value in small <= every value in large
        if self.small and self.large and (-self.small[0]) > self.large[0]:
            heapq.heappush(self.large, -heapq.heappop(self.small))

        # rebalance so the sizes never differ by more than 1
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.large) > len(self.small) + 1:
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        if len(self.large) > len(self.small):
            return float(self.large[0])
        # equal sizes: the median straddles both heap tops
        return (-self.small[0] + self.large[0]) / 2
# addNum: O(log n), findMedian: O(1)
# Space: O(n)
# The design idea: you never need the data sorted, only the two values adjacent to the
# middle. Two heaps expose exactly those in O(1) while keeping inserts logarithmic.


if __name__ == "__main__":
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(3)
    print(mf.findMedian(), mf.findMedian() == 2.0)
    mf.addNum(2)
    print(mf.findMedian(), mf.findMedian() == 2.0)

    mf2 = MedianFinder()
    expected = [1.0, 1.5, 2.0, 2.5, 3.0]
    got = []
    for num in [1, 2, 3, 4, 5]:
        mf2.addNum(num)
        got.append(mf2.findMedian())
    print(got, got == expected)

    # descending input exercises the rebalancing in the other direction
    mf3 = MedianFinder()
    got3 = []
    for num in [5, 4, 3, 2, 1]:
        mf3.addNum(num)
        got3.append(mf3.findMedian())
    print(got3, got3 == [5.0, 4.5, 4.0, 3.5, 3.0])

    mf4 = MedianFinder()
    mf4.addNum(-1)
    mf4.addNum(-2)
    print(mf4.findMedian(), mf4.findMedian() == -1.5)

    sorted_version = MedianFinderSorted()
    for num in [1, 3, 2]:
        sorted_version.addNum(num)
    print(sorted_version.findMedian())   # 2.0
