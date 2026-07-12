# Week 5: Data Metrics and Model Evaluation

---

## Day 1: pandas groupby + SQL aggregation

### Goal

- Practice pandas `groupby`, `agg`, `reset_index`, `sort_values`.
- Practice SQL `GROUP BY`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- Compute user-level, city-level, and channel-level metrics.

```
df.groupby("key").agg(
    metric_name=("column", "function")
).reset_index()
```
```
SELECT group_col, COUNT(*) AS n, AVG(metric) AS avg_metric
FROM table
GROUP BY group_col;
```

## Day 2: pandas merge and SQL-style joins

### Main goal

Practice how relational data tables connect to each other.

The key idea is **grain**.

* `customers`: one row = one customer
* `orders`: one row = one order
* `products`: one row = one product

After joining tables, the grain can change. For example, if one customer has multiple orders, a customer-level table joined with an order-level table becomes customer-order level.

---

## 1. pandas `merge`

### Basic left join

```python
customer_orders = customers.merge(
    orders,
    on="customer_id",
    how="left",
    indicator=True,
)
```

### What this does

* Keeps all rows from `customers`
* Adds matching order information from `orders`
* Customers with no orders remain in the result
* `_merge` shows where each row came from

Possible `_merge` values:

```text
both        matched in both tables
left_only   exists only in the left table
right_only  exists only in the right table
```

---

## 2. Anti-join in pandas

### Goal

Find customers who have no orders.

```python
no_order_customers = (
    customer_orders[customer_orders["_merge"] == "left_only"]
    [["customer_id", "customer_name", "city"]]
)
```

---

## 3. Join orders with products

### Goal

Attach product names and categories to each order.

```python
order_products = orders.merge(
    products,
    on="product_id",
    how="left",
)
```

### Expected grain

After this join:

```text
one row = one order with product information
```

---

## 4. Category-level revenue summary

### Goal

Compute revenue metrics by product category.

```python
category_summary = (
    order_products
    .groupby("category")
    .agg(
        n_orders=("order_id", "nunique"),
        total_revenue=("amount", "sum"),
        avg_order_value=("amount", "mean"),
    )
    .reset_index()
    .sort_values("total_revenue", ascending=False)
)
```

### Key functions

```python
.groupby("category")
```

Splits rows by product category.

```python
.agg(...)
```

Computes summary metrics for each group.

```python
.reset_index()
```

Turns the group key back into a normal column.

```python
.sort_values("total_revenue", ascending=False)
```

Sorts categories from highest to lowest revenue.

---

## 5. Customer-level purchase summary

### Goal

Compute order count and total spend by customer.

```python
customer_summary = (
    customer_orders
    .groupby(["customer_id", "customer_name", "city"])
    .agg(
        n_orders=("order_id", "nunique"),
        total_spend=("amount", "sum"),
    )
    .reset_index()
)
```

### Fill missing spend with 0

Customers with no orders have missing order amounts after a left join.

```python
customer_summary["total_spend"] = customer_summary["total_spend"].fillna(0)
```

### Sort customers

```python
customer_summary = customer_summary.sort_values(
    ["total_spend", "n_orders"],
    ascending=[False, False],
)
```

---

## 6. Repeat customers

### Definition

A repeat customer has at least two orders.

```python
repeat_customers = customer_summary[customer_summary["n_orders"] >= 2]
```

---

## Day 2 full main workflow

