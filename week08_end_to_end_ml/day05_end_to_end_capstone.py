
"""
END-TO-END CAPSTONE

Problem
-------
We have a one-row-per-customer feature table.

Goal:
Predict whether each customer will make a purchase
during the next 30 days.

We want to practice the complete modeling workflow:

1. Validate the feature table.
2. Reserve a final test set.
3. Compare candidate models using cross-validation.
4. Select a model using development data only.
5. Fit the selected model on all development data.
6. Evaluate once on the final test set.
7. Inspect subgroup performance.
8. Save and reload the complete Pipeline.
9. Verify that predictions remain unchanged.

Important:
The final test set must not be used to choose the model.
"""


from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline

from day02_preprocessing_pipeline import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET_COLUMN,
    build_model_pipeline,
    build_preprocessor,
    make_training_data,
)


def validate_feature_table(
    frame: pd.DataFrame,
) -> None:
    """
    Problem:
    Before modeling, verify that the feature table has
    the columns and target values expected by the model.

    Requirements:
    - all expected features exist
    - target exists
    - target contains only 0 and 1
    """

    # TODO
    required = (
        set(NUMERIC_FEATURES)
        | set(CATEGORICAL_FEATURES)
        | {TARGET_COLUMN}
    )

    missing = required - set(
        frame.columns
    )

    if missing:
        raise ValueError(
            "Missing required columns: "
            f"{sorted(missing)}"
        )

    target_values = set(
        frame[TARGET_COLUMN]
        .dropna()
        .unique()
    )

    if not target_values.issubset(
        {0, 1}
    ):
        raise ValueError(
            "Target must contain only 0 and 1."
        )

    if frame[
        TARGET_COLUMN
    ].isna().any():
        raise ValueError(
            "Target contains missing values."
        )

    

def build_candidate_models() -> dict[str, Pipeline]:
    """
    Problem:
    Build two candidate models that use the same
    leakage-safe preprocessing:

    1. Logistic Regression
    2. Random Forest
    """

    # TODO
    logistic = build_model_pipeline(
        numeric_features = NUMERIC_FEATURES,
        categorical_features = CATEGORICAL_FEATURES,
    )

    forest_preprocessor = (
        build_preprocessor(
            numeric_features = NUMERIC_FEATURES,
            categorical_features = CATEGORICAL_FEATURES
        )
    )

    random_forest = Pipeline(
        steps = [
            (
                "preprocess",
                forest_preprocessor,
            ),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators = 300,
                    max_depth = None,
                    min_samples_leaf = 3,
                    class_weight = "balanced",
                    random_state = 42,
                    n_jobs = -1,
                ),
            ),
        ]
    )

    return {
        "logistic_regression": logistic,
        "random_forest": random_forest,
    }


def compare_models(
    models: dict[str, Pipeline],
    X_dev: pd.DataFrame,
    y_dev: pd.Series,
) -> pd.DataFrame:
    """
    Problem:
    Compare candidate models using 5-fold CV.

    Required metrics:
    - ROC AUC
    - F1

    Return one row per model with:
    - mean_cv_roc_auc
    - sd_cv_roc_auc
    - mean_cv_f1
    """

    # TODO
    cv = StratifiedKFold(
        n_splits = 5,
        shuffle = True,
        random_state = 42,
    )

    scoring = {
        "roc_auc": "roc_auc",
        "f1": "f1",
    }

    rows = []

    for name, model in models.items():
        scores = cross_validate(
            estimator = model,
            X = X_dev,
            y = y_dev,
            cv = cv,
            scoring = scoring,
            n_jobs = -1
        )
        rows.append({
            "model": name,
            "mean_cv_roc_auc": (
                scores[
                    "test_roc_auc"
                ].std()
            ),
            "mean_cv_f1": (
                scores[
                    "test_f1"
                ].mean()
            ),
        })

    return (
        pd.DataFrame(rows)
        .sort_values(
            "mean_cv_roc_auc",
            ascending = False,
        )
        .reset_index(drop = True)
    )

