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

