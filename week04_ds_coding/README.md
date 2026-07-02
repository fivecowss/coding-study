# Week 4: DS Coding Catch-up

## Day 1: Pandas Filtering, GroupBy, SQL Basics

### Goals

- Use pandas to filter rows.
- Select specific columns.
- Add derived columns.
- Group rows and compute aggregate summaries.
- Translate pandas filtering/groupby into SQL SELECT/WHERE/GROUP BY.
- Review Week 1 hash-map problems.

---


### New pandas concepts

| Concept | Syntax | Meaning |
|---|---|---|
| Create DataFrame | `pd.DataFrame({...})` | Create a tabular dataset |
| Boolean filtering | `df[df["active"]]` | Keep rows where condition is True |
| Multiple conditions | `df[(cond1) & (cond2)]` | Keep rows satisfying both conditions |
| Select columns | `df[["a", "b"]]` | Return selected columns |
| Add column | `df.assign(new_col=...)` | Create a derived column |
| Group by | `df.groupby("country")` | Split rows into groups |
| Aggregation | `.agg(total=("x", "sum"))` | Compute summary statistics |
| Reset index | `.reset_index()` | Convert group index into regular column |
| Sort rows | `.sort_values("x", ascending=False)` | Sort by column |

---

## Day 1 SQL File



### SQL concepts

| Concept | Syntax | Meaning |
|---|---|---|
| Select columns | `SELECT col1, col2` | Choose output columns |
| Filter rows | `WHERE condition` | Keep rows before grouping |
| Sort rows | `ORDER BY col DESC` | Sort output |
| Group rows | `GROUP BY col` | Aggregate by group |
| Aggregate | `SUM`, `AVG`, `COUNT` | Compute summary statistics |
| Filter groups | `HAVING condition` | Keep groups after aggregation |

### SQL execution order

Logical order:

```sql
FROM
WHERE
GROUP BY
HAVING
SELECT
ORDER BY
```

Important distinction:

```sql
WHERE revenue >= 100
```

filters individual rows before grouping.

```sql
HAVING SUM(revenue) >= 100
```

filters groups after aggregation.

---

## Day 1 Simulation Example

Dataset:

| user_id | country | revenue | active | sessions |
|---:|---|---:|---|---:|
| 1 | US | 100 | True | 3 |
| 2 | US | 200 | True | 5 |
| 3 | KR | 150 | False | 2 |
| 4 | KR | 80 | True | 4 |
| 5 | US | 50 | False | 1 |
| 6 | KR | 120 | True | 6 |

Task:

```python
df[(df["active"]) & (df["revenue"] >= 100)]
```

Step-by-step:

1. Check `active`.
   - user 1: True
   - user 2: True
   - user 3: False
   - user 4: True
   - user 5: False
   - user 6: True

2. Check `revenue >= 100`.
   - user 1: 100 >= 100, True
   - user 2: 200 >= 100, True
   - user 4: 80 >= 100, False
   - user 6: 120 >= 100, True

3. Keep rows satisfying both:
   - user 1
   - user 2
   - user 6

---

## Day 1 Required Problems

### P0: Must solve

| Platform | Problem | Type | Difficulty |
|---|---|---|---|
| LeetCode Pandas | Big Countries | Filtering | Easy |
| LeetCode Pandas | Recyclable and Low Fat Products | Multiple conditions | Easy |
| LeetCode Pandas | Customers Who Never Order | Anti-join intro | Easy |
| LeetCode SQL 50 | Big Countries | SQL filtering | Easy |
| LeetCode SQL 50 | Recyclable and Low Fat Products | SQL WHERE | Easy |

### P1: If time allows

| Platform | Problem | Type | Difficulty |
|---|---|---|---|
| LeetCode Pandas | Article Views I | Filtering + distinct | Easy |
| LeetCode Pandas | Invalid Tweets | String length filtering | Easy |
| HackerRank SQL | Revising the Select Query I | SQL basics | Easy |
| HackerRank SQL | Select All | SQL basics | Easy |

