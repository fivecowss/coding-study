# Week 1 — Arrays, Hashing, and Basic ML Workflow

# Day 1 — Set, Dict, and Frequency Counting

## Concepts

Day 1 introduced the difference between `set` and `dict`.

Use a `set` when I only need to know whether a value has appeared before.

Use a `dict` when I need to store information associated with a value, such as count, index, or a list.

---

## Problem 1: Contains Duplicate

### Question

Given an integer array `nums`, return `True` if any value appears at least twice.
Return `False` if every element is distinct.

### Example

```python
nums = [1, 2, 3, 1]
```

Output:

```python
True
```

Why?

The value `1` appears twice.

---

## Core Pattern: Seen Set

```python
seen = set()

for x in nums:
    if x in seen:
        return True
    seen.add(x)

return False
```

### Purpose

This pattern checks whether each value has been seen before.

### Key Idea

* `seen = set()` creates an empty set.
* `x in seen` checks whether `x` already appeared.
* `seen.add(x)` records that `x` has now been seen.

### Final Solution

```python
def contains_duplicate(nums):
    seen = set()

    for x in nums:
        if x in seen:
            return True
        seen.add(x)

    return False
```

### Short Version

```python
def contains_duplicate_v2(nums):
    return len(nums) != len(set(nums))
```

The short version is useful, but the manual `seen` version is better for coding-test practice because it teaches the reusable hash-set pattern.

---

## Problem 2: Valid Anagram

### Question

Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`.
Return `False` otherwise.

An anagram means both strings contain the same characters with the same frequencies.

### Example

```python
s = "anagram"
t = "nagaram"
```

Output:

```python
True
```

Why?

Both strings contain:

```text
a: 3
n: 1
g: 1
r: 1
m: 1
```

---

## Core Pattern: Frequency Dictionary

```python
freq = {}

for ch in s:
    freq[ch] = freq.get(ch, 0) + 1
```

### Purpose

This pattern counts how many times each character appears.

### Key Idea

* `freq = {}` creates an empty dictionary.
* `freq.get(ch, 0)` returns the current count if `ch` exists.
* If `ch` does not exist, it starts from `0`.
* `+ 1` increments the count.

### Final Solution

```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False

    freq = {}

    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    for ch in t:
        if ch not in freq:
            return False

        freq[ch] -= 1

        if freq[ch] < 0:
            return False

    return True
```

### Counter Version

```python
from collections import Counter

def is_anagram_counter(s, t):
    return Counter(s) == Counter(t)
```

The `Counter` version is convenient, but the manual dictionary-counting version is more important for coding-test practice.

---

## Set vs Dict

### Use `set` when I only need existence.

```python
seen = set()

for x in nums:
    if x in seen:
        return True
    seen.add(x)
```

Question answered:

```text
Have I seen this value before?
```

---

### Use `dict` when I need to store information.

```python
freq = {}

for x in nums:
    freq[x] = freq.get(x, 0) + 1
```

Question answered:

```text
What information is associated with this value?
```

Examples:

```python
freq[x] = count
pos[x] = index
groups[key] = list_of_items
```

---

# Day 2 — Hash Map Patterns

## Problem 3: Two Sum

### Question

Given an array of integers `nums` and an integer `target`, return the indices of two numbers such that they add up to `target`.

### Example

```python
nums = [2, 7, 11, 15]
target = 9
```

Output:

```python
[0, 1]
```

Why?

```python
nums[0] + nums[1] == 2 + 7 == 9
```

---

## Core Pattern: Value to Index Dictionary

```python
pos = {}

for i, x in enumerate(nums):
    need = target - x

    if need in pos:
        return [pos[need], i]

    pos[x] = i
```

### Purpose

This pattern stores values that have already appeared and their indices.

### Key Idea

At each value `x`, calculate the value needed to complete the target:

```python
need = target - x
```

If `need` has already appeared, then `need + x == target`.

### Why Store After Checking?

```python
if need in pos:
    return [pos[need], i]

pos[x] = i
```

We check before storing the current value to avoid using the same element twice.

### Final Solution

```python
def two_sum(nums, target):
    pos = {}

    for i, x in enumerate(nums):
        need = target - x

        if need in pos:
            return [pos[need], i]

        pos[x] = i

    return []
```

### New Function: `enumerate`

```python
for i, x in enumerate(nums):
    ...
