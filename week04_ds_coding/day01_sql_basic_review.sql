
/* -------------------------------------------------------------
   0. Sample table setup
   ------------------------------------------------------------- */

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER,
    country VARCHAR(10),
    revenue INTEGER,
    active BOOLEAN,
    sessions INTEGER
);

INSERT INTO users (user_id, country, revenue, active, sessions) VALUES
    (1, 'US', 100, TRUE, 3),
    (2, 'US', 200, TRUE, 5),
    (3, 'KR', 150, FALSE, 2),
    (4, 'KR', 80, TRUE, 4),
    (5, 'US', 50, FALSE, 1),
    (6, 'KR', 120, TRUE, 6),
    (7, 'CA', 90, TRUE, 2),
    (8, 'CA', 300, FALSE, 7);


/* -------------------------------------------------------------
   1. SELECT all rows
   ------------------------------------------------------------- */

SELECT *
FROM users;


/* -------------------------------------------------------------
   2. Select specific columns

   Question:
   Return user_id, country, and revenue for all users.
   ------------------------------------------------------------- */

SELECT
    user_id,
    country,
    revenue
FROM users;


/* -------------------------------------------------------------
   3. WHERE filtering

   Question:
   Return only active users.
   ------------------------------------------------------------- */

SELECT *
FROM users
WHERE active = TRUE;


/* -------------------------------------------------------------
   4. Multiple WHERE conditions

   Question:
   Return users who are active and have revenue >= 100.

   Important:
   - SQL uses AND, OR, NOT.
   - This is different from pandas, where you use &, |, ~.
   ------------------------------------------------------------- */

SELECT *
FROM users
WHERE active = TRUE
  AND revenue >= 100;


/* -------------------------------------------------------------
   5. ORDER BY

   Question:
   Return all users sorted by revenue from highest to lowest.
   ------------------------------------------------------------- */

SELECT *
FROM users
ORDER BY revenue DESC;


/* -------------------------------------------------------------
   6. GROUP BY with aggregation

   Question:
   For each country, compute:
   - total_revenue
   - avg_revenue
   - n_users
   - avg_sessions
   ------------------------------------------------------------- */

SELECT
    country,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS avg_revenue,
    COUNT(*) AS n_users,
    AVG(sessions) AS avg_sessions
FROM users
GROUP BY country
ORDER BY total_revenue DESC;


/* -------------------------------------------------------------
   7. WHERE before GROUP BY

   Question:
   For active users only, compute total revenue by country.

   Flow:
   1. FROM users
   2. WHERE active = TRUE
   3. GROUP BY country
   4. SELECT country, SUM(revenue)
   5. ORDER BY total_revenue DESC
   ------------------------------------------------------------- */

SELECT
    country,
    SUM(revenue) AS active_total_revenue,
    COUNT(*) AS active_users
FROM users
WHERE active = TRUE
GROUP BY country
ORDER BY active_total_revenue DESC;


/* -------------------------------------------------------------
   8. HAVING after GROUP BY

   Question:
   Return countries with at least 2 users.

   Important:
   - WHERE filters rows before grouping.
   - HAVING filters groups after aggregation.
   ------------------------------------------------------------- */

SELECT
    country,
    COUNT(*) AS n_users
FROM users
GROUP BY country
HAVING COUNT(*) >= 2
ORDER BY n_users DESC;


/* -------------------------------------------------------------
   9. Practice version of LeetCode-style filtering

   Equivalent idea:
   Products table with columns:
   - product_id
   - low_fats
   - recyclable

   Question:
   Return product_id where low_fats = 'Y' and recyclable = 'Y'.
   ------------------------------------------------------------- */

DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INTEGER,
    low_fats VARCHAR(1),
    recyclable VARCHAR(1)
);

INSERT INTO products (product_id, low_fats, recyclable) VALUES
    (0, 'Y', 'N'),
    (1, 'Y', 'Y'),
    (2, 'N', 'Y'),
    (3, 'Y', 'Y'),
    (4, 'N', 'N');

SELECT
    product_id
FROM products
WHERE low_fats = 'Y'
  AND recyclable = 'Y';


