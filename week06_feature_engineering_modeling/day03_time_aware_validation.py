"""
Day 3: Time-Aware Validation and Rolling/Lag Features

Goal:
- Create lag and rolling features.
- Avoid temporal leakage.
- Split data by time rather than random split.
- Optionally demonstrate TimeSeriesSplit.
"""

import pandas as pd

from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def build_price_data() -> pd.DataFrame:
    """
    Build a small time-ordered price dataset.

    Required columns:
    - date
    - price
    """
    # TODO:
    # Return a DataFrame with 12 daily prices.
    return pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods = 12, freq = "D"),
        "price": [
            100.0,
            101.1,
            103.0,
            102.0,
            105.0,
            107.0,
            106.0,
            108.0,
            110.0,
            109.0,
            112.0,
            115.0,
        ]
    })


def create_return_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create return, lag, and rolling features.

    Required features:
    - return
    - lag_return_1
    - rolling_mean_3
    - rolling_std_3

    Important:
    - rolling features must use shift(1) before rolling.
    - This avoids using current/future information.
    """
    # TODO:
    # 1. Sort by date.
    # 2. Compute pct_change.
    # 3. Create lag_return_1.
    # 4. Create rolling_mean_3 using shift(1).rolling(3).mean().
    # 5. Create rolling_std_3 using shift(1).rolling(3).std().
    # 6. Create target as next-day return.
    out = df.copy()
    out = out.sort_values("date").reset_index(drop=True)

    out["return"] = out["price"].pct_change()

    out["lag_return_1"] = out["return"].shift(1)

    shifted_return = out["return"].shift(1)
    out["rolling_mean_3"] = shifted_return.rolling(3).mean()
    out["rolling_std_3"] = shifted_return.rolling(3).std()

    out["target_next_return"] = out["return"].shift(-1)

    return out


def temporal_train_test_split(
    df: pd.DataFrame,
    split_date: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data by date.

    Train:
    - date < split_date

    Test:
    - date >= split_date
    """
    # TODO:
    # Return train, test
    split_ts = pd.Timestamp(split_date)

    train = df[df["date"] < split_ts].copy()
    test = df[df["date"] >= split_ts].copy()

    return train, test


def prepare_model_data(df: pd.DataFrame):
    """
    Drop rows with missing features/target.

    Features:
    - lag_return_1
    - rolling_mean_3
    - rolling_std_3

    Target:
    - target_next_return
    """
    # TODO:
    # Return X, y
    feature_cols = [
        "lag_return_1",
        "rolling_mean_3",
        "rolling_std_3",
    ]

    model_df = df.dropna(subset = feature_cols + ["target_next_return"])

    X = model_df[feature_cols]
    y = model_df["target_next_return"]

    return X,y


def run_time_series_split(X, y) -> None:
    """
    Demonstrate TimeSeriesSplit.

    This is not for high performance.
    It is for understanding how temporal CV works.
    """
    # TODO:
    # Use TimeSeriesSplit(n_splits=3)
    # Print train/test indices.
    splitter = TimeSeriesSplit(n_splits = 3)

    for fold, (train_idx, test_idx) in enumerate(splitter.split(X), start=1):
        print(f"Fold {fold}")
        print("train indices:", train_idx)
        print("test indices:", test_idx)


def fit_baseline_model(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """
    Fit a simple baseline model.

    Model:
    - RandomForestRegressor

    Metric:
    - mean squared error
    """
    # TODO:
    # Prepare train/test X/y.
    # Fit model.
    # Predict.
    # Print MSE.
    X_train, y_train = prepare_model_data(train)
    X_test, y_test = prepare_model_data(test)

    if len(X_train) == 0 or len(X_test) == 0:
        print("Not enough non-missing rows for modeling.")
        return
    
    model = RandomForestRegressor(
        n_estimators=200,
        random_state = 42,
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    mse = mean_squared_error(y_test, pred)

    print("Predictions:", pred)
    print("True values:", y_test.to_numpy())
    print("Test MSE:", mse)

def main() -> None:
    df = build_price_data()
    print("Raw data:")
    print(df)
    print()

    features = create_return_features(df)
    print("Feature table:")
    print(features)
    print()

    clean_features = features.dropna().reset_index(drop=True)
    X, y = prepare_model_data(clean_features)

    print("TimeSeriesSplit demo:")
    run_time_series_split(X, y)
    print()

    train, test = temporal_train_test_split(
        clean_features,
        split_date="2026-01-10",
    )

    print("Train:")
    print(train)
    print()

    print("Test:")
    print(test)
    print()

    fit_baseline_model(train, test)


if __name__ == "__main__":
    main()