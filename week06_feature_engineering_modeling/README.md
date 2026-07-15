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

