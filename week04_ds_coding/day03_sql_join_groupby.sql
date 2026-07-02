/*
Week 4 Day 3: SQL Join and GroupBy Review

Main concepts:
- INNER JOIN
- LEFT JOIN
- GROUP BY after JOIN
- HAVING
- COUNT(column) vs COUNT(*)
- COALESCE
- CASE WHEN
*/


/* -------------------------------------------------------------
   0. Sample table setup
   ------------------------------------------------------------- */

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER,
    name VARCHAR(50),
    country VARCHAR(10)
);

CREATE TABLE orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    status VARCHAR(20)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    amount INTEGER
);

INSERT INTO customers (customer_id, name, country) VALUES
    (1, 'Alice', 'US'),
    (2, 'Bob', 'US'),
    (3, 'Cathy', 'KR'),
    (4, 'David', 'KR'),
    (5, 'Eve', 'CA');

INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
    (101, 1, '2026-07-01', 'completed'),
    (102, 2, '2026-07-01', 'completed'),
    (103, 2, '2026-07-02', 'cancelled'),
    (104, 3, '2026-07-03', 'completed'),
    (105, 1, '2026-07-04', 'completed');

INSERT INTO order_items (order_id, product_id, amount) VALUES
    (101, 1001, 50),
    (101, 1002, 70),
    (102, 1001, 80),
    (103, 1003, 20),
    (104, 1002, 100),
    (105, 1001, 60);


/* -------------------------------------------------------------
   1. Basic INNER JOIN

   Question:
   Return each order with customer name and country.

   Key idea:
   INNER JOIN keeps only matching rows.
   ------------------------------------------------------------- */

SELECT
    o.order_id,
    o.order_date,
    o.status,
    c.customer_id,
    c.name,
    c.country
FROM orders AS o
INNER JOIN customers AS c
    ON o.customer_id = c.customer_id
ORDER BY o.order_id;


/* -------------------------------------------------------------
   2. LEFT JOIN and customers without orders

   Question:
   Return customers who have no orders.

   Pattern:
   LEFT JOIN + WHERE right_table.key IS NULL

   This is the SQL version of pandas anti-join.
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;


/* -------------------------------------------------------------
   3. Total completed order amount by customer

   Question:
   For each customer, compute total amount from completed orders only.

   Step logic:
   1. customers LEFT JOIN orders
   2. join order_items
   3. count only completed orders
   4. replace NULL total with 0

   Important:
   Filtering completed orders in WHERE would remove customers with no orders.
   To keep all customers, use conditional aggregation.
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name,
    COALESCE(
        SUM(
            CASE
                WHEN o.status = 'completed' THEN oi.amount
                ELSE 0
            END
        ),
        0
    ) AS completed_total_amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
LEFT JOIN order_items AS oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.name
ORDER BY completed_total_amount DESC;


/* -------------------------------------------------------------
   4. Number of completed orders by customer

   Question:
   Count completed orders per customer.

   Important:
   One order can have multiple order_items.
   If we join to order_items and count o.order_id directly,
   an order with two items may be counted twice.

   Safer:
   Use COUNT(DISTINCT CASE WHEN ... THEN o.order_id END)
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name,
    COUNT(
        DISTINCT CASE
            WHEN o.status = 'completed' THEN o.order_id
        END
    ) AS n_completed_orders
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
LEFT JOIN order_items AS oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.name
ORDER BY n_completed_orders DESC;


/* -------------------------------------------------------------
   5. Customers with completed total amount >= 100

   Question:
   Return customers whose completed order amount is at least 100.

   Key idea:
   Aggregate filtering uses HAVING.
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name,
    SUM(
        CASE
            WHEN o.status = 'completed' THEN oi.amount
            ELSE 0
        END
    ) AS completed_total_amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
LEFT JOIN order_items AS oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.name
HAVING
    SUM(
        CASE
            WHEN o.status = 'completed' THEN oi.amount
            ELSE 0
        END
    ) >= 100
ORDER BY completed_total_amount DESC;


/* -------------------------------------------------------------
   6. Revenue by country

   Question:
   Compute completed revenue by country.

   This is common in DS analytics interviews:
   group by a dimension after joining fact tables.
   ------------------------------------------------------------- */

SELECT
    c.country,
    SUM(
        CASE
            WHEN o.status = 'completed' THEN oi.amount
            ELSE 0
        END
    ) AS completed_revenue
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
LEFT JOIN order_items AS oi
    ON o.order_id = oi.order_id
GROUP BY c.country
ORDER BY completed_revenue DESC;


/* -------------------------------------------------------------
   7. LeetCode-style exercise: Confirmation Rate pattern

   Concept:
   conditional average / conditional count

   Suppose:
   - action = 'confirmed' or 'timeout'

   General pattern:
   AVG(CASE WHEN action = 'confirmed' THEN 1.0 ELSE 0.0 END)

   Practice query below uses order status instead.
   Compute completion rate by country.
   ------------------------------------------------------------- */

SELECT
    c.country,
    AVG(
        CASE
            WHEN o.status = 'completed' THEN 1.0
            ELSE 0.0
        END
    ) AS completed_order_rate
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY completed_order_rate DESC;
