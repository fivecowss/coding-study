import pandas as pd


def build_orders_data() -> pd.DataFrame:
    """
    Create a small toy orders dataset.

    Each row represents one order-level event.
    Grain: one row = one order.
    """

    orders = pd.DataFrame({
        "user_id": [101, 101, 102, 102, 102, 103, 104, 104, 105, 106, 106, 107],
        "order_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "city": [
            "Ann Arbor", "Ann Arbor",
            "Detroit", "Detroit", "Detroit",
            "Chicago",
            "Ann Arbor", "Ann Arbor",
            "Detroit",
            "Chicago", "Chicago",
            "Ann Arbor",
        ],
        "channel": ["web", "app", "web", "app", "web", "app", "web", "app", "web", "app", "web", "web"],
        "amount": [25.0, 35.0, 15.0, 40.0, 30.0, 80.0, 20.0, 22.0, 0.0, 50.0, 70.0, 12.0],
        "converted": [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        "order_date": pd.to_datetime([
            "2026-07-01", "2026-07-03",
            "2026-07-01", "2026-07-02", "2026-07-05",
            "2026-07-03",
            "2026-07-04", "2026-07-06",
            "2026-07-02",
            "2026-07-01", "2026-07-06",
            "2026-07-05",
        ]),
    })

    return orders


def main() -> None:
    orders = build_orders_data()

    print("\n=== Raw orders data ===")
    print(orders)

    print("\n=== Basic dataset checks ===")
    print("Rows:", len(orders))
    print("Unique users:", orders["user_id"].nunique())
    print("Total revenue:", orders["amount"].sum())
    print("Overall conversion rate:", orders["converted"].mean())

    # ------------------------------------------------------------------
    # TODO 1:
    # Create a user-level summary.
    #
    # Required output columns:
    # - user_id
    # - n_orders: number of unique order_id
    # - total_amount: sum of amount
    # - avg_order_value: mean of amount
    # - conversion_rate: mean of converted
    # - first_order_date: min order_date
    # - last_order_date: max order_date
    #
    # Hint:
    # Use groupby("user_id").agg(...).reset_index()
    # ------------------------------------------------------------------

    user_summary = (
        orders.groupby("user_id")
        .agg(
            n_orders = ("order_id", "nunique"),
            total_amount = ("amount", "sum"),
            avg_order_value = ("amount", "mean"),
            conversion_rate = ("converted", "mean"),
            first_order_date = ("order_date", "min"),
            last_order_date = ("order_date", "max"),
        )
        .reset_index()
    )

    print("\n=== User-level summary ===")
    print(user_summary)

    # ------------------------------------------------------------------
    # TODO 2:
    # Create a city-level summary.
    #
    # Required output columns:
    # - city
    # - n_users: number of unique users
    # - n_orders: number of unique orders
    # - total_revenue: sum of amount
    # - avg_order_value: mean of amount
    # - conversion_rate: mean of converted
    #
    # Sort by total_revenue descending.
    # ------------------------------------------------------------------

    city_summary = (
        orders.groupby("city")
        .agg(
            users = ("user_id", "nunique"),
            n_orders = ("order_id", "nunique"),
            total_revenue = ("amount", "sum"),
            avg_order_value = ("amount", "mean"),
            conversion_rate = ("converted", "mean"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    print("\n=== City-level summary ===")
    print(city_summary)

    # ------------------------------------------------------------------
    # TODO 3:
    # Find high-value users.
    #
    # Definition:
    # - total_amount >= 60
    # - n_orders >= 2
    #
    # Use the user_summary created in TODO 1.
    # Sort by total_amount descending, then n_orders descending.
    # ------------------------------------------------------------------

    high_value_users = (
        user_summary[
            (user_summary["total_amount"] >= 60)
            & (user_summary["n_orders"] >= 2)
        ]
        .sort_values(["total_amount", "n_orders"],
                     ascending = [False, False])
    )

    print("\n=== High-value users ===")
    print(high_value_users)

    # ------------------------------------------------------------------
    # TODO 4:
    # Create a channel-level conversion summary.
    #
    # Required output columns:
    # - channel
    # - n_orders
    # - total_revenue
    # - conversion_rate
    #
    # Sort by conversion_rate descending.
    # ------------------------------------------------------------------

    channel_summary = (
        orders.groupby("channel")
        .agg(
            n_orders = ("order_id", "nunique"),
            total_revenue = ("amount", "sum"),
            conversion_rate = ("converted", "mean"),
        )
        .reset_index()
        .sort_values("conversion_rate", ascending = False)
    )

    print("\n=== Channel-level summary ===")
    print(channel_summary)


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# SAMPLE ANSWER
# ----------------------------------------------------------------------
#
# user_summary = (
#     orders
#     .groupby("user_id")
#     .agg(
#         n_orders=("order_id", "nunique"),
#         total_amount=("amount", "sum"),
#         avg_order_value=("amount", "mean"),
#         conversion_rate=("converted", "mean"),
#         first_order_date=("order_date", "min"),
#         last_order_date=("order_date", "max"),
#     )
#     .reset_index()
#     .sort_values("total_amount", ascending=False)
# )
#
# city_summary = (
#     orders
#     .groupby("city")
#     .agg(
#         n_users=("user_id", "nunique"),
#         n_orders=("order_id", "nunique"),
#         total_revenue=("amount", "sum"),
#         avg_order_value=("amount", "mean"),
#         conversion_rate=("converted", "mean"),
#     )
#     .reset_index()
#     .sort_values("total_revenue", ascending=False)
# )
#
# high_value_users = (
#     user_summary[
#         (user_summary["total_amount"] >= 60)
#         & (user_summary["n_orders"] >= 2)
#     ]
#     .sort_values(["total_amount", "n_orders"], ascending=[False, False])
# )
#
# channel_summary = (
#     orders
#     .groupby("channel")
#     .agg(
#         n_orders=("order_id", "nunique"),
#         total_revenue=("amount", "sum"),
#         conversion_rate=("converted", "mean"),
#     )
#     .reset_index()
#     .sort_values("conversion_rate", ascending=False)
# )