```python
def main() -> None:
    customers = build_customers()
    orders = build_orders()
    products = build_products()

    print("\n=== Customers ===")
    print(customers)

    print("\n=== Orders ===")
    print(orders)

    print("\n=== Products ===")
    print(products)

    print("\n=== Grain checks ===")
    print("customers rows:", len(customers), "| unique customers:", customers["customer_id"].nunique())
    print("orders rows:", len(orders), "| unique orders:", orders["order_id"].nunique())
    print("products rows:", len(products), "| unique products:", products["product_id"].nunique())

    customer_orders = customers.merge(
        orders,
        on="customer_id",
        how="left",
        indicator=True,
    )

    no_order_customers = (
        customer_orders[customer_orders["_merge"] == "left_only"]
        [["customer_id", "customer_name", "city"]]
    )

    print("\n=== Customer-orders left join ===")
    print(customer_orders)

    print("\n=== Customers with no orders ===")
    print(no_order_customers)

    order_products = orders.merge(
        products,
        on="product_id",
        how="left",
    )

    print("\n=== Order-products table ===")
    print(order_products)

    category_summary = (
        order_products
        .groupby("category")
        .agg(
            n_orders=("order_id", "nunique"),
            total_revenue=("amount", "sum"),
            avg_order_value=("amount", "mean"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    print("\n=== Category-level revenue summary ===")
    print(category_summary)

    customer_summary = (
        customer_orders
        .groupby(["customer_id", "customer_name", "city"])
        .agg(
            n_orders=("order_id", "nunique"),
            total_spend=("amount", "sum"),
        )
        .reset_index()
    )

    customer_summary["total_spend"] = customer_summary["total_spend"].fillna(0)

    customer_summary = customer_summary.sort_values(
        ["total_spend", "n_orders"],
        ascending=[False, False],
    )

    print("\n=== Customer-level purchase summary ===")
    print(customer_summary)

    repeat_customers = customer_summary[customer_summary["n_orders"] >= 2]

    print("\n=== Repeat customers ===")
    print(repeat_customers)
```

---

## Day 2 SQL examples

### Anti-join: customers with no orders

```sql
SELECT
    c.customer_id,
    c.customer_name,
    c.city
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

### Join orders with products

```sql
SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    p.product_name,
    p.category,
    o.amount
FROM orders o
LEFT JOIN products p
    ON o.product_id = p.product_id
ORDER BY o.order_id;
```

### Category-level revenue summary

```sql
SELECT
    p.category,
    COUNT(DISTINCT o.order_id) AS n_orders,
    SUM(o.amount) AS total_revenue,
    AVG(o.amount) AS avg_order_value
FROM orders o
LEFT JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
```

### Customer-level purchase summary

```sql
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS n_orders,
    COALESCE(SUM(o.amount), 0) AS total_spend
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spend DESC, n_orders DESC;
```

### Repeat customers

```sql
WITH customer_summary AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(DISTINCT o.order_id) AS n_orders,
        COALESCE(SUM(o.amount), 0) AS total_spend
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city
)
SELECT *
FROM customer_summary
WHERE n_orders >= 2
ORDER BY total_spend DESC, n_orders DESC;
```

---

# Day 3: Retention, conversion, and SQL window functions

## Main goal

Practice user-level metrics from event-level data.

The key idea is again **grain**.

* `events`: one row = one user event
* `experiment_assignments`: one row = one assigned user
* retention: user-level metric
* conversion: user-level metric
* experiment outcome: user-level metric

---

## 1. First event date by user

### pandas

```python
first_event = (
    events
    .groupby("user_id")["event_date"]
    .min()
    .reset_index()
    .rename(columns={"event_date": "first_event_date"})
)
```

### SQL

```sql
SELECT
    user_id,
    MIN(event_date) AS first_event_date
FROM events
GROUP BY user_id;
```

### Why this matters

The first event date is often the cohort start date.

Common examples:

```text
signup date
first visit date
first purchase date
first app open date
```

---

## 2. Days since first event

### pandas

```python
events_with_first = events.merge(
    first_event,
    on="user_id",
    how="left",
)

events_with_first["days_since_first_event"] = (
    events_with_first["event_date"] - events_with_first["first_event_date"]
).dt.days
```

### Why this matters

Retention is usually defined relative to a user’s first activity date.

Example:

```text
D1 retained = user came back exactly 1 day after first event
D7 retained = user came back exactly 7 days after first event
```

---

## 3. D1 retention

### Definition

A user is D1 retained if they have at least one event exactly one day after their first event.

### pandas

```python
user_d1 = (
    events_with_first
    .groupby("user_id")["days_since_first_event"]
    .apply(lambda x: int(1 in set(x)))
    .reset_index()
    .rename(columns={"days_since_first_event": "d1_retained"})
)

d1_retention_rate = user_d1["d1_retained"].mean()
```

### Why this works

For each user:

```text
days_since_first_event = [0, 1, 3]
```

Since `1` is present, the user is D1 retained.

---

## 4. User-level conversion

### Definition

A user is converted if they have at least one purchase event.

### pandas

```python
user_conversion = (
    events
    .assign(is_purchase=lambda df: (df["event_type"] == "purchase").astype(int))
    .groupby("user_id")["is_purchase"]
    .max()
    .reset_index()
    .rename(columns={"is_purchase": "converted"})
)
```

### SQL

```sql
SELECT
    user_id,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS converted
