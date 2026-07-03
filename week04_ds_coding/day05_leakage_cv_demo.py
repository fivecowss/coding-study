from __future__ import annotations

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score


def load_data():
    """
    Task:
    Load breast cancer dataset.

    Direction:
    - Return X, y.
    """
    # TODO
    data = load_breast_cancer(as_frame = True)
    X = data.data
    y = data.target
    return X, y


def wrong_workflow_scaling_before_split(X, y) -> float:
    """
    Task:
    Demonstrate a risky workflow.

    Wrong flow:
    1. Fit StandardScaler on the entire dataset.
    2. Transform the entire dataset.
    3. Split into train/test.
    4. Train model.
    5. Evaluate test ROC AUC.

    Why risky:
    - The scaler has already seen test-set information.
    - This can make performance estimates overly optimistic.

    Direction:
    - Fit scaler on X before train_test_split.
    - Then split scaled X.
    - Fit LogisticRegression.
    - Return test ROC AUC.
    """
    # TODO:
    # 1. scaler = StandardScaler()
    # 2. X_scaled = scaler.fit_transform(X)
    # 3. train/test split X_scaled, y
    # 4. fit LogisticRegression
    # 5. compute test ROC AUC
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y, 
        test_size = 0.2,
        random_state = 42,
        stratify = y
    )
    model = LogisticRegression(max_iter = 2000)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    return roc_auc_score(y_test, prob)
    


def correct_workflow_pipeline_after_split(X, y) -> float:
    """
    Task:
    Implement the safer workflow.

    Correct flow:
    1. Split raw X, y into train/test.
    2. Create Pipeline(StandardScaler + LogisticRegression).
    3. Fit pipeline only on training data.
    4. Evaluate on test data.

    Why safer:
    - StandardScaler.fit is performed only on X_train.
    - X_test is transformed using training-set mean/std.
    """
    # TODO:
    # 1. train/test split raw X, y
    # 2. build Pipeline
    # 3. fit on X_train, y_train
    # 4. compute test ROC AUC
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size = 0.2,
        random_state = 42,
        stratify = y
    )
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter = 2000))
    ])
    pipe.fit(X_train, y_train)
    prob = pipe.predict_proba(X_test)[:, 1]
    return roc_auc_score(y_test, prob)



def cross_validate_pipeline(X, y):
    """
    Task:
    Run cross-validation using a Pipeline.

    Direction:
    - Build Pipeline(StandardScaler + LogisticRegression).
    - Run cross_val_score with cv=5 and scoring="roc_auc".
    - Return scores.

    Key idea:
    - In each fold, scaler is fit only on that fold's training subset.
    - This is safer than scaling once before cross-validation.
    """
    # TODO:
    # 1. build pipeline
    # 2. run cross_val_score
    # 3. return scores
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter = 2000))
    ])
    scores = cross_val_score(
        pipe,
        X,
        y,
        cv = 5,
        scoring = "roc_auc"
    )
    return scores


def main() -> None:
    X, y = load_data()

    wrong_auc = wrong_workflow_scaling_before_split(X, y)
    print("Wrong workflow test ROC AUC:", wrong_auc)

    correct_auc = correct_workflow_pipeline_after_split(X, y)
    print("Correct workflow test ROC AUC:", correct_auc)

    cv_scores = cross_validate_pipeline(X, y)
    print("Pipeline CV scores:", cv_scores)
    print("Pipeline CV mean:", cv_scores.mean())

    print("Implement TODO functions, then uncomment blocks in main().")


if __name__ == "__main__":
    main()


# -------------------------------------------------------------------
# SAMPLE ANSWER — REFERENCE ONLY
# Keep this section commented out while practicing.
# -------------------------------------------------------------------

# def load_data():
#     data = load_breast_cancer(as_frame=True)
#     X = data.data
#     y = data.target
#     return X, y
#
#
# def wrong_workflow_scaling_before_split(X, y) -> float:
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)
#
#     X_train, X_test, y_train, y_test = train_test_split(
#         X_scaled,
#         y,
#         test_size=0.2,
#         random_state=42,
#         stratify=y,
#     )
#
#     model = LogisticRegression(max_iter=2000)
#     model.fit(X_train, y_train)
#
#     prob = model.predict_proba(X_test)[:, 1]
#     return roc_auc_score(y_test, prob)
#
#
# def correct_workflow_pipeline_after_split(X, y) -> float:
#     X_train, X_test, y_train, y_test = train_test_split(
#         X,
#         y,
#         test_size=0.2,
#         random_state=42,
#         stratify=y,
#     )
#
#     pipe = Pipeline([
#         ("scaler", StandardScaler()),
#         ("model", LogisticRegression(max_iter=2000)),
#     ])
#
#     pipe.fit(X_train, y_train)
#
#     prob = pipe.predict_proba(X_test)[:, 1]
#     return roc_auc_score(y_test, prob)
#
#
# def cross_validate_pipeline(X, y):
#     pipe = Pipeline([
#         ("scaler", StandardScaler()),
#         ("model", LogisticRegression(max_iter=2000)),
#     ])
#
#     scores = cross_val_score(
#         pipe,
#         X,
#         y,
#         cv=5,
#         scoring="roc_auc",
#     )
#
#     return scores