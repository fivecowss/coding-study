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

## Nested Cross-Validation and Model Diagnostics

Nested cross-validation separates hyperparameter selection from performance estimation.

* The inner CV loop selects hyperparameters.
* The outer CV loop evaluates the complete model-selection procedure.
* A final held-out test set should remain untouched until modeling decisions are complete.

```python
inner_cv = StratifiedKFold(
    n_splits=4,
    shuffle=True,
    random_state=42,
)

outer_cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=43,
)

search = GridSearchCV(
    estimator=model,
    param_grid={
        "classifier__C": [
            0.01,
            0.1,
            1.0,
            10.0,
        ],
    },
    scoring="roc_auc",
    cv=inner_cv,
)

nested_scores = cross_val_score(
    estimator=search,
    X=X,
    y=y,
    scoring="roc_auc",
    cv=outer_cv,
)
```

### Subgroup Diagnostics

Overall model performance can hide poor performance in individual subgroups.

Useful subgroup summaries include:

* sample size
* target prevalence
* precision
* recall
* F1
* mean predicted probability

```python
for group, frame in results.groupby(
    "acquisition_channel",
    dropna=False,
):
    row = {
        "group": group,
        "n": len(frame),
        "positive_rate": frame["y_true"].mean(),
        "precision": precision_score(
            frame["y_true"],
            frame["y_pred"],
            zero_division=0,
        ),
        "recall": recall_score(
            frame["y_true"],
            frame["y_pred"],
            zero_division=0,
        ),
        "f1": f1_score(
            frame["y_true"],
            frame["y_pred"],
            zero_division=0,
        ),
    }
```

## SQL Window Functions

Window functions retain the original rows while computing statistics over related rows.

```sql
SELECT
    user_id,
    order_date,
    amount,

    ROW_NUMBER() OVER (
        PARTITION BY user_id
        ORDER BY order_date
    ) AS order_number,

    LAG(amount) OVER (
        PARTITION BY user_id
        ORDER BY order_date
    ) AS previous_amount,

    AVG(amount) OVER (
        PARTITION BY user_id
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING
                 AND CURRENT ROW
    ) AS rolling_3_order_mean

FROM orders;
```

`ROW_NUMBER` assigns a unique sequential number within a partition.

`RANK` assigns equal ranks to ties and leaves gaps.

`DENSE_RANK` assigns equal ranks to ties without leaving gaps.

`LAG` retrieves a value from a previous row in the ordered partition.

## Inference Contract

Training and inference should use the same preprocessing pipeline.

```python
def predict_records(
    model,
    records,
    threshold=0.5,
):
    if not 0 <= threshold <= 1:
        raise ValueError(
            "threshold must be between 0 and 1"
        )

    frame = pd.DataFrame(records)

    probabilities = (
        model.predict_proba(frame)[:, 1]
    )

    predictions = (
        probabilities >= threshold
    ).astype(int)

    return pd.DataFrame({
        "probability": probabilities,
        "prediction": predictions,
    })
```

A prediction output should have a stable contract, including well-defined columns, valid probabilities, and deterministic threshold behavior.

## Unit Testing

Unit tests verify behavior of data-processing and inference functions independently of overall model accuracy.

```python
def test_invalid_threshold_raises():
    with pytest.raises(
        ValueError,
    ):
        validate_threshold(1.5)
```

```python
def test_prediction_probability_range():
    result = predict_records(
        model,
        records,
    )

    assert result[
        "probability"
    ].between(
        0,
        1,
    ).all()
```

Tests are especially useful for:

* invalid inputs
* missing values
* unseen categories
* feature-schema changes
* output contracts
* save/load consistency

## Model Persistence

A fitted preprocessing pipeline and estimator can be persisted together.

```python
from pathlib import Path
import joblib

model_path = Path(
    "models/pipeline.joblib"
)

model_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

joblib.dump(
    model,
    model_path,
)

restored_model = joblib.load(
    model_path
)
```

Persisting the entire Pipeline preserves both the preprocessing parameters and the fitted estimator.

Prediction consistency can be verified after loading:

```python
before = model.predict_proba(
    X_test
)[:, 1]

after = restored_model.predict_proba(
    X_test
)[:, 1]

assert np.allclose(
    before,
    after,
)
```

Pickle-based model artifacts such as joblib files should only be loaded from trusted sources.

## End-to-End Model Selection

A complete applied ML workflow should separate model development from final evaluation.

```text
feature table
→ development / final-test split
→ cross-validation
→ model selection
→ fit selected model on development data
→ final test evaluation
→ subgroup analysis
→ model persistence
```

