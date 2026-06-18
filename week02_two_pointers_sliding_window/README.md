# Week 2 — Two Pointers, Sliding Window, Prefix Sum

## Day 1 — Basic Two Pointers

### Problems

1. Valid Palindrome
2. Two Sum II: Input Array Is Sorted

### Pattern: Two Pointers

Use two pointers when:
- the array/string can be scanned from both ends
- the input is sorted
- we need to compare pairs
- moving one pointer has a clear logical reason

### Valid Palindrome

Key idea:
- Use left and right pointers.
- Skip non-alphanumeric characters.
- Compare lowercase characters.

Python methods:
- `isalnum()`
- `lower()`
- `continue`

### Two Sum II

Key idea:
- Because the input array is sorted, use left and right pointers.
- If the sum is too small, move left.
- If the sum is too large, move right.
- Return 1-indexed positions.

Mistakes to watch:
- Returning zero-based indices.
- Moving the wrong pointer.
- Forgetting that the input is already sorted.