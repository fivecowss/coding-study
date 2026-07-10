-- week05_data_metrics_model_eval/day03_sql_window_functions.sql
--
-- Week 5 Day 3: retention, conversion, and SQL window functions
--
-- Goal:
-- - Practice first event date.
-- - Practice D1 retention.
-- - Practice conversion rate by treatment group.
-- - Practice ROW_NUMBER window function.
--
-- Suggested environment:
-- - DBeaver + SQLite

DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS experiment_assignments;

CREATE TABLE events (
    user_id INTEGER,
    event_date TEXT,
    event_type TEXT
);

CREATE TABLE experiment_assignments (
    user_id INTEGER,
    treatment_group TEXT,
    assigned_date TEXT
);

INSERT INTO events VALUES
(1, '2026-07-01', 'visit'),
(1, '2026-07-02', 'visit'),
(1, '2026-07-04', 'purchase'),
(2, '2026-07-01', 'visit'),
(2, '2026-07-03', 'purchase'),
(3, '2026-07-02', 'visit'),
(4, '2026-07-03', 'visit'),
(4, '2026-07-04', 'purchase'),
(5, '2026-07-04', 'visit'),
(6, '2026-07-01', 'visit'),
(6, '2026-07-02', 'visit');

INSERT INTO experiment_assignments VALUES
(1, 'control', '2026-07-01'),
(2, 'control', '2026-07-01'),
(3, 'treatment', '2026-07-02'),
(4, 'treatment', '2026-07-03'),
(5, 'control', '2026-07-04'),
(6, 'treatment', '2026-07-01');

-- Raw checks
SELECT * FROM events;
SELECT * FROM experiment_assignments;

-- --------------------------------------------------------------------
-- TODO 1:
-- Find each user's first event date.
--
-- Required columns:
-- - user_id
-- - first_event_date
-- --------------------------------------------------------------------

-- Your query here:
SELECT
    user_id,
    MIN(event_date) AS first_event_date
FROM events
GROUP BY user_id;

-- --------------------------------------------------------------------
-- TODO 2:
-- Add row_number to each event by user.
--
-- Required columns:
-- - user_id
-- - event_date
-- - event_type
-- - event_number
--
-- Hint:
-- ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_date)
-- --------------------------------------------------------------------

-- Your query here:
SELECT
    user_id,
    event_date,
    event_type,
    ROW_NUMBER() OVER (
        PARTITION BY user_id
        ORDER BY event_date
    ) AS event_number
FROM events
ORDER BY user_id, event_date;


-- --------------------------------------------------------------------
-- TODO 3:
-- Compute D1 retention by user.
--
-- Definition:
-- A user is D1 retained if they have an event exactly 1 day
-- after their first event.
--
-- SQLite hint:
-- julianday(event_date) - julianday(first_event_date) = 1
-- --------------------------------------------------------------------

-- Your query here:
WITH first_event AS (
    SELECT
        user_id,
        MIN(event_date) AS first_event_date
    FROM events
    GROUP BY user_id
),
evets_with_first AS (
    SELECT
        e.user_id,
        e.event_date,
        f.first_event_date,
        julianday(e.event_date) - julianday(f.first_event_date) AS days_since_first
    FROM events e
    LEFT JOIN first_event f
        ON e.user_id = f.user_id
),
user_d1 AS (
    SELECT
        user_id,
        MAX(CASE WHEN day_since_first = 1 THEN 1 ELSE 0) AS d1_retained
    FROM events_with_first
    GROUP BY user_id
)
SELECT
    AVG(d1_retained) AS d1_retention_rate
FROM user_d1;


-- --------------------------------------------------------------------
-- TODO 4:
-- Compute user-level conversion.
--
-- Definition:
-- converted = 1 if user has at least one purchase event.
--
-- Required columns:
-- - user_id
-- - converted
-- --------------------------------------------------------------------

-- Your query here:
SELECT
    user_id,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS converted
FROM events
GROUP BY user_id;

