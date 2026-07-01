"""
Week 4 Day 2: Sorting, Heap, Top-K

Goal:
- Practice sorting with key functions.
- Practice Counter for frequency counting.
- Practice heapq for top-k problems.
- Leave sample answers commented out at the bottom.

Core ideas:
1. Sorting is often simplest and safest.
2. Heap is useful when we only need top k, not full sorting.
3. Counter gives frequency map quickly.
"""

from collections import Counter
import heapq


def sort_pairs_by_second_value(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    Sort list of pairs by second value ascending.

    Example:
    items = [("a", 3), ("b", 1), ("c", 2)]
    output = [("b", 1), ("c", 2), ("a", 3)]

    TODO:
    1. Use sorted().
    2. Use key=lambda x: x[1].
    """
    # Your code here
    return sorted(items, key = lambda x: x[1])


def sort_words_by_length_then_alphabet(words: list[str]) -> list[str]:
    """
    Sort words by:
    1. length ascending
    2. alphabetically ascending if same length

    Example:
    ["pear", "a", "dog", "apple", "cat"]
    -> ["a", "cat", "dog", "pear", "apple"]

    TODO:
    1. Use sorted().
    2. key should be a tuple: (len(word), word).
    """
    # Your code here
    return [sorted(words, key = lambda word: (len(word), word))]


def kth_largest(nums: list[int], k: int) -> int:
    """
    Return the kth largest element.

    Direction:
    - Use a min-heap of size k.
    - Push each number.
    - If heap size exceeds k, pop the smallest.
    - At the end, heap[0] is the kth largest.

    TODO:
    1. Initialize empty heap.
    2. Loop over nums.
    3. heappush each value.
    4. If len(heap) > k, heappop.
    5. Return heap[0].
    """
    # Your code here
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def top_k_frequent_by_sorting(nums: list[int], k: int) -> list[int]:
    """
    Return k most frequent elements using Counter + sorting.

    Direction:
    - Count frequencies.
    - Sort items by frequency descending.
    - Return first k numbers.

    TODO:
    1. freq = Counter(nums)
    2. Convert freq.items() to sorted list.
    3. Sort by count descending.
    4. Extract only the numbers.
    """
    freq = Counter(nums)
    sorted_items = sorted(freq.items(), key = lambda x: x[1], reverse = True)
    return [num for num, count in sorted_items[:k]]


def top_k_frequent_by_heap(nums: list[int], k: int) -> list[int]:
    """
    Return k most frequent elements using Counter + min-heap.

    Direction:
    - Heap should store (count, num).
    - Keep heap size <= k.
    - If size exceeds k, pop the smallest frequency.
    - Return the numbers left in the heap.

    Note:
    - Output order usually does not matter for LeetCode Top K Frequent.
    """
    # Your code here
    freq = Counter(nums)
    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for count, num in heap]


def main() -> None:
    items = [("a", 3), ("b", 1), ("c", 2)]
    words = ["pear", "a", "dog", "apple", "cat"]
    nums = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]

    print("1. Sort pairs by second value")
    print(sort_pairs_by_second_value(items))

    print("\n2. Sort words by length, then alphabet")
    print(sort_words_by_length_then_alphabet(words))

    print("\n3. Kth largest")
    print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # expected: 5

    print("\n4. Top k frequent by sorting")
    print(top_k_frequent_by_sorting(nums, 2))

    print("\n5. Top k frequent by heap")
    print(top_k_frequent_by_heap(nums, 2))


if __name__ == "__main__":
    main()


# -------------------------------------------------------------------
# SAMPLE ANSWER — REFERENCE ONLY
# Keep this section commented out.
# -------------------------------------------------------------------

# def sort_pairs_by_second_value(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
#     return sorted(items, key=lambda x: x[1])
#
#
# def sort_words_by_length_then_alphabet(words: list[str]) -> list[str]:
#     return sorted(words, key=lambda word: (len(word), word))
#
#
# def kth_largest(nums: list[int], k: int) -> int:
#     heap = []
#
#     for x in nums:
#         heapq.heappush(heap, x)
#
#         if len(heap) > k:
#             heapq.heappop(heap)
#
#     return heap[0]
#
#
# def top_k_frequent_by_sorting(nums: list[int], k: int) -> list[int]:
#     freq = Counter(nums)
#     sorted_items = sorted(
#         freq.items(),
#         key=lambda x: x[1],
#         reverse=True,
#     )
#     return [num for num, count in sorted_items[:k]]
#
#
# def top_k_frequent_by_heap(nums: list[int], k: int) -> list[int]:
#     freq = Counter(nums)
#     heap = []
#
#     for num, count in freq.items():
#         heapq.heappush(heap, (count, num))
#
#         if len(heap) > k:
#             heapq.heappop(heap)
#
#     return [num for count, num in heap]