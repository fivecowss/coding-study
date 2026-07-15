"""
Day 2 Algorithm Practice:
- Kth Largest Element
- Merge Intervals
"""

import heapq


def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Return the kth largest element.

    Example:
    nums = [3, 2, 1, 5, 6, 4], k = 2
    answer = 5
    """
    # TODO:
    # Use a min-heap of size k.
    heap = []

    for x in nums:
        heapq.heappush(heap, x)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge overlapping intervals.

    Example:
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    answer = [[1, 6], [8, 10], [15, 18]]
    """
    # TODO:
    # Sort intervals by start.
    # Merge if current start <= previous end.
    if not intervals:
        return []
    
    intervals.sort(key = lambda x: x[0])

    merged = []

    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged


def main() -> None:
    print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))
    print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))


if __name__ == "__main__":
    main()