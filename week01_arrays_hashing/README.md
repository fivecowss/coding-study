## Week 1 Day 2 — Hash Map Patterns

### Problems

1. Two Sum
2. Group Anagrams

### Python concepts

- `enumerate`
- `dict[value] = index`
- `defaultdict(list)`
- `"".join(sorted(word))`

### Key patterns

pos = {}

for i, x in enumerate(nums):
    need = target - x

    if need in pos:
        return [pos[need], i]

    pos[x] = i

from collections import defaultdict

groups = defaultdict(list)

for word in strs:
    key = "".join(sorted(word))
    groups[key].append(word)

---

## Week 1 Day 3 - Frequency and Set Patterns
### Problems

1. Top K Frequent Elements
2. Longest Consecutive Sequence

### Python concepts
- `Counter`
- `most_common`
- `sorted(..., key=...)`
- `set`
- `while`

### Key patterns
from collections import Counter

freq = Counter(nums)
freq.most_common(k)

num_set = set(nums)

for x in num_set:
    if x - 1 not in num_set:
        length = 1

        while x + length in num_set:
            length += 1

## Sklearn practice

### Concepts
- `load_breast_cancer`
- `train_test_split`
- `test_size`
- `random_state`
- `stratify`

---

## Week 1 Day 4 — Array Construction and Grid Validation

### Problems

1. Product of Array Except Self
2. Valid Sudoku

### Concepts

- prefix product
- suffix product
- reverse range
- nested loops
- grid indexing
- integer division `//`
- tuple keys
- set-based validation

### Key Patterns

Product Except Self:

- Use result array initialized with 1s.
- First pass stores left-side products.
- Second pass multiplies right-side products.

Valid Sudoku:

- Use sets to track seen row/column/box entries.
- Store keys such as `(row, value)`, `(col, value)`, and `(box_id, value)`.

---

## Week 1 Day 5 — Review and Metrics

### Coding Review

Problems reviewed:

1. Contains Duplicate
2. Valid Anagram
3. Two Sum
4. Group Anagrams
5. Top K Frequent Elements
6. Longest Consecutive Sequence
7. Product of Array Except Self
8. Valid Sudoku

### sklearn Metrics

Concepts:

- `accuracy`
- `precision`
- `recall`
- `F1`
- `confusion matrix`
- `classification report`