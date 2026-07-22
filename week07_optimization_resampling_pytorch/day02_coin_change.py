from typing import List


def coin_change(coins: List[int], amount: int) -> int:
    """
    Problem:
    Given coin denominations and a target amount, return the minimum
    number of coins required to make the target amount. Each coin may
    be used any number of times. Return -1 when the amount cannot be made.

    Example:
    coins = [1, 2, 5]
    amount = 11
    result = 3

    Explanation:
    11 = 5 + 5 + 1
    """

    # TODO: Create a one-dimensional DP table in which dp[value]
    # stores the minimum number of coins needed to make value.
    # Initialize dp[0] as zero and all other states as unreachable.
    # For each target value, try every usable coin and update the state.

    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0

    for current_amount in range(1, amount + 1):
        for coin in coins:
            if coin <= current_amount:
                dp[current_amount] = min(
                    dp[current_amount],
                    dp[current_amount - coin] + 1,
                )

    if dp[amount] == unreachable:
        return -1


def run_examples() -> None:
    examples = [
        ([1, 2, 5], 11, 3),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1, 3, 4], 6, 2),
    ]

    for coins, amount, expected in examples:
        result = coin_change(coins, amount)

        print(
            f"coins={coins}, "
            f"amount={amount}, "
            f"result={result}, "
            f"expected={expected}"
        )


if __name__ == "__main__":
    run_examples()