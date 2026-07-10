-- week05_data_metrics_model_eval/day02_sql_join_anti_join.sql
--
-- Week 5 Day 2: SQL joins and anti-joins
--
-- Goal:
-- - Practice LEFT JOIN, INNER JOIN, anti-join, GROUP BY.
-- - Use the same structure as the pandas script.
--
-- Suggested environment:
-- - DBeaver + SQLite

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;

CREATE TABLE customers (
    customer_id INTEGER,
    customer_name TEXT,
    city TEXT,
    signup_date TEXT
);

CREATE TABLE orders (
    order_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    amount REAL,
    order_date TEXT
);

CREATE TABLE products (
    product_id INTEGER,
    product_name TEXT,
    category TEXT
);

INSERT INTO customers VALUES
(1, 'Amy', 'Ann Arbor', '2026-07-01'),
(2, 'Bob', 'Detroit', '2026-07-01'),
(3, 'Cara', 'Chicago', '2026-07-02'),
(4, 'Dan', 'Ann Arbor', '2026-07-03'),
(5, 'Eun', 'Detroit', '2026-07-04');

INSERT INTO orders VALUES
(101, 1, 10, 25.0, '2026-07-01'),
(102, 1, 20, 35.0, '2026-07-03'),
(103, 2, 10, 15.0, '2026-07-01'),
(104, 2, 30, 40.0, '2026-07-02'),
(105, 3, 20, 80.0, '2026-07-03'),
(106, 4, 30, 20.0, '2026-07-04'),
(107, 4, 40, 22.0, '2026-07-06');

INSERT INTO products VALUES
(10, 'Coffee', 'Food'),
(20, 'Notebook', 'Stationery'),
(30, 'Backpack', 'Bags'),
(40, 'Pen', 'Stationery');

-- Raw checks
SELECT * FROM customers;
SELECT * FROM orders;
SELECT * FROM products;

-- --------------------------------------------------------------------
-- TODO 1:
-- Find customers with no orders.
--
-- Required columns:
-- - customer_id
-- - customer_name
-- - city
--
-- Hint:
-- LEFT JOIN orders and filter WHERE o.order_id IS NULL.
-- --------------------------------------------------------------------

-- Your query here:
SELECT 
    c.customer_id,
    c.customer_name,
    c.city
FROM customer c 
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order IS NULL;


-- --------------------------------------------------------------------
-- TODO 2:
-- Join orders with products.
--
-- Required columns:
-- - order_id
-- - customer_id
-- - product_id
-- - product_name
-- - category
-- - amount
-- --------------------------------------------------------------------

-- Your query here:
SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    p.product_name,
    p.category,
    o.amount
FROM orders o
LEFT JOIN products p
    ON o.product_id = p.product_id
ORDER BY o.order_id;


-- --------------------------------------------------------------------
-- TODO 3:
-- Category-level revenue summary.
--
-- Required columns:
-- - category
-- - n_orders
-- - total_revenue
-- - avg_order_value
--
-- Sort by total_revenue descending.
-- --------------------------------------------------------------------

-- Your query here:
SELECT
    p.category,
    COUNT(DISTINCT  o.order_id) AS n_orders,
    SUM(o.omount) AS total_revenue,
    AVG(o.amount) AS avg_order_value
FROM orders o
LEFT JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- --------------------------------------------------------------------
-- TODO 4:
-- Customer-level purchase summary.
--
-- Required columns:
-- - customer_id
-- - customer_name
-- - city
-- - n_orders
-- - total_spend
--
-- Include customers with no orders.
-- Missing total_spend should become 0.
-- --------------------------------------------------------------------

-- Your query here:
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS n_orders,
    COALESCE(SUM(o.amount), 0) AS total_spend
FROM customer c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spend DESC, n_orders DESC;


-- --------------------------------------------------------------------
-- TODO 5:
-- Repeat customers.
--
-- Definition:
-- - n_orders >= 2
--
-- Hint:
-- Use a CTE named customer_summary.
-- --------------------------------------------------------------------

-- Your query here:
WITH customer_summary AS(
    SELECT
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(DISTINCT o.order_id) AS n_orders,
        COALESCE(SUM(o.amount), 0) AS total_spend
    FROM customer c
    LEFT JOIN orders o
        on c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.city
)
SELECT *
FROM customer_summary
WHERE n_orders >= 2
ORDER BY total_spend DESC, n_oders DESC;


-- --------------------------------------------------------------------
-- SAMPLE ANSWER
-- --------------------------------------------------------------------

-- TODO 1 sample:
--
-- SELECT
--     c.customer_id,
--     c.customer_name,
--     c.city
-- FROM customers c
-- LEFT JOIN orders o
--     ON c.customer_id = o.customer_id
-- WHERE o.order_id IS NULL;

-- TODO 2 sample:
--
-- SELECT
--     o.order_id,
--     o.customer_id,
--     o.product_id,
--     p.product_name,
--     p.category,
--     o.amount
-- FROM orders o
-- LEFT JOIN products p
--     ON o.product_id = p.product_id
-- ORDER BY o.order_id;

-- TODO 3 sample:
--
-- SELECT
--     p.category,
--     COUNT(DISTINCT o.order_id) AS n_orders,
--     SUM(o.amount) AS total_revenue,
--     AVG(o.amount) AS avg_order_value
-- FROM orders o
-- LEFT JOIN products p
--     ON o.product_id = p.product_id
-- GROUP BY p.category
-- ORDER BY total_revenue DESC;

-- TODO 4 sample:
--
-- SELECT
--     c.customer_id,
--     c.customer_name,
--     c.city,
--     COUNT(DISTINCT o.order_id) AS n_orders,
--     COALESCE(SUM(o.amount), 0) AS total_spend
-- FROM customers c
-- LEFT JOIN orders o
--     ON c.customer_id = o.customer_id
-- GROUP BY c.customer_id, c.customer_name, c.city
-- ORDER BY total_spend DESC, n_orders DESC;

-- TODO 5 sample:
--
-- WITH customer_summary AS (
--     SELECT
--         c.customer_id,
--         c.customer_name,
--         c.city,
--         COUNT(DISTINCT o.order_id) AS n_orders,
--         COALESCE(SUM(o.amount), 0) AS total_spend
--     FROM customers c
--     LEFT JOIN orders o
--         ON c.customer_id = o.customer_id
--     GROUP BY c.customer_id, c.customer_name, c.city
-- )
-- SELECT *
-- FROM customer_summary
-- WHERE n_orders >= 2
-- ORDER BY total_spend DESC, n_orders DESC;