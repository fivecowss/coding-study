# week03_stack_binary_search/day04_search_2d_matrix.py


# ============================================================
# Problem: LeetCode 74. Search a 2D Matrix
# Pattern: Binary Search
#
# Key idea:
#   - Treat m x n matrix as a sorted 1D array.
#   - Convert 1D index mid into 2D index:
#       row = mid // n
#       col = mid % n
# ============================================================


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """
    Return True if target exists in matrix.
    Otherwise return False.

    Args:
        matrix: m x n sorted matrix
        target: integer to find

    Returns:
        True or False
    """

    # --------------------------------------------------------
    # Step 1. Get dimensions.
    # m = number of rows
    # n = number of columns
    # --------------------------------------------------------
    # TODO: define m and n
    m = len(matrix)
    n = len(matrix[0]
            )

    # --------------------------------------------------------
    # Step 2. Define search range over virtual 1D array.
    # The matrix has m * n total elements.
    # Valid 1D indices are from 0 to m*n - 1.
    # --------------------------------------------------------
    # TODO: set l and r
    l, r = 0, m * n - 1

    # --------------------------------------------------------
    # Step 3. Run binary search.
    # --------------------------------------------------------
    # TODO: while l <= r:
    while l <= r:

        # ----------------------------------------------------
        # Step 4. Compute middle 1D index.
        # ----------------------------------------------------
        mid = (l + r) // 2

        # ----------------------------------------------------
        # Step 5. Convert 1D index to 2D row/col.
        # ----------------------------------------------------
        # TODO: row = ...
        # TODO: col = ...
        row = mid // n
        col = mid % n

        # ----------------------------------------------------
        # Step 6. Read matrix value at converted position.
        # ----------------------------------------------------
        # TODO: value = matrix[row][col]
        value = matrix[row][col]

        # ----------------------------------------------------
        # Step 7. Compare value with target.
        # ----------------------------------------------------
        if value == target:
            return True
        elif value < target:
            l = mid + 1
        else:
            r = mid - 1
    # --------------------------------------------------------
    # Step 8. If loop ends, target does not exist.
    # --------------------------------------------------------
    return False


if __name__ == "__main__":
    matrix1 = [
        [1, 3, 5, 7],
        [10, 11, 16, 20],
        [23, 30, 34, 60],
    ]

    print(search_matrix(matrix1, 3))
    # Expected: True

    print(search_matrix(matrix1, 13))
    # Expected: False

    print(search_matrix([[1]], 1))
    # Expected: True