# week03_stack_binary_search/day04_binary_search.py


# ============================================================
# Problem: LeetCode 704. Binary Search
# Pattern: Binary Search
#
# Key idea:
#   - nums is sorted.
#   - Maintain search range [l, r].
#   - Compare nums[mid] with target.
#   - Remove the impossible half.
# ============================================================


def binary_search(nums: list[int], target: int) -> int:
    """
    Return the index of target if target exists in nums.
    Otherwise return -1.

    Args:
        nums: sorted list of integers
        target: integer to find

    Returns:
        index of target, or -1
    """

    # --------------------------------------------------------
    # Step 1. Initialize left and right boundary.
    # Search range is nums[l:r+1].
    # --------------------------------------------------------
    # TODO: set l and r
    l, r = 0, len(nums) - 1

    # --------------------------------------------------------
    # Step 2. Continue while search range is non-empty.
    # l <= r means there is at least one candidate index.
    # --------------------------------------------------------
    # TODO: while l <= r:
    while l <= r:

        # ----------------------------------------------------
        # Step 3. Choose middle index.
        # ----------------------------------------------------
        # TODO: compute mid
        mid = (l + r) // 2

        # ----------------------------------------------------
        # Step 4. If nums[mid] is target, return mid.
        # ----------------------------------------------------
        if nums[mid] == target:
            return mid

        # ----------------------------------------------------
        # Step 5. If nums[mid] is smaller than target,
        # target must be on the right half.
        # ----------------------------------------------------
        elif nums[mid] < target:
            l = mid + 1

        # ----------------------------------------------------
        # Step 6. If nums[mid] is greater than target,
        # target must be on the left half.
        # ----------------------------------------------------
        else:
            r = mid - 1

    # --------------------------------------------------------
    # Step 7. If loop ends, target does not exist.
    # --------------------------------------------------------
    return -1


if __name__ == "__main__":
    print(binary_search([-1, 0, 3, 5, 9, 12], 9))
    # Expected: 4

    print(binary_search([-1, 0, 3, 5, 9, 12], 2))
    # Expected: -1

    print(binary_search([5], 5))
    # Expected: 0