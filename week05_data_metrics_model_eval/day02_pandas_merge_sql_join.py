import pandas as pd


def build_customers() -> pd.DataFrame:
    return pd.DataFrame({
        "customer_id": [1, 2, 3, 4, 5],
        "customer_name": ["Amy", "Bob", "Cara", "Dan", "Eun"],
        "city": ["Ann Arbor", "Detroit", "Chicago", "Ann Arbor", "Detroit"],
        "signup_date": pd.to_datetime([
            "2026-07-01",
            "2026-07-01",
            "2026-07-02",
            "2026-07-03",
            "2026-07-04",
        ]),
    })


def build_orders() -> pd.DataFrame:
    """Each row is one order."""
    return pd.DataFrame({
        "order_id": [101, 102, 103, 104, 105, 106, 107],
        "customer_id": [1, 1, 2, 2, 3, 4, 4],
        "product_id": [10, 20, 10, 30, 20, 30, 40],
        "amount": [25.0, 35.0, 15.0, 40.0, 80.0, 20.0, 22.0],
        "order_date": pd.to_datetime([
            "2026-07-01",
            "2026-07-03",
            "2026-07-01",
            "2026-07-02",
            "2026-07-03",
            "2026-07-04",
            "2026-07-06",
        ]),
    })


def build_products() -> pd.DataFrame:
    """Each row is one product."""
    return pd.DataFrame({
        "product_id": [10, 20, 30, 40],
        "product_name": ["Coffee", "Notebook", "Backpack", "Pen"],
        "category": ["Food", "Stationery", "Bags", "Stationery"],
    })


def main() -> None:
    customers = build_customers()
    orders = build_orders()
    products = build_products()

    print("\n=== Customers ===")
    print(customers)

    print("\n=== Orders ===")
    print(orders)

    print("\n=== Products ===")
    print(products)

    print("\n=== Grain checks ===")
    print("customers rows:", len(customers), "| unique customers:", customers["customer_id"].nunique())
    print("orders rows:", len(orders), "| unique orders:", orders["order_id"].nunique())
    print("products rows:", len(products), "| unique products:", products["product_id"].nunique())

    # ------------------------------------------------------------------
    # TODO 1:
    # Left join customers and orders.
    #
    # Question:
    # Which customers have no orders?
    #
    # Required output:
    # - customer_id
    # - customer_name
    # - city
    #
    # Hint:
    # Use merge(..., how="left", indicator=True)
    # Then filter _merge == "left_only".
    # ------------------------------------------------------------------

    customer_orders = customers.merge(
        orders,
        on = "customer_id",
        how = "left",
        indicator = True,
    )
    no_order_customers = (
        customer_orders[customer_orders["_merge"] == "left_only"]
        [["customer_id", "customer_name", "city"]]
    )


    print("\n=== Customer-orders left join ===")
    print(customer_orders)

    print("\n=== Customers with no orders ===")
    print(no_order_customers)

    # ------------------------------------------------------------------
    # TODO 2:
    # Join orders with products.
    #
    # Question:
    # What product/category does each order belong to?
    #
    # Required output:
    # - order_id
    # - customer_id
    # - product_id
    # - product_name
    # - category
    # - amount
    #
    # Hint:
    # Use orders.merge(products, on="product_id", how="left")
    # ------------------------------------------------------------------

    order_products = orders.merge(
        products,
        on = "product_id",
        how = "left",
    )
    

    print("\n=== Order-products table ===")
    print(order_products)

    # ------------------------------------------------------------------
    # TODO 3:
    # Create category-level revenue summary.
    #
    # Required output:
    # - category
    # - n_orders
    # - total_revenue
    # - avg_order_value
    #
    # Sort by total_revenue descending.
    # ------------------------------------------------------------------

    category_summary = (
        order_products
        .groupby("category")
        .agg(
            n_orders = ("order_id", "nunique"),
            total_revenue = ("amount", "sum"),
            avg_order_value = ("amount", "mean"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending = False)
    )

    print("\n=== Category-level revenue summary ===")
    print(category_summary)

    # ------------------------------------------------------------------
    # TODO 4:
    # Create customer-level purchase summary.
    #
    # Use customer_orders, but be careful:
    # after left join, customers with no orders have NaN order_id.
    #
    # Required output:
    # - customer_id
    # - customer_name
    # - city
    # - n_orders
    # - total_spend
    #
    # Replace missing total_spend with 0.
    # Sort by total_spend descending.
    # ------------------------------------------------------------------

    customer_summary = (
        customer_orders
        .groupby(["customer_id", "customer_name", "city"])
        .agg(
            n_orders = ("order_id", "nunique"),
            total_spend = ("amount", "sum")
        )
        .reset_index()
    )
    customer_summary["total_spend"] = customer_summary["total_spend"].fillna(0)

    customer_summary = customer_summary.sort_values(
        ["total_spend", "n_orders"],
        ascending = [False, False],
    )

    print("\n=== Customer-level purchase summary ===")
    print(customer_summary)

    # ------------------------------------------------------------------
    # TODO 5:
    # Find repeat customers.
    #
    # Definition:
    # - n_orders >= 2
    #
    # Use customer_summary.
    # ------------------------------------------------------------------

    repeat_customers = customer_summary[customer_summary["n_orders"] >= 2]

    print("\n=== Repeat customers ===")
    print(repeat_customers)


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# SAMPLE ANSWER
# ----------------------------------------------------------------------
#
# customer_orders = customers.merge(
#     orders,
#     on="customer_id",
#     how="left",
#     indicator=True,
# )
#
# no_order_customers = (
#     customer_orders[customer_orders["_merge"] == "left_only"]
#     [["customer_id", "customer_name", "city"]]
# )
#
# order_products = orders.merge(
#     products,
#     on="product_id",
#     how="left",
# )
#
# category_summary = (
#     order_products
#     .groupby("category")
#     .agg(
#         n_orders=("order_id", "nunique"),
#         total_revenue=("amount", "sum"),
#         avg_order_value=("amount", "mean"),
#     )
#     .reset_index()
#     .sort_values("total_revenue", ascending=False)
# )
#
# customer_summary = (
#     customer_orders
#     .groupby(["customer_id", "customer_name", "city"])
#     .agg(
#         n_orders=("order_id", "nunique"),
#         total_spend=("amount", "sum"),
#     )
#     .reset_index()
# )
#
# customer_summary["total_spend"] = customer_summary["total_spend"].fillna(0)
#
# customer_summary = customer_summary.sort_values(
#     ["total_spend", "n_orders"],
#     ascending=[False, False],
# )
#
# repeat_customers = customer_summary[customer_summary["n_orders"] >= 2]