FROM events
GROUP BY user_id;
```

### Why `MAX` works

If a user has any purchase event:

```text
[0, 0, 1] → max = 1
```

If a user has no purchase event:

```text
[0, 0, 0] → max = 0
```

---

## 5. Conversion rate by experiment group

### pandas

```python
experiment_outcomes = assignments.merge(
    user_conversion,
    on="user_id",
    how="left",
)

experiment_outcomes["converted"] = (
    experiment_outcomes["converted"]
    .fillna(0)
    .astype(int)
)

conversion_by_group = (
    experiment_outcomes
    .groupby("treatment_group")
    .agg(
        n_users=("user_id", "nunique"),
        n_converted=("converted", "sum"),
        conversion_rate=("converted", "mean"),
    )
    .reset_index()
)
```

### Important

All assigned users should remain in the analysis.

If a user was assigned but never converted, they should count as:

```text
converted = 0
```

Do not drop them.

---

## Day 3 full main workflow

```python
def main() -> None:
    events = build_events()
    assignments = build_experiment_assignments()

    print("\n=== Events ===")
    print(events)

    print("\n=== Experiment assignments ===")
    print(assignments)

    print("\n=== Grain checks ===")
    print("event rows:", len(events), "| unique users in events:", events["user_id"].nunique())
    print("assignment rows:", len(assignments), "| unique assigned users:", assignments["user_id"].nunique())

    first_event = (
        events
        .groupby("user_id")["event_date"]
        .min()
        .reset_index()
        .rename(columns={"event_date": "first_event_date"})
    )

    print("\n=== First event date by user ===")
    print(first_event)

    events_with_first = events.merge(
        first_event,
        on="user_id",
        how="left",
    )

    events_with_first["days_since_first_event"] = (
        events_with_first["event_date"] - events_with_first["first_event_date"]
    ).dt.days

    print("\n=== Events with days since first event ===")
    print(events_with_first)

    user_d1 = (
        events_with_first
        .groupby("user_id")["days_since_first_event"]
        .apply(lambda x: int(1 in set(x)))
        .reset_index()
        .rename(columns={"days_since_first_event": "d1_retained"})
    )

    d1_retention_rate = user_d1["d1_retained"].mean()

    print("\n=== D1 retained by user ===")
    print(user_d1)

    print("\nD1 retention rate:", d1_retention_rate)

    user_conversion = (
        events
        .assign(is_purchase=lambda df: (df["event_type"] == "purchase").astype(int))
        .groupby("user_id")["is_purchase"]
        .max()
        .reset_index()
        .rename(columns={"is_purchase": "converted"})
    )

    print("\n=== User-level conversion ===")
    print(user_conversion)

    experiment_outcomes = assignments.merge(
        user_conversion,
        on="user_id",
        how="left",
    )

    experiment_outcomes["converted"] = experiment_outcomes["converted"].fillna(0).astype(int)

    conversion_by_group = (
        experiment_outcomes
        .groupby("treatment_group")
        .agg(
            n_users=("user_id", "nunique"),
            n_converted=("converted", "sum"),
            conversion_rate=("converted", "mean"),
        )
        .reset_index()
    )

    print("\n=== Experiment outcomes ===")
    print(experiment_outcomes)

    print("\n=== Conversion rate by group ===")
    print(conversion_by_group)
```

---

## Day 3 SQL examples

### First event date

```sql
SELECT
    user_id,
    MIN(event_date) AS first_event_date
FROM events
GROUP BY user_id;
```

### Add event number by user

```sql
SELECT
    user_id,
    event_date,
    event_type,
    ROW_NUMBER() OVER (
        PARTITION BY user_id
        ORDER BY event_date
    ) AS event_number
FROM events
ORDER BY user_id, event_date;
```

### D1 retention by user

```sql
WITH first_event AS (
    SELECT
        user_id,
        MIN(event_date) AS first_event_date
    FROM events
    GROUP BY user_id
),
events_with_first AS (
    SELECT
        e.user_id,
        e.event_date,
        f.first_event_date,
        julianday(e.event_date) - julianday(f.first_event_date) AS days_since_first
    FROM events e
    LEFT JOIN first_event f
        ON e.user_id = f.user_id
),
user_d1 AS (
    SELECT
        user_id,
        MAX(CASE WHEN days_since_first = 1 THEN 1 ELSE 0 END) AS d1_retained
    FROM events_with_first
    GROUP BY user_id
)
SELECT
    user_id,
    d1_retained