The final test set should not be used to select the model.

## Multi-Metric Cross-Validation

```python
scoring = {
    "roc_auc": "roc_auc",
    "f1": "f1",
}

scores = cross_validate(
    estimator=model,
    X=X_dev,
    y=y_dev,
    cv=cv,
    scoring=scoring,
)

mean_auc = (
    scores["test_roc_auc"].mean()
)

sd_auc = (
    scores["test_roc_auc"].std()
)

mean_f1 = (
    scores["test_f1"].mean()
)
```

Compare both average validation performance and variability across folds.

## Candidate Model Comparison

A simple baseline can be compared with a more flexible model.

```python
models = {
    "logistic": logistic_pipeline,

    "random_forest": Pipeline([
        (
            "preprocess",
            preprocessor,
        ),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                min_samples_leaf=3,
                random_state=42,
            ),
        ),
    ]),
}
```

Logistic Regression provides a strong linear baseline.

Random Forest allows nonlinear effects and feature interactions.

## Final Test Evaluation

```python
predictions = model.predict(
    X_test
)

probabilities = (
    model.predict_proba(
        X_test
    )[:, 1]
)

print(
    classification_report(
        y_test,
        predictions,
    )
)

test_auc = roc_auc_score(
    y_test,
    probabilities,
)
```

Use probability scores for ROC AUC rather than thresholded class predictions.

## Subgroup Diagnostics

Overall metrics can hide failure in important subgroups.

```python
results = pd.DataFrame({
    "group":
        X_test[
            "acquisition_channel"
        ].reset_index(drop=True),

    "y_true":
        y_test.reset_index(drop=True),

    "y_pred":
        predictions,

    "y_prob":
        probabilities,
})
```

Useful subgroup summaries include:

```python
group_summary = {
    "n": len(group_frame),

    "positive_rate":
        group_frame[
            "y_true"
        ].mean(),

    "precision":
        precision_score(
            group_frame["y_true"],
            group_frame["y_pred"],
            zero_division=0,
        ),

    "recall":
        recall_score(
            group_frame["y_true"],
            group_frame["y_pred"],
            zero_division=0,
        ),

    "f1":
        f1_score(
            group_frame["y_true"],
            group_frame["y_pred"],
            zero_division=0,
        ),
}
```

Always interpret subgroup metrics together with sample size and target prevalence.

## SQL Feature Aggregation

A prediction feature table should preserve the target population and use only historical data available at prediction time.

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
        COUNT(DISTINCT order_id)
            AS n_orders,
        SUM(amount)
            AS total_amount,
        AVG(amount)
            AS avg_amount,
        MAX(order_date)
            AS last_order_date
    FROM eligible_orders
    GROUP BY user_id
)

SELECT
    u.user_id,
    COALESCE(
        f.n_orders,
        0
    ) AS n_orders,
    COALESCE(
        f.total_amount,
        0.0
    ) AS total_amount,
    f.avg_amount,
    DATE '2026-01-31'
        - f.last_order_date
        AS days_since_last_order
FROM users AS u
LEFT JOIN order_features AS f
    ON u.user_id = f.user_id;
```

## Cross-Language Aggregation

The same grouped analysis can be expressed in pandas, SQL, and R.

```python
summary = (
    frame.groupby(
        "acquisition_channel"
    )
    .agg(
        n_users=(
            "user_id",
            "nunique",
        ),
        conversion_rate=(
            "target",
            "mean",
        ),
        avg_amount=(
            "total_amount",
            "mean",
        ),
    )
    .reset_index()
)
```

```sql
SELECT
    acquisition_channel,
    COUNT(DISTINCT user_id)
        AS n_users,
    AVG(target)
        AS conversion_rate,
    AVG(total_amount)
        AS avg_amount
FROM feature_table
GROUP BY acquisition_channel;
```

```r
summary <- frame |>
  summarise(
    n_users =
      n_distinct(user_id),

    conversion_rate =
      mean(target),

    avg_amount =
      mean(total_amount),

    .by =
      acquisition_channel
  )
```

## Model Persistence

Persist the complete fitted Pipeline so preprocessing and model parameters remain together.

```python
joblib.dump(
    final_model,
    model_path,
)

restored_model = joblib.load(
    model_path
)
```

Verify prediction consistency:

```python
before = (
    final_model.predict_proba(
        X_test
    )[:, 1]
)

after = (
    restored_model.predict_proba(
        X_test
    )[:, 1]
)

assert np.allclose(
    before,
    after,
)
```

A persisted model should be accompanied by compatible code, dependencies, feature definitions, and evaluation information.
````