### Algorithm review

| Problem | Pattern | Difficulty |
|---|---|---|
| Two Sum | Hash map | Easy |
| Group Anagrams | Hash map + grouping | Medium |

---

# Day 2: Sorting, Heap, Top-K, Pandas Merge, SQL Join

## Goals

- Use `sorted` with `key`.
- Use `Counter` for frequency counting.
- Use `heapq` for kth largest and top-k problems.
- Understand pandas `merge`.
- Translate pandas merge into SQL joins.
- Practice anti-join patterns.

---

## Day 2 New Python Concepts

### Sorting

```python
sorted(items, key=lambda x: x[1])
```

Meaning:
- Sort items by the second element.

Example:

```python
items = [("a", 3), ("b", 1), ("c", 2)]
```

Output:

```python
[("b", 1), ("c", 2), ("a", 3)]
```

### Tie-breaking

```python
sorted(items, key=lambda x: (-x[1], x[0]))
```

Meaning:
- Sort count descending.
- If count ties, sort name ascending.

### Counter

```python
from collections import Counter

freq = Counter(nums)
```

Meaning:
- Count how often each value appears.

Example:

```python
nums = [1, 1, 1, 2, 2, 3]
```

Output:

```python
Counter({1: 3, 2: 2, 3: 1})
```

### heapq

```python
import heapq

heapq.heappush(heap, x)
heapq.heappop(heap)
```

Meaning:
- Python heapq is a min-heap.
- The smallest element is always at `heap[0]`.

---

## Day 2 Simulation Example: Kth Largest

Input:

```python
nums = [3, 2, 1, 5, 6, 4]
k = 2
```

Goal:
- Return the 2nd largest element.

Process:
- Keep a min-heap of size 2.

Step-by-step:

```text
push 3
heap = [3]

push 2
heap = [2, 3]

push 1
heap = [1, 3, 2]
size > 2, pop 1
heap = [2, 3]

push 5
heap = [2, 3, 5]
size > 2, pop 2
heap = [3, 5]

push 6
heap = [3, 5, 6]
size > 2, pop 3
heap = [5, 6]

push 4
heap = [4, 6, 5]
size > 2, pop 4
heap = [5, 6]
```

Final:

```python
heap[0] == 5
```

So the 2nd largest element is 5.

---

## Day 2 Pandas Merge Concepts

### Left join

```python
customers.merge(orders, on="customer_id", how="left")
```

Meaning:
- Keep all customers.
- Attach matching orders.
- If no order exists, order columns become missing values.

### Inner join

```python
customers.merge(orders, on="customer_id", how="inner")
```

Meaning:
- Keep only customers with matching orders.

### Anti-join

Pattern:

```python
joined = customers.merge(orders, on="customer_id", how="left")
joined[joined["order_id"].isna()]
```

Meaning:
- Find rows in the left table with no match in the right table.

---

## Day 2 SQL File


### SQL join patterns

```sql
SELECT *
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id;
```

```sql
SELECT *
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id;
```

