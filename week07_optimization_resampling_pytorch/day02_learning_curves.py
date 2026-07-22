import numpy as np
import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, learning_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_learning_curve_summary() -> pd.DataFrame:
    """
    Build a learning-curve summary for a logistic regression classifier.

    Return columns:
    - train_size
    - train_score_mean
    - train_score_std
    - validation_score_mean
    - validation_score_std
    """

    # TODO: Load the breast-cancer dataset, define a scaling and logistic
    # regression pipeline, configure stratified cross-validation, and call
    # learning_curve with several training-set fractions and ROC AUC scoring.
    # Summarize the mean and standard deviation across folds in a DataFrame.

    data = load_breast_cancer(as_frame = True)

    X = data.data
    y = data.target

    model = Pipeline([
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                max_iter = 3000,
                random_state = 42,
            ),
        ),
    ])

    cv = StratifiedKFold(
        n_splits = 5,
        shuffle = True,
        random_state = 42,
    )

    train_sizes, train_scores, validation_scores = learning_curve(
        estimator = model,
        X=X,
        y=y,
        train_sizes = np.linspace(0.2, 1.0, 5),
        cv = cv,
        scoring = "roc_auc",
        shuffle = True,
        random_state= 42,
        n_jobs = None,
    )

    summary = pd.DataFrame({
        "train_size": train_sizes,
        "train_score_mean": train_scores.mean(axis = 1),
        "train_score_std": train_scores.std(axis = 1),
        "validation_score_mean": validation_scores.mean(axis = 1),
        "validation_score_std": validation_scores.std(axis = 1),
    })

    return summary


def main() -> None:
    summary = build_learning_curve_summary()

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()