```

`enumerate(nums)` gives both index and value.

For example:

```python
nums = [2, 7, 11, 15]

for i, x in enumerate(nums):
    print(i, x)
```

Conceptual output:

```text
0 2
1 7
2 11
3 15
```

---

## Problem 4: Group Anagrams

### Question

Given an array of strings `strs`, group the anagrams together.

### Example

```python
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
```

One valid output:

```python
[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

Why?

```text
"eat", "tea", "ate" all become "aet" when sorted.
"tan", "nat" both become "ant" when sorted.
"bat" becomes "abt" and stays alone.
```

---

## Core Pattern: Group by Canonical Key

```python
from collections import defaultdict

groups = defaultdict(list)

for word in strs:
    key = "".join(sorted(word))
    groups[key].append(word)

return list(groups.values())
```

### Purpose

This pattern groups items that share the same canonical representation.

### Key Idea

All anagrams have the same sorted character string.

```python
"eat" -> "aet"
"tea" -> "aet"
"ate" -> "aet"
```

### Final Solution

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)

    for word in strs:
        key = "".join(sorted(word))
        groups[key].append(word)

    return list(groups.values())
```

### New Function: `defaultdict(list)`

```python
groups = defaultdict(list)
```

This automatically creates an empty list for a new key.

Without `defaultdict`, I would need:

```python
if key not in groups:
    groups[key] = []

groups[key].append(word)
```

With `defaultdict(list)`, I can directly write:

```python
groups[key].append(word)
```

### New Function: `sorted`

```python
sorted(word)
```

For a string, `sorted(word)` returns a list of characters in sorted order.

Example:

```python
sorted("eat")
```

Conceptual result:

```python
["a", "e", "t"]
```

### New Function: `"".join(...)`

```python
"".join(sorted(word))
```

This combines a list of characters into a string.

Example:

```python
"".join(["a", "e", "t"])
```

Result:

```python
"aet"
```

---

# Day 3 — Frequency and Set Patterns

## Problem 5: Top K Frequent Elements

### Question

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

### Example

```python
nums = [1, 1, 1, 2, 2, 3]
k = 2
```

Output:

```python
[1, 2]
```

Why?

```text
1 appears 3 times.
2 appears 2 times.
3 appears 1 time.

The two most frequent elements are 1 and 2.
```

---

## Manual Core Pattern: Frequency Dict + Sorting

```python
freq = {}

for x in nums:
    freq[x] = freq.get(x, 0) + 1

items = list(freq.items())
items.sort(key=lambda pair: pair[1], reverse=True)

result = []
for i in range(k):
    result.append(items[i][0])

return result
```

### Purpose

This pattern manually counts frequencies and sorts by count.

### Final Manual Solution

```python
def top_k_frequent(nums, k):
    freq = {}

    for x in nums:
        freq[x] = freq.get(x, 0) + 1

    items = list(freq.items())
    items.sort(key=lambda pair: pair[1], reverse=True)

    result = []

    for i in range(k):
        result.append(items[i][0])

    return result
```

### New Function: `.items()`

```python
freq.items()
```

Returns key-value pairs.

Example:

```python
freq = {1: 3, 2: 2, 3: 1}
```

Then:

```python
freq.items()
```

Conceptually gives:

```python
[(1, 3), (2, 2), (3, 1)]
```

### New Function: `.sort(key=..., reverse=True)`

```python
items.sort(key=lambda pair: pair[1], reverse=True)
```

This sorts the pairs by frequency.

* `pair[0]` is the number.
* `pair[1]` is the frequency.
* `reverse=True` sorts from largest to smallest.

---

## Counter Version

```python
from collections import Counter

def top_k_frequent_counter(nums, k):
    freq = Counter(nums)
    return [num for num, count in freq.most_common(k)]
```

This is concise, but for coding-test study, the manual version is more useful.

---

## Problem 6: Longest Consecutive Sequence

### Question

Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

The target time complexity is usually `O(n)`.

### Example

```python
nums = [100, 4, 200, 1, 3, 2]
```

Output:

```python
4
```

Why?

The longest consecutive sequence is:

```python
[1, 2, 3, 4]
```

Its length is `4`.

---

## Core Pattern: Start Only at Sequence Beginning

```python
num_set = set(nums)
best = 0

for x in num_set:
    if x - 1 not in num_set:
        length = 1

        while x + length in num_set:
            length += 1

        best = max(best, length)

