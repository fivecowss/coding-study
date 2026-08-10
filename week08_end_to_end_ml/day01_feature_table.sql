WITH eligible_orders AS (
    SELECT
        order_id,
        user_id,
        order_date,
        amount
    FROM orders
    WHERE order_date <= DATE '2026-01-31'
),
order_features AS (
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
    u.user_id,
    u.country,
    u.acquisition_channel,
    COALESCE(f.n_orders, 0) AS n_orders,
    COALESCE(f.total_amount, 0.0) AS total_amount,
    f.avg_amount,
    f.last_order_date,
    DATE '2026-01-31' - f.last_order_date
        AS days_since_last_order
FROM users AS u
LEFT JOIN order_features AS f
    ON u.user_id = f.user_id
ORDER BY u.user_id;