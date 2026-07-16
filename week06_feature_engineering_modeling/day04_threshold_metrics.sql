-- Day 4: Threshold Metrics in SQL

-- Goal:
-- Compute confusion matrix and precision/recall by threshold.

-- predictions table:
-- id
-- y_true
-- prob

WITH thresholds AS (
    SELECT 0.3 AS threshold
    UNION ALL SELECT 0.5
    UNION ALL SELECT 0.7
),
scored AS (
    SELECT
        -- TODO:
        -- threshold
        -- id
        -- y_true
        -- prob
        -- pred = 1 if prob >= threshold else 0
        t.threshold,
        p.id,
        p.y_true,
        p.prob,
        CASE
            WHEN p.prob >= t.threshold THEN 1
            ELSE 0
        END AS pred
    FROM predictions p
    CROSS JOIN thresholds t
),
confusion AS (
    SELECT
        threshold,

        -- TODO:
        -- tp
        -- fp
        -- tn
        -- fn
        threshold,
        SUM(CASE WHEN y_true = 0 AND pred = 1 THEN 1 ELSE 0 END) AS tp,
        SUM(CASE WHEN y_true = 1 AND pred = 1 THEN 1 ELSE 0 END) AS fp,
        SUM(CASE WHEN y_true = 0 AND pred = 0 THEN 1 ELSE 0 END) AS tn,
        SUM(CASE WHEN y_true = 1 AND pred = 0 THEN 1 ELSE 0 END) AS fn

    FROM scored
    GROUP BY threshold
),
metrics AS (
    SELECT
        threshold,
        tp,
        fp,
        tn,
        fn,

        -- TODO:
        -- precision = tp / (tp + fp)
        -- recall = tp / (tp + fn)
        -- f1 = 2 * precision * recall / (precision + recall)
        CASE
            WHEN tp + fp = 0 THEN 0.0
            ELSE 1.0 * tp / (tp + fp)
        END AS precision,

        CASE
            WHEN tp + fn = 0 THEN 0.0
            ELSE 1.0 * tp / (tp + fn)
        END AS recall

    FROM confusion
)
    SELECT
        threshold,
        tp,
        fp,
        tn,
        fn,
        precision,
        recall,
        CASE
            WHEN precision + recall = 0 THEN 0.0
            ELSE 2.0 * precision * recall / (precision + recall)
        END AS f1
    FROM metrics
    ORDER BY threshold;