return best
```

### Purpose

This pattern avoids recounting the same consecutive sequence multiple times.

### Key Idea

A number `x` is the start of a sequence only if `x - 1` does not exist.

Example:

```python
num_set = {1, 2, 3, 4, 100, 200}
```

For each value:

```text
1: 0 is not in set -> start
2: 1 is in set -> not start
3: 2 is in set -> not start
4: 3 is in set -> not start
100: 99 is not in set -> start
200: 199 is not in set -> start
```

### Final Solution

```python
def longest_consecutive(nums):
    num_set = set(nums)
    best = 0

    for x in num_set:
        if x - 1 not in num_set:
            length = 1

            while x + length in num_set:
                length += 1

            best = max(best, length)

    return best
```

### State Change Example

For:

```python
nums = [100, 4, 200, 1, 3, 2]
```

`num_set` becomes:

```python
{1, 2, 3, 4, 100, 200}
```

When `x = 1`:

```python
length = 1
```

Check:

```python
1 + 1 = 2
1 + 2 = 3
1 + 3 = 4
1 + 4 = 5
```

Since `5` is not in the set, the sequence stops.

The sequence length is `4`.

---

# Day 4 — Array Construction and Grid Validation

## Problem 7: Product of Array Except Self

### Question

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`.

Do not use division.

### Example

```python
nums = [1, 2, 3, 4]
```

Output:

```python
[24, 12, 8, 6]
```

Why?

```text
answer[0] = 2 * 3 * 4 = 24
answer[1] = 1 * 3 * 4 = 12
answer[2] = 1 * 2 * 4 = 8
answer[3] = 1 * 2 * 3 = 6
```

---

## Core Pattern: Prefix Product + Suffix Product

```python
result = [1] * len(nums)

prefix = 1
for i in range(len(nums)):
    result[i] = prefix
    prefix *= nums[i]

suffix = 1
for i in range(len(nums) - 1, -1, -1):
    result[i] *= suffix
    suffix *= nums[i]

return result
```

### Purpose

Each answer can be written as:

```text
product of elements on the left * product of elements on the right
```

### Final Solution

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n

    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
```

### New Pattern: Reverse Range

```python
for i in range(n - 1, -1, -1):
    ...
