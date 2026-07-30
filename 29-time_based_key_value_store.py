# Time Based Key-Value Store
# Design a store where set(key, value, timestamp) records a value, and
# get(key, timestamp) returns the value set at the LARGEST timestamp <= the one asked
# for, or "" if none exists. Timestamps for a key arrive strictly increasing.
# Example: set("a","one",1) ; set("a","two",3)
#          get("a",1) -> "one" ; get("a",2) -> "one" ; get("a",3) -> "two"
#          get("a",0) -> ""


# Case 1: Naive: scan a key's history backwards for the first valid timestamp
class TimeMapNaive:
    def __init__(self):
        self.store = {}                # key -> list of (timestamp, value)

    def set(self, key, value, timestamp):
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key, timestamp):
        for time, value in reversed(self.store.get(key, [])):
            if time <= timestamp:
                return value
        return ""
# set: O(1), get: O(n)
# Space: O(n)


# Case 2: Optimal: binary search over the timestamp list
class TimeMap:
    def __init__(self):
        self.store = {}                # key -> list of [timestamp, value]

    def set(self, key, value, timestamp):
        # timestamps arrive increasing, so appending keeps each list sorted for free
        self.store.setdefault(key, []).append([timestamp, value])

    def get(self, key, timestamp):
        history = self.store.get(key, [])
        result = ""

        left, right = 0, len(history) - 1
        while left <= right:
            mid = (left + right) // 2
            if history[mid][0] <= timestamp:
                result = history[mid][1]   # valid candidate, but a later one may exist
                left = mid + 1             # so keep searching to the RIGHT
            else:
                right = mid - 1            # too new, discard this half
        return result
# set: O(1), get: O(log n)
# Space: O(n)
# This is binary search for an UPPER BOUND rather than an exact match: instead of
# returning on a hit, remember the best candidate so far and keep pushing right.


# Case 3: Same, using the standard library's bisect
from bisect import bisect_right

class TimeMapBisect:
    def __init__(self):
        self.times = {}                # key -> sorted list of timestamps
        self.values = {}               # key -> values, parallel to self.times

    def set(self, key, value, timestamp):
        self.times.setdefault(key, []).append(timestamp)
        self.values.setdefault(key, []).append(value)

    def get(self, key, timestamp):
        if key not in self.times:
            return ""
        # bisect_right gives the insert position, so i-1 is the last time <= timestamp
        i = bisect_right(self.times[key], timestamp)
        return self.values[key][i - 1] if i else ""
# set: O(1), get: O(log n)


if __name__ == "__main__":
    tm = TimeMap()
    tm.set("a", "one", 1)
    tm.set("a", "two", 3)
    print(tm.get("a", 1), tm.get("a", 1) == "one")
    print(tm.get("a", 2), tm.get("a", 2) == "one")   # falls back to timestamp 1
    print(tm.get("a", 3), tm.get("a", 3) == "two")
    print(repr(tm.get("a", 0)), tm.get("a", 0) == "")   # nothing set that early
    print(repr(tm.get("z", 5)), tm.get("z", 5) == "")   # unknown key

    tm2 = TimeMap()
    for i in range(1, 6):
        tm2.set("k", f"v{i}", i * 10)
    print(tm2.get("k", 35), tm2.get("k", 35) == "v3")   # 30 <= 35 < 40
    print(tm2.get("k", 100), tm2.get("k", 100) == "v5")

    naive = TimeMapNaive()
    naive.set("a", "one", 1)
    print(naive.get("a", 2))           # one

    bis = TimeMapBisect()
    bis.set("a", "one", 1)
    bis.set("a", "two", 3)
    print(bis.get("a", 2), repr(bis.get("a", 0)))   # one ''
