WITH ordered_orders AS (
    SELECT
        user_id,
        order_id,
        order_date,
        amount,

        -- TODO:
        -- chronological order number for each user
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY order_date
        ) AS order_number,

        -- TODO:
        -- previous order amount
        LAG(amount) OVER (
            PARTITION BY user_id
            ORDER BY order_date
        ) AS previous_amount,

        -- TODO:
        -- previous order date
        LAG(order_date) OVER (
            PARTITION BY user_id
            ORDER BY order_date
        ) AS previous_order_date,

        -- TODO:
        -- rolling 3-order average amount
        AVG(amount) OVER(
            PARTITION BY user_id
            ORDER BY order_date
            ROWS BETWEEN 2 PRECEDING
                     AND CURRENT ROW
        ) AS rolling_3_order_mean

    FROM orders
)
SELECT
    *
FROM ordered_orders
ORDER BY
    user_id,
    order_date;