# week03_stack_binary_search/day03_largest_rectangle_histogram.py


# ============================================================
# Problem: LeetCode 84. Largest Rectangle in Histogram
# Pattern: Monotonic Increasing Stack
#
# Key idea:
#   - Stack stores (start_index, height).
#   - Heights in stack are increasing.
#   - When current height is smaller than stack top height,
#     the rectangle with stack top height must end before current index.
# ============================================================


def largest_rectangle_area(heights: list[int]) -> int:
    """
    Return the largest rectangle area in a histogram.

    Args:
        heights: list of bar heights

    Returns:
        maximum rectangle area
    """

    # --------------------------------------------------------
    # Step 1. Create empty stack.
    # Stack stores pairs: (start_index, height)
    # --------------------------------------------------------
    stack = []

    # --------------------------------------------------------
    # Step 2. Track maximum area.
    # --------------------------------------------------------
    max_area = 0

    # --------------------------------------------------------
    # Step 3. Iterate through each bar.
    # i: current index
    # h: current height
    # --------------------------------------------------------
    for i, h in enumerate(heights):

        # ----------------------------------------------------
        # Step 4. Assume current rectangle starts at i.
        # This may move left if we pop taller bars.
        # ----------------------------------------------------
        start = i

        # ----------------------------------------------------
        # Step 5. While stack top is taller than current height:
        #   - pop previous height
        #   - compute area using popped height
        #   - update max_area
        #   - move start index left
        # ----------------------------------------------------
        while stack and stack[-1][1] > h:
            index, height = stack.pop()
            max_area = max(max_area, height * (i - index))
            start = index

        # ----------------------------------------------------
        # Step 6. Push current height with the earliest start.
        # ----------------------------------------------------
        stack.append((start, h))
        

    # --------------------------------------------------------
    # Step 7. Process bars that remain in stack.
    # These bars can extend to the end of the histogram.
    # --------------------------------------------------------
    
    for index, height in stack:
        max_area = max(max_area, height * (len(heights) - index))

    # --------------------------------------------------------
    # Step 8. Return max_area.
    # --------------------------------------------------------
    return max_area
    


if __name__ == "__main__":
    print(largest_rectangle_area([2, 1, 5, 6, 2, 3]))
    # Expected: 10

    print(largest_rectangle_area([2, 4]))
    # Expected: 4

    print(largest_rectangle_area([1, 1]))
    # Expected: 2