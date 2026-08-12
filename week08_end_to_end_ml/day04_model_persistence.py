from pathlib import Path
from collections.abc import Sequence

import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
)

from day02_preprocessing_pipeline import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET_COLUMN,
    build_model_pipeline,
    make_training_data,
)


def validate_threshold(
    threshold: float,
) -> None:
    """
    Ensure threshold is between 0 and 1.
    """

    # TODO
    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "threshold must be between 0 and 1"
        )


def train_model(
    frame: pd.DataFrame,
):
    """
    Fit the full preprocessing/model Pipeline.
    """

    # TODO:
    # 1. Split X and y.
    # 2. Train/test split.
    # 3. Build model Pipeline.
    # 4. Fit on train.
    # 5. Return model and X_test/y_test.

    X = frame.drop(
        columns = TARGET_COLUMN
    )

    y = frame[TARGET_COLUMN]

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size = 0.2,
        random_state = 42,
        stratify = y,
    )

    model = build_model_pipeline(
        numeric_features = NUMERIC_FEATURES,
        categorical_features = CATEGORICAL_FEATURES,
    )

    model.fit(
        X_train,
        y_train,
    )

    return (
        model,
        X_test.reset_index(drop = True),
        y_test.reset_index(drop = True)
    )


def predict_records(
    model,
    records: Sequence[dict],
    threshold: float = 0.5,
) -> pd.DataFrame:
    """
    Return probability and class prediction.
    """

    # TODO:
    # 1. Validate threshold.
    # 2. Convert records to DataFrame.
    # 3. Get positive probability.
    # 4. Apply custom threshold.
    # 5. Return DataFrame.

    validate_threshold(
        threshold
    )

    if len(records) == 0:
        return pd.DataFrame({
            "probability": [],
            "prediction": [],
        })

    frame = pd.DataFrame(
        records
    )

    probabilities = (
        model.predict_proba(
            frame
        )[:, 1]
    )

    predictions = (
        probabilities >= threshold
    ).astype(int)

    return pd.DataFrame({
        "probability": probabilities,
        "prediction": predictions,
    })

def save_model(
    model,
    path: str | Path,
) -> None:
    """
    Persist fitted model.
    """

    # TODO:
    # 1. Convert to Path.
    # 2. Create parent directory.
    # 3. joblib.dump.

    path = Path(path)

    path.parent.mkdir(
        parents = True,
        exist_ok = True,
    )

    joblib.dump(
        model,
        path,
    )


def load_model(
    path: str | Path,
):
    """
    Load persisted model.
    """

    # TODO:
    # Check path exists.
    # Load with joblib.

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Model file not found: {path}"
            )
    
    return joblib.load(
        path
    )


def main() -> None:
    frame = make_training_data(
        n_rows=250,
        random_state=42,
    )

    # TODO:
    # train model
    (
        model,
        X_test,
        y_test,
    ) = train_model(
        frame
    )

    # TODO:
    # predict several test rows
    sample_records = (
        X_test
        .head(5)
        .to_dict("records")
    )

    before = predict_records(
        model = model,
        records = sample_records,
        threshold = 0.5,
    )

    model_path = Path(
        "week08_end_to_end_ml"
    ) / "models" / "pipeline.joblib"


    # TODO:
    # save model
    save_model(
        model = model,
        path = model_path,
    )

    # TODO:
    # load model
    restored_model = load_model(
        model_path
    )

    # TODO:
    # verify predictions are identical
    after = predict_records(
        model = restored_model,
        records = sample_records,
        threshold = 0.5,
    )

    same_probabilities = np.allclose(
        before["probability"],
        after["probability"],
    )

    print("Before save:")
    print(before)

    print()

    print("After load:")
    print(after)

    print()

    print(
        "Probabilities identical:",
        same_probabilities,
    )

    assert same_probabilities



if __name__ == "__main__":
    main()