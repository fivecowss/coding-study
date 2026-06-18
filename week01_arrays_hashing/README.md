# Week 1 Day 1 — Arrays & Hashing Basics

## Concepts

### set
Use a set when I need to check whether I have seen a value before.


seen = set()

for x in nums:
    if x in seen:
        return True
    seen.add(x)


### dict counting
Use a dictionary when I need to count frequencies.

count = {}

for ch in s:
    count[ch] = count.get(ch, 0) + 1


### Counter

### Counter is a convenient way to count frequencies.
from collections import Counter
Counter(s) == Counter(t)