```sql
SELECT c.customer_id, c.name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

---

## Day 2 Required Problems

### P0: Must solve

| Platform | Problem | Pattern | Difficulty |
|---|---|---|---|
| LeetCode / NeetCode | Kth Largest Element in an Array | Heap / top-k | Medium |
| LeetCode / NeetCode | Top K Frequent Elements | Counter + sorting/heap | Medium |
| LeetCode Pandas | Customers Who Never Order | Anti-join | Easy |
| LeetCode SQL 50 | Customer Who Visited but Did Not Make Any Transactions | LEFT JOIN + NULL | Easy/Medium |
| LeetCode SQL 50 | Product Sales Analysis I | JOIN | Easy |

### P1: If time allows

| Platform | Problem | Pattern | Difficulty |
|---|---|---|---|
| LeetCode | Sort Colors | Sorting / counting / two pointers | Medium |
| LeetCode / NeetCode | K Closest Points to Origin | Heap / sorting | Medium |
| LeetCode | Last Stone Weight | Heap simulation | Easy |
| LeetCode Pandas | Replace Employee ID With The Unique Identifier | Merge/join | Easy |
| HackerRank SQL | African Cities | JOIN | Easy |

---

# Common Mistakes

## Pandas

### Mistake 1: using `and` instead of `&`

Wrong:

```python
df[(df["active"]) and (df["revenue"] >= 100)]
```

Correct:

```python
df[(df["active"]) & (df["revenue"] >= 100)]
```

### Mistake 2: forgetting parentheses

Wrong:

```python
df[df["active"] & df["revenue"] >= 100]
```

Correct:

```python
df[(df["active"]) & (df["revenue"] >= 100)]
```

---

## SQL

### Mistake 1: using WHERE instead of HAVING after aggregation

Wrong:

```sql
SELECT country, SUM(revenue)
FROM users
GROUP BY country
WHERE SUM(revenue) >= 100;
```

Correct:

```sql
SELECT country, SUM(revenue)
FROM users
GROUP BY country
HAVING SUM(revenue) >= 100;
```

### Mistake 2: using COUNT(*) after LEFT JOIN

If you want to count actual orders, use:

```sql
COUNT(o.order_id)
```

not:

```sql
COUNT(*)
```

because `COUNT(*)` also counts the left-table row with NULL order columns.

---

## Python Sorting / Heap

### Mistake 1: forgetting that heapq is a min-heap

For kth largest:
- Keep min-heap of size k.
- Pop smallest when size exceeds k.
- heap[0] is kth largest.

### Mistake 2: sorting in the wrong direction

For top frequency descending:

```python
sorted(freq.items(), key=lambda x: x[1], reverse=True)
```

or:

```python
sorted(freq.items(), key=lambda x: -x[1])
```

## Day 3: Intervals and Greedy

### Interval Sorting

Intervals are usually represented as:

```python
[start, end]
```

Common first step:

```python
intervals.sort(key=lambda x: x[0])
```

This sorts intervals by start time.

For some greedy problems, sorting by end time is better:

```python
intervals.sort(key=lambda x: x[1])
```

---

### Merge Intervals Pattern

Use this pattern when overlapping intervals should be combined.

```python
intervals.sort(key=lambda x: x[0])
merged = []

for start, end in intervals:
    if not merged or start > merged[-1][1]:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)
```

Key logic:

```python
start <= merged[-1][1]
```

means the current interval overlaps with the previous merged interval.

Example:

```python
[[1, 3], [2, 6]]
```

Since `2 <= 3`, they overlap.

Merged result:

```python
[1, 6]
```

---

### Insert Interval Pattern

There are three cases:

1. Current interval is before new interval.
2. Current interval is after new interval.
3. Current interval overlaps with new interval.

Overlap update:

```python
new_interval = [
    min(start, new_start),
    max(end, new_end),
]
```

---

### Non-overlapping Intervals Greedy Pattern

To remove the minimum number of overlapping intervals:

1. Sort by end time.
2. Keep the interval that ends earliest.
3. Remove intervals that overlap with the current kept interval.

Why sort by end time?

The interval that ends earliest leaves the largest possible room for future intervals.

---

### Meeting Rooms Pattern

For checking whether all meetings can be attended:

```python
intervals.sort(key=lambda x: x[0])

for i in range(1, len(intervals)):
    if intervals[i][0] < intervals[i - 1][1]:
        return False
```

For minimum number of rooms:

```python
starts = sorted(start for start, end in intervals)
ends = sorted(end for start, end in intervals)
```

Use two pointers:

- If next meeting starts before earliest ending meeting, need a new room.
- Otherwise, one room becomes free.

---

### SQL Join and GroupBy Concepts

#### INNER JOIN

Keeps only matching rows from both tables.

```sql
SELECT *
FROM orders AS o
INNER JOIN customers AS c
    ON o.customer_id = c.customer_id;
