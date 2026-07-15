# Contains Duplicate
# Given an integer array nums, return True if any value appears at least twice,
# and False if every element is distinct.


# Case 1: Brute force: compare every pair
def contains_duplicate_brute(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
# Time:  O(n^2) 
# Space: O(1)   


# Case 2: Optimal: hash set 
def contains_duplicate_optimal(nums):
    seen = set()               # like new HashSet<>() in Java
    for num in nums:
        if num in seen:        # O(1) average membership check
            return True
        seen.add(num)
    return False
# Time:  O(n)    
# Space: O(n)   

# Case 3: set concepts single line
def contains_duplicate_short(nums):
    return len(set(nums)) != len(nums)
# Time: O(n), Space: O(n)



if __name__ == "__main__":
    print(contains_duplicate_brute([1, 2, 3, 1]))    # True
    print(contains_duplicate_optimal([1, 2, 3, 4]))  # False
    print(contains_duplicate_short([1, 1, 1, 3, 3]))  # True
