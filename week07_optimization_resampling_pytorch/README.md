# Week 7 Study Notes

## Day 1: Greedy Algorithms and Segment-Level Model Evaluation

---

## 1. Greedy Algorithms

A greedy algorithm makes the best available choice at the current step and does not revisit previous decisions.

A greedy solution is not simply an algorithm that sorts the input. A valid greedy solution requires a rule that can be justified as preserving at least one globally optimal solution.

### When to Consider a Greedy Approach

A greedy approach may be appropriate when:

* The problem asks for a minimum or maximum.s
* Items can be ordered by a meaningful priority.
* Each decision changes the set of future available choices.
* A local decision preserves as many future options as possible.
* A greedy choice can replace the corresponding choice in an optimal solution without making the solution worse.

---

## 2. Interval Scheduling

Interval problems contain pairs of values representing a start and an end.

```python
intervals = [
    [1, 2],
    [2, 3],
    [1, 3],
    [3, 4],
]
```

Two intervals are compatible when the second interval starts at or after the first interval ends.

```text
[1, 2] and [2, 3] are compatible.

[1, 3] and [2, 4] overlap.
```

Different interval problems require different sorting rules.

| Problem                   | Sorting Rule                  | Goal                                            |
| ------------------------- | ----------------------------- | ----------------------------------------------- |
| Merge Intervals           | Sort by start time            | Combine overlapping intervals                   |
| Non-overlapping Intervals | Sort by end time              | Keep the largest number of compatible intervals |
| Meeting Rooms II          | Sort events or use a min-heap | Track concurrent intervals                      |

---

## 3. Non-overlapping Intervals

### Problem

Given a list of intervals, return the minimum number of intervals that must be removed so that the remaining intervals do not overlap.

```text
Input:
[[1, 2], [2, 3], [3, 4], [1, 3]]

Output:
1
```

Removing `[1, 3]` leaves:

```text
[[1, 2], [2, 3], [3, 4]]
```

These intervals do not overlap.

### Greedy Rule

Sort the intervals by end time and keep the interval that finishes earliest.

```python
intervals.sort(key=lambda interval: interval[1])
```

Keeping the earliest finishing interval leaves the largest possible amount of time for later intervals.

### State

```python
previous_end
```

`previous_end` represents the end of the last interval selected for the non-overlapping solution.

### Implementation

```python
from typing import List


def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    """
    Return the minimum number of intervals that must be removed
    so the remaining intervals do not overlap.
    """

    if not intervals:
        return 0

    intervals.sort(key=lambda interval: interval[1])

    removed = 0
    previous_end = float("-inf")

    for start, end in intervals:
        if start >= previous_end:
            previous_end = end
        else:
            removed += 1

    return removed
```

### Example Simulation

```python
intervals = [
    [1, 2],
    [2, 3],
    [3, 4],
    [1, 3],
]
```

After sorting by end time:

```text
[[1, 2], [2, 3], [1, 3], [3, 4]]
```

| Current Interval | Previous End | Decision | Removed |
| ---------------- | -----------: | -------- | ------: |
| `[1, 2]`         |       `-inf` | Keep     |       0 |
| `[2, 3]`         |            2 | Keep     |       0 |
| `[1, 3]`         |            3 | Remove   |       1 |
| `[3, 4]`         |            3 | Keep     |       1 |

Result:

```python
1
```

### Complexity

```text
Sorting: O(n log n)
Scanning: O(n)
Total time: O(n log n)
Extra algorithmic space: O(1)
```

### Common Mistake

Sorting by start time is useful for merging intervals but does not directly solve the interval scheduling problem.

For non-overlapping interval selection, the important value is the ending time because it determines how much room remains for future intervals.

---

## 4. Jump Game

### Problem

Given an integer array, each value represents the maximum jump length from that position.

Return `True` if the final index is reachable from index `0`.

```text
Input:
[2, 3, 1, 1, 4]

Output:
True
```

From index `0`, it is possible to jump to index `1`, and from index `1`, the final index is reachable.

### Greedy State

```python
farthest
```

`farthest` represents the farthest index reachable using all positions processed so far.

There is no need to store every possible jump path. Only the maximum reachable boundary is needed.

### Implementation

```python
from typing import List


def can_jump(nums: List[int]) -> bool:
    """
    Return True if the final index is reachable from index zero.
    """

    if not nums:
        return False

    farthest = 0
    final_index = len(nums) - 1

    for index, jump_length in enumerate(nums):
        if index > farthest:
            return False

        farthest = max(
            farthest,
            index + jump_length,
        )

        if farthest >= final_index:
            return True

    return True
```

