-- TODO: Create a CTE that counts TP, TN, FP, and FN by segment.

WITH confusion_counts AS (
    SELECT
        segment,
        COUNT(*) AS n,
        SUM(
            CASE
                WHEN y_true = 1 AND y_pred = 1 THEN 1
                ELSE 0
            END
        ) AS tp,
        SUM(
            CASE
                WHEN y_true = 0 AND y_pred = 0 THEN 1
                ELSE 0
            END
        ) AS tn,
        SUM(
            CASE
                WHEN y_true = 0 AND y_pred = 1 THEN 1
                ELSE 0
            END
        ) AS fp,
        SUM(
            CASE
                WHEN y_true = 1 AND y_pred = 0 THEN 1
                ELSE 0 
            END
        ) AS fn
    FROM model_results
    GROUP BY segment
),
metrics AS (
    SELECT
    -- TODO: Return segment and sample size.
        segment,
        n,
    -- TODO: Calculate accuracy.
        1.0 * (tp + tn) / NULLIF(n, 0) AS accuracy,
        1.0 * tp / NULLIF(tp + fp, 0) AS precision,
        1.0 * tp / NULLIF(tp + fn, 0) AS recall
FROM confusion_counts
)
SELECT
    segment,
    n,
    accuracy,
    precision,
    recall,
    2.0 * precision * recall / NULLIF(precision + recall, 0) AS f1
FROM metrics
ORDER BY segment
;