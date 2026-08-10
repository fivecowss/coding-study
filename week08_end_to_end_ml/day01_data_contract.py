from collections.abc import Iterable

import pandas as pd


USER_REQUIRED_COLUMNS = {
    "user_id",
    "country",
    "acquisition_channel",
}

ORDER_REQUIRED_COLUMNS = {
    "order_id",
    "user_id",
    "order_date",
    "amount",
}


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: Iterable[str],
    table_name: str,
) -> None:
    """
    Raise ValueError if required columns are missing.
    """

    # TODO:
    # 1. Convert required_columns to a set.
    # 2. Compare it with df.columns.
    # 3. Raise ValueError when columns are missing.
    required = set(required_columns)
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"{table_name}: missing required columns: "
            f"{sorted(missing)}"
        )


def validate_non_null_key(
    df: pd.DataFrame,
    key_columns: list[str],
    table_name: str,
) -> None:
    """
    Raise ValueError if any key column contains a missing value.
    """

    # TODO:
    # Use isna().any().any() on the key columns.
    has_missing_key = (
        df[key_columns]
        .isna()
        .any()
        .any()
    )

    if has_missing_key:
        raise ValueError(
            f"{table_name}: key columns contain missing values: "
            f"{key_columns}"
        )


def validate_unique_key(
    df: pd.DataFrame,
    key_columns: list[str],
    table_name: str,
) -> None:
    """
    Raise ValueError if the declared key is duplicated.
    """

    # TODO:
    # 1. Use duplicated(..., keep=False).
    # 2. Extract several duplicate examples.
    # 3. Raise ValueError if duplicates exist.
    duplicated = df.duplicated(
        subset = key_columns,
        keep = False,
    )

    if duplicated.any():
        examples = (
            df.loc[duplicated, key_columns]
            .head()
            .to_dict("records")
        )


def filter_orders_at_cutoff(
    orders: pd.DataFrame,
    cutoff_date: str,
) -> pd.DataFrame:
    """
    Convert order_date to datetime and retain only rows
    available at the prediction cutoff.
    """

    # TODO:
    # 1. Copy the input.
    # 2. Parse order_date.
    # 3. Convert cutoff_date to pd.Timestamp.
    # 4. Keep rows with order_date <= cutoff.
    frame = orders.copy()

    frame["order_date"] = pd.to_datetime(
        frame["order_date"],
        errors = "raise",
    )

    cutoff = pd.Timestamp(cutoff_date)

    eligible = frame.loc[
        frame["order_date"] <= cutoff
    ].copy()

    return eligible


def build_user_features(
    users: pd.DataFrame,
    orders: pd.DataFrame,
    cutoff_date: str,
) -> pd.DataFrame:
    """
    Return one row per user using only eligible historical orders.
    """

    # TODO:
    # 1. Validate users and orders schemas.
    # 2. Validate primary keys.
    # 3. Filter orders at cutoff.
    # 4. Aggregate order features by user_id.
    # 5. LEFT JOIN aggregated features onto users.
    # 6. Fill n_orders and total_amount for users with no orders.
    # 7. Compute days_since_last_order.
    # 8. Validate that user_id is unique in the final table.
    validate_required_columns(
        users,
        USER_REQUIRED_COLUMNS,
        "users",
    )

    validate_required_columns(
        orders,
        ORDER_REQUIRED_COLUMNS,
        "orders",
    )

    validate_non_null_key(
        users,
        ["user_id"],
        "users",
    )

    validate_non_null_key(
        orders,
        ["order_id"],
        "orders",
    )

    validate_unique_key(
        orders,
        ["order_id"],
        "orders",
    )

    users_frame = users.copy()

    eligible_orders = filter_orders_at_cutoff(
        orders=orders,
        cutoff_date = cutoff_date,
    )

    order_features = (
        eligible_orders
        .groupby(
            "user_id",
            as_index = False,
        )
        .agg(
            n_orders = ("order_id", "nunique"),
            total_amount = ('amount', 'sum'),
            avg_amount = ('amount', 'mean'),
            last_order_date = ('order_date', 'max')
        )
    )

    features = users_frame.merge(
        order_features,
        on = 'user_id',
        how = 'left',
        validate = 'one_to_one',
    )

    features['n_orders'] = (
        features['n_orders']
        .fillna(0)
        .astype(int)
    )

    features['total_amount'] = (
        features['total_amount']
        .fillna(0.0)
    )

    cutoff = pd.Timestamp(cutoff_date)

    features["days_since_last_order"] = (
        cutoff - features['last_order_date']
    ).dt.days

    validate_unique_key(
        features,
        ["user_id"],
        "feature_table",
    )

    ordered_columns = [
        "user_id",
        "country",
        "acquisition_channel",
        "n_orders",
        "total_amount",
        "avg_amount",
        "last_order_date",
        "days_since_last_order",
    ]
    return features[ordered_columns]


def make_example_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    users = pd.DataFrame({
        "user_id": [1, 2, 3],
        "country": ["US", "CA", "US"],
        "acquisition_channel": [
            "search",
            "referral",
            "social",
        ],
    })

    orders = pd.DataFrame({
        "order_id": [101, 102, 201, 202],
        "user_id": [1, 1, 2, 2],
        "order_date": [
            "2026-01-10",
            "2026-02-10",
            "2026-01-05",
            "2026-01-20",
        ],
        "amount": [20.0, 1000.0, 15.0, 25.0],
    })

    return users, orders


def main() -> None:
    users, orders = make_example_data()

    features = build_user_features(
        users=users,
        orders=orders,
        cutoff_date="2026-01-31",
    )

    print("Users:")
    print(users)
    print()

    print("Orders:")
    print(orders)
    print()

    print("Feature table:")
    print(features)


if __name__ == "__main__":
    main()