FROM user_d1
ORDER BY user_id;
```

### D1 retention rate

```sql
WITH first_event AS (
    SELECT
        user_id,
        MIN(event_date) AS first_event_date
    FROM events
    GROUP BY user_id
),
events_with_first AS (
    SELECT
        e.user_id,
        e.event_date,
        f.first_event_date,
        julianday(e.event_date) - julianday(f.first_event_date) AS days_since_first
    FROM events e
    LEFT JOIN first_event f
        ON e.user_id = f.user_id
),
user_d1 AS (
    SELECT
        user_id,
        MAX(CASE WHEN days_since_first = 1 THEN 1 ELSE 0 END) AS d1_retained
    FROM events_with_first
    GROUP BY user_id
)
SELECT
    AVG(d1_retained) AS d1_retention_rate
FROM user_d1;
```

### User-level conversion

```sql
SELECT
    user_id,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS converted
FROM events
GROUP BY user_id;
```

### Conversion rate by treatment group

```sql
WITH user_conversion AS (
    SELECT
        user_id,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS converted
    FROM events
    GROUP BY user_id
)
SELECT
    a.treatment_group,
    COUNT(DISTINCT a.user_id) AS n_users,
    SUM(COALESCE(u.converted, 0)) AS n_converted,
    AVG(COALESCE(u.converted, 0)) AS conversion_rate
FROM experiment_assignments a
LEFT JOIN user_conversion u
    ON a.user_id = u.user_id
GROUP BY a.treatment_group;
```

---

# Key functions and commands

## pandas

### `merge`

```python
left.merge(right, on="id", how="left")
```

Combines two DataFrames by a key.

Common join types:

```python
# Keep only matched rows
left.merge(right, on="id", how="inner")

# Keep all rows from the left table
left.merge(right, on="id", how="left")

# Add join source information
left.merge(right, on="id", how="left", indicator=True)
```

---

### `groupby`

```python
df.groupby("user_id")
```

Splits a DataFrame into groups.

Usually followed by:

```python
.agg(...)
.apply(...)
.max()
.min()
.mean()
.sum()
```

---

### `agg`

```python
df.groupby("group_col").agg(
    new_col=("source_col", "function")
)
```

Creates named summary columns.

Example:

```python
summary = (
    df.groupby("city")
    .agg(
        n_users=("user_id", "nunique"),
        total_revenue=("amount", "sum"),
    )
    .reset_index()
)
```

---

### `fillna`

```python
df["converted"] = df["converted"].fillna(0)
```

Replaces missing values.

Common use case:

```text
After a left join, users with no event/purchase/order may have missing values.
Those values often need to become 0.
```

---

### `.dt.days`

```python
df["days"] = (df["event_date"] - df["first_event_date"]).dt.days
```

Converts date differences into integer day counts.

---

### `.assign`

```python
df.assign(is_purchase=lambda df: (df["event_type"] == "purchase").astype(int))
```

Creates a new column inside a method chain.

---

## SQL

### `LEFT JOIN`

```sql
SELECT *
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id;
```

Keeps every row from the left table.

---

### Anti-join

```sql
SELECT c.*
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

Finds rows that exist in the left table but not in the right table.

---

### `COALESCE`

```sql
COALESCE(SUM(amount), 0)
```

Replaces `NULL` with a fallback value.

---

### `CASE WHEN`

```sql
CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END
```

Creates a conditional indicator.

---

### `ROW_NUMBER`

```sql
ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY event_date
)
```

Assigns row order within each user group.

---

### `julianday`

```sql
julianday(event_date) - julianday(first_event_date)
```

Computes date differences in SQLite.

---

# Reflection questions

## Day 2

1. What is the grain of `customers`?
2. What is the grain of `orders`?
3. What is the grain after joining `customers` and `orders`?
4. Why does the row count increase after a one-to-many join?
5. How do you find customers with no orders?
6. Why should missing total spend become 0?

## Day 3