```

#### LEFT JOIN

Keeps all rows from the left table.

```sql
SELECT *
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id;
```

If no matching row exists in the right table, right-table columns become `NULL`.

---

### Anti-join Pattern

Find rows in the left table with no match in the right table.

```sql
SELECT c.customer_id, c.name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

This is the SQL version of:

```python
joined = customers.merge(orders, on="customer_id", how="left")
joined[joined["order_id"].isna()]
```

---

### Conditional Aggregation

Use `CASE WHEN` inside aggregation.

```sql
SUM(
    CASE
        WHEN status = 'completed' THEN amount
        ELSE 0
    END
)
```

This is useful when filtering rows directly with `WHERE` would remove rows that should remain in the denominator or output.

---

### COUNT After LEFT JOIN

Use:

```sql
COUNT(o.order_id)
```

not always:

```sql
COUNT(*)
```

Reason:

- `COUNT(*)` counts the left-table row even when right-table columns are NULL.
- `COUNT(o.order_id)` counts only non-null matched orders.

---

## Day 4: Probability and Statistics Coding

### Monte Carlo Simulation

Monte Carlo simulation estimates probabilities by repeated random experiments.

Basic structure:

```python
count = 0

for _ in range(n_sim):
    outcome = simulate_once()

    if event_happened:
        count += 1

estimate = count / n_sim
```

As `n_sim` increases, the estimate should become more stable.

---

### Simulating a Fair Coin

Encoding:

```python
1 = heads
0 = tails
```

Simulation:

```python
coin = random.choice([0, 1])
```

Two-head event:

```python
coin1 == 1 and coin2 == 1
```

True probability:

```text
P(HH) = 1/4 = 0.25
```

---

### Simulating Dice

A fair die roll:

```python
die = random.randint(1, 6)
```

Event example:

```python
die1 + die2 >= 8
```

Conditional probability:

```text
P(A | B) = P(A and B) / P(B)
```

Simulation structure:

```python
numerator = 0
denominator = 0

if B:
    denominator += 1

    if A:
        numerator += 1

estimate = numerator / denominator
```

---

### Bernoulli Simulation

Bernoulli random variable:

```python
X = 1 with probability p
X = 0 with probability 1 - p
```

Simulation:

```python
if random.random() < p:
    x = 1
else:
    x = 0
```

Sample mean:

```python
sum(sample) / len(sample)
```

Across many repeated samples, sample means concentrate around the true probability `p`.

---

### Basic Summary Statistics

Mean:

```python
statistics.mean(data)
```

Sample variance:

```python
statistics.variance(data)
```

Population variance:

```python
statistics.pvariance(data)
```

Sample standard deviation:

```python
statistics.stdev(data)
```

Population standard deviation:

```python
statistics.pstdev(data)
```

Important distinction:

- `variance()` divides by `n - 1`.
- `pvariance()` divides by `n`.

---

### Manual Sample Variance

Formula:

```text
sum((x - mean)^2) / (n - 1)
```

Python structure:

```python
xbar = sum(data) / len(data)

squared_deviations = []

for x in data:
    squared_deviations.append((x - xbar) ** 2)

sample_variance = sum(squared_deviations) / (len(data) - 1)
```

---

### Bootstrap

Bootstrap resampling means:

1. Start with observed data.
2. Sample with replacement.
3. Each bootstrap sample has the same size as the original data.
4. Compute statistic of interest.
5. Repeat many times.

Example:

```python
sample = [random.choice(data) for _ in range(len(data))]
bootstrap_mean = statistics.mean(sample)
```

Bootstrap means can be used to approximate the uncertainty of the sample mean.

---

### Percentile Interval

Simple percentile interval:

```python
sorted_values = sorted(values)
lower_index = int(0.025 * len(values))
upper_index = int(0.975 * len(values))

interval = (
    sorted_values[lower_index],
    sorted_values[upper_index],
)
```
