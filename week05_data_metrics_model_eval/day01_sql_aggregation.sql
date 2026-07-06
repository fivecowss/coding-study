DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    user_id INTEGER,
    order_id INTEGER,
    city TEXT,
    channel TEXT,
    amount REAL,
    converted INTEGER,
    order_date TEXT
);

INSERT INTO orders (user_id, order_id, city, channel, amount, converted, order_date) VALUES
(101, 1, 'Ann Arbor', 'web', 25.0, 1, '2026-07-01'),
(101, 2, 'Ann Arbor', 'app', 35.0, 1, '2026-07-03'),
(102, 3, 'Detroit', 'web', 15.0, 0, '2026-07-01'),
(102, 4, 'Detroit', 'app', 40.0, 1, '2026-07-02'),
(102, 5, 'Detroit', 'web', 30.0, 1, '2026-07-05'),
(103, 6, 'Chicago', 'app', 80.0, 1, '2026-07-03'),
(104, 7, 'Ann Arbor', 'web', 20.0, 0, '2026-07-04'),
(104, 8, 'Ann Arbor', 'app', 22.0, 1, '2026-07-06'),
(105, 9, 'Detroit', 'web', 0.0, 0, '2026-07-02'),
(106, 10, 'Chicago', 'app', 50.0, 1, '2026-07-01'),
(106, 11, 'Chicago', 'web', 70.0, 1, '2026-07-06'),
(107, 12, 'Ann Arbor', 'web', 12.0, 0, '2026-07-05');

-- Check raw data
SELECT *
FROM orders
ORDER BY order_id;

-- --------------------------------------------------------------------
-- TODO 1:
-- Create a user-level summary.
--
-- Required columns:
-- - user_id
-- - n_orders
-- - total_amount
-- - avg_order_value
-- - conversion_rate
-- - first_order_date
-- - last_order_date
--
-- Sort by total_amount descending.
-- --------------------------------------------------------------------

-- Your query here:
CREATE TABLE user_summary AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS n_orders,
        SUM(amount) AS total_amount,
        AVG(amount) AS avg_order_value,
        AVG(converted) AS conversion_rate,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY user_id
    ORDER BY total_amount DESC
);


-- --------------------------------------------------------------------
-- TODO 2:
-- Create a city-level summary.
--
-- Required columns:
-- - city
-- - n_users
-- - n_orders
-- - total_revenue
-- - avg_order_value
-- - conversion_rate
--
-- Sort by total_revenue descending.
-- --------------------------------------------------------------------

-- Your query here:
CREATE TABLE city_summary AS (
    SELECT
        city,
        COUNT(DISTINCT user_id) AS n_users,
        COUNT(DISTINCT order_id) AS n_orders,
        SUM(amount) AS total_revenue,
        AVG(amount) AS avg_order_value,
        AVG(converted) AS conversion_rate
    FROM orders
    GROUP BY city
    ORDER BY total_revenue DESC
);


-- --------------------------------------------------------------------
-- TODO 3:
-- Find high-value users.
--
-- Definition:
-- - total_amount >= 60
-- - n_orders >= 2
--
-- Hint:
-- Use a CTE called user_summary.
-- --------------------------------------------------------------------

-- Your query here:
SELECT * 
FROM user_summary
WHERE total_amount >= 60
    AND n_orders >= 2
ORDER BY total_amount DESC, n_orders DESC;


-- --------------------------------------------------------------------
-- TODO 4:
-- Create a channel-level conversion summary.
--
-- Required columns:
-- - channel
-- - n_orders
-- - total_revenue
-- - conversion_rate
--
-- Sort by conversion_rate descending.
-- --------------------------------------------------------------------

-- Your query here:
CREATE TABLE channel_summary AS (
    SELECT
        channel,
        COUNT(DISTINCT order_id) AS n_orders,
        SUM(amount) AS total_revenue,
        AVG(converted) AS conversion_rate
    FROM orders
    GROUP BY channel
    ORDER BY conversion_rate DESC
);


-- --------------------------------------------------------------------
-- SAMPLE ANSWER
-- --------------------------------------------------------------------

-- TODO 1 sample:
--
-- SELECT
--     user_id,
--     COUNT(DISTINCT order_id) AS n_orders,
--     SUM(amount) AS total_amount,
--     AVG(amount) AS avg_order_value,
--     AVG(converted) AS conversion_rate,
--     MIN(order_date) AS first_order_date,
--     MAX(order_date) AS last_order_date
-- FROM orders
-- GROUP BY user_id
-- ORDER BY total_amount DESC;

-- TODO 2 sample:
--
-- SELECT
--     city,
--     COUNT(DISTINCT user_id) AS n_users,
--     COUNT(DISTINCT order_id) AS n_orders,
--     SUM(amount) AS total_revenue,
--     AVG(amount) AS avg_order_value,
--     AVG(converted) AS conversion_rate
-- FROM orders
-- GROUP BY city
-- ORDER BY total_revenue DESC;

-- TODO 3 sample:
--
-- WITH user_summary AS (
--     SELECT
--         user_id,
--         COUNT(DISTINCT order_id) AS n_orders,
--         SUM(amount) AS total_amount,
--         AVG(amount) AS avg_order_value,
--         AVG(converted) AS conversion_rate,
--         MIN(order_date) AS first_order_date,
--         MAX(order_date) AS last_order_date
--     FROM orders
--     GROUP BY user_id
-- )
-- SELECT *
-- FROM user_summary
-- WHERE total_amount >= 60
--   AND n_orders >= 2
-- ORDER BY total_amount DESC, n_orders DESC;

-- TODO 4 sample:
--
-- SELECT
--     channel,
--     COUNT(DISTINCT order_id) AS n_orders,
--     SUM(amount) AS total_revenue,
--     AVG(converted) AS conversion_rate
-- FROM orders
-- GROUP BY channel
-- ORDER BY conversion_rate DESC;