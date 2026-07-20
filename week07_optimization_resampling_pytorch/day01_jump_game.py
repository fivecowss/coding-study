from typing import List


def can_jump(nums: List[int]) -> bool:
    """
    Return True if the final index is reachable from index zero.
    """

    # TODO: Handle an empty local input if desired.
    if not nums:
        return False

    # TODO: Track the farthest reachable index.
    farthest = 0
    final_index = len(nums) - 1


    # TODO: Iterate through each index and jump value.
    for index, jump_length in enumerate(nums):
        # TODO: If the current index is beyond the reachable boundary,
        # return False.
        if index > farthest:
            return False

        # TODO: Update the farthest reachable index.
        farthest = max(
            farthest,
            index + jump_length,
        )

        # TODO: Return True early if the final index is reachable.
        if farthest >= final_index:
            return True

    # TODO: Return the final result.

    return True


def run_examples() -> None:
    examples = [
        ([2, 3, 1, 1, 4], True),
        ([3, 2, 1, 0, 4], False),
        ([0], True),
        ([2, 0, 0], True),
        ([1, 0, 1], False),
    ]

    for nums, expected in examples:
        result = can_jump(nums)
        print(
            f"nums={nums}, "
            f"result={result}, "
            f"expected={expected}"
        )


if __name__ == "__main__":
    run_examples()