```

This loops backward.

For:

```python
n = 4
```

The values of `i` are:

```python
3, 2, 1, 0
```

### State Change Example

For:

```python
nums = [1, 2, 3, 4]
```

After prefix pass:

```python
result = [1, 1, 2, 6]
```

Meaning:

```text
result[i] contains the product of values to the left of i.
```

After suffix pass:

```python
result = [24, 12, 8, 6]
```

---

## Problem 8: Valid Sudoku

### Question

Determine if a 9 x 9 Sudoku board is valid.

Rules:

* Each row must contain digits `1-9` without repetition.
* Each column must contain digits `1-9` without repetition.
* Each 3 x 3 sub-box must contain digits `1-9` without repetition.
* Empty cells are represented by `"."`.

### Core Pattern: Set of Tuple Keys

```python
rows = set()
cols = set()
boxes = set()
```

Each filled cell creates three keys:

```python
row_key = (r, value)
col_key = (c, value)
box_key = (box_id, value)
```

### Purpose

The set stores whether a number has already appeared in a specific row, column, or box.

---

## Final Solution

```python
def is_valid_sudoku(board):
    rows = set()
    cols = set()
    boxes = set()

    for r in range(9):
        for c in range(9):
            value = board[r][c]

            if value == ".":
                continue

            box_id = (r // 3, c // 3)

            row_key = (r, value)
            col_key = (c, value)
            box_key = (box_id, value)

            if row_key in rows or col_key in cols or box_key in boxes:
                return False

            rows.add(row_key)
            cols.add(col_key)
            boxes.add(box_key)

    return True
```

### New Operator: Integer Division

```python
box_id = (r // 3, c // 3)
```

The operator `//` performs integer division.

Examples:

```python
0 // 3 == 0
1 // 3 == 0
2 // 3 == 0
3 // 3 == 1
4 // 3 == 1
5 // 3 == 1
6 // 3 == 2
```

This groups row and column indices into 3 x 3 boxes.

### Example

If:

```python
r = 4
c = 7
```

Then:

```python
box_id = (4 // 3, 7 // 3)
```

Result:

```python
(1, 2)
```

This means the cell belongs to box row `1`, box column `2`.

### Why Use Set?

We only need to know whether a row/column/box has already seen a value.

So `set` is appropriate.

```python
if row_key in rows:
    return False
```

This means the same value already appeared in the same row.

---

# Day 5 — Review and Metrics

## Coding Review Problems

The main Week 1 review problems were:

1. Contains Duplicate
2. Valid Anagram
3. Two Sum
4. Group Anagrams
5. Top K Frequent Elements
6. Longest Consecutive Sequence
7. Product of Array Except Self
8. Valid Sudoku

---

## Review Template

For each problem, I should be able to answer:

```text
1. What is the problem asking?
2. What is the input?
3. What is the output?
4. Why does the sample output make sense?
5. What data structure should I use?
6. What is the reusable coding pattern?
7. What are the time and space complexities?
```

---

## Pattern Summary

### 1. Seen Set

Use when I only need to check whether a value appeared before.

```python
seen = set()

for x in nums:
    if x in seen:
        return True
    seen.add(x)
```

Problems:

```text
Contains Duplicate
Visited-node problems
Cycle/checking problems
```

---

### 2. Frequency Dictionary

Use when I need to count values.

```python
freq = {}

for x in nums:
    freq[x] = freq.get(x, 0) + 1
```

Problems:

```text
Valid Anagram
Top K Frequent Elements
Frequency comparison problems
```

---

### 3. Value to Index Dictionary

Use when I need to remember where a value appeared.

```python
pos = {}

for i, x in enumerate(nums):
    need = target - x

    if need in pos:
        return [pos[need], i]

    pos[x] = i
```

Problems:

```text
Two Sum
Complement lookup problems
```

---

### 4. Group by Key

Use when multiple items should belong to the same group.

```python
from collections import defaultdict

groups = defaultdict(list)

for item in items:
    key = get_key(item)
    groups[key].append(item)

return list(groups.values())
```

Specific example for anagrams:

```python
from collections import defaultdict

groups = defaultdict(list)

for word in strs:
    key = "".join(sorted(word))
    groups[key].append(word)

return list(groups.values())
```

Problems:

```text
Group Anagrams
Grouping by category
Grouping by transformed representation
```

---

### 5. Start Point Detection

Use when I need to count sequences but avoid repeated work.

```python
num_set = set(nums)

for x in num_set:
    if x - 1 not in num_set:
        length = 1

        while x + length in num_set:
            length += 1
```

Problems:

```text
Longest Consecutive Sequence
Sequence expansion problems
```

---

### 6. Prefix/Suffix Construction

Use when each answer depends on values to the left and right.

```python
result = [1] * len(nums)

prefix = 1
for i in range(len(nums)):
    result[i] = prefix
    prefix *= nums[i]

suffix = 1
for i in range(len(nums) - 1, -1, -1):
    result[i] *= suffix
    suffix *= nums[i]
```

Problems:

```text
Product of Array Except Self
Left/right accumulation problems
```

---

### 7. Grid Validation with Tuple Keys

Use when validating rows, columns, and boxes.

```python
rows = set()
cols = set()
boxes = set()

for r in range(9):
    for c in range(9):
        value = board[r][c]

        if value == ".":
            continue

        box_id = (r // 3, c // 3)

        row_key = (r, value)
        col_key = (c, value)
        box_key = (box_id, value)

        if row_key in rows or col_key in cols or box_key in boxes:
            return False

        rows.add(row_key)
        cols.add(col_key)
        boxes.add(box_key)

return True
```

Problems:

```text
Valid Sudoku
Matrix validation
Grid-based duplicate detection
```

---

# Data Science Practice — scikit-learn Logistic Regression

This section is separate from coding-test practice.

For coding-test problems, avoid packages.
For practical DS/ML workflow, use `pandas`, `numpy`, and `scikit-learn`.

---

## Basic Workflow

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

data = load_breast_cancer(as_frame=True)

X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))
```

---

## Key Concepts

### `train_test_split`

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)
```

Meaning:

```text
test_size=0.2
- Use 20% of the data as test data.

random_state=42
- Make the split reproducible.

stratify=y
- Preserve class proportions in train and test sets.
```

---

### `LogisticRegression`

```python
model = LogisticRegression(max_iter=1000)
```

Meaning:

```text
Create a logistic regression classification model.
```

