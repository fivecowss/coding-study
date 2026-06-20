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

## Day 2 — Sorted Two Pointers

### Problems

1. 3Sum
2. Container With Most Water

---

### Pattern: Sort + Two Pointers

Use this pattern when:
- the problem asks for pairs or triplets
- sorting gives a clear direction for pointer movement
- we need to avoid brute force over all combinations

General structure:

```python
nums.sort()

for i in range(len(nums)):
    left = i + 1
    right = len(nums) - 1

    while left < right:
        total = nums[i] + nums[left] + nums[right]
```

## Day 3 — Sliding Window I

### Problems

1. Best Time to Buy and Sell Stock
2. Longest Substring Without Repeating Characters

---

### Pattern: One-pass state tracking

Use this pattern when:
- we scan the array once
- we only need to remember the best previous state
- the answer can be updated at each step

Example: Best Time to Buy and Sell Stock

Key variables:
- `min_price`: the lowest price seen so far
- `best`: the maximum profit seen so far

Logic:
- update `min_price`
- compute current profit
- update `best`

---

### Pattern: Sliding Window

Use this pattern when:
- the problem asks about a contiguous substring or subarray
- we need the longest or shortest valid window
- we can expand with `right` and shrink with `left`

General template:

```python
left = 0
state = set()
best = 0

for right in range(len(s)):
    while window_is_invalid:
        remove s[left] from state
        left += 1

    add s[right] to state
    best = max(best, right - left + 1)
```

## Day 4 — Sliding Window II: Frequency Window

### Problems

1. Longest Repeating Character Replacement
2. Permutation in String

---

### Pattern: Frequency Sliding Window

Use this pattern when:
- the problem asks about character counts
- the window validity depends on frequency
- we need to know how many times each character appears in the current window

General structure:

```python
left = 0
count = {}

for right in range(len(s)):
    add s[right] to count

    while window is invalid:
        remove s[left] from count
        left += 1

    update answer
```
## Day 5 — Prefix Sum

### Problems

1. Range Sum Query: Immutable
2. Subarray Sum Equals K

---

### Pattern 1: Prefix Array

Use this pattern when:
- the array does not change
- we need to answer multiple range sum queries
- we want O(1) range sum after O(n) preprocessing

Template:

```python
prefix = [0]

for x in nums:
    prefix.append(prefix[-1] + x)

range_sum = prefix[right + 1] - prefix[left]
```

Why length n + 1?
- It avoids special handling when `left == 0`.
- Every query can use the same formula.

---

### Pattern 2: Prefix Sum + Hash Map

Use this pattern when:
- we need to count subarrays with target sum
- the array may contain negative numbers
- sliding window is not reliable

Core equation:

```text
current_sum - previous_sum = k
previous_sum = current_sum - k
```

Template:

```python
count = {0: 1}
cur = 0
ans = 0

for x in nums:
    cur += x
    ans += count.get(cur - k, 0)
    count[cur] = count.get(cur, 0) + 1
```

Important:
- `count = {0: 1}` handles subarrays starting at index 0.
- Check previous prefix sums before recording the current prefix sum.
- The dict stores frequency, not just existence.

Mistakes to watch:
- Starting with `count = {}`.
- Updating `count[cur]` before checking `cur - k`.
- Using `k - cur` instead of `cur - k`.
- Trying to use sliding window when negative numbers are allowed.