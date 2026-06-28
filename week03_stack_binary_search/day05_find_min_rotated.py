# ============================================================
# Problem: LeetCode 153. Find Minimum in Rotated Sorted Array
# Pattern: Rotated Binary Search / Boundary Search
#
# Key idea:
#   - nums is sorted but rotated.
#   - Compare nums[mid] with nums[r].
#   - If nums[mid] > nums[r], minimum is on the right side.
#   - Otherwise, minimum is at mid or on the left side.
# ============================================================


def find_min(nums: list[int]) -> int:
    """
    Return the minimum value in a rotated sorted array.

    Args:
        nums: rotated sorted list of unique integers

    Returns:
        minimum value
    """

    # --------------------------------------------------------
    # Step 1. Initialize left and right boundary.
    # The minimum is somewhere inside nums[l:r+1].
    # --------------------------------------------------------
    # TODO: set l and r
    l = 0
    r = len(nums) - 1

    # --------------------------------------------------------
    # Step 2. Continue until l and r meet.
    # Here we use while l < r, not l <= r.
    # When l == r, the minimum index is found.
    # --------------------------------------------------------
    # TODO: while l < r:
    while l < r:

        # ----------------------------------------------------
        # Step 3. Compute middle index.
        # ----------------------------------------------------
        # TODO: compute mid
        mid = (l + r) // 2

        # ----------------------------------------------------
        # Step 4. Decide which side contains the minimum.
        #
        if nums[mid] > nums[r]:
            l = mid + 1
        #
        else:
            r = mid
 
    return nums[l]

if __name__ == "__main__":
    print(find_min([3, 4, 5, 1, 2]))
    # Expected: 1

    print(find_min([4, 5, 6, 7, 0, 1, 2]))
    # Expected: 0

    print(find_min([11, 13, 15, 17]))
    # Expected: 11

    print(find_min([1]))
    # Expected: 1