def evaluate_final_model(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Problem:
    Evaluate the selected model on the untouched
    final test set.

    Print:
    - classification report
    - ROC AUC

    Return:
    - predictions
    - positive-class probabilities
    """

    # TODO
    predictions = model.predict(
        X_test
    )

    probabilities = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

    print("\nFinal test classification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division = 0,
        )
    )

    test_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    print(
        "Final test ROC AUC:",
        round(test_auc, 4)
    )

    return (
        predictions,
        probabilities
    )


def subgroup_diagnostics(
    X_test: pd.DataFrame,
    y_test: pd.Series,
    predictions: np.ndarray,
    probabilities: np.ndarray,
    group_column: str,
) -> pd.DataFrame:
    """
    Problem:
    Overall metrics may hide poor performance for
    particular user segments.

    Calculate per-group:
    - n
    - positive rate
    - precision
    - recall
    - F1
    - mean predicted probability
    """

    # TODO
    results = pd.DataFrame({
        group_column: (
            X_test[
                group_column
            ].reset_index(
                drop = True
            )
        ),
        "y_true": (
            y_test.reset_index(
                drop = True
            )
        ),
        "y_pred": predictions,
        "y_prob": probabilities,
    })


    rows = []

    for group, group_frame in (
        results.groupby(
            group_column,
            dropna = False,
        )
    ):
        rows.append({
            group_column: group,
            "n": len(
                group_frame
            ),
            "positive_rate": (
                group_frame[
                    "y_true"
                ].mean()
            ),
            "precision": (
                precision_score(
                    group_frame[
                        "y_true"
                    ],
                    group_frame[
                        "y_pred"
                    ],
                    zero_division = 0,
                )
            ),
            "recall": (
                recall_score(
                    group_frame[
                        "y_true"
                    ],
                    group_frame[
                        "y_pred"
                    ],
                    zero_division = 0,
                )
            ),
            "mean_probability": (
                group_frame[
                    "y_prob"
                ].mean()
            ),
        })

    return (
        pd.DataFrame(rows)
        .sort_values(
            "recall"
        )
        .reset_index(drop=True)
    )

def save_and_verify_model(
    model: Pipeline,
    X_test: pd.DataFrame,
    path: str | Path,
) -> None:
    """
    Problem:
    Save the complete fitted Pipeline, reload it,
    and verify that probabilities are unchanged.
    """

    # TODO
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    before = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

    joblib.dump(
        model,
        path,
    )

    restored = joblib.load(
        path
    )

    after = (
        restored.predict_proba(
            X_test
        )[:, 1]
    )

    if not np.allclose(
        before,
        after,
    ):
        raise AssertionError(
            "Predictions changed after model reload."
        )

    print(
        "\nPersistence check passed:"
        "predictions are unchanged."
    )

def main() -> None:
    # TODO:
    # 1. Create reproducible feature table.
    # 2. Add user_id for demonstration.
    # 3. Validate table.
    # 4. Separate X/y.
    # 5. Reserve final test.
    # 6. Build candidate models.
    # 7. Compare with CV.
    # 8. Select best model by mean ROC AUC.
    # 9. Fit selected model on all dev data.
    # 10. Evaluate final test.
    # 11. Run subgroup diagnostics.
    # 12. Save and verify model.

    frame = make_training_data(
        n_rows = 500,
        random_state= 42,
    )

    frame.insert(
        0,
        "user_id",
        range(
            1,
            len(frame) + 1,
        ),
    )

    validate_feature_table(
        frame
    )

    X = frame.drop(
        columns = TARGET_COLUMN
    )

    y = frame[
        TARGET_COLUMN
    ]

    (
        X_dev,
        X_test,
        y_dev,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size = 0.20,
        random_state = 42,
        stratify = y,
    )

    models = (
        build_candidate_models()
    )

    comparison = compare_models(
        models = models,
        X_dev = X_dev,
        y_dev = y_dev,
    )

    print(
        "Model Comparison:"
    )

    print(
        comparison.to_string(
            index = False
        )
    )

    best_model_name = (
        comparison.loc[
            0,
            "model",
        ]
    )

    print(
        "\nSelected model:",
        best_model_name,
    )

    final_model = models[
        best_model_name
    ]

    final_model.fit(
        X_dev,
        y_dev,
    )

    (
        predictions,
        probabilities,
    ) = evaluate_final_model(
        model = final_model,
        X_test = X_test,
        y_test = y_test,
    )

    subgroup_table = (
        subgroup_diagnostics(
            X_test = X_test,
            y_test = y_test,
            predictions = predictions,
            probabilities= probabilities,
            group_column=(
                "acquisition_channel"
            ),
        )
    )

    print(
        "\nSubgroup disgnostics:"
    )

    print(
        subgroup_table.to_string(
            index = False
        )
    )

    model_path = (
        Path(
            "week08_end_to_end_ml"
        )
        / "models"
        / "final_pipeline.joblib"
    )

    save_and_verify_model(
        model = final_model,
        X_test = X_test,
        path = model_path,
    )


if __name__ == "__main__":
    main()
