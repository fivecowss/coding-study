
from __future__ import annotations

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score


def load_data():
    """
    Task:
    Load a binary classification dataset.

    New concepts:
    - load_breast_cancer(as_frame=True):
        returns a dataset object where data can be accessed as a pandas DataFrame.
    - X:
        feature matrix
    - y:
        target labels

    Direction:
    - Use load_breast_cancer(as_frame=True).
    - Return X and y.
    """
    # TODO:
    # 1. load breast cancer data with as_frame=True
    data = load_breast_cancer(as_frame = True)
    # 2. set X = data.data
    X = data.data
    # 3. set y = data.target
    y = data.target
    # 4. return X, y
    return X, y


def make_train_test_split(X, y):
    """
    Task:
    Split data into train and test sets.

    New concepts:
    - train_test_split:
        creates random train/test subsets.
    - test_size=0.2:
        use 20% as test set.
    - random_state=42:
        makes the random split reproducible.
    - stratify=y:
        preserves class proportions in train/test split.

    Direction:
    - Return X_train, X_test, y_train, y_test.
    """
    # TODO:
    # use train_test_split with:
    # test_size=0.2
    # random_state=42
    # stratify=y
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size = 0.2,
        random_state = 42,
        stratify = y
    )

    return X_train, X_test, y_train, y_test

def build_logistic_pipeline() -> Pipeline:
    """
    Task:
    Build a preprocessing + model pipeline.

    New concepts:
    - Pipeline:
        chains preprocessing and model steps.
    - StandardScaler:
        standardizes numerical features.
    - LogisticRegression:
        binary classification model.
    - max_iter:
        increases optimization iterations if convergence is slow.

    Direction:
    - Create Pipeline with two steps:
        1. "scaler": StandardScaler()
        2. "model": LogisticRegression(max_iter=2000)
    """
    # TODO: return pipeline
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter = 2000))
    ])
    return pipeline


def run_cross_validation(model: Pipeline, X_train, y_train):
    """
    Task:
    Evaluate model using cross-validation on training data.

    New concepts:
    - cross_val_score:
        returns one score per CV split.
    - cv=5:
        five-fold cross-validation.
    - scoring="roc_auc":
        evaluate ranking quality for binary classification.

    Direction:
    - Run cross_val_score.
    - Return scores.
    """
    # TODO:
    # scores = cross_val_score(...)
    # return scores
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv = 5,
        scoring = "roc_auc"
    )
    return scores

def run_grid_search(model: Pipeline, X_train, y_train) -> GridSearchCV:
    """
    Task:
    Tune LogisticRegression hyperparameter C using GridSearchCV.

    New concepts:
    - C:
        inverse regularization strength for LogisticRegression.
        Smaller C means stronger regularization.
    - model__C:
        Pipeline parameter naming format.
        "model" is the pipeline step name.
        "C" is the LogisticRegression parameter.
    - GridSearchCV:
        tries all parameter combinations using cross-validation.

    Direction:
    - param_grid should test:
        [0.01, 0.1, 1.0, 10.0]
    - scoring should be "roc_auc"
    - cv should be 5
    - fit on X_train, y_train
    - return fitted grid object
    """
    # TODO:
    # 1. create param_grid
    # 2. create GridSearchCV
    # 3. fit it on training data
    # 4. return grid
    param_grid = {
        "model__C": [0.01, 0.1, 1.0, 10.0]
    }
    grid = GridSearchCV(
        estimator = model,
        param_grid = param_grid,
        scoring = "roc_auc",
        cv = 5 
    )
    grid.fit(X_train, y_train)
    return grid


def evaluate_on_test(best_model: Pipeline, X_test, y_test) -> None:
    """
    Task:
    Evaluate the selected model on the held-out test set.

    New concepts:
    - predict:
        returns predicted class labels.
    - predict_proba:
        returns predicted probabilities.
    - classification_report:
        precision, recall, F1-score.
    - roc_auc_score:
        threshold-free ranking metric.

    Direction:
    - Compute predicted labels.
    - Compute predicted probability for positive class.
    - Print accuracy, ROC AUC, and classification report.
    """
    # TODO:
    # 1. pred = best_model.predict(X_test)
    # 2. prob = best_model.predict_proba(X_test)[:, 1]
    # 3. print accuracy
    # 4. print ROC AUC
    # 5. print classification report
    pred = best_model.predict(X_test)
    prob = best_model.predict_proba(X_test)[:, 1]
    print("Accuracy:", accuracy_score(y_test, pred))
    print("ROC AUC:", roc_auc_score(y_test, prob))
    print("Classification report:")
    print(classification_report(y_test, pred))



def main() -> None:
    """
    Suggested workflow:

    1. Implement load_data().
    2. Implement make_train_test_split().
    3. Implement build_logistic_pipeline().
    4. Implement run_cross_validation().
    5. Implement run_grid_search().
    6. Implement evaluate_on_test().

    After each function is implemented, uncomment the corresponding block below.
    """

    X, y = load_data()
    X_train, X_test, y_train, y_test = make_train_test_split(X, y)
    model = build_logistic_pipeline()

    print("Cross-validation scores")
    scores = run_cross_validation(model, X_train, y_train)
    print(scores)
    print("Mean CV ROC AUC:", scores.mean())

    print("\nGrid search")
    grid = run_grid_search(model, X_train, y_train)
    print("Best parameters:", grid.best_params_)
    print("Best CV ROC AUC:", grid.best_score_)

    print("\nFinal test evaluation")
    evaluate_on_test(grid.best_estimator_, X_test, y_test)

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
# def make_train_test_split(X, y):
#     return train_test_split(
#         X,
#         y,
#         test_size=0.2,
#         random_state=42,
#         stratify=y,
#     )
#
#
# def build_logistic_pipeline() -> Pipeline:
#     return Pipeline([
#         ("scaler", StandardScaler()),
#         ("model", LogisticRegression(max_iter=2000)),
#     ])
#
#
# def run_cross_validation(model: Pipeline, X_train, y_train):
#     scores = cross_val_score(
#         model,
#         X_train,
#         y_train,
#         cv=5,
#         scoring="roc_auc",
#     )
#     return scores
#
#
# def run_grid_search(model: Pipeline, X_train, y_train) -> GridSearchCV:
#     param_grid = {
#         "model__C": [0.01, 0.1, 1.0, 10.0],
#     }
#
#     grid = GridSearchCV(
#         estimator=model,
#         param_grid=param_grid,
#         scoring="roc_auc",
#         cv=5,
#     )
#
#     grid.fit(X_train, y_train)
#     return grid
#
#
# def evaluate_on_test(best_model: Pipeline, X_test, y_test) -> None:
#     pred = best_model.predict(X_test)
#     prob = best_model.predict_proba(X_test)[:, 1]
#
#     print("Accuracy:", accuracy_score(y_test, pred))
#     print("ROC AUC:", roc_auc_score(y_test, prob))
#     print("Classification report:")
#     print(classification_report(y_test, pred))