### Successful Example

```python
nums = [2, 3, 1, 1, 4]
```

| Index | Jump Length | Previous Farthest | New Farthest |
| ----: | ----------: | ----------------: | -----------: |
|     0 |           2 |                 0 |            2 |
|     1 |           3 |                 2 |            4 |

The final index is `4`, so the function returns `True`.

### Failed Example

```python
nums = [3, 2, 1, 0, 4]
```

| Index | Jump Length | Previous Farthest | New Farthest |
| ----: | ----------: | ----------------: | -----------: |
|     0 |           3 |                 0 |            3 |
|     1 |           2 |                 3 |            3 |
|     2 |           1 |                 3 |            3 |
|     3 |           0 |                 3 |            3 |

The next index is `4`, but:

```python
4 > farthest
```

Therefore, index `4` is unreachable.

### Complexity

```text
Time: O(n)
Space: O(1)
```

### Common Mistake

A brute-force approach tries every possible jump and produces a branching search tree.

The greedy approach does not need to know the exact path. It only needs to know whether the current index is reachable and how far the reachable boundary can be extended.

---

## 5. Review: Merge Intervals vs Non-overlapping Intervals

### Merge Intervals

Sort by start time.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    intervals.sort(key=lambda interval: interval[0])

    merged = []

    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(
                merged[-1][1],
                end,
            )

    return merged
```

The goal is to process intervals in chronological starting order and extend the most recently merged interval when an overlap occurs.

### Non-overlapping Intervals

Sort by end time.

```python
intervals.sort(key=lambda interval: interval[1])
```

The goal is to keep the interval that finishes earliest so that future intervals have the greatest chance of remaining compatible.

---

## 6. Python Sorting Patterns

### `list.sort()`

`list.sort()` modifies the original list.

```python
values = [3, 1, 2]

values.sort()

print(values)
```

Output:

```text
[1, 2, 3]
```

It returns `None`.

```python
result = values.sort()

print(result)
```

Output:

```text
None
```

### `sorted()`

`sorted()` returns a new list and preserves the original iterable.

```python
values = [3, 1, 2]

sorted_values = sorted(values)

print(values)
print(sorted_values)
```

Output:

```text
[3, 1, 2]
[1, 2, 3]
```

### The `key` Argument

The `key` function receives one element and returns the value used for comparison.

Sort intervals by start time:

```python
intervals.sort(
    key=lambda interval: interval[0],
)
```

Sort intervals by end time:

```python
intervals.sort(
    key=lambda interval: interval[1],
)
```

The following lambda:

```python
lambda interval: interval[1]
```

is equivalent to:

```python
def get_end(interval):
    return interval[1]
```

### Multiple Sorting Conditions

Sort by descending score and then ascending name:

```python
items = [
    ("A", 10),
    ("C", 8),
    ("B", 10),
]

items.sort(
    key=lambda item: (-item[1], item[0]),
)
```

Result:

```text
[("A", 10), ("B", 10), ("C", 8)]
```

---

## 7. Segment-Level Model Evaluation

An overall model metric can hide poor performance in an important subgroup.

Examples of useful grouping columns include:

```text
- customer segment
- geographic region
- device type
- time period
- product category
- experiment cohort
- hospital or research site
```

Subgroup evaluation should begin by checking the row grain.

```text
Is one row:

- one user?
- one event?
- one transaction?
- one prediction?
```

Metrics should normally be computed at the same unit at which predictions and decisions are made.

---

## 8. Classification Metrics

For binary classification:

```text
TP: true positive
TN: true negative
FP: false positive
FN: false negative
```

### Accuracy

```text
Accuracy = (TP + TN) / Total
```

Accuracy measures the overall fraction of correct predictions.

### Precision

```text
Precision = TP / (TP + FP)
```

Precision answers:

```text
Among predicted positives, how many were actually positive?
```

### Recall

```text
Recall = TP / (TP + FN)
```

Recall answers:

```text
Among actual positives, how many were identified?
```

### F1 Score

```text
F1 = 2 × Precision × Recall / (Precision + Recall)
```

F1 is the harmonic mean of precision and recall.

---

## 9. Python Implementation: Metrics by Group

```python
from typing import List, Dict, Any

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


