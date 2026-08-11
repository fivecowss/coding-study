import pandas as pd

from sklearn.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)

from day02_preprocessing_pipeline import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET_COLUMN,
    build_model_pipeline,
    make_training_data,
)


def run_nested_cv(
    X: pd.DataFrame,
    y: pd.Series,
) -> list[float]:
    """
    Estimate generalization performance of the
    full hyperparameter-selection procedure.
    """

    # TODO:
    # 1. Create inner StratifiedKFold.
    # 2. Create outer StratifiedKFold.
    # 3. Build the full preprocessing/model Pipeline.
    # 4. Define classifier__C grid.
    # 5. Put GridSearchCV inside cross_val_score.
    # 6. Return the outer-fold scores.

    inner_cv = StratifiedKFold(
        n_splits = 4,
        shuffle = True,
        random_state = 42,
    )

    outer_cv = StratifiedKFold(
        n_splits = 5,
        shuffle = True,
        random_state = 42,
    )

    model = build_model_pipeline(
        numeric_features = NUMERIC_FEATURES,
        categorical_features = CATEGORICAL_FEATURES,
    )

    param_grid = {
        "classifier__C": [
            0.01,
            0.1,
            1.0,
            10.0,
        ],
    }

    search = GridSearchCV(
        estimator= model,
        param_grid = param_grid,
        scoring = "roc_auc",
        cv=inner_cv,
        n_jobs = -1,
    )

    scores = cross_val_score(
        estimator = search,
        X = X,
        y = y,
        scoring = "roc_auc",
        cv = outer_cv,
        n_jobs = -1,
    )
    return scores

def fit_final_search(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> GridSearchCV:
    """
    Tune hyperparameters using all development data.
    """

    # TODO:
    # Build model.
    # Build CV.
    # Define parameter grid.
    # Fit GridSearchCV.
    # Return fitted search object.

    cv = StratifiedKFold(
        n_splits = 5,
        shuffle = True,
        random_state = 42,
    )

    model = build_model_pipeline(
        numeric_features = NUMERIC_FEATURES,
        categorical_features = CATEGORICAL_FEATURES,
    )

    param_grid = {
        "classifier__C": [
            0.01,
            0.1,
            1.0,
            10.0,
        ],
    }

    search = GridSearchCV(
        estimator = model,
        param_grid = param_grid,
        scoring = "roc_auc",
        cv = cv,
        n_jobs = -1,
        refit = True,
    )

    search.fit(
        X_train,
        y_train,
    )

    return search


def build_subgroup_metrics(
    X_test: pd.DataFrame,
    y_test: pd.Series,
    predictions,
    probabilities,
    group_column: str,
) -> pd.DataFrame:
    """
    Calculate classification performance separately
    for each subgroup.
    """

    # TODO:
    # 1. Create a result DataFrame.
    # 2. Add y_true, y_pred, y_prob.
    # 3. groupby(group_column).
    # 4. Calculate n, prevalence,
    #    precision, recall, F1,
    #    mean predicted probability.
    # 5. Return one row per group.

    results = X_test[
        [group_column]
    ].copy()

    results["y_true"] = (
        y_test
        .reset_index(drop = True)
    )

    results["y_pred"] = predictions
    results["y_prob"] = probabilities

    rows = []

    for group, group_frame in results.groupby(
        group_column,
        dropna = False,
    ):
        rows.append({
            group_column: group,
            "n": len(group_frame),
            "positive_rate": (
                group_frame["y_true"].mean()
            ),
            "precision": precision_score(
                group_frame["y_true"],
                group_frame["y_pred"],
                zero_division = 0,
            ),
            "recall": recall_score(
                group_frame["y_true"],
                group_frame["y_pred"],
                zero_division = 0,
            ),
            "f1": f1_score(
                group_frame["y_true"],
                group_frame["y_pred"],
                zero_division = 0,
            ),
            "mean_probability": (
                group_frame["y_prob"].mean()
            ),
        })

    return pd.DataFrame(rows)


def main() -> None:
    frame = make_training_data(
        n_rows=300,
        random_state=42,
    )

    X = frame.drop(
        columns=TARGET_COLUMN
    )

    y = frame[TARGET_COLUMN]

    # TODO:
    # Reserve final test set FIRST.
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

    # TODO:
    # Run nested CV using development data only.
    nested_scores = run_nested_cv(
        X = X_dev,
        y = y_dev,
    )

    print("Nested CV ROC AUC:")
    print(nested_scores)

    print(
        "Nested CV mean:",
        round(
            nested_scores.mean(),
            4,
        ),
    )

    print(
        "Nested CV SD:",
        round(
            nested_scores.std(),
            4,
        ),
    )

    # TODO:
    # Tune final model on all development data.
    final_search = fit_final_search(
        X_train = X_dev,
        y_train = y_dev,
    )

    print(
        "Best parameters:",
        final_search.best_params_,
    )

    final_model = (
        final_search.best_estimator_
    )

    predictions = final_model.predict(
        X_test
    )

    probabilities = (
        final_model.predict_proba(
            X_test
        )[:, 1]
    )

    # TODO:
    # Evaluate final held-out test data.
    print("Final test report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division = 0,
        )
    )

    print(
        "Final test ROC AUC:",
        round(
            roc_auc_score(
                y_test,
                probabilities,
            ),
            4,
        ),
    )

    # TODO:
    # Build subgroup diagnostics by
    # acquisition_channel.
    subgroup_table = build_subgroup_metrics(
        X_test = X_test.reset_index(
            drop = True
        ),
        y_test = y_test.reset_index(
            drop = True
        ),
        predictions = predictions,
        probabilities = probabilities,
        group_column = "acquisition_channel",
    )

    print("Subgroup diagnostics:")
    print(
        subgroup_table.sort_values(
            "recall"
        )
    )

if __name__ == "__main__":
    main()