-- Day 3: SQL Time-Series Metrics

-- Goal:
-- 1. Compare today's value with yesterday's value.
-- 2. Compute first activity date.
-- 3. Compute D1 retention.
-- 4. Compute rolling revenue.

-- ============================================================
-- Part 1: Rising Temperature style problem
-- ============================================================

-- weather table:
-- id
-- recordDate
-- temperature

-- TODO:
-- Return IDs where today's temperature is higher than yesterday's.

SELECT
    w_today.id
FROM weather w_today
JOIN weather w_yesterday
    ON w_today.recordDate = w_yesterday.recordDate + INTERVAL '1 day'
WHERE w_today.temperature > w_yesterday.temperature;


-- ============================================================
-- Part 2: First activity date
-- ============================================================

-- activity table:
-- player_id
-- event_date
-- games_played

-- TODO:
-- Return each player's first login date.

SELECT
    player_id,
    MIN(event_date) AS first_login
FROM activity
GROUP BY player_id;


-- ============================================================
-- Part 3: D1 retention
-- ============================================================

-- TODO:
-- Compute fraction of players who logged in again
-- exactly one day after their first login.

WITH first_login AS (
    SELECT
        player_id,
        MIN(event_date) AS first_login
    FROM activity
    GROUP BY player_id
),
next_day_login AS (
    SELECT DISTINCT
        f.player_id
    FROM first_login f
    JOIN activity a
        ON f.player_id = a.player_id
        AND a.event_date = f.first_login + INTERVAL '1 day'
)
SELECT
    ROUND(
        COUNT(n.player_id)::numeric / COUNT(f.player_id),
        2
    ) AS d1_retention
FROM first_login f
LEFT JOIN next_day_login n
    ON f.player_id = n.player_id
;


-- ============================================================
-- Part 4: Rolling 7-day revenue
-- ============================================================

-- orders table:
-- order_date
-- amount

-- TODO:
-- Compute daily revenue and rolling 7-day revenue.

WITH daily_revenue AS (
    SELECT
        ordet_date,
        SUM(amount) AS revenue
    FROM orders
    GROUP BY order_date
)
SELECT
    order_date,
    revenue,
    SUM(revenue) OVER(
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_revenue
FROM daily_revenue
ORDER BY order_date;