1. Why is retention a user-level metric?
2. Why is conversion usually computed after converting event-level data to user-level data?
3. Why should all assigned users remain in experiment analysis?
4. What does `ROW_NUMBER()` do?
5. What is the difference between event-level conversion and user-level conversion?
6. Why can `AVG(converted)` be interpreted as conversion rate?

---

# Practice questions

## Day 2 practice

### LeetCode SQL

* Customers Who Visited but Did Not Make Any Transactions
* Product Sales Analysis I
* Replace Employee ID With The Unique Identifier
* Employee Bonus
* Students and Examinations
* Managers with at Least 5 Direct Reports

### LeetCode Pandas

* Customers Who Never Order
* Product Sales Analysis I
* Replace Employee ID With The Unique Identifier
* Sales Person

### HackerRank SQL

* African Cities
* Average Population of Each Continent
* The Report

---

## Day 3 practice

### LeetCode SQL

* Confirmation Rate
* Game Play Analysis I
* Game Play Analysis IV
* Monthly Transactions I
* Restaurant Growth
* Department Top Three Salaries

### LeetCode Pandas

* Game Play Analysis I
* Department Highest Salary
* Rank Scores
* Group Sold Products By The Date

### Algorithm review

* Merge Intervals
* Subarray Sum Equals K
* Kth Largest Element in an Array

---

# Git commands

## Start

```powershell
cd C:\path\to\coding-study
git pull
conda activate coding-study
code .
```

## End

```powershell
git status

git add week05_data_metrics_model_eval/day02_pandas_merge_sql_join.py
git add week05_data_metrics_model_eval/day02_sql_join_anti_join.sql
git add week05_data_metrics_model_eval/day03_retention_conversion_metrics.py
git add week05_data_metrics_model_eval/day03_sql_window_functions.sql
git add week05_data_metrics_model_eval/README.md

git status

git commit -m "week5 day2 day3 joins retention conversion metrics"

git push
```
## Day 4: experiment statistics and probability simulation

### Key concepts

#### Bernoulli conversion

```python
converted = 1  # user converted
converted = 0  # user did not convert
```

For 0/1 conversion data:

```python
conversion_rate = mean(converted)
```

#### Difference in conversion rates

```python
p_control = x_control / n_control
p_treatment = x_treatment / n_treatment

diff = p_treatment - p_control
```

#### Two-proportion z-test

```python
pooled = (x_control + x_treatment) / (n_control + n_treatment)

se = math.sqrt(
    pooled * (1 - pooled) * (1 / n_control + 1 / n_treatment)
)

z = diff / se
```

#### Two-sided p-value

```python
p_value = 2 * (1 - normal_cdf(abs(z)))
```

#### Bootstrap confidence interval

```python
control_sample = [random.choice(control) for _ in range(len(control))]
treatment_sample = [random.choice(treatment) for _ in range(len(treatment))]

diff = statistics.mean(treatment_sample) - statistics.mean(control_sample)
```

### Reflection

---

## Day 5: sklearn cross-validation, GridSearchCV, and metrics

### Goal

- Build a clean sklearn modeling workflow.
- Use train/test split.
- Use Pipeline to avoid preprocessing leakage.
- Use cross-validation for model selection.
- Use GridSearchCV for hyperparameter tuning.
- Interpret classification metrics.

### Key concepts

#### Train/test split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)
```

#### Pipeline

```python
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=3000)),
])
```

Pipeline helps ensure preprocessing is fit only on training folds during cross-validation.

#### Cross-validation

```python
cv_scores = cross_val_score(
    pipe,
    X_train,
    y_train,
    cv=5,
    scoring="roc_auc",
)
```

#### GridSearchCV

```python
param_grid = {
    "model__C": [0.01, 0.1, 1.0, 10.0],
}

grid = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    scoring="roc_auc",
    cv=5,
)

grid.fit(X_train, y_train)
```

#### Final test evaluation

```python
best_model = grid.best_estimator_

pred = best_model.predict(X_test)
prob = best_model.predict_proba(X_test)[:, 1]

print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))
print(roc_auc_score(y_test, prob))
```

### Metric interpretation

```text
precision = among predicted positives, how many are truly positive?
recall = among actual positives, how many did we find?
F1 = harmonic mean of precision and recall
ROC AUC = ranking quality across thresholds
```