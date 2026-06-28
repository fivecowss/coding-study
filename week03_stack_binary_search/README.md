# Week 3 Day 1: Basic Stack

## Today's Goals

- Understand stack as a Last-In, First-Out data structure.
- Use Python list as a stack with append, pop, and stack[-1].
- Solve Valid Parentheses using a stack.
- Implement MinStack with O(1) getMin.

---

## 1. Stack Basics

A stack follows Last-In, First-Out order.

Python stack operations:

```python
stack = []

stack.append(x)   # push
stack[-1]         # peek
stack.pop()       # pop
```

## Day 2: Expression Stack and Monotonic Stack

### Evaluate Reverse Polish Notation

Pattern:
- Use stack to store numbers.
- If token is a number, push it.
- If token is an operator, pop two numbers.
- Apply the operator.
- Push the result back.

Important:
```python
b = stack.pop()
a = stack.pop()
```

## Day 3: Monotonic Stack Advanced

### Car Fleet

Pattern:
- Sort cars by position in descending order.
- Compute each car's arrival time.
- Use stack to store fleet arrival times.

Key idea:
- If a car behind reaches the target earlier than or at the same time as the fleet ahead, it joins that fleet.

Template:

```python
cars = sorted(zip(position, speed), reverse=True)
stack = []

for pos, spd in cars:
    time = (target - pos) / spd
    stack.append(time)

    if len(stack) >= 2 and stack[-1] <= stack[-2]:
        stack.pop()

return len(stack)
```

Questions:
- Why do we sort by position descending?
- Why does stack store arrival time?
- What does popping mean?

---

### Largest Rectangle in Histogram

Pattern:
- Use a monotonic increasing stack.
- Stack stores `(start_index, height)`.
- When current height is smaller than stack top height, pop and compute area.

Template:

```python
stack = []
max_area = 0

for i, h in enumerate(heights):
    start = i

    while stack and stack[-1][1] > h:
        index, height = stack.pop()
        max_area = max(max_area, height * (i - index))
        start = index

    stack.append((start, h))

for index, height in stack:
    max_area = max(max_area, height * (len(heights) - index))

return max_area
```

Key idea:
- Popping means the popped height cannot extend past the current index.
- Remaining bars in stack can extend to the end of the histogram.

## Day 4: Binary Search Basics

### Binary Search

Pattern:
- Use when the array is sorted.
- Maintain search range `[l, r]`.
- Compare `nums[mid]` with `target`.
- Remove the impossible half.

Template:

```python
l, r = 0, len(nums) - 1

while l <= r:
    mid = (l + r) // 2

    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        l = mid + 1
    else:
        r = mid - 1

return -1
```

Invariant:
- If target exists, it is inside `nums[l:r+1]`.

---

### Search a 2D Matrix

Pattern:
- Treat an `m x n` matrix as a virtual sorted 1D array.
- Search over indices from `0` to `m*n - 1`.

Index conversion:

```python
row = mid // n
col = mid % n
```

Template:

```python
m = len(matrix)
n = len(matrix[0])

l, r = 0, m * n - 1

while l <= r:
    mid = (l + r) // 2

    row = mid // n
    col = mid % n
    value = matrix[row][col]

    if value == target:
        return True
    elif value < target:
        l = mid + 1
    else:
        r = mid - 1

return False
```

Key questions:
1. What is the current search range?
2. What does `mid` represent?
3. How do we decide which half to discard?
4. In 2D matrix search, how do we convert `mid` into row and column?

## Day 5: Rotated Binary Search and Binary Search on Answer

### Find Minimum in Rotated Sorted Array

Pattern:
- Rotated binary search.
- Use `nums[mid]` and `nums[r]` to decide where the minimum is.
- If `nums[mid] > nums[r]`, the minimum is on the right.
- Otherwise, the minimum is at `mid` or on the left.

Template:

```python
l, r = 0, len(nums) - 1

while l < r:
    mid = (l + r) // 2

    if nums[mid] > nums[r]:
        l = mid + 1
    else:
        r = mid

return nums[l]
```

Important:
- Use `while l < r`.
- Use `r = mid`, not `r = mid - 1`.
- `nums[mid]` may be the minimum, so we should not discard it.

---

### Koko Eating Bananas

Pattern:
- Binary search on answer.
- Search for the minimum feasible eating speed.
- Feasibility is monotone.

Search space:

```python
l, r = 1, max(piles)
```

Integer ceiling:

```python
hours += (pile + k - 1) // k
```

Template:

```python
l, r = 1, max(piles)
ans = r

while l <= r:
    k = (l + r) // 2

    hours = 0
    for pile in piles:
        hours += (pile + k - 1) // k

    if hours <= h:
        ans = k
        r = k - 1
    else:
        l = k + 1

return ans
```

Key questions:
1. What is the search space?
2. What does `mid` represent?
3. What is the feasibility condition?
4. If `mid` is feasible, why do we move left?
5. If `mid` is not feasible, why do we move right?