-- --------------------------------------------------------------------
-- TODO 5:
-- Compute conversion rate by treatment group.
--
-- Required columns:
-- - treatment_group
-- - n_users
-- - n_converted
-- - conversion_rate
--
-- All assigned users should be included.
-- --------------------------------------------------------------------

-- Your query here:
WITH user_conversion AS (
    SELECT
        user_id,
        MAX(CASE WHEN event_type = "purchase" THEN 1 ELSE 0 END) AS converted
    FROM events
    GROUP BY user_id
)
SELECT
    a.treatment_group,
    COUNT(DISTINCT a.user_id) AS n_users,
    SUM(COALESCE(u.converted, 0)) AS u_converted,
    AVG(COALESCE(u.converted, 0)) AS conversion_rate
FROM experiment_assignments a
LEFT JOIN user_conversion u
    ON a.user_id = u.user_id
GROUP BY a.treatment_group;


-- --------------------------------------------------------------------
-- SAMPLE ANSWER
-- --------------------------------------------------------------------

-- TODO 1 sample:
--
-- SELECT
--     user_id,
--     MIN(event_date) AS first_event_date
-- FROM events
-- GROUP BY user_id;

-- TODO 2 sample:
--
-- SELECT
--     user_id,
--     event_date,
--     event_type,
--     ROW_NUMBER() OVER (
--         PARTITION BY user_id
--         ORDER BY event_date
--     ) AS event_number
-- FROM events
-- ORDER BY user_id, event_date;

-- TODO 3 sample:
--
-- WITH first_event AS (
--     SELECT
--         user_id,
--         MIN(event_date) AS first_event_date
--     FROM events
--     GROUP BY user_id
-- ),
-- events_with_first AS (
--     SELECT
--         e.user_id,
--         e.event_date,
--         f.first_event_date,
--         julianday(e.event_date) - julianday(f.first_event_date) AS days_since_first
--     FROM events e
--     LEFT JOIN first_event f
--         ON e.user_id = f.user_id
-- ),
-- user_d1 AS (
--     SELECT
--         user_id,
--         MAX(CASE WHEN days_since_first = 1 THEN 1 ELSE 0 END) AS d1_retained
--     FROM events_with_first
--     GROUP BY user_id
-- )
-- SELECT
--     user_id,
--     d1_retained
-- FROM user_d1
-- ORDER BY user_id;

-- D1 retention rate sample:
--
-- WITH first_event AS (
--     SELECT
--         user_id,
--         MIN(event_date) AS first_event_date
--     FROM events
--     GROUP BY user_id
-- ),
-- events_with_first AS (
--     SELECT
--         e.user_id,
--         e.event_date,
--         f.first_event_date,
--         julianday(e.event_date) - julianday(f.first_event_date) AS days_since_first
--     FROM events e
--     LEFT JOIN first_event f
--         ON e.user_id = f.user_id
-- ),
-- user_d1 AS (
--     SELECT
--         user_id,
--         MAX(CASE WHEN days_since_first = 1 THEN 1 ELSE 0 END) AS d1_retained
--     FROM events_with_first
--     GROUP BY user_id
-- )
-- SELECT
--     AVG(d1_retained) AS d1_retention_rate
-- FROM user_d1;

-- TODO 4 sample:
--
-- SELECT
--     user_id,
--     MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS converted
-- FROM events
-- GROUP BY user_id;

-- TODO 5 sample:
--
-- WITH user_conversion AS (
--     SELECT
--         user_id,
--         MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS converted
--     FROM events
--     GROUP BY user_id
-- )
-- SELECT
--     a.treatment_group,
--     COUNT(DISTINCT a.user_id) AS n_users,
--     SUM(COALESCE(u.converted, 0)) AS n_converted,
--     AVG(COALESCE(u.converted, 0)) AS conversion_rate
-- FROM experiment_assignments a
-- LEFT JOIN user_conversion u
--     ON a.user_id = u.user_id
-- GROUP BY a.treatment_group;