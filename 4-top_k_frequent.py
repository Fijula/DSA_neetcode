# Top K Frequent Elements
# Given an integer array nums and an integer k, return the k most frequent
# elements. The answer may be returned in any order.
# Example: nums=[1,1,1,2,2,3], k=2 -> [1,2]
#          nums=[1],           k=1 -> [1]


# Case 1: Brute force: count, then sort by frequency and take top k
def top_k_frequent_brute(nums, k):
    counts = {}
    for num in nums:
        counts[num] = counts.get(num, 0) + 1
    # sort the unique numbers by their count, highest first
    ordered = sorted(counts.keys(), key=lambda x: counts[x], reverse=True)
    return ordered[:k]             # first k after sorting
# Time:  O(n + m log m)   m = number of unique elements
# Space: O(m)


# Case 2: Optimal: min-heap of size -k 
import heapq

def top_k_frequent_heap(nums, k):
    counts = {}
    for num in nums:
        counts[num] = counts.get(num, 0) + 1

    heap = []                          
    for num, freq in counts.items():
        heapq.heappush(heap, (freq, num))   
        if len(heap) > k:
            heapq.heappop(heap)        

    return [num for freq, num in heap] 
# Time:  O(m log k)   m = unique elements
# Space: O(m + k)


# Case 3: Counter concepts single line
def top_k_frequent_short(nums, k):
    from collections import Counter
    return [num for num, _ in Counter(nums).most_common(k)] 
# Time: O(n log k), Space: O(n)


if __name__ == "__main__":
    print(top_k_frequent_brute([1, 1, 1, 2, 2, 3], 2))         
    print(top_k_frequent_heap([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2))    
    print(top_k_frequent_short([1], 1))                         # [1]
