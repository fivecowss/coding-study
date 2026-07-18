"""
Day 5: Compare Manual Logistic Regression with sklearn

Goal:
- Reuse synthetic data.
- Fit sklearn LogisticRegression.
- Compare sklearn model with manual implementation.
"""

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from day05_numpy_logistic_regression import (
    build_toy_data,
    fit_logistic_regression,
    predict_proba,
    predict,
)


def fit_manual_model(X_train, y_train):
    """
    Fit manual logistic regression.
    """
    # TODO:
    # Use fit_logistic_regression.
    w, b, _ = fit_logistic_regression(
        X_train,
        y_train,
        learning_rate = 0.1,
        n_steps = 1000,
        print_every = 200,
    )

    return w, b


def fit_sklearn_model(X_train, y_train):
    """
    Fit sklearn LogisticRegression with StandardScaler.
    """
    # TODO:
    # Build Pipeline:
    # - StandardScaler
    # - LogisticRegression(max_iter=3000)
    # Fit and return model.
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter = 3000)),
    ])

    model.fit(X_train, y_train)

    return model


def evaluate_model(name, y_true, y_prob, y_pred):
    """
    Print accuracy, ROC AUC, and log loss.
    """
    # TODO:
    # Print metrics.
    print("=" * 60)
    print(name)
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("ROC AUC:", roc_auc_score(y_true, y_prob))
    print("Log loss:", log_loss(y_true, y_prob))


def main():
    X, y = build_toy_data(seed=42)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    manual_w, manual_b = fit_manual_model(X_train, y_train)

    manual_prob = predict_proba(X_test, manual_w, manual_b)
    manual_pred = predict(X_test, manual_w, manual_b)

    sklearn_model = fit_sklearn_model(X_train, y_train)
    sklearn_prob = sklearn_model.predict_proba(X_test)[:, 1]
    sklearn_pred = sklearn_model.predict(X_test)

    evaluate_model("Manual logistic regression", y_test, manual_prob, manual_pred)
    evaluate_model("sklearn LogisticRegression", y_test, sklearn_prob, sklearn_pred)

    print("Manual weights:", manual_w)
    print("Manual bias:", manual_b)


if __name__ == "__main__":
    main()