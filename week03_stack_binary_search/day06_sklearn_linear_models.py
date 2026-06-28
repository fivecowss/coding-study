# week03_stack_binary_search/day06_sklearn_linear_models.py


# ============================================================
# Week 3 Day 6
# Topic: sklearn Linear Models + Cross-Validation
#
# Part A:
#   Regression with LinearRegression, Ridge, Lasso
#
# Part B:
#   Classification with LogisticRegression
#
# Key ideas:
#   - Use Pipeline to combine preprocessing and model.
#   - Use StandardScaler before linear models.
#   - Use train/test split for final held-out evaluation.
#   - Use cross_val_score for cross-validation.
# ============================================================


# ------------------------------------------------------------
# Step 0. Imports
# ------------------------------------------------------------
# TODO: import load_diabetes, load_breast_cancer
from sklearn.datasets import load_diabetes, load_breast_cancer
# TODO: import train_test_split, cross_val_score
from sklearn.model_selection import train_test_split, cross_val_score
# TODO: import StandardScaler
from sklearn.preprocessing import StandardScaler
# TODO: import Pipeline
from sklearn.pipeline import Pipeline
# TODO: import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
    LogisticRegression
)
# TODO: import mean_squared_error, r2_score
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    classification_report,
    roc_auc_score
)
# TODO: import classification_report, roc_auc_score


def run_regression_models() -> None:
    """
    Compare LinearRegression, Ridge, and Lasso
    on the diabetes regression dataset.
    """

    # --------------------------------------------------------
    # Step 1. Load regression dataset.
    # --------------------------------------------------------
    # TODO: load diabetes dataset with as_frame=True
    data = load_diabetes(as_frame = True)

    # TODO: define X and y
    X = data.data
    y = data.target

    # --------------------------------------------------------
    # Step 2. Split data into train and test.
    # --------------------------------------------------------
    # TODO: train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size= 0.2,
        random_state= 42,
    )

    # --------------------------------------------------------
    # Step 3. Define models.
    # Each model will be wrapped inside a Pipeline.
    # --------------------------------------------------------
    models = {
        # TODO: add LinearRegression
        "LinearRegression": LinearRegression(),

        # TODO: add Ridge(alpha=1.0)
        "Ridge": Ridge(alpha = 1.0),
        # TODO: add Lasso(alpha=0.1, max_iter=10000)
        "Lasso": Lasso(alpha = 0.1, max_iter = 10000),
    }

    print("=" * 60)
    print("REGRESSION: LinearRegression vs Ridge vs Lasso")
    print("=" * 60)

    # --------------------------------------------------------
    # Step 4. Loop over models.
    # --------------------------------------------------------
    for name, model in models.items():

        # ----------------------------------------------------
        # Step 4a. Build Pipeline.
        # Pipeline:
        #   StandardScaler -> model
        # ----------------------------------------------------
        # TODO: create pipeline
        pipe = Pipeline([
            ("scalar", StandardScaler()),
            ("model", model),
        ])

        # ----------------------------------------------------
        # Step 4b. Fit on training data.
        # ----------------------------------------------------
        # TODO: fit pipeline
        pipe.fit(X_train, y_train)

        # ----------------------------------------------------
        # Step 4c. Predict on test data.
        # ----------------------------------------------------
        # TODO: predict
        pred = pipe.predict(X_test)

        # ----------------------------------------------------
        # Step 4d. Evaluate with MSE and R2.
        # ----------------------------------------------------
        # TODO: compute mse
        # TODO: compute r2
        mse = mean_squared_error(y_test, pred)
        r2 = r2_score(y_test, pred)

        # ----------------------------------------------------
        # Step 4e. Cross-validation.
        # Use R2 as scoring.
        # ----------------------------------------------------
        # TODO: cross_val_score with cv=5 and scoring="r2"
        cv_scores = cross_val_score(
            pipe,
            X,
            y,
            cv = 5,
            scoring = "r2",
        )

        print(f"\nModel: {name}")
        print(f"Test MSE: {mse:.4f}")
        print(f"Test R2: {r2:.4f}")
        print(f"CV R2 scores: {cv_scores}")
        print(f"Mean CV R2: {cv_scores.mean():.4f}")


def run_classification_model() -> None:
    """
    Train LogisticRegression on the breast cancer classification dataset.
    """

    # --------------------------------------------------------
    # Step 1. Load classification dataset.
    # --------------------------------------------------------
    # TODO: load breast cancer dataset with as_frame=True
    data = load_breast_cancer(as_frame = True)
    X = data.data
    y = data.target

    # --------------------------------------------------------
    # Step 2. Split data into train and test.
    # Use stratify=y because this is classification.
    # --------------------------------------------------------
    # TODO: train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size= 0.2,
        random_state= 42,
        stratify = y,
    )

    # --------------------------------------------------------
    # Step 3. Build Pipeline.
    # StandardScaler -> LogisticRegression
    # --------------------------------------------------------
    # TODO: create pipeline
    pipe = Pipeline([
        ("scalar", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000)),
    ])

    # --------------------------------------------------------
    # Step 4. Fit model.
    # --------------------------------------------------------
    # TODO: fit pipeline
    pipe.fit(X_train, y_train)


    # --------------------------------------------------------
    # Step 5. Predict class labels and probabilities.
    # --------------------------------------------------------
    # TODO: pred = pipe.predict(X_test)
    # TODO: prob = pipe.predict_proba(X_test)[:, 1]
    pred = pipe.predict(X_test)
    prob = pipe.predict_proba(X_test)[:,1]

    # --------------------------------------------------------
    # Step 6. Evaluate.
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("CLASSIFICATION: LogisticRegression")
    print("=" * 60)

    # TODO: print classification_report
    print(classification_report(y_test, pred))
    # TODO: print ROC AUC
    print(f"ROC AUC: {roc_auc_score(y_test, prob):.4f}")

    # --------------------------------------------------------
    # Step 7. Cross-validation with ROC AUC.
    # --------------------------------------------------------
    # TODO: cross_val_score with cv=5 and scoring="roc_auc"
    cv_scores = cross_val_score(
        pipe,
        X,
        y,
        cv = 5,
        scoring = "roc_auc",
    )

    print(f"CV ROC AUC scores: {cv_scores}")
    print(f"Mean CV ROC AUC: {cv_scores.mean():.4f}")


if __name__ == "__main__":
    run_regression_models()
    run_classification_model()