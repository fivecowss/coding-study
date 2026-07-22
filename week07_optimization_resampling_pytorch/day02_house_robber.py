from typing import List


def rob(nums: List[int]) -> int:
    """
    Problem:
    Each value represents money stored in one house. Adjacent houses
    cannot both be selected. Return the maximum amount that can be
    collected.

    Example:
    nums = [2, 7, 9, 3, 1]
    result = 12

    Explanation:
    Select houses with values 2, 9, and 1.
    """

    # TODO: Implement one-pass dynamic programming with two variables.
    # Track the best result through the house two positions back and
    # the best result through the previous house. At each house, compare
    # taking the current house with skipping it.

    prev_two = 0
    prev_one = 0

    for money in nums:
        take_current = prev_two + money
        skip_current = prev_one

        current = max(
            take_current,
            skip_current,
        )

        prev_two = prev_one
        prev_one = current

    return prev_one

def run_examples() -> None:
    examples = [
        ([1, 2, 3, 1], 4),
        ([2, 7, 9, 3, 1], 12),
        ([2, 1, 1, 2], 4),
        ([], 0),
        ([5], 5),
    ]

    for nums, expected in examples:
        result = rob(nums)

        print(
            f"nums={nums}, "
            f"result={result}, "
            f"expected={expected}"
        )


if __name__ == "__main__":
    run_examples()