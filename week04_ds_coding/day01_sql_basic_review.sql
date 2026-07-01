/*
Week 4 Day 1: SQL Basic Review

Goal:
- Practice SELECT, WHERE, ORDER BY, GROUP BY, HAVING.
- This file uses small toy tables so that each query is easy to reason about.

Main SQL patterns:
1. SELECT columns
2. WHERE row-level filtering
3. GROUP BY aggregation
4. HAVING group-level filtering
5. ORDER BY sorting result rows

Recommended LeetCode SQL 50 problems:
- Big Countries
- Recyclable and Low Fat Products
- Find Customer Referee
- Article Views I
- Invalid Tweets
*/

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS tweets;

CREATE TABLE users (
    user_id INTEGER,
    country VARCHAR(10),
    device VARCHAR(20),
    revenue INTEGER,
    active INTEGER,
    days_since_signup INTEGER
);

INSERT INTO users (user_id, country, device, revenue, active, days_since_signup) VALUES
(1, 'US', 'mobile', 100, 1, 3),
(2, 'US', 'desktop', 200, 1, 20),
(3, 'KR', 'mobile', 150, 0, 7),
(4, 'KR', 'desktop', 80, 1, 30),
(5, 'US', 'mobile', 50, 0, 2),
(6, 'KR', 'mobile', 120, 1, 10),
(7, 'CA', 'desktop', 300, 1, 15),
(8, 'CA', 'mobile', 40, 0, 1);

CREATE TABLE products (
    product_id INTEGER,
    low_fats VARCHAR(1),
    recyclable VARCHAR(1),
    category VARCHAR(20),
    price INTEGER
);

INSERT INTO products (product_id, low_fats, recyclable, category, price) VALUES
(1, 'Y', 'Y', 'food', 10),
(2, 'Y', 'N', 'food', 20),
(3, 'N', 'Y', 'home', 30),
(4, 'Y', 'Y', 'home', 40),
(5, 'N', 'N', 'tech', 100);

CREATE TABLE tweets (
    tweet_id INTEGER,
    content VARCHAR(200)
);

INSERT INTO tweets (tweet_id, content) VALUES
(1, 'short tweet'),
(2, 'this tweet is intentionally written to be much longer than fifteen characters'),
(3, 'hello'),
(4, 'another long tweet content');


/*
Task 1:
Return all active users.

Expected columns:
- user_id
- country
- device
- revenue

Hint:
- active = 1 means active.
- WHERE filters rows before grouping.
*/

-- Write your query here:
-- SELECT ...


/*
Task 2:
Return users with revenue >= 100 and days_since_signup <= 10.

Expected columns:
- user_id
- country
- revenue
- days_since_signup

Hint:
- Use AND.
*/

-- Write your query here:
-- SELECT ...


/*
Task 3:
Return total revenue by country.

Expected columns:
- country
- total_revenue
- n_users

Hint:
- Use GROUP BY country.
- COUNT(*) counts rows.
- SUM(revenue) sums revenue.
*/

-- Write your query here:
-- SELECT ...


/*
Task 4:
Return countries with total revenue >= 250.

Expected columns:
- country
- total_revenue

Hint:
- WHERE filters rows before grouping.
- HAVING filters groups after grouping.
- Since total_revenue is an aggregate, use HAVING.
*/

-- Write your query here:
-- SELECT ...


/*
Task 5:
Return product_id for products that are both low fat and recyclable.

This mirrors LeetCode:
- Recyclable and Low Fat Products

Expected columns:
- product_id

Hint:
- low_fats = 'Y'
- recyclable = 'Y'
*/

-- Write your query here:
-- SELECT ...


/*
Task 6:
Return tweets with content length greater than 15.

This mirrors LeetCode:
- Invalid Tweets

Expected columns:
- tweet_id

Hint:
- Many SQL engines support LENGTH(content).
*/

-- Write your query here:
-- SELECT ...


/*
Task 7:
Return average revenue by device, sorted by avg_revenue descending.

Expected columns:
- device
- avg_revenue
- n_users

Hint:
- AVG(revenue)
- GROUP BY device
- ORDER BY avg_revenue DESC
*/

-- Write your query here:
-- SELECT ...


/* -------------------------------------------------------------------
Sample answers
------------------------------------------------------------------- */

/* Solution 1 */
SELECT
    user_id,
    country,
    device,
    revenue
FROM users
WHERE active = 1;


/* Solution 2 */
SELECT
    user_id,
    country,
    revenue,
    days_since_signup
FROM users
WHERE revenue >= 100
  AND days_since_signup <= 10;


/* Solution 3 */
SELECT
    country,
    SUM(revenue) AS total_revenue,
    COUNT(*) AS n_users
FROM users
GROUP BY country;


/* Solution 4 */
SELECT
    country,
    SUM(revenue) AS total_revenue
FROM users
GROUP BY country
HAVING SUM(revenue) >= 250;


/* Solution 5 */
SELECT
    product_id
FROM products
WHERE low_fats = 'Y'
  AND recyclable = 'Y';


/* Solution 6 */
SELECT
    tweet_id
FROM tweets
WHERE LENGTH(content) > 15;


/* Solution 7 */
SELECT
    device,
    AVG(revenue) AS avg_revenue,
    COUNT(*) AS n_users
FROM users
GROUP BY device
ORDER BY avg_revenue DESC;