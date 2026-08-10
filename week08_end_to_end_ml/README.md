# Data Contracts and Leakage-Safe Preprocessing

## 1. Data Grain

Before performing any aggregation or join, define what one row represents.

Examples:

- one row per user
- one row per order
- one row per event
- one row per user-date
- one row per experiment assignment

The primary key must match the declared row grain.

For example:

- `users`: `user_id` must be unique
- `orders`: `order_id` must be unique
- `feature_table`: `user_id` must be unique

`orders.user_id` does not need to be unique because one user may place multiple orders.

## 2. Data Contract Checks

A minimum data contract should specify:

- required columns
- primary key
- null constraints
- expected types
- prediction cutoff
- expected output grain

```python
def validate_required_columns(
    df,
    required_columns,
    table_name,
):
    required = set(required_columns)
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"{table_name}: missing columns: "
            f"{sorted(missing)}"
        )
```

```python
def validate_unique_key(
    df,
    key_columns,
    table_name,
):
    duplicated = df.duplicated(
        subset=key_columns,
        keep=False,
    )

    if duplicated.any():
        raise ValueError(
            f"{table_name}: duplicate key"
        )
```

## 3. Prediction Cutoff

Features must contain only information available at prediction time.

```python
def filter_orders_at_cutoff(
    orders,
    cutoff_date,
):
    frame = orders.copy()

    frame["order_date"] = pd.to_datetime(
        frame["order_date"],
        errors="raise",
    )

    cutoff = pd.Timestamp(cutoff_date)

    return frame.loc[
        frame["order_date"] <= cutoff
    ].copy()
```

## 4. User-Level Feature Table

Start from the complete user population and left join historical aggregates.

```python
order_features = (
    eligible_orders
    .groupby(
        "user_id",
        as_index=False,
    )
    .agg(
        n_orders=("order_id", "nunique"),
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean"),
        last_order_date=("order_date", "max"),
    )
)

features = users.merge(
    order_features,
    on="user_id",
    how="left",
    validate="one_to_one",
)
```

The same logic in SQL:

```sql
WITH eligible_orders AS (
    SELECT
        order_id,
        user_id,
        order_date,
        amount
    FROM orders
    WHERE order_date <= DATE '2026-01-31'
),
order_features AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS n_orders,
        SUM(amount) AS total_amount,
        AVG(amount) AS avg_amount,
        MAX(order_date) AS last_order_date
    FROM eligible_orders
    GROUP BY user_id
)
SELECT
    u.user_id,
    COALESCE(f.n_orders, 0) AS n_orders,
    COALESCE(f.total_amount, 0.0) AS total_amount,
    f.avg_amount,
    f.last_order_date
FROM users AS u
LEFT JOIN order_features AS f
    ON u.user_id = f.user_id;
```

## 5. Fit Versus Transform

`fit` learns parameters from training data.

Examples:

- imputation median
- scaling mean and standard deviation
- one-hot category vocabulary
- model coefficients

`transform` applies already learned parameters.

Correct workflow:

```text
Training:
fit_transform

Validation and test:
transform only
```

## 6. Numeric Preprocessing

```python
numeric_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="median",
        ),
    ),
    (
        "scaler",
        StandardScaler(),
    ),
])
```

## 7. Categorical Preprocessing

```python
categorical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="most_frequent",
        ),
    ),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore",
        ),
    ),
])
```

## 8. ColumnTransformer

```python
preprocessor = ColumnTransformer([
    (
        "numeric",
        numeric_pipeline,
        numeric_features,
    ),
    (
        "categorical",
        categorical_pipeline,
        categorical_features,
    ),
])
```

## 9. Full Modeling Pipeline

```python
model = Pipeline([
    (
        "preprocess",
        preprocessor,
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=3000,
            random_state=42,
        ),
    ),
])
```

## 10. Leakage-Safe Split

```python
X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )
)

model.fit(
    X_train,
    y_train,
)
```

Never fit imputers, scalers, encoders, or feature selectors on the full dataset before the train/test split.

## 11. Prediction Outputs

```python
predictions = model.predict(
    X_test
)

probabilities = model.predict_proba(
    X_test
)[:, 1]
```

- `predict`: final class label
- `predict_proba`: class probabilities
- `[:, 1]`: probability of the positive class

## 12. Common Failure Modes

- validating the wrong key for the table grain
- losing users with no events
- including post-cutoff events
- fitting preprocessing before train/test split
- recomputing scaling statistics on test data
- failing on unseen categories
- silently changing row counts after joins
- filling every missing value with zero
- evaluating only overall metrics
- using a feature unavailable at prediction time
