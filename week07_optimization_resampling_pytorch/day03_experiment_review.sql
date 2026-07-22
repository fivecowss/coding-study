/*
Problem:

The Signups table contains every registered user.
The Confirmations table contains zero or more confirmation events
for each user. Each event has action = 'confirmed' or action = 'timeout'.

Return every signup user and the proportion of that user's confirmation
events that were confirmed. Users without confirmation events must have
a confirmation rate of 0. Round the result to two decimal places.
*/

-- TODO: Start from Signups so every registered user is retained.
-- Left join the confirmation events, convert confirmed events to 1 and
-- all other outcomes to 0, average the indicator by user, and round it.
SELECT
    s.user_id,
    ROUND(
        AVG(
            CASE
                WHEN c.action = 'confirmed' THEN 1.0
                ELSE 0.0
            END
        ),
        2
    ) AS confirmation_rate
FROM Signups AS s
LEFT JOIN Confirmations AS c
    ON s.user_id = c.user_id
GROUP BY
    s.user_id;