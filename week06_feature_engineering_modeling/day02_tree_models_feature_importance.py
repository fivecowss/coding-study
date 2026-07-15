"""
Day 2: Tree-Based Models and Feature Importance

Goal:
- Compare Logistic Regression, Random Forest, and Gradient Boosting.
- Compute ROC AUC.
- Inspect impurity-based feature importance.
- Inspect permutation importance.
"""

import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score, classification_report


def load_data():
    """
    Load a toy binary classification dataset.

    Return:
    - X: feature DataFrame
    - y: target Series
    """
    # TODO:
    # Use load_breast_cancer(as_frame=True)
    data = load_breast_cancer(as_frame = True)
    X = data.data
    y = data.target

    return X, y


def split_data(X, y):
    """
    Create train/test split.

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
        random_state = 42,
        stratify = y,
    )


def build_models():
    """
    Build models to compare.

    Required:
    - logistic regression pipeline with StandardScaler
    - random forest
    - hist gradient boosting
    """
    # TODO:
    # Return dictionary of models
    models = {
        "logistic": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter= 3000)),
        ]),
        "random_forest": RandomForestClassifier(
            n_estimators = 300,
            random_state = 42,
            class_weight = "balanced",
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            random_state = 42,
        ),
    }

    return models

def evaluate_models(models, X_train, X_test, y_train, y_test):
    """
    Fit each model and print ROC AUC.

    Return:
    - fitted models dictionary
    """
    # TODO:
    # Loop over models.
    # Fit model.
    # Compute predicted probabilities.
    # Print ROC AUC.
    fitted_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)

        prob = model.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, prob)

        pred = model.predict(X_test)

        print("=" * 60)
        print(name)
        print("ROC AUC:", roc_auc)
        print(classification_report(y_test, pred))
        
        fitted_models[name] = model

    return fitted_models
    


def show_random_forest_importance(rf_model, feature_names):
    """
    Show impurity-based feature importance from RandomForestClassifier.
    """
    # TODO:
    # Use rf_model.feature_importances_
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": rf_model.feature_importances_,
    })

    importance_df = importance_df.sort_values(
        "importance",
        ascending = False,
    )

    print(importance_df.head(10))

def show_permutation_importance(rf_model, X_test, y_test):
    """
    Show permutation importance.

    Requirements:
    - scoring="roc_auc"
    - n_repeats=10
    - random_state=42
    """
    # TODO:
    # Use permutation_importance(...)
    result = permutation_importance(
        rf_model,
        X_test,
        y_test,
        scoring = "roc_auc",
        n_repeats = 10,
        random_state = 42,
    )

    importance_df = pd.DataFrame({
        "feature": X_test.columns,
        "importance_mean": result.importances_mean,
        "importance_std": result.importances_std,
    })

    importance_df = importance_df.sort_values(
        "importance_mean",
        ascending = False,
    )

def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    models = build_models()
    fitted_models = evaluate_models(
        models,
        X_train,
        X_test,
        y_train,
        y_test,
    )

    rf_model = fitted_models["random_forest"]

    print("\nImpurity-based Random Forest importance:")
    show_random_forest_importance(rf_model, X.columns)

    print("\nPermutation importance:")
    show_permutation_importance(rf_model, X_test, y_test)


if __name__ == "__main__":
    main()