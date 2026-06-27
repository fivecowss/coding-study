# week03_stack_binary_search/day03_car_fleet.py


# ============================================================
# Problem: LeetCode 853. Car Fleet
# Pattern: Sorting + Stack
#
# Key idea:
#   - Sort cars by position in descending order.
#   - Compute each car's time to reach target.
#   - Use stack to store fleet arrival times.
#   - If a car behind reaches earlier or at the same time,
#     it joins the fleet ahead.
# ============================================================


def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    """
    Return the number of car fleets that will arrive at the target.

    Args:
        target: destination position
        position: current positions of cars
        speed: speeds of cars

    Returns:
        number of car fleets
    """

    # --------------------------------------------------------
    # Step 1. Pair each car's position and speed.
    # Example:
    #   position = [10, 8]
    #   speed = [2, 4]
    #   zip(position, speed) -> [(10, 2), (8, 4)]
    # --------------------------------------------------------
    # TODO: create cars sorted by position descending
    cars = sorted(zip(position, speed), reverse= True)

    # --------------------------------------------------------
    # Step 2. Create stack.
    # Stack stores fleet arrival times.
    # --------------------------------------------------------
    stack = []

    # --------------------------------------------------------
    # Step 3. Loop through cars from closest to target
    # to farthest from target.
    # --------------------------------------------------------
    for pos, spd in cars:

        # ----------------------------------------------------
        # Step 4. Compute time to reach target.
        # ----------------------------------------------------
        # TODO: compute arrival time
        time = (pos - target) / spd

        # ----------------------------------------------------
        # Step 5. Push current car's arrival time.
        # ----------------------------------------------------
        # TODO: append time to stack
        stack.append(time)

        # ----------------------------------------------------
        # Step 6. If current car catches up to fleet ahead,
        # merge it by removing current time.
        #
        # Condition:
        #   if current time <= previous fleet time
        # ----------------------------------------------------
        if len(stack) >= 2 and stack[-1] <= stack[-2]:
            stack.pop()

    # --------------------------------------------------------
    # Step 7. Each remaining time in stack represents one fleet.
    # --------------------------------------------------------
    return len(stack)


if __name__ == "__main__":
    print(car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]))
    # Expected: 3

    print(car_fleet(10, [3], [3]))
    # Expected: 1

    print(car_fleet(100, [0, 2, 4], [4, 2, 1]))
    # Expected: 1