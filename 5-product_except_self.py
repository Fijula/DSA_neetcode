# Products of Array Except Self
# Given an integer array nums, return an array output where output[i] is the
# product of all the elements of nums except nums[i].
# Example: nums=[1,2,4,6]     -> [48,24,12,8]
#          nums=[-1,0,1,2,3]  -> [0,-6,0,0,0]


# Case 1: Brute force: for each index, multiply every other element
def product_except_self_brute(nums):
    n = len(nums)
    output = []
    for i in range(n):
        product = 1
        for j in range(n):
            if j != i:                 # skip the element at index i itself
                product *= nums[j]
        output.append(product)
    return output
# Time:  O(n^2)
# Space: O(n)   for the output


# Case 2: Division: total product / nums[i]  (breaks on zeros, so count them)
def product_except_self_division(nums):
    total = 1
    zeros = 0
    for num in nums:
        if num == 0:
            zeros += 1
        else:
            total *= num               # product of the non-zero elements

    if zeros > 1:                      # two zeros -> every product has a zero
        return [0] * len(nums)
    if zeros == 1:                     # only the zero's own slot survives
        return [total if num == 0 else 0 for num in nums]
    return [total // num for num in nums]
# Time:  O(n)
# Space: O(n)
# Note: uses division, so it does not satisfy the follow-up.


# Case 3: Two arrays: store every left product and every right product, no division
def product_except_self_two_arrays(nums):
    n = len(nums)
    left = [1] * n                     # left[i]  = product of nums[0 .. i-1]
    right = [1] * n                    # right[i] = product of nums[i+1 .. n-1]

    for i in range(1, n):              # left[0] stays 1: nothing to the left
        left[i] = left[i - 1] * nums[i - 1]

    for i in range(n - 2, -1, -1):     # right[n-1] stays 1: nothing to the right
        right[i] = right[i + 1] * nums[i + 1]

    return [left[i] * right[i] for i in range(n)]
# Time:  O(n)   three passes
# Space: O(n)   two helper arrays
# Note: same idea as Case 4, just written out explicitly instead of rolling scalars.


# Case 4: Optimal: prefix and suffix products, no division
def product_except_self(nums):
    n = len(nums)
    output = [1] * n

    prefix = 1                         # product of everything left of i
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]

    suffix = 1                         # product of everything right of i
    for i in range(n - 1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]

    return output
# Time:  O(n)   two passes
# Space: O(1)   extra, ignoring the output array


if __name__ == "__main__":
    print(product_except_self_brute([1, 2, 4, 6]))        # [48, 24, 12, 8]
    print(product_except_self_division([-1, 0, 1, 2, 3]))  # [0, -6, 0, 0, 0]
    print(product_except_self([1, 2, 4, 6]))              # [48, 24, 12, 8]
    print(product_except_self([-1, 0, 1, 2, 3]))          # [0, -6, 0, 0, 0]
