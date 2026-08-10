import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)


NUMERIC_FEATURES = [
    "age",
    "n_orders",
    "total_amount",
    "days_since_last_order",
]

CATEGORICAL_FEATURES = [
    "country",
    "acquisition_channel",
]

TARGET_COLUMN = "target"


def make_training_data(
    n_rows: int = 240,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Create a reproducible mixed-type binary-classification dataset.
    """

    # TODO:
    # 1. Create numeric features.
    # 2. Create categorical features.
    # 3. Construct probability from a logistic formula.
    # 4. Sample a binary target.
    # 5. Add several missing values.
    if n_rows < 20:
        raise ValueError(
            "n_rows must be at least 20."
        )

    rng = np.random.default_rng(
        random_state
    )

    frame = pd.DataFrame({
        "age": rng.integers(
            20,
            71,
            size = n_rows,
        ).astype(float),
        "n_orders": rng.poisson(
            lam = 4,
            size = n_rows,
        ).astype(float),
        "total_amount": rng.gamma(
            shape = 2.0,
            scale = 60.0,
            size = n_rows,
        ),
        "days_since_last_order": rng. integers(
            0,
            181,
            size = n_rows,
        ).astype(float),
        "country": rng.choice(
            ["US", "CA", "UK"],
            size = n_rows,
            p = [0.60, 0.25, 0.15],
        ),
        "acquisition_channel": rng.choice(
            [
                "search",
                "social",
                "referral",
            ],
            size=n_rows,
        ),
    }
    )

    logits = (
        -0.80
        + 0.18 * frame["n_orders"]
        + 0.003 * frame["total_amount"]
        - 0.015
        * frame["days_since_last_order"]
        + 0.35
        * (
            frame["acquisition_channel"]
            == "search"
        ).astype(float)
        + 0.25
        * (
            frame["acquisition_channel"]
            == "referral"
        ).astype(float)
    )

    probabilities = (
        1.0
        / (1.0 + np.exp(-logits))
    )
    frame[TARGET_COLUMN] = rng.binomial(
        n = 1,
        p = probabilities,
    )

    frame.loc[
        frame.index[::17],
        "age",
    ] = np.nan

    frame.loc[
        frame.index[::19],
        "country",
    ] = np.nan

    return frame

def build_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
) -> ColumnTransformer:
    """
    Create numeric and categorical preprocessing pipelines.
    """

    # TODO:
    # Numeric:
    # median imputation -> StandardScaler
    #
    # Categorical:
    # most-frequent imputation -> OneHotEncoder
    #
    # Combine with ColumnTransformer.
    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median",
                ),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps = [
            (
                "imputer",
                SimpleImputer(
                    strategy = "most_frequent",
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown = "ignore",
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                numeric_features,
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_features,
            ),
        ],
        remainder= "drop"
    )

    return preprocessor

def build_model_pipeline(
    numeric_features: list[str],
    categorical_features: list[str],
) -> Pipeline:
    """
    Combine preprocessing with LogisticRegression.
    """

    # TODO:
    # 1. Build preprocessor.
    # 2. Add LogisticRegression as the final pipeline step.
    preprocessor = build_preprocessor(
        numeric_features=numeric_features,
        categorical_features=categorical_features,
    )

    model = Pipeline(
        steps = [
            (
                "preprocess",
                preprocessor,
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter= 3000,
                    random_state=42,
                ),
            ),
        ]
    )

    return model


def evaluate_model(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> None:
    """
    Print classification metrics and ROC AUC.
    """

    # TODO:
    # 1. Generate class predictions.
    # 2. Generate positive-class probabilities.
    # 3. Print classification_report.
    # 4. Print ROC AUC.
    predictions = model.predict(
        X_test
    )
    probabilities = model.predict_proba(
        X_test
    )[:,1]

    print("Classification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    print(
        "ROC AUC:",
        round(
            roc_auc_score(
                y_test,
                probabilities,
            ),
            4,
        ),
    )


def main() -> None:
    frame = make_training_data()

    X = frame.drop(columns=TARGET_COLUMN)
    y = frame[TARGET_COLUMN]

    # TODO:
    # Use stratified train/test split.
    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size = 0.25,
        random_state= 42,
        stratify= y,
    )

    # TODO:
    # Build and fit model.
    model = build_model_pipeline(
        numeric_features=NUMERIC_FEATURES,
        categorical_features=CATEGORICAL_FEATURES,
    )
    model.fit(
        X_train,
        y_train,
    )

    # TODO:
    # Evaluate test performance.
    evaluate_model(
        model = model,
        X_test = X_test,
        y_test = y_test,
    )


    fitted_preprocessor = (
        model.named_steps[
            "preprocess"
        ]
    )

    # TODO:
    # Print transformed feature names.
    feature_names = (
        fitted_preprocessor
        .get_feature_names_out()
    )
    print("Transformed features:")
    for feature_name in feature_names:
        print(feature_name)

    # TODO:
    # Predict a new record containing:
    # - missing numeric value
    # - unseen country category
    new_record = pd.DataFrame([{
        "age": np.nan,
        "n_orders": 3.0,
        "total_amount": 80.0,
        "days_since_last_order": 20.0,
        "country": "MX",
        "acquisition_channel": "search",
    }])

    new_probability = (
        model.predict_proba(
            new_record
        )[:, 1]
    )

    new_prediction = model.predict(
        new_record
    )

    print(
        "Neworecord probability:",
        round(
            float(new_probability[0]),
            4,
        ),
    )

    print(
        "New-record prediction:",
        int(new_prediction[0]),
    )


if __name__ == "__main__":
    main()