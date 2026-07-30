# Search a 2D Matrix
# An m x n matrix where each row is sorted ascending AND the first value of a row is
# greater than the last value of the row above it. Return True if target is present.
# Example: matrix=[[1,2,4,8],[10,11,12,13],[14,20,30,40]], target=10 -> True
#                                                          target=15 -> False


# Case 1: Brute force: look at every cell
def search_matrix_brute(matrix, target):
    for row in matrix:
        for value in row:
            if value == target:
                return True
    return False
# Time:  O(m * n)
# Space: O(1)


# Case 2: Two binary searches: find the row, then search inside it
def search_matrix_two_pass(matrix, target):
    if not matrix or not matrix[0]:
        return False

    top, bottom = 0, len(matrix) - 1
    while top <= bottom:               # first search: which row COULD hold target
        mid = (top + bottom) // 2
        if target < matrix[mid][0]:
            bottom = mid - 1
        elif target > matrix[mid][-1]:
            top = mid + 1
        else:
            break                      # target is within this row's range
    else:
        return False                   # loop ended without breaking: no candidate row

    row = matrix[mid]
    left, right = 0, len(row) - 1
    while left <= right:               # second search: inside that one row
        mid_col = (left + right) // 2
        if row[mid_col] == target:
            return True
        if row[mid_col] < target:
            left = mid_col + 1
        else:
            right = mid_col - 1
    return False
# Time:  O(log m + log n)
# Space: O(1)


# Case 3: Optimal: treat the matrix as ONE sorted array of length m*n
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1

    while left <= right:
        mid = (left + right) // 2
        # unflatten the 1D index back into (row, column)
        value = matrix[mid // cols][mid % cols]

        if value == target:
            return True
        if value < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
# Time:  O(log(m * n))   which equals O(log m + log n)
# Space: O(1)
# The row-ordering guarantee is what lets us pretend the whole grid is one sorted
# array: reading it row by row produces a single ascending sequence.


if __name__ == "__main__":
    matrix = [[1, 2, 4, 8], [10, 11, 12, 13], [14, 20, 30, 40]]
    cases = [
        (matrix, 10, True),
        (matrix, 15, False),
        (matrix, 1, True),             # first cell
        (matrix, 40, True),            # last cell
        (matrix, 0, False),            # below the range
        (matrix, 99, False),           # above the range
        ([], 1, False),
        ([[1]], 1, True),
    ]
    for mat, target, expected in cases:
        got = search_matrix(mat, target)
        print(target, "->", got, got == expected)

    print(search_matrix_brute(matrix, 12))      # True
    print(search_matrix_two_pass(matrix, 15))   # False
    print(search_matrix_two_pass(matrix, 20))   # True
