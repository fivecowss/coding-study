from typing import List


def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    """
    Return the minimum number of intervals that must be removed
    so the remaining intervals do not overlap.
    """

    # TODO: Handle an empty input if your local implementation allows it.
    if not intervals:
        return 0

    # TODO: Sort intervals using the end value as the sorting key.
    intervals.sort(key = lambda interval: interval[1])

    # TODO: Initialize the number of removed intervals.
    removed = 0

    # TODO: Initialize the end point of the last selected interval.
    previous_end = float("-inf")

    # TODO: Iterate through every interval.
    for start, end in intervals:

        # TODO: If the current interval is compatible, keep it.
        if start >= previous_end:
            previous_end = end

        # TODO: Otherwise, count it as removed.
        else:
            removed += 1


    # TODO: Return the removal count.

    return removed


def run_examples() -> None:
    examples = [
        ([[1, 2], [2, 3], [3, 4], [1, 3]], 1),
        ([[1, 2], [1, 2], [1, 2]], 2),
        ([[1, 2], [2, 3]], 0),
        ([[-3, -1], [-2, 1], [1, 2]], 1),
    ]

    for intervals, expected in examples:
        result = erase_overlap_intervals(intervals)
        print(
            f"intervals={intervals}, "
            f"result={result}, "
            f"expected={expected}"
        )


if __name__ == "__main__":
    run_examples()