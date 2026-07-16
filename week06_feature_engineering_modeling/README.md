# Week 6 Notes: Feature Engineering and Tree-Based Modeling

## Feature Engineering

### Feature Table Grain

Before building features, identify the row unit.

Common grains:

- user-level
- order-level
- event-level
- user-date-level
- product-date-level

Wrong grain can create duplicated rows, incorrect metrics, or leakage.

Example:

```python
orders = pd.DataFrame({
    "user_id": [1, 1, 2, 2, 3],
    "order_id": [101, 102, 103, 104, 105],
    "amount": [20.0, 35.0, 15.0, 40.0, None],
})
```

This is order-level data because each row is one order.

To build user-level features:

```python
user_features = (
    orders
    .groupby("user_id")
    .agg(
        n_orders=("order_id", "nunique"),
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean"),
    )
    .reset_index()
)
```

---

## Missing Value Handling

### Numeric missing values

Common choices:

- fill with median
- fill with mean
- fill with 0
- add missing indicator
- use model-based imputation

Example:

```python
amount_median = orders["amount"].median()
orders["amount_filled"] = orders["amount"].fillna(amount_median)
```

### Categorical missing values

Common choices:

- fill with `"unknown"`
- fill with `"missing"`
- use most frequent category
- add missing indicator

Example:

```python
orders["category_filled"] = orders["category"].fillna("unknown")
```

---

## pandas groupby Pattern

Use when creating group-level features.

```python
features = (
    df
    .groupby("user_id")
    .agg(
        n_events=("event_id", "nunique"),
        total_value=("value", "sum"),
        avg_value=("value", "mean"),
        max_value=("value", "max"),
    )
    .reset_index()
)
```

Key points:

- `groupby("user_id")` splits data by user.
- `agg(...)` computes summary features.
- `reset_index()` turns the group key back into a regular column.

---

## pandas merge Pattern

Use when joining feature tables.

```python
final_features = user_features.merge(
    user_profiles,
    on="user_id",
    how="left",
)
```

Common join types:

- `inner`: keep matched rows only
- `left`: keep all rows from left table
- `right`: keep all rows from right table
- `outer`: keep all rows from both tables

Anti-join example:

```python
joined = customers.merge(
    orders,
    on="customer_id",
    how="left",
    indicator=True,
)

no_order_customers = joined[joined["_merge"] == "left_only"]
```

---

## SQL Feature Table Pattern

Use `GROUP BY` to create entity-level features.

```sql
SELECT
    user_id,
    COUNT(DISTINCT order_id) AS n_orders,
    SUM(COALESCE(amount, 0)) AS total_amount,
    AVG(amount) AS avg_amount,
    MAX(amount) AS max_amount,
    COUNT(DISTINCT COALESCE(category, 'unknown')) AS n_categories,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM orders
GROUP BY user_id;
```

Notes:

- `COALESCE(x, value)` is similar to `fillna`.
- `COUNT(DISTINCT ...)` counts unique values.
- `MIN(date)` and `MAX(date)` create first/last activity features.

---

## Tree-Based Models

### Logistic Regression vs Random Forest

Logistic Regression:

- linear decision boundary
- scaling is important
- coefficients are interpretable
- strong baseline for classification

Random Forest:

- ensemble of decision trees
- captures nonlinear interactions
- scaling is usually not required
- provides impurity-based feature importance

Example:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

logistic = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=3000)),
])

random_forest = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
)
```

---

## Model Evaluation

Use predicted probabilities for ROC AUC.

```python
prob = model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, prob)
```

Use predicted labels for classification report.

```python
pred = model.predict(X_test)
print(classification_report(y_test, pred))
```

---

## Feature Importance

### Impurity-Based Importance

```python
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": rf_model.feature_importances_,
}).sort_values("importance", ascending=False)
```

Caution:

- not causal
- can be biased toward high-cardinality features
- affected by correlated predictors

### Permutation Importance

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(
    rf_model,
    X_test,
    y_test,
    scoring="roc_auc",
    n_repeats=10,
    random_state=42,
)
```

Interpretation:

- shuffle one feature
- recompute model score
- larger score drop means the model relied more on that feature

Caution:

- still not causal
- correlated predictors can make importance harder to interpret
- depends on model, metric, and evaluation data

---

## Heap Pattern: Kth Largest

Use a min-heap of size `k`.

```python
import heapq

def find_kth_largest(nums, k):
    heap = []

    for x in nums:
        heapq.heappush(heap, x)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]
```

Why this works:

- the heap stores the largest `k` values seen so far
- the smallest among those `k` values is the kth largest overall

---

## Interval Merge Pattern

```python
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])

    merged = []

    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged
```

Use when:

- merging sessions
- combining date ranges
- detecting overlapping events
- scheduling meetings/resources

---
## Threshold Tuning, Calibration, and Imbalanced Metrics

### Predicted Probability vs Class Label

A classifier can output predicted probabilities.

```python
prob = model.predict_proba(X_test)[:, 1]
```

A threshold converts probabilities into class labels.