The option:

```python
max_iter=1000
```

allows the optimization algorithm to run for up to 1000 iterations.

---

### `fit`

```python
model.fit(X_train, y_train)
```

Meaning:

```text
Train the model on the training data.
```

---

### `predict`

```python
pred = model.predict(X_test)
```

Meaning:

```text
Predict class labels for the test data.
```

---

## Classification Metrics

### Accuracy

```python
accuracy_score(y_test, pred)
```

Meaning:

```text
Correct predictions / total predictions
```

Good for:

```text
Overall performance when classes are reasonably balanced.
```

Weakness:

```text
Can be misleading under class imbalance.
```

---

### Classification Report

```python
classification_report(y_test, pred)
```

Shows:

```text
precision
recall
f1-score
support
```

---

### Precision

```text
Of the samples predicted as positive, how many were actually positive?
```

Good for:

```text
Reducing false positives.
```

---

### Recall

```text
Of the actual positive samples, how many did the model catch?
```

Good for:

```text
Reducing false negatives.
```

Important in:

```text
Medical diagnosis
Fraud detection
Risk detection
```

---

### F1-score

```text
Harmonic mean of precision and recall.
```

Good for:

```text
Summarizing precision and recall together.
```

---

### Confusion Matrix

```python
from sklearn.metrics import confusion_matrix

confusion_matrix(y_test, pred)
```

Binary layout is usually:

```text
[[TN, FP],
 [FN, TP]]
```

This helps show exactly how the model is making mistakes.

---

# Week 1 Main Takeaways

## Python Coding-Test Takeaways

I should be able to manually write:

```python
seen = set()

for x in nums:
    if x in seen:
        return True
    seen.add(x)
```

```python
freq = {}

for x in nums:
    freq[x] = freq.get(x, 0) + 1
```

```python
pos = {}

for i, x in enumerate(nums):
    need = target - x

    if need in pos:
        return [pos[need], i]

    pos[x] = i
```

```python
from collections import defaultdict

groups = defaultdict(list)

for word in strs:
    key = "".join(sorted(word))
    groups[key].append(word)
```

```python
num_set = set(nums)

for x in num_set:
    if x - 1 not in num_set:
        length = 1

        while x + length in num_set:
            length += 1
```

```python
result = [1] * len(nums)

prefix = 1
for i in range(len(nums)):
    result[i] = prefix
    prefix *= nums[i]

suffix = 1
for i in range(len(nums) - 1, -1, -1):
    result[i] *= suffix
    suffix *= nums[i]
```

---

## Problems to Retry

| Problem                      | Pattern               | Retry Needed? | Notes |
| ---------------------------- | --------------------- | ------------: | ----- |
| Contains Duplicate           | Seen set              |               |       |
| Valid Anagram                | Frequency dict        |               |       |
| Two Sum                      | Value to index dict   |               |       |
| Group Anagrams               | Group by sorted key   |               |       |
| Top K Frequent Elements      | Frequency sorting     |               |       |
| Longest Consecutive Sequence | Start point detection |               |       |
| Product of Array Except Self | Prefix/suffix product |               |       |
| Valid Sudoku                 | Tuple keys in sets    |               |       |

---

# Complexity Summary

| Problem                      |         Time Complexity |         Space Complexity | Main Pattern              |
| ---------------------------- | ----------------------: | -----------------------: | ------------------------- |
| Contains Duplicate           |                    O(n) |                     O(n) | set                       |
| Valid Anagram                |                    O(n) |             O(1) or O(k) | frequency dict            |
| Two Sum                      |                    O(n) |                     O(n) | hash map                  |
| Group Anagrams               |            O(n k log k) |                    O(nk) | sorted key grouping       |
| Top K Frequent Elements      | O(n log n) with sorting |                     O(n) | frequency sort            |
| Longest Consecutive Sequence |            O(n) average |                     O(n) | set start detection       |
| Product of Array Except Self |                    O(n) | O(1) extra except output | prefix/suffix             |
| Valid Sudoku                 |                    O(1) |                     O(1) | fixed 9x9 grid validation |

Notes:

```text
For Valid Anagram, if characters are limited to lowercase English letters, space can be treated as O(1).
For Valid Sudoku, the board size is fixed at 9x9, so time and space are O(1) in strict complexity terms.
For Group Anagrams, n = number of words and k = average word length.
```


