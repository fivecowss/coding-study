/* -------------------------------------------------------------
   0. Sample table setup
   ------------------------------------------------------------- */

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
    amount INTEGER
);

INSERT INTO customers (customer_id, name, country) VALUES
    (1, 'Alice', 'US'),
    (2, 'Bob', 'US'),
    (3, 'Cathy', 'KR'),
    (4, 'David', 'KR'),
    (5, 'Eve', 'CA');

INSERT INTO orders (order_id, customer_id, amount) VALUES
    (101, 1, 50),
    (102, 2, 80),
    (103, 2, 20),
    (104, 3, 100),
    (105, 1, 70);


/* -------------------------------------------------------------
   1. INNER JOIN

   Question:
   Return customers who have at least one order.

   Meaning:
   - Keep only rows where customer_id exists in both tables.
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name,
    c.country,
    o.order_id,
    o.amount
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;


/* -------------------------------------------------------------
   2. LEFT JOIN

   Question:
   Return all customers and attach their orders if available.

   Meaning:
   - Keep every customer.
   - If there is no matching order, order_id and amount become NULL.
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name,
    c.country,
    o.order_id,
    o.amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;


/* -------------------------------------------------------------
   3. Anti-join pattern

   Question:
   Return customers who never placed an order.

   Pattern:
   1. LEFT JOIN
   2. Keep rows where right table key is NULL
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;


/* -------------------------------------------------------------
   4. GROUP BY after join

   Question:
   For each customer, compute total order amount.

   Important:
   - Customers without orders should still appear.
   - Use COALESCE to replace NULL with 0.
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name,
    COALESCE(SUM(o.amount), 0) AS total_amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name
ORDER BY total_amount DESC;


/* -------------------------------------------------------------
   5. Number of orders by customer

   Question:
   For each customer, count how many orders they placed.

   Important:
   - COUNT(*) would count the left-join row even when no order exists.
   - COUNT(o.order_id) counts only non-null order IDs.
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS n_orders
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name
ORDER BY n_orders DESC;


/* -------------------------------------------------------------
   6. Customers with total order amount >= 100

   Question:
   Return customers whose total order amount is at least 100.

   Important:
   - Filtering on aggregate result should use HAVING, not WHERE.
   ------------------------------------------------------------- */

SELECT
    c.customer_id,
    c.name,
    SUM(o.amount) AS total_amount
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name
HAVING SUM(o.amount) >= 100
ORDER BY total_amount DESC;


/* -------------------------------------------------------------
   7. LeetCode-style pattern: Customers Who Never Order

   Given:
   Customers(id, name)
   Orders(id, customerId)

   Expected pattern:
   SELECT name AS Customers
   FROM Customers c
   LEFT JOIN Orders o
       ON c.id = o.customerId
   WHERE o.id IS NULL;
   ------------------------------------------------------------- */
