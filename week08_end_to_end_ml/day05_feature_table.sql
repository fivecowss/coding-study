/*
CAPSTONE FEATURE TABLE

Problem:
Create one row per customer at a prediction cutoff.

Use only information available on or before
2026-01-31.

Output features:
- user_id
- n_orders
- total_amount
- avg_amount
- days_since_last_order

Important:
Customers with no historical orders must remain
in the output.
*/


WITH eligible_orders AS (

    -- TODO:
    -- Keep only orders available at cutoff.
    SELECT
        order_id,
        user_id,
        order_date,
        amount
    FROM orders
    WHERE order_date <= DATE '2026-01-31'
),

order_features AS (

    -- TODO:
    -- Aggregate historical orders by user_id.
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS n_orders,
        SUM(amount) AS total_amount,
        AVG(amount) AS avg_amount,
        MAX(order_date) AS last_order_date
    FROM eligible_orders
    GROUP BY user_id

)

SELECT
    -- TODO:
    -- Start from users.
    -- LEFT JOIN order_features.
    -- Handle missing counts/totals.
    u.user_id,
    COALESCE(
        f.total_amount,
        0.0
    ) AS total_amount,
    f.avg_amount,
    f.last_order_Date,
    DATE '2026-01-31'
        - f.last_order_date AS days_since_last_order
FROM users AS u
LEFT JOIN order_features AS f
    ON u.user_id = f.user_id
ORDER BY u.user_id;
