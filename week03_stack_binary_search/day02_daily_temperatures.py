
# ============================================================
# Problem: LeetCode 739. Daily Temperatures
# Pattern: Monotonic Stack
# Key idea:
#   - Store indices whose warmer future day has not been found yet.
#   - When current temperature is warmer than stack top's temperature,
#     we can fill the answer for that previous day.
# ============================================================


def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    For each day, return how many days we have to wait
    until a warmer temperature.

    Args:
        temperatures: list of daily temperatures

    Returns:
        list of waiting days
    """

    # --------------------------------------------------------
    # Step 1. Create result array filled with 0.
    # Default answer is 0 because some days may never find
    # a warmer future day.
    # --------------------------------------------------------
    # TODO: initialize result list
    res = [0] * len(temperatures)

    # --------------------------------------------------------
    # Step 2. Create empty stack.
    # Stack stores indices, not temperatures.
    # --------------------------------------------------------
    stack = []

    # --------------------------------------------------------
    # Step 3. Loop through each day.
    # i: current day index
    # temp: current day's temperature
    # --------------------------------------------------------
    for i, temp in enumerate(temperatures):

        # ----------------------------------------------------
        # Step 4. While current temperature is warmer than
        # the temperature at stack top index:
        #
        #   - pop previous index
        #   - compute waiting days
        #   - update result
        # ----------------------------------------------------
        while stack and temp > temperatures[stack[-1]]:
            prev = stack.pop()
            res[prev] = i - prev
        # ----------------------------------------------------
        # Step 5. Push current index because this day is now
        # waiting for a warmer future day.
        # ----------------------------------------------------
        stack.append(i)

    # --------------------------------------------------------
    # Step 6. Return result.
    # Days that never found a warmer future day remain 0.
    # --------------------------------------------------------
    return res


if __name__ == "__main__":
    print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
    # Expected: [1, 1, 4, 2, 1, 1, 0, 0]

    print(daily_temperatures([30, 40, 50, 60]))
    # Expected: [1, 1, 1, 0]

    print(daily_temperatures([30, 60, 90]))
    # Expected: [1, 1, 0]