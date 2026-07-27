# Valid Sudoku
# Given a 9 x 9 Sudoku board, return True if it is valid:
#   1. each row    contains the digits 1-9 without duplicates
#   2. each column contains the digits 1-9 without duplicates
#   3. each 3 x 3 sub-box contains the digits 1-9 without duplicates
# Empty cells are "." and are always skipped.
# Note: the board does NOT need to be full or solvable to be valid.
# Example: the board below is valid -> True
#          change its first cell 5 -> 8 and it becomes    -> False


# Case 1: Brute force: three separate scans, one per rule
def is_valid_sudoku_brute(board):
    def no_duplicates(cells):
        digits = [c for c in cells if c != "."]   # ignore empty cells
        return len(digits) == len(set(digits))

    for r in range(9):                            # rule 1: every row
        if not no_duplicates(board[r]):
            return False

    for c in range(9):                            # rule 2: every column
        if not no_duplicates([board[r][c] for r in range(9)]):
            return False

    for box_r in range(0, 9, 3):                  # rule 3: every 3 x 3 box
        for box_c in range(0, 9, 3):
            box = [board[box_r + i][box_c + j] for i in range(3) for j in range(3)]
            if not no_duplicates(box):
                return False

    return True
# Time:  O(81) -> O(1)   the board size is fixed, but 3 passes over it
# Space: O(9)  -> O(1)   one small set at a time


# Case 2: Optimal: single pass, one set per row / column / box
from collections import defaultdict

def is_valid_sudoku(board):
    rows = defaultdict(set)                       # rows[r]  = digits seen in row r
    cols = defaultdict(set)                       # cols[c]  = digits seen in column c
    boxes = defaultdict(set)                      # boxes[(r//3, c//3)] = digits in that box

    for r in range(9):
        for c in range(9):
            digit = board[r][c]
            if digit == ".":                      # empty cell, nothing to check
                continue

            box = (r // 3, c // 3)                # which 3 x 3 box this cell belongs to
            if digit in rows[r] or digit in cols[c] or digit in boxes[box]:
                return False                      # duplicate found, stop early

            rows[r].add(digit)
            cols[c].add(digit)
            boxes[box].add(digit)

    return True
# Time:  O(81) -> O(1)   every cell visited exactly once
# Space: O(27 sets) -> O(1)


# Case 3: Short: tag every digit with its row / column / box, then look for repeats
def is_valid_sudoku_short(board):
    seen = [
        key
        for r in range(9)
        for c in range(9)
        if board[r][c] != "."
        for key in ((board[r][c], "row", r),      # same digit in the same row
                    (board[r][c], "col", c),      # same digit in the same column
                    (board[r][c], "box", r // 3, c // 3))
    ]
    return len(seen) == len(set(seen))            # any collision means invalid
# Time:  O(1), Space: O(1)   fixed 9 x 9 board


if __name__ == "__main__":
    valid_board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]

    # same board with the first cell changed 5 -> 8: now two 8s in the top-left box
    invalid_board = [row[:] for row in valid_board]
    invalid_board[0][0] = "8"

    print(is_valid_sudoku_brute(valid_board))     # True
    print(is_valid_sudoku_brute(invalid_board))   # False
    print(is_valid_sudoku(valid_board))           # True
    print(is_valid_sudoku(invalid_board))         # False
    print(is_valid_sudoku_short(valid_board))     # True
    print(is_valid_sudoku_short(invalid_board))   # False
