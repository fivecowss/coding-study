import pandas as pd


def build_customers() -> pd.DataFrame:
    """
    Create customer table.

    New concept:
    - This is similar to a SQL table.
    - customer_id is the key column.
    """
    customers = pd.DataFrame({
        "customer_id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Cathy", "David", "Eve"],
        "country": ["US", "US", "KR", "KR", "CA"],
    })
    return customers


def build_orders() -> pd.DataFrame:
    """
    Create order table.

    New concept:
    - A customer may have multiple orders.
    - Some customers may have no orders.
    """
    orders = pd.DataFrame({
        "order_id": [101, 102, 103, 104, 105],
        "customer_id": [1, 2, 2, 3, 1],
        "amount": [50, 80, 20, 100, 70],
    })
    return orders


def left_join_customers_orders(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """
    Task:
    Left join customers with orders.

    New concepts:
    - merge:
        customers.merge(orders, on="customer_id", how="left")

    Meaning:
    - Keep all rows from customers.
    - Attach matching rows from orders.
    - If a customer has no order, order columns become NaN.

    Simulation example:
    customers:
        customer_id = 4, name = David

    orders:
        no row with customer_id = 4

    left join result:
        David remains in the output.
        order_id = NaN, amount = NaN
    """
    # TODO: return left join result
    return customers.merge(
        orders,
        on = "customer_id",
        how = "left"
    )


def inner_join_customers_orders(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """
    Task:
    Inner join customers with orders.

    Meaning:
    - Keep only customers who have matching orders.
    - Customers without orders disappear.

    Direction:
    - Use how="inner".
    """
    # TODO: return inner join result
    return customers.merge(
        orders,
        on = "customer_id",
        how = "inner"
    )


def find_customers_without_orders(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """
    Task:
    Return customers who never placed an order.

    Pattern:
    1. Left join customers with orders.
    2. Keep rows where order_id is NaN.
    3. Select customer_id and name.

    New concepts:
    - isna():
        checks missing values.
    - Anti-join:
        rows in left table with no match in right table.
    """
    # TODO:
    # 1. left join
    # 2. filter where order_id is missing
    # 3. return customer_id and name
    customer_orders = customers.merge(
        orders,
        on = "customer_id",
        how = "left"
    )
    return customer_orders[customer_orders["order_id"].isna()][["customer_id", "name"]]

def summarize_order_amount_by_customer(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
) -> pd.DataFrame:
    """
    Task:
    For each customer, compute total order amount.

    Direction:
    - Left join customers and orders.
    - Group by customer_id and name.
    - Sum amount.
    - Missing order amount should become 0.

    New concepts:
    - fillna(0): replace missing values with 0.
    - groupby(["customer_id", "name"])
    - agg(total_amount=("amount", "sum"))

    Simulation example:
    Alice has orders:
        50 and 70
        total = 120

    David has no orders:
        amount = NaN after left join
        after fillna(0), total = 0
    """
    # TODO:
    # 1. left join
    # 2. fill amount missing values with 0
    # 3. group by customer_id and name
    # 4. compute total_amount
    customer_orders = customers.merge(
        orders,
        on = "customer_id",
        how = "left"
    )
    customer_orders["amount"] = customer_orders["amount"].fillna(0)
    return (
        customer_orders.groupby(["customer_id", "name"])
        .agg(total_amount = ("amount", "sum"))
        .reset_index()
        .sort_values("total_amount", ascending = False)
    )


def main() -> None:
    customers = build_customers()
    orders = build_orders()

    print("Customers")
    print(customers)

    print("\nOrders")
    print(orders)

    print("\nTODO 1: Left join")
    print(left_join_customers_orders(customers, orders))

    print("\nTODO 2: Inner join")
    print(inner_join_customers_orders(customers, orders))

    print("\nTODO 3: Customers without orders")
    print(find_customers_without_orders(customers, orders))

    print("\nTODO 4: Order amount summary")
    print(summarize_order_amount_by_customer(customers, orders))


if __name__ == "__main__":
    main()


# -------------------------------------------------------------------
# SAMPLE ANSWER — REFERENCE ONLY
# Keep this section commented out while practicing.
# -------------------------------------------------------------------

# def left_join_customers_orders(
#     customers: pd.DataFrame,
#     orders: pd.DataFrame,
# ) -> pd.DataFrame:
#     return customers.merge(
#         orders,
#         on="customer_id",
#         how="left",
#     )
#
#
# def inner_join_customers_orders(
#     customers: pd.DataFrame,
#     orders: pd.DataFrame,
# ) -> pd.DataFrame:
#     return customers.merge(
#         orders,
#         on="customer_id",
#         how="inner",
#     )
#
#
# def find_customers_without_orders(
#     customers: pd.DataFrame,
#     orders: pd.DataFrame,
# ) -> pd.DataFrame:
#     joined = customers.merge(
#         orders,
#         on="customer_id",
#         how="left",
#     )
#
#     no_orders = joined[joined["order_id"].isna()]
#
#     return no_orders[["customer_id", "name"]]
#
#
# def summarize_order_amount_by_customer(
#     customers: pd.DataFrame,
#     orders: pd.DataFrame,
# ) -> pd.DataFrame:
#     joined = customers.merge(
#         orders,
#         on="customer_id",
#         how="left",
#     )
#
#     joined["amount"] = joined["amount"].fillna(0)
#
#     return (
#         joined.groupby(["customer_id", "name"])
#         .agg(total_amount=("amount", "sum"))
#         .reset_index()
#         .sort_values("total_amount", ascending=False)
#     )