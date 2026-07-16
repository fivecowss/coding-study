"""
Day 4: Threshold Tuning, Calibration, and Imbalanced Metrics

Goal:
- Train a classifier.
- Get predicted probabilities.
- Compare metrics at multiple thresholds.
- Compute expected cost.
- Compare uncalibrated vs calibrated probabilities.
"""

import numpy as np
import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


def load_data():
    """
    Load binary classification dataset.

    Return:
    - X: feature DataFrame
    - y: target Series
    """
    # TODO:
    # Use load_breast_cancer(as_frame=True)
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    return X, y


def split_data(X, y):
    """
    Create stratified train/test split.

    Requirements:
    - test_size=0.2
    - random_state=42
    - stratify=y
    """
    # TODO:
    # Return X_train, X_test, y_train, y_test
    return train_test_split(
        X,
        y,
        test_size = 0.2,
        random_state=42,
        stratify = y,
    )


def build_base_model():
    """
    Build baseline logistic regression pipeline.

    Required:
    - StandardScaler
    - LogisticRegression(max_iter=3000)
    """
    # TODO:
    # Return Pipeline
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter = 3000)),
    ])


def build_calibrated_model(base_model):
    """
    Wrap base model with CalibratedClassifierCV.

    Requirements:
    - method="sigmoid"
    - cv=5
    """
    # TODO:
    # Return calibrated classifier
    return CalibratedClassifierCV(
        estimator = base_model,
        method = "sigmoid",
        cv = 5,
    )


def evaluate_thresholds(y_true, prob, thresholds):
    """
    Evaluate precision, recall, F1, confusion matrix by threshold.

    Return:
    - DataFrame with threshold-level metrics
    """
    # TODO:
    # For each threshold:
    # pred = (prob >= threshold).astype(int)
    # compute precision, recall, f1, tn, fp, fn, tp
    rows = []

    for threshold in thresholds:
        pred = (prob >= threshold).astype(int)

        tn, fp, fn, tp = confusion_matrix(y_true, pred).ravel()

        rows.append({
            "threshold": threshold,
            "precision": precision_score(y_true, pred, zero_division = 0),
            "recall": recall_score(y_true, pred, zero_division = 0),
            "f1": f1_score(y_true, pred, zero_division = 0),
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp,
        })
    return pd.DataFrame(rows)

def compute_expected_cost(
    y_true,
    prob,
    thresholds,
    fp_cost=1.0,
    fn_cost=5.0,
):
    """
    Compute expected cost for each threshold.

    Cost:
    - fp_cost * FP + fn_cost * FN
    """
    # TODO:
    # Return DataFrame with threshold and cost.
    rows = []

    for threshold in thresholds:
        pred = (prob >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, pred).ravel()

        cost = fp_cost * fp + fn_cost * fn

        rows.append({
            "threshold": threshold,
            "fp": fp,
            "fn": fn,
            "fp_cost": fp_cost,
            "fn_cost": fn_cost,
            "total_cost": cost,
        })

    return pd.DataFrame(rows)


def make_prediction_table(y_true, prob, threshold=0.5):
    """
    Build row-level prediction table.

    Columns:
    - y_true
    - prob
    - pred
    - outcome_type
    """
    # TODO:
    # outcome_type should be TP, TN, FP, FN.
    pred = (prob >= threshold).astype(int)

    table = pd.DataFrame({
        "y_true": np.asarray(y_true),
        "prob": prob,
        "pred": pred,
    })

    conditions = [
        (table["y_true"] == 1) & (table["pred"] == 1),
        (table["y_true"] == 0) & (table["pred"] == 0),
        (table["y_true"] == 0) & (table["pred"] == 1),
        (table["y_true"] == 1) & (table["pred"] == 0),
    ]

    labels = ["TP", "TN", "FP", "FN"]

    table["outcome_type"] = np.select(
        conditions,
        labels,
        default = "unknown",
    )

    return table

def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    base_model = build_base_model()
    base_model.fit(X_train, y_train)

    base_prob = base_model.predict_proba(X_test)[:, 1]

    calibrated_model = build_calibrated_model(build_base_model())
    calibrated_model.fit(X_train, y_train)

    calibrated_prob = calibrated_model.predict_proba(X_test)[:, 1]

    thresholds = [0.2, 0.3, 0.5, 0.7, 0.8]

    print("Base model ROC AUC:")
    print(roc_auc_score(y_test, base_prob))
    print()

    print("Calibrated model ROC AUC:")
    print(roc_auc_score(y_test, calibrated_prob))
    print()

    print("Base model threshold metrics:")
    print(evaluate_thresholds(y_test, base_prob, thresholds))
    print()

    print("Calibrated model threshold metrics:")
    print(evaluate_thresholds(y_test, calibrated_prob, thresholds))
    print()

    print("Expected cost by threshold:")
    print(compute_expected_cost(y_test, calibrated_prob, thresholds))
    print()

    print("Prediction table sample:")
    pred_table = make_prediction_table(y_test, calibrated_prob, threshold=0.5)
    print(pred_table.head(10))


if __name__ == "__main__":
    main()