```python
pred = (prob >= 0.5).astype(int)
```

The default threshold is often 0.5, but it is not always the best decision threshold.

---

## Confusion Matrix

Binary classification outcomes:

```text
TP: actual 1, predicted 1
TN: actual 0, predicted 0
FP: actual 0, predicted 1
FN: actual 1, predicted 0
```

Python:

```python
from sklearn.metrics import confusion_matrix

tn, fp, fn, tp = confusion_matrix(y_true, pred).ravel()
```

---

## Precision

Precision answers:

```text
Among predicted positives, how many are truly positive?
```

Formula:

```text
precision = TP / (TP + FP)
```

Python:

```python
from sklearn.metrics import precision_score

precision = precision_score(y_true, pred)
```

Use precision when false positives are expensive.

Examples:

- fraud alert investigation
- spam detection
- candidate selection
- unnecessary medical follow-up

---

## Recall

Recall answers:

```text
Among actual positives, how many did the model find?
```

Formula:

```text
recall = TP / (TP + FN)
```

Python:

```python
from sklearn.metrics import recall_score

recall = recall_score(y_true, pred)
```

Use recall when false negatives are expensive.

Examples:

- disease screening
- fraud detection
- churn detection
- risk detection

---

## F1 Score

F1 balances precision and recall.

```text
F1 = 2 * precision * recall / (precision + recall)
```

Python:

```python
from sklearn.metrics import f1_score

f1 = f1_score(y_true, pred)
```

Use F1 when:

- classes are imbalanced
- both false positives and false negatives matter
- a single threshold-dependent metric is needed

---

## ROC AUC

ROC AUC uses predicted scores or probabilities.

```python
from sklearn.metrics import roc_auc_score

roc_auc = roc_auc_score(y_test, prob)
```

ROC AUC is threshold-independent.

It measures ranking quality rather than performance at one fixed threshold.

---

## Threshold Tuning

Evaluate several thresholds.

```python
thresholds = [0.2, 0.3, 0.5, 0.7, 0.8]

for threshold in thresholds:
    pred = (prob >= threshold).astype(int)
    precision = precision_score(y_true, pred)
    recall = recall_score(y_true, pred)
    f1 = f1_score(y_true, pred)
```

General pattern:

```text
Lower threshold:
- more predicted positives
- usually higher recall
- usually lower precision

Higher threshold:
- fewer predicted positives
- usually lower recall
- usually higher precision
```

This is not guaranteed in every tiny sample, but it is the usual tradeoff.

---

## Expected Cost

If false positives and false negatives have different costs, choose threshold by cost.

```python
def expected_cost(y_true, prob, threshold, fp_cost=1.0, fn_cost=5.0):
    pred = (prob >= threshold).astype(int)

    fp = ((pred == 1) & (y_true == 0)).sum()
    fn = ((pred == 0) & (y_true == 1)).sum()

    return fp_cost * fp + fn_cost * fn
```

Use this when:

- false negatives are more expensive than false positives
- false positives are more expensive than false negatives
- business decision cost is known

---

## Calibration

Calibration asks:

```text
When the model predicts 0.8 probability,
are about 80% of those cases truly positive?
```

Use calibrated probabilities when probabilities are used as risk scores.

```python
from sklearn.calibration import CalibratedClassifierCV

calibrated_model = CalibratedClassifierCV(
    estimator=base_model,
    method="sigmoid",
    cv=5,
)
```

Calibration matters for:

- risk scoring
- expected cost
- threshold tuning
- decision policy
- probability interpretation

---

## SQL Threshold Metrics

Given a prediction table:

```text
id | y_true | prob
```

Create threshold-level predictions:

```sql
WITH thresholds AS (
    SELECT 0.3 AS threshold
    UNION ALL SELECT 0.5
    UNION ALL SELECT 0.7
),
scored AS (
    SELECT
        t.threshold,
        p.id,
        p.y_true,
        p.prob,
        CASE
            WHEN p.prob >= t.threshold THEN 1
            ELSE 0
        END AS pred
    FROM predictions p
    CROSS JOIN thresholds t
)
SELECT *
FROM scored;
```

Compute confusion matrix:

```sql
SELECT
    threshold,
    SUM(CASE WHEN y_true = 1 AND pred = 1 THEN 1 ELSE 0 END) AS tp,
    SUM(CASE WHEN y_true = 0 AND pred = 1 THEN 1 ELSE 0 END) AS fp,
    SUM(CASE WHEN y_true = 0 AND pred = 0 THEN 1 ELSE 0 END) AS tn,
    SUM(CASE WHEN y_true = 1 AND pred = 0 THEN 1 ELSE 0 END) AS fn
FROM scored
GROUP BY threshold;
```

---

## Statistical Power Simulation

Power is the probability of detecting a real effect.

Simple simulation idea:

```python
for _ in range(n_sim):
    simulate control conversions
    simulate treatment conversions
    compute z score
    count whether abs(z) >= 1.96
```

Power increases when:

- sample size increases
- effect size increases
- noise decreases
- significance threshold is less strict

---