def summarize_by_group(
    results: pd.DataFrame,
    group_col: str,
) -> pd.DataFrame:
    """
    Compute classification metrics separately for each group.
    """

    required_columns = {
        group_col,
        "y_true",
        "y_pred",
    }

    missing_columns = required_columns - set(results.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    summaries = []

    for group_value, group_frame in results.groupby(
        group_col,
        dropna=False,
        sort=True,
    ):
        y_true = group_frame["y_true"]
        y_pred = group_frame["y_pred"]

        summaries.append({
            group_col: group_value,
            "n": len(group_frame),
            "positive_rate": y_true.mean(),
            "predicted_positive_rate": y_pred.mean(),
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
            "recall": recall_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
            "f1": f1_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
        })

    return pd.DataFrame(summaries)
```

### Example Data

```python
data: Dict[str, List[Any]] = {
    "segment": [
        "A", "A", "A", "A",
        "B", "B", "B", "B",
        "C", "C",
    ],
    "y_true": [
        1, 1, 0, 0,
        1, 1, 1, 0,
        0, 0,
    ],
    "y_pred": [
        1, 0, 1, 0,
        1, 1, 0, 0,
        0, 0,
    ],
}

results = pd.DataFrame(data)

summary = summarize_by_group(
    results=results,
    group_col="segment",
)

print(summary)
```

---

## 10. Segment Metric Example

For Segment A:

| Row | `y_true` | `y_pred` | Classification |
| --: | -------: | -------: | -------------- |
|   1 |        1 |        1 | TP             |
|   2 |        1 |        0 | FN             |
|   3 |        0 |        1 | FP             |
|   4 |        0 |        0 | TN             |

Therefore:

```text
TP = 1
TN = 1
FP = 1
FN = 1
```

Metrics:

```text
Accuracy = (1 + 1) / 4 = 0.50

Precision = 1 / (1 + 1) = 0.50

Recall = 1 / (1 + 1) = 0.50

F1 = 0.50
```

---

## 11. Important `groupby` Arguments

```python
results.groupby(
    group_col,
    dropna=False,
    sort=True,
)
```

### `group_col`

The column used to separate observations into groups.

```python
results.groupby("segment")
```

### `dropna`

```python
dropna=True
```

Rows with a missing grouping value are excluded.

```python
dropna=False
```

Missing grouping values are retained as their own group.

### `sort`

```python
sort=True
```

Group keys are returned in sorted order.

```python
sort=False
```

Group keys follow their observed order, which may be faster for large data.

---

## 12. The `zero_division` Argument

A group may have no predicted positive observations.

In that case:

```text
TP + FP = 0
```

Precision would be undefined.

```python
precision_score(
    y_true,
    y_pred,
    zero_division=0,
)
```

`zero_division=0` returns `0` instead of producing an undefined metric warning.

This is useful for automated group summaries, but the result must still be interpreted carefully. A value of zero may mean that the model never predicted the positive class in that group.

---

## 13. SQL Implementation: Metrics by Group

Assume a table named `model_results`.

```text
model_results

segment
y_true
y_pred
```

```sql
WITH confusion_counts AS (
    SELECT
        segment,
        COUNT(*) AS n,
        SUM(
            CASE
                WHEN y_true = 1 AND y_pred = 1 THEN 1
                ELSE 0
            END
        ) AS tp,
        SUM(
            CASE
                WHEN y_true = 0 AND y_pred = 0 THEN 1
                ELSE 0
            END
        ) AS tn,
        SUM(
            CASE
                WHEN y_true = 0 AND y_pred = 1 THEN 1
                ELSE 0
            END
        ) AS fp,
        SUM(
            CASE
                WHEN y_true = 1 AND y_pred = 0 THEN 1
                ELSE 0
            END
        ) AS fn
    FROM model_results
    GROUP BY segment
),
metrics AS (
    SELECT
        segment,
        n,
        1.0 * (tp + tn) / NULLIF(n, 0) AS accuracy,
        1.0 * tp / NULLIF(tp + fp, 0) AS precision,
        1.0 * tp / NULLIF(tp + fn, 0) AS recall
    FROM confusion_counts
)
SELECT
    segment,
    n,
    accuracy,
    precision,
    recall,
    2.0 * precision * recall
        / NULLIF(precision + recall, 0) AS f1
FROM metrics
ORDER BY segment;
```

### `CASE WHEN`

`CASE WHEN` creates row-level indicator values.

```sql
CASE
    WHEN y_true = 1 AND y_pred = 1 THEN 1
    ELSE 0
END
```

Summing the indicator counts true positives.

### `NULLIF`

```sql
NULLIF(tp + fp, 0)
```

If the denominator is zero, `NULLIF` returns `NULL` and avoids a division-by-zero error.

### Floating-Point Division

```sql
1.0 * tp / NULLIF(tp + fp, 0)
```

Multiplying by `1.0` prevents integer division in database systems where division between integers returns an integer.

---

## 14. Interpreting Subgroup Results

A subgroup metric difference is a diagnostic signal, not an automatic causal conclusion.

Before interpreting a difference, check:

```text
- group sample size
- positive-class prevalence
- prediction rate
- label quality
- missing-data rate
- threshold choice
- data collection period
- distribution shift
```

A group with only a few observations may have unstable precision or recall.

A group with no positive cases cannot provide an informative estimate of recall.

A group with a different positive prevalence may naturally have a different precision even when ranking performance is similar.

---

## 15. Core Patterns to Retain

### Interval Scheduling

```python
intervals.sort(key=lambda interval: interval[1])

previous_end = float("-inf")

for start, end in intervals:
    if start >= previous_end:
        previous_end = end
    else:
        removed += 1
```

Use when:

```text
- intervals are unweighted
- the goal is to maximize compatible intervals
- or minimize removals
```

### Reachability Boundary

```python
farthest = 0

for index, jump_length in enumerate(nums):
    if index > farthest:
        return False

    farthest = max(
        farthest,
        index + jump_length,
    )
```

Use when:

```text
- exact paths are not required
- only the reachable range matters
- each reachable position can extend the boundary
```

### Group-Level Evaluation

```python
for group_value, group_frame in results.groupby(group_col):
    ...
```

Use when:

```text
- overall performance may hide heterogeneous behavior
- decisions affect identifiable operational segments
- model monitoring requires segment-level diagnostics
```

## Days 2–3: Dynamic Programming, Model Diagnosis, and Statistical Resampling

### One-Dimensional Dynamic Programming

Dynamic programming is useful when a problem contains overlapping subproblems and the solution to a larger state can be expressed using smaller states.

Before coding, define:

* the meaning of the state,
* the transition,
* the base case,
* and the final state to return.

For House Robber, the decision at each house is to either take the current value and combine it with the best result two positions back, or skip the current value and keep the best previous result.

```python
def rob(nums: list[int]) -> int:
    prev_two = 0
    prev_one = 0

    for money in nums:
        current = max(
            prev_two + money,
            prev_one,
        )

        prev_two = prev_one
        prev_one = current

    return prev_one
```

For Coin Change, `dp[value]` stores the minimum number of coins required to create `value`.

```python
def coin_change(coins: list[int], amount: int) -> int:
    unreachable = amount + 1

    dp = [unreachable] * (amount + 1)
    dp[0] = 0

    for current_amount in range(1, amount + 1):
        for coin in coins:
            if coin <= current_amount:
                dp[current_amount] = min(
                    dp[current_amount],
                    dp[current_amount - coin] + 1,
                )

    return -1 if dp[amount] == unreachable else dp[amount]
```

The House Robber solution uses constant memory because the current state only depends on the previous two states. Coin Change requires a table because each amount may depend on several earlier amounts.

### Learning Curves and Model Diagnosis

A learning curve compares training and validation performance over different training-set sizes.

```python
train_sizes, train_scores, validation_scores = learning_curve(
    estimator=model,
    X=X,
    y=y,
    train_sizes=np.linspace(0.2, 1.0, 5),
    cv=cv,
    scoring="roc_auc",
)
```

When training and validation scores are both low, the model may be underfitting. When the training score is high but the validation score is substantially lower, the model may be overfitting. If the validation score continues to improve as the training size increases, additional data may improve generalization.

Preprocessing must remain inside a Pipeline so that each cross-validation training fold fits its own preprocessing parameters.

### Bootstrap, Permutation Tests, and Power

Bootstrap resampling estimates uncertainty by repeatedly drawing observations from the original sample with replacement.

```python
sample = rng.choice(
    data,
    size=len(data),
    replace=True,
)
```

A bootstrap distribution can be used to estimate a standard error or confidence interval for a statistic.

A permutation test evaluates a null hypothesis by repeatedly rearranging group assignments and comparing the observed statistic with the resulting null distribution.

```python
result = permutation_test(
    data=(control, treatment),
    statistic=mean_difference,
    permutation_type="independent",
    alternative="two-sided",
)
```

Bootstrap and permutation tests serve different purposes:

* bootstrap estimates sampling uncertainty,
* permutation tests evaluate a null hypothesis,
* and power analysis estimates the sample size needed to detect a specified effect.

Power depends on the effect size, sample size, significance level, variability, and study design. Smaller target effects generally require larger samples.

For independent A/B-test groups, the resampling unit and analysis unit must match the unit of randomization. Repeated observations from the same user should not be treated as independent users without an appropriate clustered or user-level analysis.
