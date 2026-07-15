"""
Day 1: Feature Engineering with pandas

Goal:
- Build user-level features from raw order-level data.
- Handle missing numeric and categorical values.
- Practice groupby, agg, reset_index, and merge.
"""

import pandas as pd


def build_raw_orders() -> pd.DataFrame:
    """
    Create a toy order-level dataset.

    Each row is one order.
    The target feature table should be user-level.
    """
    # TODO:
    # Return a DataFrame with columns:
    # user_id, order_id, amount, category, order_date
    return pd.DataFrame({
        "user_id": [1, 1, 2, 2, 3, 4, 4],
        "order_id": [101, 102, 103, 104,105, 106,107],
        "amount": [20.0, 35.0, 15.0, 40.0, None, 25.0, 30.0],
        "category":[
            "books",
            "food",
            "food",
            "electroninc",
            "books",
            None,
            "food"
            ],
            "order_date": pd.to_datetime([
                "2026-01-01",
                "2026-01-03",
                "2026-01-02",
                "2026-01-05",
                "2026-01-03",
                "2026-01-04",
                "2026-01-07",
            ]),                       
        })


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values.

    Numeric:
    - Fill missing amount with the median amount.

    Categorical:
    - Fill missing category with "unknown".
    """
    # TODO:
    # 1. Copy the input DataFrame.
    # 2. Compute median amount.
    # 3. Fill missing amount.
    # 4. Fill missing category.
    # 5. Return cleaned DataFrame.
    cleaned = orders.copy()
    amount_median = cleaned["amount"].median()
    cleaned["amount_filled"] = cleaned["amount"].fillna(amount_median)
    cleaned["category_filled"] = cleaned["category"].fillna("unknown")
    return cleaned


def build_user_features(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Build user-level feature table.

    Required features:
    - n_orders
    - total_amount
    - avg_amount
    - max_amount
    - n_categories
    - first_order_date
    - last_order_date
    """
    # TODO:
    # Use groupby("user_id").agg(...)
    # Reset index before returning.
    user_features = (
        orders
        .groupby("user_id")
        .agg(
            n_orders = ("order_id", "nunique"),
            total_amount = ("amount_filled","sum"),
            avg_amount = ("amount_filled", "mean"),
            max_amount = ("amount_filled", "max"),
            n_categories = ("category_filled", "nunique"),
            first_order_date = ("order_date", "min"),
            last_order_date = ("order_date", "max"),
        )
        .reset_index()
    )
    return user_features

def add_user_profile_features(
    user_features: pd.DataFrame,
    user_profiles: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join user-level features with user profile table.

    Required:
    - left join user_features with user_profiles
    - keep all users from user_features
    """
    # TODO:
    # Use pandas merge.
    return user_features.merge(
        user_profiles,
        on = "user_id",
        how = "left",
    )


def main() -> None:
    orders = build_raw_orders()
    print("Raw orders:")
    print(orders)
    print()

    cleaned = clean_orders(orders)
    print("Cleaned orders:")
    print(cleaned)
    print()

    user_features = build_user_features(cleaned)
    print("User-level features:")
    print(user_features)
    print()

    user_profiles = pd.DataFrame({
        "user_id": [1, 2, 3, 4],
        "country": ["US", "US", "KR", "US"],
        "signup_channel": ["organic", "paid", "organic", "referral"],
    })

    final_features = add_user_profile_features(user_features, user_profiles)
    print("Final feature table:")
    print(final_features)


if __name__ == "__main__":
    main()