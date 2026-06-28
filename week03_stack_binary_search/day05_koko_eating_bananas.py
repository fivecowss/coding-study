# ============================================================
# Problem: LeetCode 875. Koko Eating Bananas
# Pattern: Binary Search on Answer
#
# Key idea:
#   - We are not searching for an index in piles.
#   - We are searching for the minimum feasible eating speed k.
#   - If speed k can finish within h hours,
#     try smaller speeds.
#   - Otherwise, speed k is too slow, so try larger speeds.
# ============================================================


def min_eating_speed(piles: list[int], h: int) -> int:
    """
    Return the minimum integer eating speed k
    such that Koko can eat all bananas within h hours.

    Args:
        piles: list of banana piles
        h: maximum allowed hours

    Returns:
        minimum feasible eating speed
    """

    # --------------------------------------------------------
    # Step 1. Define search space for speed k.
    # Slowest possible speed is 1.
    # Fastest necessary speed is max(piles).
    # --------------------------------------------------------
    # TODO: set l and r
    l = 0
    r = max(piles)
    

    # --------------------------------------------------------
    # Step 2. Store current best answer.
    # Initialize with r because max(piles) is always feasible
    # under standard problem constraints.
    # --------------------------------------------------------
    # TODO: initialize ans
    ans = r

    # --------------------------------------------------------
    # Step 3. Binary search over possible speed k.
    # --------------------------------------------------------
    # TODO: while l <= r:
    while l <= r:

        # ----------------------------------------------------
        # Step 4. Candidate speed.
        # ----------------------------------------------------
        # TODO: compute k
        k = (l + r) // 2

        # ----------------------------------------------------
        # Step 5. Compute total hours needed at speed k.
        # For each pile:
        #   hours += ceil(pile / k)
        #
        # Use integer ceiling:
        #   (pile + k - 1) // k
        # ----------------------------------------------------
        hours = 0

        for pile in piles:
            hours += (pile + k - 1) // k

        # ----------------------------------------------------
        # Step 6. If hours <= h, k is feasible.
        # Save answer and try smaller speed.
        # ----------------------------------------------------
        # TODO:
        if hours <= h:
            ans = k
            r = k - 1
        else:
            l = k + 1

    # --------------------------------------------------------
    # Step 7. Return minimum feasible speed.
    # --------------------------------------------------------
    return ans


if __name__ == "__main__":
    print(min_eating_speed([3, 6, 7, 11], 8))
    # Expected: 4

    print(min_eating_speed([30, 11, 23, 4, 20], 5))
    # Expected: 30

    print(min_eating_speed([30, 11, 23, 4, 20], 6))
    # Expected: 23