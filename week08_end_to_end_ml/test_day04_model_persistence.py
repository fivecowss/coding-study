import numpy as np
import pytest

from day02_preprocessing_pipeline import (
    make_training_data,
)

from day04_model_persistence import (
    load_model,
    predict_records,
    save_model,
    train_model,
    validate_threshold,
)

def make_fitted_model():
    frame = make_training_data(
        n_rows = 180,
        random_state = 42,
    )

    model, X_test, y_test = train_model(
        frame
    )

    return model, X_test, y_test


def test_invalid_threshold_raises():
    # TODO
    with pytest.raises(
        ValueError,
        match = "threshold must be between",
    ):
        validate_threshold(
            threshold = 1.5
        )


def test_prediction_output_contract():
    # TODO:
    # train model
    # predict one record
    # assert expected columns
    # assert one row
    # assert probability in [0, 1]
    model, X_test, _ = (
        make_fitted_model()
    )

    records = (
        X_test
        .head(1)
        .to_dict("records")
    )

    result = predict_records(
        model = model,
        records = records,
    )

    assert list(
        result.columns
    ) == [
        "probability",
        "prediction",
    ]

    assert len(result) == 1

    assert result[
        "probability"
    ].between(
        0,
        1,
    ).all()

    assert result[
        "prediction"
    ].isin(
        [0, 1]
    ).all()

def test_unseen_category_does_not_crash():
    # TODO:
    # use country="MX"
    # predict
    # assert valid output
    model, X_test, _ = (
        make_fitted_model()
    )

    record = (
        X_test
        .head(1)
        .to_dict("records")[0]
    )

    record["country"] = "MX"

    result = predict_records(
        model = model,
        records = [record],
    )

    assert len(result) == 1

    assert result[
        "probability"
    ].between(
        0,
        1,
    ).all()

def test_missing_numeric_value_does_not_crash():
    model, X_test, _ = (
        make_fitted_model()
    )

    record = (
        X_test
        .head(1)
        .to_dict("records")[0]
    )

    record["age"] = np.nan

    result = predict_records(
        model = model,
        records = [record],
    )

    assert len(result) == 1


def test_save_load_predictions_match(
    tmp_path,
):
    # TODO:
    # train
    # compute probability before save
    # save to tmp_path
    # reload
    # compute probability again
    # assert np.allclose
    model, X_test, _ = (
        make_fitted_model()
    )

    records = (
        X_test
        .head(5)
        .to_dict("records")
    )

    before = predict_records(
        model = model,
        records = records,
    )

    path = (
        tmp_path
        / "pipeline.joblib"
    )

    save_model(
        model = model,
        path = path,
    )

    restored = load_model(
        path
    )

    after = predict_records(
        model = restored,
        records = records,
    )

    assert np.allclose(
        before["probability"],
        after["probability"],
    )

    assert np.array_equal(
        before["prediction"],
        after["prediction"],
    )