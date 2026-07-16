-- Day 1: SQL Feature Table

-- Goal:
-- Build a user-level feature table from an order-level table.

-- orders table:
-- user_id
-- order_id
-- amount
-- category
-- order_date

-- TODO 1:
-- Create user-level features:
-- - n_orders
-- - total_amount
-- - avg_amount
-- - max_amount
-- - n_categories
-- - first_order_date
-- - last_order_date

SELECT
    user_id,
    -- TODO: number of distinct orders
    COUNT(DISTINCT order_id) AS n_orders,
    -- TODO: total amount with missing amount handled
    SUM(COALESCE(amount, 0)) AS total_amount,
    -- TODO: average amount
    AVG(amount) AS avg_amount,
    -- TODO: maximum amount
    MAX(amount) AS max_amount,
    -- TODO: number of distinct categories
    COUNT(DISTINCT COALESCE(category, 'unknown')) AS n_categories,
    -- TODO: first order date
    MIN(order_date) AS first_order_date,
    -- TODO: last order date
    MAX(order_date) AS last_order_date
FROM orders
GROUP BY user_id;


-- TODO 2:
-- Join user_features with user_profiles.

WITH user_features AS (
    SELECT
        user_id
        -- TODO: add feature columns
        COUNT(DISTINCT order_id) AS n_orders,
        SUM(COALESCE(amount, 0)) AS total_amount,
        AVG(amount) AS avg_amount,
        MAX(amount) AS max_amount,
        COUNT(DISTINCT COALESCE(category, 'unknown')) AS n_categories,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY user_id
)
SELECT
    uf.*,
    up.country,
    up.signup_channel
FROM user_features uf
LEFT JOIN user_profiles up
    ON uf.user_id = up.user_id;