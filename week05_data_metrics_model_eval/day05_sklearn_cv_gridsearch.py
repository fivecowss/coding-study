from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_auc_score,
)


def load_data():
    """
    Load the breast cancer classification dataset.

    X: feature matrix
    y: binary target
    """
    # TODO 1:
    # Use load_breast_cancer(as_frame=True).
    # Return X, y.
    data = load_breast_cancer(as_frame = True)
    X = data.data
    y = data.target
    return X, y


def build_logistic_pipeline() -> Pipeline:
    """
    Build a LogisticRegression pipeline.

    Steps:
    - StandardScaler
    - LogisticRegression
    """
    # TODO 2:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=3000))
    ])
    


def evaluate_predictions(y_test, pred, prob) -> None:
    """
    Print confusion matrix, classification report, and ROC AUC.
    """
    # TODO 3:
    # Print confusion_matrix(y_test, pred)
    print("Confusion matrix:")
    print(confusion_matrix(y_test, pred))

    # TODO 4:
    print("\nClassification report:")
    print (classification_report(y_test, pred))

    # TODO 5:

    print ("ROC AUC:", roc_auc_score(y_test, prob))


def main() -> None:
    print("\n=== Load data ===")

    X, y = load_data()

    print("X shape:", X.shape)
    print("y distribution:")
    print(y.value_counts())

    print("\n=== Train/test split ===")

    # TODO 6:
    # Split X and y.
    # Use:
    # test_size=0.2
    # random_state=42
    # stratify=y

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify = y,
    )

    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)

    print("\n=== Build logistic regression pipeline ===")

    # TODO 7:
    # Build logistic pipeline.

    logistic_pipe = build_logistic_pipeline()

    print(logistic_pipe)

    print("\n=== Cross-validation ROC AUC ===")

    # TODO 8:
    # Use cross_val_score on X_train, y_train.
    # cv=5
    # scoring="roc_auc"

    cv_scores = cross_val_score(
        logistic_pipe,
        X_train,
        y_train,
        cv=5,
        scoring= "roc_auc",
    )

    print("CV scores:", cv_scores)
    print("Mean CV ROC AUC:", cv_scores.mean())

    print("\n=== GridSearchCV for LogisticRegression C ===")

    param_grid = {
        "model__C": [0.01, 0.1, 1.0, 10.0],
    }

    # TODO 9:
    # Create GridSearchCV with:
    # estimator=logistic_pipe
    # param_grid=param_grid
    # scoring="roc_auc"
    # cv=5

    grid = GridSearchCV(
        estimator=logistic_pipe,
        param_grid=param_grid,
        scoring = "roc_auc",
        cv = 5,
    )

    # TODO 10:
    # Fit grid on X_train, y_train.

    grid.fit(X_train, y_train)

    print("Best params:", grid.best_params_)
    print("Best CV ROC AUC:", grid.best_score_)

    print("\n=== Final test evaluation ===")

    # TODO 11:
    # Use grid.best_estimator_ as final model.

    best_model = grid.best_estimator_

    # TODO 12:
    # Generate pred and prob on X_test.

    pred = best_model.predict(X_test)
    prob = best_model.predict_proba(X_test)[:, 1]

    evaluate_predictions(y_test, pred, prob)

    print("\n=== Random forest baseline ===")

    # TODO 13:
    # Create RandomForestClassifier:
    # n_estimators=300
    # random_state=42
    # class_weight="balanced"

    rf = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
    )

    # TODO 14:
    # Fit rf on X_train, y_train.

    rf.fit(X_train, y_train)

    # TODO 15:
    # Compute rf_prob and ROC AUC.

    rf_prob = rf.predict_proba(X_test)[:, 1]

    print("Random Forest Test ROC AUC:", roc_auc_score(y_test, rf_prob))


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# SAMPLE ANSWER
# ----------------------------------------------------------------------
#
# def load_data():
#     data = load_breast_cancer(as_frame=True)
#     X = data.data
#     y = data.target
#     return X, y
#
#
# def build_logistic_pipeline() -> Pipeline:
#     return Pipeline([
#         ("scaler", StandardScaler()),
#         ("model", LogisticRegression(max_iter=3000)),
#     ])
#
#
# def evaluate_predictions(y_test, pred, prob) -> None:
#     print("Confusion matrix:")
#     print(confusion_matrix(y_test, pred))
#
#     print("\nClassification report:")
#     print(classification_report(y_test, pred))
#
#     print("ROC AUC:", roc_auc_score(y_test, prob))
#
#
# def main() -> None:
#     print("\n=== Load data ===")
#
#     X, y = load_data()
#
#     print("X shape:", X.shape)
#     print("y distribution:")
#     print(y.value_counts())
#
#     print("\n=== Train/test split ===")
#
#     X_train, X_test, y_train, y_test = train_test_split(
#         X,
#         y,
#         test_size=0.2,
#         random_state=42,
#         stratify=y,
#     )
#
#     print("Train shape:", X_train.shape)
#     print("Test shape:", X_test.shape)
#
#     print("\n=== Build logistic regression pipeline ===")
#
#     logistic_pipe = build_logistic_pipeline()
#
#     print(logistic_pipe)
#
#     print("\n=== Cross-validation ROC AUC ===")
#
#     cv_scores = cross_val_score(
#         logistic_pipe,
#         X_train,
#         y_train,
#         cv=5,
#         scoring="roc_auc",
#     )
#
#     print("CV scores:", cv_scores)
#     print("Mean CV ROC AUC:", cv_scores.mean())
#
#     print("\n=== GridSearchCV for LogisticRegression C ===")
#
#     param_grid = {
#         "model__C": [0.01, 0.1, 1.0, 10.0],
#     }
#
#     grid = GridSearchCV(
#         estimator=logistic_pipe,
#         param_grid=param_grid,
#         scoring="roc_auc",
#         cv=5,
#     )
#
#     grid.fit(X_train, y_train)
#
#     print("Best params:", grid.best_params_)
#     print("Best CV ROC AUC:", grid.best_score_)
#
#     print("\n=== Final test evaluation ===")
#
#     best_model = grid.best_estimator_
#
#     pred = best_model.predict(X_test)
#     prob = best_model.predict_proba(X_test)[:, 1]
#
#     evaluate_predictions(y_test, pred, prob)
#
#     print("\n=== Random forest baseline ===")
#
#     rf = RandomForestClassifier(
#         n_estimators=300,
#         random_state=42,
#         class_weight="balanced",
#     )
#
#     rf.fit(X_train, y_train)
#     rf_prob = rf.predict_proba(X_test)[:, 1]
#
#     print("Random Forest Test ROC AUC:", roc_auc_score(y_test, rf_prob))